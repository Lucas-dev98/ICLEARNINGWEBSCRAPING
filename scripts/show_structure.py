#!/usr/bin/env python3
"""
Exibe a estrutura organizada do projeto
======================================
"""

import os
from pathlib import Path

def mostrar_estrutura():
    """Mostra a estrutura organizada do projeto."""
    
    print("🏗️  ESTRUTURA ORGANIZADA DO PROJETO ICLearningWebScraping")
    print("=" * 65)
    
    # Estrutura do projeto
    estrutura = """
📁 ICLearningWebScraping/           # Diretório raiz do projeto
├── 📄 README.md                    # Documentação principal
├── 📄 requirements.txt             # Dependências Python
├── 📄 setup.py                     # Configuração de instalação
├── 📄 .gitignore                   # Arquivos ignorados pelo Git
├── 📄 MANIFEST.in                  # Controle de distribuição
│
├── 📁 src/                         # Código fonte principal
│   ├── 📄 __init__.py             # Módulo Python
│   │
│   ├── 📁 examples/               # ⭐ EXEMPLOS BÁSICOS
│   │   ├── 📄 __init__.py
│   │   ├── 🐍 example_01_RequestHTML.py          # HTTP requests básicos
│   │   ├── 🐍 example_02_parsing_beatifulSoup.py # Parsing HTML
│   │   └── 🐍 example_03_DOMnavigation.py        # Navegação DOM
│   │
│   ├── 📁 exercises/              # 💪 EXERCÍCIOS PRÁTICOS  
│   │   ├── 📄 __init__.py
│   │   ├── 🐍 exercice_01.py     # Download HTML + validação
│   │   ├── 🐍 exercice_02.py     # Extração e deduplicação
│   │   ├── 🐍 exercice_03.py     # Manipulação de arquivos
│   │   ├── 🐍 exercice_04.py     # Padrões regex
│   │   ├── 🐍 exercice_05.py     # Regex avançado
│   │   └── 🐍 exercice_06.py     # Seletores CSS avançados
│   │
│   └── 📁 scrapers/               # 🚀 SCRAPERS PROFISSIONAIS
│       ├── 📄 __init__.py
│       └── 🐍 scraper_noticias.py # Sistema OOP completo
│
├── 📁 docs/                       # 📚 DOCUMENTAÇÃO
│   └── 📄 DEPENDENCIES.md        # Guia de dependências
│
├── 📁 config/                     # ⚙️  CONFIGURAÇÕES
│   ├── 📄 .inputrc               # Configurações readline
│   └── 📄 .terminal_config       # Configurações terminal
│
├── 📁 data/                       # 💾 DADOS E EXEMPLOS
│   └── 📄 uvv.html               # Página HTML de exemplo
│
├── 📁 scripts/                    # 🛠️  UTILITÁRIOS
│   ├── 🔧 install_dependencies.sh    # Instalação automática
│   ├── 🐍 run_all_examples.py       # Executar todos exemplos
│   ├── 🐍 verify_installation.py    # Verificar instalação
│   └── 🐍 setup_path.py            # Configurar PYTHONPATH
│
├── 📁 tests/                      # 🧪 TESTES (futuro)
│
└── 📁 venv/                       # 🐍 AMBIENTE VIRTUAL
    └── ... (ambiente Python isolado)
    """
    
    print(estrutura)
    
    print("\n🎯 ORGANIZAÇÃO POR CATEGORIA")
    print("=" * 40)
    
    categorias = [
        ("🎓 APRENDIZADO BÁSICO", [
            "src/examples/ - Conceitos fundamentais",
            "src/exercises/ - Prática progressiva"
        ]),
        ("🚀 NÍVEL AVANÇADO", [
            "src/scrapers/ - Sistemas profissionais",
            "tests/ - Testes automatizados (futuro)"
        ]),
        ("📖 DOCUMENTAÇÃO", [
            "README.md - Guia principal",
            "docs/ - Documentação detalhada",
            "setup.py - Configuração instalação"
        ]),
        ("⚙️ CONFIGURAÇÃO", [
            "requirements.txt - Dependências",
            "config/ - Configurações sistema", 
            "scripts/ - Utilitários e automação"
        ]),
        ("💾 RECURSOS", [
            "data/ - Dados exemplo e resultados",
            "venv/ - Ambiente virtual isolado"
        ])
    ]
    
    for categoria, itens in categorias:
        print(f"\n{categoria}")
        for item in itens:
            print(f"  • {item}")
    
    print("\n🚀 COMO USAR A NOVA ESTRUTURA")
    print("=" * 40)
    
    usos = [
        ("🔰 Para iniciantes:", [
            "1. Ative: source venv/bin/activate",
            "2. Execute: python src/examples/example_01_RequestHTML.py",
            "3. Continue com: src/examples/example_02_*, etc.",
            "4. Pratique: src/exercises/exercice_01.py, etc."
        ]),
        ("🎓 Para estudar:", [
            "• Leia: README.md (guia completo)",
            "• Explore: src/examples/ (conceitos)",
            "• Pratique: src/exercises/ (hands-on)",
            "• Analise: src/scrapers/ (código profissional)"
        ]),
        ("🔧 Para desenvolver:", [
            "• Use: from src.scrapers import NoticiasScraper",
            "• Estenda: class MeuScraper(NoticiasScraper)",
            "• Configure: config/ para suas necessidades",
            "• Teste: scripts/verify_installation.py"
        ])
    ]
    
    for uso, passos in usos:
        print(f"\n{uso}")
        for passo in passos:
            print(f"  {passo}")
    
    print("\n✨ BENEFÍCIOS DA REORGANIZAÇÃO")
    print("=" * 40)
    
    beneficios = [
        "📂 Estrutura clara e profissional",
        "🔍 Fácil navegação e localização de arquivos", 
        "📚 Progressão lógica de aprendizado",
        "🚀 Escalabilidade para projetos maiores",
        "🎯 Separação clara entre conceitos e prática",
        "⚙️ Configuração e scripts organizados",
        "📖 Documentação centralizada e clara",
        "🐍 Módulos Python adequadamente estruturados"
    ]
    
    for beneficio in beneficios:
        print(f"  ✅ {beneficio}")
    
    print(f"\n🎉 Projeto reorganizado com sucesso!")
    print("💡 Agora é muito mais fácil aprender e navegar!")

if __name__ == "__main__":
    mostrar_estrutura()