# TrouveTaMusique

Ton style musical, trouvé par le quiz et pas par la chance.

**Le concept** : tu réponds à 7 questions (son préféré, énergie, époque,
langue, ambiance, voix + un artiste que tu aimes) → l'app calcule tes
3 styles les plus proches avec un pourcentage d'affinité et LE POURQUOI
→ puis elle sort de **vrais titres** (les tubes des artistes de ces
styles) que tu écoutes en un clic (extraits de 30 s, bouton ▶).

**L'affinage** : sur chaque titre, 👍 / 👎 recalcule tes styles et
propose d'autres pistes — à force, la boîte apprend ce que tu aimes
(sessions mémorisées dans data/).

## Comment ça marche

```
quiz ──► app/questions.py   7 questions; chaque option ajoute des points
      ──► app/moteur.py     scores par style (transparent, zéro boîte noire),
                            top 3 + pourcentage + explications
      ──► app/genres.py     20 styles + artistes « semences » tagués
                            (langue, décennie) — leurs TOPS Deezer = les pistes
      ──► app/deezer.py     API Deezer publique (gratuite, sans compte) :
                            top titres + extrait 30 s jouable ;
                            IA (nuage déjà installé) en appoint pour classer
                            un artiste inconnu — repli discret sans elle
      ──► app/main.py       API FastAPI + sert l'interface
      ──► app/db.py         sessions + retours (SQLite)
```

## Démarrer

```bash
./run.sh                 # puis ouvrir http://localhost:8020
```

Ou l'icône de bureau « TrouveTaMusique » (1 clic, ouvre le navigateur).
Depuis le téléphone : `http://100.113.18.49:8020` (par Tailscale, réseau
déjà en place).

## Versions

- Une version archivée après chaque vérification : `~/trouvemusique-versions/`
- Journal : `CHANGELOG.md`

## Limites assumées (v1.0)

- Extraits limités à 30 s (extrait d'écoute, pas la chanson complète) —
  le lien « entier ↗ » ouvre le titre sur Deezer.
- Les artistes semences sont un choix curé : pour un style très pointu
  (metal extrême, rap underground…), le top peut paraître « grand public ».
- L'IA nuage sert UNIQUEMENT à classer un artiste cité ; si elle est
  indisponible, l'app marche pareil (sans cette aide).
