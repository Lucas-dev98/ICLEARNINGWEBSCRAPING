#!/usr/bin/env python3
"""
Exemplo 07 - Scraping de Redes Sociais e APIs Públicas
=======================================================

Este exemplo demonstra como fazer scraping em redes sociais e APIs públicas com:
- Rate limiting e controle de requisições
- Análise de engagement e métricas sociais
- Processamento de dados em tempo real
- Monitoramento de tendências

IMPORTANTE: Sempre respeite os termos de uso e políticas de API das plataformas!

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
from urllib.parse import urljoin, urlparse, parse_qs
from collections import Counter, defaultdict
import time
import hashlib
from dataclasses import dataclass
from typing import List, Dict, Optional
import threading
import queue

def simular_rede_social():
    """Simula uma rede social pública para demonstração."""
    html_exemplo = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SocialHub - Rede Social de Desenvolvedores</title>
        <meta name="description" content="Comunidade de desenvolvedores">
    </head>
    <body>
        <div class="container">
            <!-- Post 1 -->
            <article class="post" data-post-id="post001" data-timestamp="2025-09-24T10:30:00Z">
                <header class="post-header">
                    <div class="user-info">
                        <img src="/avatars/maria_dev.jpg" alt="Maria Dev" class="avatar">
                        <div class="user-details">
                            <h3 class="username">@maria_dev</h3>
                            <span class="user-title">Full Stack Developer</span>
                            <span class="followers" data-count="15420">15.4K seguidores</span>
                        </div>
                    </div>
                    <time class="post-time" datetime="2025-09-24T10:30:00Z">há 2 horas</time>
                </header>
                
                <div class="post-content">
                    <p class="post-text">
                        🚀 Acabei de lançar uma nova biblioteca Python para web scraping! 
                        Ela inclui rate limiting automático, cache inteligente e suporte a JavaScript. 
                        
                        O que acham? Feedback é sempre bem-vindo! 
                        
                        #Python #WebScraping #OpenSource #Development
                    </p>
                    
                    <div class="post-media">
                        <img src="/posts/webscraper_lib.png" alt="Screenshot da biblioteca" class="post-image">
                    </div>
                    
                    <div class="post-links">
                        <a href="https://github.com/maria_dev/awesome-scraper" class="external-link">
                            🔗 github.com/maria_dev/awesome-scraper
                        </a>
                    </div>
                </div>
                
                <footer class="post-interactions">
                    <div class="engagement-stats">
                        <button class="like-btn" data-count="234">
                            ❤️ 234 curtidas
                        </button>
                        <button class="comment-btn" data-count="45">
                            💬 45 comentários
                        </button>
                        <button class="share-btn" data-count="67">
                            🔄 67 compartilhamentos
                        </button>
                        <button class="save-btn" data-count="89">
                            🔖 89 salvamentos
                        </button>
                    </div>
                    
                    <div class="hashtags">
                        <span class="hashtag">#Python</span>
                        <span class="hashtag">#WebScraping</span>
                        <span class="hashtag">#OpenSource</span>
                        <span class="hashtag">#Development</span>
                    </div>
                </footer>
            </article>

            <!-- Post 2 -->
            <article class="post" data-post-id="post002" data-timestamp="2025-09-24T09:15:00Z">
                <header class="post-header">
                    <div class="user-info">
                        <img src="/avatars/carlos_ai.jpg" alt="Carlos AI" class="avatar">
                        <div class="user-details">
                            <h3 class="username">@carlos_ai</h3>
                            <span class="user-title">AI/ML Engineer</span>
                            <span class="followers" data-count="28750">28.7K seguidores</span>
                        </div>
                    </div>
                    <time class="post-time" datetime="2025-09-24T09:15:00Z">há 3 horas</time>
                </header>
                
                <div class="post-content">
                    <p class="post-text">
                        🤖 Thread sobre as tendências de IA em 2025:
                        
                        1/5 - LLMs estão se tornando mais eficientes
                        2/5 - Edge AI está crescendo exponencialmente 
                        3/5 - Computer Vision atinge novos patamares
                        4/5 - NLP conversacional evolui rapidamente
                        5/5 - Ética em IA ganha mais importância
                        
                        Qual tendência vocês acham mais promissora? 
                        
                        #AI #MachineLearning #Tech2025 #Innovation
                    </p>
                </div>
                
                <footer class="post-interactions">
                    <div class="engagement-stats">
                        <button class="like-btn" data-count="892">
                            ❤️ 892 curtidas
                        </button>
                        <button class="comment-btn" data-count="156">
                            💬 156 comentários
                        </button>
                        <button class="share-btn" data-count="203">
                            🔄 203 compartilhamentos
                        </button>
                        <button class="save-btn" data-count="445">
                            🔖 445 salvamentos
                        </button>
                    </div>
                    
                    <div class="hashtags">
                        <span class="hashtag">#AI</span>
                        <span class="hashtag">#MachineLearning</span>
                        <span class="hashtag">#Tech2025</span>
                        <span class="hashtag">#Innovation</span>
                    </div>
                </footer>
            </article>

            <!-- Post 3 -->
            <article class="post viral" data-post-id="post003" data-timestamp="2025-09-23T16:45:00Z">
                <header class="post-header">
                    <div class="user-info">
                        <img src="/avatars/ana_data.jpg" alt="Ana Data" class="avatar">
                        <div class="user-details">
                            <h3 class="username">@ana_data</h3>
                            <span class="user-title">Data Scientist</span>
                            <span class="followers" data-count="42300">42.3K seguidores</span>
                        </div>
                    </div>
                    <time class="post-time" datetime="2025-09-23T16:45:00Z">ontem</time>
                    <span class="viral-badge">🔥 VIRAL</span>
                </header>
                
                <div class="post-content">
                    <p class="post-text">
                        📊 Análise: Salários em Tech 2025
                        
                        Baseado em 10K+ dados coletados:
                        
                        • Junior Dev: R$ 4.5K - R$ 8K
                        • Pleno Dev: R$ 8K - R$ 15K  
                        • Senior Dev: R$ 15K - R$ 25K
                        • Tech Lead: R$ 20K - R$ 35K
                        • Data Scientist: R$ 12K - R$ 30K
                        
                        Stack que mais paga: Python + Cloud + IA
                        
                        Thread completa com gráficos nos comentários ⬇️
                        
                        #Tech #Salarios #CarreiraeDev #DataScience
                    </p>
                    
                    <div class="post-media">
                        <img src="/posts/salary_chart.png" alt="Gráfico de salários" class="post-image">
                    </div>
                </div>
                
                <footer class="post-interactions">
                    <div class="engagement-stats">
                        <button class="like-btn" data-count="2847">
                            ❤️ 2.8K curtidas
                        </button>
                        <button class="comment-btn" data-count="456">
                            💬 456 comentários
                        </button>
                        <button class="share-btn" data-count="1203">
                            🔄 1.2K compartilhamentos
                        </button>
                        <button class="save-btn" data-count="1689">
                            🔖 1.7K salvamentos
                        </button>
                    </div>
                    
                    <div class="hashtags">
                        <span class="hashtag">#Tech</span>
                        <span class="hashtag">#Salarios</span>
                        <span class="hashtag">#CarreiraeDev</span>
                        <span class="hashtag">#DataScience</span>
                    </div>
                </footer>
            </article>

            <!-- Post 4 -->
            <article class="post" data-post-id="post004" data-timestamp="2025-09-23T14:20:00Z">
                <header class="post-header">
                    <div class="user-info">
                        <img src="/avatars/joao_mobile.jpg" alt="João Mobile" class="avatar">
                        <div class="user-details">
                            <h3 class="username">@joao_mobile</h3>
                            <span class="user-title">Mobile Developer</span>
                            <span class="followers" data-count="19800">19.8K seguidores</span>
                        </div>
                    </div>
                    <time class="post-time" datetime="2025-09-23T14:20:00Z">ontem</time>
                </header>
                
                <div class="post-content">
                    <p class="post-text">
                        📱 Dica rápida para devs React Native:
                        
                        Sempre testem a performance em dispositivos reais, não apenas no simulador!
                        
                        Descobri um vazamento de memória que só aparecia em Android real 😅
                        
                        Tools que salvam:
                        ✅ Flipper
                        ✅ Reactotron  
                        ✅ Android Studio Profiler
                        ✅ Xcode Instruments
                        
                        #ReactNative #Mobile #Performance #Development
                    </p>
                </div>
                
                <footer class="post-interactions">
                    <div class="engagement-stats">
                        <button class="like-btn" data-count="387">
                            ❤️ 387 curtidas
                        </button>
                        <button class="comment-btn" data-count="73">
                            💬 73 comentários
                        </button>
                        <button class="share-btn" data-count="95">
                            🔄 95 compartilhamentos
                        </button>
                        <button class="save-btn" data-count="234">
                            🔖 234 salvamentos
                        </button>
                    </div>
                    
                    <div class="hashtags">
                        <span class="hashtag">#ReactNative</span>
                        <span class="hashtag">#Mobile</span>
                        <span class="hashtag">#Performance</span>
                        <span class="hashtag">#Development</span>
                    </div>
                </footer>
            </article>

            <!-- Post 5 -->
            <article class="post promoted" data-post-id="post005" data-timestamp="2025-09-23T11:30:00Z">
                <header class="post-header">
                    <div class="user-info">
                        <img src="/avatars/techcorp.jpg" alt="TechCorp" class="avatar">
                        <div class="user-details">
                            <h3 class="username">@techcorp</h3>
                            <span class="user-title">Empresa • Tecnologia</span>
                            <span class="followers" data-count="156700">156.7K seguidores</span>
                        </div>
                    </div>
                    <time class="post-time" datetime="2025-09-23T11:30:00Z">ontem</time>
                    <span class="promoted-badge">📢 PROMOVIDO</span>
                </header>
                
                <div class="post-content">
                    <p class="post-text">
                        🚀 Estamos contratando Desenvolvedores Python!
                        
                        Posições disponíveis:
                        • Python Backend Developer (Pleno)
                        • Data Engineer (Senior)
                        • DevOps Engineer (Pleno/Senior)
                        
                        Benefícios:
                        ✅ Remoto 100%
                        ✅ Horário flexível
                        ✅ PLR + Stock Options
                        ✅ Budget para cursos
                        ✅ Setup home office
                        
                        Interessados? Link na bio ou DM! 
                        
                        #Jobs #Python #Remote #Hiring #TechJobs
                    </p>
                </div>
                
                <footer class="post-interactions">
                    <div class="engagement-stats">
                        <button class="like-btn" data-count="1245">
                            ❤️ 1.2K curtidas
                        </button>
                        <button class="comment-btn" data-count="289">
                            💬 289 comentários
                        </button>
                        <button class="share-btn" data-count="567">
                            🔄 567 compartilhamentos
                        </button>
                        <button class="save-btn" data-count="892">
                            🔖 892 salvamentos
                        </button>
                    </div>
                    
                    <div class="hashtags">
                        <span class="hashtag">#Jobs</span>
                        <span class="hashtag">#Python</span>
                        <span class="hashtag">#Remote</span>
                        <span class="hashtag">#Hiring</span>
                        <span class="hashtag">#TechJobs</span>
                    </div>
                </footer>
            </article>
        </div>

        <!-- API Endpoints simulados -->
        <script type="application/json" id="trending-topics">
        {
            "trending": [
                {"tag": "Python", "posts": 1247, "engagement": 45230, "growth": 12.5},
                {"tag": "AI", "posts": 892, "engagement": 67890, "growth": 23.8},
                {"tag": "WebScraping", "posts": 234, "engagement": 12340, "growth": 45.2},
                {"tag": "ReactNative", "posts": 567, "engagement": 23450, "growth": 8.7},
                {"tag": "DataScience", "posts": 445, "engagement": 34560, "growth": 15.3}
            ]
        }
        </script>

        <script type="application/json" id="user-analytics">
        {
            "analytics": {
                "total_users": 125000,
                "active_24h": 34500,
                "posts_24h": 2840,
                "engagement_rate": 7.8,
                "top_content_types": [
                    {"type": "tutorial", "percentage": 35},
                    {"type": "discussion", "percentage": 28},
                    {"type": "news", "percentage": 20},
                    {"type": "job_posting", "percentage": 12},
                    {"type": "meme", "percentage": 5}
                ]
            }
        }
        </script>
    </body>
    </html>
    """
    return html_exemplo

@dataclass
class RateLimiter:
    """Controlador de rate limiting para APIs."""
    requests_per_second: float
    requests_per_minute: int
    requests_per_hour: int
    
    def __post_init__(self):
        self.request_times = []
        self.lock = threading.Lock()
    
    def can_make_request(self) -> bool:
        """Verifica se pode fazer uma nova requisição."""
        now = time.time()
        
        with self.lock:
            # Remove requisições antigas (mais de 1 hora)
            self.request_times = [t for t in self.request_times if now - t < 3600]
            
            # Verifica limites
            recent_1s = len([t for t in self.request_times if now - t < 1])
            recent_1m = len([t for t in self.request_times if now - t < 60])
            recent_1h = len(self.request_times)
            
            return (recent_1s < self.requests_per_second and
                    recent_1m < self.requests_per_minute and
                    recent_1h < self.requests_per_hour)
    
    def record_request(self):
        """Registra uma nova requisição."""
        with self.lock:
            self.request_times.append(time.time())
    
    def wait_time(self) -> float:
        """Retorna tempo necessário para esperar antes da próxima requisição."""
        if self.can_make_request():
            return 0
        return 1 / self.requests_per_second

class SocialMediaScraper:
    """
    Scraper especializado em redes sociais com rate limiting e análise de engagement.
    
    Funcionalidades:
    - Rate limiting automático
    - Extração de posts e interações
    - Análise de engagement
    - Monitoramento de tendências
    - Processamento de hashtags
    """
    
    def __init__(self, requests_per_second=1, requests_per_minute=30, requests_per_hour=500):
        """
        Inicializa o scraper de redes sociais.
        
        Args:
            requests_per_second (float): Limite de requests por segundo
            requests_per_minute (int): Limite de requests por minuto  
            requests_per_hour (int): Limite de requests por hora
        """
        self.rate_limiter = RateLimiter(requests_per_second, requests_per_minute, requests_per_hour)
        self.session = requests.Session()
        
        # Headers apropriados para redes sociais
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; SocialBot/1.0; Research Purpose)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        }
        self.session.headers.update(self.headers)
        
        # Cache para evitar requests desnecessários
        self.cache = {}
        self.cache_duration = 300  # 5 minutos
    
    def make_request_with_limit(self, url: str, **kwargs) -> requests.Response:
        """
        Faz requisição respeitando rate limiting.
        
        Args:
            url (str): URL para requisição
            **kwargs: Argumentos adicionais para requests
            
        Returns:
            requests.Response: Resposta da requisição
        """
        # Verifica cache primeiro
        cache_key = hashlib.md5(f"{url}{str(kwargs)}".encode()).hexdigest()
        if cache_key in self.cache:
            cached_time, cached_response = self.cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                print(f"🗄️  Usando cache para: {url}")
                return cached_response
        
        # Rate limiting
        while not self.rate_limiter.can_make_request():
            wait_time = self.rate_limiter.wait_time()
            print(f"⏱️  Rate limit atingido. Aguardando {wait_time:.2f}s...")
            time.sleep(wait_time)
        
        # Fazer requisição
        self.rate_limiter.record_request()
        response = self.session.get(url, **kwargs)
        
        # Armazenar no cache
        self.cache[cache_key] = (time.time(), response)
        
        return response
    
    def extrair_engagement(self, interaction_elem):
        """
        Extrai métricas de engagement de um elemento.
        
        Args:
            interaction_elem: Elemento BeautifulSoup com interações
            
        Returns:
            dict: Métricas de engagement
        """
        engagement = {
            'likes': 0,
            'comments': 0,
            'shares': 0,
            'saves': 0,
            'total_engagement': 0,
            'engagement_rate': 0.0
        }
        
        if not interaction_elem:
            return engagement
        
        # Extrair likes
        like_btn = interaction_elem.find('button', class_='like-btn')
        if like_btn:
            count = like_btn.get('data-count', '0')
            engagement['likes'] = self.parse_count(count)
        
        # Extrair comentários
        comment_btn = interaction_elem.find('button', class_='comment-btn')
        if comment_btn:
            count = comment_btn.get('data-count', '0')
            engagement['comments'] = self.parse_count(count)
        
        # Extrair compartilhamentos
        share_btn = interaction_elem.find('button', class_='share-btn')
        if share_btn:
            count = share_btn.get('data-count', '0')
            engagement['shares'] = self.parse_count(count)
        
        # Extrair salvamentos
        save_btn = interaction_elem.find('button', class_='save-btn')
        if save_btn:
            count = save_btn.get('data-count', '0')
            engagement['saves'] = self.parse_count(count)
        
        # Calcular total
        engagement['total_engagement'] = (
            engagement['likes'] +
            engagement['comments'] +
            engagement['shares'] +
            engagement['saves']
        )
        
        return engagement
    
    def parse_count(self, count_str: str) -> int:
        """
        Converte string de contador (ex: "2.8K", "1.2M") para número.
        
        Args:
            count_str (str): String do contador
            
        Returns:
            int: Número convertido
        """
        if not count_str:
            return 0
        
        count_str = str(count_str).upper().replace(',', '.')
        
        if 'K' in count_str:
            number = float(count_str.replace('K', ''))
            return int(number * 1000)
        elif 'M' in count_str:
            number = float(count_str.replace('M', ''))
            return int(number * 1000000)
        elif 'B' in count_str:
            number = float(count_str.replace('B', ''))
            return int(number * 1000000000)
        else:
            try:
                return int(float(count_str))
            except ValueError:
                return 0
    
    def extrair_hashtags(self, texto: str, elementos_hashtag=None) -> List[str]:
        """
        Extrai hashtags do texto ou elementos específicos.
        
        Args:
            texto (str): Texto para extrair hashtags
            elementos_hashtag: Elementos HTML com hashtags
            
        Returns:
            list: Lista de hashtags
        """
        hashtags = []
        
        # Extrair de elementos específicos primeiro
        if elementos_hashtag:
            hashtag_spans = elementos_hashtag.find_all('span', class_='hashtag')
            for span in hashtag_spans:
                tag = span.get_text().strip()
                if tag.startswith('#'):
                    hashtags.append(tag)
        
        # Extrair do texto também
        if texto:
            hashtags_texto = re.findall(r'#\w+', texto)
            hashtags.extend(hashtags_texto)
        
        # Remover duplicatas e retornar
        return list(set(hashtags))
    
    def calcular_engagement_rate(self, engagement: dict, followers: int) -> float:
        """
        Calcula taxa de engagement baseada no número de seguidores.
        
        Args:
            engagement (dict): Métricas de engagement
            followers (int): Número de seguidores
            
        Returns:
            float: Taxa de engagement em percentual
        """
        if followers == 0:
            return 0.0
        
        total_engagement = engagement.get('total_engagement', 0)
        return (total_engagement / followers) * 100
    
    def scrape_posts(self, html_content: str) -> List[Dict]:
        """
        Extrai posts de uma rede social.
        
        Args:
            html_content (str): HTML da página
            
        Returns:
            list: Lista de posts com métricas completas
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        posts = []
        
        # Encontrar elementos de posts
        elementos_post = soup.find_all('article', class_='post')
        
        print(f"📱 Encontrados {len(elementos_post)} posts na rede social")
        
        for i, post in enumerate(elementos_post, 1):
            post_info = {}
            
            # ID e metadados básicos
            post_info['id'] = post.get('data-post-id', f'post_{i}')
            post_info['timestamp'] = post.get('data-timestamp', '')
            
            # Classificar tipo de post
            classes = post.get('class', [])
            post_info['viral'] = 'viral' in classes
            post_info['promoted'] = 'promoted' in classes
            
            # Informações do usuário
            user_info = post.find('div', class_='user-info')
            if user_info:
                username_elem = user_info.find('h3', class_='username')
                post_info['username'] = username_elem.get_text().strip() if username_elem else 'N/A'
                
                title_elem = user_info.find('span', class_='user-title')
                post_info['user_title'] = title_elem.get_text().strip() if title_elem else 'N/A'
                
                followers_elem = user_info.find('span', class_='followers')
                if followers_elem:
                    followers_count = followers_elem.get('data-count', '0')
                    post_info['followers'] = self.parse_count(followers_count)
                else:
                    post_info['followers'] = 0
            
            # Conteúdo do post
            content_div = post.find('div', class_='post-content')
            if content_div:
                text_elem = content_div.find('p', class_='post-text')
                post_info['content'] = text_elem.get_text().strip() if text_elem else ''
                
                # Verificar se tem mídia
                media_elem = content_div.find('div', class_='post-media')
                post_info['has_media'] = media_elem is not None
                
                if media_elem:
                    img = media_elem.find('img')
                    post_info['media_url'] = img.get('src') if img else None
                
                # Links externos
                links_elem = content_div.find('div', class_='post-links')
                if links_elem:
                    external_links = links_elem.find_all('a', class_='external-link')
                    post_info['external_links'] = [link.get('href') for link in external_links]
                else:
                    post_info['external_links'] = []
            
            # Métricas de engagement
            interactions = post.find('footer', class_='post-interactions')
            if interactions:
                engagement_stats = interactions.find('div', class_='engagement-stats')
                post_info['engagement'] = self.extrair_engagement(engagement_stats)
                
                # Calcular engagement rate
                post_info['engagement']['engagement_rate'] = self.calcular_engagement_rate(
                    post_info['engagement'], 
                    post_info['followers']
                )
                
                # Hashtags
                hashtags_div = interactions.find('div', class_='hashtags')
                post_info['hashtags'] = self.extrair_hashtags(
                    post_info.get('content', ''), 
                    hashtags_div
                )
                post_info['num_hashtags'] = len(post_info['hashtags'])
            
            # Análise do conteúdo
            content = post_info.get('content', '')
            post_info['content_length'] = len(content)
            post_info['word_count'] = len(content.split())
            post_info['has_emojis'] = bool(re.search(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', content))
            post_info['has_links'] = bool(re.search(r'http[s]?://|www\.', content))
            post_info['has_mentions'] = bool(re.search(r'@\w+', content))
            
            # Data de processamento
            post_info['processed_at'] = datetime.now().isoformat()
            
            posts.append(post_info)
        
        return posts
    
    def extrair_trending_topics(self, html_content: str) -> Dict:
        """
        Extrai tópicos em tendência de dados JSON embutidos.
        
        Args:
            html_content (str): HTML da página
            
        Returns:
            dict: Dados de trending topics
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Procurar script com dados de trending
        trending_script = soup.find('script', id='trending-topics')
        if trending_script:
            try:
                trending_data = json.loads(trending_script.get_text())
                return trending_data
            except json.JSONDecodeError:
                pass
        
        return {'trending': []}
    
    def extrair_analytics(self, html_content: str) -> Dict:
        """
        Extrai dados de analytics da plataforma.
        
        Args:
            html_content (str): HTML da página
            
        Returns:
            dict: Dados de analytics
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Procurar script com analytics
        analytics_script = soup.find('script', id='user-analytics')
        if analytics_script:
            try:
                analytics_data = json.loads(analytics_script.get_text())
                return analytics_data
            except json.JSONDecodeError:
                pass
        
        return {'analytics': {}}
    
    def analisar_engagement_patterns(self, posts: List[Dict]) -> Dict:
        """
        Analisa padrões de engagement nos posts.
        
        Args:
            posts (list): Lista de posts
            
        Returns:
            dict: Análise de padrões de engagement
        """
        if not posts:
            return {'erro': 'Nenhum post para analisar'}
        
        df = pd.DataFrame(posts)
        
        # Separar posts virais, promovidos e normais
        posts_virais = [p for p in posts if p.get('viral')]
        posts_promovidos = [p for p in posts if p.get('promoted')]
        posts_normais = [p for p in posts if not p.get('viral') and not p.get('promoted')]
        
        analise = {
            'total_posts': len(posts),
            'posts_virais': len(posts_virais),
            'posts_promovidos': len(posts_promovidos),
            'posts_normais': len(posts_normais),
        }
        
        # Análise de engagement
        engagements = [p['engagement']['total_engagement'] for p in posts if 'engagement' in p]
        if engagements:
            analise['engagement_stats'] = {
                'total': sum(engagements),
                'media': sum(engagements) / len(engagements),
                'maximo': max(engagements),
                'minimo': min(engagements)
            }
        
        # Análise de hashtags populares
        todas_hashtags = []
        for post in posts:
            todas_hashtags.extend(post.get('hashtags', []))
        
        analise['hashtags_populares'] = dict(Counter(todas_hashtags).most_common(10))
        
        # Análise por tipo de conteúdo
        posts_com_media = len([p for p in posts if p.get('has_media')])
        posts_com_links = len([p for p in posts if p.get('has_links')])
        posts_com_emojis = len([p for p in posts if p.get('has_emojis')])
        
        analise['tipos_conteudo'] = {
            'com_media': posts_com_media,
            'com_links': posts_com_links,
            'com_emojis': posts_com_emojis,
            'percentual_media': (posts_com_media / len(posts)) * 100,
            'percentual_links': (posts_com_links / len(posts)) * 100,
            'percentual_emojis': (posts_com_emojis / len(posts)) * 100
        }
        
        # Usuários mais engajados
        usuarios_engagement = defaultdict(int)
        for post in posts:
            username = post.get('username', 'unknown')
            engagement = post.get('engagement', {}).get('total_engagement', 0)
            usuarios_engagement[username] += engagement
        
        analise['usuarios_top_engagement'] = dict(
            Counter(usuarios_engagement).most_common(5)
        )
        
        # Análise temporal (se temos timestamps)
        posts_com_time = [p for p in posts if p.get('timestamp')]
        if posts_com_time:
            analise['posts_por_periodo'] = len(posts_com_time)
        
        # Performance por tipo de post
        if posts_virais:
            viral_eng = [p['engagement']['total_engagement'] for p in posts_virais if 'engagement' in p]
            if viral_eng:
                analise['performance_viral'] = {
                    'engagement_medio': sum(viral_eng) / len(viral_eng),
                    'total_engagement': sum(viral_eng)
                }
        
        if posts_promovidos:
            promo_eng = [p['engagement']['total_engagement'] for p in posts_promovidos if 'engagement' in p]
            if promo_eng:
                analise['performance_promovido'] = {
                    'engagement_medio': sum(promo_eng) / len(promo_eng),
                    'total_engagement': sum(promo_eng)
                }
        
        return analise

def exemplo_uso():
    """Demonstra o uso prático do SocialMediaScraper."""
    print("📱 === EXEMPLO DE SCRAPING DE REDES SOCIAIS ===")
    print("=" * 58)
    
    # Inicializar scraper com rate limiting
    scraper = SocialMediaScraper(
        requests_per_second=2,
        requests_per_minute=60,
        requests_per_hour=1000
    )
    
    # Simular rede social
    print("1️⃣ Obtendo dados da rede social...")
    html_content = simular_rede_social()
    
    # Extrair posts
    print("2️⃣ Extraindo posts e métricas de engagement...")
    posts = scraper.scrape_posts(html_content)
    
    # Exibir posts encontrados
    print(f"\n📱 === POSTS ENCONTRADOS ({len(posts)}) ===")
    for i, post in enumerate(posts, 1):
        badges = []
        if post.get('viral'):
            badges.append('🔥 VIRAL')
        if post.get('promoted'):
            badges.append('📢 PROMOVIDO')
        
        status = ' '.join(badges) if badges else ''
        
        print(f"\n📄 Post {i}: {post['id']} {status}")
        print(f"   👤 {post.get('username', 'N/A')} • {post.get('user_title', 'N/A')}")
        print(f"   👥 {post.get('followers', 0):,} seguidores")
        
        # Conteúdo (resumido)
        content = post.get('content', '')[:100] + '...' if len(post.get('content', '')) > 100 else post.get('content', '')
        print(f"   💬 {content}")
        
        # Engagement
        eng = post.get('engagement', {})
        print(f"   📊 Engagement: {eng.get('total_engagement', 0):,} total")
        print(f"      ❤️  {eng.get('likes', 0):,} curtidas")
        print(f"      💬 {eng.get('comments', 0):,} comentários")
        print(f"      🔄 {eng.get('shares', 0):,} shares")
        print(f"      🔖 {eng.get('saves', 0):,} salvamentos")
        print(f"      📈 {eng.get('engagement_rate', 0):.2f}% engagement rate")
        
        # Hashtags
        hashtags = post.get('hashtags', [])
        if hashtags:
            print(f"   🏷️  {', '.join(hashtags[:5])}")
        
        # Métricas adicionais
        print(f"   📝 {post.get('word_count', 0)} palavras")
        
        features = []
        if post.get('has_media'):
            features.append('📸 Mídia')
        if post.get('has_links'):
            features.append('🔗 Links')
        if post.get('has_emojis'):
            features.append('😊 Emojis')
        if post.get('has_mentions'):
            features.append('@ Menções')
        
        if features:
            print(f"   ✨ {', '.join(features)}")
    
    # Extrair trending topics
    print(f"\n🔥 === TÓPICOS EM TENDÊNCIA ===")
    trending_data = scraper.extrair_trending_topics(html_content)
    
    if trending_data.get('trending'):
        for i, topic in enumerate(trending_data['trending'], 1):
            print(f"{i}. {topic['tag']}")
            print(f"   📊 {topic['posts']} posts • {topic['engagement']:,} engagement")
            print(f"   📈 {topic['growth']:+.1f}% crescimento")
    
    # Analytics da plataforma
    print(f"\n📊 === ANALYTICS DA PLATAFORMA ===")
    analytics_data = scraper.extrair_analytics(html_content)
    
    if analytics_data.get('analytics'):
        analytics = analytics_data['analytics']
        print(f"👥 Usuários totais: {analytics.get('total_users', 0):,}")
        print(f"🟢 Ativos (24h): {analytics.get('active_24h', 0):,}")
        print(f"📝 Posts (24h): {analytics.get('posts_24h', 0):,}")
        print(f"📊 Taxa de engagement: {analytics.get('engagement_rate', 0):.1f}%")
        
        # Tipos de conteúdo
        content_types = analytics.get('top_content_types', [])
        if content_types:
            print(f"\n📋 Tipos de conteúdo populares:")
            for content_type in content_types:
                print(f"   • {content_type['type'].title()}: {content_type['percentage']}%")
    
    # Análise de padrões de engagement
    print(f"\n🧠 === ANÁLISE DE PADRÕES DE ENGAGEMENT ===")
    analise = scraper.analisar_engagement_patterns(posts)
    
    print(f"📱 Total de posts analisados: {analise['total_posts']}")
    print(f"🔥 Posts virais: {analise['posts_virais']}")
    print(f"📢 Posts promovidos: {analise['posts_promovidos']}")
    print(f"📝 Posts normais: {analise['posts_normais']}")
    
    # Estatísticas de engagement
    eng_stats = analise.get('engagement_stats', {})
    if eng_stats:
        print(f"\n📊 Engagement total: {eng_stats['total']:,}")
        print(f"📈 Engagement médio: {eng_stats['media']:,.1f}")
        print(f"🚀 Maior engagement: {eng_stats['maximo']:,}")
        print(f"📉 Menor engagement: {eng_stats['minimo']:,}")
    
    # Hashtags populares
    hashtags_pop = analise.get('hashtags_populares', {})
    if hashtags_pop:
        print(f"\n🏷️  Top hashtags:")
        for i, (tag, count) in enumerate(list(hashtags_pop.items())[:5], 1):
            print(f"   {i}. {tag}: {count} usos")
    
    # Tipos de conteúdo
    tipos = analise.get('tipos_conteudo', {})
    if tipos:
        print(f"\n📋 Análise de conteúdo:")
        print(f"   📸 Posts com mídia: {tipos['com_media']} ({tipos['percentual_media']:.1f}%)")
        print(f"   🔗 Posts com links: {tipos['com_links']} ({tipos['percentual_links']:.1f}%)")
        print(f"   😊 Posts com emojis: {tipos['com_emojis']} ({tipos['percentual_emojis']:.1f}%)")
    
    # Usuários top
    top_users = analise.get('usuarios_top_engagement', {})
    if top_users:
        print(f"\n👑 Top usuários por engagement:")
        for i, (username, engagement) in enumerate(list(top_users.items())[:3], 1):
            print(f"   {i}. {username}: {engagement:,} engagement total")
    
    # Performance por tipo
    if analise.get('performance_viral'):
        viral = analise['performance_viral']
        print(f"\n🔥 Performance posts virais:")
        print(f"   📊 Engagement médio: {viral['engagement_medio']:,.1f}")
        print(f"   🚀 Engagement total: {viral['total_engagement']:,}")
    
    if analise.get('performance_promovido'):
        promo = analise['performance_promovido']
        print(f"\n📢 Performance posts promovidos:")
        print(f"   📊 Engagement médio: {promo['engagement_medio']:,.1f}")
        print(f"   💰 Engagement total: {promo['total_engagement']:,}")
    
    # Salvar dados
    print(f"\n💾 === SALVANDO DADOS ===")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # CSV dos posts
    df_posts = pd.DataFrame(posts)
    filename_posts = f"social_media_posts_{timestamp}.csv"
    df_posts.to_csv(filename_posts, index=False, encoding='utf-8')
    print(f"✅ Posts salvos em: {filename_posts}")
    
    # JSON da análise completa
    dados_completos = {
        'posts': posts,
        'trending_topics': trending_data,
        'analytics': analytics_data,
        'analise_engagement': analise,
        'metadata': {
            'total_posts': len(posts),
            'scraped_at': datetime.now().isoformat(),
            'rate_limits': {
                'requests_per_second': scraper.rate_limiter.requests_per_second,
                'requests_per_minute': scraper.rate_limiter.requests_per_minute,
                'requests_per_hour': scraper.rate_limiter.requests_per_hour
            }
        }
    }
    
    filename_json = f"social_media_analysis_{timestamp}.json"
    with open(filename_json, 'w', encoding='utf-8') as f:
        json.dump(dados_completos, f, ensure_ascii=False, indent=2, default=str)
    print(f"✅ Análise completa salva em: {filename_json}")
    
    # Aplicações práticas
    print(f"\n💡 === APLICAÇÕES PRÁTICAS ===")
    aplicacoes = [
        "📊 Monitoramento de marca e menções",
        "🔥 Detecção de conteúdo viral",
        "📈 Análise de tendências em tempo real",
        "🎯 Identificação de influenciadores",
        "💰 Otimização de conteúdo promovido",
        "📱 Análise de concorrência",
        "🤖 Sistema de recomendações",
        "⚠️  Detecção de fake news"
    ]
    
    for app in aplicacoes:
        print(f"   {app}")
    
    print(f"\n🔧 === DICAS PARA PRODUÇÃO ===")
    dicas = [
        "🚦 Implemente rate limiting rigoroso",
        "⚖️  Respeite termos de uso das APIs",
        "🔐 Use autenticação OAuth quando disponível",
        "📊 Configure monitoramento de quotas",
        "🗄️  Implemente cache inteligente",
        "⚡ Use processamento assíncrono",
        "📧 Configure alertas para conteúdo viral",
        "🛡️  Implemente detecção de captcha/bloqueio"
    ]
    
    for dica in dicas:
        print(f"   {dica}")

if __name__ == "__main__":
    exemplo_uso()