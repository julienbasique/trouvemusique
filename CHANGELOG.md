# TrouveTaMusique — les versions

Chaque version est une copie complète qui marchait (code + base de sessions).
Copies dans `~/trouvemusique-versions/` — historique technique : dépôt git ici.
Nouvelle version : `scripts/nouvelle_version.sh <X.Y> "ce qui change"`.

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
