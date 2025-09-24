"""
Exercício 06: Seletores CSS Avançados com BeautifulSoup

Este script demonstra o uso de seletores CSS para busca sofisticada em documentos HTML,
proporcionando uma sintaxe familiar para desenvolvedores web e maior expressividade
nas consultas ao DOM.

Funcionalidades implementadas:
- Seletores de atributos com padrões (iniciando/terminando)
- Combinação de múltiplos critérios (tag + classe + atributo)
- Seletores de relacionamento (filhos diretos)
- Comparação entre diferentes abordagens de busca
- Análise de performance e legibilidade

Conceitos de CSS Selectors abordados:
- Seletores de atributo: [attr^="valor"], [attr$="valor"]
- Seletores de classe: .classe
- Seletores combinados: tag.classe[attr="valor"]
- Seletores de filho direto: parent > child
- Pseudoseletores e wildcards: *

Vantagens dos seletores CSS:
- Sintaxe familiar para desenvolvedores web
- Expressividade maior que métodos find()
- Combinação complexa de critérios em uma linha
- Suporte nativo no BeautifulSoup
"""

# Importação da biblioteca BeautifulSoup
from bs4 import BeautifulSoup

def usar_seletores_css(html_string):
    """
    Demonstra o uso de seletores CSS avançados com BeautifulSoup
    
    Esta função ilustra três padrões comuns de seleção CSS:
    1. Seletores de atributo com wildcards (prefixo/sufixo)
    2. Combinação de múltiplos critérios (tag + classe + atributo)
    3. Seletores de relacionamento hierárquico (filho direto)
    
    Args:
        html_string (str): String HTML para análise com seletores CSS
    
    Returns:
        dict: Resultados organizados das três consultas CSS:
            - 'ids_link': Elementos com ID iniciando por "link"
            - 'a_pig_mo': Links classe "pig" com href terminando "mo"
            - 'filhos_story': Filhos diretos de parágrafos classe "story"
    """
    # === PARSING DO DOCUMENTO HTML ===
    soup = BeautifulSoup(html_string, "html.parser")
    
    # === ESTRUTURA DE RESULTADOS ===
    resultados = {}
    
    # === CASO (A): SELETOR DE ATRIBUTO COM PREFIXO ===
    # Busca tags com ID que inicie por "link"
    resultados['ids_link'] = soup.select("[id^='link']")
    
    # Explicação do seletor "[id^='link']":
    # [attr^=value] -> seletor CSS para "atributo inicia com valor"
    # id            -> nome do atributo HTML
    # ^             -> operador "inicia com" (prefix match)
    # 'link'        -> valor do prefixo a buscar
    
    # Seletores de atributo similares:
    # [id$='suffix']    -> termina com "suffix"
    # [id*='contains']  -> contém "contains"
    # [id~='word']      -> contém palavra completa "word"
    # [id|='lang']      -> inicia com "lang" ou "lang-"
    # [id]              -> possui o atributo (qualquer valor)
    
    # === CASO (B): SELETOR COMBINADO COMPLEXO ===
    # Busca tags <a> com classe "pig" E href terminando com "mo"
    resultados['a_pig_mo'] = soup.select("a.pig[href$='mo']")
    
    # Explicação do seletor "a.pig[href$='mo']":
    # a             -> tag <a> (elemento âncora/link)
    # .pig          -> classe CSS "pig" (note o ponto antes do nome)
    # [href$='mo']  -> atributo href terminando com "mo"
    # Combinação: TODOS os critérios devem ser atendidos (E lógico)
    
    # Outros combinadores CSS:
    # a, p          -> tags <a> OU <p> (OU lógico)
    # a p           -> <p> descendente de <a> (espaço = descendant)
    # a > p         -> <p> filho direto de <a>
    # a + p         -> <p> imediatamente após <a> (sibling adjacente)
    # a ~ p         -> <p> irmão de <a> (sibling geral)
    
    # === CASO (C): SELETOR DE FILHO DIRETO ===
    # Busca filhos diretos de <p> com classe "story"
    resultados['filhos_story'] = soup.select("p.story > *")
    
    # Explicação do seletor "p.story > *":
    # p.story       -> parágrafo com classe "story"
    # >             -> combinator de filho direto (não descendente)
    # *             -> wildcard (qualquer elemento)
    # Resultado: elementos que são filhos DIRETOS de p.story
    
    # Diferença filho vs descendente:
    # p.story *     -> TODOS os descendentes (qualquer nível)
    # p.story > *   -> APENAS filhos diretos (1 nível abaixo)
    
    return resultados

# === DADOS DE TESTE ESTRUTURADOS ===
# HTML de teste baseado no exemplo clássico dos Três Porquinhos
pig_html = """
<html><head><title>Os Tres Porquinhos</title></head>
<body>
<p class="title"><b>Os Tres Porquinhos</b></p>
<p class="story">Era uma vez tres porquinhos chamados
<a href="http://example.com/larry" class="pig" id="link1">Larry,</a>
<a href="http://example.com/mo" class="pig" id="link2">Mo</a> e
<a href="http://example.com/curly" class="pig" id="link3">Curly.</a>
</p>
<p>Os tres porquinhos tinham um fascinio peculiar por construcoes experimentais.</p>
<p>...</p>
</body></html>
"""

# Análise estrutural dos dados de teste:
# 
# Caso A - IDs iniciando com "link":
#   - id="link1" ✓ (inicia com "link")
#   - id="link2" ✓ (inicia com "link") 
#   - id="link3" ✓ (inicia com "link")
#   - Resultado esperado: 3 elementos
#
# Caso B - Links classe "pig" com href terminando "mo":
#   - <a class="pig" href="...larry"> ✗ (não termina com "mo")
#   - <a class="pig" href="...mo"> ✓ (termina com "mo")
#   - <a class="pig" href="...curly"> ✗ (não termina com "mo")
#   - Resultado esperado: 1 elemento
#
# Caso C - Filhos diretos de p.story:
#   - Text node "Era uma vez..." ✗ (* não inclui text nodes)
#   - <a id="link1"> ✓ (filho direto)
#   - Text node "\n" ✗ (text node)
#   - <a id="link2"> ✓ (filho direto)
#   - Text node " e\n" ✗ (text node)
#   - <a id="link3"> ✓ (filho direto)
#   - Resultado esperado: 3 elementos <a>

# === EXECUÇÃO E ANÁLISE DOS RESULTADOS ===
resultados = usar_seletores_css(pig_html)

print("=== DEMONSTRAÇÃO DE SELETORES CSS ===")

print(f"\n(A) IDs iniciados por 'link': {len(resultados['ids_link'])} encontrados")
for i, tag in enumerate(resultados['ids_link'], 1):
    id_value = tag.get('id')
    texto = tag.get_text().strip()
    print(f"  {i}. id='{id_value}' -> texto: '{texto}'")

print(f"\n(B) Links classe 'pig' href terminando 'mo': {len(resultados['a_pig_mo'])} encontrado")
for i, tag in enumerate(resultados['a_pig_mo'], 1):
    href = tag.get('href')
    classe = tag.get('class')
    texto = tag.get_text().strip()
    print(f"  {i}. href='{href}' class='{classe}' -> texto: '{texto}'")

print(f"\n(C) Filhos diretos de <p class='story'>: {len(resultados['filhos_story'])} encontrados")
for i, tag in enumerate(resultados['filhos_story'], 1):
    tag_name = tag.name
    attrs = dict(tag.attrs) if tag.attrs else {}
    texto = tag.get_text().strip()
    print(f"  {i}. <{tag_name}> {attrs} -> texto: '{texto}'")

# === COMPARAÇÃO COM MÉTODOS ALTERNATIVOS ===
print("\n=== COMPARAÇÃO COM OUTROS MÉTODOS ===")
soup = BeautifulSoup(pig_html, "html.parser")

# Método tradicional vs CSS selector:
print("\nMétodo find_all() vs select():")
print(f"find_all('a', class_='pig'): {len(soup.find_all('a', class_='pig'))} elementos")
print(f"select('a.pig'): {len(soup.select('a.pig'))} elementos")

# === SELETORES CSS ADICIONAIS ÚTEIS ===
# Outros seletores CSS úteis para web scraping:
# 'a:contains("texto")'     -> links contendo texto (não suportado pelo BeautifulSoup)
# 'tr:nth-child(2n)'        -> linhas pares de tabela
# 'input[type="email"]'     -> campos de email
# 'div:not(.exclude)'       -> divs sem classe "exclude"
# ':first-child'            -> primeiro filho
# ':last-child'             -> último filho
# ':empty'                  -> elementos vazios