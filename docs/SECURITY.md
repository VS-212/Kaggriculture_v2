# SECURITY.md — как хранить Kaggle API-ключ, чтобы агент его не видел

## Принцип
**Код репозитория никогда не читает и не печатает секрет.**
Токен читает только официальный Kaggle CLI из стандартного места
**вне репозитория** (`~/.kaggle/`). Наш пайплайн (`scripts/pipeline.py`)
просто запускает CLI подпроцессом — в его командах секретов нет.

## Настройка (делает только человек, один раз)
1. Kaggle → Settings → API → **Generate New Token** (или token string для access_token).
2. Положите файл ВНЕ репозитория (варианты, любой):
   - `~/.kaggle/access_token` — одна строка-токен (рекомендовано организаторами), или
   - `~/.kaggle/kaggle.json` — `{"username":"...","key":"..."}`.
3. Права: `chmod 600 ~/.kaggle/access_token`.
4. Всё. Больше ничего нигде указывать не нужно — CLI найдёт файл сам.

Чего делать НЕ надо: класть токен в репозиторий, в `.env` внутри репозитория,
в переменные окружения оболочки агента, в чат.

## Три рубежа защиты
1. **`.gitignore`** — `kaggle.json`, `access_token`, `.env*` и т.п. игнорируются
   (даже случайный `git add .` их не подхватит).
2. **pre-commit хук** (`scripts/install-git-guard.sh` → `scripts/scan-secrets.sh`) —
   блокирует коммит, если в staged-файлах есть имена секретов или паттерны токенов.
3. **Дисциплина пайплайна** — `pipeline.py` не логирует секреты; его команды
   (submit/monitor/intel/replays) содержат только публичные идентификаторы.

## Использование пайплайна
```bash
# проверить авторизацию (печатает только статус, без токена)
scripts/pipeline.py auth-check

# репетиция сабмита без сети (не нужен ключ): сборка + smoke-тест + размер
.venv/bin/python scripts/pipeline.py submit --agent agents/baseline.py --message "v0" --dry-run

# реальный сабмит
.venv/bin/python scripts/pipeline.py submit --agent agents/baseline.py --message "v0"

# статус и эпизоды / лидерборд и топ-реплеи / скачать свой реплей
.venv/bin/python scripts/pipeline.py monitor --submission-id <ID>
.venv/bin/python scripts/pipeline.py intel
.venv/bin/python scripts/pipeline.py replays --episode-id <ID>
```

## Ротация и проверка
- Скомпрометирован? Kaggle → Settings → API → Expire All Tokens → новый токен в тот же файл.
- Проверка рубежа: `bash scripts/scan-secrets.sh /tmp/test/kaggle.json` → должен вернуть
  код 1 и «SECRET-БЛОК». Файл-приманку держать в /tmp, не в репозитории.
