"""Le questionnaire — léger, jamais intrusif : des goûts et des lieux de vie,
PAS de questions personnelles (leçon v1.1→v1.2 : « trop perso » interdit —
pas d'identité, pas de souvenirs intimes, pas d'humeur mentale).

Une option = dico de points (style -> points). L'ancre « artiste » reste.
"""

QUESTIONS = [
    {
        "id": "weekend",
        "question": "Un weekend idéal pour toi, c'est plutôt ?",
        "options": [
            {"id": "dehors", "libelle": "Dehors, bouger, marcher, voir du pays",
             "points": {"rock_classique": 1.5, "electro": 1.5, "indie": 1.5, "reggae": 1}},
            {"id": "mains", "libelle": "Faire des trucs de ses mains",
             "points": {"lofi": 2, "jazz": 1.5, "blues": 1.5, "chanson_fr": 1}},
            {"id": "sortie", "libelle": "Une sortie, du monde autour",
             "points": {"funk": 2, "latino": 2, "pop": 1.5, "electro": 1}},
            {"id": "poser", "libelle": "Rien de prévu, se poser tranquille",
             "points": {"lofi": 2, "classique": 1.5, "rnb": 1.5, "jazz": 1}},
        ],
    },
    {
        "id": "endroit",
        "question": "Un endroit où tu te sens tout de suite bien ?",
        "options": [
            {"id": "eau", "libelle": "Au bord de l'eau, une rivière ou la mer",
             "points": {"reggae": 2, "electro": 1.5, "indie": 1.5, "funk": 1}},
            {"id": "haut", "libelle": "En hauteur : colline, montagne, la vue",
             "points": {"rock_classique": 2, "indie": 1.5, "cinema": 1.5}},
            {"id": "comptoir", "libelle": "Au comptoir ou à la table d'un resto",
             "points": {"latino": 2, "funk": 1.5, "chanson_fr": 1.5, "jazz": 1}},
            {"id": "maison", "libelle": "Chez toi, au chaud, rien à demander",
             "points": {"lofi": 2, "classique": 1.5, "rnb": 1.5, "jazz": 1}},
        ],
    },
    {
        "id": "soiree",
        "question": "Ta soirée type, si tu en choisis une ?",
        "options": [
            {"id": "petit_comite", "libelle": "Petit comité, la discussion qui traîne",
             "points": {"jazz": 2, "chanson_fr": 2, "blues": 1.5}},
            {"id": "danser", "libelle": "Une soirée à danser, fort",
             "points": {"electro": 2, "latino": 2, "pop": 1.5, "rap_fr": 1.5}},
            {"id": "repas", "libelle": "Un bon repas qui dure des heures",
             "points": {"chanson_fr": 2, "funk": 1.5, "variete_80s": 1.5, "latino": 1}},
            {"id": "pas_fete", "libelle": "Pas trop la fête, autre chose ?",
             "points": {"lofi": 2, "blues": 1.5, "classique": 1.5, "cinema": 1}},
        ],
    },
    {
        "id": "route",
        "question": "Sur la route ou en balade, tu mets quoi ?",
        "options": [
            {"id": "radio", "libelle": "La radio qui tourne, on n'y touche pas",
             "points": {"variete_80s": 1.5, "pop": 1.5, "chanson_fr": 1}},
            {"id": "tape", "libelle": "Une playlist de vieux morceaux sûrs",
             "points": {"rock_classique": 2, "funk": 1.5, "variete_80s": 1.5}},
            {"id": "ton_son", "libelle": "Ton son du moment, à fond",
             "points": {"rap_fr": 2, "electro": 2, "metal": 1.5}},
            {"id": "calme", "libelle": "Le calme, juste le moteur et la route",
             "points": {"lofi": 2, "classique": 2, "jazz": 1.5}},
        ],
    },
    {
        "id": "moment",
        "question": "Le moment de la journée qui te plaît le plus ?",
        "options": [
            {"id": "matin", "libelle": "Le matin, tout est encore à faire",
             "points": {"jazz": 1.5, "indie": 1.5, "pop": 1, "lofi": 1}},
            {"id": "apresmidi", "libelle": "L'après-midi, la journée qui roule",
             "points": {"rock_classique": 1.5, "latino": 1.5, "pop": 1.5}},
            {"id": "soir", "libelle": "Le soir, la lumière qui baisse",
             "points": {"chanson_fr": 1.5, "jazz": 1.5, "blues": 1.5, "lofi": 1}},
            {"id": "nuit", "libelle": "La nuit, quand tout le monde dort",
             "points": {"electro": 2, "techno": 1.5, "cinema": 1.5, "lofi": 1.5}},
        ],
    },
    {
        "id": "voix",
        "question": "Dans les voix, tu préfères ?",
        "options": [
            {"id": "masculine", "libelle": "Une voix masculine",
             "points": {"rap_fr": 1, "rap_us": 1, "rock_classique": 1, "metal": 1}},
            {"id": "feminine", "libelle": "Une voix féminine",
             "points": {"pop": 1.5, "jazz": 1.5, "rnb": 1.5, "chanson_fr": 1}},
            {"id": "instrumental", "libelle": "Pas de voix — juste l'instru",
             "points": {"classique": 2.5, "lofi": 2, "cinema": 2, "techno": 2}},
            {"id": "voix_peu", "libelle": "Les deux, ou peu importe",
             "points": {}},
        ],
    },
    {
        "id": "artiste",
        "question": "Un artiste que tu aimes déjà (indice en or, pas obligatoire) ?",
        "type": "texte",
        "placeholder": "Ex. : NTM, Dire Straits, Zaz… (tu peux laisser vide)",
    },
]

# Les styles gagnants sont présentés dans cet ordre de score décroissant.
NOMS = {
    "rock_classique": "Rock",
    "metal": "Métal",
    "punk": "Punk",
    "indie": "Indie / Alternatif",
    "pop": "Pop",
    "electro": "Électro / Dance",
    "techno": "Techno",
    "rap_fr": "Rap français",
    "rap_us": "Rap US",
    "rnb": "R&B / Soul",
    "funk": "Funk / Disco",
    "chanson_fr": "Chanson française",
    "variete_80s": "Variété & Années 80",
    "jazz": "Jazz",
    "blues": "Blues",
    "reggae": "Reggae / Dub",
    "latino": "Latino / Salsa",
    "classique": "Classique",
    "cinema": "Musique de film",
    "lofi": "Lo-fi / Chill",
}
