#!/usr/bin/env bash
# scan-secrets.sh — блокирует попадание секретов в git.
# Используется git pre-commit хуком (scripts/install-git-guard.sh), можно вызывать вручную:
#   scripts/scan-secrets.sh [файл ...]      # без аргументов — staged diff
set -u

RED='\033[31m'; NC='\033[0m'

detect() {
    local file="$1"
    local name base
    base=$(basename "$file")
    name=$(printf '%s' "$base" | tr '[:upper:]' '[:lower:]')

    # 1) Запрещённые имена файлов
    case "$name" in
        kaggle.json|access_token|.env|.env.*|*.pem|*.key|id_rsa*|credentials*|secrets*|*.token)
            echo -e "${RED}SECRET-БЛОК: имя файла $file выглядит как секрет${NC}"; return 1 ;;
    esac

    # 2) Паттерны содержимого (только для текстовых файлов)
    if file -b "$file" 2>/dev/null | grep -q 'text'; then
        if grep -nE '("key"\s*:\s*"[^"]{16,}"|KAGGLE_API_TOKEN\s*=\s*[^[:space:]"]{16,}|access_token[=:]\s*[^[:space:]"]{16,}|"username"\s*:\s*"[^"]+")' "$file" 2>/dev/null | head -5; then
            echo -e "${RED}SECRET-БЛОК: $file содержит похожий на токен/ключ текст (строки выше)${NC}"
            return 1
        fi
    fi
    return 0
}

rc=0
if [ "$#" -gt 0 ]; then
    for f in "$@"; do detect "$f" || rc=1; done
else
    while IFS= read -r f; do
        [ -z "$f" ] && continue
        detect "$f" || rc=1
    done < <(git diff --cached --name-only --diff-filter=ACMR)
fi

if [ "$rc" -ne 0 ]; then
    echo -e "${RED}КОММИТ ЗАБЛОКИРОВАН: найдены секреты. Уберите файл/строку и повторите.${NC}"
    echo "Исключения: .gitignore уже содержит kaggle.json / access_token / .env* —"
    echo "если файл не должен попадать в git, просто не добавляйте его (git rm --cached)."
fi
exit $rc
