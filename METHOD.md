# Method

This file documents every number in `inputs.csv`, `scores.csv` and the mechanic flags in `apps.csv`. `score.py` recomputes every score from the inputs. Same formula for every product, no weights, no fixed positions, no exceptions.

## Score: plain mean of six signals

| # | Signal | Input columns | Formula |
|---|---|---|---|
| 1 | App Store rating | `rating_weighted` | stars × 20. Stars are the rating-count-weighted average across 24 App Store storefronts. No prior, no shrinkage. |
| 2 | Rating volume | `rating_count_total` | `min(100, max(0, 40 + 10·log10(N)))`, and 0 when N = 0. 100 ratings = 60, 1,000 = 70, 10,000 = 80, 100,000 = 90, 1,000,000+ = 100. |
| 3 | Newest reviews | `newest_reviews_avg`, `newest_reviews_n`, `cohort_median`, `integrity_penalty` | stars × 20 minus the integrity penalty (floored at 0), then pulled toward the cohort median with weight n ÷ (n + 50): 50 reviews count half, 500 count 91%. Cohort median is the median raw signal across ranked products with at least 10 reviews (67.36 in the 2026-09-18 run). |
| 4 | Freshness | `days_since_update` | 100 up to 30 days, then `100 × (1 − ((days − 30) ÷ 1065)^0.84)`, 0 at three years. Days counted from the current version's release date to the snapshot date 2026-09-18. |
| 5 | Documented features | `feature_checks_documented` | checks ÷ 9 × 100. The nine yes/no checks read from the App Store description: swipe and match, your own typed replies, memory, relationship consequences, rejection or loss, earned progression, voice messages, live voice calls, character creation. |
| 6 | Conversation quality | `quality_p`, `quality_m`, `quality_n`, `quality_neutral` | newest reviews about the conversation itself, coded positive, mixed or negative by two independent coders (one person, one language model from a different family, blind to app name and stars). Only agreed codes count. `q = (P + 0.5M + 1) ÷ (n + 2)`, × 100. Fewer than three agreed codes: neutral 50. |

Review integrity: confirmed reports of rewards for ratings or forced rating prompts reduce signal 3 by 10 points per 0.5% of that product's newest reviews, capped at 40. Reviews calling the ratings fake reduce it by 5 points per 0.5%, capped at 20. The applied value is `integrity_penalty`. Nothing else in the score is touched.

Not scored, only recorded: platforms, price, age rating, App Store search position.

## Storefronts and dates

Ratings and newest reviews were captured from 24 App Store storefronts between 2026-09-11 and 2026-09-17 and scored on 2026-09-18. The storefronts are United States, United Kingdom, Canada, Australia, Germany, Italy, Netherlands, Spain, Mexico, Türkiye, Sweden, Poland, Brazil, Japan, South Korea, India, Singapore, Indonesia, Philippines, Switzerland, Taiwan, Hong Kong, Argentina, Thailand. Only products with ratings in at least 10 storefronts are scored. Every product in `apps.csv` that is not in `inputs.csv` is unscored because it is not on the App Store or did not meet that floor.

## Mechanic flags in apps.csv

Eight flags, each `true` only when the product's own store listing or website says so in words. The sentence that justifies each `true` is quoted in `notes`. Nothing is inferred from screenshots, reviews or hands-on use. A sentence that denies a mechanic, such as "zero ghosting", does not count. Detection is a keyword pass over the listing text followed by a manual read of every match, and the patterns are published in the build tooling of the awesome list repository.

| Flag | What counts |
|---|---|
| `meter` | A named relationship, trust, affection or bond score that moves during conversation. |
| `message_scoring` | The product states that your messages are evaluated or rated and that this changes the relationship. |
| `ghost` | Characters can stop replying as a consequence of what you send. |
| `fail_state` | A character can end the relationship permanently: block, leave for good, be lost. |
| `progression` | Levels, milestones or stages that unlock as the relationship develops. This replaces "progressive difficulty" from the awesome list glossary because difficulty scaling is documented by a single product and a one-check column would say nothing. |
| `proactive` | The character messages first, follows up or checks in on its own. |
| `availability` | The character has online and offline hours or is sometimes unavailable. |
| `memory` | Details from earlier sessions come back without being restated, or the listing describes a memory system. |

`platforms` lists every platform the product ships on as of `last_checked`, verified against the US App Store, Google Play (US) and the product's own site. Platform count is not a signal anywhere in this dataset.

## Categories

`simulator` means you meet and court several characters through a match or roster flow and the relationship has a state that can progress, stall or fail. `companion` means one ongoing character relationship with persistent state and no failure state. `character_chat` means a roster or user-made characters, romance optional, with no relationship progression system. The category is read from the product's own description. When the description fits two categories, the narrower one is used only if a failure or progression mechanic is documented.

## Scope

Work safe. Products whose main draw is explicit content are not in the dataset. Wingman and reply-generator apps are not in the dataset because they do not simulate a conversation partner.

## Challenges

Challenge any number by opening an issue with the listing text or the storefront data that contradicts it. Corrections are logged in the commit history rather than silently edited.
