# AI dating simulator and companion app data

Open data behind [Awesome AI Dating Simulators](https://github.com/ai-dating-simulators/awesome-ai-dating-simulators).

One row per product across iOS, Android and web. For each product: the platforms it ships on, the relationship mechanics its own store listing documents (with the sentence quoted), store ratings with capture dates, and a six-signal score that `score.py` recomputes from the published inputs.

## Snapshot 2026-09-18

| Measure | Value |
|---|---|
| Products | 63 (4 dating simulators, 15 companions, 44 character chat platforms) |
| Platform coverage | 52 on iOS, 40 on Android, 28 on the web. 18 products ship on all three, 21 on two, 24 on one. |
| Mechanic flags | 8 per product, 504 cells, 23 true. 15 products document at least one mechanic in their listing. |
| Scored products | 48 (App Store products with ratings in at least 10 of 24 storefronts) |
| Capture window | App Store data 2026-09-11 to 2026-09-17, platform and web checks 2026-09-18 |

## Files

| File | Rows | What it is |
|---|---|---|
| `apps.csv`, `apps.json` | 63 | Category, platforms, store and web URLs, developer, eight mechanic flags with the listing sentence for each, pricing, ratings. |
| `inputs.csv` | 48 | The raw inputs behind the score: weighted rating, rating count, newest-review average and count, cohort median, integrity penalty, days since update, feature checks, quality codes. |
| `scores.csv` | 48 | Output of `score.py`: six signals and their mean, sorted by score. |
| `score.py` | | Recomputes `scores.csv` from `inputs.csv`. Python 3 standard library, no dependencies. |
| `METHOD.md` | | Every formula, every flag definition, storefront list, exclusions. |

## Reproduce

```
python3 score.py
git diff --exit-code scores.csv
```

The second command exits 0 when the recomputed file is byte-identical to the committed one.

## How to read apps.csv

- `category` is `simulator`, `companion` or `character_chat`. Definitions and the assignment rule are in METHOD.md.
- `platforms` joins `ios`, `android` and `web` with a semicolon character. A platform is listed only when the store page or web app was opened on the check date. Platform count enters no score.
- The mechanic columns `meter`, `message_scoring`, `ghost`, `fail_state`, `progression`, `proactive`, `availability`, `memory` are `true` only when the product's own listing states the mechanic. `notes` quotes the sentence. `false` means the listing does not describe it, which is not the same as the product lacking it.
- `ios_rating` is the rating-count-weighted average across the 24 storefronts. `android_rating` and `android_installs` are read from the US Google Play page.
- `last_checked` is the date the row was verified.

## What this dataset does not measure

- Behaviour in use. Every flag comes from listing text, not from running the product.
- Google Play ratings outside the US storefront.
- Products whose main draw is explicit content. They are excluded by scope, not scored low.
- Web-only products have no store ratings and are therefore unscored.

## Update cadence

Store data is refreshed monthly and `last_checked` on every row says when. Mechanic flags change only when a listing changes. A pull request that flips a flag must add the new listing sentence to `notes`.


## License

CC0 1.0. Use the data and cite the repo if you can.
