"""
Exemplo 03: Navegação no DOM com BeautifulSoup

Este script demonstra técnicas avançadas de navegação na árvore DOM (Document Object Model),
incluindo navegação hierárquica (pais/filhos) e navegação horizontal (elementos irmãos).

Conceitos fundamentais abordados:
- Estrutura hierárquica do DOM (árvore de elementos)
- Navegação vertical: parent (pai) e children (filhos)
- Navegação horizontal: siblings (elementos irmãos)
- Diferença entre elements e text nodes (nós de texto)
- Métodos de navegação do BeautifulSoup

DOM Structure (Document Object Model):
O DOM representa um documento HTML como uma árvore hierárquica onde:
- Cada tag é um "element node" (nó elemento)
- Texto entre tags são "text nodes" (nós de texto)
- Espaços em branco e quebras de linha também são text nodes
"""

# Importação da biblioteca BeautifulSoup
from bs4 import BeautifulSoup

# === DOCUMENTO HTML COMPLEXO PARA DEMONSTRAÇÃO ===
pig_html = """
<html><head><title>Os Tres Porquinhos</title></head>
<body>
<p class="title"><b>Os Tres Porquinhos</b></p>
<p class="story">Era uma vez tres porquinhos chamados
<a href="http://example.com/larry" class="pig" id="link1">Larry,</a>
<a href="http://example.com/mo" class="pig" id="link2">Mo</a> e
<a href="http://example.com/curly" class="pig" id="link3">Curly.</a>
<p>Os tres porquinhos tinham um fascinio peculiar por construcoes experimentais.</p>
<p>...</p>
</body></html>
"""

# Estrutura DOM visualizada:
# html
# ├── head
# │   └── title: "Os Tres Porquinhos"
# └── body
#     ├── p.title
#     │   └── b: "Os Tres Porquinhos"
#     ├── p.story
#     │   ├── texto: "Era uma vez tres porquinhos chamados\n"
#     │   ├── a#link1: "Larry,"
#     │   ├── texto: "\n"
#     │   ├── a#link2: "Mo"
#     │   ├── texto: " e\n"
#     │   └── a#link3: "Curly."
#     ├── p: "Os tres porquinhos tinham..."
#     └── p: "..."

# === CRIAÇÃO DO OBJETO BEAUTIFULSOUP ===
pig_soup = BeautifulSoup(pig_html, "html.parser")

# === ACESSO DIRETO A ELEMENTOS ===
# Acessa a PRIMEIRA tag <p> encontrada (class="title")
print(pig_soup.p)
# Nota: pig_soup.p sempre retorna a PRIMEIRA ocorrência da tag <p>

# Acessa a PRIMEIRA tag <a> encontrada (id="link1")
print(pig_soup.a)
# Mesmo princípio: sempre o primeiro elemento encontrado

# === NAVEGAÇÃO PELA ÁRVORE DOM ===
# Obtém referência para a primeira tag <a> para navegação
a_tag = pig_soup.a  # Este é o link "Larry"
print(a_tag)

# === NAVEGAÇÃO HIERÁRQUICA: ELEMENTOS PAIS ===
# Cria lista com nomes de todas as tags "pais" até a raiz
print([par.name for par in a_tag.parents])
# a_tag.parents é um gerador que percorre a hierarquia:
# 1. p (parágrafo pai direto)
# 2. body (corpo do documento)
# 3. html (elemento raiz)
# 4. [document] (documento completo)

# Explicação da hierarquia:
# <a> está dentro de <p class="story">
# <p> está dentro de <body>
# <body> está dentro de <html>
# <html> está dentro do [document] (raiz absoluta)

# === NAVEGAÇÃO HORIZONTAL: ELEMENTOS IRMÃOS ===
# Acessa o próximo "irmão" (sibling) na mesma hierarquia
print(a_tag.next_sibling)
# IMPORTANTE: retorna um TEXT NODE (quebra de linha "\n")
# Isso acontece porque existe texto/espaço entre as tags <a>

# Acessa o irmão seguinte ao text node (segunda tag <a>)
print(a_tag.next_sibling.next_sibling)
# Primeiro next_sibling: texto "\n"
# Segundo next_sibling: <a id="link2">Mo</a>

# MÉTODOS DE NAVEGAÇÃO DISPONÍVEIS:
# Navegação Horizontal (Siblings):
# - next_sibling: próximo elemento irmão (inclui text nodes)
# - previous_sibling: elemento irmão anterior
# - next_siblings: gerador de todos os irmãos seguintes
# - previous_siblings: gerador de todos os irmãos anteriores

# Navegação Vertical (Hierarquia):
# - parent: elemento pai direto
# - parents: gerador de todos os ancestrais
# - children: gerador dos filhos diretos
# - descendants: gerador de todos os descendentes

# Navegação apenas por elementos (ignora text nodes):
# - next_element: próximo elemento (qualquer nível)
# - previous_element: elemento anterior
# - next_elements: gerador de próximos elementos
# - previous_elements: gerador de elementos anteriores