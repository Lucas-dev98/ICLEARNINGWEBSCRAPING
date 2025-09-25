#!/bin/bash
# =========================================
# Script de Informações do Repositório Git
# =========================================

echo "📊 INFORMAÇÕES DO REPOSITÓRIO ICLEARNINGWEBSCRAPING"
echo "=================================================="

echo ""
echo "🔗 REPOSITÓRIO REMOTO:"
git remote -v

echo ""
echo "🌿 BRANCH ATUAL:"
git branch -v

echo ""
echo "📝 ÚLTIMO COMMIT:"
git log --oneline -1

echo ""
echo "📁 ARQUIVOS NO REPOSITÓRIO:"
git ls-files | wc -l
echo "   Total de arquivos versionados: $(git ls-files | wc -l)"

echo ""
echo "📈 ESTATÍSTICAS DO PROJETO:"
echo "   Linhas de código Python:"
find src/ -name "*.py" -exec wc -l {} + | tail -1 | awk '{print "   " $1 " linhas"}'

echo "   Arquivos Python:"
find src/ -name "*.py" | wc -l | awk '{print "   " $1 " arquivos"}'

echo ""
echo "🎯 ESTRUTURA DE PASTAS:"
find . -type d -not -path "./venv*" -not -path "./.git*" | sort

echo ""
echo "✅ REPOSITÓRIO CONFIGURADO COM SUCESSO!"
echo "🔗 Acesse: https://github.com/Lucas-dev98/ICLEARNINGWEBSCRAPING"
echo ""
echo "💡 PRÓXIMOS PASSOS:"
echo "   • Visite o repositório no GitHub para ver o README"
echo "   • Clone em outras máquinas: git clone git@github.com:Lucas-dev98/ICLEARNINGWEBSCRAPING.git"
echo "   • Para contribuir: git pull, faça mudanças, git add, git commit, git push"
echo ""