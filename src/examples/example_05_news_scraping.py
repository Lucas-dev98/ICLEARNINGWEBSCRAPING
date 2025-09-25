#!/usr/bin/env python3
"""
Exemplo 05 - Scraping de Notícias e Blogs
=========================================

Este exemplo demonstra como fazer scraping em sites de notícias para:
- Extrair manchetes e artigos completos
- Coletar metadados (autor, data, categoria)
- Analisar sentimento das notícias
- Monitorar tendências de tópicos

IMPORTANTE: Sempre respeite os direitos autorais e robots.txt dos sites!

Autor: ICLearning WebScraping Project
Data: 2025-09-24
"""

# === IMPORTAÇÕES NECESSÁRIAS ===
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import json
from collections import Counter
import time

def simular_site_noticias():
    """Simula um site de notícias para demonstração."""
    html_exemplo = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Portal de Notícias Tech</title>
    </head>
    <body>
        <header>
            <h1>TechNews Brasil</h1>
        </header>
        
        <main class="container">
            <!-- Notícia Principal -->
            <article class="noticia destaque" data-id="1">
                <header class="noticia-header">
                    <h1 class="titulo">Inteligência Artificial revoluciona setor de saúde no Brasil</h1>
                    <div class="metadados">
                        <span class="autor">Por João Silva</span>
                        <time class="data-publicacao" datetime="2025-09-24T08:30:00">24/09/2025 08:30</time>
                        <span class="categoria">Tecnologia</span>
                        <span class="tempo-leitura">5 min de leitura</span>
                    </div>
                </header>
                <div class="conteudo">
                    <p class="lead">Hospitais brasileiros começam a implementar sistemas de IA para diagnósticos mais precisos e tratamentos personalizados.</p>
                    <p>A inteligência artificial está transformando rapidamente o setor de saúde brasileiro. Nos últimos meses, diversos hospitais começaram a adotar sistemas de IA para auxiliar em diagnósticos, especialmente na área de radiologia e oncologia.</p>
                    <p>Segundo dados do Ministério da Saúde, a implementação dessas tecnologias tem resultado em uma redução de 30% no tempo de diagnóstico e aumento de 25% na precisão dos resultados.</p>
                </div>
                <div class="tags">
                    <span class="tag">IA</span>
                    <span class="tag">Saúde</span>
                    <span class="tag">Brasil</span>
                    <span class="tag">Inovação</span>
                </div>
                <div class="engagement">
                    <span class="visualizacoes">12.543 visualizações</span>
                    <span class="compartilhamentos">234 compartilhamentos</span>
                    <span class="comentarios">89 comentários</span>
                </div>
            </article>

            <!-- Notícia 2 -->
            <article class="noticia" data-id="2">
                <header class="noticia-header">
                    <h2 class="titulo">Startup brasileira desenvolve app para agricultura sustentável</h2>
                    <div class="metadados">
                        <span class="autor">Por Maria Santos</span>
                        <time class="data-publicacao" datetime="2025-09-24T10:15:00">24/09/2025 10:15</time>
                        <span class="categoria">Startups</span>
                        <span class="tempo-leitura">3 min de leitura</span>
                    </div>
                </header>
                <div class="conteudo">
                    <p class="lead">Aplicativo utiliza dados de satélite e sensores IoT para otimizar uso de recursos na agricultura.</p>
                    <p>A startup AgroTech, com sede em São Paulo, lançou um aplicativo inovador que combina dados de satélite com sensores IoT para ajudar agricultores a otimizar o uso de água e fertilizantes.</p>
                    <p>A solução já está sendo testada em 50 propriedades rurais no interior de São Paulo, com resultados promissores de redução de 40% no consumo de água.</p>
                </div>
                <div class="tags">
                    <span class="tag">Agricultura</span>
                    <span class="tag">Startup</span>
                    <span class="tag">Sustentabilidade</span>
                    <span class="tag">IoT</span>
                </div>
                <div class="engagement">
                    <span class="visualizacoes">8.921 visualizações</span>
                    <span class="compartilhamentos">156 compartilhamentos</span>
                    <span class="comentarios">43 comentários</span>
                </div>
            </article>

            <!-- Notícia 3 -->
            <article class="noticia" data-id="3">
                <header class="noticia-header">
                    <h2 class="titulo">Criptomoedas brasileiras ganham espaço no mercado internacional</h2>
                    <div class="metadados">
                        <span class="autor">Por Carlos Oliveira</span>
                        <time class="data-publicacao" datetime="2025-09-24T14:45:00">24/09/2025 14:45</time>
                        <span class="categoria">Finanças</span>
                        <span class="tempo-leitura">4 min de leitura</span>
                    </div>
                </header>
                <div class="conteudo">
                    <p class="lead">Tokens desenvolvidos no Brasil começam a ser negociados em exchanges internacionais.</p>
                    <p>O cenário de criptomoedas brasileiras está em expansão, com várias tokens nacionais sendo listadas em exchanges estrangeiras. Especialistas apontam crescimento de 150% no último trimestre.</p>
                    <p>Entre os destaques estão tokens focados em sustentabilidade e inclusão financeira, áreas onde o Brasil tem se mostrado inovador.</p>
                </div>
                <div class="tags">
                    <span class="tag">Criptomoedas</span>
                    <span class="tag">Blockchain</span>
                    <span class="tag">Finanças</span>
                    <span class="tag">Brasil</span>
                </div>
                <div class="engagement">
                    <span class="visualizacoes">15.672 visualizações</span>
                    <span class="compartilhamentos">298 compartilhamentos</span>
                    <span class="comentarios">127 comentários</span>
                </div>
            </article>

            <!-- Notícia 4 -->
            <article class="noticia" data-id="4">
                <header class="noticia-header">
                    <h2 class="titulo">Educação digital: Universidades brasileiras lideram pesquisa em IA</h2>
                    <div class="metadados">
                        <span class="autor">Por Ana Costa</span>
                        <time class="data-publicacao" datetime="2025-09-23T16:20:00">23/09/2025 16:20</time>
                        <span class="categoria">Educação</span>
                        <span class="tempo-leitura">6 min de leitura</span>
                    </div>
                </header>
                <div class="conteudo">
                    <p class="lead">Pesquisadores brasileiros publicam estudos inovadores sobre aplicações educacionais da inteligência artificial.</p>
                    <p>Universidades como USP, UNICAMP e UFMG estão na vanguarda da pesquisa em IA aplicada à educação, desenvolvendo sistemas adaptativos de aprendizagem.</p>
                    <p>Os projetos incluem tutores virtuais inteligentes e sistemas de recomendação de conteúdo personalizado para diferentes perfis de estudantes.</p>
                </div>
                <div class="tags">
                    <span class="tag">Educação</span>
                    <span class="tag">IA</span>
                    <span class="tag">Universidades</span>
                    <span class="tag">Pesquisa</span>
                </div>
                <div class="engagement">
                    <span class="visualizacoes">7.234 visualizações</span>
                    <span class="compartilhamentos">189 compartilhamentos</span>
                    <span class="comentarios">65 comentários</span>
                </div>
            </article>
        </main>
    </body>
    </html>
    """
    return html_exemplo

class NoticiasScraper:
    """
    Scraper especializado em sites de notícias e blogs.
    
    Funcionalidades:
    - Extração de manchetes e conteúdo completo
    - Coleta de metadados (autor, data, categoria)
    - Análise de engajamento
    - Monitoramento de tendências
    """
    
    def __init__(self, delay_requests=1):
        """
        Inicializa o scraper de notícias.
        
        Args:
            delay_requests (int): Delay entre requests em segundos
        """
        self.delay = delay_requests
        self.session = requests.Session()
        
        # Headers apropriados para sites de notícias
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; NewsBot/1.0; Educational Purpose)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0'
        }
        self.session.headers.update(self.headers)
    
    def extrair_data_publicacao(self, elemento_data):
        """
        Extrai e normaliza data de publicação.
        
        Args:
            elemento_data: Elemento BeautifulSoup contendo data
            
        Returns:
            datetime: Data de publicação normalizada
        """
        if not elemento_data:
            return None
        
        # Tentar extrair de atributo datetime primeiro
        datetime_attr = elemento_data.get('datetime')
        if datetime_attr:
            try:
                return datetime.fromisoformat(datetime_attr.replace('Z', '+00:00'))
            except ValueError:
                pass
        
        # Extrair do texto do elemento
        texto_data = elemento_data.get_text().strip()
        
        # Padrões comuns de data em português
        padroes_data = [
            r'(\d{1,2})/(\d{1,2})/(\d{4})\s*(\d{1,2}):(\d{2})',  # 24/09/2025 08:30
            r'(\d{1,2})/(\d{1,2})/(\d{4})',                      # 24/09/2025
            r'(\d{4})-(\d{1,2})-(\d{1,2})\s*(\d{1,2}):(\d{2})',  # 2025-09-24 08:30
            r'(\d{4})-(\d{1,2})-(\d{1,2})',                      # 2025-09-24
        ]
        
        for padrao in padroes_data:
            match = re.search(padrao, texto_data)
            if match:
                try:
                    grupos = match.groups()
                    if len(grupos) >= 3:
                        if '/' in padrao:  # Formato brasileiro
                            dia, mes, ano = grupos[0], grupos[1], grupos[2]
                            hora, minuto = grupos[3:5] if len(grupos) >= 5 else ('0', '0')
                        else:  # Formato ISO
                            ano, mes, dia = grupos[0], grupos[1], grupos[2]
                            hora, minuto = grupos[3:5] if len(grupos) >= 5 else ('0', '0')
                        
                        return datetime(int(ano), int(mes), int(dia), 
                                     int(hora), int(minuto))
                except ValueError:
                    continue
        
        return None
    
    def extrair_numeros_engagement(self, texto):
        """
        Extrai números de engagement (visualizações, comentários, etc.).
        
        Args:
            texto (str): Texto contendo números
            
        Returns:
            int: Número extraído
        """
        if not texto:
            return 0
        
        # Extrair números, incluindo formatação com pontos/vírgulas
        numeros = re.findall(r'[\d.,]+', texto)
        if numeros:
            # Remover pontos de milhares
            numero_limpo = numeros[0].replace('.', '').replace(',', '')
            try:
                return int(numero_limpo)
            except ValueError:
                return 0
        return 0
    
    def extrair_tempo_leitura(self, texto):
        """
        Extrai tempo estimado de leitura.
        
        Args:
            texto (str): Texto contendo tempo de leitura
            
        Returns:
            int: Tempo em minutos
        """
        if not texto:
            return 0
        
        # Procurar padrões como "5 min", "3 minutos", etc.
        match = re.search(r'(\d+)\s*(min|minuto)', texto.lower())
        if match:
            return int(match.group(1))
        return 0
    
    def scrape_noticias(self, html_content):
        """
        Extrai notícias de uma página de site de notícias.
        
        Args:
            html_content (str): HTML da página
            
        Returns:
            list: Lista de notícias com metadados
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        noticias = []
        
        # Encontrar artigos de notícias
        elementos_noticia = soup.find_all('article', class_='noticia')
        
        print(f"📰 Encontradas {len(elementos_noticia)} notícias na página")
        
        for i, noticia in enumerate(elementos_noticia, 1):
            noticia_info = {}
            
            # ID da notícia
            noticia_info['id'] = noticia.get('data-id', f'noticia_{i}')
            
            # Título
            titulo_elem = noticia.find(['h1', 'h2'], class_='titulo')
            noticia_info['titulo'] = titulo_elem.get_text().strip() if titulo_elem else 'N/A'
            
            # Verificar se é destaque
            noticia_info['destaque'] = 'destaque' in noticia.get('class', [])
            
            # Metadados
            metadados = noticia.find('div', class_='metadados')
            if metadados:
                # Autor
                autor_elem = metadados.find('span', class_='autor')
                noticia_info['autor'] = autor_elem.get_text().replace('Por ', '').strip() if autor_elem else 'N/A'
                
                # Data de publicação
                data_elem = metadados.find('time', class_='data-publicacao')
                data_publicacao = self.extrair_data_publicacao(data_elem)
                noticia_info['data_publicacao'] = data_publicacao.isoformat() if data_publicacao else None
                noticia_info['data_publicacao_formatada'] = data_publicacao.strftime('%d/%m/%Y %H:%M') if data_publicacao else 'N/A'
                
                # Calcular idade da notícia
                if data_publicacao:
                    idade = datetime.now() - data_publicacao
                    noticia_info['horas_publicacao'] = idade.total_seconds() / 3600
                    noticia_info['idade_relativa'] = self.formatar_idade_noticia(idade)
                
                # Categoria
                categoria_elem = metadados.find('span', class_='categoria')
                noticia_info['categoria'] = categoria_elem.get_text().strip() if categoria_elem else 'Geral'
                
                # Tempo de leitura
                tempo_elem = metadados.find('span', class_='tempo-leitura')
                noticia_info['tempo_leitura'] = self.extrair_tempo_leitura(tempo_elem.get_text() if tempo_elem else '')
            
            # Lead (resumo)
            lead_elem = noticia.find('p', class_='lead')
            noticia_info['lead'] = lead_elem.get_text().strip() if lead_elem else ''
            
            # Conteúdo completo
            conteudo_div = noticia.find('div', class_='conteudo')
            if conteudo_div:
                paragrafos = conteudo_div.find_all('p')
                conteudo_completo = '\n\n'.join([p.get_text().strip() for p in paragrafos])
                noticia_info['conteudo'] = conteudo_completo
                
                # Estatísticas do texto
                noticia_info['num_paragrafos'] = len(paragrafos)
                noticia_info['num_caracteres'] = len(conteudo_completo)
                noticia_info['num_palavras'] = len(conteudo_completo.split())
            
            # Tags
            tags_elems = noticia.find_all('span', class_='tag')
            noticia_info['tags'] = [tag.get_text().strip() for tag in tags_elems]
            noticia_info['num_tags'] = len(noticia_info['tags'])
            
            # Métricas de engajamento
            engagement = noticia.find('div', class_='engagement')
            if engagement:
                # Visualizações
                views_elem = engagement.find('span', class_='visualizacoes')
                noticia_info['visualizacoes'] = self.extrair_numeros_engagement(
                    views_elem.get_text() if views_elem else ''
                )
                
                # Compartilhamentos
                shares_elem = engagement.find('span', class_='compartilhamentos')
                noticia_info['compartilhamentos'] = self.extrair_numeros_engagement(
                    shares_elem.get_text() if shares_elem else ''
                )
                
                # Comentários
                comments_elem = engagement.find('span', class_='comentarios')
                noticia_info['comentarios'] = self.extrair_numeros_engagement(
                    comments_elem.get_text() if comments_elem else ''
                )
                
                # Calcular engagement total
                noticia_info['engagement_total'] = (
                    noticia_info['compartilhamentos'] + 
                    noticia_info['comentarios']
                )
                
                # Taxa de engajamento (se houver visualizações)
                if noticia_info['visualizacoes'] > 0:
                    noticia_info['taxa_engajamento'] = (
                        noticia_info['engagement_total'] / noticia_info['visualizacoes'] * 100
                    )
            
            # Timestamp da coleta
            noticia_info['coletado_em'] = datetime.now().isoformat()
            
            noticias.append(noticia_info)
        
        return noticias
    
    def formatar_idade_noticia(self, idade):
        """
        Formata idade da notícia em texto legível.
        
        Args:
            idade (timedelta): Diferença de tempo
            
        Returns:
            str: Idade formatada
        """
        if idade.days > 0:
            return f"{idade.days} dia(s) atrás"
        elif idade.seconds > 3600:
            horas = idade.seconds // 3600
            return f"{horas} hora(s) atrás"
        elif idade.seconds > 60:
            minutos = idade.seconds // 60
            return f"{minutos} minuto(s) atrás"
        else:
            return "Agora mesmo"
    
    def analisar_tendencias(self, noticias):
        """
        Analisa tendências nas notícias coletadas.
        
        Args:
            noticias (list): Lista de notícias
            
        Returns:
            dict: Análise de tendências
        """
        if not noticias:
            return {'erro': 'Nenhuma notícia para analisar'}
        
        df = pd.DataFrame(noticias)
        
        # Contadores
        todas_tags = []
        todas_categorias = []
        todos_autores = []
        
        for noticia in noticias:
            todas_tags.extend(noticia.get('tags', []))
            todas_categorias.append(noticia.get('categoria', 'Geral'))
            todos_autores.append(noticia.get('autor', 'N/A'))
        
        analise = {
            'total_noticias': len(noticias),
            'noticias_destaque': len([n for n in noticias if n.get('destaque')]),
            
            # Tendências de tópicos
            'tags_populares': dict(Counter(todas_tags).most_common(10)),
            'categorias_populares': dict(Counter(todas_categorias).most_common(5)),
            'autores_ativos': dict(Counter(todos_autores).most_common(5)),
            
            # Métricas de engajamento
            'total_visualizacoes': sum(n.get('visualizacoes', 0) for n in noticias),
            'total_compartilhamentos': sum(n.get('compartilhamentos', 0) for n in noticias),
            'total_comentarios': sum(n.get('comentarios', 0) for n in noticias),
            
            # Métricas de conteúdo
            'tempo_leitura_medio': sum(n.get('tempo_leitura', 0) for n in noticias) / len(noticias),
            'palavras_media': sum(n.get('num_palavras', 0) for n in noticias) / len(noticias),
        }
        
        # Notícia mais popular
        if df['visualizacoes'].sum() > 0:
            mais_popular = df.loc[df['visualizacoes'].idxmax()]
            analise['noticia_mais_popular'] = {
                'titulo': mais_popular['titulo'],
                'visualizacoes': mais_popular['visualizacoes'],
                'autor': mais_popular['autor']
            }
        
        # Melhor engajamento
        if 'taxa_engajamento' in df.columns and not df['taxa_engajamento'].isna().all():
            melhor_engajamento = df.loc[df['taxa_engajamento'].idxmax()]
            analise['melhor_engajamento'] = {
                'titulo': melhor_engajamento['titulo'],
                'taxa': melhor_engajamento['taxa_engajamento'],
                'categoria': melhor_engajamento['categoria']
            }
        
        return analise

def exemplo_uso():
    """Demonstra o uso prático do NoticiasScraper."""
    print("📰 === EXEMPLO DE SCRAPING DE NOTÍCIAS ===")
    print("=" * 50)
    
    # Inicializar scraper
    scraper = NoticiasScraper(delay_requests=1)
    
    # Simular site de notícias (em produção seria requests.get())
    print("1️⃣ Obtendo dados do site de notícias...")
    html_content = simular_site_noticias()
    
    # Extrair notícias
    print("2️⃣ Extraindo notícias da página...")
    noticias = scraper.scrape_noticias(html_content)
    
    # Exibir notícias encontradas
    print(f"\n📋 === NOTÍCIAS EXTRAÍDAS ({len(noticias)}) ===")
    for i, noticia in enumerate(noticias, 1):
        print(f"\n📰 Notícia {i} {'🌟 DESTAQUE' if noticia.get('destaque') else ''}")
        print(f"   📄 {noticia['titulo']}")
        print(f"   ✍️  {noticia['autor']} | 📅 {noticia['data_publicacao_formatada']}")
        print(f"   🏷️  {noticia['categoria']} | ⏱️  {noticia['tempo_leitura']} min leitura")
        
        if noticia.get('lead'):
            print(f"   📝 {noticia['lead']}")
        
        if noticia.get('tags'):
            print(f"   🏪 Tags: {', '.join(noticia['tags'])}")
        
        print(f"   👀 {noticia.get('visualizacoes', 0):,} visualizações")
        print(f"   🔄 {noticia.get('compartilhamentos', 0)} compartilhamentos")
        print(f"   💬 {noticia.get('comentarios', 0)} comentários")
        
        if noticia.get('taxa_engajamento'):
            print(f"   📊 Taxa engajamento: {noticia['taxa_engajamento']:.2f}%")
        
        if noticia.get('idade_relativa'):
            print(f"   🕐 {noticia['idade_relativa']}")
    
    # Análise de tendências
    print(f"\n📊 === ANÁLISE DE TENDÊNCIAS ===")
    analise = scraper.analisar_tendencias(noticias)
    
    print(f"📈 Total de notícias: {analise['total_noticias']}")
    print(f"🌟 Notícias em destaque: {analise['noticias_destaque']}")
    print(f"👀 Total de visualizações: {analise['total_visualizacoes']:,}")
    print(f"🔄 Total de compartilhamentos: {analise['total_compartilhamentos']:,}")
    print(f"💬 Total de comentários: {analise['total_comentarios']:,}")
    print(f"⏱️  Tempo médio de leitura: {analise['tempo_leitura_medio']:.1f} min")
    print(f"📝 Palavras por notícia: {analise['palavras_media']:.0f}")
    
    # Tags populares
    if analise['tags_populares']:
        print(f"\n🔥 Tags mais populares:")
        for tag, count in list(analise['tags_populares'].items())[:5]:
            print(f"   • {tag}: {count} notícias")
    
    # Categorias populares
    if analise['categorias_populares']:
        print(f"\n📂 Categorias mais ativas:")
        for categoria, count in analise['categorias_populares'].items():
            print(f"   • {categoria}: {count} notícias")
    
    # Autores ativos
    if analise['autores_ativos']:
        print(f"\n✍️  Autores mais ativos:")
        for autor, count in list(analise['autores_ativos'].items())[:3]:
            print(f"   • {autor}: {count} notícias")
    
    # Notícia mais popular
    if 'noticia_mais_popular' in analise:
        popular = analise['noticia_mais_popular']
        print(f"\n🏆 Notícia mais popular:")
        print(f"   📄 {popular['titulo']}")
        print(f"   👀 {popular['visualizacoes']:,} visualizações")
        print(f"   ✍️  {popular['autor']}")
    
    # Melhor engajamento
    if 'melhor_engajamento' in analise:
        engajamento = analise['melhor_engajamento']
        print(f"\n📊 Melhor engajamento:")
        print(f"   📄 {engajamento['titulo']}")
        print(f"   📈 {engajamento['taxa']:.2f}% de engajamento")
        print(f"   🏷️  {engajamento['categoria']}")
    
    # Salvar dados
    print(f"\n💾 Salvando dados...")
    df = pd.DataFrame(noticias)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # CSV das notícias
    filename_csv = f"noticias_{timestamp}.csv"
    df.to_csv(filename_csv, index=False, encoding='utf-8')
    print(f"✅ Notícias salvas em: {filename_csv}")
    
    # JSON da análise
    filename_json = f"analise_tendencias_{timestamp}.json"
    with open(filename_json, 'w', encoding='utf-8') as f:
        json.dump(analise, f, ensure_ascii=False, indent=2, default=str)
    print(f"✅ Análise salva em: {filename_json}")
    
    # Dicas para uso real
    print(f"\n💡 === APLICAÇÕES PRÁTICAS ===")
    aplicacoes = [
        "📊 Monitoramento de trending topics",
        "🎯 Análise de sentimento de notícias",
        "📈 Tracking de menções de marca/pessoa",
        "🔍 Descoberta de fontes de notícias",
        "📢 Alertas para palavras-chave específicas",
        "📰 Agregação automática de notícias",
        "🏷️  Classificação automática por tópico",
        "⚡ Feed personalizado de notícias"
    ]
    
    for app in aplicacoes:
        print(f"   {app}")
    
    print(f"\n🔧 === DICAS PARA PRODUÇÃO ===")
    dicas = [
        "⏱️  Use delays apropriados entre requests",
        "🔄 Implemente cache para evitar re-scraping",
        "📊 Configure banco de dados para histórico",
        "🤖 Respeite robots.txt e rate limits",
        "📧 Configure alertas para breaking news",
        "🔐 Use proxies se necessário",
        "📈 Monitore métricas de qualidade dos dados",
        "🛡️  Trate exceções de rede adequadamente"
    ]
    
    for dica in dicas:
        print(f"   {dica}")

if __name__ == "__main__":
    exemplo_uso()