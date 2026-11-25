# TrouveTaMusique — les versions

Chaque version est une copie complète qui marchait (code + base de sessions).
Copies dans `~/trouvemusique-versions/` — historique technique : dépôt git ici.
Nouvelle version : `scripts/nouvelle_version.sh <X.Y> "ce qui change"`.

## v2.1 — 25 novembre 2026 (vendredi)

L'application devient interactive et fluide (demande de Julien) :

- **Écran d'attente vivant** pendant la recherche (points qui dansent + « on
  fouille 24 styles ») — plus de page qui disparaît en blanc.
- **Touche 1 à 6 au clavier** pour répondre, avec le numéro affiché dans
  chaque option ; petit temps de confirmation au clic avant de passer.
- **Pistes qui glissent en douceur** à l'apparition (décalage en cascade).
- **Barre de progression jaune** sous le titre joué (les 30 s se voient),
  ligne surlignée, bouton ❚❚.
- **Le son ne se coupe plus** quand on raffine avec 👍/👎 (le lecteur est
  global, la lignée en lecture se retrouve toute seule).
- **Toasts** : les messages (« raffiné d'après ton retour ») glissent en bas
  et se retirnent seuls ; gestion d'erreur propre si le réseau blesse.

## v2.0 — 25 novembre 2026 (jeudi soir, toujours)

**Prêt pour le nuage** (« faire tourner sans ton PC ») :

- La même app, déployable gratuitement chez Render (plan offert, pas de
  carte) juste en connectant le dépôt GitHub : fichier render.yaml qui
  dit à l'hébergeur quoi construire, port lu automatiquement, données
  sessions incluses.
- L'IA qui classe un artiste inconnu est désactivable par variable
  (IA_ARTISTE=0 chez l'hébergeur — pas d'Ollama à disposition) : le repli
  existe déjà, l'app marche pareil, juste sans cette aide.
- Ton PC reste la version locale (icône de bureau) ; BrocScan lui est
  indispensable sur le PC d'une autre façon (modèles + Chrome + données).

## v1.9 — 25 novembre 2026 (jeudi soir, encore)

Diversifié et adapté (demande de Julien : « il en existe plein ! ») :

- **Le catalogue passe à 24 styles** : ajout du **Folk & Country** (Dylan,
  Cash…), de la **K-pop** (BTS, BLACKPINK, NewJeans), de l'**Afro & Zouk**
  (Kassav', Magic System, Fally Ipupa), de la **Musette & Accordéon**
  (Tiersen, Caravan Palace — le genre brocante) — branchés sur les
  réponses (le punch tropical → afro, le téléphone → K-pop, le concert
  du village → musette…).
- **L'écran final montre 5 styles** (au lieu de 3) : le n°1 en gros, les
  4 suivants dessous ; les pistes restent en profondeur sur les 3 gros,
  allégées sur les 2 suivants.
- Vérifié sur 3 profils opposés (fête / calme / brocante) : 5 styles
  adaptés chacun, 16 pistes jouables par profil, aucun doublon.

## v1.8 — 25 novembre 2026 (jeudi soir)

Répartition demandée : **5 questions sur 15, sur la musique** —

- L'instrument que tu aurais joué, le volume parfait, est-ce que tu chantes
  (+ les 2 existantes : le son qui accroche, la voix) — ce sont les 5
  questions musicales, placées en fin de quiz.
- Les 10 autres restent des goûts de vie légers (weekend, endroit, soirée,
  boisson, gadgets, concert, avec qui, route, moment). Enlevé au passage :
  le transport, le film, le resto, le sport (qui faisaient doublons).
- Toujours 6 options par question (5 sur le volume), l'artiste à la fin.

## v1.6 — 25 novembre 2026 (soir, encore)

- **Plus de choix partout** : chaque question passe à 6 options (la mer
  dans le weekend, le punch tropical, la pétanque du café, le grec du
  soir, « je démonte tout », le concert du casino du village…).
- **Nouvel écran final, comme demandé** : à GAUCHE le petit bloc
  « CE QUE TU AIMES » écrit en gros (le style n°1 en très gros jaune, les
  suivants en moyenne) ; à DROITE la GROSSE CASE qui prend toute la place
  avec toutes les pistes (pochettes, bouton 30 s, 👍/👎). Sur téléphone,
  ça s'empile proprement.

## v1.5 — 25 novembre 2026 (après-midi)

- Licence MIT ajoutée à l'app (le dépôt reste public et signé du nom de Julien).

## v1.4 — 25 novembre 2026 (après-midi)

- **Publication sur GitHub** : https://github.com/julienbasique/trouvemusique
  (public, les données de sessions de Julien EXCLUES du dépôt par .gitignore).

## v1.3 — 25 novembre 2026 (soir, encore)

Taille et aération (demande de Julien) :

- **15 questions** : les 6 de vie + 8 nouvelles, toutes légères (la boisson
  pour traîner, le transport, le film du soir, le resto, le sport, les
  gadgets, le concert idéal, avec qui écouter — le tout sans intrusif).
- **Le site s'élargit et respire** : page passée de 720 à 960 px, options
  en 2 colonnes plus larges, pochettes plus grosses, espaces entre les
  pistes, titre de question plus grand. Toujours organisé — testé en réel :
  profil « festival + bière + nuit » → Électro, Rap français, Latino,
  12 pistes toutes jouables, aucun doublon.

## v1.2 — 25 novembre 2026 (soir)

Retour de Julien : v1.1 allait « trop perso ». Le quiz repart du bon côté :

- Plus AUCUNE question qui sonde l'intérieur (identité, souvenirs d'enfance,
  humeur mentale, quartier) — remplacées par des goûts LÉGERS : le weekend
  idéal, l'endroit où on se sent bien, ta soirée type, ce qu'on met sur la
  route, le moment de la journée préféré (+ voix & artiste).
- 7 questions au total, toutes de bon goût, aucune gênante — testé : la
  personne « bricolage du dimanche + vieux morceaux sûrs + soir » reçoit
  Jazz, Lo-fi, Chanson française.

## v1.1 — 25 novembre 2026 (fin d'après-midi)

Deux retours de Julien appliqués :

- **Le quiz parle de la PERSONNE d'abord** (« la musique, c'est une façon
  d'être ») : comment tu te vois, où tu viens, un son d'enfance, le bruit
  parfait, ton petit moment, ton humeur des derniers jours — la musique se
  déduit de QUI tu es (2 questions musicales gardées). Mesuré : réponses
  « tranquille + campagne + radio de la cuisine » → Chanson française,
  Jazz, Lo-fi (Piaf, Brel, Brassens, Cabrel).
- **Zéro émoji + plus de dashboard** : les gros pourcentages et les grosses
  cartes font IA — remplacés par des chips sobres, la 1re marquée
  « le plus proche ». Et l'accent passe du violet au **jaune** (boutons et
  touches jaunes sur le fond sombre conservé).

## v1.0 — 25 novembre 2026

Première version complète, vérifiée en direct :

- Quiz de 7 questions (son, énergie, époque, langue, ambiance, voix, artiste)
- Moteur de points transparent : top 3 styles + pourcentage + justification
- Vrais titres depuis Deezer (gratuit, sans compte) avec extraits 30 s ▶
- 20 styles, ~65 artistes semences tagués langue/époque
- Raffinement : 👍/👎 recalcule les styles et sort d'autres pistes
- L'IA nuage classe un artiste inconnu (repli discret si indispo)
- Icône de bureau + lanceur ; accessible du téléphone (100.113.18.49:8020)
- Tests réels : quiz → 10 pistes toutes jouables, 0 doublon, raffinage OK
