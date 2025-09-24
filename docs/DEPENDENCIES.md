# 🕷️ WEB SCRAPING COM PYTHON - GUIA COMPLETO

## 📋 RESUMO DAS DEPENDÊNCIAS

Este projeto requer as seguintes bibliotecas Python para funcionar corretamente:

### 🚨 DEPENDÊNCIAS OBRIGATÓRIAS

```bash
# Instalação rápida de todas as dependências:
pip install requests beautifulsoup4 pandas lxml html5lib
```

#### Detalhamento das bibliotecas:

| Biblioteca | Versão Mínima | Usado Em | Funcionalidade |
|------------|---------------|----------|----------------|
| **requests** | 2.31.0+ | `example_01_RequestHTML.py`<br>`exercice_01.py`<br>`scraper_noticias.py` | Requisições HTTP/HTTPS, download de páginas |
| **beautifulsoup4** | 4.12.0+ | Todos os exercícios BeautifulSoup | Parsing HTML/XML, navegação DOM |
| **pandas** | 2.0.0+ | `scraper_noticias.py` | Análise de dados, DataFrames |
| **lxml** | 4.9.0+ | Opcional (melhora performance) | Parser HTML rápido |
| **html5lib** | 1.1+ | Opcional (HTML malformado) | Parser robusto |

### ✅ BIBLIOTECAS PADRÃO (já incluídas no Python)

Estas bibliotecas **NÃO precisam ser instaladas** pois já vêm com Python:

- `socket` - Operações de rede (DNS)
- `urllib.parse` - Parsing de URLs
- `os` - Operações do sistema operacional
- `re` - Expressões regulares
- `csv` - Manipulação de arquivos CSV
- `time` - Controle de tempo e delays
- `datetime` - Manipulação de datas
- `collections` - Estruturas de dados (Counter, etc.)

## 🛠️ MÉTODOS DE INSTALAÇÃO

### Método 1: Script Automático (Recomendado)
```bash
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Método 2: Requirements.txt
```bash
pip install -r requirements.txt
```

### Método 3: Instalação Manual
```bash
# Dependências principais
pip install requests>=2.31.0
pip install beautifulsoup4>=4.12.0
pip install pandas>=2.0.0

# Parsers opcionais (recomendados)
pip install lxml>=4.9.0
pip install html5lib>=1.1
```

### Método 4: Conda (se preferir)
```bash
conda install requests beautifulsoup4 pandas lxml html5lib
```

## 🗂️ ARQUIVOS DO PROJETO E SUAS DEPENDÊNCIAS

### 📁 Exemplos Básicos
- **`example_01_RequestHTML.py`**
  - Dependências: `requests`, `socket`, `urllib.parse`
  - Função: Demonstra requisições HTTP básicas

- **`example_02_parsing_beatifulSoup.py`** 
  - Dependências: `beautifulsoup4`
  - Função: Parsing HTML com BeautifulSoup

- **`example_03_DOMnavigation.py`**
  - Dependências: `beautifulsoup4`
  - Função: Navegação na árvore DOM

### 📁 Exercícios Práticos
- **`exercice_01.py`** - `requests`, `os`
- **`exercice_02.py`** - `beautifulsoup4`
- **`exercice_03.py`** - `beautifulsoup4`
- **`exercice_04.py`** - `beautifulsoup4`, `re`
- **`exercice_05.py`** - `beautifulsoup4`, `re` (duplicata do 04)
- **`exercice_06.py`** - `beautifulsoup4`

### 📁 Sistema Completo
- **`scraper_noticias.py`**
  - Dependências: `requests`, `beautifulsoup4`, `pandas`, `csv`, `time`, `datetime`
  - Função: Sistema profissional de scraping de notícias

## 🧪 TESTE DE INSTALAÇÃO

Execute este comando para verificar se tudo está instalado corretamente:

```python
python3 -c "
import requests, bs4, pandas, lxml, html5lib
print('✅ Todas as dependências instaladas com sucesso!')
print(f'requests: {requests.__version__}')
print(f'beautifulsoup4: {bs4.__version__}')
print(f'pandas: {pandas.__version__}')
print(f'lxml: {lxml.__version__}')
print(f'html5lib: {html5lib.__version__}')
"
```

## ⚙️ REQUISITOS DO SISTEMA

- **Python**: 3.8 ou superior
- **Sistema Operacional**: Linux, macOS, Windows
- **Memória**: Mínimo 512MB RAM
- **Espaço em Disco**: ~100MB para todas as dependências

## 🔧 SOLUÇÃO DE PROBLEMAS

### Erro: "ModuleNotFoundError: No module named 'requests'"
```bash
pip install requests
```

### Erro: "ModuleNotFoundError: No module named 'bs4'"
```bash
pip install beautifulsoup4
```

### Erro: "Permission denied" no Linux/macOS
```bash
sudo pip3 install requests beautifulsoup4 pandas
# OU use virtual environment (recomendado):
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pandas
```

### Erro: "lxml not found" 
```bash
# Ubuntu/Debian:
sudo apt-get install libxml2-dev libxslt-dev
pip install lxml

# CentOS/RHEL:
sudo yum install libxml2-devel libxslt-devel
pip install lxml

# macOS:
brew install libxml2 libxslt
pip install lxml
```

### Performance lenta do BeautifulSoup
```bash
# Instale parsers mais rápidos:
pip install lxml html5lib

# Use no código:
soup = BeautifulSoup(html, "lxml")  # Mais rápido
# ou
soup = BeautifulSoup(html, "html5lib")  # Mais robusto
```

## 🌐 DEPENDÊNCIAS OPCIONAIS PARA PROJETOS AVANÇADOS

Para casos de uso mais complexos, considere instalar:

```bash
# Selenium para JavaScript
pip install selenium

# Requisições assíncronas
pip install aiohttp

# Logs estruturados
pip install loguru

# Configuração com variáveis de ambiente
pip install python-dotenv

# Testes automatizados
pip install pytest pytest-cov

# Formatação de código
pip install black isort flake8
```

## 📚 RECURSOS ADICIONAIS

- [Documentação do Requests](https://docs.python-requests.org/)
- [Documentação do BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Documentação do Pandas](https://pandas.pydata.org/docs/)
- [Ética em Web Scraping](https://blog.apify.com/web-scraping-ethics/)

## 🎯 EXECUÇÃO DOS EXEMPLOS

Após instalar as dependências:

```bash
# Exemplos básicos
python3 example_01_RequestHTML.py
python3 example_02_parsing_beatifulSoup.py

# Exercícios práticos  
python3 exercice_01.py
python3 exercice_06.py

# Sistema completo
python3 scraper_noticias.py
```

## 🐛 SUPORTE

Se encontrar problemas de instalação:

1. Verifique sua versão do Python: `python3 --version`
2. Atualize pip: `pip3 install --upgrade pip`  
3. Use ambientes virtuais: `python3 -m venv venv`
4. Consulte os logs de erro específicos
5. Abra uma issue no repositório

---

**✨ Projeto documentado e pronto para uso educacional e profissional! 🚀**