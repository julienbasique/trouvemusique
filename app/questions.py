"""Le questionnaire — chaque réponse AJOUTE des points à certains styles.

Principe : transparent et rapide. Une question, des options, et pour
chaque option un dico de points (style -> points, points négatifs possibles).
Le style gagnant sortira du total ; l'explication cite les réponses qui
ont pesé le plus (moteur.py les re-calcul).
"""

QUESTIONS = [
    {
        "id": "son",
        "question": "Ce que tu préfères entendre DANS la musique ?",
        "options": [
            {"id": "guitare", "libelle": "🎸 Guitare qui déchire",
             "points": {"rock_classique": 3, "punk": 2, "metal": 2, "indie": 2}},
            {"id": "piano_voix", "libelle": "🎹 Piano, voix, mélodies",
             "points": {"chanson_fr": 3, "jazz": 2, "rnb": 2, "classique": 2, "pop": 1}},
            {"id": "son_electronique", "libelle": "🔊 Sons électroniques, synthés",
             "points": {"electro": 3, "techno": 2, "lofi": 2, "variete_80s": 2, "cinema": 1}},
            {"id": "beat", "libelle": "🥁 Un bon beat, du rythme parlé",
             "points": {"rap_fr": 3, "rap_us": 3, "rnb": 1, "electro": 1}},
            {"id": "cuivre", "libelle": "🎺 Cornes, cuivres, groove",
             "points": {"funk": 3, "jazz": 2, "latino": 2, "blues": 2}},
        ],
    },
    {
        "id": "energie",
        "question": "Tu veux une musique pour… ?",
        "options": [
            {"id": "danser", "libelle": "💃 Bouger et danser",
             "points": {"electro": 2, "funk": 2, "latino": 2, "rap_fr": 1.5, "pop": 1}},
            {"id": "secouer", "libelle": "🤘 Secouer la tête fort",
             "points": {"metal": 3, "punk": 2, "rock_classique": 2}},
            {"id": "chill", "libelle": "🛋️ Chill, tranquille, fond sonore",
             "points": {"lofi": 3, "jazz": 2, "blues": 1.5, "classique": 1.5, "chanson_fr": 1}},
            {"id": "puissance", "libelle": "💪 Te sentir puissant",
             "points": {"metal": 2, "rap_us": 2, "cinema": 2, "electro": 1}},
            {"id": "roadtrip", "libelle": "🚗 Au volant, fenêtres ouvertes",
             "points": {"rock_classique": 2, "rap_fr": 2, "electro": 1.5, "variete_80s": 1.5}},
        ],
    },
    {
        "id": "epoque",
        "question": "L'époque qui te parle le plus ?",
        "options": [
            {"id": "80s_90s", "libelle": "📻 Années 80-90",
             "points": {"variete_80s": 3, "rock_classique": 1.5, "rnb": 1.5, "funk": 1.5}},
            {"id": "2000s", "libelle": "📼 Années 2000",
             "points": {"rap_fr": 2, "metal": 1.5, "reggae": 1, "indie": 1.5}},
            {"id": "frais", "libelle": "🆕 Dernières sorties",
             "points": {"rap_fr": 2, "indie": 2, "electro": 1.5, "pop": 1.5}},
            {"id": "peu_importe", "libelle": "🗂️ Peu importe, je veux découvrir",
             "points": {}},   # +0 partout : moteur ajoute un léger bonus découverte
        ],
    },
    {
        "id": "langue",
        "question": "Les paroles, en quelle langue principalement ?",
        "options": [
            {"id": "francais", "libelle": "🇫🇷 En français",
             "points": {"rap_fr": 2.5, "chanson_fr": 2.5, "variete_80s": 1.5}},
            {"id": "anglais", "libelle": "🇬🇧 En anglais",
             "points": {"rock_classique": 1.5, "rap_us": 2, "pop": 1.5, "metal": 1.5,
                        "electro": 1.5, "indie": 1.5, "jazz": 1, "blues": 1}},
            {"id": "fous", "libelle": "🌍 Peu importe, surprends-moi",
             "points": {},      # bonus découverte géré par le moteur
        },
        ],
    },
    {
        "id": "ambiance",
        "question": "Et pour quelle occasion tu écoutes le plus ?",
        "options": [
            {"id": "apero", "libelle": "🍻 L'apéro entre amis",
             "points": {"funk": 2, "latino": 2, "pop": 1.5, "variete_80s": 1.5, "reggae": 1}},
            {"id": "concentration", "libelle": "🎯 Le travail, concentré",
             "points": {"classique": 3, "lofi": 3, "cinema": 2, "jazz": 1}},
            {"id": "triste", "libelle": "🌧️ Pensif, écrire/rêver",
             "points": {"chanson_fr": 2, "jazz": 2, "blues": 2, "indie": 1.5}},
            {"id": "sport", "libelle": "🏋️ Le sport, la motivation",
             "points": {"metal": 2, "rap_us": 2, "electro": 2}},
        ],
    },
    {
        "id": "voix",
        "question": "Dans les voix, tu préfères ?",
        "options": [
            {"id": "masculine", "libelle": "🗣️ Voix masculine",
             "points": {"rap_fr": 1, "rap_us": 1, "rock_classique": 1, "metal": 1}},
            {"id": "feminine", "libelle": "🎙️ Voix féminine",
             "points": {"pop": 1.5, "jazz": 1.5, "rnb": 1.5, "chanson_fr": 1}},
            {"id": "instrumental", "libelle": "🎺 Sans voix (instrumental)",
             "points": {"classique": 2.5, "lofi": 2, "cinema": 2, "techno": 2}},
            {"id": "voix_peu", "libelle": "🔀 Les deux, ou peu importe",
             "points": {}},
        ],
    },
    {
        "id": "artiste",
        "question": "Un artiste que tu aimes déjà (c'est un indice en or) ?",
        "type": "texte",
        "placeholder": "Ex. : Daft Punk, NTM, Queen… (laisse vide si tu ne sais pas)",
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
