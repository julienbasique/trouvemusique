"""Les 20 styles + les artistes SEMENCES (curés à la main, tagués).

Chaque style a une liste de (nom_artiste, langue, décennie). L'app tire les
titres directement du top Deezer DE CES artistes — ce sont leurs plus gros
titres, donc des pistes de qualité (pas une recherche aveugle par mot-clé).
La langue/decade des graines sert à FILTRER selon les réponses du quiz.
"""

STYLES = {
    "rock_classique": {
        "seeds": [
            ("Queen", "en", "1970"), ("AC/DC", "en", "1980"),
            ("Led Zeppelin", "en", "1970"), ("Dire Straits", "en", "1980"),
            ("Téléphone", "fr", "1980"), ("U2", "en", "1980"),
            ("The Rolling Stones", "en", "1970"),
        ],
    },
    "metal": {
        "seeds": [
            ("Metallica", "en", "1980"), ("Iron Maiden", "en", "1980"),
            ("Rammstein", "de", "1990"), ("Linkin Park", "en", "2000"),
            ("Slipknot", "en", "2000"),
        ],
    },
    "punk": {
        "seeds": [
            ("The Clash", "en", "1980"), ("Sex Pistols", "en", "1970"),
            ("Ramones", "en", "1970"), ("Noir Désir", "fr", "1990"),
            ("Green Day", "en", "1990"),
        ],
    },
    "indie": {
        "seeds": [
            ("Arctic Monkeys", "en", "2000"), ("Phoenix", "fr", "2000"),
            ("Gorillaz", "en", "2000"), ("Imagine Dragons", "en", "2000"),
            ("Twenty One Pilots", "en", "2000"), ("Stromae", "fr", "2000"),
        ],
    },
    "pop": {
        "seeds": [
            ("Michael Jackson", "en", "1980"), ("ABBA", "en", "1970"),
            ("Beyoncé", "en", "2000"), ("Dua Lipa", "en", "2000"),
            ("Bruno Mars", "en", "2000"), ("Rihanna", "en", "2000"),
        ],
    },
    "electro": {
        "seeds": [
            ("Daft Punk", "fr", "1990"), ("David Guetta", "fr", "2000"),
            ("Avicii", "en", "2000"), ("Calvin Harris", "en", "2000"),
            ("Deadmau5", "en", "2000"),
        ],
    },
    "techno": {
        "seeds": [
            ("Kraftwerk", "de", "1970"), ("Laurent Garnier", "fr", "1990"),
            ("The Prodigy", "en", "1990"), ("Fatboy Slim", "en", "1990"),
        ],
    },
    "rap_fr": {
        "seeds": [
            ("IAM", "fr", "1990"), ("Suprême NTM", "fr", "1990"),
            ("MC Solaar", "fr", "1990"), ("Orelsan", "fr", "2000"),
            ("PNL", "fr", "2000"), ("Booba", "fr", "2000"),
            ("Soprano", "fr", "2000"),
        ],
    },
    "rap_us": {
        "seeds": [
            ("Eminem", "en", "2000"), ("2Pac", "en", "1990"),
            ("The Notorious B.I.G.", "en", "1990"), ("Kanye West", "en", "2000"),
            ("Dr. Dre", "en", "1990"),
        ],
    },
    "rnb": {
        "seeds": [
            ("Marvin Gaye", "en", "1970"), ("Amy Winehouse", "en", "2000"),
            ("Usher", "en", "2000"), ("Alicia Keys", "en", "2000"),
            ("Jorja Smith", "en", "2000"),
        ],
    },
    "funk": {
        "seeds": [
            ("Earth, Wind & Fire", "en", "1970"), ("Chic", "en", "1970"),
            ("Jamiroquai", "en", "1990"), ("Boney M.", "en", "1970"),
        ],
    },
    "chanson_fr": {
        "seeds": [
            ("Georges Brassens", "fr", "1970"), ("Jacques Brel", "fr", "1970"),
            ("Jean-Jacques Goldman", "fr", "1980"), ("Francis Cabrel", "fr", "1980"),
            ("Zazie", "fr", "1990"), ("Édith Piaf", "fr", "1950"),
        ],
    },
    "variete_80s": {
        "seeds": [
            ("Indochine", "fr", "1980"), ("Dalida", "fr", "1980"),
            ("Michel Sardou", "fr", "1980"), ("Depeche Mode", "en", "1980"),
            ("A-ha", "en", "1980"), ("The Cure", "en", "1980"),
        ],
    },
    "jazz": {
        "seeds": [
            ("Miles Davis", "en", "1970"), ("Louis Armstrong", "en", "1970"),
            ("Nina Simone", "en", "1970"), ("Ella Fitzgerald", "en", "1970"),
            ("Madeleine Peyroux", "en", "2000"),
        ],
    },
    "blues": {
        "seeds": [
            ("B.B. King", "en", "1970"), ("Muddy Waters", "en", "1970"),
            ("John Lee Hooker", "en", "1970"), ("Gary Moore", "en", "1980"),
        ],
    },
    "reggae": {
        "seeds": [
            ("Bob Marley & The Wailers", "en", "1970"),
            ("Tiken Jah Fakoly", "fr", "2000"), ("Alborosie", "en", "2000"),
            ("Mellow mood", "en", "2000"),
        ],
    },
    "latino": {
        "seeds": [
            ("Gipsy Kings", "fr", "1990"), ("Shakira", "es", "2000"),
            ("Daddy Yankee", "es", "2000"), ("Rosalía", "es", "2000"),
        ],
    },
    "classique": {
        "seeds": [
            ("Mozart", "en", "classic"), ("Vivaldi", "en", "classic"),
            ("Debussy", "fr", "classic"), ("Ludovico Einaudi", "en", "2000"),
        ],
    },
    "cinema": {
        "seeds": [
            ("Hans Zimmer", "en", "2000"), ("Ennio Morricone", "en", "1970"),
            ("John Williams", "en", "1980"), ("Yann Tiersen", "fr", "2000"),
        ],
    },
    "lofi": {
        # pas d'artiste star : on passe par une recherche directe d'ambiance
        "recherche": "lofi chill beats",
        "seeds": [],
    },
}
