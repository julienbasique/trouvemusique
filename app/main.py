"""TrouveTaMusique — API FastAPI.

Routes :
    GET  /api/questions   le questionnaire (sans les poids)
    POST /api/resultat    réponses -> styles + pistes jouables
    POST /api/retour      j'aime / j'aime pas -> pistes raffinées
    GET  /                l'interface
"""

import random
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from . import db, deezer
from .questions import NOMS, QUESTIONS
from .moteur import (calculer_scores, decades_autorisees, raisons_pour,
                     top_styles)

BASE = Path(__file__).resolve().parent.parent
app = FastAPI(title="TrouveTaMusique", version="2.0.0")
db.init_db()

INSTRUMENTAUX = {"classique", "lofi", "cinema", "techno"}   # échappent à la langue
CLE_STYLES = list(NOMS.keys())

# Sur un hébergement nuage (Render…) le serveur Ollama local n'existe pas :
# IA_ARTISTE=0 coupe le classement IA d'artistes (repli : leurs titres seuls).
IA_ARTISTE = os.environ.get("IA_ARTISTE", "1") not in ("0", "false", "non")


def _gains_artiste(nom_artiste: str, raisons: list) -> tuple[dict, dict | None]:
    """Bonus de style via l'artiste cité (+ ses titres en ancre)."""
    artists = deezer.chercher_artiste(nom_artiste)
    if not artists:
        return {}, None
    nom_propre = artists["nom"]
    from .genres import STYLES
    cible = None
    for cle, config in STYLES.items():
        for seed_nom, _langue, _era in config["seeds"]:
            if seed_nom.lower() == nom_propre.lower():
                cible = cle
                break
        if cible:
            break
    if not cible and IA_ARTISTE:
        cible = deezer.genre_depuis_nom(nom_propre, CLE_STYLES)
    gains = {}
    if cible:
        gains[cible] = 3.0
        raisons.append(f"« {nom_propre} » rime avec le style {NOMS.get(cible, cible)}")
    else:
        raisons.append(f"« {nom_propre} » : on part de ses titres à lui")
    return gains, artists


@app.get("/api/questions")
def questions():
    """Le questionnaire sans révéler les poids."""
    prop = []
    for q in QUESTIONS:
        if q.get("type") == "texte":
            prop.append({"id": q["id"], "question": q["question"],
                         "type": "texte", "placeholder": q.get("placeholder", "")})
            continue
        prop.append({
            "id": q["id"], "question": q["question"],
            "options": [{"id": o["id"], "libelle": o["libelle"]} for o in q["options"]],
        })
    return {"questions": prop}


def _dedupe(pistes: list) -> list:
    """Supprime les doublons (artiste — titre) en gardant l'ordre (ancre d'abord)."""
    vus_cles = set()
    uniques = []
    for p in pistes:
        cle = (p["artiste"] + " — " + p["titre"]).lower()
        if cle in vus_cles:
            continue
        vus_cles.add(cle)
        uniques.append(p)
    return uniques


@app.post("/api/resultat")
def resultat(reponses: dict = {}):
    """Réponses du quiz -> session, styles, pistes."""
    reponses = reponses or {}
    nom_artiste = (reponses.get("artiste") or "").strip()
    raisons = []
    gains, artists = _gains_artiste(nom_artiste, raisons) if nom_artiste else ({}, None)
    scores, _ = calculer_scores(reponses)
    styles = top_styles(scores, gains, k=5)
    langue = reponses.get("langue")
    eras = decades_autorisees(reponses.get("epoque"))
    pistes = (deezer.titres_pour_styles(styles[:3], langue, eras, INSTRUMENTAUX, vus=set(), par_style=4)
              + deezer.titres_pour_styles(styles[3:5], langue, eras, INSTRUMENTAUX, vus=set(), par_style=2))
    if artists and gains:                     # l'ancre en tête de liste
        cible = next(iter(gains), None)
        ancre = deezer.top_titres(artists["id"], n=2)
        for p in ancre:
            p["style_cle"] = cible or ""
            p["style_nom"] = NOMS.get(cible, "Ton artiste") if cible else "Ton artiste"
        pistes = ancre + [p for p in pistes if p["artiste"] != artists["nom"]]
    elif artists:
        ancre = deezer.top_titres(artists["id"], n=3)
        for p in ancre:
            p["style_cle"] = ""
            p["style_nom"] = "Ton artiste"
        pistes = ancre + pistes
    pistes = _dedupe(pistes)
    sid = db.nouvelle_session(
        {k: v for k, v in reponses.items() if k != "artiste"},
        gains, {k: v + (gains.get(k) or 0) for k, v in scores.items()}, [], )
    vus = [f"{p['artiste']} — {p['titre']}".lower() for p in pistes]
    db.maj_retours(sid, [], vus)
    return {
        "session_id": sid,
        "styles": styles,
        "raisons": raisons,
        "pistes": pistes,
        "ancre": artists,
    }


@app.post("/api/retour")
def retour(payload: dict):
    """j'aime / j'aime pas sur des titres -> recommandations RÉAJUSTÉES."""
    sid = payload.get("session_id")
    artiste = payload.get("artiste")
    action = payload.get("action")          # "aime" | "pas"
    style = payload.get("style_cle")
    session = db.lire(sid)
    if not session or not artiste or action not in ("aime", "pas"):
        raise HTTPException(400, "retour incomplet")
    retours = session["retours"] + [{"artiste": artiste, "action": action,
                                     "titre": payload.get("titre", "")}]
    scores = dict(session["scores"])
    if style:
        scores[style] = scores.get(style, 0.0) + (1.5 if action == "aime" else -2.0)
    db.maj_retours(sid, retours, session["vus"])
    styles = top_styles(scores, k=5)
    pistes = (deezer.titres_pour_styles(styles[:3], session["reponses"].get("langue"),
              decades_autorisees(session["reponses"].get("epoque")),
              INSTRUMENTAUX, vus=set(session["vus"]), par_style=4)
              + deezer.titres_pour_styles(styles[3:5], session["reponses"].get("langue"),
              decades_autorisees(session["reponses"].get("epoque")),
              INSTRUMENTAUX, vus=set(session["vus"]), par_style=2))
    nouvelles = [f"{p['artiste']} — {p['titre']}".lower() for p in pistes]
    db.maj_retours(sid, retours, list(set(session["vus"]) | set(nouvelles)))
    return {"styles": styles, "pistes": pistes,
            "note": "raffinées d'après tes retours"}


app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")


@app.get("/", include_in_schema=False)
def racine():
    return FileResponse(BASE / "static" / "index.html")
