"""
Exercício 05: Duplicata do Exercício 04

NOTA: Este arquivo é uma duplicata exata do exercice_04.py.
Possivelmente foi criado por engano ou para backup durante o desenvolvimento.

O conteúdo é idêntico ao exercício anterior, incluindo:
- Busca com expressões regulares no BeautifulSoup
- Três casos de uso: domínios .edu.br, texto com maiúscula+ponto, IDs numéricos
- Mesmos dados de teste e resultados

Para documentação completa, consulte o exercice_04.py que contém
a explicação detalhada de todos os conceitos e implementações.
"""

from bs4 import BeautifulSoup
import re

def buscar_com_regex(html_string):
    """
    Utiliza expressões regulares para localizar tags específicas
    
    Args:
        html_string (str): String HTML para análise
    
    Returns:
        dict: Dicionário com as três categorias de resultados
    """
    soup = BeautifulSoup(html_string, "html.parser")
    
    resultados = {
        'dominios_edu_br': [],
        'strings_maiuscula_ponto': [],
        'ids_apenas_digitos': []
    }
    
    # (a) Tags com href terminando em .edu.br
    href_edu_pattern = re.compile(r'\.edu\.br$')
    tags_edu = soup.find_all(href=href_edu_pattern)
    resultados['dominios_edu_br'] = tags_edu
    
    # (b) Strings que iniciem com maiúscula e terminem com ponto
    texto_pattern = re.compile(r'^[A-Z].*\.$')
    strings_maiusc = soup.find_all(string=texto_pattern)
    resultados['strings_maiuscula_ponto'] = [s.parent for s in strings_maiusc]
    
    # (c) IDs que contenham apenas dígitos
    id_digits_pattern = re.compile(r'^\d+$')
    tags_id_digitos = soup.find_all(id=id_digits_pattern)
    resultados['ids_apenas_digitos'] = tags_id_digitos
    
    return resultados

# HTML de teste
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

resultados = buscar_com_regex(html_teste)

print("=== RESULTADOS ===")
print(f"Domínios .edu.br encontrados: {len(resultados['dominios_edu_br'])}")
for tag in resultados['dominios_edu_br']:
    print(f"  - {tag}")

print(f"\nStrings maiúscula+ponto: {len(resultados['strings_maiuscula_ponto'])}")
for tag in resultados['strings_maiuscula_ponto']:
    print(f"  - {tag}")

print(f"\nIDs apenas dígitos: {len(resultados['ids_apenas_digitos'])}")
for tag in resultados['ids_apenas_digitos']:
    print(f"  - {tag}")