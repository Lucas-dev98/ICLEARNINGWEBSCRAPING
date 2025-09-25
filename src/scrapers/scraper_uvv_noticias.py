#!/usr/bin/env python3
"""
Scraper Específico para Notícias da UVV - Setembro 2025
=======================================================

Este script coleta especificamente as notícias da Universidade Vila Velha (UVV)
do mês de setembro de 2025, incluindo todas as notícias do portal Inova UVV.

Funcionalidades:
- Coleta de notícias do site oficial da UVV
- Filtragem por data (setembro 2025)
- Extração de dados completos (título, data, resumo, link)
- Tratamento de datas com biblioteca datetime
- Requisições HTTP com biblioteca requests
- Exportação para CSV e JSON

Autor: ICLearning WebScraping Project
Data: 2025-09-24
URL Alvo: https://www.uvv.br/noticias/
"""

# === IMPORTAÇÕES NECESSÁRIAS ===
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import csv
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import time
import re
from collections import defaultdict

class UVVNoticiasScraper:
    """
    Scraper especializado para notícias da UVV (Universidade Vila Velha).
    
    Coleta notícias do portal oficial da UVV com foco em:
    - Notícias do mês de setembro 2025
    - Notícias do portal Inova UVV
    - Metadados completos de cada notícia
    """
    
    def __init__(self):
        """Inicializa o scraper da UVV com configurações específicas."""
        self.base_url = "https://www.uvv.br"
        self.noticias_url = "https://www.uvv.br/noticias/"
        
        # Headers para parecer um navegador real
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Session para manter cookies e conexões
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Armazenamento das notícias coletadas
        self.noticias = []
        
        # Data alvo: setembro 2025
        self.mes_alvo = 9
        self.ano_alvo = 2025
        
        # Timestamp do início do scraping
        self.timestamp_scraping = datetime.now()
        
        print(f"🎓 UVV Notícias Scraper inicializado")
        print(f"📅 Coletando notícias de setembro/{self.ano_alvo}")
        print(f"🕐 Scraping iniciado em: {self.timestamp_scraping.strftime('%d/%m/%Y %H:%M:%S')}")
    
    def fazer_requisicao(self, url, timeout=30):
        """
        Faz requisição HTTP com tratamento de erros.
        
        Args:
            url (str): URL para requisição
            timeout (int): Timeout em segundos
            
        Returns:
            requests.Response or None: Resposta ou None se erro
        """
        try:
            print(f"🔍 Fazendo requisição: {url}")
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            
            print(f"✅ Status: {response.status_code} | Tamanho: {len(response.content)} bytes")
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na requisição para {url}: {e}")
            return None
    
    def extrair_data_noticia(self, elemento_data):
        """
        Extrai e converte data da notícia para objeto datetime.
        
        Args:
            elemento_data: Elemento HTML contendo a data
            
        Returns:
            datetime or None: Data convertida ou None se não conseguir
        """
        if not elemento_data:
            return None
        
        texto_data = elemento_data.get_text().strip()
        
        # Padrões de data comuns em sites brasileiros
        padroes_data = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})',  # dd/mm/yyyy ou d/m/yyyy
            r'(\d{1,2})-(\d{1,2})-(\d{4})',  # dd-mm-yyyy
            r'(\d{4})-(\d{1,2})-(\d{1,2})',  # yyyy-mm-dd
            r'(\d{1,2}) de (\w+) de (\d{4})', # dd de mês de yyyy
        ]
        
        # Mapeamento de meses em português
        meses_pt = {
            'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
            'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
            'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
        }
        
        for padrao in padroes_data:
            match = re.search(padrao, texto_data.lower())
            if match:
                try:
                    if 'de' in padrao:  # Formato "dd de mês de yyyy"
                        dia, mes_nome, ano = match.groups()
                        mes = meses_pt.get(mes_nome.lower())
                        if mes:
                            return datetime(int(ano), mes, int(dia))
                    else:
                        grupos = match.groups()
                        if padrao.startswith(r'(\d{4})'):  # yyyy-mm-dd
                            ano, mes, dia = grupos
                        else:  # dd/mm/yyyy ou dd-mm-yyyy
                            dia, mes, ano = grupos
                        
                        return datetime(int(ano), int(mes), int(dia))
                
                except ValueError:
                    continue
        
        return None
    
    def eh_noticia_setembro(self, data_noticia):
        """
        Verifica se a notícia é do mês de setembro 2025.
        
        Args:
            data_noticia (datetime): Data da notícia
            
        Returns:
            bool: True se for de setembro 2025
        """
        if not data_noticia:
            return False
        
        return (data_noticia.month == self.mes_alvo and 
                data_noticia.year == self.ano_alvo)
    
    def extrair_noticias_pagina(self, html_content, url_pagina):
        """
        Extrai notícias de uma página específica.
        
        Args:
            html_content (str): HTML da página
            url_pagina (str): URL da página atual
            
        Returns:
            list: Lista de notícias extraídas
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        noticias_pagina = []
        
        print(f"📄 Analisando página: {url_pagina}")
        
        # Seletores específicos para o site da UVV baseados na estrutura observada
        seletores_noticias = [
            # Seletores específicos da UVV
            '.col-md-3',  # Cards de notícias na grid
            '.card',      # Cards individuais
            '.row .col-md-3',  # Colunas com notícias
            'div[class*="col-"]',  # Qualquer coluna
            
            # Seletores gerais
            'article',
            '.noticia',
            '.news',
            '.post', 
            '.entry',
            '.item-noticia',
            '.news-item',
            'div[class*="noticia"]',
            'div[class*="news"]'
        ]
        
        elementos_encontrados = []
        
        # Buscar elementos com diferentes seletores
        for seletor in seletores_noticias:
            elementos = soup.select(seletor)
            elementos_encontrados.extend(elementos)
        
        # Estratégia mais agressiva: buscar por divs que contenham imagens + títulos
        if not elementos_encontrados:
            divs_com_imagem = soup.find_all('div', lambda x: x and x.find('img'))
            for div in divs_com_imagem:
                # Verificar se tem título (h1, h2, h3, h4, h5, h6, a)
                if div.find(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a']):
                    elementos_encontrados.append(div)
        
        # Buscar por links que contenham texto longo (possíveis títulos de notícias)
        links_noticias = soup.find_all('a', href=True)
        for link in links_noticias:
            texto_link = link.get_text().strip()
            if len(texto_link) > 20 and ('inova' in texto_link.lower() or 'uvv' in texto_link.lower()):
                # Encontrar o container pai do link
                container = link.find_parent(['div', 'article', 'section'])
                if container and container not in elementos_encontrados:
                    elementos_encontrados.append(container)
        
        print(f"🔍 Encontrados {len(elementos_encontrados)} elementos candidatos a notícias")
        
        for i, elemento in enumerate(elementos_encontrados):
            try:
                noticia = self.processar_elemento_noticia(elemento, url_pagina)
                if noticia:
                    noticias_pagina.append(noticia)
            except Exception as e:
                print(f"⚠️ Erro ao processar elemento {i}: {e}")
                continue
        
        return noticias_pagina
    
    def processar_elemento_noticia(self, elemento, url_pagina):
        """
        Processa um elemento individual de notícia.
        
        Args:
            elemento: Elemento BeautifulSoup
            url_pagina (str): URL da página atual
            
        Returns:
            dict or None: Dados da notícia ou None se inválida
        """
        noticia = {
            'titulo': '',
            'resumo': '',
            'data_publicacao': None,
            'data_publicacao_texto': '',
            'link': '',
            'categoria': '',
            'autor': '',
            'tags': [],
            'eh_inova': False,
            'url_fonte': url_pagina,
            'timestamp_coleta': self.timestamp_scraping.isoformat(),
            'conteudo_completo': '',
            'imagens': [],
            'videos': [],
            'links_relacionados': []
        }
        
        # Extrair título
        titulo_elem = None
        for seletor in ['h1', 'h2', 'h3', '.titulo', '.title', '.headline', 'a']:
            titulo_elem = elemento.find(seletor)
            if titulo_elem:
                break
        
        if titulo_elem:
            noticia['titulo'] = titulo_elem.get_text().strip()
        
        # Filtrar títulos muito curtos ou vazios
        if len(noticia['titulo']) < 10:
            return None
        
        # Verificar se é notícia do Inova UVV (com mais palavras-chave)
        texto_completo = elemento.get_text().lower()
        palavras_inova = [
            'inovaweek', 'inova week', 'inova', 'inovação', 'pesquisa', 'ciência',
            'tecnologia', 'inovador', 'startup', 'empreendedorismo', 'desenvolvimento',
            'projeto', 'laboratório', 'extensão'
        ]
        if any(palavra in texto_completo for palavra in palavras_inova):
            noticia['eh_inova'] = True
        
        # Extrair link
        link_elem = elemento.find('a')
        if link_elem and link_elem.get('href'):
            link = link_elem.get('href')
            if link.startswith('/'):
                link = urljoin(self.base_url, link)
            noticia['link'] = link
        
        # Extrair resumo/descrição
        resumo_selectors = ['.resumo', '.excerpt', '.description', 'p', '.lead']
        for seletor in resumo_selectors:
            resumo_elem = elemento.find(seletor)
            if resumo_elem:
                resumo_texto = resumo_elem.get_text().strip()
                if len(resumo_texto) > 20 and len(resumo_texto) < 500:
                    noticia['resumo'] = resumo_texto
                    break
        
        # Extrair data
        data_selectors = ['.data', '.date', '.published', '.time', 'time']
        for seletor in data_selectors:
            data_elem = elemento.find(seletor)
            if data_elem:
                noticia['data_publicacao_texto'] = data_elem.get_text().strip()
                data_convertida = self.extrair_data_noticia(data_elem)
                if data_convertida:
                    noticia['data_publicacao'] = data_convertida
                    break
        
        # Se não encontrou data específica, tentar extrair do texto e atributos
        if not noticia['data_publicacao']:
            texto_elemento = elemento.get_text()
            
            # Buscar atributos datetime, data-date, etc.
            for elem in elemento.find_all(['time', 'span', 'div']):
                for attr in ['datetime', 'data-date', 'data-time', 'data-created']:
                    if elem.get(attr):
                        data_attr = elem.get(attr)
                        try:
                            # Tentar parsear ISO format
                            if 'T' in data_attr:
                                data_encontrada = datetime.fromisoformat(data_attr.replace('Z', ''))
                                noticia['data_publicacao'] = data_encontrada
                                noticia['data_publicacao_texto'] = data_encontrada.strftime('%d/%m/%Y')
                                break
                        except ValueError:
                            continue
                if noticia['data_publicacao']:
                    break
            
            # Se ainda não encontrou, buscar padrões de data no texto
            if not noticia['data_publicacao']:
                padroes_texto = [
                    r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})',  # dd/mm/yyyy
                    r'(\d{1,2}) de (\w+) de (\d{4})',          # dd de mês de yyyy
                    r'(\d{1,2})\.(\d{1,2})\.(\d{4})',          # dd.mm.yyyy
                    r'setembro de (\d{4})',                     # setembro de yyyy
                    r'(\d{4})-(\d{1,2})-(\d{1,2})'             # yyyy-mm-dd
                ]
                
                for padrao in padroes_texto:
                    match = re.search(padrao, texto_elemento.lower())
                    if match:
                        try:
                            if 'setembro de' in padrao:
                                ano = int(match.group(1))
                                # Assumir dia 1 de setembro
                                data_encontrada = datetime(ano, 9, 1)
                            elif 'de' in padrao:
                                dia, mes_nome, ano = match.groups()
                                meses_pt = {
                                    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
                                    'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
                                    'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
                                }
                                mes = meses_pt.get(mes_nome.lower())
                                if mes:
                                    data_encontrada = datetime(int(ano), mes, int(dia))
                            else:
                                grupos = match.groups()
                                if padrao.startswith(r'(\d{4})'):  # yyyy-mm-dd
                                    ano, mes, dia = grupos
                                else:  # dd/mm/yyyy variants
                                    dia, mes, ano = grupos
                                data_encontrada = datetime(int(ano), int(mes), int(dia))
                            
                            noticia['data_publicacao'] = data_encontrada
                            noticia['data_publicacao_texto'] = data_encontrada.strftime('%d/%m/%Y')
                            break
                        except ValueError:
                            continue
        
        # Verificar se é de setembro 2025 (mais flexível para incluir notícias sem data)
        if noticia['data_publicacao'] and not self.eh_noticia_setembro(noticia['data_publicacao']):
            # Se tem data mas não é de setembro, verificar se é notícia do Inova (pode ser relevante)
            if not noticia['eh_inova']:
                print(f"📅 Notícia de {noticia['data_publicacao'].strftime('%m/%Y')} - pulando (fora de setembro/2025)")
                return None
            else:
                print(f"🔬 Notícia Inova de {noticia['data_publicacao'].strftime('%m/%Y')} - incluindo mesmo fora de setembro")
        elif not noticia['data_publicacao']:
            print(f"📅 Notícia sem data identificada - incluindo para análise manual")
        
        # Extrair categoria
        categoria_selectors = ['.categoria', '.category', '.tag']
        for seletor in categoria_selectors:
            cat_elem = elemento.find(seletor)
            if cat_elem:
                noticia['categoria'] = cat_elem.get_text().strip()
                break
        
        # Extrair autor
        autor_selectors = ['.autor', '.author', '.by']
        for seletor in autor_selectors:
            autor_elem = elemento.find(seletor)
            if autor_elem:
                noticia['autor'] = autor_elem.get_text().strip()
                break
        
        # Se é uma notícia do InovaWeek, extrair conteúdo completo
        if noticia['eh_inova'] and noticia['link']:
            print(f"🔬 Coletando conteúdo completo da notícia Inova: {noticia['titulo'][:50]}...")
            conteudo_completo = self.extrair_conteudo_completo(noticia['link'])
            if conteudo_completo:
                noticia.update(conteudo_completo)
        
        return noticia
    
    def extrair_conteudo_completo(self, url_noticia):
        """
        Extrai o conteúdo completo de uma página de notícia específica da UVV.
        
        Args:
            url_noticia (str): URL da notícia específica
            
        Returns:
            dict: Conteúdo completo extraído ou None se erro
        """
        try:
            print(f"📄 Acessando página completa: {url_noticia}")
            
            # Aguardar um pouco para não sobrecarregar o servidor
            time.sleep(1)
            
            response = self.fazer_requisicao(url_noticia)
            if not response:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            conteudo = {
                'conteudo_completo': '',
                'imagens': [],
                'videos': [],
                'links_relacionados': []
            }
            
            # PRIMEIRO: Remover elementos que sabemos ser desnecessários
            elementos_para_remover = [
                'script', 'style', 'noscript', 'iframe[src*="facebook"]', 
                'iframe[src*="twitter"]', 'iframe[src*="instagram"]',
                'nav', 'header', 'footer', 'aside',
                '.menu', '.navigation', '.nav', '.breadcrumb', '.sidebar',
                '.social-share', '.comments', '.related-posts', '.widget',
                '.advertisement', '.ads', '.cookie-notice', '.newsletter'
            ]
            
            for seletor in elementos_para_remover:
                for elemento in soup.select(seletor):
                    elemento.decompose()
            
            # Extrair conteúdo principal do artigo com seletores específicos da UVV
            conteudo_selectors = [
                # Seletores específicos da UVV
                '.single-post .entry-content',
                '.post-content .entry-content',
                '.news-content',
                '.noticia-texto',
                '.article-body',
                '.post-body',
                '.entry-text',
                
                # Seletores mais específicos primeiro  
                '.post-content',
                '.entry-content',
                '.article-content',
                '.content-area',
                '.single-post-content',
                '.wp-block-group__inner-container',
                '.entry-summary',
                
                # Seletores genéricos
                '.content',
                '.noticia-content',
                '.texto',
                '.texto-noticia',
                'main article',
                '.main-content',
                '[class*="content"]',
                'article',
                'main'
            ]
            
            conteudo_texto = ""
            print(f"   🔍 Tentando extrair conteúdo com seletores específicos...")
            
            for seletor in conteudo_selectors:
                elemento_conteudo = soup.select_one(seletor)
                if elemento_conteudo:
                    print(f"   ✅ Encontrou elemento com seletor: {seletor}")
                    
                    # Fazer uma cópia para não modificar o original
                    elemento_temp = BeautifulSoup(str(elemento_conteudo), 'html.parser')
                    
                    # Remover elementos específicos que aparecem em páginas da UVV
                    elementos_indesejaveis = [
                        'script', 'style', 'nav', 'header', 'footer', 'aside', 'form',
                        '.menu', '.navigation', '.breadcrumb', '.sidebar', '.widget',
                        '.social-media', '.share-buttons', '.tags', '.categories',
                        '.author-info', '.related-posts', '.comments-section'
                    ]
                    
                    for seletor_remover in elementos_indesejaveis:
                        for elem in elemento_temp.select(seletor_remover):
                            elem.decompose()
                    
                    # Extrair texto preservando estrutura de parágrafos
                    paragrafos = elemento_temp.find_all(['p', 'div', 'span'], string=True)
                    textos_paragrafos = []
                    
                    for p in paragrafos:
                        texto_p = p.get_text().strip()
                        if (texto_p and 
                            len(texto_p) > 20 and 
                            not self._eh_linha_menu(texto_p) and
                            not self._eh_texto_navegacao_uvv(texto_p)):
                            textos_paragrafos.append(texto_p)
                    
                    # Se encontrou parágrafos válidos, usar eles
                    if textos_paragrafos and len('\n\n'.join(textos_paragrafos)) > 200:
                        conteudo_texto = '\n\n'.join(textos_paragrafos)
                        print(f"   ✅ Conteúdo extraído com {len(textos_paragrafos)} parágrafos")
                        break
                    
                    # Senão, tentar extração simples mas filtrada
                    else:
                        conteudo_bruto = elemento_temp.get_text(separator='\n', strip=True)
                        linhas = [linha.strip() for linha in conteudo_bruto.split('\n') if linha.strip()]
                        linhas_relevantes = []
                        
                        for linha in linhas:
                            if (len(linha) > 15 and 
                                not self._eh_linha_menu(linha) and
                                not self._eh_texto_navegacao_uvv(linha)):
                                linhas_relevantes.append(linha)
                        
                        if len(linhas_relevantes) >= 3 and len('\n'.join(linhas_relevantes)) > 200:
                            conteudo_texto = '\n'.join(linhas_relevantes)
                            print(f"   ✅ Conteúdo extraído com {len(linhas_relevantes)} linhas filtradas")
                            break
            
            # Se não encontrou com seletores específicos, tentar estratégias mais inteligentes
            if not conteudo_texto or len(conteudo_texto) < 200:
                print(f"   🔍 Tentando estratégias alternativas para extrair conteúdo...")
                
                # Estratégia 1: Procurar especificamente por parágrafos longos e relevantes
                paragrafos_relevantes = []
                for p in soup.find_all('p'):
                    texto_p = p.get_text().strip()
                    if (len(texto_p) > 80 and  # Parágrafos mais longos
                        not self._eh_linha_menu(texto_p) and
                        not self._eh_texto_navegacao_uvv(texto_p) and
                        not any(palavra in texto_p.lower() for palavra in [
                            'copyright', '©', 'todos os direitos', 'reserved', 'política de privacidade',
                            'termos de uso', 'cookies', 'desenvolvido por'
                        ])):
                        # Verificar se o parágrafo tem conteúdo substantivo
                        palavras = texto_p.split()
                        if len(palavras) >= 10:  # Pelo menos 10 palavras
                            paragrafos_relevantes.append(texto_p)
                
                if paragrafos_relevantes and len('\n\n'.join(paragrafos_relevantes)) > 200:
                    conteudo_texto = '\n\n'.join(paragrafos_relevantes)
                    print(f"   ✅ Conteúdo extraído de {len(paragrafos_relevantes)} parágrafos relevantes")
                
                # Estratégia 2: Procurar por divs/sections com densidade alta de texto
                if not conteudo_texto or len(conteudo_texto) < 200:
                    print(f"   🔍 Analisando densidade de texto em containers...")
                    
                    candidatos_conteudo = []
                    for container in soup.find_all(['div', 'section', 'article']):
                        # Pular containers que são claramente navegação
                        if any(classe in str(container.get('class', [])).lower() 
                               for classe in ['menu', 'nav', 'header', 'footer', 'sidebar', 'widget']):
                            continue
                        
                        # Extrair texto do container
                        texto_container = container.get_text(separator=' ', strip=True)
                        palavras = texto_container.split()
                        
                        # Calcular métricas de qualidade do conteúdo
                        if len(palavras) >= 50:  # Pelo menos 50 palavras
                            # Verificar se não é majoritariamente navegação
                            linhas_texto = [l.strip() for l in texto_container.split('\n') if l.strip()]
                            linhas_navegacao = sum(1 for linha in linhas_texto 
                                                 if self._eh_texto_navegacao_uvv(linha) or self._eh_linha_menu(linha))
                            
                            # Se menos de 30% é navegação, é um bom candidato
                            if len(linhas_texto) > 0 and (linhas_navegacao / len(linhas_texto)) < 0.3:
                                candidatos_conteudo.append((container, len(palavras), texto_container))
                    
                    # Pegar o container com mais palavras (mais provável de ser o conteúdo principal)
                    if candidatos_conteudo:
                        melhor_container = max(candidatos_conteudo, key=lambda x: x[1])
                        conteudo_bruto = melhor_container[2]
                        
                        # Filtrar o conteúdo linha por linha
                        linhas_filtradas = []
                        for linha in conteudo_bruto.split('\n'):
                            linha = linha.strip()
                            if (linha and 
                                len(linha) > 20 and
                                not self._eh_linha_menu(linha) and
                                not self._eh_texto_navegacao_uvv(linha)):
                                linhas_filtradas.append(linha)
                        
                        if linhas_filtradas and len('\n'.join(linhas_filtradas)) > 200:
                            conteudo_texto = '\n'.join(linhas_filtradas)
                            print(f"   ✅ Conteúdo extraído do melhor container ({melhor_container[1]} palavras)")
                
                # Estratégia 3: Fallback - buscar qualquer texto estruturado
                if not conteudo_texto or len(conteudo_texto) < 200:
                    print(f"   🔍 Estratégia fallback - busca de texto estruturado...")
                    
                    # Procurar por qualquer elemento que tenha texto longo e não seja navegação
                    elementos_texto = soup.find_all(['div', 'section', 'article', 'main'])
                    for elemento in elementos_texto:
                        if elemento.name in ['script', 'style', 'nav', 'header', 'footer']:
                            continue
                        
                        texto_elemento = elemento.get_text(separator='\n', strip=True)
                        linhas = [linha.strip() for linha in texto_elemento.split('\n') if linha.strip()]
                        
                        # Filtrar linhas relevantes
                        linhas_relevantes = []
                        for linha in linhas:
                            if (len(linha) > 25 and 
                                not self._eh_linha_menu(linha) and
                                not self._eh_texto_navegacao_uvv(linha)):
                                linhas_relevantes.append(linha)
                        
                        # Se encontrou conteúdo relevante suficiente, usar
                        if len(linhas_relevantes) >= 5 and len('\n'.join(linhas_relevantes)) > 300:
                            conteudo_texto = '\n'.join(linhas_relevantes)
                            print(f"   ✅ Conteúdo extraído com estratégia fallback ({len(linhas_relevantes)} linhas)")
                            break
            
            conteudo['conteudo_completo'] = conteudo_texto
            
            # Extrair imagens relacionadas à notícia
            imagens = []
            for img in soup.find_all('img'):
                src = img.get('src')
                alt = img.get('alt', '')
                title = img.get('title', '')
                
                if src:
                    if src.startswith('/'):
                        src = urljoin(self.base_url, src)
                    
                    # Filtrar imagens muito pequenas (provavelmente ícones)
                    width = img.get('width')
                    height = img.get('height')
                    
                    if width and height:
                        try:
                            if int(width) < 50 or int(height) < 50:
                                continue
                        except ValueError:
                            pass
                    
                    # Filtrar imagens de logos e ícones comuns
                    if any(palavra in src.lower() for palavra in ['logo', 'icon', 'favicon', 'button']):
                        continue
                    
                    imagem_info = {
                        'src': src,
                        'alt': alt,
                        'title': title
                    }
                    
                    if imagem_info not in imagens:
                        imagens.append(imagem_info)
            
            conteudo['imagens'] = imagens[:10]  # Limitar a 10 imagens
            
            # Extrair vídeos (YouTube, Vimeo, etc.)
            videos = []
            
            # iframes de vídeo
            for iframe in soup.find_all('iframe'):
                src = iframe.get('src', '')
                if any(plataforma in src.lower() for plataforma in ['youtube', 'vimeo', 'dailymotion']):
                    videos.append({
                        'src': src,
                        'tipo': 'iframe',
                        'titulo': iframe.get('title', '')
                    })
            
            # Tags de vídeo HTML5
            for video in soup.find_all('video'):
                src = video.get('src')
                if src:
                    if src.startswith('/'):
                        src = urljoin(self.base_url, src)
                    videos.append({
                        'src': src,
                        'tipo': 'video',
                        'titulo': video.get('title', '')
                    })
            
            conteudo['videos'] = videos
            
            # Extrair links relacionados dentro do conteúdo
            links_relacionados = []
            for link in soup.find_all('a', href=True):
                href = link.get('href')
                texto_link = link.get_text().strip()
                
                # Filtrar apenas links internos da UVV ou links relevantes
                if (href.startswith('/') or 'uvv.br' in href) and len(texto_link) > 10:
                    if href.startswith('/'):
                        href = urljoin(self.base_url, href)
                    
                    link_info = {
                        'url': href,
                        'texto': texto_link
                    }
                    
                    if link_info not in links_relacionados:
                        links_relacionados.append(link_info)
            
            conteudo['links_relacionados'] = links_relacionados[:5]  # Limitar a 5 links
            
            print(f"✅ Conteúdo extraído: {len(conteudo_texto)} caracteres, {len(imagens)} imagens, {len(videos)} vídeos")
            
            return conteudo
            
        except Exception as e:
            print(f"❌ Erro ao extrair conteúdo completo de {url_noticia}: {e}")
            return None
    
    def _eh_linha_menu(self, linha):
        """
        Verifica se uma linha de texto parece ser de menu/navegação.
        
        Args:
            linha (str): Linha de texto para verificar
            
        Returns:
            bool: True se parecer ser linha de menu
        """
        # Palavras típicas de menu e navegação
        palavras_menu = [
            'institucional', 'cpa', 'trabalhe conosco', 'graduação', 'pós graduação',
            'mestrado', 'doutorado', 'capacitação', 'pesquisa', 'extensão',
            'serviços', 'comunidade', 'quero abrir', 'saiba mais', 'notícias',
            'eventos', 'blog', 'contato', 'portal', 'manual', 'diploma',
            'bolsas', 'financiamentos', 'a uvv', 'cursos', 'residência'
        ]
        
        linha_lower = linha.lower()
        
        # Verificar se é linha muito curta (típico de menu)
        if len(linha) < 5:
            return True
        
        # Verificar se contém palavras de menu
        if any(palavra in linha_lower for palavra in palavras_menu):
            return True
        
        # Verificar se é apenas uma palavra ou palavras muito curtas
        palavras = linha.split()
        if len(palavras) <= 2 and all(len(palavra) < 15 for palavra in palavras):
            return True
        
        return False
    
    def _eh_texto_navegacao_uvv(self, texto):
        """
        Verifica se o texto é específicamente de navegação/menu do site da UVV.
        
        Args:
            texto (str): Texto para verificar
            
        Returns:
            bool: True se for texto de navegação da UVV
        """
        # Textos específicos que aparecem na navegação da UVV
        textos_navegacao_uvv = [
            'A UVV',
            'Institucional',
            'CPA', 
            'Manual da marca',
            'Trabalhe conosco',
            'Cursos',
            'Graduação',
            'MBA e Pós Graduação',
            'Residência',
            'Mestrado e Doutorado',
            'Capacitação',
            'Pesquisa e extensão',
            'Pesquisa',
            'Extensão',
            'Serviços para a comunidade',
            'Quero abrir um polo',
            'Saiba mais',
            'Notícias',
            'Eventos',
            'Blog',
            'Contato',
            'Portal do Aluno',
            'Biblioteca',
            'Webmail'
        ]
        
        texto_limpo = texto.strip()
        
        # Verificar se é exatamente um dos textos de navegação
        if texto_limpo in textos_navegacao_uvv:
            return True
        
        # Verificar se contém apenas textos de navegação
        texto_lower = texto_limpo.lower()
        for nav_text in textos_navegacao_uvv:
            if nav_text.lower() == texto_lower:
                return True
        
        # Verificar se é uma combinação de textos de menu (muito comum no site da UVV)
        if len(texto_limpo.split('\n')) > 5:
            linhas = texto_limpo.split('\n')
            linhas_menu = sum(1 for linha in linhas if linha.strip() in textos_navegacao_uvv)
            if linhas_menu / len(linhas) > 0.7:  # 70% das linhas são de menu
                return True
        
        return False
    
    def debug_html_estrutura(self, html_content):
        """Faz debug da estrutura HTML para entender o layout."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        print(f"\n🔍 === DEBUG DA ESTRUTURA HTML ===")
        
        # Procurar por textos que contenham "inova"
        elementos_inova = soup.find_all(string=re.compile(r'inova', re.IGNORECASE))
        print(f"📝 Textos contendo 'inova': {len(elementos_inova)}")
        
        for i, texto in enumerate(elementos_inova[:5]):  # Primeiros 5
            elemento_pai = texto.parent if hasattr(texto, 'parent') else None
            if elemento_pai:
                print(f"   {i+1}. '{texto.strip()[:50]}...' em <{elemento_pai.name}>")
        
        # Procurar imagens (notícias geralmente têm imagens)
        imagens = soup.find_all('img')
        print(f"�️ Imagens encontradas: {len(imagens)}")
        
        # Procurar links
        links = soup.find_all('a', href=True)
        links_internos = [l for l in links if 'uvv.br' in l.get('href', '') or l.get('href', '').startswith('/')]
        print(f"🔗 Links internos: {len(links_internos)}")
        
        # Mostrar alguns links que podem ser notícias
        print(f"\n📋 Primeiros links que podem ser notícias:")
        for i, link in enumerate(links_internos[:10]):
            texto_link = link.get_text().strip()[:60]
            href = link.get('href')
            if len(texto_link) > 15:  # Links com texto substancial
                print(f"   {i+1}. {texto_link}... → {href}")
    
    def coletar_noticias_uvv(self):
        """
        Método principal para coletar notícias da UVV.
        
        Returns:
            list: Lista de notícias coletadas
        """
        print(f"\n🚀 === INICIANDO COLETA DE NOTÍCIAS UVV ===")
        print(f"🎯 Objetivo: Notícias de setembro/{self.ano_alvo}")
        print(f"📍 URL base: {self.noticias_url}")
        
        # Lista de URLs para verificar
        urls_para_verificar = [
            self.noticias_url,
        ]
        
        total_noticias = 0
        
        for i, url in enumerate(urls_para_verificar, 1):
            print(f"\n--- Verificando URL {i}/{len(urls_para_verificar)} ---")
            
            # Fazer requisição
            response = self.fazer_requisicao(url)
            if not response:
                print(f"⚠️ Pulando URL devido a erro: {url}")
                continue
            
            # Debug da estrutura HTML na primeira URL
            if i == 1:
                self.debug_html_estrutura(response.text)
            
            # Extrair notícias da página
            noticias_pagina = self.extrair_noticias_pagina(response.text, url)
            
            # Não filtrar por data inicialmente, vamos ver tudo que foi capturado
            print(f"📰 Encontradas {len(noticias_pagina)} notícias total")
            
            # Adicionar à coleção principal
            self.noticias.extend(noticias_pagina)
            total_noticias += len(noticias_pagina)
            
            # Rate limiting apenas se tivermos mais URLs
            if i < len(urls_para_verificar):
                print(f"⏳ Aguardando 2s antes da próxima requisição...")
                time.sleep(2)
        
        # Remover duplicatas baseado no título
        self.remover_duplicatas()
        
        print(f"\n🎉 === COLETA FINALIZADA ===")
        print(f"📊 Total coletado: {len(self.noticias)} notícias únicas")
        print(f"� Notícias do Inova: {sum(1 for n in self.noticias if n.get('eh_inova'))}")
        print(f"� Notícias com data: {sum(1 for n in self.noticias if n.get('data_publicacao'))}")
        
        return self.noticias
    
    def remover_duplicatas(self):
        """Remove notícias duplicadas baseado no título."""
        print(f"🔄 Removendo duplicatas...")
        
        titulos_vistos = set()
        noticias_unicas = []
        duplicatas = 0
        
        for noticia in self.noticias:
            titulo_normalizado = noticia['titulo'].lower().strip()
            if titulo_normalizado not in titulos_vistos:
                titulos_vistos.add(titulo_normalizado)
                noticias_unicas.append(noticia)
            else:
                duplicatas += 1
        
        self.noticias = noticias_unicas
        print(f"🗑️ Removidas {duplicatas} duplicatas")
    
    def salvar_resultados(self):
        """Salva os resultados em múltiplos formatos."""
        if not self.noticias:
            print("⚠️ Nenhuma notícia para salvar")
            return
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Salvar CSV
        filename_csv = f"uvv_noticias_setembro_{timestamp}.csv"
        self.salvar_csv(filename_csv)
        
        # Salvar JSON
        filename_json = f"uvv_noticias_setembro_{timestamp}.json"
        self.salvar_json(filename_json)
        
        # Criar relatório
        self.gerar_relatorio()
    
    def salvar_csv(self, filename):
        """Salva notícias em formato CSV com estrutura otimizada."""
        try:
            fieldnames = [
                'titulo', 'resumo', 'data_publicacao', 'data_publicacao_texto',
                'link', 'categoria', 'autor', 'tags', 'eh_inova', 
                'conteudo_completo', 'tamanho_conteudo', 'qualidade_extracao',
                'num_imagens', 'num_videos', 'num_links_relacionados',
                'url_fonte', 'timestamp_coleta'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                
                for noticia in self.noticias:
                    conteudo = noticia.get('conteudo_completo', '')
                    
                    # Calcular qualidade da extração
                    qualidade = 'Baixa'
                    if len(conteudo) > 500:
                        qualidade = 'Alta'
                    elif len(conteudo) > 200:
                        qualidade = 'Média'
                    
                    # Verificar se parece ser navegação (baixa qualidade)
                    if conteudo and self._eh_texto_navegacao_uvv(conteudo[:200]):
                        qualidade = 'Menu/Navegação'
                    
                    # Preparar dados para CSV
                    row = {
                        'titulo': noticia.get('titulo', ''),
                        'resumo': noticia.get('resumo', ''),
                        'data_publicacao': noticia.get('data_publicacao').strftime('%Y-%m-%d') if noticia.get('data_publicacao') else '',
                        'data_publicacao_texto': noticia.get('data_publicacao_texto', ''),
                        'link': noticia.get('link', ''),
                        'categoria': noticia.get('categoria', ''),
                        'autor': noticia.get('autor', ''),
                        'tags': ', '.join(noticia.get('tags', [])),
                        'eh_inova': noticia.get('eh_inova', False),
                        'conteudo_completo': conteudo,
                        'tamanho_conteudo': len(conteudo),
                        'qualidade_extracao': qualidade,
                        'num_imagens': len(noticia.get('imagens', [])),
                        'num_videos': len(noticia.get('videos', [])),
                        'num_links_relacionados': len(noticia.get('links_relacionados', [])),
                        'url_fonte': noticia.get('url_fonte', ''),
                        'timestamp_coleta': noticia.get('timestamp_coleta', '')
                    }
                    writer.writerow(row)
            
            print(f"💾 CSV salvo: {filename}")
            
            # Estatísticas de qualidade
            noticias_com_conteudo = [n for n in self.noticias if n.get('conteudo_completo')]
            conteudo_alto = sum(1 for n in noticias_com_conteudo if len(n.get('conteudo_completo', '')) > 500)
            conteudo_medio = sum(1 for n in noticias_com_conteudo if 200 <= len(n.get('conteudo_completo', '')) <= 500)
            conteudo_baixo = sum(1 for n in noticias_com_conteudo if len(n.get('conteudo_completo', '')) < 200)
            
            print(f"   📊 Qualidade do conteúdo extraído:")
            print(f"   🟢 Alta qualidade (>500 chars): {conteudo_alto}")
            print(f"   🟡 Média qualidade (200-500 chars): {conteudo_medio}")
            print(f"   � Baixa qualidade (<200 chars): {conteudo_baixo}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar CSV: {e}")
    
    def salvar_json(self, filename):
        """Salva notícias em formato JSON."""
        try:
            # Preparar dados para JSON
            dados_json = {
                'metadata': {
                    'total_noticias': len(self.noticias),
                    'mes_alvo': self.mes_alvo,
                    'ano_alvo': self.ano_alvo,
                    'timestamp_scraping': self.timestamp_scraping.isoformat(),
                    'url_base': self.base_url,
                    'noticias_inova': sum(1 for n in self.noticias if n.get('eh_inova')),
                    'noticias_com_conteudo_completo': sum(1 for n in self.noticias if n.get('conteudo_completo')),
                    'total_imagens': sum(len(n.get('imagens', [])) for n in self.noticias),
                    'total_videos': sum(len(n.get('videos', [])) for n in self.noticias)
                },
                'noticias': []
            }
            
            for noticia in self.noticias:
                dados_noticia = noticia.copy()
                if dados_noticia.get('data_publicacao'):
                    dados_noticia['data_publicacao'] = dados_noticia['data_publicacao'].isoformat()
                dados_json['noticias'].append(dados_noticia)
            
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(dados_json, file, ensure_ascii=False, indent=2)
            
            print(f"💾 JSON salvo: {filename}")
            
        except Exception as e:
            print(f"❌ Erro ao salvar JSON: {e}")
    
    def gerar_relatorio(self):
        """Gera relatório detalhado das notícias coletadas."""
        print(f"\n📊 === RELATÓRIO DETALHADO ===")
        
        if not self.noticias:
            print("❌ Nenhuma notícia coletada")
            return
        
        # Estatísticas gerais
        print(f"📰 Total de notícias: {len(self.noticias)}")
        print(f"📅 Período alvo: setembro/{self.ano_alvo}")
        print(f"🔬 Notícias do Inova UVV: {sum(1 for n in self.noticias if n.get('eh_inova'))}")
        
        # Notícias com data
        com_data = [n for n in self.noticias if n.get('data_publicacao')]
        print(f"📅 Notícias com data identificada: {len(com_data)}")
        
        # Notícias com resumo
        com_resumo = [n for n in self.noticias if n.get('resumo')]
        print(f"📝 Notícias com resumo: {len(com_resumo)}")
        
        # Notícias com link
        com_link = [n for n in self.noticias if n.get('link')]
        print(f"🔗 Notícias com link: {len(com_link)}")
        
        # Notícias com conteúdo completo
        com_conteudo = [n for n in self.noticias if n.get('conteudo_completo')]
        print(f"📖 Notícias com conteúdo completo: {len(com_conteudo)}")
        
        # Estatísticas de mídia
        total_imagens = sum(len(n.get('imagens', [])) for n in self.noticias)
        total_videos = sum(len(n.get('videos', [])) for n in self.noticias)
        print(f"🖼️ Total de imagens coletadas: {total_imagens}")
        print(f"🎥 Total de vídeos encontrados: {total_videos}")
        
        # Categorias mais comuns
        categorias = defaultdict(int)
        for noticia in self.noticias:
            if noticia.get('categoria'):
                categorias[noticia['categoria']] += 1
        
        if categorias:
            print(f"\n🏷️ Categorias encontradas:")
            for categoria, count in sorted(categorias.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   • {categoria}: {count} notícias")
        
        # Autores mais ativos
        autores = defaultdict(int)
        for noticia in self.noticias:
            if noticia.get('autor'):
                autores[noticia['autor']] += 1
        
        if autores:
            print(f"\n✍️ Autores mais ativos:")
            for autor, count in sorted(autores.items(), key=lambda x: x[1], reverse=True)[:3]:
                print(f"   • {autor}: {count} notícias")
        
        # Amostra de títulos
        print(f"\n📋 Amostra de títulos coletados:")
        for i, noticia in enumerate(self.noticias[:5], 1):
            status = "🔬 INOVA" if noticia.get('eh_inova') else "📰 GERAL"
            conteudo_status = " ✅" if noticia.get('conteudo_completo') else " ❌"
            data_str = ""
            if noticia.get('data_publicacao'):
                data_str = f" | {noticia['data_publicacao'].strftime('%d/%m/%Y')}"
            print(f"   {i}. {status}{conteudo_status} | {noticia['titulo'][:80]}...{data_str}")
        
        # Notícias Inova com conteúdo completo
        noticias_inova = [n for n in self.noticias if n.get('eh_inova')]
        if noticias_inova:
            print(f"\n🔬 Detalhes das notícias do InovaWeek:")
            for i, noticia in enumerate(noticias_inova[:3], 1):
                conteudo_size = len(noticia.get('conteudo_completo', ''))
                num_imagens = len(noticia.get('imagens', []))
                print(f"   {i}. {noticia['titulo'][:60]}...")
                print(f"      📄 Conteúdo: {conteudo_size} caracteres")
                print(f"      🖼️ Imagens: {num_imagens}")
                if noticia.get('link'):
                    print(f"      🔗 Link: {noticia['link']}")
        
        print(f"\n🕐 Scraping finalizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

def executar_scraping_uvv():
    """Função principal para executar o scraping da UVV."""
    print("🎓 === SCRAPER UVV - NOTÍCIAS SETEMBRO 2025 ===")
    print("=" * 55)
    
    # Criar instância do scraper
    scraper = UVVNoticiasScraper()
    
    try:
        # Coletar notícias
        noticias = scraper.coletar_noticias_uvv()
        
        # Salvar resultados
        scraper.salvar_resultados()
        
        print(f"\n✅ Scraping concluído com sucesso!")
        print(f"📊 Total coletado: {len(noticias)} notícias")
        
        return noticias
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Scraping interrompido pelo usuário")
        if scraper.noticias:
            print(f"💾 Salvando {len(scraper.noticias)} notícias coletadas até agora...")
            scraper.salvar_resultados()
        
    except Exception as e:
        print(f"\n❌ Erro durante o scraping: {e}")
        if scraper.noticias:
            print(f"💾 Salvando {len(scraper.noticias)} notícias coletadas até o erro...")
            scraper.salvar_resultados()

if __name__ == "__main__":
    # Executar scraping da UVV
    executar_scraping_uvv()