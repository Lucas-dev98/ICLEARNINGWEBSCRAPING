#!/usr/bin/env python3
"""
Script para executar todos os exemplos em sequência
==================================================

Este script executa todos os exemplos do projeto em ordem lógica,
demonstrando os conceitos de web scraping progressivamente.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def executar_comando(comando, diretorio=None):
    """Executa um comando e exibe o resultado."""
    try:
        resultado = subprocess.run(
            comando, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd=diretorio,
            timeout=30
        )
        return resultado.returncode == 0, resultado.stdout, resultado.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout: Comando levou mais de 30 segundos"
    except Exception as e:
        return False, "", str(e)

def main():
    """Executa todos os exemplos do projeto."""
    print("🚀 ICLearning WebScraping - Executar Todos os Exemplos")
    print("=" * 55)
    
    # Definir diretório base do projeto
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Verificar se estamos no diretório correto
    if not (project_root / "src").exists():
        print("❌ Erro: Execute este script do diretório raiz do projeto")
        sys.exit(1)
    
    # Lista de exemplos para executar
    exemplos = [
        {
            'nome': '1. Requisições HTTP Básicas',
            'arquivo': 'src/examples/example_01_RequestHTML.py',
            'descricao': 'Demonstra requisições HTTP, DNS e análise de headers'
        },
        {
            'nome': '2. Parsing HTML com BeautifulSoup',
            'arquivo': 'src/examples/example_02_parsing_beatifulSoup.py',
            'descricao': 'Mostra parsing básico e extração de elementos'
        },
        {
            'nome': '3. Navegação no DOM',
            'arquivo': 'src/examples/example_03_DOMnavigation.py',
            'descricao': 'Ensina navegação entre elementos e estrutura DOM'
        },
    ]
    
    exercicios = [
        {
            'nome': '4. Download e Manipulação HTML',
            'arquivo': 'src/exercises/exercice_01.py',
            'descricao': 'Prática de download e validação de conteúdo'
        },
        {
            'nome': '5. Scraper de Notícias Profissional',
            'arquivo': 'src/scrapers/scraper_noticias.py',
            'descricao': 'Sistema completo OOP para scraping estruturado'
        },
    ]
    
    todos_scripts = exemplos + exercicios
    
    print(f"📋 {len(todos_scripts)} scripts serão executados:")
    for i, script in enumerate(todos_scripts, 1):
        print(f"   {i}. {script['nome']}")
    
    print("\n" + "=" * 55)
    
    # Verificar ambiente virtual
    if 'VIRTUAL_ENV' not in os.environ:
        print("⚠️  Aviso: Ambiente virtual não detectado")
        print("   Execute: source venv/bin/activate")
        resposta = input("   Continuar mesmo assim? (s/N): ")
        if resposta.lower() != 's':
            sys.exit(0)
    
    sucessos = 0
    falhas = 0
    
    for i, script in enumerate(todos_scripts, 1):
        print(f"\n🔄 Executando {i}/{len(todos_scripts)}: {script['nome']}")
        print(f"📄 Arquivo: {script['arquivo']}")
        print(f"📝 {script['descricao']}")
        print("-" * 50)
        
        # Executar o script
        sucesso, stdout, stderr = executar_comando(
            f"python {script['arquivo']}", 
            project_root
        )
        
        if sucesso:
            print("✅ Executado com sucesso!")
            sucessos += 1
            if stdout:
                # Limitar output para não poluir muito
                linhas = stdout.strip().split('\n')
                if len(linhas) > 10:
                    print("📤 Output (primeiras/últimas linhas):")
                    for linha in linhas[:5]:
                        print(f"   {linha}")
                    print(f"   ... ({len(linhas) - 10} linhas omitidas) ...")
                    for linha in linhas[-5:]:
                        print(f"   {linha}")
                else:
                    print("📤 Output:")
                    for linha in linhas:
                        print(f"   {linha}")
        else:
            print("❌ Erro na execução!")
            falhas += 1
            if stderr:
                print(f"🔴 Erro: {stderr.strip()}")
        
        # Pausa entre execuções
        if i < len(todos_scripts):
            time.sleep(1)
    
    # Resumo final
    print("\n" + "=" * 55)
    print("📊 RESUMO DA EXECUÇÃO")
    print("=" * 55)
    print(f"✅ Sucessos: {sucessos}/{len(todos_scripts)}")
    print(f"❌ Falhas: {falhas}/{len(todos_scripts)}")
    
    if falhas == 0:
        print("\n🎉 Todos os exemplos executados com sucesso!")
        print("🎓 Agora você pode:")
        print("   • Modificar os exemplos para experimentar")
        print("   • Criar seus próprios scrapers")
        print("   • Estudar o código dos exercícios")
        print("   • Ler a documentação em docs/")
    else:
        print(f"\n⚠️  {falhas} script(s) falharam. Verifique:")
        print("   • Se todas as dependências estão instaladas")
        print("   • Se o ambiente virtual está ativo")
        print("   • Se há conexão com a internet")
        print("   • Os logs de erro acima")
    
    return falhas == 0

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Execução interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)