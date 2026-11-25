"""Les PISTES réelles : API publique Deezer (gratuite, sans compte).

- /search/artist?q=...     -> id d'artiste
- /artist/{id}/top?limit=3 -> ses plus gros titres, avec `preview` (30 s, mp3)

Les recommandations sortent du TOP des artistes semences des styles gagnants :
des tubes, pas des pistes aléatoires. L'IA (moteur nuage déjà en place sur la
machine) sert d'appoint : classer un artiste INCONNU dans nos styles — avec
repli discret si elle est indisponible.
"""

import random
import time

import requests

BASE = "https://api.deezer.com"
_MEMO: dict[str, tuple[float, object]] = {}      # cache 10 min (moins d'appels)
_MEMO_TTL = 600

OLLLAMA_URL = "http://localhost:11434"
MODELES_CLOUD = ["glm-5.3-flash:cloud"]


def _cache_get(cle):
    memo = _MEMO.get(cle)
    if memo and time.time() - memo[0] < _MEMO_TTL:
        return memo[1]
    return None


def _cache_set(cle, valeur):
    _MEMO[cle] = (time.time(), valeur)
    return valeur


def chercher_artiste(nom: str) -> dict | None:
    """{id, nom, lien, image} ou None si introuvable/indispo."""
    cle = "art:" + (nom or "").strip().lower()
    if len(cle) <= 6:
        return None
    memo = _cache_get(cle)
    if memo is not None:
        return memo
    try:
        r = requests.get(f"{BASE}/search/artist",
                         params={"q": nom, "limit": 1}, timeout=8)
        data = r.json().get("data") or []
        if not data:
            return None
        a = data[0]
        return _cache_set(cle, {
            "id": a["id"], "nom": a["name"], "lien": a["link"],
            "image": a.get("picture_medium", ""),
        })
    except Exception:
        return None


def top_titres(artiste_id, n: int = 3) -> list[dict]:
    memo = _cache_get(f"top:{artiste_id}:{n}")
    if memo is not None:
        return memo
    try:
        r = requests.get(f"{BASE}/artist/{artiste_id}/top",
                         params={"limit": n}, timeout=8)
        data = r.json().get("data") or []
    except Exception:
        data = []
    pistes = []
    for t in data:
        if not t.get("preview"):
            continue
        pistes.append({
            "titre": t["title"],
            "artiste": t["artist"]["name"],
            "album": t["album"]["title"],
            "preview": t["preview"],
            "lien": t.get("link", ""),
            "image": t.get("album", {}).get("cover_medium", ""),
        })
    return _cache_set(f"top:{artiste_id}:{n}", pistes)


def recherche_directe(requete: str, n: int = 4) -> list[dict]:
    """Titres par mots-clés (repli pour les styles sans artiste star)."""
    memo = _cache_get(f"q:{requete}:{n}")
    if memo is not None:
        return memo
    try:
        r = requests.get(f"{BASE}/search/track",
                         params={"q": requete, "limit": n}, timeout=8)
        data = r.json().get("data") or []
    except Exception:
        data = []
    pistes = []
    for t in data:
        if not t.get("preview"):
            continue
        pistes.append({
            "titre": t["title"],
            "artiste": t["artist"]["name"],
            "album": t["album"]["title"],
            "preview": t["preview"],
            "lien": t.get("link", ""),
            "image": t.get("album", {}).get("cover_medium", ""),
        })
    return _cache_set(f"q:{requete}:{n}", pistes)


def _langue_ok(langue_seed: str, langue: str | None, genre: str,
               instrumentaux: set[str]) -> bool:
    if langue in (None, "", "fous"):
        return True
    if genre in instrumentaux:
        return True
    if langue == "francais":
        return langue_seed == "fr"
    if langue == "anglais":
        return langue_seed != "fr"
    return True


def deja_vues(piste: dict, vus: set[str]) -> bool:
    cle = (piste["artiste"] + " — " + piste["titre"]).lower()
    return cle in vus


def titres_pour_styles(styles, langue, eras, instrumentaux, vus, par_style=4):
    """Pistes variées par style : semences curées D'ABORD, bibliothèque
    Deezer complète en remplissage (le pool ne se vide plus jamais)."""
    from .genres import STYLES, DEEZER_QUERIES
    resultats = []
    for s in styles:
        cle = s["cle"]
        config = STYLES.get(cle, {})
        graines = config.get("seeds", [])
        if eras is not None:
            filtrees = [g for g in graines if g[2] in eras]
            if filtrees:
                graines = filtrees
        eligibles = [g for g in graines
                     if _langue_ok(g[1], langue, cle, instrumentaux)]
        if not eligibles:
            eligibles = graines
        random.shuffle(eligibles)
        prises = 0
        for nom, _langue, _era in eligibles:
            if prises >= par_style:
                break
            artiste = chercher_artiste(nom)
            if not artiste:
                continue
            for piste in top_titres(artiste["id"], n=6):
                if deja_vues(piste, vus):
                    continue
                enrichi = dict(piste)
                enrichi["style_cle"] = cle
                enrichi["style_nom"] = s["nom"]
                resultats.append(enrichi)
                prises += 1
                break            # 1 titre par artiste : de la variété
        # REMPLISSAGE : toute la bibliothèque Deezer (recherche par genre)
        besoin = par_style - prises
        if besoin > 0:
            recherche = DEEZER_QUERIES.get(cle)
            if recherche:
                for piste in titres_bibliotheque(recherche, vus, besoin):
                    enrichi = dict(piste)
                    enrichi["style_cle"] = cle
                    enrichi["style_nom"] = s["nom"]
                    resultats.append(enrichi)
                    prises += 1
        if prises == 0 and config.get("recherche"):
            for piste in recherche_directe(config["recherche"], n=par_style):
                enrichi = dict(piste)
                enrichi["style_cle"] = cle
                enrichi["style_nom"] = s["nom"]
                resultats.append(enrichi)
    return resultats


def titres_bibliotheque(recherche: str, vus: set, limite: int) -> list[dict]:
    """Pioche des titres DANS TOUTE la bibliothèque Deezer (hors semences).

    Un index aléatoire par appel : deux sessions ne sortent jamais les
    mêmes ; on filtre sur l'existence du preview de 30 s et sur les
    morceaux déjà vus.
    """
    import time as _temps
    memo = _cache_get("bib:" + recherche)
    if memo is not None:
        pioche = list(memo)
    else:
        try:
            r = requests.get(f"{BASE}/search/track", params={
                "q": recherche, "limit": 45, "index": 0}, timeout=10)
            data = r.json().get("data") or []
        except Exception:
            data = []
        pioche = [t for t in data if t.get("preview")]
        _cache_set("bib:" + recherche, pioche)
    if not pioche:
        return []
    random.shuffle(pioche)
    rendus = []
    for t in pioche:
        if len(rendus) >= limite:
            break
        if not t.get("preview"):
            continue
        piste = {
            "titre": t["title"],
            "artiste": t["artist"]["name"],
            "album": t["album"]["title"],
            "preview": t["preview"],
            "lien": t.get("link", ""),
            "image": t.get("album", {}).get("cover_medium", ""),
        }
        if deja_vues(piste, vus):
            continue
        rendus.append(piste)
    return rendus


def genre_depuis_nom(nom_artiste: str, cles_valides: list) -> str | None:
    """Appoint IA : classe un artiste inconnu dans notre vocabulaire de styles."""
    noms = ", ".join(cles_valides)
    for modele in MODELES_CLOUD:
        try:
            r = requests.post(OLLLAMA_URL + "/api/chat", json={
                "model": modele, "stream": False, "think": False,
                "messages": [{
                    "role": "user",
                    "content":
                        f"Style musical de l'artiste « {nom_artiste} » ? Réponds UNIQUEMENT "
                        f"avec une seule clé, exactement l'une de : {noms} — au plus proche "
                        "du style. Aucun autre texte.",
                }],
                "options": {"num_predict": 30},
            }, timeout=12)
            contenu = (r.json().get("message", {}).get("content") or "").strip()
            for cle in cles_valides:
                if cle in contenu:
                    return cle
        except Exception:
            continue
    return None          # IA indispo : l'app reste fonctionnelle sans elle
