"""
Exemplo 02: Parsing de HTML com BeautifulSoup

Este script demonstra os fundamentos do parsing (análise) de documentos HTML 
usando a biblioteca BeautifulSoup, incluindo navegação básica no DOM,
acesso a elementos e extração de dados.

Conceitos abordados:
- Parsing de HTML com BeautifulSoup
- Navegação básica no DOM (Document Object Model)
- Acesso direto a tags e suas propriedades
- Extração de texto, atributos e estrutura de elementos

Bibliotecas utilizadas:
- bs4 (BeautifulSoup): Parser HTML/XML que cria uma árvore navegável
"""

# Importação da biblioteca BeautifulSoup para parsing HTML
from bs4 import BeautifulSoup

# === DOCUMENTO HTML DE EXEMPLO ===
# String contendo HTML simples para demonstração
small_example_html = """<html><body>
<p>Clique <a id='info' href='https://www.uvv.br'>aqui</a>
para mais informacoes.</p></body></html>
"""
# Estrutura DOM deste HTML:
# html (raiz)
#  └── body
#       └── p (parágrafo)
#           ├── texto: "Clique "
#           ├── a (link com id='info' e href='https://www.uvv.br')
#           │    └── texto: "aqui"
#           └── texto: " para mais informacoes."

# === CRIAÇÃO DO OBJETO BEAUTIFULSOUP ===
# Cria um objeto BeautifulSoup que parseia o HTML
small_soup = BeautifulSoup(small_example_html, "html.parser")
# Parâmetros:
# - small_example_html: string HTML para analisar
# - "html.parser": parser interno do Python (outras opções: lxml, html5lib)

# Exibe o HTML formatado de forma legível (indentado)
print(small_soup.prettify())
# prettify() adiciona quebras de linha e indentação para melhor visualização

# === NAVEGAÇÃO DIRETA POR TAGS ===
# Acessa diretamente a primeira tag <p> encontrada no documento
print(small_soup.p, "\n")
# small_soup.p é equivalente a small_soup.find('p')
# Retorna o elemento <p> completo com todo seu conteúdo interno

# === NAVEGAÇÃO ANINHADA ===
# Acessa a subtag <a> que está dentro da tag <p>
a_tag = small_soup.p.a
# Navegação hierárquica: vai para <p>, depois para <a> dentro de <p>
print(a_tag, type(a_tag), sep='\n')
# Exibe o elemento <a> e seu tipo (bs4.element.Tag)

# === EXTRAÇÃO DE PROPRIEDADES DO ELEMENTO ===
# Extrai informações específicas da tag <a>
print(a_tag.name, a_tag.attrs, a_tag.string, sep='\n')
# a_tag.name: nome da tag ('a')
# a_tag.attrs: dicionário com todos os atributos ({'id': 'info', 'href': 'https://www.uvv.br'})
# a_tag.string: texto interno da tag ('aqui')

# Outros atributos úteis disponíveis:
# - a_tag.text: todo o texto da tag e sub-tags (sem HTML)
# - a_tag['href']: acesso direto a um atributo específico
# - a_tag.get('href'): método seguro para obter atributo (retorna None se não existir)
# - a_tag.parent: elemento pai desta tag
# - a_tag.children: iterador dos elementos filhos