#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🗃️ Demonstração do Sistema de Cache - UVV InovaWeek Scraper
==========================================================

Este script demonstra como o sistema de cache funciona no scraper UVV InovaWeek.
Você pode ver a diferença de performance entre requisições com e sem cache.

Funcionalidades demonstradas:
- Cache automático de requisições HTTP
- Estatísticas de hit/miss do cache
- Comparação de tempo com e sem cache
- Limpeza de cache
- Configuração de expiração

Autor: ICLearning WebScraping Project
Data: 26/09/2025
"""

import sys
import os
import time
from datetime import datetime

# Adicionar o diretório pai ao path para importar o scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.scraper_uvv_inovaweek_revisado import UVVInovaWeekScraper, CacheManager

def demonstracao_basica():
    """Demonstra o funcionamento básico do cache"""
    print("🗃️ === DEMONSTRAÇÃO DO SISTEMA DE CACHE ===\n")
    
    # 1. Scraper com cache
    print("1️⃣ Inicializando scraper COM cache...")
    scraper = UVVInovaWeekScraper(use_cache=True)
    
    # URL de teste
    url_teste = "https://www.uvv.br/noticias/"
    
    print("2️⃣ Fazendo primeira requisição (será armazenada no cache)...")
    inicio = time.time()
    response1 = scraper.fazer_requisicao(url_teste)
    tempo1 = time.time() - inicio
    print(f"⏱️ Primeira requisição: {tempo1:.2f} segundos")
    
    print("3️⃣ Fazendo segunda requisição (deve vir do cache)...")
    inicio = time.time()
    response2 = scraper.fazer_requisicao(url_teste)
    tempo2 = time.time() - inicio
    print(f"⏱️ Segunda requisição: {tempo2:.2f} segundos")
    
    # Calcular melhoria
    if tempo1 > 0 and tempo2 >= 0:
        if tempo2 == 0:
            melhoria = 100
        else:
            melhoria = ((tempo1 - tempo2) / tempo1) * 100
        print(f"🚀 Melhoria de performance: {melhoria:.1f}% mais rápida!")
    
    print("4️⃣ Estatísticas do cache:")
    scraper.print_cache_stats()
    
    try:
        input("\n⏸️ Pressione Enter para continuar...")
    except EOFError:
        print("\n⏭️ Continuando automaticamente...")

def comparacao_com_sem_cache():
    """Compara performance com e sem cache"""
    print("\n⚡ === COMPARAÇÃO: COM CACHE vs SEM CACHE ===\n")
    
    urls_teste = [
        "https://www.uvv.br/noticias/",
        "https://www.uvv.br/noticias/page/2/", 
        "https://www.uvv.br/noticias/page/3/"
    ]
    
    print("1️⃣ Testando SEM cache...")
    scraper_sem_cache = UVVInovaWeekScraper(use_cache=False)
    inicio = time.time()
    for url in urls_teste:
        scraper_sem_cache.fazer_requisicao(url)
    tempo_sem_cache = time.time() - inicio
    print(f"⏱️ Tempo SEM cache: {tempo_sem_cache:.2f} segundos")
    
    print("\n2️⃣ Testando COM cache...")
    scraper_com_cache = UVVInovaWeekScraper(use_cache=True)
    
    print("   Primeira passada (populando cache)...")
    inicio = time.time()
    for url in urls_teste:
        scraper_com_cache.fazer_requisicao(url)
    tempo_primeira_passada = time.time() - inicio
    
    print("   Segunda passada (usando cache)...")
    inicio = time.time() 
    for url in urls_teste:
        scraper_com_cache.fazer_requisicao(url)
    tempo_com_cache = time.time() - inicio
    print(f"⏱️ Tempo COM cache: {tempo_com_cache:.2f} segundos")
    
    # Calcular melhoria
    if tempo_sem_cache > 0:
        melhoria = ((tempo_sem_cache - tempo_com_cache) / tempo_sem_cache) * 100
        print(f"\n🚀 Melhoria: {melhoria:.1f}% mais rápido!")
        print(f"💾 Economia de tempo: {tempo_sem_cache - tempo_com_cache:.2f} segundos")
    
    print("\n📊 Estatísticas finais do cache:")
    scraper_com_cache.print_cache_stats()
    
    try:
        input("\n⏸️ Pressione Enter para continuar...")
    except EOFError:
        print("\n⏭️ Continuando automaticamente...")

def gerenciamento_cache():
    """Demonstra gerenciamento do cache"""
    print("\n🔧 === GERENCIAMENTO DO CACHE ===\n")
    
    # Criar scraper com cache
    scraper = UVVInovaWeekScraper(use_cache=True)
    
    print("1️⃣ Fazendo algumas requisições para popular o cache...")
    urls = [
        "https://www.uvv.br/noticias/",
        "https://www.uvv.br/noticias/page/2/"
    ]
    
    for i, url in enumerate(urls, 1):
        scraper.fazer_requisicao(url)
        print(f"   ✅ Requisição {i} concluída")
    
    print("\n2️⃣ Estatísticas atuais do cache:")
    scraper.print_cache_stats()
    
    print("\n3️⃣ Limpando o cache...")
    scraper.clear_cache()
    print("   🧹 Cache limpo!")
    
    print("\n4️⃣ Estatísticas após limpeza:")
    scraper.print_cache_stats()
    
    try:
        input("\n⏸️ Pressione Enter para continuar...")
    except EOFError:
        print("\n⏭️ Continuando automaticamente...")

def demonstrar_cache_expiracao():
    """
    ⏰ Demonstra funcionamento da expiração do cache
    """
    print("\n⏰ === EXPIRAÇÃO DO CACHE ===\n")
    
    # Criar cache com expiração muito curta (1 minuto para demonstração)
    print("1️⃣ Criando scraper com cache de 1 minuto...")
    cache_manager = CacheManager(cache_dir="cache_demo_expiracao", expiration_hours=0.0167)  # ~1 minuto
    
    # Simular cache expirado criando arquivo antigo
    import os
    test_file = os.path.join("cache_demo_expiracao", "test.cache")
    os.makedirs("cache_demo_expiracao", exist_ok=True)
    
    with open(test_file, 'w') as f:
        f.write("cache antigo")
    
    # Alterar timestamp do arquivo para simular expiração
    old_time = time.time() - 3600  # 1 hora atrás
    os.utime(test_file, (old_time, old_time))
    
    print("2️⃣ Verificando limpeza automática de cache expirado...")
    cache_manager._clean_expired_cache()
    
    # Verificar se arquivo foi removido
    if not os.path.exists(test_file):
        print("✅ Cache expirado foi removido automaticamente!")
    else:
        print("❌ Cache expirado não foi removido")
    
    # Limpar diretório de teste
    import shutil
    if os.path.exists("cache_demo_expiracao"):
        shutil.rmtree("cache_demo_expiracao")
        print("🧹 Diretório de teste limpo")

def menu_interativo():
    """
    📋 Menu interativo para demonstrações
    """
    while True:
        print("\n" + "="*60)
        print("🗃️ DEMONSTRAÇÃO DO SISTEMA DE CACHE - UVV SCRAPER")
        print("="*60)
        print("1️⃣  Demonstração básica do cache")
        print("2️⃣  Comparação: Com cache vs Sem cache") 
        print("3️⃣  Gerenciamento do cache")
        print("4️⃣  Expiração do cache")
        print("5️⃣  Executar scraper real com cache")
        print("0️⃣  Sair")
        print("-"*60)
        
        try:
            escolha = input("Digite sua opção: ").strip()
        except EOFError:
            print("\n👋 Entrada finalizada automaticamente.")
            break
        
        try:
            if escolha == "1":
                demonstracao_basica()
            elif escolha == "2":
                comparacao_com_sem_cache()
            elif escolha == "3":
                gerenciamento_cache()
            elif escolha == "4":
                demonstrar_cache_expiracao()
            elif escolha == "5":
                executar_scraper_real()
            elif escolha == "0":
                print("\n👋 Obrigado por usar a demonstração do cache!")
                break
            else:
                print("❌ Opção inválida! Tente novamente.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Demonstração interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"\n❌ Erro durante execução: {e}")
            try:
                input("\n⏸️ Pressione Enter para continuar...")
            except EOFError:
                print("\n⏭️ Continuando automaticamente...")

def executar_scraper_real():
    """
    🚀 Executa o scraper real com cache habilitado
    """
    print("\n🚀 === EXECUTANDO SCRAPER REAL COM CACHE ===\n")
    
    scraper = UVVInovaWeekScraper(use_cache=True, cache_hours=24)
    
    print("🎯 Coletando notícias do InovaWeek (primeira página)...")
    
    try:
        # Executar coleta real
        noticias = scraper.coletar_noticias_inovaweek(
            max_paginas=1  # Apenas primeira página para demo
        )
        
        print(f"\n✅ Coleta concluída!")
        print(f"📰 Notícias encontradas: {len(noticias)}")
        
        # Mostrar estatísticas do cache
        print("\n📊 Estatísticas do cache:")
        scraper.print_cache_stats()
        
    except Exception as e:
        print(f"❌ Erro durante coleta: {e}")

if __name__ == "__main__":
    try:
        menu_interativo()
    except KeyboardInterrupt:
        print("\n\n👋 Demonstração finalizada.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")