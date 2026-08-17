# Kaggriculture v2 — агент для Kaggle Kaggriculture

Соревнование: https://www.kaggle.com/competitions/kaggriculture (1v1 симуляция фермы,
720 ходов, рейтинг + финал по Брэдли-Терри, $50k призовых).

## Структура
- `agents/` — агенты (baseline.py = v0, жадный пшеничный фермер)
- `eval.py` — локальный харнесс: `.venv/bin/python eval.py --a agents/baseline.py --b starter --games 50`
- `env/` — исходник движка (источник истины по механикам)
- `docs/` — память проекта: `brain.md` (ядро, всегда в контексте), `todo.md`,
  `lessons.md` (журнал уроков), `research/` (исследования и планы), отчёты фаз
- `docs/competition/` — проверенный снимок скрытых Rules, runtime-лимитов,
  лицензий и balance patches (актуальность: 2026-08-17)
- `competition-data/` — два официальных файла со вкладки Kaggle Data
- `data/` — реплеи и датасеты (в git не хранится)

## Установка
```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Как работает цикл
1. Гипотеза → правка агента в `agents/`.
2. Локальная проверка: eval.py против starter/предыдущих версий (50+ партий).
3. Сабмит (≤5/день, активны 2 последних) → рейтинг на лестнице.
4. Анализ реплеев (своих + ежедневный датасет топ-эпизодов) → выводы в docs/, новый цикл.

## Ключевые ограничения (из правил)
- `actTimeout=1` сек/ход и общий overage-bank 60 сек; no ingress/egress во время
  эпизода → в сабмите только автономный код, без вызовов LLM/API.
- 100 MiB; 8 GiB HDD; 6.5 GiB RAM; 1.6 vCPU; `main.py` с `agent` в корне.
- Приватный обмен competition code/data вне официальной команды запрещён.
- Победители обязаны открыть код (CC-BY 4.0) и дать воспроизводимое описание.
- Полный аудит: [`docs/competition/rules-audit.md`](docs/competition/rules-audit.md).
