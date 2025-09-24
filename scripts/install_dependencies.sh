#!/bin/bash

# ===================================================================
# SCRIPT DE INSTALAÇÃO AUTOMÁTICA - WEB SCRAPING PROJECT
# ===================================================================
# 
# Este script automatiza a instalação de todas as dependências
# necessárias para executar os exemplos de web scraping.
#
# Uso:
# chmod +x install_dependencies.sh
# ./install_dependencies.sh
# ===================================================================

echo "🚀 === INSTALAÇÃO AUTOMÁTICA DE DEPENDÊNCIAS ==="
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale Python 3.8+ primeiro."
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "   CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "   macOS: brew install python3"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instalando..."
    python3 -m ensurepip --upgrade
fi

echo "✅ pip encontrado: $(pip3 --version)"
echo ""

# Atualiza pip para versão mais recente
echo "📦 Atualizando pip..."
pip3 install --upgrade pip
echo ""

# === INSTALAÇÃO DAS DEPENDÊNCIAS PRINCIPAIS ===
echo "📚 Instalando dependências principais..."
echo ""

# Bibliotecas obrigatórias
echo "1️⃣ Instalando requests (requisições HTTP)..."
pip3 install "requests>=2.31.0"

echo "2️⃣ Instalando beautifulsoup4 (parsing HTML)..."
pip3 install "beautifulsoup4>=4.12.0"

echo "3️⃣ Instalando pandas (análise de dados)..."
pip3 install "pandas>=2.0.0"

# Parsers opcionais mas recomendados
echo "4️⃣ Instalando lxml (parser rápido)..."
pip3 install "lxml>=4.9.0"

echo "5️⃣ Instalando html5lib (parser robusto)..."
pip3 install "html5lib>=1.1"

echo ""
echo "✅ === INSTALAÇÃO CONCLUÍDA ==="
echo ""

# Verifica instalação
echo "🔍 Verificando instalações..."
echo ""

python3 -c "
import sys
print(f'Python: {sys.version}')
print()

try:
    import requests
    print(f'✅ requests: {requests.__version__}')
except ImportError:
    print('❌ requests: NÃO INSTALADO')

try:
    import bs4
    print(f'✅ beautifulsoup4: {bs4.__version__}')
except ImportError:
    print('❌ beautifulsoup4: NÃO INSTALADO')

try:
    import pandas as pd
    print(f'✅ pandas: {pd.__version__}')
except ImportError:
    print('❌ pandas: NÃO INSTALADO')

try:
    import lxml
    print(f'✅ lxml: {lxml.__version__}')
except ImportError:
    print('❌ lxml: NÃO INSTALADO')

try:
    import html5lib
    print(f'✅ html5lib: {html5lib.__version__}')
except ImportError:
    print('❌ html5lib: NÃO INSTALADO')

# Testa bibliotecas padrão
try:
    import socket, urllib.parse, os, re, csv, time
    from datetime import datetime
    print('✅ Bibliotecas padrão: OK')
except ImportError as e:
    print(f'❌ Biblioteca padrão: {e}')
"

echo ""
echo "🎯 === PRÓXIMOS PASSOS ==="
echo ""
echo "1. Execute qualquer script de exemplo:"
echo "   python3 example_01_RequestHTML.py"
echo "   python3 exercice_01.py"
echo "   python3 scraper_noticias.py"
echo ""
echo "2. Para instalar dependências adicionais (opcional):"
echo "   pip3 install selenium loguru python-dotenv"
echo ""
echo "3. Para desenvolvimento:"
echo "   pip3 install pytest pytest-cov black isort"
echo ""
echo "📖 Leia a documentação nos arquivos .py para mais detalhes!"
echo ""
echo "🎉 Instalação completa! Bom web scraping! 🕷️"