#!/bin/bash
# Editorial health check. Roda a qualquer momento para ver progresso do plano.
# Meta: tudo zerado ao fim da Fase 3.

cd "$(dirname "$0")/.."

echo "=== Buzzwords / openers ==="
grep -rE "advanced|powerful|comprehensive|seamless|intelligent|cutting-edge|leverage|synergy|robust|AI-powered|AI-driven|world-class|enterprise-grade|sophisticated|in just [0-9]+ minute|This endpoint allows|Este endpoint permite" en/ pt-br/ --include="*.mdx" -l 2>/dev/null | wc -l | xargs echo "files com buzzword/opener filler:"

echo ""
echo "=== Headings em Title Case ==="
grep -rE "^## (Request Headers|Request Body|Path Parameters|Query Parameters|Error Responses|Best Practices|Important Notes)" en/ pt-br/ --include="*.mdx" 2>/dev/null | wc -l | xargs echo "headings em Title Case:"

echo ""
echo "=== Tabelas com emoji ❌/✅ ==="
grep -rE "[✅❌]" en/ pt-br/ --include="*.mdx" -l 2>/dev/null | wc -l | xargs echo "files com emoji em tabela:"

echo ""
echo "=== 'etc.' em listas de enum ==="
grep -rE "Options:.*etc\." en/ pt-br/ --include="*.mdx" 2>/dev/null | wc -l | xargs echo "ocorrências de etc. em enum:"

echo ""
echo "=== Exemplos pt-BR não localizados ==="
grep -rE "\+1[0-9]{10}|America/New_York|\bJohn Doe\b" pt-br/ --include="*.mdx" 2>/dev/null | wc -l | xargs echo "exemplos US em pt-br:"

echo ""
echo "=== Localização US incorreta em ambos locales ==="
grep -rE "\bAcme Corp\b|\bAcme Inc\b" en/ pt-br/ --include="*.mdx" 2>/dev/null | wc -l | xargs echo "Acme genérico:"

echo ""
echo "Meta: todos zerados após Fase 3."
