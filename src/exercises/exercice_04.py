"""
Exercício 04: Busca Avançada com Expressões Regulares

Este script demonstra o uso de expressões regulares (regex) integradas ao BeautifulSoup
para realizar buscas sofisticadas e filtros complexos em documentos HTML.

Funcionalidades implementadas:
- Busca de atributos href com padrões específicos (domínios .edu.br)
- Filtro de conteúdo textual baseado em padrões (maiúscula + ponto)
- Validação de IDs com formato específico (apenas dígitos)
- Compilação de padrões regex para performance otimizada
- Organização de resultados em estrutura de dados clara

Conceitos de programação abordados:
- Expressões regulares (regex) com módulo 're'
- Compilação de padrões com re.compile()
- Integração de regex com métodos find_all() do BeautifulSoup
- Navegação DOM (parent) para contexto de elementos
- Estruturas de dados organizadas (dicionários)
- Metacaracteres regex: ^, $, \d, \., .*
"""

# Importações necessárias
from bs4 import BeautifulSoup  # Parser HTML
import re                      # Expressões regulares

def buscar_com_regex(html_string):
    """
    Utiliza expressões regulares para localizar tags específicas com padrões complexos
    
    Esta função demonstra três casos de uso comuns de regex em web scraping:
    1. Validação de domínios em URLs (filtro por extensão)
    2. Análise de padrões textuais (formatação de frases)
    3. Validação de identificadores (formato de IDs)
    
    Args:
        html_string (str): String HTML para análise com regex
    
    Returns:
        dict: Dicionário com três categorias de resultados:
            - 'dominios_edu_br': Tags com href terminando em .edu.br
            - 'strings_maiuscula_ponto': Tags contendo texto maiúscula+ponto
            - 'ids_apenas_digitos': Tags com IDs contendo apenas dígitos
    """
    # === PARSING DO DOCUMENTO HTML ===
    soup = BeautifulSoup(html_string, "html.parser")
    
    # === ESTRUTURA DE RESULTADOS ===
    resultados = {
        'dominios_edu_br': [],          # Tags <a> com href *.edu.br
        'strings_maiuscula_ponto': [],  # Tags com texto "Maiúscula...ponto."
        'ids_apenas_digitos': []        # Tags com id="123456"
    }
    
    # === CASO (A): BUSCA POR DOMÍNIOS .EDU.BR ===
    # Compila padrão regex para URLs terminadas em .edu.br
    href_edu_pattern = re.compile(r'\.edu\.br$')
    # Explicação do padrão r'\.edu\.br$':
    # r''          -> raw string (evita escape duplo)
    # \.           -> ponto literal (escapado porque . é metacaractere)
    # edu          -> texto literal "edu"
    # \.           -> ponto literal novamente
    # br           -> texto literal "br"
    # $            -> final da string (âncora)
    
    # Busca todas as tags que possuem href correspondente ao padrão
    tags_edu = soup.find_all(href=href_edu_pattern)
    # find_all(href=pattern): BeautifulSoup aceita regex como valor
    # Procura qualquer tag (não apenas <a>) com atributo href
    # que corresponda ao padrão compilado
    
    resultados['dominios_edu_br'] = tags_edu
    
    # === CASO (B): BUSCA POR TEXTO COM PADRÃO ESPECÍFICO ===
    # Compila padrão para texto iniciando com maiúscula e terminando com ponto
    texto_pattern = re.compile(r'^[A-Z].*\.$')
    # Explicação do padrão r'^[A-Z].*\.$':
    # ^            -> início da string (âncora)
    # [A-Z]        -> classe de caracteres: qualquer letra maiúscula
    # .*           -> qualquer caractere (.) zero ou mais vezes (*)
    # \.           -> ponto literal (escapado)
    # $            -> final da string (âncora)
    
    # Busca strings (text nodes) que correspondam ao padrão
    strings_maiusc = soup.find_all(string=texto_pattern)
    # find_all(string=pattern): busca em text nodes (não tags)
    # Retorna os próprios text nodes, não as tags que os contêm
    
    # Obtém as tags que contêm essas strings (elementos pais)
    resultados['strings_maiuscula_ponto'] = [s.parent for s in strings_maiusc]
    # s.parent: navega do text node para a tag que o contém
    # List comprehension para transformar text nodes em tags
    
    # === CASO (C): BUSCA POR IDs NUMÉRICOS ===
    # Compila padrão para IDs contendo apenas dígitos
    id_digits_pattern = re.compile(r'^\d+$')
    # Explicação do padrão r'^\d+$':
    # ^            -> início da string
    # \d           -> qualquer dígito (equivale a [0-9])
    # +            -> um ou mais (pelo menos um dígito)
    # $            -> final da string
    # Resultado: apenas strings compostas exclusivamente de dígitos
    
    # Busca tags com atributo id correspondente ao padrão
    tags_id_digitos = soup.find_all(id=id_digits_pattern)
    # find_all(id=pattern): busca por atributo id específico
    # Qualquer tag pode ter id, não apenas divs
    
    resultados['ids_apenas_digitos'] = tags_id_digitos
    
    return resultados

# === DADOS DE TESTE ABRANGENTES ===
html_teste = """
<html>
<body>
    <p>Este é um exemplo.</p>
    <a href="https://univasf.edu.br">UNIVASF</a>
    <a href="https://ufes.br">UFES</a>
    <a href="https://pucminas.edu.br">PUC Minas</a>
    <div id="123">Div com ID numérico</div>
    <div id="abc123">Div com ID alfanumérico</div>
    <div id="456">Outro ID numérico</div>
    <span>Texto iniciando maiúscula.</span>
    <span>texto minúsculo</span>
    <p>Parágrafo correto com ponto.</p>
</body>
</html>
"""

# Análise dos dados de teste:
# Caso A - Domínios .edu.br:
#   - https://univasf.edu.br ✓ (corresponde)
#   - https://ufes.br ✗ (não termina com .edu.br)
#   - https://pucminas.edu.br ✓ (corresponde)
#
# Caso B - Texto maiúscula+ponto:
#   - "Este é um exemplo." ✓ (inicia maiúscula, termina ponto)
#   - "Texto iniciando maiúscula." ✓ (corresponde)
#   - "texto minúsculo" ✗ (não inicia maiúscula)
#   - "Parágrafo correto com ponto." ✓ (corresponde)
#
# Caso C - IDs apenas dígitos:
#   - id="123" ✓ (apenas dígitos)
#   - id="abc123" ✗ (contém letras)
#   - id="456" ✓ (apenas dígitos)

# === EXECUÇÃO E ANÁLISE ===
resultados = buscar_com_regex(html_teste)

print("=== RESULTADOS DA BUSCA COM REGEX ===")

print(f"\n(A) Domínios .edu.br encontrados: {len(resultados['dominios_edu_br'])}")
for i, tag in enumerate(resultados['dominios_edu_br'], 1):
    href = tag.get('href', 'N/A')
    texto = tag.get_text().strip()
    print(f"  {i}. {tag} -> href: {href}, texto: '{texto}'")

print(f"\n(B) Strings maiúscula+ponto: {len(resultados['strings_maiuscula_ponto'])}")
for i, tag in enumerate(resultados['strings_maiuscula_ponto'], 1):
    texto = tag.get_text().strip()
    print(f"  {i}. <{tag.name}> -> texto: '{texto}'")

print(f"\n(C) IDs apenas dígitos: {len(resultados['ids_apenas_digitos'])}")
for i, tag in enumerate(resultados['ids_apenas_digitos'], 1):
    id_value = tag.get('id', 'N/A')
    print(f"  {i}. <{tag.name} id='{id_value}'> -> {tag}")

# === PADRÕES REGEX ADICIONAIS ÚTEIS ===
# Outros padrões comuns para web scraping:
# r'https?://'              -> URLs HTTP ou HTTPS
# r'\b\d{4}\b'             -> Anos (4 dígitos)
# r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' -> Emails
# r'\(\d{2}\)\s\d{4,5}-\d{4}' -> Telefones formato (11) 99999-9999
# r'#[a-fA-F0-9]{6}'       -> Cores hexadecimais
# r'R\$\s?\d+[.,]\d{2}'    -> Preços em reais