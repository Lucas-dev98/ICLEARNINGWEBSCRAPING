"""
Scraper Profissional de Notícias - Web Scraping Avançado

Este script demonstra um sistema completo e profissional de web scraping
para coleta automatizada de notícias, incluindo tratamento de erros robusto,
gerenciamento de dados e exportação para múltiplos formatos.

Funcionalidades implementadas:
- Classe orientada a objetos para scraping estruturado
- Tratamento de requisições HTTP com headers customizados
- Parsing inteligente com múltiplos seletores
- Detecção automática de links e estruturas
- Remoção de duplicatas e limpeza de dados
- Exportação para CSV e DataFrame pandas
- Rate limiting para requisições responsáveis
- Logging e relatórios de progresso

Conceitos avançados abordados:
- Programação orientada a objetos aplicada ao web scraping
- Gerenciamento de estado e dados persistentes
- Headers HTTP para evitar bloqueios (User-Agent spoofing)
- Delay entre requisições (rate limiting)
- Estruturas de dados complexas (listas de dicionários)
- Integração com pandas para análise de dados
- Manipulação de arquivos CSV com encoding UTF-8
- Tratamento de casos edge e validações

Casos de uso:
- Monitoramento automático de portais de notícias
- Coleta de dados para análise de sentimento
- Agregação de conteúdo de múltiplas fontes
- Alertas automáticos sobre tópicos específicos
- Análise de trends e padrões de mídia
"""

# === IMPORTAÇÕES ORGANIZADAS ===
# Requisições HTTP e parsing
import requests                 # Biblioteca para requisições HTTP/HTTPS
from bs4 import BeautifulSoup  # Parser HTML/XML avançado

# Manipulação e análise de dados
import pandas as pd            # Biblioteca para análise de dados estruturados
import csv                     # Módulo para manipulação de arquivos CSV

# Utilitários de sistema e tempo
import time                    # Controle de delay e timing
from datetime import datetime  # Manipulação de datas e timestamps

class NoticiasScraper:
    """
    Classe principal para scraping profissional de notícias
    
    Esta classe implementa um sistema completo de web scraping orientado a objetos
    com funcionalidades avançadas para coleta, processamento e armazenamento
    de dados de notícias de forma escalável e responsável.
    
    Attributes:
        base_url (str): URL base do site para scraping
        headers (dict): Cabeçalhos HTTP para requisições
        noticias (list): Lista acumuladora de notícias coletadas
    
    Design Patterns utilizados:
    - Template Method: estrutura de scraping reutilizável
    - Strategy: diferentes estratégias de extração por site
    - Builder: construção incremental da coleção de notícias
    """
    
    def __init__(self, base_url, headers=None):
        """
        Inicializa o scraper com configurações básicas
        
        Args:
            base_url (str): URL base do site alvo para scraping
            headers (dict, optional): Cabeçalhos HTTP customizados.
                                    Se None, usa User-Agent padrão para evitar bloqueios.
        
        Design Notes:
        - User-Agent spoofing para parecer um navegador real
        - Headers personalizáveis para diferentes sites
        - Estado interno para acumular resultados entre chamadas
        """
        # === CONFIGURAÇÃO BASE ===
        self.base_url = base_url
        
        # === HEADERS HTTP PARA EVITAR DETECÇÃO ===
        self.headers = headers or {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        # User-Agent spoofing é crucial porque:
        # - Muitos sites bloqueiam requests com User-Agent padrão do Python
        # - Simula um navegador real (Chrome no Windows)
        # - Reduz chance de ser detectado como bot
        # - Alguns sites servem conteúdo diferente baseado no User-Agent
        
        # === ARMAZENAMENTO DE DADOS ===
        self.noticias = []  # Lista acumuladora de todas as notícias coletadas
        # Estrutura de cada notícia: dict com chaves 'titulo', 'link', 'tag', 'timestamp'
    
    def fazer_requisicao(self, url):
        """
        Executa requisição HTTP com tratamento robusto de erros
        
        Método centralizado para todas as requisições HTTP do scraper,
        implementando boas práticas de tratamento de erros e logging.
        
        Args:
            url (str): URL completa ou relativa para requisição
        
        Returns:
            requests.Response or None: Objeto Response se sucesso, None se erro
        
        Error Handling:
        - ConnectionError: problemas de rede/conectividade
        - Timeout: requisição demorou mais que o limite
        - HTTPError: status codes 4xx/5xx
        - RequestException: qualquer outro erro de requisição
        """
        try:
            # === EXECUÇÃO DA REQUISIÇÃO ===
            response = requests.get(url, headers=self.headers)
            # requests.get() automaticamente:
            # - Gerencia conexões TCP/TLS
            # - Segue redirecionamentos (até 30 por padrão)
            # - Decodifica conteúdo baseado em Content-Type
            # - Aplica os headers especificados
            
            # === VALIDAÇÃO DE STATUS HTTP ===
            response.raise_for_status()
            # Levanta HTTPError se status code indica erro:
            # - 4xx: Client errors (400 Bad Request, 404 Not Found, 403 Forbidden)
            # - 5xx: Server errors (500 Internal Server Error, 502 Bad Gateway)
            # - 2xx e 3xx: considerados sucessos
            
            return response
            
        except requests.RequestException as e:
            # === TRATAMENTO UNIFICADO DE ERROS ===
            print(f"❌ Erro na requisição para {url}: {e}")
            # RequestException é a classe base para todos os erros do requests:
            # - ConnectionError: DNS, network unreachable, connection refused
            # - Timeout: ReadTimeout, ConnectTimeout
            # - HTTPError: status codes de erro (via raise_for_status)
            # - TooManyRedirects: loop de redirecionamentos
            # - InvalidURL: URL malformada
            
            # TODO: Implementar logging mais sofisticado
            # TODO: Retry mechanism com backoff exponencial
            # TODO: Diferentes estratégias por tipo de erro
            
            return None
    
    def extrair_noticias_exemplo(self, html_content):
        """
        Extrai notícias usando estratégia de seletores múltiplos
        
        Implementa uma abordagem genérica e adaptável para extração de notícias
        que funciona com a maioria dos sites de notícias, usando padrões comuns
        de estruturação de conteúdo HTML.
        
        Args:
            html_content (str): Conteúdo HTML bruto da página
        
        Returns:
            list: Lista de dicionários com dados das notícias extraídas
                 Estrutura: {'titulo', 'link', 'tag', 'timestamp'}
        
        Strategy Pattern:
        Esta função implementa uma estratégia genérica que pode ser
        substituída por estratégias específicas para diferentes sites.
        
        Adaptation Notes:
        Para sites específicos, adapte:
        1. Lista de seletores CSS
        2. Lógica de extração de links
        3. Filtros de qualidade de conteúdo
        4. Campos adicionais específicos do site
        """
        # === PARSING DO CONTEÚDO HTML ===
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # === LISTA ACUMULADORA DE RESULTADOS ===
        manchetes = []
        
        # === ESTRATÉGIA DE SELETORES MÚLTIPLOS ===
        # Lista de seletores CSS ordenada por prioridade/especificidade
        seletores_prioritarios = [
            'h1',           # Títulos principais (maior prioridade)
            'h2',           # Subtítulos importantes
            'h3',           # Títulos secundários
            '.titulo',      # Classes comuns para títulos
            '.manchete',    # Classes específicas de notícias
            '.headline',    # Padrão internacional
            '.title',       # Variação comum
            '.news-title'   # Padrão específico de sites de notícias
        ]
        
        # === EXTRAÇÃO ITERATIVA POR SELETOR ===
        for seletor in seletores_prioritarios:
            elementos = soup.select(seletor)
            # select() retorna lista de elementos que correspondem ao seletor CSS
            
            for elemento in elementos:
                # === EXTRAÇÃO E LIMPEZA DE TEXTO ===
                texto = elemento.get_text().strip()
                # get_text(): extrai todo texto interno (sem HTML)
                # strip(): remove espaços/quebras de linha nas extremidades
                
                # === FILTRO DE QUALIDADE DE CONTEÚDO ===
                if len(texto) > 20:  # Filtra textos muito curtos (provavelmente não são notícias)
                    # TODO: Implementar filtros mais sofisticados:
                    # - Detecção de idioma
                    # - Filtro de palavras-chave spam
                    # - Análise de estrutura de frase
                    
                    # === DETECÇÃO INTELIGENTE DE LINKS ===
                    link = None
                    
                    # Caso 1: O próprio elemento é um link <a>
                    if elemento.name == 'a':
                        link = elemento.get('href')
                    
                    # Caso 2: Link dentro do elemento (filho)
                    else:
                        link_tag = elemento.find('a')  # Procura primeiro <a> filho
                        if not link_tag:
                            # Caso 3: Elemento está dentro de um link (pai)
                            link_tag = elemento.find_parent('a')  # Procura <a> pai
                        
                        if link_tag:
                            link = link_tag.get('href')
                    
                    # === NORMALIZAÇÃO DE LINKS ===
                    # TODO: Implementar conversão de links relativos para absolutos
                    # if link and not link.startswith('http'):
                    #     link = urljoin(self.base_url, link)
                    
                    # === CONSTRUÇÃO DO OBJETO NOTÍCIA ===
                    manchetes.append({
                        'titulo': texto,                    # Texto limpo da manchete
                        'link': link,                       # URL da notícia (pode ser None)
                        'tag': elemento.name,               # Tag HTML original (h1, h2, div, etc.)
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Momento da coleta
                    })
                    
                    # Campos adicionais que podem ser úteis:
                    # - 'fonte': self.base_url
                    # - 'resumo': extração de primeiras linhas
                    # - 'categoria': classificação automática
                    # - 'autor': extração de byline
                    # - 'data_publicacao': parsing de datas do conteúdo
        
        # === REMOÇÃO DE DUPLICATAS LOCAIS ===
        # Remove duplicatas dentro desta página baseado no título
        titulos_vistos = set()
        manchetes_unicas = []
        
        for manchete in manchetes:
            titulo_normalizado = manchete['titulo'].lower().strip()
            if titulo_normalizado not in titulos_vistos:
                titulos_vistos.add(titulo_normalizado)
                manchetes_unicas.append(manchete)
        
        return manchetes_unicas
    
    def scrape_site(self, url):
        """
        Executa pipeline completo de scraping para um site específico
        
        Método principal que orquestra todo o processo de coleta de dados
        de uma URL, desde a requisição até a extração estruturada.
        
        Args:
            url (str): URL completa do site para fazer scraping
        
        Returns:
            list: Lista de notícias extraídas ou lista vazia se erro
        
        Pipeline Implementation:
        1. Log de início da operação
        2. Requisição HTTP com tratamento de erros
        3. Validação de resposta
        4. Extração de dados estruturados
        5. Log de resultados
        6. Retorno de dados limpos
        """
        # === LOG DE INÍCIO DA OPERAÇÃO ===
        print(f"🔍 Fazendo scraping de: {url}")
        # Log importante para debugging e monitoramento de progresso
        
        # === REQUISIÇÃO COM TRATAMENTO DE ERROS ===
        response = self.fazer_requisicao(url)
        if not response:
            # Se requisição falhou, retorna lista vazia
            # Permite que o scraping continue com outras URLs
            print(f"⚠️  Pulando {url} devido a erro de requisição")
            return []
        
        # === EXTRAÇÃO DE DADOS ESTRUTURADOS ===
        noticias = self.extrair_noticias_exemplo(response.text)
        # response.text contém o HTML completo da página
        # extrair_noticias_exemplo() processa e estrutura os dados
        
        # === LOG DE RESULTADOS ===
        print(f"✅ Encontradas {len(noticias)} notícias em {url}")
        
        # === ESTATÍSTICAS ADICIONAIS (OPCIONAL) ===
        if noticias:
            com_link = sum(1 for n in noticias if n['link'])
            print(f"   📎 {com_link}/{len(noticias)} notícias com links válidos")
        
        return noticias
    
    def salvar_csv(self, filename='noticias.csv'):
        """
        Exporta notícias coletadas para arquivo CSV com encoding seguro
        
        Método de persistência que salva todos os dados coletados em formato
        estruturado CSV, adequado para análise posterior e importação em
        outras ferramentas (Excel, Google Sheets, bancos de dados).
        
        Args:
            filename (str): Nome do arquivo CSV de destino
                          Padrão: 'noticias.csv'
        
        CSV Structure:
        - titulo: Manchete/título da notícia
        - link: URL da notícia (pode ser None)
        - tag: Tag HTML original do elemento
        - timestamp: Data/hora da coleta no formato ISO
        
        Encoding & Compatibility:
        - UTF-8 para suporte completo a acentos/caracteres especiais
        - newline='' para compatibilidade com Excel
        - DictWriter para mapeamento automático de campos
        """
        # === VALIDAÇÃO DE DADOS ===
        if not self.noticias:
            print("⚠️  Nenhuma notícia coletada para salvar")
            return
        
        try:
            # === ABERTURA SEGURA DO ARQUIVO ===
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                # Context manager garante fechamento mesmo com erro
                # newline='': evita linhas em branco extras no CSV
                # encoding='utf-8': suporte completo a caracteres especiais
                
                # === CONFIGURAÇÃO DO WRITER CSV ===
                fieldnames = ['titulo', 'link', 'tag', 'timestamp']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                # DictWriter mapeia automaticamente chaves do dict para colunas
                
                # === ESCRITA DE CABEÇALHO E DADOS ===
                writer.writeheader()            # Primeira linha com nomes das colunas
                writer.writerows(self.noticias) # Todas as linhas de dados
                
            # === CONFIRMAÇÃO DE SUCESSO ===
            print(f"💾 {len(self.noticias)} notícias salvas em '{filename}'")
            
        except IOError as e:
            # === TRATAMENTO DE ERROS DE ARQUIVO ===
            print(f"❌ Erro ao salvar CSV: {e}")
            # Possíveis erros: sem permissão, disco cheio, caminho inválido
    
    def criar_dataframe(self):
        """
        Converte dados coletados em DataFrame pandas para análise avançada
        
        Transforma a lista de notícias em um DataFrame pandas, estrutura
        otimizada para análise de dados, visualização e operações estatísticas.
        
        Returns:
            pd.DataFrame or None: DataFrame com notícias ou None se sem dados
        
        DataFrame Features:
        - Indexação eficiente para consultas rápidas
        - Operações vetorizadas para análise em massa
        - Integração com matplotlib/seaborn para visualização
        - Exportação fácil para múltiplos formatos (Excel, JSON, SQL)
        - Operações de grupo, filtro e agregação
        
        Análises possíveis com o DataFrame:
        - Contagem de notícias por tag HTML
        - Análise temporal de coletas
        - Detecção de padrões em títulos
        - Estatísticas de disponibilidade de links
        - Agrupamento por fonte/domínio
        """
        # === VALIDAÇÃO DE DADOS ===
        if not self.noticias:
            print("⚠️  Nenhuma notícia para converter em DataFrame")
            return None
        
        try:
            # === CRIAÇÃO DO DATAFRAME ===
            df = pd.DataFrame(self.noticias)
            # pandas automaticamente:
            # - Detecta tipos de dados apropriados
            # - Cria índice numérico sequencial
            # - Otimiza armazenamento em memória
            # - Permite operações vetorizadas
            
            # === OTIMIZAÇÕES OPCIONAIS ===
            # Conversão de timestamp para datetime para análise temporal
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Categorização da coluna 'tag' para economia de memória
            if 'tag' in df.columns:
                df['tag'] = df['tag'].astype('category')
            
            print(f"📊 DataFrame criado com {len(df)} notícias e {len(df.columns)} colunas")
            return df
            
        except Exception as e:
            # === TRATAMENTO DE ERROS DE PANDAS ===
            print(f"❌ Erro ao criar DataFrame: {e}")
            return None
    
    def executar_scraping(self, urls, delay=1):
        """
        Executa scraping em lote com rate limiting e deduplicação
        
        Método principal para operações de scraping em massa, implementando
        boas práticas de web scraping responsável e processamento eficiente.
        
        Args:
            urls (list): Lista de URLs para processar sequencialmente
            delay (int): Segundos de delay entre requisições (padrão: 1s)
        
        Features Implementadas:
        - Rate limiting para não sobrecarregar servidores
        - Processamento sequencial com tratamento de erros individual
        - Acumulação progressiva de resultados
        - Deduplicação global baseada em título
        - Relatórios de progresso e estatísticas finais
        
        Ethical Web Scraping:
        - Respeita recursos do servidor com delays
        - Não faz requisições paralelas excessivas  
        - Implementa User-Agent apropriado
        - Permite configuração de rate limit por site
        
        Data Quality:
        - Remove duplicatas cross-site
        - Normaliza dados para consistência
        - Valida qualidade de conteúdo extraído
        """
        print(f"🚀 Iniciando scraping de {len(urls)} URLs com delay de {delay}s")
        
        # === PROCESSAMENTO SEQUENCIAL COM RATE LIMITING ===
        for i, url in enumerate(urls, 1):
            print(f"\n--- Processando {i}/{len(urls)} ---")
            
            # === SCRAPING INDIVIDUAL DA URL ===
            noticias = self.scrape_site(url)
            
            # === ACUMULAÇÃO PROGRESSIVA DE RESULTADOS ===
            self.noticias.extend(noticias)
            # extend() adiciona todos os elementos da lista ao invés de 
            # append() que adicionaria a lista como um único elemento
            
            print(f"📈 Total acumulado até agora: {len(self.noticias)} notícias")
            
            # === RATE LIMITING RESPONSÁVEL ===
            if i < len(urls):  # Não faz delay após a última URL
                print(f"⏳ Aguardando {delay}s antes da próxima requisição...")
                time.sleep(delay)
                # Rate limiting é essencial para:
                # - Evitar sobrecarga dos servidores
                # - Reduzir chance de ser bloqueado/banido
                # - Simular comportamento humano
                # - Respeitar robots.txt e ToS dos sites
        
        # === DEDUPLICAÇÃO GLOBAL AVANÇADA ===
        print(f"\n🔄 Removendo duplicatas...")
        titulos_vistos = set()
        noticias_unicas = []
        duplicatas_removidas = 0
        
        for noticia in self.noticias:
            # === NORMALIZAÇÃO DE TÍTULO PARA COMPARAÇÃO ===
            titulo_normalizado = noticia['titulo'].lower().strip()
            # lower(): padroniza caixa para comparação case-insensitive
            # strip(): remove espaços extras que podem causar falsos negativos
            
            # TODO: Implementar normalização mais avançada:
            # - Remoção de pontuação
            # - Stemming/lemmatização para raízes de palavras
            # - Detecção de títulos similares (fuzzy matching)
            # - Normalização de encoding (acentos, caracteres especiais)
            
            if titulo_normalizado not in titulos_vistos:
                titulos_vistos.add(titulo_normalizado)
                noticias_unicas.append(noticia)
            else:
                duplicatas_removidas += 1
        
        # === ATUALIZAÇÃO DOS DADOS LIMPOS ===
        self.noticias = noticias_unicas
        
        # === RELATÓRIO FINAL DETALHADO ===
        print(f"\n🎯 === RELATÓRIO FINAL ===")
        print(f"✅ URLs processadas: {len(urls)}")
        print(f"📰 Notícias coletadas: {len(self.noticias)} únicas")
        print(f"🗑️  Duplicatas removidas: {duplicatas_removidas}")
        
        # === ESTATÍSTICAS ADICIONAIS ===
        if self.noticias:
            com_links = sum(1 for n in self.noticias if n['link'])
            taxa_links = (com_links / len(self.noticias)) * 100
            print(f"🔗 Notícias com links: {com_links} ({taxa_links:.1f}%)")
            
            # Análise de tags mais comuns
            from collections import Counter
            tags_counter = Counter(n['tag'] for n in self.noticias)
            tag_mais_comum = tags_counter.most_common(1)[0] if tags_counter else ('N/A', 0)
            print(f"🏷️  Tag mais comum: {tag_mais_comum[0]} ({tag_mais_comum[1]} ocorrências)")
        
        print(f"⏱️  Tempo total estimado: {len(urls) * delay:.1f}s (delays) + tempo de processamento")

# === SEÇÃO DE DEMONSTRAÇÃO E TESTES ===

def exemplo_uso():
    """
    Função de demonstração completa do sistema de scraping
    
    Esta função exemplifica todos os recursos principais do NoticiasScraper
    usando dados HTML simulados, demonstrando um fluxo completo desde
    a coleta até a exportação dos dados.
    
    Funcionalidades demonstradas:
    1. Inicialização do scraper com configurações
    2. Extração de dados de HTML estruturado
    3. Processamento e limpeza dos resultados
    4. Análise com pandas DataFrame
    5. Exportação para arquivo CSV
    6. Relatórios e estatísticas
    
    Casos de teste incluídos:
    - Títulos com diferentes tags HTML (h1, h2, h3, div)
    - Links diretos e aninhados
    - Conteúdo sem links (edge case)
    - Diferentes estruturas de markup
    """
    
    print("🧪 === DEMONSTRAÇÃO DO SCRAPER DE NOTÍCIAS ===\n")
    
    # === DADOS DE TESTE REALISTAS ===
    html_exemplo = """
    <html>
    <head>
        <title>Portal de Notícias - Exemplo</title>
    </head>
    <body>
        <div class="noticias">
            <h1><a href="/noticia1">Brasil registra crescimento econômico no último trimestre</a></h1>
            <h2><a href="/noticia2">Nova tecnologia promete revolucionar energia solar</a></h2>
            <h3>Pequena notícia sem link relevante</h3>
            <div class="manchete">
                <a href="/noticia3">Descoberta arqueológica importante no interior de Minas Gerais</a>
            </div>
            <p class="titulo">
                <a href="/noticia4">Startup brasileira desenvolve solução inovadora para agricultura</a>
            </p>
            <span class="headline">Texto muito curto</span>
            <div class="news-title">
                <a href="/noticia5">Universidades públicas lideram ranking de pesquisa científica no país</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Este HTML de teste simula uma estrutura típica de portal de notícias:
    # - Diferentes níveis de títulos (h1, h2, h3)
    # - Classes CSS comuns (.manchete, .titulo, .headline, .news-title) 
    # - Links em diferentes estruturas (diretos, aninhados)
    # - Casos edge: sem links, textos curtos
    # - Markup variado para testar flexibilidade dos seletores
    
    # === INICIALIZAÇÃO DO SCRAPER ===
    print("1️⃣ Inicializando scraper...")
    scraper = NoticiasScraper("https://exemplo.com")
    # URL base fictícia para demonstração
    
    # === EXTRAÇÃO DE DADOS ===
    print("2️⃣ Extraindo notícias do HTML de exemplo...")
    noticias = scraper.extrair_noticias_exemplo(html_exemplo)
    scraper.noticias = noticias  # Simula coleta real
    
    # === EXIBIÇÃO DE RESULTADOS ESTRUTURADOS ===
    print(f"\n📰 === NOTÍCIAS EXTRAÍDAS ({len(noticias)} encontradas) ===")
    for i, noticia in enumerate(noticias, 1):
        print(f"\n{i}. 📰 {noticia['titulo']}")
        print(f"   🔗 Link: {noticia['link'] or 'Sem link'}")
        print(f"   🏷️  Tag HTML: <{noticia['tag']}>")
        print(f"   ⏰ Coletado: {noticia['timestamp']}")
    
    # === ANÁLISE COM PANDAS DATAFRAME ===
    print(f"\n3️⃣ Criando DataFrame para análise...")
    df = scraper.criar_dataframe()
    
    if df is not None:
        print(f"\n📊 === ANÁLISE DOS DADOS ===")
        print(f"Dimensões: {df.shape[0]} linhas × {df.shape[1]} colunas")
        
        # Mostra preview dos dados
        print(f"\n📋 Preview do DataFrame:")
        print(df[['titulo', 'tag', 'link']].to_string(index=False, max_colwidth=50))
        
        # Estatísticas básicas
        print(f"\n📈 Estatísticas:")
        print(f"• Notícias com links: {df['link'].notna().sum()}/{len(df)}")
        print(f"• Tags mais usadas: {df['tag'].value_counts().to_dict()}")
        
        # Análise de qualidade dos títulos
        df['tamanho_titulo'] = df['titulo'].str.len()
        print(f"• Tamanho médio dos títulos: {df['tamanho_titulo'].mean():.1f} caracteres")
        print(f"• Título mais longo: {df['tamanho_titulo'].max()} chars")
        print(f"• Título mais curto: {df['tamanho_titulo'].min()} chars")
    
    # === EXPORTAÇÃO PARA CSV ===
    print(f"\n4️⃣ Exportando dados para CSV...")
    scraper.salvar_csv('exemplo_noticias.csv')
    
    # === DEMONSTRAÇÃO DE SCRAPING EM LOTE ===
    print(f"\n5️⃣ Simulando scraping em múltiplas URLs...")
    urls_exemplo = [
        "https://exemplo1.com/noticias",
        "https://exemplo2.com/ultimas",  
        "https://exemplo3.com/manchetes"
    ]
    
    print("URLs que seriam processadas:")
    for i, url in enumerate(urls_exemplo, 1):
        print(f"   {i}. {url}")
    
    print("\n💡 Para scraping real, descomente a linha abaixo:")
    print("# scraper.executar_scraping(urls_exemplo, delay=2)")
    
    # === DICAS DE USO AVANÇADO ===
    print(f"\n🎯 === PRÓXIMOS PASSOS ===")
    print("Para usar em produção:")
    print("1. Adapte os seletores CSS para sites específicos")
    print("2. Implemente tratamento de JavaScript (Selenium)")
    print("3. Configure proxies/rotação de User-Agents")
    print("4. Adicione cache/banco de dados para persistência")
    print("5. Implemente classificação automática de notícias")
    print("6. Configure alertas para tópicos específicos")
    
    print(f"\n✅ Demonstração concluída com sucesso!")

# === EXECUÇÃO DA DEMONSTRAÇÃO ===
if __name__ == "__main__":
    # Executa apenas se o script for rodado diretamente
    exemplo_uso()
else:
    # Mensagem para quando o módulo é importado
    print("📦 Módulo NoticiasScraper carregado. Execute exemplo_uso() para ver demonstração.")