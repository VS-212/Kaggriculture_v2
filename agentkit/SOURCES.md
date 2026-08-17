# SOURCES.md — источники

## Соревнование
- https://www.kaggle.com/competitions/kaggriculture (overview / rules / discussion / leaderboard)
- Правила: 5 сабмитов/день, активны 2 последних, no ingress/egress в эпизоде,
  победители открывают код (CC-BY 4.0).

## Движок (источник истины)
- PyPI: `kaggle-environments` (локально установлен, v1.32.7)
- GitHub: https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture
- Локальная копия: `env/kaggriculture.py` (1086 строк), `env/README-engine.md`, `env/AGENTS-engine.md`

## Данные
- Ежедневные топ-реплеи (IL/RL): https://www.kaggle.com/datasets/kaggle/kaggriculture-episodes-index
- Реплеи/логи своих эпизодов: `kaggle competitions replay|logs <episode_id>` (CLI)

## Форум (ключевые треды)
- Баланс-патчи: discussion/733431, discussion/735311 (пины организаторов)
- Self-play PPO: discussion/734952 · Расхождения доков и движка: discussion/732450
- Discord и «как начать»: discussion/730708

## MCP Kaggle (конвейер интела, не память)
- https://github.com/54yyyu/kaggle-mcp
- Galaxy-Dawn Kaggle-MCP: https://mcpmarket.com/server/kaggle-5
- Официальный CLI (использует наш пайплайн): `pip install kaggle`

## Академия
- Lux AI S3 (NeurIPS 2024): https://openreview.net/pdf?id=7t8kWYbOcj
- MLE-bench (OpenAI, ICLR 2025): https://arxiv.org/abs/2410.07095
- Agent K: https://arxiv.org/abs/2411.03562
- Память агентов: Letta/MemGPT, Mem0 (arXiv:2504.19413), A-MEM (arXiv:2502.12110),
  GraphRAG (arXiv:2404.16130), обзор zylos.ai (2026)

## Сборники решений Kaggle (для сверки подходов в Simulations)
- https://farid.one/kaggle-solutions/
