# SOURCES.md — источники

## Соревнование
- https://www.kaggle.com/competitions/kaggriculture (overview / rules / discussion / leaderboard)
- Локальный аудит на 2026-08-17: `docs/competition/README.md`,
  `docs/competition/rules-audit.md`, `docs/competition/official-rules-extract.md`.
- Скрытые условия: 5 сабмитов/день, до 2 финальных (Overview: последние 2),
  no ingress/egress, команда ≤5, запрет приватного sharing вне команды,
  winner code CC-BY 4.0 + воспроизводимое описание.
- Runtime: `actTimeout=1`, общий overage-bank 60 сек; 100 MiB, 8 GiB HDD,
  6.5 GiB RAM, 1.6 vCPU.

## Движок (источник истины)
- PyPI: `kaggle-environments` (локально установлен, v1.32.7)
- GitHub: https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture
- Официальный Data-пакет: `competition-data/README.md`,
  `competition-data/AGENTS.md`.
- Локальная копия движка: `env/kaggriculture.py` (1086 строк),
  `env/kaggriculture.json`; прежние копии docs: `env/README-engine.md`,
  `env/AGENTS-engine.md`.
- Все файлы побайтово сверены 2026-08-17 с upstream commit
  `28b6d8af3ce73926b3d0fda1410c1ddd8384ab8c`; хеши: `docs/competition/SHA256SUMS`.

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
