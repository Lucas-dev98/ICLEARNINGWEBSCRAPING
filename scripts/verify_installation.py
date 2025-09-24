#!/usr/bin/env python3
"""
Script de Verificação da Instalação
===================================

Verifica se todas as dependências estão instaladas e funcionando
corretamente no projeto ICLearningWebScraping.
"""

import sys
import subprocess
import importlib
import requests
from pathlib import Path

# Configurar PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))
try:
    from scripts.setup_path import setup_python_path
    setup_python_path()
except ImportError:
    pass

def verificar_python():
    """Verifica a versão do Python."""
    version = sys.version_info
    print(f"🐍 Python {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 12):
        print("❌ Python 3.12+ é recomendado")
        return False
    else:
        print("✅ Versão do Python OK")
        return True

def verificar_dependencia(nome, import_name=None, version_attr='__version__'):
    """Verifica se uma dependência está instalada."""
    try:
        if import_name is None:
            import_name = nome
        
        modulo = importlib.import_module(import_name)
        
        # Tentar obter versão
        version = "desconhecida"
        if hasattr(modulo, version_attr):
            version = getattr(modulo, version_attr)
        elif hasattr(modulo, 'VERSION'):
            version = getattr(modulo, 'VERSION')
        elif hasattr(modulo, 'version'):
            version = getattr(modulo, 'version')
        
        print(f"✅ {nome} ({version})")
        return True
        
    except ImportError:
        print(f"❌ {nome} - NÃO INSTALADO")
        return False
    except Exception as e:
        print(f"⚠️  {nome} - Erro: {e}")
        return False

def verificar_estrutura_projeto():
    """Verifica se a estrutura do projeto está correta."""
    print("\n📁 Verificando estrutura do projeto...")
    
    pastas_obrigatorias = [
        'src',
        'src/examples',
        'src/exercises', 
        'src/scrapers',
        'docs',
        'config',
        'data',
        'scripts',
        'venv'
    ]
    
    arquivos_obrigatorios = [
        'README.md',
        'requirements.txt',
        'setup.py',
        'src/__init__.py',
        'src/examples/example_01_RequestHTML.py',
        'src/scrapers/scraper_noticias.py'
    ]
    
    project_root = Path.cwd()
    tudo_ok = True
    
    # Verificar pastas
    for pasta in pastas_obrigatorias:
        caminho = project_root / pasta
        if caminho.exists() and caminho.is_dir():
            print(f"✅ Pasta: {pasta}")
        else:
            print(f"❌ Pasta faltando: {pasta}")
            tudo_ok = False
    
    # Verificar arquivos
    for arquivo in arquivos_obrigatorios:
        caminho = project_root / arquivo
        if caminho.exists() and caminho.is_file():
            print(f"✅ Arquivo: {arquivo}")
        else:
            print(f"❌ Arquivo faltando: {arquivo}")
            tudo_ok = False
    
    return tudo_ok

def verificar_conexao_internet():
    """Verifica se há conexão com a internet."""
    print("\n🌐 Testando conexão com a internet...")
    
    try:
        response = requests.get('https://httpbin.org/get', timeout=10)
        if response.status_code == 200:
            print("✅ Conexão com a internet OK")
            return True
        else:
            print(f"⚠️  Conexão instável (Status: {response.status_code})")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Sem conexão com a internet: {e}")
        return False

def verificar_imports_projeto():
    """Verifica se os módulos do projeto podem ser importados."""
    print("\n📦 Testando imports do projeto...")
    
    testes = [
        ('src.examples', 'Módulo de exemplos'),
        ('src.exercises', 'Módulo de exercícios'), 
        ('src.scrapers', 'Módulo de scrapers'),
        ('src.scrapers.scraper_noticias', 'Scraper de notícias')
    ]
    
    tudo_ok = True
    
    for modulo, descricao in testes:
        try:
            importlib.import_module(modulo)
            print(f"✅ {descricao}")
        except ImportError as e:
            print(f"❌ {descricao}: {e}")
            tudo_ok = False
        except Exception as e:
            print(f"⚠️  {descricao}: Erro inesperado - {e}")
            tudo_ok = False
    
    return tudo_ok

def executar_teste_basico():
    """Executa um teste básico de scraping."""
    print("\n🧪 Executando teste básico de scraping...")
    
    try:
        # Importar o scraper
        sys.path.append(str(Path.cwd()))
        from src.scrapers.scraper_noticias import NoticiasScraper
        
        # Criar instância
        scraper = NoticiasScraper("https://example.com")
        print("✅ Scraper criado com sucesso")
        
        # Testar método básico
        html_teste = "<html><body><h1>Teste</h1></body></html>"
        resultado = scraper.extrair_noticias_exemplo(html_teste)
        
        if isinstance(resultado, list):
            print("✅ Extração de dados funcionando")
            return True
        else:
            print("❌ Extração de dados retornou tipo incorreto")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal de verificação."""
    print("🔍 ICLearning WebScraping - Verificação da Instalação")
    print("=" * 60)
    
    resultados = []
    
    # Verificações
    print("\n📋 VERIFICAÇÕES BÁSICAS")
    print("-" * 30)
    resultados.append(verificar_python())
    
    print("\n📦 DEPENDÊNCIAS PYTHON")
    print("-" * 30)
    dependencias = [
        ('requests', None),
        ('bs4', 'beautifulsoup4'),
        ('pandas', None),
        ('lxml', None), 
        ('html5lib', None)
    ]
    
    for dep in dependencias:
        nome = dep[1] if dep[1] else dep[0]
        resultados.append(verificar_dependencia(nome, dep[0]))
    
    # Verificações do projeto
    resultados.append(verificar_estrutura_projeto())
    resultados.append(verificar_conexao_internet())
    resultados.append(verificar_imports_projeto())
    resultados.append(executar_teste_basico())
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 60)
    
    sucessos = sum(resultados)
    total = len(resultados)
    
    print(f"✅ Verificações bem-sucedidas: {sucessos}/{total}")
    print(f"❌ Verificações falharam: {total - sucessos}/{total}")
    
    if sucessos == total:
        print("\n🎉 INSTALAÇÃO PERFEITA!")
        print("✨ Tudo funcionando corretamente!")
        print("🚀 Você pode executar os exemplos sem problemas.")
        print("\n💡 Próximos passos:")
        print("   • Execute: python scripts/run_all_examples.py")
        print("   • Leia: README.md para guia completo")
        print("   • Explore: src/examples/ para aprender")
    else:
        print(f"\n⚠️  PROBLEMAS ENCONTRADOS ({total - sucessos})")
        print("🔧 Para resolver:")
        print("   • Ative o ambiente virtual: source venv/bin/activate")
        print("   • Instale dependências: pip install -r requirements.txt")
        print("   • Execute do diretório correto do projeto")
        print("   • Verifique conexão com a internet")
        
    return sucessos == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Verificação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado na verificação: {e}")
        sys.exit(1)