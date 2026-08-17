# Kaggriculture: локальный снимок официального контента

Дата проверки: **2026-08-17 (UTC)**.

Этот каталог отвечает на два разных вопроса:

1. какие файлы и описание окружения нужны для разработки агента;
2. какие обязательные условия находятся не только на вкладке Overview, но и в
   раскрывающихся Official / Foundational Rules, FAQ и официальных объявлениях.

## Что уже загружено в репозиторий

На вкладке Kaggle Data сейчас опубликованы ровно два файла (40.53 kB, Apache 2.0):
`README.md` и `AGENTS.md`. Их локальные копии уже находятся здесь:

| Официальный файл | Локальная копия | SHA-256 |
|---|---|---|
| `README.md` | [`../../competition-data/README.md`](../../competition-data/README.md) | `3081e52baf8eb2da5d861acc63a3636ce29425f6bdb79a67036ba234ac4ade00` |
| `AGENTS.md` | [`../../competition-data/AGENTS.md`](../../competition-data/AGENTS.md) | `e1a80501a7b02a212eaac9370ada4129a64e0ee6cb3cbc790f3d77d22863fe22` |

В `env/README-engine.md` и `env/AGENTS-engine.md` остались идентичные прежние
копии. Оригинальные имена в `competition-data/` сохранены, чтобы внутренние
ссылки официального пакета работали без изменений.

Кроме них сохранены файлы фактического окружения — источник истины по механике:

| Файл | Локальная копия | SHA-256 |
|---|---|---|
| `kaggriculture.py` | [`../../env/kaggriculture.py`](../../env/kaggriculture.py) | `bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e` |
| `kaggriculture.json` | [`../../env/kaggriculture.json`](../../env/kaggriculture.json) | `a82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867` |

Все четыре файла побайтово совпадают с официальным репозиторием
`Kaggle/kaggle-environments` на коммите
[`28b6d8af3ce73926b3d0fda1410c1ddd8384ab8c`](https://github.com/Kaggle/kaggle-environments/commit/28b6d8af3ce73926b3d0fda1410c1ddd8384ab8c)
от **2026-08-15 01:24:24 UTC**. Таблица для машинной проверки находится в
[`SHA256SUMS`](SHA256SUMS).

Актуальная обязательная версия пакета: **`kaggle-environments >= 1.32.7`**;
в [`requirements.txt`](../../requirements.txt) она зафиксирована как `1.32.7`.

## Правила

- [`rules-audit.md`](rules-audit.md) — практический аудит на русском: все важные
  скрытые ограничения, сроки, лимиты, лицензии, runtime и найденные противоречия.
- [`official-rules-extract.md`](official-rules-extract.md) — выдержка исходных
  англоязычных формулировок и номера разделов, чтобы выводы можно было сверить.
- Канонический полный юридический текст:
  <https://www.kaggle.com/competitions/kaggriculture/rules>.
- Текущие Overview / Evaluation / FAQ:
  <https://www.kaggle.com/competitions/kaggriculture/overview>.

Правила и окружение могут измениться. Перед каждым важным сабмитом и обязательно
перед дедлайном нужно повторно сверять страницы Kaggle, pinned announcements и
версию `kaggle-environments`.

## Почему не выполнен authenticated download с Kaggle API

Kaggle CLI установлен в локальную игнорируемую `.venv`, но в рабочей среде нет
авторизации Kaggle, а аккаунт ещё должен принять юридически обязательные правила
кнопкой **Join Competition**. Такое принятие нельзя делать от имени владельца
аккаунта автоматически. Поэтому содержимое сверено с официальным публичным
репозиторием, а не получено через пользовательскую Kaggle-сессию.

После личного принятия правил проверить пакет можно так:

```bash
.venv/bin/kaggle competitions download kaggriculture -p data/kaggriculture
sha256sum competition-data/README.md competition-data/AGENTS.md \
          env/kaggriculture.py env/kaggriculture.json
```

Секреты Kaggle нельзя добавлять в Git; соответствующие пути уже закрыты
[`.gitignore`](../../.gitignore).

## Иерархия источников

- Для юридических ограничений: **Kaggle Foundational Rules** имеют приоритет при
  конфликте; далее применяются Competition-Specific Rules и требования сайта.
- Для поведения игры: развернутая версия движка — источник истины. Kaggle Staff
  отдельно подтвердил это после исправления расхождений документации.
- Форум важен для официальных balance patches, но не заменяет Rules и исходник.
