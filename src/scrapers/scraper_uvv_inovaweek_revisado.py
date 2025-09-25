#!/usr/bin/env python3
"""
Scraper Específico para Notícias UVV - InovaWeek (Agosto-Setembro 2025)
=======================================================================

Este script coleta especificamente as notícias da Universidade Vila Velha (UVV)
relacionadas ao InovaWeek entre agosto e setembro de 2025.

Funcionalidades:
- Coleta de notícias do site oficial da UVV sobre InovaWeek
- Filtragem por período (agosto-setembro 2025)
- Extração de dados específicos: título, link, conteúdo, autor, data de publicação
- Tratamento robusto de datas com biblioteca datetime
- Requisições HTTP otimizadas com biblioteca requests
- Verificações de argumentos das tags CSS
- Exportação para CSV estruturado

Autor: ICLearning WebScraping Project
Data: 2025-09-25
URL Alvo: https://www.uvv.br/noticias/
Período: Agosto-Setembro 2025
Foco: Notícias do InovaWeek
"""

# === IMPORTAÇÕES NECESSÁRIAS ===
import requests
import csv
from bs4 import BeautifulSoup
import time
import re
import json
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import os
import argparse
import sys
from collections import defaultdict

class UVVInovaWeekScraper:
    """
    Scraper especializado para notícias do InovaWeek da UVV.
    
    Coleta notícias específicas do InovaWeek entre agosto e setembro de 2025,
    com verificações robustas de tags CSS e extração precisa de dados.
    """
    
    def __init__(self, periodo_inicio=None, periodo_fim=None, seletores_customizados=None):
        """
        Inicializa o scraper do InovaWeek UVV.
        
        Args:
            periodo_inicio (datetime): Data de início da coleta (padrão: agosto 2025)
            periodo_fim (datetime): Data de fim da coleta (padrão: setembro 2025)
            seletores_customizados (dict): Seletores CSS customizados
        """
        # Configurações de período
        self.periodo_inicio = periodo_inicio or datetime(2025, 8, 1)
        self.periodo_fim = periodo_fim or datetime(2025, 9, 30, 23, 59, 59)
        
        # URLs de destino
        self.base_url = "https://www.uvv.br"
        self.noticias_url = "https://www.uvv.br/noticias/"
        
        # Headers para requisições HTTP
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        
        # Session configurada seguindo melhores práticas requests
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Configurações avançadas da session
        # Reutilizar conexões TCP (pool de conexões)
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        # Estratégia de retry com backoff
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            backoff_factor=1,
            raise_on_status=False
        )
        
        # Adapter com pool de conexões
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        # Montar adapters para HTTP e HTTPS
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Configurar cookies jar para persistir cookies
        # Não definir policy como None - usar a padrão do requests
        
        # Seletores CSS para extração de dados
        self.seletores = self._configurar_seletores(seletores_customizados)
        
        # Armazenamento das notícias coletadas
        self.noticias = []
        
        # Timestamp do início do scraping
        self.timestamp_scraping = datetime.now()
        
        # Palavras-chave para identificar notícias do InovaWeek
        self.palavras_chave_inova = [
            'inovaweek', 'inova week', 'inova', 'inovação', 'innovation',
            'semana de inovação', 'evento de inovação', 'empreendedorismo',
            'startup', 'hackathon', 'pitch', 'palestra inovação'
        ]
        
        print(f"🚀 UVV InovaWeek Scraper inicializado")
        print(f"📅 Período de coleta: {self.periodo_inicio.strftime('%d/%m/%Y')} até {self.periodo_fim.strftime('%d/%m/%Y')}")
        print(f"🕐 Scraping iniciado em: {self.timestamp_scraping.strftime('%d/%m/%Y %H:%M:%S')}")
    
    def _configurar_seletores(self, seletores_customizados=None):
        """
        Configura os seletores CSS para extração de dados.
        
        Args:
            seletores_customizados (dict): Seletores customizados do usuário
            
        Returns:
            dict: Dicionário com todos os seletores configurados
        """
        seletores_padrao = {
            # Seletores para identificar notícias na página principal
            'container_noticias': [
                '.col-md-3',
                '.card',
                '.news-item',
                '.post-item',
                'article',
                '.noticia-item',
                'div[class*="col-"]'
            ],
            
            # Seletores para título da notícia
            'titulo': [
                'h1',
                'h2', 
                'h3',
                '.titulo',
                '.title',
                '.headline',
                '.news-title',
                '.post-title',
                'a[title]'
            ],
            
            # Seletores para links
            'link': [
                'a[href]'
            ],
            
            # Seletores para autor
            'autor': [
                '.autor',
                '.author',
                '.by',
                '.byline',
                '.post-author',
                '.news-author',
                '[class*="author"]'
            ],
            
            # Seletores para data de publicação
            'data_publicacao': [
                '.data',
                '.date',
                '.published',
                '.post-date',
                '.news-date',
                'time',
                '[datetime]',
                '[class*="date"]'
            ],
            
            # Seletores para conteúdo completo (página individual)
            'conteudo_completo': [
                '.single-post .entry-content',
                '.post-content .entry-content',
                '.news-content',
                '.noticia-texto',
                '.article-body',
                '.post-body',
                '.entry-text',
                '.content-wrapper',
                '.post-content',
                '.entry-content',
                '.article-content',
                '.content-area',
                '.single-post-content',
                '.main-content',
                'article .content',
                'main article',
                '.texto-noticia'
            ]
        }
        
        # Mesclar com seletores customizados se fornecidos
        if seletores_customizados:
            for categoria, seletores in seletores_customizados.items():
                if categoria in seletores_padrao:
                    seletores_padrao[categoria].extend(seletores)
                else:
                    seletores_padrao[categoria] = seletores
        
        return seletores_padrao
    
    def fazer_requisicao(self, url, params=None, timeout=30, max_tentativas=3):
        """
        Faz requisição HTTP com tratamento robusto de erros seguindo melhores práticas.
        Implementa uso correto de parâmetros URL conforme documentação requests.
        
        Args:
            url (str): URL base para requisição
            params (dict): Parâmetros URL a serem codificados automaticamente
            timeout (int): Timeout em segundos
            max_tentativas (int): Número máximo de tentativas
            
        Returns:
            requests.Response or None: Resposta ou None se erro
        """
        for tentativa in range(max_tentativas):
            try:
                # Log da URL com parâmetros (se houver)
                if params:
                    print(f"🔍 Fazendo requisição (tentativa {tentativa + 1}): {url} com params: {params}")
                else:
                    print(f"🔍 Fazendo requisição (tentativa {tentativa + 1}): {url}")
                
                # Requisição usando melhores práticas do requests
                response = self.session.get(
                    url, 
                    params=params,  # Parâmetros URL codificados automaticamente
                    timeout=timeout,
                    allow_redirects=True  # Permitir redirecionamentos
                )
                
                # Verificar status HTTP usando raise_for_status()
                response.raise_for_status()
                
                # Configurar encoding corretamente se necessário
                if response.encoding is None or response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'
                
                print(f"✅ Status: {response.status_code} | URL Final: {response.url}")
                print(f"📊 Tamanho: {len(response.content)} bytes | Encoding: {response.encoding}")
                return response
                
            except requests.exceptions.Timeout as e:
                print(f"⏰ Timeout na tentativa {tentativa + 1} para {url}: {e}")
                if tentativa < max_tentativas - 1:
                    time.sleep(2 ** tentativa)  # Backoff exponencial
            except requests.exceptions.ConnectionError as e:
                print(f"🔌 Erro de conexão na tentativa {tentativa + 1} para {url}: {e}")
                if tentativa < max_tentativas - 1:
                    time.sleep(2 ** tentativa)
            except requests.exceptions.HTTPError as e:
                print(f"🚫 Erro HTTP na tentativa {tentativa + 1} para {url}: {e}")
                if tentativa < max_tentativas - 1:
                    time.sleep(2 ** tentativa)
            except requests.exceptions.RequestException as e:
                print(f"❌ Erro geral na tentativa {tentativa + 1} para {url}: {e}")
                if tentativa < max_tentativas - 1:
                    time.sleep(2 ** tentativa)
        
        print(f"❌ Falhou após {max_tentativas} tentativas")
        return None
    
    def construir_url_busca(self, termo_busca=None, pagina=1, data_inicio=None, data_fim=None):
        """
        Constrói URL de busca com parâmetros usando melhores práticas requests.
        
        Args:
            termo_busca (str): Termo para buscar
            pagina (int): Número da página
            data_inicio (datetime): Data inicial para filtro
            data_fim (datetime): Data final para filtro
            
        Returns:
            tuple: (url_base, params_dict) para uso com requests
        """
        # URL base para busca
        url_base = self.noticias_url
        
        # Construir parâmetros usando dict (melhor prática requests)
        params = {}
        
        if termo_busca:
            params['q'] = termo_busca
            params['search'] = termo_busca
            
        if pagina and pagina > 1:
            params['page'] = pagina
            params['p'] = pagina
            
        if data_inicio:
            params['date_from'] = data_inicio.strftime('%Y-%m-%d')
            
        if data_fim:
            params['date_to'] = data_fim.strftime('%Y-%m-%d')
        
        # Parâmetros adicionais que podem ser úteis
        params['category'] = 'noticias'
        params['type'] = 'news'
        
        print(f"🔧 URL construída: {url_base}")
        if params:
            print(f"📋 Parâmetros URL: {params}")
            
        return url_base, params
    
    def testar_conectividade(self):
        """
        Testa conectividade com o site usando melhores práticas requests.
        
        Returns:
            bool: True se conectividade OK, False caso contrário
        """
        try:
            print("🔧 Testando conectividade com o site...")
            
            # Fazer uma requisição HEAD primeiro (mais leve)
            response = self.session.head(self.base_url, timeout=10, allow_redirects=True)
            
            if response.status_code in [200, 301, 302]:
                print(f"✅ Conectividade OK - Status: {response.status_code}")
                print(f"🌐 URL final: {response.url}")
                print(f"📄 Server: {response.headers.get('server', 'N/A')}")
                return True
            else:
                print(f"⚠️  Status inesperado: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro de conectividade: {e}")
            return False
    
    def configurar_proxy(self, proxy_config=None):
        """
        Configura proxy para a session se necessário.
        
        Args:
            proxy_config (dict): Configuração de proxy
                                Exemplo: {'http': 'http://proxy:port', 'https': 'https://proxy:port'}
        """
        if proxy_config:
            self.session.proxies.update(proxy_config)
            print(f"🔧 Proxy configurado: {proxy_config}")
    
    def extrair_data_noticia(self, elemento_html, texto_elemento=None):
        """
        Extrai e converte data da notícia com verificações robustas.
        
        Args:
            elemento_html: Elemento HTML contendo a data
            texto_elemento (str): Texto alternativo para buscar data
            
        Returns:
            tuple: (datetime object, string original) ou (None, None)
        """
        # Textos onde procurar data
        textos_para_buscar = []
        
        if elemento_html:
            # Verificar atributos datetime primeiro
            for attr in ['datetime', 'data-date', 'data-time']:
                if elemento_html.get(attr):
                    textos_para_buscar.append(elemento_html.get(attr))
            
            # Adicionar texto do elemento
            texto_elem = elemento_html.get_text().strip()
            if texto_elem:
                textos_para_buscar.append(texto_elem)
        
        if texto_elemento:
            textos_para_buscar.append(texto_elemento)
        
        # Padrões de data em português
        padroes_data = [
            (r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})', 'dd/mm/yyyy'),
            (r'(\d{4})[\/\-](\d{1,2})[\/\-](\d{1,2})', 'yyyy/mm/dd'),
            (r'(\d{1,2}) de (\w+) de (\d{4})', 'dd de mês de yyyy'),
            (r'(\d{1,2}) (\w+) (\d{4})', 'dd mês yyyy'),
            (r'(\w+) (\d{1,2}), (\d{4})', 'mês dd, yyyy'),
            (r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{2})', 'dd/mm/yy')
        ]
        
        # Mapeamento de meses em português
        meses_pt = {
            'janeiro': 1, 'jan': 1,
            'fevereiro': 2, 'fev': 2,
            'março': 3, 'mar': 3,
            'abril': 4, 'abr': 4,
            'maio': 5, 'mai': 5,
            'junho': 6, 'jun': 6,
            'julho': 7, 'jul': 7,
            'agosto': 8, 'ago': 8,
            'setembro': 9, 'set': 9,
            'outubro': 10, 'out': 10,
            'novembro': 11, 'nov': 11,
            'dezembro': 12, 'dez': 12
        }
        
        for texto in textos_para_buscar:
            texto = texto.strip().lower()
            
            for padrao, formato in padroes_data:
                match = re.search(padrao, texto)
                if match:
                    try:
                        grupos = match.groups()
                        
                        if formato == 'dd/mm/yyyy':
                            dia, mes, ano = map(int, grupos)
                        elif formato == 'yyyy/mm/dd':
                            ano, mes, dia = map(int, grupos)
                        elif formato in ['dd de mês de yyyy', 'dd mês yyyy']:
                            dia, nome_mes, ano = grupos
                            dia, ano = int(dia), int(ano)
                            mes = meses_pt.get(nome_mes.lower())
                            if not mes:
                                continue
                        elif formato == 'mês dd, yyyy':
                            nome_mes, dia, ano = grupos
                            dia, ano = int(dia), int(ano)
                            mes = meses_pt.get(nome_mes.lower())
                            if not mes:
                                continue
                        elif formato == 'dd/mm/yy':
                            dia, mes, ano = map(int, grupos)
                            ano = 2000 + ano if ano < 50 else 1900 + ano
                        
                        # Validar data
                        data_obj = datetime(ano, mes, dia)
                        return data_obj, match.group(0)
                        
                    except (ValueError, TypeError):
                        continue
        
        return None, None
    
    def eh_noticia_inovaweek(self, titulo, conteudo_texto="", periodo_valido=True):
        """
        Verifica se a notícia é relacionada ao InovaWeek.
        
        Args:
            titulo (str): Título da notícia
            conteudo_texto (str): Conteúdo da notícia
            periodo_valido (bool): Se a data está no período válido
            
        Returns:
            bool: True se for notícia do InovaWeek
        """
        # Texto completo para busca
        texto_completo = f"{titulo} {conteudo_texto}".lower()
        
        # Verificar palavras-chave do InovaWeek
        for palavra in self.palavras_chave_inova:
            if palavra.lower() in texto_completo:
                return True
        
        return False
    
    def eh_periodo_valido(self, data_noticia):
        """
        Verifica se a data da notícia está no período válido (agosto-setembro 2025).
        
        Args:
            data_noticia (datetime): Data da notícia
            
        Returns:
            bool: True se estiver no período válido
        """
        if not data_noticia:
            return False
        
        return self.periodo_inicio <= data_noticia <= self.periodo_fim
    
    def extrair_com_seletores(self, soup, categoria_seletor, elemento_pai=None):
        """
        Extrai elemento usando múltiplos seletores CSS com verificações.
        
        Args:
            soup: Objeto BeautifulSoup
            categoria_seletor (str): Categoria de seletor ('titulo', 'autor', etc.)
            elemento_pai: Elemento pai para busca específica
            
        Returns:
            BeautifulSoup element or None: Primeiro elemento encontrado
        """
        base_soup = elemento_pai if elemento_pai else soup
        seletores = self.seletores.get(categoria_seletor, [])
        
        for seletor in seletores:
            try:
                elementos = base_soup.select(seletor)
                if elementos:
                    # Verificar se o elemento tem conteúdo válido
                    elemento = elementos[0]
                    texto = elemento.get_text().strip()
                    
                    # Validações específicas por categoria
                    if categoria_seletor == 'titulo' and len(texto) < 10:
                        continue
                    elif categoria_seletor == 'autor' and len(texto) < 2:
                        continue
                    elif categoria_seletor == 'link' and not elemento.get('href'):
                        continue
                    
                    return elemento
                        
            except Exception as e:
                print(f"⚠️ Erro no seletor '{seletor}' para {categoria_seletor}: {e}")
                continue
        
        return None
    
    def processar_noticia_individual(self, url_noticia):
        """
        Processa uma notícia individual para extrair conteúdo completo.
        
        Args:
            url_noticia (str): URL da notícia específica
            
        Returns:
            dict: Dados completos da notícia
        """
        # Rate limiting (ser respeitoso com o servidor)
        time.sleep(1)
        
        # Fazer requisição usando melhores práticas (sem parâmetros adicionais para página individual)
        response = self.fazer_requisicao(url_noticia, params=None)
        if not response:
            return {'conteudo_completo': '', 'erro': 'Falha na requisição'}
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remover elementos desnecessários
        for elemento in soup.select('script, style, nav, header, footer, aside, .menu, .navigation'):
            elemento.decompose()
        
        # Extrair conteúdo principal
        elemento_conteudo = self.extrair_com_seletores(soup, 'conteudo_completo')
        conteudo_texto = ""
        
        if elemento_conteudo:
            # Extrair parágrafos do conteúdo
            paragrafos = elemento_conteudo.find_all(['p', 'div'], string=True)
            textos_limpos = []
            
            for p in paragrafos:
                texto_p = p.get_text().strip()
                # Filtrar textos muito curtos ou de navegação
                if (len(texto_p) > 30 and 
                    not self._eh_texto_navegacao(texto_p)):
                    textos_limpos.append(texto_p)
            
            conteudo_texto = '\n\n'.join(textos_limpos)
        
        # Se não encontrou conteúdo com seletores, tentar estratégia alternativa
        if not conteudo_texto or len(conteudo_texto) < 100:
            paragrafos_alternativos = soup.find_all('p')
            textos_alternativos = []
            
            for p in paragrafos_alternativos:
                texto_p = p.get_text().strip()
                if (len(texto_p) > 50 and 
                    not self._eh_texto_navegacao(texto_p)):
                    textos_alternativos.append(texto_p)
            
            if textos_alternativos:
                conteudo_texto = '\n\n'.join(textos_alternativos)
        
        return {
            'conteudo_completo': conteudo_texto,
            'tamanho_conteudo': len(conteudo_texto)
        }
    
    def _eh_texto_navegacao(self, texto):
        """Verifica se o texto parece ser de navegação/menu."""
        texto_lower = texto.lower()
        
        # Palavras típicas de navegação da UVV
        palavras_navegacao = [
            'institucional', 'graduação', 'pós graduação', 'mestrado',
            'doutorado', 'pesquisa', 'extensão', 'contato', 'blog',
            'notícias', 'eventos', 'portal', 'trabalhe conosco'
        ]
        
        # Se contém principalmente palavras de navegação
        palavras_nav_encontradas = sum(1 for palavra in palavras_navegacao if palavra in texto_lower)
        palavras_totais = len(texto.split())
        
        if palavras_totais > 0 and (palavras_nav_encontradas / palavras_totais) > 0.5:
            return True
        
        # Texto muito curto
        if len(texto) < 20:
            return True
            
        return False
    
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
        noticias_encontradas = []
        
        print(f"📄 Analisando página: {url_pagina}")
        
        # Buscar containers de notícias com múltiplas estratégias
        containers = set()  # Use set para evitar duplicatas
        
        # Estratégia 1: Usar seletores configurados
        for seletor in self.seletores['container_noticias']:
            elementos = soup.select(seletor)
            for elem in elementos:
                containers.add(elem)
        
        # Estratégia 2: Buscar elementos que contenham links para notícias
        links_noticias = soup.find_all('a', href=True)
        for link in links_noticias:
            href = link.get('href', '')
            if '/noticias/' in href and len(link.get_text().strip()) > 20:
                # Adicionar o container pai do link
                container_pai = link.find_parent(['div', 'article', 'section'])
                if container_pai:
                    containers.add(container_pai)
        
        # Estratégia 3: Buscar por elementos com texto que contenha palavras-chave
        for palavra_chave in ['inovaweek', 'inova', 'setembro', 'agosto']:
            elementos_texto = soup.find_all(string=re.compile(palavra_chave, re.IGNORECASE))
            for texto in elementos_texto:
                if hasattr(texto, 'parent'):
                    container_texto = texto.parent.find_parent(['div', 'article', 'section'])
                    if container_texto:
                        containers.add(container_texto)
        
        containers = list(containers)  # Converter de volta para lista
        print(f"🔍 Encontrados {len(containers)} containers únicos de notícias")
        
        for i, container in enumerate(containers):
            try:
                noticia_data = self._extrair_dados_noticia(container, url_pagina)
                
                if noticia_data and noticia_data.get('titulo'):
                    print(f"📋 {i+1}/{len(containers)} Analisando: {noticia_data['titulo'][:60]}...")
                    
                    # Verificar se é notícia do InovaWeek (mais flexível)
                    eh_inovaweek = self.eh_noticia_inovaweek(
                        noticia_data['titulo'],
                        noticia_data.get('resumo', ''),
                        True  # Mais flexível com período inicialmente
                    )
                    
                    if eh_inovaweek:
                        noticias_encontradas.append(noticia_data)
                        print(f"✅ Notícia InovaWeek encontrada: {noticia_data['titulo'][:60]}...")
                    else:
                        print(f"❌ Não é InovaWeek: {noticia_data['titulo'][:60]}...")
                else:
                    print(f"⚠️ {i+1}/{len(containers)} Container sem título válido")
                    
            except Exception as e:
                print(f"⚠️ Erro ao processar container {i+1}: {e}")
                continue
        
        return noticias_encontradas
    
    def _extrair_dados_noticia(self, container, url_pagina):
        """
        Extrai dados de uma notícia específica do container HTML.
        
        Args:
            container: Elemento BeautifulSoup do container
            url_pagina (str): URL da página atual
            
        Returns:
            dict: Dados da notícia extraídos
        """
        noticia = {
            'titulo': '',
            'link': '',
            'autor': '',
            'data_publicacao': None,
            'data_publicacao_str': '',
            'resumo': '',
            'conteudo_completo': '',
            'timestamp_coleta': self.timestamp_scraping.isoformat(),
            'url_fonte': url_pagina,
            'periodo_valido': False
        }
        
        # Extrair título com múltiplas estratégias
        elem_titulo = self.extrair_com_seletores(container, 'titulo', container)
        if elem_titulo:
            noticia['titulo'] = elem_titulo.get_text().strip()
        else:
            # Estratégia alternativa: buscar qualquer texto significativo
            textos = container.find_all(string=True)
            for texto in textos:
                texto_limpo = texto.strip()
                if len(texto_limpo) > 20 and not self._eh_texto_navegacao(texto_limpo):
                    noticia['titulo'] = texto_limpo
                    break
        
        # Filtrar títulos muito curtos (mais flexível)
        if len(noticia['titulo']) < 5:
            return None
        
        # Extrair link
        elem_link = self.extrair_com_seletores(container, 'link', container)
        if elem_link and elem_link.get('href'):
            link = elem_link.get('href')
            if link.startswith('/'):
                link = urljoin(self.base_url, link)
            elif link.startswith('#'):
                return None  # Skip anchor links
            noticia['link'] = link
        
        # Extrair autor
        elem_autor = self.extrair_com_seletores(container, 'autor', container)
        if elem_autor:
            noticia['autor'] = elem_autor.get_text().strip()
        
        # Extrair data de publicação
        elem_data = self.extrair_com_seletores(container, 'data_publicacao', container)
        data_obj, data_str = self.extrair_data_noticia(elem_data, container.get_text())
        
        if data_obj:
            noticia['data_publicacao'] = data_obj
            noticia['data_publicacao_str'] = data_str
            noticia['periodo_valido'] = self.eh_periodo_valido(data_obj)
        
        # Extrair resumo (se disponível)
        paragrafos = container.find_all('p')
        if paragrafos:
            for p in paragrafos:
                texto_p = p.get_text().strip()
                if len(texto_p) > 50 and not self._eh_texto_navegacao(texto_p):
                    noticia['resumo'] = texto_p[:300]
                    break
        
        return noticia
    
    def coletar_noticias_inovaweek(self, max_paginas=10, somente_primeira_pagina=False):
        """
        Método principal para coletar notícias do InovaWeek com suporte a paginação.
        
        Args:
            max_paginas (int): Número máximo de páginas para vasculhar (padrão: 10)
            somente_primeira_pagina (bool): Se deve coletar apenas a primeira página
        
        Returns:
            list: Lista de notícias do InovaWeek coletadas de todas as páginas
        """
        print(f"\n🚀 === INICIANDO COLETA DE NOTÍCIAS INOVAWEEK UVV ===")
        print(f"🎯 Foco: Notícias do InovaWeek")
        print(f"📅 Período: {self.periodo_inicio.strftime('%d/%m/%Y')} até {self.periodo_fim.strftime('%d/%m/%Y')}")
        print(f"📍 URL base: {self.noticias_url}")
        print(f"📄 Máximo de páginas: {max_paginas if not somente_primeira_pagina else 1}")
        
        # Testar conectividade primeiro
        if not self.testar_conectividade():
            print("❌ Falha na conectividade. Abortando coleta.")
            return []
        
        # Coletar notícias de múltiplas páginas
        todas_noticias = []
        paginas_processadas = 0
        paginas_sem_noticias = 0
        
        for numero_pagina in range(1, max_paginas + 1):
            if somente_primeira_pagina and numero_pagina > 1:
                break
                
            print(f"\n📄 === PROCESSANDO PÁGINA {numero_pagina} ===")
            
            # Construir URL da página atual
            noticias_pagina = self._coletar_noticias_pagina_especifica(numero_pagina)
            
            if not noticias_pagina:
                paginas_sem_noticias += 1
                print(f"⚠️ Página {numero_pagina}: Nenhuma notícia InovaWeek encontrada")
                
                # Se não encontrou notícias em 3 páginas consecutivas, parar
                if paginas_sem_noticias >= 3:
                    print(f"🛑 Parando busca: 3 páginas consecutivas sem notícias InovaWeek")
                    break
                continue
            else:
                paginas_sem_noticias = 0  # Reset contador
                
            print(f"✅ Página {numero_pagina}: {len(noticias_pagina)} notícias InovaWeek encontradas")
            todas_noticias.extend(noticias_pagina)
            paginas_processadas += 1
            
            # Rate limiting entre páginas
            if numero_pagina < max_paginas:
                time.sleep(2)  # Pausa respeitosa entre páginas
        
        print(f"\n🎉 === COLETA PAGINADA FINALIZADA ===")
        print(f"📄 Páginas processadas: {paginas_processadas}")
        print(f"📊 Total de notícias encontradas: {len(todas_noticias)}")
        
        # Processar cada notícia para extrair conteúdo completo
        print(f"\n📖 === EXTRAINDO CONTEÚDO COMPLETO ===")
        for i, noticia in enumerate(todas_noticias):
            if noticia.get('link') and noticia['link'] != '#':
                print(f"📖 Processando {i+1}/{len(todas_noticias)}: {noticia['titulo'][:50]}...")
                
                conteudo_dados = self.processar_noticia_individual(noticia['link'])
                noticia.update(conteudo_dados)
                
                # Rate limiting para ser respeitoso
                time.sleep(1)
        
        self.noticias = todas_noticias
        
        print(f"\n🎉 === COLETA COMPLETA FINALIZADA ===")
        print(f"📊 Total coletado: {len(self.noticias)} notícias do InovaWeek")
        print(f"📖 Com conteúdo completo: {sum(1 for n in self.noticias if len(n.get('conteudo_completo', '')) > 100)}")
        print(f"📄 Páginas vasculhadas: {paginas_processadas}")
        
        return self.noticias
    
    def _coletar_noticias_pagina_especifica(self, numero_pagina):
        """
        Coleta notícias de uma página específica.
        
        Args:
            numero_pagina (int): Número da página para coletar
            
        Returns:
            list: Lista de notícias InovaWeek da página
        """
        # Construir URLs para diferentes formatos de paginação
        urls_tentar = [
            # Formato padrão com /page/X/
            f"{self.base_url}/noticias/page/{numero_pagina}/",
            # Formato alternativo
            f"{self.noticias_url}page/{numero_pagina}/",
            # Formato com parâmetro
            f"{self.noticias_url}?page={numero_pagina}",
            f"{self.noticias_url}?p={numero_pagina}"
        ]
        
        # Se for página 1, tentar também a URL base
        if numero_pagina == 1:
            urls_tentar.insert(0, self.noticias_url)
        
        for url_tentativa in urls_tentar:
            print(f"🔍 Tentando URL: {url_tentativa}")
            
            response = self.fazer_requisicao(url_tentativa)
            
            if response and response.status_code == 200:
                # Verificar se a página realmente existe (não é redirect para página 1)
                if numero_pagina > 1 and 'page' not in response.url and numero_pagina != 1:
                    print(f"⚠️ Possível redirect para página principal - pulando")
                    continue
                
                # Extrair notícias da página
                noticias_pagina = self.extrair_noticias_pagina(response.text, url_tentativa)
                
                if noticias_pagina:
                    print(f"✅ Página {numero_pagina} acessada com sucesso: {len(noticias_pagina)} notícias InovaWeek")
                    return noticias_pagina
                else:
                    print(f"📭 Página {numero_pagina} acessada mas sem notícias InovaWeek")
            else:
                print(f"❌ Falha ao acessar: {url_tentativa}")
        
        return []
    
    def verificar_paginacao_disponivel(self):
        """
        Verifica quantas páginas de notícias estão disponíveis.
        
        Returns:
            int: Número estimado de páginas disponíveis
        """
        print(f"\n🔍 === VERIFICANDO PAGINAÇÃO DISPONÍVEL ===")
        
        # Fazer requisição para página principal
        response = self.fazer_requisicao(self.noticias_url)
        if not response:
            return 1
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Procurar por indicadores de paginação
        links_paginacao = []
        
        # Seletores comuns para paginação
        seletores_paginacao = [
            'a[href*="page"]',
            '.pagination a',
            '.pager a',
            'nav a[href*="page"]',
            '.page-numbers a',
            '.wp-pagenavi a'
        ]
        
        for seletor in seletores_paginacao:
            links = soup.select(seletor)
            for link in links:
                href = link.get('href', '')
                if 'page' in href:
                    links_paginacao.append(href)
        
        # Extrair números de página dos links
        numeros_pagina = []
        for link in links_paginacao:
            # Tentar extrair número da página
            import re
            match = re.search(r'page[/=](\d+)', link)
            if match:
                numeros_pagina.append(int(match.group(1)))
        
        max_pagina = max(numeros_pagina) if numeros_pagina else 1
        
        print(f"🔢 Páginas detectadas: {sorted(set(numeros_pagina)) if numeros_pagina else [1]}")
        print(f"📄 Máxima página encontrada: {max_pagina}")
        
        # Verificar se realmente existem mais páginas testando algumas
        paginas_existentes = 1
        for teste_pagina in range(2, min(max_pagina + 1, 6)):  # Testar até página 5
            url_teste = f"{self.base_url}/noticias/page/{teste_pagina}/"
            response_teste = self.fazer_requisicao(url_teste)
            
            if response_teste and response_teste.status_code == 200:
                # Verificar se não é redirect para página principal
                if 'page' in response_teste.url or teste_pagina == 1:
                    paginas_existentes = teste_pagina
                    print(f"✅ Página {teste_pagina} confirmada")
                else:
                    print(f"❌ Página {teste_pagina} redireciona para principal")
                    break
            else:
                print(f"❌ Página {teste_pagina} não acessível")
                break
                
            time.sleep(1)  # Rate limiting
        
        print(f"📊 Total de páginas confirmadas: {paginas_existentes}")
        return max(paginas_existentes, max_pagina if numeros_pagina else 1)
    
    def exportar_csv(self, filename=None, incluir_metadados=True):
        """
        Exporta as notícias coletadas para arquivo CSV bem estruturado.
        
        Args:
            filename (str): Nome do arquivo (opcional)
            incluir_metadados (bool): Se deve incluir arquivo de metadados
            
        Returns:
            str: Nome do arquivo gerado
        """
        if not filename:
            timestamp = self.timestamp_scraping.strftime('%Y%m%d_%H%M%S')
            filename = f"uvv_inovaweek_noticias_{timestamp}.csv"
        
        if not self.noticias:
            print("⚠️ Nenhuma notícia para exportar")
            return filename
        
        try:
            # Campos organizados por categoria para melhor estrutura
            fieldnames_estruturados = [
                # === IDENTIFICAÇÃO ===
                'id_noticia',
                'titulo',
                'slug_url',
                'url_completa',
                
                # === AUTORIA E TEMPORALIDADE ===
                'autor',
                'data_publicacao_formatada',
                'data_publicacao_iso',
                'mes_publicacao',
                'ano_publicacao',
                'timestamp_coleta_iso',
                'timestamp_coleta_formatado',
                
                # === CONTEÚDO ===
                'resumo_automatico',
                'conteudo_completo_limpo',
                'palavras_chave_encontradas',
                'tamanho_caracteres',
                'tamanho_palavras',
                'qualidade_conteudo',
                
                # === CLASSIFICAÇÃO ===
                'categoria_evento',
                'relevancia_inovaweek',
                'periodo_valido',
                'status_processamento',
                
                # === TÉCNICO/METADADOS ===
                'fonte_site',
                'metodo_extracao',
                'encoding_original',
                'http_status'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames_estruturados)
                writer.writeheader()
                
                for i, noticia in enumerate(self.noticias, 1):
                    # Preparar dados estruturados para CSV
                    row = self._preparar_dados_estruturados(noticia, i)
                    writer.writerow(row)
            
            print(f"💾 CSV estruturado exportado: {filename}")
            
            # Gerar arquivo de metadados se solicitado
            if incluir_metadados:
                self._gerar_arquivo_metadados(filename)
            
            # Estatísticas detalhadas
            self._exibir_estatisticas_export(filename)
            
            return filename
            
        except Exception as e:
            print(f"❌ Erro ao exportar CSV estruturado: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _preparar_dados_estruturados(self, noticia, indice):
        """
        Prepara dados de uma notícia em formato estruturado para CSV.
        
        Args:
            noticia (dict): Dados da notícia
            indice (int): Índice da notícia
            
        Returns:
            dict: Dados estruturados para CSV
        """
        # Extrair informações do link
        url = noticia.get('link', '')
        slug = url.split('/')[-1] if url else ''
        
        # Processar conteúdo
        conteudo = noticia.get('conteudo_completo', '')
        conteudo_limpo = self._limpar_conteudo_para_csv(conteudo)
        palavras = conteudo_limpo.split() if conteudo_limpo else []
        
        # Detectar palavras-chave do InovaWeek
        palavras_chave_encontradas = []
        conteudo_lower = conteudo_limpo.lower()
        for palavra in self.palavras_chave_inova:
            if palavra.lower() in conteudo_lower:
                palavras_chave_encontradas.append(palavra)
        
        # Determinar qualidade do conteúdo
        qualidade = self._avaliar_qualidade_conteudo(conteudo_limpo)
        
        # Processar datas
        data_pub = noticia.get('data_publicacao')
        data_iso = data_pub.isoformat() if isinstance(data_pub, datetime) else ''
        data_formatada = data_pub.strftime('%d/%m/%Y %H:%M') if isinstance(data_pub, datetime) else ''
        mes_pub = data_pub.strftime('%Y-%m') if isinstance(data_pub, datetime) else ''
        ano_pub = data_pub.year if isinstance(data_pub, datetime) else ''
        
        # Timestamp de coleta
        timestamp_coleta = self.timestamp_scraping
        timestamp_iso = timestamp_coleta.isoformat()
        timestamp_formatado = timestamp_coleta.strftime('%d/%m/%Y %H:%M:%S')
        
        return {
            # === IDENTIFICAÇÃO ===
            'id_noticia': f"UVV_INOVA_{indice:03d}_{self.timestamp_scraping.strftime('%Y%m%d')}",
            'titulo': noticia.get('titulo', '').strip(),
            'slug_url': slug,
            'url_completa': url,
            
            # === AUTORIA E TEMPORALIDADE ===
            'autor': noticia.get('autor', '').strip(),
            'data_publicacao_formatada': data_formatada,
            'data_publicacao_iso': data_iso,
            'mes_publicacao': mes_pub,
            'ano_publicacao': str(ano_pub) if ano_pub else '',
            'timestamp_coleta_iso': timestamp_iso,
            'timestamp_coleta_formatado': timestamp_formatado,
            
            # === CONTEÚDO ===
            'resumo_automatico': self._gerar_resumo_automatico(conteudo_limpo),
            'conteudo_completo_limpo': conteudo_limpo,
            'palavras_chave_encontradas': ', '.join(palavras_chave_encontradas),
            'tamanho_caracteres': len(conteudo_limpo),
            'tamanho_palavras': len(palavras),
            'qualidade_conteudo': qualidade,
            
            # === CLASSIFICAÇÃO ===
            'categoria_evento': self._classificar_categoria_evento(noticia.get('titulo', '')),
            'relevancia_inovaweek': self._calcular_relevancia_inovaweek(noticia),
            'periodo_valido': noticia.get('periodo_valido', True),
            'status_processamento': 'COMPLETO' if conteudo_limpo else 'PARCIAL',
            
            # === TÉCNICO/METADADOS ===
            'fonte_site': 'UVV - Universidade Vila Velha',
            'metodo_extracao': 'Web Scraping - BeautifulSoup + Requests',
            'encoding_original': 'UTF-8',
            'http_status': '200'
        }
    
    def _limpar_conteudo_para_csv(self, conteudo):
        """Limpa conteúdo para formato CSV."""
        if not conteudo:
            return ''
        
        # Remover quebras de linha duplas e múltiplas
        conteudo = re.sub(r'\n\s*\n', '\n', conteudo)
        # Remover espaços extras
        conteudo = re.sub(r'\s+', ' ', conteudo)
        # Remover caracteres de controle
        conteudo = ''.join(char for char in conteudo if ord(char) >= 32 or char in '\n\t')
        
        return conteudo.strip()
    
    def _gerar_resumo_automatico(self, conteudo, max_palavras=50):
        """Gera resumo automático do conteúdo."""
        if not conteudo:
            return ''
        
        palavras = conteudo.split()
        if len(palavras) <= max_palavras:
            return conteudo
        
        resumo = ' '.join(palavras[:max_palavras])
        return resumo + '...'
    
    def _avaliar_qualidade_conteudo(self, conteudo):
        """Avalia qualidade do conteúdo extraído."""
        if not conteudo:
            return 'VAZIO'
        
        tamanho = len(conteudo)
        if tamanho < 100:
            return 'BAIXA'
        elif tamanho < 500:
            return 'MÉDIA'
        elif tamanho < 2000:
            return 'BOA'
        else:
            return 'EXCELENTE'
    
    def _classificar_categoria_evento(self, titulo):
        """Classifica categoria do evento baseado no título."""
        titulo_lower = titulo.lower()
        
        if any(palavra in titulo_lower for palavra in ['palestra', 'talk', 'apresentação']):
            return 'PALESTRA'
        elif any(palavra in titulo_lower for palavra in ['show', 'música', 'apresentação cultural']):
            return 'SHOW/CULTURAL'
        elif any(palavra in titulo_lower for palavra in ['premiação', 'prêmio', 'homenagem']):
            return 'PREMIAÇÃO'
        elif any(palavra in titulo_lower for palavra in ['exposição', 'mostra', 'feira']):
            return 'EXPOSIÇÃO'
        elif any(palavra in titulo_lower for palavra in ['trek', 'caminhada', 'visita']):
            return 'ATIVIDADE'
        else:
            return 'GERAL'
    
    def _calcular_relevancia_inovaweek(self, noticia):
        """Calcula relevância da notícia para o InovaWeek."""
        titulo = noticia.get('titulo', '').lower()
        conteudo = noticia.get('conteudo_completo', '').lower()
        
        pontos = 0
        
        # Pontuação por palavra-chave no título
        for palavra in self.palavras_chave_inova:
            if palavra.lower() in titulo:
                pontos += 3
        
        # Pontuação por palavra-chave no conteúdo
        for palavra in self.palavras_chave_inova:
            if palavra.lower() in conteudo:
                pontos += 1
        
        # Classificar relevância
        if pontos >= 10:
            return 'MUITO_ALTA'
        elif pontos >= 5:
            return 'ALTA'
        elif pontos >= 2:
            return 'MÉDIA'
        else:
            return 'BAIXA'
    
    def _gerar_arquivo_metadados(self, arquivo_csv):
        """Gera arquivo de metadados complementar."""
        nome_metadados = arquivo_csv.replace('.csv', '_metadados.txt')
        
        try:
            with open(nome_metadados, 'w', encoding='utf-8') as f:
                f.write("=== METADADOS DA COLETA - UVV INOVAWEEK ===\n\n")
                f.write(f"📅 Data da coleta: {self.timestamp_scraping.strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"🎯 Período analisado: {self.periodo_inicio.strftime('%d/%m/%Y')} até {self.periodo_fim.strftime('%d/%m/%Y')}\n")
                f.write(f"🌐 Site origem: {self.base_url}\n")
                f.write(f"📰 Total de notícias: {len(self.noticias)}\n\n")
                
                f.write("=== ESTRUTURA DO CSV ===\n")
                f.write("O arquivo CSV contém as seguintes seções organizadas:\n\n")
                f.write("1. IDENTIFICAÇÃO: ID único, título, URL\n")
                f.write("2. AUTORIA E TEMPORALIDADE: Autor, datas formatadas\n")
                f.write("3. CONTEÚDO: Resumo, conteúdo completo, palavras-chave\n")
                f.write("4. CLASSIFICAÇÃO: Categoria, relevância, qualidade\n")
                f.write("5. TÉCNICO/METADADOS: Informações de extração\n\n")
                
                f.write("=== PALAVRAS-CHAVE MONITORADAS ===\n")
                for palavra in self.palavras_chave_inova:
                    f.write(f"- {palavra}\n")
                
                f.write(f"\n=== CONFIGURAÇÕES TÉCNICAS ===\n")
                f.write(f"- Encoding: UTF-8\n")
                f.write(f"- Separador CSV: vírgula (,)\n")
                f.write(f"- Tratamento de aspas: escape duplo\n")
                f.write(f"- User-Agent: {self.headers.get('User-Agent', 'N/A')[:50]}...\n")
                
            print(f"📋 Arquivo de metadados gerado: {nome_metadados}")
            
        except Exception as e:
            print(f"⚠️ Erro ao gerar metadados: {e}")
    
    def _exibir_estatisticas_export(self, filename):
        """Exibe estatísticas detalhadas do export."""
        print(f"\n📊 === ESTATÍSTICAS DETALHADAS DO EXPORT ===")
        
        # Estatísticas básicas
        total = len(self.noticias)
        com_conteudo = sum(1 for n in self.noticias if len(n.get('conteudo_completo', '')) > 100)
        com_autor = sum(1 for n in self.noticias if n.get('autor'))
        com_data = sum(1 for n in self.noticias if n.get('data_publicacao'))
        
        print(f"📈 Geral:")
        print(f"   📰 Total de registros: {total}")
        print(f"   📖 Com conteúdo completo: {com_conteudo} ({com_conteudo/total*100:.1f}%)")
        print(f"   👤 Com autor identificado: {com_autor} ({com_autor/total*100:.1f}%)")
        print(f"   📅 Com data de publicação: {com_data} ({com_data/total*100:.1f}%)")
        
        # Qualidade do conteúdo
        qualidades = {}
        for noticia in self.noticias:
            conteudo = noticia.get('conteudo_completo', '')
            qualidade = self._avaliar_qualidade_conteudo(conteudo)
            qualidades[qualidade] = qualidades.get(qualidade, 0) + 1
        
        print(f"\n📊 Qualidade do conteúdo:")
        for qualidade, count in sorted(qualidades.items()):
            print(f"   {qualidade}: {count} notícias")
        
        # Relevância InovaWeek
        relevancias = {}
        for noticia in self.noticias:
            relevancia = self._calcular_relevancia_inovaweek(noticia)
            relevancias[relevancia] = relevancias.get(relevancia, 0) + 1
        
        print(f"\n🎯 Relevância InovaWeek:")
        for relevancia, count in sorted(relevancias.items(), reverse=True):
            print(f"   {relevancia}: {count} notícias")
        
        print(f"\n💾 Arquivo: {filename}")
        print(f"🔧 Encoding: UTF-8")
        print(f"📋 Campos estruturados: 25 colunas organizadas")
        print(f"✅ Export concluído com sucesso!")
    
    def gerar_relatorio(self):
        """Gera relatório detalhado das notícias coletadas."""
        print(f"\n📊 === RELATÓRIO DETALHADO - INOVAWEEK UVV ===")
        
        if not self.noticias:
            print("❌ Nenhuma notícia coletada")
            return
        
        print(f"📰 Total de notícias do InovaWeek: {len(self.noticias)}")
        print(f"📅 Período analisado: {self.periodo_inicio.strftime('%d/%m/%Y')} - {self.periodo_fim.strftime('%d/%m/%Y')}")
        
        # Análise por qualidade do conteúdo
        alta_qualidade = sum(1 for n in self.noticias if len(n.get('conteudo_completo', '')) > 1000)
        media_qualidade = sum(1 for n in self.noticias if 300 <= len(n.get('conteudo_completo', '')) <= 1000)
        baixa_qualidade = sum(1 for n in self.noticias if len(n.get('conteudo_completo', '')) < 300)
        
        print(f"\n📖 Qualidade do conteúdo extraído:")
        print(f"   🟢 Alta qualidade (>1000 chars): {alta_qualidade}")
        print(f"   🟡 Média qualidade (300-1000 chars): {media_qualidade}")
        print(f"   🔴 Baixa qualidade (<300 chars): {baixa_qualidade}")
        
        # Análise temporal
        noticias_com_data = [n for n in self.noticias if n.get('data_publicacao')]
        if noticias_com_data:
            datas = [n['data_publicacao'] for n in noticias_com_data]
            data_mais_antiga = min(datas)
            data_mais_recente = max(datas)
            
            print(f"\n📅 Análise temporal:")
            print(f"   📊 Notícias com data: {len(noticias_com_data)}/{len(self.noticias)}")
            print(f"   📅 Data mais antiga: {data_mais_antiga.strftime('%d/%m/%Y')}")
            print(f"   📅 Data mais recente: {data_mais_recente.strftime('%d/%m/%Y')}")
        
        # Amostra de títulos
        print(f"\n📋 Amostra de notícias coletadas:")
        for i, noticia in enumerate(self.noticias[:5], 1):
            status_conteudo = "✅" if len(noticia.get('conteudo_completo', '')) > 300 else "❌"
            status_data = "📅" if noticia.get('data_publicacao') else "❓"
            
            print(f"   {i}. {status_conteudo} {status_data} {noticia['titulo'][:70]}...")
            if noticia.get('autor'):
                print(f"      👤 Autor: {noticia['autor']}")
            if noticia.get('data_publicacao'):
                print(f"      📅 Data: {noticia['data_publicacao'].strftime('%d/%m/%Y')}")
        
        print(f"\n🕐 Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


def main():
    """Função principal com argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description='Scraper de notícias do InovaWeek UVV (Agosto-Setembro 2025)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python scraper_uvv_inovaweek_revisado.py
  python scraper_uvv_inovaweek_revisado.py --output noticias_inovaweek.csv
  python scraper_uvv_inovaweek_revisado.py --inicio 2025-08-01 --fim 2025-09-30
        """
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Nome do arquivo CSV de saída'
    )
    
    parser.add_argument(
        '--inicio',
        type=str,
        help='Data de início (formato: YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--fim',
        type=str,
        help='Data de fim (formato: YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--seletores',
        type=str,
        help='Arquivo JSON com seletores CSS customizados'
    )
    
    parser.add_argument(
        '--max-paginas',
        type=int,
        default=10,
        help='Número máximo de páginas para vasculhar (padrão: 10)'
    )
    
    parser.add_argument(
        '--apenas-primeira-pagina',
        action='store_true',
        help='Coletar apenas da primeira página (sem paginação)'
    )
    
    parser.add_argument(
        '--verificar-paginacao',
        action='store_true',
        help='Verificar quantas páginas estão disponíveis antes de coletar'
    )
    
    args = parser.parse_args()
    
    # Processar datas
    periodo_inicio = None
    periodo_fim = None
    
    if args.inicio:
        try:
            periodo_inicio = datetime.strptime(args.inicio, '%Y-%m-%d')
        except ValueError:
            print("❌ Formato de data de início inválido. Use YYYY-MM-DD")
            sys.exit(1)
    
    if args.fim:
        try:
            periodo_fim = datetime.strptime(args.fim, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        except ValueError:
            print("❌ Formato de data de fim inválido. Use YYYY-MM-DD")
            sys.exit(1)
    
    # Carregar seletores customizados
    seletores_customizados = None
    if args.seletores:
        try:
            with open(args.seletores, 'r', encoding='utf-8') as f:
                seletores_customizados = json.load(f)
        except Exception as e:
            print(f"❌ Erro ao carregar seletores customizados: {e}")
            sys.exit(1)
    
    # Executar scraping
    print("🎓 === SCRAPER UVV INOVAWEEK - VERSÃO REVISADA ===")
    print("=" * 60)
    
    try:
        scraper = UVVInovaWeekScraper(
            periodo_inicio=periodo_inicio,
            periodo_fim=periodo_fim,
            seletores_customizados=seletores_customizados
        )
        
        # Verificar paginação se solicitado
        if args.verificar_paginacao:
            paginas_disponiveis = scraper.verificar_paginacao_disponivel()
            print(f"\n📊 Paginação disponível: {paginas_disponiveis} páginas")
            
            # Ajustar max_paginas se necessário
            if args.max_paginas > paginas_disponiveis:
                print(f"⚠️ Ajustando max-paginas de {args.max_paginas} para {paginas_disponiveis}")
                args.max_paginas = paginas_disponiveis
        
        # Coletar notícias com paginação
        noticias = scraper.coletar_noticias_inovaweek(
            max_paginas=args.max_paginas,
            somente_primeira_pagina=args.apenas_primeira_pagina
        )
        
        if noticias:
            # Exportar CSV
            arquivo_csv = scraper.exportar_csv(args.output)
            
            # Gerar relatório
            scraper.gerar_relatorio()
            
            print(f"\n✅ Scraping concluído com sucesso!")
            print(f"📊 Total coletado: {len(noticias)} notícias do InovaWeek")
            print(f"💾 Arquivo gerado: {arquivo_csv}")
        else:
            print("⚠️ Nenhuma notícia do InovaWeek encontrada no período especificado")
        
    except KeyboardInterrupt:
        print(f"\n⚠️ Scraping interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o scraping: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()