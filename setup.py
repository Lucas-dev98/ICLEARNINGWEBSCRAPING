#!/usr/bin/env python3
"""
Setup.py para o projeto ICLearningWebScraping
===========================================

Script de configuração e instalação do projeto educacional
de web scraping com Python.
"""

from setuptools import setup, find_packages
import os

# Lê o README para usar como descrição longa
def read_readme():
    """Lê o arquivo README.md para usar como descrição."""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Projeto educacional de Web Scraping com Python"

# Lê os requirements para usar como dependências
def read_requirements():
    """Lê o arquivo requirements.txt para extrair dependências."""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    requirements = []
    
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Ignora comentários e linhas vazias
                if line and not line.startswith('#'):
                    # Remove comentários inline
                    if '#' in line:
                        line = line[:line.index('#')].strip()
                    requirements.append(line)
    
    return requirements

setup(
    # === INFORMAÇÕES BÁSICAS ===
    name="iclearning-webscraping",
    version="1.0.0",
    description="Projeto educacional completo para aprender Web Scraping com Python",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    
    # === AUTOR E CONTATO ===
    author="ICLearning WebScraping Project",
    author_email="contato@iclearning.com",
    url="https://github.com/seu-usuario/ICLearningWebScraping",
    
    # === LICENÇA E CLASSIFICAÇÃO ===
    license="Educational Use",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "License :: Free for Educational Use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    
    # === REQUISITOS PYTHON ===
    python_requires=">=3.12",
    
    # === ESTRUTURA DO PROJETO ===
    packages=find_packages(),
    package_dir={'': '.'},
    include_package_data=True,
    
    # === DEPENDÊNCIAS ===
    install_requires=read_requirements(),
    
    # === DEPENDÊNCIAS EXTRAS ===
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ],
        'docs': [
            'sphinx>=6.0.0',
            'sphinx-rtd-theme>=1.2.0',
        ],
        'performance': [
            'cchardet>=2.1.7',  # Detector de encoding mais rápido
            'ujson>=5.7.0',     # JSON parser mais rápido
        ],
    },
    
    # === SCRIPTS E ENTRY POINTS ===
    entry_points={
        'console_scripts': [
            'webscraping-setup=scripts.setup_project:main',
            'webscraping-test=scripts.run_tests:main',
        ],
    },
    
    # === METADADOS ADICIONAIS ===
    keywords=[
        'web-scraping', 'beautifulsoup', 'requests', 'html-parsing',
        'education', 'tutorial', 'python', 'data-extraction', 'crawler'
    ],
    
    project_urls={
        "Documentação": "https://github.com/seu-usuario/ICLearningWebScraping/docs",
        "Código Fonte": "https://github.com/seu-usuario/ICLearningWebScraping",
        "Bug Reports": "https://github.com/seu-usuario/ICLearningWebScraping/issues",
    },
    
    # === ARQUIVOS DE DADOS ===
    package_data={
        'config': ['*.inputrc', '*.terminal_config'],
        'data': ['*.html', '*.json', '*.csv'],
        'docs': ['*.md', '*.rst'],
        'scripts': ['*.sh', '*.py'],
    },
    
    # === ZIP SAFE ===
    zip_safe=False,
)

# === INSTRUÇÕES PÓS-INSTALAÇÃO ===
def post_install_message():
    """Exibe mensagem após instalação bem-sucedida."""
    print("""
    🎉 ICLearningWebScraping instalado com sucesso!
    
    📚 Próximos passos:
    1. Ative o ambiente virtual: source venv/bin/activate
    2. Teste a instalação: python -c "from src.examples import *"
    3. Execute os exemplos: python src/examples/example_01_RequestHTML.py
    4. Leia o README.md para guia completo de uso
    
    🔗 Recursos úteis:
    - Documentação completa: docs/
    - Configurações: config/
    - Scripts utilitários: scripts/
    
    🚀 Bom aprendizado com Web Scraping!
    """)

if __name__ == "__main__":
    setup()
    post_install_message()