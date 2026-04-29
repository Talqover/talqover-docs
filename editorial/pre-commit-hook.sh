#!/bin/bash
# Optional pre-commit hook. To install:
#   ln -s ../../editorial/pre-commit-hook.sh .git/hooks/pre-commit
#
# Roda editorial/check.sh sempre antes de commit. Avisa mas não bloqueia
# (commit segue, decisão fica com o reviewer).

cd "$(git rev-parse --show-toplevel)" || exit 0

# Só roda se algum .mdx foi modificado
if git diff --cached --name-only | grep -qE "^(en|pt-br)/.*\.mdx$"; then
    echo "Editorial check (warning only):"
    bash editorial/check.sh
    echo ""
    echo "(continuando commit — corrigir antes de mergear PR)"
fi

exit 0
