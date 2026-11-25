"""Le moteur à poids : réponses du quiz -> scores par style + POURQUOI.

100 % déterministe : aucune boîte noire. Chaque option du questionnaire
additionne des points sur certains styles ; on cite les réponses qui ont
le plus pesé pour que l'utilisateur comprenne la proposition.
"""

from .questions import QUESTIONS, NOMS

# styles "instrumentaux" de référence (la préférence de langue ne les exclut pas)
INSTRUMENTAUX = {"classique", "lofi", "cinema", "techno"}


def calculer_scores(reponses: dict) -> tuple[dict, dict]:
    """reponses {id_question: id_option} -> (scores {style: float}, raisons {style: str})."""
    scores = {cle: 0.0 for cle in NOMS}
    apports = {}          # style -> max points venus d'UNE réponse (pour les raisons)
    sources = {}          # style -> libellé de la réponse qui a le plus pesé
    for q in QUESTIONS:
        if q.get("type") == "texte":
            continue
        valeur = reponses.get(q["id"])
        if not valeur:
            continue
        option = next((o for o in q["options"] if o["id"] == valeur), None)
        if not option:
            continue
        for style, points in option["points"].items():
            scores[style] = scores.get(style, 0.0) + points
            if points > apports.get(style, 0):
                apports[style] = points
                sources[style] = option["libelle"]
    return scores, {"apports": apports, "sources": sources}


def top_styles(scores: dict, gains: dict | None = None, k: int = 5) -> list[dict]:
    """Retourne les k meilleurs styles, ordre décroissant."""
    total = dict(scores)
    for cle, points in (gains or {}).items():
        total[cle] = total.get(cle, 0.0) + points
    tries = sorted(total.items(), key=lambda x: -x[1])
    retenus = [(cle, s) for cle, s in tries[:k] if s > 0.5]
    if not retenus:                      # aucune affinité forte : on ouvre 3 mondes
        retenus = [("electro", 1.0), ("rap_fr", 1.0), ("lofi", 1.0)]
    premier = retenus[0][1] or 1.0
    return [
        {
            "cle": cle,
            "nom": NOMS.get(cle, cle),
            "points": round(s, 1),
        }
        for cle, s in retenus
    ]


def raisons_pour(gains: dict | None, sources: dict, styles: list[dict]) -> list[str]:
    """Phrases de justification, style : « because réponse → style »."""
    lignes = []
    g = gains or {}
    for s in styles:
        cle = s["cle"]
        motif = sources.get(cle)
        if cle in g:
            lignes.append(f"tu as cité un artiste qui colle au {s['nom']}")
        elif motif:
            lignes.append(f"{motif} → {s['nom']}")
    return lignes[:3]


# décennies autorisées selon la réponse "epoque"
ERAS = {
    "80s_90s": {"1970", "1980", "1990", "classic"},
    "2000s": {"1990", "2000", "classic"},
    "frais": {"2000", "classic"},
    "peu_importe": None,        # tout
}


def decades_autorisees(epoque: str | None) -> set[str] | None:
    return ERAS.get(epoque)
