#!/usr/bin/env python3
"""
Exemplo 06 - Scraping de Sites Educacionais
==========================================

Este exemplo demonstra como fazer scraping em plataformas educacionais para:
- Extrair informações de cursos e aulas
- Coletar dados de instrutores e avaliações
- Monitorar preços de cursos
- Analisar conteúdo educacional

IMPORTANTE: Sempre respeite os termos de uso das plataformas educacionais!

Autor: ICLearning WebScraping Project  
Data: 2025-09-24
"""

# === IMPORTAÇÕES NECESSÁRIAS ===
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
from collections import Counter
import time

def simular_plataforma_educacional():
    """Simula uma plataforma educacional para demonstração."""
    html_exemplo = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>EduTech - Plataforma de Cursos Online</title>
    </head>
    <body>
        <div class="container">
            <!-- Curso 1 -->
            <div class="curso" data-id="curso-001">
                <header class="curso-header">
                    <h2 class="titulo-curso">Python para Data Science - Completo</h2>
                    <div class="instrutor">
                        <img src="/avatar/joao.jpg" alt="João Silva" class="avatar">
                        <div class="info-instrutor">
                            <span class="nome-instrutor">João Silva</span>
                            <span class="titulo-instrutor">PhD em Ciência de Dados</span>
                            <div class="rating-instrutor">
                                <span class="estrelas">★★★★★</span>
                                <span class="nota">4.8</span>
                                <span class="num-avaliacoes">(1.234 avaliações)</span>
                            </div>
                        </div>
                    </div>
                </header>
                
                <div class="curso-conteudo">
                    <p class="descricao">Aprenda Python do zero ao avançado com foco em análise de dados, machine learning e visualização.</p>
                    
                    <div class="estatisticas">
                        <span class="duracao">40 horas</span>
                        <span class="aulas">85 aulas</span>
                        <span class="nivel">Iniciante ao Avançado</span>
                        <span class="idioma">Português</span>
                        <span class="certificado">✓ Certificado</span>
                    </div>
                    
                    <div class="topicos">
                        <h4>O que você vai aprender:</h4>
                        <ul class="lista-topicos">
                            <li>Fundamentos do Python</li>
                            <li>NumPy e Pandas para análise de dados</li>
                            <li>Matplotlib e Seaborn para visualização</li>
                            <li>Scikit-learn para Machine Learning</li>
                            <li>Projetos práticos reais</li>
                        </ul>
                    </div>
                    
                    <div class="preco-info">
                        <span class="preco-atual">R$ 199,90</span>
                        <span class="preco-original">R$ 399,90</span>
                        <span class="desconto">50% OFF</span>
                        <span class="promocao-tempo">Promoção até 30/09/2025</span>
                    </div>
                </div>
                
                <div class="curso-stats">
                    <span class="estudantes">15.678 estudantes</span>
                    <span class="rating">4.7/5.0</span>
                    <span class="reviews">2.345 reviews</span>
                    <span class="conclusao">89% conclusão</span>
                    <span class="atualizado">Atualizado em Set/2025</span>
                </div>
                
                <div class="tags-curso">
                    <span class="tag">Python</span>
                    <span class="tag">Data Science</span>
                    <span class="tag">Machine Learning</span>
                    <span class="tag">Pandas</span>
                    <span class="tag">NumPy</span>
                </div>
            </div>

            <!-- Curso 2 -->
            <div class="curso" data-id="curso-002">
                <header class="curso-header">
                    <h2 class="titulo-curso">Web Scraping com Python - Do Básico ao Profissional</h2>
                    <div class="instrutor">
                        <img src="/avatar/maria.jpg" alt="Maria Santos" class="avatar">
                        <div class="info-instrutor">
                            <span class="nome-instrutor">Maria Santos</span>
                            <span class="titulo-instrutor">Engenheira de Software Sênior</span>
                            <div class="rating-instrutor">
                                <span class="estrelas">★★★★☆</span>
                                <span class="nota">4.6</span>
                                <span class="num-avaliacoes">(856 avaliações)</span>
                            </div>
                        </div>
                    </div>
                </header>
                
                <div class="curso-conteudo">
                    <p class="descricao">Domine web scraping com Python, BeautifulSoup, Selenium e técnicas avançadas para extrair dados da web.</p>
                    
                    <div class="estatisticas">
                        <span class="duracao">25 horas</span>
                        <span class="aulas">60 aulas</span>
                        <span class="nivel">Intermediário</span>
                        <span class="idioma">Português</span>
                        <span class="certificado">✓ Certificado</span>
                    </div>
                    
                    <div class="topicos">
                        <h4>O que você vai aprender:</h4>
                        <ul class="lista-topicos">
                            <li>Requests e BeautifulSoup</li>
                            <li>Selenium para sites dinâmicos</li>
                            <li>Scrapy framework</li>
                            <li>APIs e tratamento de dados</li>
                            <li>Boas práticas e ética</li>
                        </ul>
                    </div>
                    
                    <div class="preco-info">
                        <span class="preco-atual">R$ 149,90</span>
                        <span class="preco-original">R$ 299,90</span>
                        <span class="desconto">50% OFF</span>
                        <span class="promocao-tempo">Oferta limitada!</span>
                    </div>
                </div>
                
                <div class="curso-stats">
                    <span class="estudantes">8.921 estudantes</span>
                    <span class="rating">4.5/5.0</span>
                    <span class="reviews">1.245 reviews</span>
                    <span class="conclusao">85% conclusão</span>
                    <span class="atualizado">Atualizado em Ago/2025</span>
                </div>
                
                <div class="tags-curso">
                    <span class="tag">Web Scraping</span>
                    <span class="tag">Python</span>
                    <span class="tag">BeautifulSoup</span>
                    <span class="tag">Selenium</span>
                    <span class="tag">APIs</span>
                </div>
            </div>

            <!-- Curso 3 -->
            <div class="curso gratuito" data-id="curso-003">
                <header class="curso-header">
                    <h2 class="titulo-curso">Introdução ao JavaScript - Curso Gratuito</h2>
                    <div class="instrutor">
                        <img src="/avatar/carlos.jpg" alt="Carlos Oliveira" class="avatar">
                        <div class="info-instrutor">
                            <span class="nome-instrutor">Carlos Oliveira</span>
                            <span class="titulo-instrutor">Desenvolvedor Full Stack</span>
                            <div class="rating-instrutor">
                                <span class="estrelas">★★★★★</span>
                                <span class="nota">4.9</span>
                                <span class="num-avaliacoes">(3.456 avaliações)</span>
                            </div>
                        </div>
                    </div>
                </header>
                
                <div class="curso-conteudo">
                    <p class="descricao">Curso gratuito completo de JavaScript para iniciantes. Aprenda a programar do zero!</p>
                    
                    <div class="estatisticas">
                        <span class="duracao">15 horas</span>
                        <span class="aulas">45 aulas</span>
                        <span class="nivel">Iniciante</span>
                        <span class="idioma">Português</span>
                        <span class="certificado">✓ Certificado</span>
                    </div>
                    
                    <div class="topicos">
                        <h4>O que você vai aprender:</h4>
                        <ul class="lista-topicos">
                            <li>Sintaxe e fundamentos do JavaScript</li>
                            <li>DOM e manipulação de elementos</li>
                            <li>Eventos e interatividade</li>
                            <li>AJAX e APIs</li>
                            <li>Projetos práticos</li>
                        </ul>
                    </div>
                    
                    <div class="preco-info gratuito">
                        <span class="preco-atual">GRATUITO</span>
                        <span class="promocao-tempo">Sempre gratuito!</span>
                    </div>
                </div>
                
                <div class="curso-stats">
                    <span class="estudantes">45.234 estudantes</span>
                    <span class="rating">4.9/5.0</span>
                    <span class="reviews">5.678 reviews</span>
                    <span class="conclusao">92% conclusão</span>
                    <span class="atualizado">Atualizado em Set/2025</span>
                </div>
                
                <div class="tags-curso">
                    <span class="tag">JavaScript</span>
                    <span class="tag">Frontend</span>
                    <span class="tag">DOM</span>
                    <span class="tag">Web Development</span>
                    <span class="tag">Gratuito</span>
                </div>
            </div>

            <!-- Curso 4 -->
            <div class="curso bestseller" data-id="curso-004">
                <header class="curso-header">
                    <h2 class="titulo-curso">Machine Learning e IA com Python - Bootcamp Completo</h2>
                    <div class="instrutor">
                        <img src="/avatar/ana.jpg" alt="Ana Costa" class="avatar">
                        <div class="info-instrutor">
                            <span class="nome-instrutor">Ana Costa</span>
                            <span class="titulo-instrutor">Cientista de Dados - Google</span>
                            <div class="rating-instrutor">
                                <span class="estrelas">★★★★★</span>
                                <span class="nota">4.8</span>
                                <span class="num-avaliacoes">(2.789 avaliações)</span>
                            </div>
                        </div>
                    </div>
                </header>
                
                <div class="curso-conteudo">
                    <p class="descricao">Bootcamp intensivo de Machine Learning e Inteligência Artificial com projetos reais da indústria.</p>
                    
                    <div class="estatisticas">
                        <span class="duracao">80 horas</span>
                        <span class="aulas">150 aulas</span>
                        <span class="nivel">Avançado</span>
                        <span class="idioma">Português</span>
                        <span class="certificado">✓ Certificado Profissional</span>
                    </div>
                    
                    <div class="topicos">
                        <h4>O que você vai aprender:</h4>
                        <ul class="lista-topicos">
                            <li>Algoritmos de Machine Learning</li>
                            <li>Deep Learning e Redes Neurais</li>
                            <li>TensorFlow e PyTorch</li>
                            <li>Computer Vision e NLP</li>
                            <li>Deploy de modelos em produção</li>
                        </ul>
                    </div>
                    
                    <div class="preco-info">
                        <span class="preco-atual">R$ 599,90</span>
                        <span class="preco-original">R$ 899,90</span>
                        <span class="desconto">33% OFF</span>
                        <span class="promocao-tempo">Black Friday Antecipada!</span>
                    </div>
                </div>
                
                <div class="curso-stats">
                    <span class="estudantes">12.456 estudantes</span>
                    <span class="rating">4.8/5.0</span>
                    <span class="reviews">3.234 reviews</span>
                    <span class="conclusao">78% conclusão</span>
                    <span class="atualizado">Atualizado em Set/2025</span>
                </div>
                
                <div class="tags-curso">
                    <span class="tag">Machine Learning</span>
                    <span class="tag">Deep Learning</span>
                    <span class="tag">TensorFlow</span>
                    <span class="tag">Python</span>
                    <span class="tag">IA</span>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_exemplo

class EducacionalScraper:
    """
    Scraper especializado em plataformas educacionais.
    
    Funcionalidades:
    - Extração de informações de cursos
    - Dados de instrutores e avaliações
    - Monitoramento de preços
    - Análise de conteúdo educacional
    """
    
    def __init__(self, delay_requests=2):
        """
        Inicializa o scraper educacional.
        
        Args:
            delay_requests (int): Delay entre requests em segundos
        """
        self.delay = delay_requests
        self.session = requests.Session()
        
        # Headers apropriados para plataformas educacionais
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; EduBot/1.0; Educational Research)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        self.session.headers.update(self.headers)
    
    def extrair_preco(self, elemento_preco):
        """
        Extrai informações de preço do curso.
        
        Args:
            elemento_preco: Elemento BeautifulSoup com informações de preço
            
        Returns:
            dict: Informações de preço
        """
        preco_info = {
            'atual': 0.0,
            'original': 0.0,
            'desconto_percentual': 0,
            'desconto_texto': None,
            'gratuito': False,
            'promocao': None
        }
        
        if not elemento_preco:
            return preco_info
        
        # Verificar se é gratuito
        if 'gratuito' in elemento_preco.get('class', []) or 'GRATUITO' in elemento_preco.get_text():
            preco_info['gratuito'] = True
            return preco_info
        
        # Extrair preço atual
        preco_atual_elem = elemento_preco.find('span', class_='preco-atual')
        if preco_atual_elem:
            preco_texto = preco_atual_elem.get_text()
            preco_info['atual'] = self.extrair_valor_numerico(preco_texto)
        
        # Extrair preço original
        preco_original_elem = elemento_preco.find('span', class_='preco-original')
        if preco_original_elem:
            preco_texto = preco_original_elem.get_text()
            preco_info['original'] = self.extrair_valor_numerico(preco_texto)
        
        # Extrair desconto
        desconto_elem = elemento_preco.find('span', class_='desconto')
        if desconto_elem:
            desconto_texto = desconto_elem.get_text()
            preco_info['desconto_texto'] = desconto_texto
            
            # Extrair percentual de desconto
            match = re.search(r'(\d+)%', desconto_texto)
            if match:
                preco_info['desconto_percentual'] = int(match.group(1))
        
        # Calcular desconto se não foi informado
        if preco_info['original'] > 0 and preco_info['desconto_percentual'] == 0:
            desconto = preco_info['original'] - preco_info['atual']
            preco_info['desconto_percentual'] = (desconto / preco_info['original']) * 100
        
        # Promoção
        promocao_elem = elemento_preco.find('span', class_='promocao-tempo')
        if promocao_elem:
            preco_info['promocao'] = promocao_elem.get_text().strip()
        
        return preco_info
    
    def extrair_valor_numerico(self, texto_preco):
        """
        Extrai valor numérico de texto de preço.
        
        Args:
            texto_preco (str): Texto contendo preço
            
        Returns:
            float: Valor numérico
        """
        if not texto_preco or 'GRATUITO' in texto_preco.upper():
            return 0.0
        
        # Remove tudo exceto números, vírgula e ponto
        preco_limpo = re.sub(r'[^\d,.]', '', texto_preco)
        
        # Converte formato brasileiro para float
        preco_limpo = preco_limpo.replace('.', '').replace(',', '.')
        
        try:
            return float(preco_limpo)
        except ValueError:
            return 0.0
    
    def extrair_duracao(self, texto_duracao):
        """
        Extrai duração em horas do curso.
        
        Args:
            texto_duracao (str): Texto contendo duração
            
        Returns:
            float: Duração em horas
        """
        if not texto_duracao:
            return 0
        
        # Procurar padrões como "40 horas", "2h30min", etc.
        match = re.search(r'(\d+(?:\.\d+)?)\s*h', texto_duracao.lower())
        if match:
            return float(match.group(1))
        
        return 0
    
    def extrair_rating(self, rating_elem):
        """
        Extrai informações de rating/avaliação.
        
        Args:
            rating_elem: Elemento BeautifulSoup com rating
            
        Returns:
            dict: Informações de rating
        """
        rating_info = {
            'nota': 0.0,
            'estrelas': 0,
            'num_avaliacoes': 0,
            'texto_estrelas': ''
        }
        
        if not rating_elem:
            return rating_info
        
        # Extrair nota numérica
        nota_elem = rating_elem.find('span', class_='nota')
        if nota_elem:
            try:
                rating_info['nota'] = float(nota_elem.get_text().replace(',', '.'))
            except ValueError:
                pass
        
        # Extrair estrelas
        estrelas_elem = rating_elem.find('span', class_='estrelas')
        if estrelas_elem:
            estrelas_texto = estrelas_elem.get_text()
            rating_info['texto_estrelas'] = estrelas_texto
            rating_info['estrelas'] = estrelas_texto.count('★')
        
        # Extrair número de avaliações
        avaliacoes_elem = rating_elem.find('span', class_='num-avaliacoes')
        if avaliacoes_elem:
            avaliacoes_texto = avaliacoes_elem.get_text()
            numeros = re.findall(r'[\d.]+', avaliacoes_texto)
            if numeros:
                rating_info['num_avaliacoes'] = int(numeros[0].replace('.', ''))
        
        return rating_info
    
    def scrape_cursos(self, html_content):
        """
        Extrai informações de cursos de uma plataforma educacional.
        
        Args:
            html_content (str): HTML da página
            
        Returns:
            list: Lista de cursos com informações completas
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        cursos = []
        
        # Encontrar elementos de cursos
        elementos_curso = soup.find_all('div', class_='curso')
        
        print(f"📚 Encontrados {len(elementos_curso)} cursos na página")
        
        for i, curso in enumerate(elementos_curso, 1):
            curso_info = {}
            
            # ID do curso
            curso_info['id'] = curso.get('data-id', f'curso_{i}')
            
            # Identificar tipo especial do curso
            classes_curso = curso.get('class', [])
            curso_info['gratuito'] = 'gratuito' in classes_curso
            curso_info['bestseller'] = 'bestseller' in classes_curso
            
            # Título do curso
            titulo_elem = curso.find(['h1', 'h2'], class_='titulo-curso')
            curso_info['titulo'] = titulo_elem.get_text().strip() if titulo_elem else 'N/A'
            
            # Descrição
            desc_elem = curso.find('p', class_='descricao')
            curso_info['descricao'] = desc_elem.get_text().strip() if desc_elem else 'N/A'
            
            # Informações do instrutor
            instrutor_div = curso.find('div', class_='info-instrutor')
            if instrutor_div:
                nome_elem = instrutor_div.find('span', class_='nome-instrutor')
                curso_info['instrutor_nome'] = nome_elem.get_text().strip() if nome_elem else 'N/A'
                
                titulo_elem = instrutor_div.find('span', class_='titulo-instrutor')
                curso_info['instrutor_titulo'] = titulo_elem.get_text().strip() if titulo_elem else 'N/A'
                
                # Rating do instrutor
                rating_inst = instrutor_div.find('div', class_='rating-instrutor')
                if rating_inst:
                    rating_info = self.extrair_rating(rating_inst)
                    curso_info['instrutor_rating'] = rating_info['nota']
                    curso_info['instrutor_avaliacoes'] = rating_info['num_avaliacoes']
            
            # Estatísticas do curso
            stats_div = curso.find('div', class_='estatisticas')
            if stats_div:
                # Duração
                duracao_elem = stats_div.find('span', class_='duracao')
                if duracao_elem:
                    curso_info['duracao'] = self.extrair_duracao(duracao_elem.get_text())
                    curso_info['duracao_texto'] = duracao_elem.get_text().strip()
                
                # Número de aulas
                aulas_elem = stats_div.find('span', class_='aulas')
                if aulas_elem:
                    aulas_texto = aulas_elem.get_text()
                    numeros = re.findall(r'\d+', aulas_texto)
                    curso_info['num_aulas'] = int(numeros[0]) if numeros else 0
                
                # Nível
                nivel_elem = stats_div.find('span', class_='nivel')
                curso_info['nivel'] = nivel_elem.get_text().strip() if nivel_elem else 'N/A'
                
                # Idioma
                idioma_elem = stats_div.find('span', class_='idioma')
                curso_info['idioma'] = idioma_elem.get_text().strip() if idioma_elem else 'N/A'
                
                # Certificado
                cert_elem = stats_div.find('span', class_='certificado')
                curso_info['certificado'] = '✓' in cert_elem.get_text() if cert_elem else False
            
            # Tópicos do curso
            topicos_ul = curso.find('ul', class_='lista-topicos')
            if topicos_ul:
                topicos_li = topicos_ul.find_all('li')
                curso_info['topicos'] = [li.get_text().strip() for li in topicos_li]
                curso_info['num_topicos'] = len(curso_info['topicos'])
            else:
                curso_info['topicos'] = []
                curso_info['num_topicos'] = 0
            
            # Informações de preço
            preco_div = curso.find('div', class_='preco-info')
            preco_info = self.extrair_preco(preco_div)
            curso_info.update(preco_info)
            
            # Estatísticas do curso (alunos, rating, etc.)
            stats_curso = curso.find('div', class_='curso-stats')
            if stats_curso:
                # Número de estudantes
                estudantes_elem = stats_curso.find('span', class_='estudantes')
                if estudantes_elem:
                    estudantes_texto = estudantes_elem.get_text()
                    numeros = re.findall(r'[\d.]+', estudantes_texto)
                    if numeros:
                        curso_info['estudantes'] = int(numeros[0].replace('.', ''))
                
                # Rating do curso
                rating_elem = stats_curso.find('span', class_='rating')
                if rating_elem:
                    rating_texto = rating_elem.get_text()
                    match = re.search(r'(\d+\.?\d*)', rating_texto)
                    if match:
                        curso_info['curso_rating'] = float(match.group(1))
                
                # Número de reviews
                reviews_elem = stats_curso.find('span', class_='reviews')
                if reviews_elem:
                    reviews_texto = reviews_elem.get_text()
                    numeros = re.findall(r'[\d.]+', reviews_texto)
                    if numeros:
                        curso_info['num_reviews'] = int(numeros[0].replace('.', ''))
                
                # Taxa de conclusão
                conclusao_elem = stats_curso.find('span', class_='conclusao')
                if conclusao_elem:
                    conclusao_texto = conclusao_elem.get_text()
                    match = re.search(r'(\d+)%', conclusao_texto)
                    if match:
                        curso_info['taxa_conclusao'] = int(match.group(1))
                
                # Data de atualização
                atualizado_elem = stats_curso.find('span', class_='atualizado')
                if atualizado_elem:
                    curso_info['atualizado'] = atualizado_elem.get_text().strip()
            
            # Tags do curso
            tags_elems = curso.find_all('span', class_='tag')
            curso_info['tags'] = [tag.get_text().strip() for tag in tags_elems]
            curso_info['num_tags'] = len(curso_info['tags'])
            
            # Calcular métricas derivadas
            if curso_info.get('duracao', 0) > 0 and curso_info.get('num_aulas', 0) > 0:
                curso_info['duracao_por_aula'] = curso_info['duracao'] / curso_info['num_aulas']
            
            if curso_info.get('atual', 0) > 0 and curso_info.get('duracao', 0) > 0:
                curso_info['preco_por_hora'] = curso_info['atual'] / curso_info['duracao']
            
            # Calcular valor por aluno (receita estimada)
            if curso_info.get('estudantes', 0) > 0 and curso_info.get('atual', 0) > 0:
                curso_info['receita_estimada'] = curso_info['estudantes'] * curso_info['atual']
            
            # Timestamp da coleta
            curso_info['coletado_em'] = datetime.now().isoformat()
            
            cursos.append(curso_info)
        
        return cursos
    
    def analisar_mercado_educacional(self, cursos):
        """
        Analisa o mercado educacional com base nos cursos coletados.
        
        Args:
            cursos (list): Lista de cursos
            
        Returns:
            dict: Análise completa do mercado
        """
        if not cursos:
            return {'erro': 'Nenhum curso para analisar'}
        
        df = pd.DataFrame(cursos)
        
        # Separar cursos gratuitos e pagos
        cursos_gratuitos = [c for c in cursos if c.get('gratuito')]
        cursos_pagos = [c for c in cursos if not c.get('gratuito')]
        
        # Análise geral
        analise = {
            'total_cursos': len(cursos),
            'cursos_gratuitos': len(cursos_gratuitos),
            'cursos_pagos': len(cursos_pagos),
            'bestsellers': len([c for c in cursos if c.get('bestseller')]),
            
            # Estatísticas de preço
            'preco_medio': df[df['atual'] > 0]['atual'].mean() if any(df['atual'] > 0) else 0,
            'preco_min': df[df['atual'] > 0]['atual'].min() if any(df['atual'] > 0) else 0,
            'preco_max': df[df['atual'] > 0]['atual'].max() if any(df['atual'] > 0) else 0,
            
            # Estatísticas de conteúdo
            'duracao_media': df['duracao'].mean() if 'duracao' in df else 0,
            'aulas_media': df['num_aulas'].mean() if 'num_aulas' in df else 0,
            
            # Estatísticas de engajamento
            'estudantes_total': df['estudantes'].sum() if 'estudantes' in df else 0,
            'rating_medio': df['curso_rating'].mean() if 'curso_rating' in df else 0,
            'conclusao_media': df['taxa_conclusao'].mean() if 'taxa_conclusao' in df else 0,
        }
        
        # Análise por nível
        if 'nivel' in df.columns:
            niveis = df['nivel'].value_counts().to_dict()
            analise['cursos_por_nivel'] = niveis
        
        # Análise de tags populares
        todas_tags = []
        for curso in cursos:
            todas_tags.extend(curso.get('tags', []))
        
        analise['tecnologias_populares'] = dict(Counter(todas_tags).most_common(10))
        
        # Instrutores mais ativos
        instrutores = [c.get('instrutor_nome', 'N/A') for c in cursos]
        analise['instrutores_ativos'] = dict(Counter(instrutores).most_common(5))
        
        # Curso mais popular
        if 'estudantes' in df.columns and not df['estudantes'].isna().all():
            mais_popular = df.loc[df['estudantes'].idxmax()]
            analise['curso_mais_popular'] = {
                'titulo': mais_popular['titulo'],
                'estudantes': mais_popular['estudantes'],
                'instrutor': mais_popular.get('instrutor_nome', 'N/A')
            }
        
        # Melhor avaliado
        if 'curso_rating' in df.columns and not df['curso_rating'].isna().all():
            melhor_avaliado = df.loc[df['curso_rating'].idxmax()]
            analise['melhor_avaliado'] = {
                'titulo': melhor_avaliado['titulo'],
                'rating': melhor_avaliado['curso_rating'],
                'reviews': melhor_avaliado.get('num_reviews', 0)
            }
        
        # Maior desconto
        cursos_com_desconto = [c for c in cursos if c.get('desconto_percentual', 0) > 0]
        if cursos_com_desconto:
            maior_desconto = max(cursos_com_desconto, key=lambda x: x['desconto_percentual'])
            analise['maior_desconto'] = {
                'titulo': maior_desconto['titulo'],
                'desconto': maior_desconto['desconto_percentual'],
                'preco_atual': maior_desconto['atual'],
                'preco_original': maior_desconto['original']
            }
        
        # Receita total estimada
        if cursos_pagos:
            receita_total = sum(c.get('receita_estimada', 0) for c in cursos_pagos)
            analise['receita_estimada_total'] = receita_total
        
        return analise

def exemplo_uso():
    """Demonstra o uso prático do EducacionalScraper."""
    print("🎓 === EXEMPLO DE SCRAPING EDUCACIONAL ===")
    print("=" * 55)
    
    # Inicializar scraper
    scraper = EducacionalScraper(delay_requests=1)
    
    # Simular plataforma educacional
    print("1️⃣ Obtendo dados da plataforma educacional...")
    html_content = simular_plataforma_educacional()
    
    # Extrair cursos
    print("2️⃣ Extraindo informações dos cursos...")
    cursos = scraper.scrape_cursos(html_content)
    
    # Exibir cursos encontrados
    print(f"\n📚 === CURSOS ENCONTRADOS ({len(cursos)}) ===")
    for i, curso in enumerate(cursos, 1):
        status_badges = []
        if curso.get('gratuito'):
            status_badges.append('🆓 GRATUITO')
        if curso.get('bestseller'):
            status_badges.append('🏆 BESTSELLER')
        
        badges = ' '.join(status_badges) if status_badges else ''
        
        print(f"\n📖 Curso {i}: {curso['titulo']} {badges}")
        print(f"   👨‍🏫 {curso.get('instrutor_nome', 'N/A')} - {curso.get('instrutor_titulo', 'N/A')}")
        
        if curso.get('gratuito'):
            print(f"   💰 GRATUITO")
        else:
            print(f"   💰 R$ {curso.get('atual', 0):.2f}", end='')
            if curso.get('original', 0) > 0:
                print(f" (era R$ {curso['original']:.2f} - {curso.get('desconto_percentual', 0):.0f}% OFF)")
            else:
                print()
        
        print(f"   ⏱️  {curso.get('duracao_texto', 'N/A')} | 📼 {curso.get('num_aulas', 0)} aulas")
        print(f"   🎯 Nível: {curso.get('nivel', 'N/A')} | 🌐 {curso.get('idioma', 'N/A')}")
        print(f"   ⭐ {curso.get('curso_rating', 0):.1f}/5.0 ({curso.get('num_reviews', 0):,} reviews)")
        print(f"   👥 {curso.get('estudantes', 0):,} estudantes")
        print(f"   📊 {curso.get('taxa_conclusao', 0)}% conclusão")
        
        if curso.get('certificado'):
            print(f"   🎖️  Inclui certificado")
        
        if curso.get('tags'):
            print(f"   🏷️  Tags: {', '.join(curso['tags'][:5])}")
        
        if curso.get('preco_por_hora', 0) > 0:
            print(f"   📈 R$ {curso['preco_por_hora']:.2f} por hora")
    
    # Análise do mercado
    print(f"\n📊 === ANÁLISE DO MERCADO EDUCACIONAL ===")
    analise = scraper.analisar_mercado_educacional(cursos)
    
    print(f"📚 Total de cursos: {analise['total_cursos']}")
    print(f"🆓 Cursos gratuitos: {analise['cursos_gratuitos']}")
    print(f"💰 Cursos pagos: {analise['cursos_pagos']}")
    print(f"🏆 Bestsellers: {analise['bestsellers']}")
    
    if analise['preco_medio'] > 0:
        print(f"💵 Preço médio: R$ {analise['preco_medio']:.2f}")
        print(f"💸 Faixa de preços: R$ {analise['preco_min']:.2f} - R$ {analise['preco_max']:.2f}")
    
    print(f"⏱️  Duração média: {analise['duracao_media']:.1f} horas")
    print(f"📼 Aulas por curso: {analise['aulas_media']:.0f} em média")
    print(f"👥 Total de estudantes: {analise['estudantes_total']:,}")
    print(f"⭐ Rating médio: {analise['rating_medio']:.1f}/5.0")
    print(f"📊 Taxa média de conclusão: {analise['conclusao_media']:.1f}%")
    
    # Tecnologias populares
    if analise.get('tecnologias_populares'):
        print(f"\n🔥 Tecnologias mais populares:")
        for tech, count in list(analise['tecnologias_populares'].items())[:5]:
            print(f"   • {tech}: {count} cursos")
    
    # Cursos por nível
    if analise.get('cursos_por_nivel'):
        print(f"\n🎯 Distribuição por nível:")
        for nivel, count in analise['cursos_por_nivel'].items():
            print(f"   • {nivel}: {count} cursos")
    
    # Destaque: curso mais popular
    if analise.get('curso_mais_popular'):
        popular = analise['curso_mais_popular']
        print(f"\n👑 Curso mais popular:")
        print(f"   📚 {popular['titulo']}")
        print(f"   👥 {popular['estudantes']:,} estudantes")
        print(f"   👨‍🏫 {popular['instrutor']}")
    
    # Destaque: melhor avaliado
    if analise.get('melhor_avaliado'):
        melhor = analise['melhor_avaliado']
        print(f"\n⭐ Melhor avaliado:")
        print(f"   📚 {melhor['titulo']}")
        print(f"   🌟 {melhor['rating']:.1f}/5.0 ({melhor['reviews']:,} reviews)")
    
    # Destaque: maior desconto
    if analise.get('maior_desconto'):
        desconto = analise['maior_desconto']
        print(f"\n💸 Maior desconto:")
        print(f"   📚 {desconto['titulo']}")
        print(f"   🏷️  {desconto['desconto']:.0f}% OFF")
        print(f"   💰 R$ {desconto['preco_atual']:.2f} (era R$ {desconto['preco_original']:.2f})")
    
    # Receita estimada
    if analise.get('receita_estimada_total', 0) > 0:
        print(f"\n💰 Receita estimada total: R$ {analise['receita_estimada_total']:,.2f}")
    
    # Salvar dados
    print(f"\n💾 Salvando dados...")
    df = pd.DataFrame(cursos)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # CSV dos cursos
    filename_csv = f"cursos_educacionais_{timestamp}.csv"
    df.to_csv(filename_csv, index=False, encoding='utf-8')
    print(f"✅ Cursos salvos em: {filename_csv}")
    
    # JSON da análise
    filename_json = f"analise_mercado_educacional_{timestamp}.json"
    with open(filename_json, 'w', encoding='utf-8') as f:
        json.dump(analise, f, ensure_ascii=False, indent=2, default=str)
    print(f"✅ Análise salva em: {filename_json}")
    
    # Aplicações práticas
    print(f"\n💡 === APLICAÇÕES PRÁTICAS ===")
    aplicacoes = [
        "💰 Monitoramento de preços de cursos",
        "📊 Análise de mercado educacional",
        "🎯 Recomendação personalizada de cursos",
        "📈 Tracking de tendências tecnológicas",
        "👨‍🏫 Análise de performance de instrutores",
        "🏆 Identificação de cursos populares",
        "💸 Alertas de promoções e descontos",
        "📚 Curadoria automática de conteúdo"
    ]
    
    for app in aplicacoes:
        print(f"   {app}")
    
    print(f"\n🔧 === DICAS PARA PRODUÇÃO ===")
    dicas = [
        "⚖️  Respeite termos de uso das plataformas",
        "⏱️  Use delays apropriados entre requests",
        "🔐 Configure autenticação se necessário",
        "📊 Implemente cache para dados históricos",
        "🎓 Monitore qualidade dos dados extraídos",
        "📧 Configure alertas para cursos novos",
        "💾 Use banco de dados para persistência",
        "🤖 Implemente detecção de mudanças de layout"
    ]
    
    for dica in dicas:
        print(f"   {dica}")

if __name__ == "__main__":
    exemplo_uso()