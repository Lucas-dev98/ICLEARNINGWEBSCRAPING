# 🕷️ ICLearningWebScraping - Projeto de Aprendizado de Web Scraping

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-4.13+-green.svg)
![Requests](https://img.shields.io/badge/Requests-2.32+-orange.svg)
![Status](https://img.shields.io/badge/Status-Ativo-brightgreen.svg)

## 📖 Sobre o Projeto

Este é um projeto educacional completo para aprender **Web Scraping** com Python, utilizando as principais bibliotecas do ecosistema: **requests**, **BeautifulSoup4**, **pandas** e outras ferramentas essenciais.

### 🎯 Objetivos de Aprendizado

- ✅ Fundamentos de requisições HTTP/HTTPS
- ✅ Parsing de HTML com BeautifulSoup
- ✅ Navegação no DOM e seletores CSS
- ✅ Tratamento de erros e boas práticas
- ✅ Scrapers profissionais orientados a objetos
- ✅ Análise de dados com pandas
- ✅ Rate limiting e ética em web scraping

## 🏗️ Estrutura do Projeto

```
ICLearningWebScreating/
├── 📁 src/                          # Código fonte principal
│   ├── 📁 examples/                 # Exemplos básicos de conceitos
│   │   ├── example_01_RequestHTML.py
│   │   ├── example_02_parsing_beatifulSoup.py
│   │   └── example_03_DOMnavigation.py
│   ├── 📁 exercises/                # Exercícios práticos
│   │   ├── exercice_01.py           # Download e manipulação HTML
│   │   ├── exercice_02.py           # Extração e deduplicação
│   │   ├── exercice_03.py           # Manipulação de arquivos
│   │   ├── exercice_04.py           # Padrões regex
│   │   ├── exercice_05.py           # Regex avançado
│   │   └── exercice_06.py           # Seletores CSS
│   └── 📁 scrapers/                 # Scrapers profissionais
│       └── scraper_noticias.py      # Sistema OOP para notícias
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

3. **Estude o scraper profissional:**
   ```bash
   cd ../scrapers
   python scraper_noticias.py  # Sistema completo OOP
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

### 📊 Análise de Dados
- Estruturação com pandas
- Limpeza e validação
- Exportação (CSV, JSON, Excel)
- Visualização básica

### 🏛️ Arquitetura
- Orientação a objetos
- Padrões de design
- Tratamento de exceções
- Logging e debugging

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

## 📄 Licença

Este projeto é para fins educacionais. Use responsavelmente e respeite os termos de uso dos sites que você fizer scraping.

## 🌟 Próximos Passos

- [ ] Adicionar testes automatizados
- [ ] Implementar scraping com Selenium
- [ ] Adicionar exemplos com APIs
- [ ] Criar dashboard de monitoramento
- [ ] Implementar cache de requisições

---

**🎓 Projeto ICLearningWebScraping - Aprendendo Web Scraping com Python**

*Desenvolvido com 💻 para educação em tecnologia*