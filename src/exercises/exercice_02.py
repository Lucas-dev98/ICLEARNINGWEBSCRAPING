"""
Exercício 02: Extração e Análise de Tags HTML

Este script demonstra como extrair e analisar todas as tags presentes em um documento HTML,
utilizando técnicas de busca abrangente, manipulação de conjuntos (sets) e ordenação de dados.

Funcionalidades implementadas:
- Busca exaustiva de todos os elementos HTML
- Extração de nomes de tags sem duplicação
- Ordenação alfabética para melhor apresentação
- Análise estrutural de documentos HTML complexos

Conceitos de programação abordados:
- List comprehensions para transformação de dados
- Sets (conjuntos) para eliminação de duplicatas
- Métodos find_all() do BeautifulSoup
- Ordenação de listas com sorted()
- Iteração sobre elementos HTML
"""

# Importação da biblioteca BeautifulSoup para parsing HTML
from bs4 import BeautifulSoup

def listar_todas_tags(html_string):
    """
    Retorna uma lista com os nomes de todas as tags presentes no HTML
    
    Esta função implementa um processo completo de análise estrutural:
    1. Parsing do HTML em árvore DOM
    2. Busca exaustiva de todos os elementos
    3. Extração de nomes das tags
    4. Eliminação de duplicatas
    5. Ordenação alfabética dos resultados
    
    Args:
        html_string (str): String contendo código HTML válido ou malformado
    
    Returns:
        list: Lista ordenada com nomes únicos das tags encontradas
        
    Example:
        >>> html = "<div><p>Texto</p><span>Mais texto</span></div>"
        >>> listar_todas_tags(html)
        ['div', 'p', 'span']
    """
    # === PARSING DO DOCUMENTO HTML ===
    soup = BeautifulSoup(html_string, "html.parser")
    # O parser automaticamente:
    # - Corrige HTML malformado
    # - Cria estrutura de árvore navegável
    # - Ignora elementos inválidos
    # - Normaliza a estrutura do documento
    
    # === BUSCA EXAUSTIVA DE ELEMENTOS ===
    # Encontra TODOS os elementos HTML no documento
    all_tags = soup.find_all()
    # find_all() sem parâmetros retorna:
    # - Todos os elementos HTML (tags)
    # - Em ordem de aparição no documento
    # - Incluindo elementos aninhados
    # - Excluindo text nodes (apenas elementos)
    
    # Métodos alternativos equivalentes:
    # soup.find_all(True)  # True significa "qualquer tag"
    # soup.descendants    # Inclui text nodes também
    # soup.select('*')    # Seletor CSS para todos elementos
    
    # === EXTRAÇÃO E PROCESSAMENTO DE NOMES ===
    # Extrai os nomes das tags e remove duplicatas usando set
    tag_names = list(set([tag.name for tag in all_tags]))
    # Processo detalhado:
    # 1. [tag.name for tag in all_tags] -> List comprehension
    #    Cria lista com nomes: ['html', 'head', 'title', 'body', 'p', 'b', 'p', 'a', 'a', 'a', 'p', 'p']
    # 2. set([...]) -> Converte para conjunto, eliminando duplicatas
    #    Resultado: {'html', 'head', 'title', 'body', 'p', 'b', 'a'}
    # 3. list(...) -> Converte de volta para lista
    #    Necessário porque sets não são ordenados nem indexáveis
    
    # === ORDENAÇÃO DOS RESULTADOS ===
    return sorted(tag_names)  # Retorna ordenado alfabeticamente
    # sorted() cria nova lista ordenada sem modificar a original
    # Alternativa: tag_names.sort() (modifica lista original)

# === DADOS DE TESTE ===
# HTML de exemplo baseado no exercício da aula
test_html = """
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

# Estrutura esperada deste HTML:
# - html: elemento raiz
# - head: cabeçalho do documento
# - title: título da página
# - body: corpo do documento  
# - p: parágrafos (múltiplas ocorrências)
# - b: texto em negrito
# - a: links/âncoras (múltiplas ocorrências)

# === EXECUÇÃO E TESTE ===
tags_encontradas = listar_todas_tags(test_html)
print("Tags encontradas:", tags_encontradas)
print(f"Total de tipos de tags diferentes: {len(tags_encontradas)}")

# Análise adicional possível:
# print("Contagem detalhada:")
# soup = BeautifulSoup(test_html, "html.parser")
# from collections import Counter
# tag_counts = Counter(tag.name for tag in soup.find_all())
# for tag, count in sorted(tag_counts.items()):
#     print(f"  {tag}: {count} ocorrência(s)")