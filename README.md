# The Investor Brain

The research brain behind an AI-agent-run investment research company. It tests every way people try to grow money (index funds, cash, gold, property, trading cards, LEGO, watches and more) on one honest scale, after every cost.

Private while the brand is being finalised.

## What lives here

| Folder | Contents | Status |
|---|---|---|
| `docs/` | Methodology, house rules, agent instructions | Methodology v0.1 drafted |
| `dossiers/` | One structured file per asset class | Planned |
| `costs/` | Cost models that turn headline returns into what an investor keeps | Planned |
| `data/` | DuckDB warehouse and pipelines (market data, evidence log, Signal Room) | Planned |
| `signal-room/` | Content research: watchlist, outlier scoring, teardowns, weekly brief | Planned |
| `lab/` | Strategy Lab: pre-registered paper strategies and results | Planned |

## Naming

| Level | Name | Covers |
|---|---|---|
| Company, app, channels, subscription | Asset Theory | The overall brand across every surface. |
| Evidence library | Research | Studies, methods, sources, findings. |
| Comparison feature and video series | Asset Autopsy | "Compare assets" — the feature and the video series deliberately share this name. |
| Strategy testing area | Strategy Lab | Pre-registered paper-portfolio testing, per `docs/methodology.md` section 9. |
| Asset-class rating feature | Asset Scorecard | Rates asset types (never individual securities) on fixed, descriptive, historical factors — see `docs/scorecard-method.md` and `docs/products.md`. |
| Portfolio description feature | Portfolio X-ray | Describes a user's own holdings by cost, concentration, currency exposure and historical outcome ranges — never rates, ranks or recommends. See `docs/products.md`. |

"Asset Theory" is the confirmed working name, subject to trademark, company and domain checks.

## Ground rules

- Every published number has an entry in the evidence log. See `docs/methodology.md`.
- Research and education only. Nothing in this repo tells anyone what to buy, sell or hold.
- Never commit secrets. API keys live in GitHub Actions secrets (for example `YOUTUBE_API_KEY`) or in a local `.env` file, which git ignores.
