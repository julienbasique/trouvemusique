# TrouveTaMusique — les versions

Chaque version est une copie complète qui marchait (code + base de sessions).
Copies dans `~/trouvemusique-versions/` — historique technique : dépôt git ici.
Nouvelle version : `scripts/nouvelle_version.sh <X.Y> "ce qui change"`.

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
