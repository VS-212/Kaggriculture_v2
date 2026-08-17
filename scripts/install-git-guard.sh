#!/usr/bin/env bash
# install-git-guard.sh — установить pre-commit хук, блокирующий коммит секретов.
set -eu
HOOK=".git/hooks/pre-commit"
mkdir -p .git/hooks
cat > "$HOOK" <<'EOF'
#!/usr/bin/env bash
# Установлен scripts/install-git-guard.sh — повторный запуск перезапишет.
scripts/scan-secrets.sh
EOF
chmod +x "$HOOK"
echo "хук установлен: $HOOK"
echo "проверка: создайте в /tmp тестовый kaggle.json и попробуйте git add — коммит будет заблокирован."
