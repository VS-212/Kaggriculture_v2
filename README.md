# Kaggriculture — Farming Agent

An autonomous agent for the [Kaggle Kaggriculture](https://www.kaggle.com/competitions/kaggriculture/overview) simulation competition: a two-player, turn-based farming game where the winner is whoever has the most coins in the bank after a 30-day (720-turn) season.

## Strategy summary

**Animals are the money makers.** The core of the strategy is a diversified herd — `COW → MILK`, `SHEEP → WOOL`, `GOOSE → EGG` — that is **sized to the town's shop draw**. Shops are drawn *with replacement* each game (observable in `town.unlocked_shops`), which determines how much of each product the town will actually consume. The agent estimates the expected season-end demand for each product and sizes its herd to a target share of that demand, so a draw with no milk shops doesn't bankrupt a milk-only farm.

Key mechanics exploited:

- **CARE + FEED doubles production.** Feeding daily (wheat) and caring daily banks a bonus that pays out on the next production day — roughly `1.5 milk/day` per cow, `1.33 wool/day` per sheep, `2 eggs/day` per goose.
- **Fertilizer is free money.** Every animal drops one fertilizer per day; it's collected and sold (no town demand, but still worth $60–100 early).
- **Wheat is grown *and* bought.** A 12-tile wheat field supplies most animal feed; the rest is topped up from the market, keeping a 3-day reserve so animals never escape.
- **Price-impact-aware selling.** Sell slots are ordered most-contested product first (milk before wool before fertilizer) so the goods with the most town demand sell at the best price.
- **Demand-aware crop diversification.** Strawberries (4 town shops) and carrots (fast turnover) are planted as secondary cash crops; this keeps the farm profitable even in draws where animal-product demand is poor.
- **Robust labor scheduling.** The farmer plus up to 6 hands are assigned greedily: feeders pick up a batch of wheat and feed nearest-first, workers do care / collect / harvest / water / plant by priority. Watering and feeding are treated as mandatory daily maintenance.
- **Cash buffer.** A reserve is kept so the farm never runs out of money for feed mid-season (avoids the "death spiral" where animals escape and revenue collapses).

## Files

- `main.py` — the submitted agent (`agent(obs)` entry point, stdlib only).
- `test_agent.py` — local benchmark harness (runs `main.agent` against `starter`, `random`, `pass`, and itself).

## Test locally

```bash
python -m venv .venv
.venv/bin/pip install -U kaggle-environments
.venv/bin/python test_agent.py          # benchmarks vs starter/random/self/pass
```

## Local results (25 seeds, seeds 1000–1024)

| Opponent | Result | Avg final bank |
| --- | --- | --- |
| `pass`   | 25/25 wins | ~$39k (max ~$53k) |
| `starter`| 25/25 wins | ~$37k |
| `random` | 25/25 wins | ~$27k |
| self-play| ~symmetric | ~$25k each |

## Submit

A submission is a single `main.py` with an `agent` function at the root:

```bash
pip install kaggle
kaggle competitions submit kaggriculture -f main.py -m "demand-adaptive herd v1"
```

You must accept the competition rules and configure Kaggle credentials
(`~/.kaggle/access_token` or `KAGGLE_API_TOKEN`) first.

## Next ideas (not yet implemented)

- Per-product market-timing (meter low-shop-count goods into small lots).
- Opponent-herd-aware share sizing (currently fixed demand share).
- Precomputed / lower-movement labor routes to cut walking overhead.
- Fertilizing strawberries/melons to double their yield.
