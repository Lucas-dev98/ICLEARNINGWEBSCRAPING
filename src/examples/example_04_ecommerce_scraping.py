#!/usr/bin/env python3
"""
Exemplo 04 - Scraping de E-commerce
==================================

Este exemplo demonstra como fazer scraping em sites de e-commerce para:
- Extrair informações de produtos
- Monitorar preços
- Coletar avaliações de clientes
- Comparar produtos entre lojas

IMPORTANTE: Este é um exemplo educacional. Sempre respeite os robots.txt
e termos de uso dos sites. Use com responsabilidade!

Autor: ICLearning WebScraping Project
Data: 2025-09-24
"""

# === IMPORTAÇÕES NECESSÁRIAS ===
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime

def simular_pagina_ecommerce():
    """
    Simula uma página de e-commerce para demonstração.
    Em um caso real, você faria requests.get() para o site.
    """
    html_exemplo = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Loja Tech - Os Melhores Produtos</title>
    </head>
    <body>
        <div class="container">
            <!-- Produto 1 -->
            <div class="produto" data-id="001">
                <h2 class="nome-produto">Smartphone Samsung Galaxy S23</h2>
                <div class="preco">
                    <span class="preco-atual">R$ 2.499,00</span>
                    <span class="preco-original">R$ 2.899,00</span>
                    <span class="desconto">14% OFF</span>
                </div>
                <div class="rating">
                    <span class="estrelas">★★★★☆</span>
                    <span class="num-avaliacoes">(1.234 avaliações)</span>
                </div>
                <p class="descricao">Smartphone com tela de 6.1", câmera tripla de 50MP e 128GB de armazenamento</p>
                <div class="tags">
                    <span class="tag">Frete Grátis</span>
                    <span class="tag">Parcelamento</span>
                </div>
                <button class="btn-comprar" data-estoque="15">Comprar Agora</button>
            </div>

            <!-- Produto 2 -->
            <div class="produto" data-id="002">
                <h2 class="nome-produto">Notebook Dell Inspiron 15</h2>
                <div class="preco">
                    <span class="preco-atual">R$ 3.299,00</span>
                    <span class="preco-original">R$ 3.699,00</span>
                    <span class="desconto">11% OFF</span>
                </div>
                <div class="rating">
                    <span class="estrelas">★★★★★</span>
                    <span class="num-avaliacoes">(856 avaliações)</span>
                </div>
                <p class="descricao">Notebook com Intel i7, 16GB RAM, SSD 512GB e tela Full HD de 15.6"</p>
                <div class="tags">
                    <span class="tag">Frete Grátis</span>
                    <span class="tag">Garantia Estendida</span>
                </div>
                <button class="btn-comprar" data-estoque="8">Comprar Agora</button>
            </div>

            <!-- Produto 3 -->
            <div class="produto" data-id="003">
                <h2 class="nome-produto">Fone Bluetooth Sony WH-1000XM4</h2>
                <div class="preco">
                    <span class="preco-atual">R$ 1.199,00</span>
                    <span class="preco-original">R$ 1.399,00</span>
                    <span class="desconto">14% OFF</span>
                </div>
                <div class="rating">
                    <span class="estrelas">★★★★★</span>
                    <span class="num-avaliacoes">(2.105 avaliações)</span>
                </div>
                <p class="descricao">Fone com cancelamento de ruído ativo, bateria de 30h e som Hi-Res</p>
                <div class="tags">
                    <span class="tag">Mais Vendido</span>
                    <span class="tag">Parcelamento</span>
                </div>
                <button class="btn-comprar" data-estoque="23">Comprar Agora</button>
            </div>

            <!-- Produto sem estoque -->
            <div class="produto esgotado" data-id="004">
                <h2 class="nome-produto">Apple iPhone 15 Pro</h2>
                <div class="preco">
                    <span class="preco-atual">R$ 8.999,00</span>
                </div>
                <div class="rating">
                    <span class="estrelas">★★★★☆</span>
                    <span class="num-avaliacoes">(567 avaliações)</span>
                </div>
                <p class="descricao">iPhone 15 Pro com chip A17 Pro, câmera de 48MP e 256GB</p>
                <div class="indisponivel">
                    <span class="status">Produto Esgotado</span>
                    <button class="btn-avisar">Avise-me quando chegar</button>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_exemplo

class EcommerceScraper:
    """
    Classe para scraping especializado em e-commerce.
    
    Funcionalidades:
    - Extração de produtos e preços
    - Monitoramento de promoções
    - Análise de avaliações
    - Comparação de preços
    """
    
    def __init__(self):
        """Inicializa o scraper com configurações adequadas para e-commerce."""
        self.session = requests.Session()
        
        # User-Agent realista para e-commerce
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.session.headers.update(self.headers)
    
    def extrair_preco(self, texto_preco):
        """
        Extrai valor numérico de texto de preço.
        
        Args:
            texto_preco (str): Texto contendo preço (ex: "R$ 1.299,00")
            
        Returns:
            float: Valor numérico do preço
        """
        if not texto_preco:
            return 0.0
        
        # Remove caracteres não numéricos exceto vírgula e ponto
        preco_limpo = re.sub(r'[^\d,.]', '', texto_preco)
        
        # Converte vírgula para ponto (formato brasileiro)
        preco_limpo = preco_limpo.replace('.', '').replace(',', '.')
        
        try:
            return float(preco_limpo)
        except ValueError:
            return 0.0
    
    def extrair_rating(self, elemento_rating):
        """
        Extrai rating em estrelas e número de avaliações.
        
        Args:
            elemento_rating: Elemento BeautifulSoup contendo rating
            
        Returns:
            dict: Informações do rating
        """
        rating_info = {
            'estrelas': 0,
            'num_avaliacoes': 0,
            'texto_estrelas': ''
        }
        
        # Extrair estrelas
        estrelas_elem = elemento_rating.find('span', class_='estrelas')
        if estrelas_elem:
            estrelas_texto = estrelas_elem.get_text()
            rating_info['texto_estrelas'] = estrelas_texto
            # Contar estrelas preenchidas (★)
            rating_info['estrelas'] = estrelas_texto.count('★')
        
        # Extrair número de avaliações
        avaliacoes_elem = elemento_rating.find('span', class_='num-avaliacoes')
        if avaliacoes_elem:
            avaliacoes_texto = avaliacoes_elem.get_text()
            # Extrair número usando regex
            numeros = re.findall(r'[\d.]+', avaliacoes_texto)
            if numeros:
                # Remove pontos de milhares
                rating_info['num_avaliacoes'] = int(numeros[0].replace('.', ''))
        
        return rating_info
    
    def scrape_produtos(self, html_content):
        """
        Extrai informações de produtos de uma página de e-commerce.
        
        Args:
            html_content (str): HTML da página
            
        Returns:
            list: Lista de produtos com suas informações
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        produtos = []
        
        # Encontrar todos os produtos
        elementos_produto = soup.find_all('div', class_='produto')
        
        print(f"🔍 Encontrados {len(elementos_produto)} produtos na página")
        
        for i, produto in enumerate(elementos_produto, 1):
            produto_info = {}
            
            # ID do produto
            produto_info['id'] = produto.get('data-id', f'produto_{i}')
            
            # Nome do produto
            nome_elem = produto.find('h2', class_='nome-produto')
            produto_info['nome'] = nome_elem.get_text().strip() if nome_elem else 'N/A'
            
            # Preços
            preco_atual_elem = produto.find('span', class_='preco-atual')
            preco_original_elem = produto.find('span', class_='preco-original')
            desconto_elem = produto.find('span', class_='desconto')
            
            produto_info['preco_atual'] = self.extrair_preco(
                preco_atual_elem.get_text() if preco_atual_elem else ''
            )
            produto_info['preco_original'] = self.extrair_preco(
                preco_original_elem.get_text() if preco_original_elem else ''
            )
            produto_info['desconto'] = desconto_elem.get_text().strip() if desconto_elem else None
            
            # Calcular economia
            if produto_info['preco_original'] > 0:
                economia = produto_info['preco_original'] - produto_info['preco_atual']
                produto_info['economia'] = economia
                produto_info['percentual_desconto'] = (economia / produto_info['preco_original']) * 100
            else:
                produto_info['economia'] = 0
                produto_info['percentual_desconto'] = 0
            
            # Rating e avaliações
            rating_elem = produto.find('div', class_='rating')
            if rating_elem:
                rating_info = self.extrair_rating(rating_elem)
                produto_info.update(rating_info)
            
            # Descrição
            desc_elem = produto.find('p', class_='descricao')
            produto_info['descricao'] = desc_elem.get_text().strip() if desc_elem else 'N/A'
            
            # Tags (frete grátis, parcelamento, etc.)
            tags_elems = produto.find_all('span', class_='tag')
            produto_info['tags'] = [tag.get_text().strip() for tag in tags_elems]
            
            # Verificar disponibilidade
            if 'esgotado' in produto.get('class', []):
                produto_info['disponivel'] = False
                produto_info['status'] = 'Esgotado'
            else:
                produto_info['disponivel'] = True
                produto_info['status'] = 'Disponível'
                
                # Estoque (se disponível)
                btn_comprar = produto.find('button', class_='btn-comprar')
                if btn_comprar:
                    estoque = btn_comprar.get('data-estoque')
                    produto_info['estoque'] = int(estoque) if estoque else None
            
            # Timestamp da coleta
            produto_info['coletado_em'] = datetime.now().isoformat()
            
            produtos.append(produto_info)
        
        return produtos
    
    def analisar_produtos(self, produtos):
        """
        Analisa os produtos coletados e gera estatísticas.
        
        Args:
            produtos (list): Lista de produtos
            
        Returns:
            dict: Análise dos produtos
        """
        if not produtos:
            return {'erro': 'Nenhum produto para analisar'}
        
        df = pd.DataFrame(produtos)
        
        analise = {
            'total_produtos': len(produtos),
            'produtos_disponiveis': len(df[df['disponivel'] == True]),
            'produtos_esgotados': len(df[df['disponivel'] == False]),
            'preco_medio': df['preco_atual'].mean(),
            'preco_min': df['preco_atual'].min(),
            'preco_max': df['preco_atual'].max(),
            'economia_total': df['economia'].sum(),
            'rating_medio': df['estrelas'].mean(),
            'total_avaliacoes': df['num_avaliacoes'].sum(),
        }
        
        # Produto mais caro e mais barato
        produto_caro = df.loc[df['preco_atual'].idxmax()]
        produto_barato = df.loc[df['preco_atual'].idxmin()]
        
        analise['produto_mais_caro'] = {
            'nome': produto_caro['nome'],
            'preco': produto_caro['preco_atual']
        }
        analise['produto_mais_barato'] = {
            'nome': produto_barato['nome'], 
            'preco': produto_barato['preco_atual']
        }
        
        # Melhor desconto
        if 'percentual_desconto' in df.columns:
            melhor_desconto = df.loc[df['percentual_desconto'].idxmax()]
            analise['melhor_desconto'] = {
                'nome': melhor_desconto['nome'],
                'desconto': melhor_desconto['percentual_desconto']
            }
        
        return analise

def exemplo_uso():
    """Demonstra o uso prático do EcommerceScraper."""
    print("🛒 === EXEMPLO DE SCRAPING E-COMMERCE ===")
    print("=" * 50)
    
    # Inicializar scraper
    scraper = EcommerceScraper()
    
    # Simular página de e-commerce (em produção, seria requests.get())
    print("1️⃣ Obtendo dados da página de produtos...")
    html_content = simular_pagina_ecommerce()
    
    # Extrair produtos
    print("2️⃣ Extraindo informações dos produtos...")
    produtos = scraper.scrape_produtos(html_content)
    
    # Exibir produtos encontrados
    print(f"\n📦 === PRODUTOS ENCONTRADOS ({len(produtos)}) ===")
    for i, produto in enumerate(produtos, 1):
        print(f"\n🏷️  Produto {i}: {produto['nome']}")
        print(f"   💰 Preço: R$ {produto['preco_atual']:.2f}")
        
        if produto['preco_original'] > 0:
            print(f"   🏷️  De: R$ {produto['preco_original']:.2f}")
            print(f"   💸 Economia: R$ {produto['economia']:.2f} ({produto['percentual_desconto']:.1f}%)")
        
        print(f"   ⭐ Rating: {produto['estrelas']}/5 ({produto['num_avaliacoes']} avaliações)")
        print(f"   📝 {produto['descricao']}")
        
        if produto['tags']:
            print(f"   🏪 Tags: {', '.join(produto['tags'])}")
        
        print(f"   📊 Status: {produto['status']}")
        
        if produto.get('estoque'):
            print(f"   📦 Estoque: {produto['estoque']} unidades")
    
    # Análise dos dados
    print(f"\n📊 === ANÁLISE DOS PRODUTOS ===")
    analise = scraper.analisar_produtos(produtos)
    
    print(f"📈 Total de produtos: {analise['total_produtos']}")
    print(f"✅ Disponíveis: {analise['produtos_disponiveis']}")
    print(f"❌ Esgotados: {analise['produtos_esgotados']}")
    print(f"💰 Preço médio: R$ {analise['preco_medio']:.2f}")
    print(f"🔻 Mais barato: {analise['produto_mais_barato']['nome']} - R$ {analise['produto_mais_barato']['preco']:.2f}")
    print(f"🔺 Mais caro: {analise['produto_mais_caro']['nome']} - R$ {analise['produto_mais_caro']['preco']:.2f}")
    print(f"⭐ Rating médio: {analise['rating_medio']:.1f}/5")
    print(f"💬 Total de avaliações: {analise['total_avaliacoes']:,}")
    print(f"💸 Economia total disponível: R$ {analise['economia_total']:.2f}")
    
    if 'melhor_desconto' in analise:
        print(f"🏆 Melhor desconto: {analise['melhor_desconto']['nome']} ({analise['melhor_desconto']['desconto']:.1f}%)")
    
    # Salvar em CSV
    print(f"\n💾 Salvando dados em CSV...")
    df = pd.DataFrame(produtos)
    filename = f"produtos_ecommerce_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False, encoding='utf-8')
    print(f"✅ Dados salvos em: {filename}")
    
    # Dicas para uso real
    print(f"\n💡 === DICAS PARA USO EM PRODUÇÃO ===")
    dicas = [
        "🔄 Implemente delays entre requests (time.sleep)",
        "🔄 Use rotação de User-Agents para evitar bloqueios",
        "📊 Configure monitoramento de preços com banco de dados",
        "🛡️  Trate exceções de rede e timeouts adequadamente",
        "🤖 Respeite robots.txt e políticas dos sites",
        "⚡ Use cache para evitar requests desnecessários",
        "📈 Implemente notificações para promoções",
        "🔐 Configure proxies se necessário"
    ]
    
    for dica in dicas:
        print(f"   {dica}")
    
    print(f"\n🎯 === APLICAÇÕES PRÁTICAS ===")
    aplicacoes = [
        "💰 Monitoramento de preços em tempo real",
        "📊 Análise de mercado e concorrência", 
        "🛍️  Comparador de preços automático",
        "📢 Alertas de promoções e descontos",
        "📈 Análise de tendências de preços",
        "⭐ Monitoramento de reputação (reviews)",
        "📦 Controle de disponibilidade de estoque"
    ]
    
    for app in aplicacoes:
        print(f"   {app}")

if __name__ == "__main__":
    exemplo_uso()