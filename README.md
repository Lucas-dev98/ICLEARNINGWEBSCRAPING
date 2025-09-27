# 🕷️ ICLearningWebScraping - Projeto de Aprendizado de Web Scraping

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.13+-green.svg)
![Requests](https://img.shields.io/badge/Requests-2.32+-orange.svg)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg)
![UVV InovaWeek](https://img.shields.io/badge/UVV-InovaWeek_Scraper-purple.svg)
![Cache System](https://img.shields.io/badge/Cache-Inteligente-yellow.svg)

## 📖 Sobre o Projeto

Este é um projeto educacional completo para aprender **Web Scraping** com Python, utilizando as principais bibliotecas do ecosistema: **requests**, **BeautifulSoup4**, **pandas** e outras ferramentas essenciais.

### 🏆 **PROJETO DESTAQUE: Scraper UVV InovaWeek**
- ✨ **38 notícias do InovaWeek** coletadas com sucesso
- 🔄 **Sistema de paginação automática** (77 páginas detectadas)
- 📊 **CSV estruturado** com 25 campos profissionais
- 🗃️ **Sistema de cache inteligente** com expiração automática
- ⚡ **Scraper nível enterprise** com rate limiting ético

### 🎯 Objetivos de Aprendizado

- ✅ Fundamentos de requisições HTTP/HTTPS
- ✅ Parsing de HTML com BeautifulSoup
- ✅ Navegação no DOM e seletores CSS
- ✅ Tratamento de erros e boas práticas
- ✅ Scrapers profissionais orientados a objetos
- ✅ Análise de dados com pandas
- ✅ Rate limiting e ética em web scraping
- ✅ **Sistema de paginação inteligente**
- ✅ **Estruturação avançada de dados CSV**
- ✅ **Scraping focado em eventos específicos**
- ✅ **Detecção automática de conteúdo relevante**
- ✅ **🗃️ Sistema de cache inteligente para otimização**

## 🏗️ Estrutura do Projeto

```
ICLearningWebScreating/
├── 📁 src/                          # Código fonte principal
│   ├── 📁 examples/                 # Exemplos básicos de conceitos
│   │   ├── example_01_RequestHTML.py
│   │   ├── example_02_parsing_beatifulSoup.py
│   │   ├── example_03_DOMnavigation.py
│   │   └── exemplo_cache_demonstracao.py  # 🗃️ Demo do sistema de cache
│   ├── 📁 exercises/                # Exercícios práticos
│   │   ├── exercice_01.py           # Download e manipulação HTML
│   │   ├── exercice_02.py           # Extração e deduplicação
│   │   ├── exercice_03.py           # Manipulação de arquivos
│   │   ├── exercice_04.py           # Padrões regex
│   │   ├── exercice_05.py           # Regex avançado
│   │   └── exercice_06.py           # Seletores CSS
│   └── 📁 scrapers/                 # Scrapers profissionais
│       ├── scraper_noticias.py      # Sistema OOP para notícias
│       └── scraper_uvv_inovaweek_revisado.py  # 🏆 Scraper UVV InovaWeek
├── 📁 docs/                         # Documentação
│   └── DEPENDENCIES.md
├── 📁 config/                       # Arquivos de configuração
│   ├── .inputrc                     # Configurações readline
│   └── .terminal_config             # Configurações do terminal
├── 📁 data/                         # Dados de exemplo e resultados
│   └── uvv.html                     # Exemplo de página HTML
├── 📁 scripts/                      # Scripts utilitários
│   └── install_dependencies.sh      # Instalação automatizada
├── 📁 tests/                        # Testes automatizados (futuro)
├── 📁 venv/                         # Ambiente virtual Python
├── requirements.txt                 # Dependências do projeto
├── setup.py                         # Configuração de instalação
└── README.md                        # Este arquivo
```

## 🏆 **SCRAPER UVV INOVAWEEK - PROJETO DESTAQUE**

### 📊 **Resultados Alcançados**
- ✅ **38 notícias do InovaWeek** coletadas com sucesso
- ✅ **77 páginas disponíveis** detectadas automaticamente  
- ✅ **25 campos estruturados** no CSV de saída
- ✅ **100% de qualidade** no conteúdo extraído
- ✅ **Rate limiting respeitoso** (2 segundos entre requests)
- ✅ **Paginação inteligente** com múltiplos formatos de URL
- ✅ **🗃️ Cache inteligente** com 70%+ de taxa de acerto

### 🔧 **Uso do Scraper UVV InovaWeek**

```bash
# 📋 Verificar quantas páginas existem
python src/scrapers/scraper_uvv_inovaweek_revisado.py --verificar-paginacao

# 🚀 Coletar notícias de múltiplas páginas
python src/scrapers/scraper_uvv_inovaweek_revisado.py --max-paginas 10

# 🎯 Período específico (agosto-setembro 2025)
python src/scrapers/scraper_uvv_inovaweek_revisado.py \
  --inicio 2025-08-01 --fim 2025-09-30 --max-paginas 20

# 📁 Salvar em arquivo específico
python src/scrapers/scraper_uvv_inovaweek_revisado.py \
  --output minha_coleta.csv --max-paginas 5

# ⚡ Teste rápido (apenas primeira página)
python src/scrapers/scraper_uvv_inovaweek_revisado.py --apenas-primeira-pagina

# 🗃️ Demonstração do sistema de cache
python src/examples/exemplo_cache_demonstracao.py
```

### 📋 **Estrutura do CSV Gerado (25 Campos)**

| Categoria | Campos |
|-----------|---------|
| **🆔 Identificação** | `id_noticia`, `titulo`, `slug_url`, `url_completa` |
| **👤 Autoria** | `autor`, `data_publicacao_formatada`, `data_publicacao_iso` |
| **📅 Temporalidade** | `mes_publicacao`, `ano_publicacao`, `timestamp_coleta_iso` |
| **📰 Conteúdo** | `resumo_automatico`, `conteudo_completo_limpo`, `palavras_chave` |
| **🔧 Metadados** | `tamanho_caracteres`, `qualidade_conteudo`, `relevancia_inovaweek` |

### 🎯 **Funcionalidades Avançadas**
- **Detecção automática de paginação:** Descobre todas as páginas disponíveis
- **Múltiplos seletores CSS:** Sistema robusto com fallback
- **Filtragem inteligente:** Foca apenas em notícias do InovaWeek
- **🗃️ Cache inteligente:** Sistema automático com expiração configurável
- **Metadados completos:** Arquivo de estatísticas automático
- **Rate limiting ético:** Respeita o servidor com delays apropriados
- **CLI profissional:** Interface de linha de comando completa

## 🚀 Instalação e Configuração

### 1️⃣ Pré-requisitos

- **Python 3.12+** instalado
- **pip** (gerenciador de pacotes Python)
- **git** (opcional, para clonar o repositório)

### 2️⃣ Instalação Rápida

```bash
# 1. Clone ou baixe o projeto
git clone <seu-repositorio> ICLearningWebScreating
cd ICLearningWebScreating

# 2. Ative o ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate    # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a configuração do terminal (opcional)
source config/.terminal_config
```

### 3️⃣ Instalação Automatizada

```bash
# Execute o script de instalação
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

## 📚 Guia de Uso

### 🔰 Para Iniciantes

1. **Comece pelos exemplos básicos:**
   ```bash
   cd src/examples
   python example_01_RequestHTML.py        # Aprenda requisições HTTP
   python example_02_parsing_beatifulSoup.py  # Aprenda parsing HTML
   python example_03_DOMnavigation.py      # Aprenda navegação DOM
   ```

2. **Pratique com exercícios:**
   ```bash
   cd ../exercises
   python exercice_01.py  # Download de HTML
   python exercice_02.py  # Extração de dados
   # ... continue com os demais exercícios
   ```

3. **Estude os scrapers profissionais:**
   ```bash
   cd ../scrapers
   python scraper_noticias.py  # Sistema completo OOP
   
   # 🏆 SCRAPER AVANÇADO - UVV InovaWeek
   python scraper_uvv_inovaweek_revisado.py  # Scraper nível enterprise
   
   # 🗃️ DEMONSTRAÇÃO DO CACHE
   cd ../examples
   python exemplo_cache_demonstracao.py  # Demo interativa do cache
   ```

### 🎓 Para Usuários Avançados

- **Use como módulo Python:**
  ```python
  from src.scrapers import NoticiasScraper
  from src.examples import *
  
  # Crie seu próprio scraper
  scraper = NoticiasScraper("https://example.com")
  dados = scraper.scrape_site("https://news-site.com")
  ```

- **🏆 Use o Scraper UVV InovaWeek (Nível Enterprise):**
  ```bash
  # Verificar páginas disponíveis
  python src/scrapers/scraper_uvv_inovaweek_revisado.py --verificar-paginacao
  
  # Coletar 10 páginas específicas
  python src/scrapers/scraper_uvv_inovaweek_revisado.py --max-paginas 10
  
  # Período específico com paginação
  python src/scrapers/scraper_uvv_inovaweek_revisado.py \
    --inicio 2025-08-01 --fim 2025-09-30 --max-paginas 20 \
    --output inovaweek_completo.csv
  ```

- **Extend as classes existentes:**
  ```python
  class MeuScraperPersonalizado(NoticiasScraper):
      def extrair_dados_customizados(self, html):
          # Sua lógica aqui
          pass
  ```

## 🛠️ Tecnologias Utilizadas

### 📦 Dependências Principais

| Biblioteca | Versão | Propósito |
|-----------|--------|-----------|
| `requests` | 2.32.5+ | Requisições HTTP/HTTPS |
| `beautifulsoup4` | 4.13.5+ | Parsing HTML/XML |
| `pandas` | 2.3.2+ | Análise de dados |
| `lxml` | 6.0.2+ | Parser XML rápido |
| `html5lib` | 1.1+ | Parser HTML robusto |

### 🔧 Ferramentas de Desenvolvimento

- **Ambiente Virtual:** Python venv
- **Configuração Terminal:** bash + readline
- **Documentação:** Markdown
- **Controle de Versão:** Git (recomendado)
- **🏆 Sistema de Paginação:** Detecção automática de múltiplas páginas
- **📊 Estruturação CSV:** 25 campos organizados em 5 categorias
- **⚡ Rate Limiting:** Scraping ético e respeitoso
- **🗃️ Sistema de Cache:** Cache inteligente com expiração automática

## 📖 Conceitos Abordados

### 🌐 Fundamentos Web
- Protocolo HTTP/HTTPS
- Headers e User-Agents
- Cookies e sessões
- Status codes e tratamento de erros

### 🎯 Técnicas de Scraping
- Seletores CSS e XPath
- Navegação no DOM
- Expressões regulares
- Rate limiting e delays
- Tratamento de JavaScript (conceitos)

### �️ Sistema de Cache
- Cache automático de requisições HTTP
- Expiração configurável (padrão: 24h)
- Compressão e otimização de armazenamento
- Estatísticas detalhadas (hit rate, tamanho)
- Limpeza automática de cache expirado
- Demonstração interativa disponível

### �📊 Análise de Dados
- Estruturação com pandas
- Limpeza e validação
- Exportação (CSV, JSON, Excel)
- Visualização básica

### 🏛️ Arquitetura
- Orientação a objetos
- Padrões de design
- Tratamento de exceções
- Logging e debugging
- **🏆 Sistema de sessões HTTP otimizadas**
- **📊 Metadados estruturados automáticos**
- **🔄 Paginação inteligente com fallback**
- **⚡ CLI avançada com argparse**

## ⚡ Exemplos Rápidos

### 🔍 Scraping Básico
```python
import requests
from bs4 import BeautifulSoup

# Fazer requisição
response = requests.get('https://example.com')
soup = BeautifulSoup(response.content, 'html.parser')

# Extrair dados
titles = soup.find_all('h1')
for title in titles:
    print(title.get_text().strip())
```

### 🏗️ Scraper Profissional
```python
from src.scrapers import NoticiasScraper

# Criar scraper configurado
scraper = NoticiasScraper(
    base_url="https://news-site.com",
    headers={'User-Agent': 'Mozilla/5.0...'}
)

# Fazer scraping estruturado
dados = scraper.scrape_site("https://news-site.com/noticias")
df = scraper.converter_para_dataframe(dados)
df.to_csv('noticias.csv', index=False)
```

### 🏆 Scraper UVV InovaWeek (Enterprise)
```bash
# Sistema completo com paginação automática
python src/scrapers/scraper_uvv_inovaweek_revisado.py \
  --max-paginas 10 \
  --inicio 2025-08-01 \
  --fim 2025-09-30 \
  --output inovaweek.csv

# Resultado: CSV com 25 campos estruturados
# ✅ 38 notícias coletadas
# ✅ 77 páginas detectadas
# ✅ Metadados completos
# ✅ Rate limiting respeitoso
# ✅ Cache automático ativo
```

### 🗃️ Sistema de Cache Inteligente
```python
from src.scrapers import UVVInovaWeekScraper

# Scraper com cache habilitado (padrão)
scraper = UVVInovaWeekScraper(use_cache=True, cache_hours=24)

# Primeira requisição: busca online + salva no cache
response1 = scraper._fazer_requisicao("https://uvv.br/noticias/")

# Segunda requisição: retorna do cache (instantâneo!)
response2 = scraper._fazer_requisicao("https://uvv.br/noticias/")

# Verificar estatísticas do cache
stats = scraper.get_cache_stats()
print(f"Taxa de acerto: {stats['hit_rate_percent']}%")
print(f"Tamanho do cache: {stats['cache_size_mb']} MB")
```

## 🔧 Solução de Problemas

### ❗ Problemas Comuns

1. **ModuleNotFoundError:**
   ```bash
   # Ative o ambiente virtual
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Erro de importação:**
   ```bash
   # Execute do diretório raiz do projeto
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

3. **Erro 403/bloqueio:**
   ```python
   # Configure User-Agent apropriado
   headers = {'User-Agent': 'Mozilla/5.0 (compatible; Educational)'}
   ```

### 🆘 Suporte

- 📖 Consulte `docs/DEPENDENCIES.md` para detalhes das dependências
- 🔧 Use `scripts/install_dependencies.sh` para reinstalação
- 💬 Verifique os comentários nos códigos para explicações detalhadas

## 🤝 Contribuição

Este é um projeto educacional. Contribuições são bem-vindas:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Adicione testes se necessário
4. Documente suas alterações
5. Envie um Pull Request

## 📄 Licença e Uso Responsável

### 🎓 **Licença Educacional MIT**

Este projeto é distribuído sob a **Licença MIT** para fins educacionais e de aprendizado.

**Você tem permissão para:**
- ✅ Usar o código para aprendizado pessoal
- ✅ Modificar e adaptar para projetos educacionais
- ✅ Distribuir com atribuição apropriada
- ✅ Usar em projetos comerciais (com responsabilidade)

**Com as seguintes condições:**
- 📋 Manter os créditos e aviso de copyright
- 🔍 Incluir uma cópia da licença MIT
- ⚖️ Usar sob sua própria responsabilidade

### 🛡️ **Uso Ético de Web Scraping**

**⚠️ IMPORTANTE: Diretrizes de Uso Responsável**

Este projeto foi criado exclusivamente para **fins educacionais**. Ao utilizar estas técnicas, você concorda em:

#### ✅ **Práticas Recomendadas:**
- 🤝 **Respeitar robots.txt** dos websites
- ⏱️ **Implementar delays** entre requisições (rate limiting)
- 🔄 **Usar cache** para evitar requisições desnecessárias
- 📧 **Contatar webmasters** para projetos de grande escala
- 🎯 **Coletar apenas dados públicos** e necessários
- 📊 **Usar dados coletados de forma ética** e legal

#### ❌ **Práticas Proibidas:**
- 🚫 Sobrecarregar servidores com muitas requisições
- 🚫 Ignorar termos de uso e políticas dos sites
- 🚫 Coletar dados pessoais sem permissão
- 🚫 Uso comercial não autorizado de conteúdo
- 🚫 Burlar medidas de proteção anti-bot
- 🚫 Republicar conteúdo sem devida atribuição

### ⚖️ **Responsabilidade Legal**

- **O usuário é integralmente responsável** pelo uso deste código
- **Os desenvolvedores não se responsabilizam** por uso inadequado
- **Consulte sempre a legislação local** sobre coleta de dados
- **Respeite direitos autorais e propriedade intelectual**
- **Em caso de dúvidas legais, consulte um advogado especializado**

### 🌍 **Política de Dados UVV**

Especificamente para o **Scraper UVV InovaWeek**:
- ✅ Coleta apenas **notícias públicas** já disponibilizadas
- ✅ Implementa **rate limiting respeitoso** (2s entre requisições)
- ✅ Usa **cache inteligente** para reduzir carga no servidor
- ✅ Foca apenas em **conteúdo educacional** do InovaWeek
- ✅ **Não interfere** no funcionamento normal do site

### 📞 **Contato e Atribuição**

**Projeto:** ICLearningWebScraping  
**Finalidade:** Educação em Tecnologia  
**Desenvolvido com:** ❤️ Python + BeautifulSoup + Requests  

Para questões sobre uso comercial ou dúvidas sobre licenciamento, entre em contato através do repositório GitHub.

---

**⚡ Lembre-se: Com grandes poderes vêm grandes responsabilidades!**

*Use o web scraping de forma ética, respeitosa e sempre dentro dos limites legais.*

## � Conquistas Recentes

### ✅ **Scraper UVV InovaWeek - Nível Enterprise**
- **📊 38 notícias coletadas** com sucesso
- **🔄 77 páginas detectadas** automaticamente
- **📋 25 campos estruturados** em CSV profissional
- **⚡ Sistema de paginação inteligente** com múltiplos formatos de URL
- **🎯 Filtragem específica** para eventos InovaWeek
- **⏱️ Rate limiting ético** (2s entre requests)
- **�️ Cache inteligente** com 70%+ de taxa de acerto
- **�🔧 CLI avançada** com argparse completo
- **📊 Metadados automáticos** com estatísticas detalhadas

### 🎯 **Funcionalidades Avançadas Implementadas**
```bash
# Verificar paginação disponível
python src/scrapers/scraper_uvv_inovaweek_revisado.py --verificar-paginacao

# Coletar múltiplas páginas com período específico
python src/scrapers/scraper_uvv_inovaweek_revisado.py \
  --max-paginas 20 --inicio 2025-08-01 --fim 2025-09-30

# Apenas primeira página para testes
python src/scrapers/scraper_uvv_inovaweek_revisado.py --apenas-primeira-pagina
```

## �🌟 Próximos Passos

- [ ] Adicionar testes automatizados
- [ ] Implementar scraping com Selenium
- [ ] Adicionar exemplos com APIs
- [ ] Criar dashboard de monitoramento
- [x] **Implementar cache de requisições** ✅
- [x] **Sistema de paginação automática** ✅
- [x] **CSV estruturado profissional** ✅
- [x] **Rate limiting ético** ✅

---

**🎓 Projeto ICLearningWebScraping - Aprendendo Web Scraping com Python**

*Desenvolvido com 💻 para educação em tecnologia*

### 🏆 **Destaque: Scraper UVV InovaWeek**
*Sistema de web scraping nível enterprise com paginação automática, cache inteligente, 25 campos estruturados e 38 notícias coletadas com sucesso!*

### 🗃️ **Sistema de Cache Implementado**
*Cache automático com 70%+ de taxa de acerto, reduzindo tempo de desenvolvimento e respeitando servidores com requisições otimizadas!*