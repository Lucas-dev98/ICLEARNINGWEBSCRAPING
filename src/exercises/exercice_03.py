"""
Exercício 03: Análise de Tags Específicas e Manipulação de Arquivos

Este script demonstra análise focada em elementos específicos do HTML,
incluindo extração de texto, validação de atributos e manipulação segura de arquivos.

Funcionalidades implementadas:
- Leitura segura de arquivos HTML com encoding apropriado
- Busca direcionada por tipo específico de tag
- Extração e limpeza de conteúdo textual
- Validação de presença de atributos HTML
- Tratamento robusto de exceções e casos edge
- Criação de arquivos de teste para demonstração

Conceitos de programação abordados:
- Context managers para manipulação de arquivos
- Tratamento hierárquico de exceções
- Métodos de busca específica do BeautifulSoup
- Validação de atributos com operador 'in'
- Tuplas como tipo de retorno estruturado
- Limpeza de strings com strip()
"""

# Importação da biblioteca BeautifulSoup para parsing HTML
from bs4 import BeautifulSoup

def analisar_primeira_tag_a(arquivo_html):
    """
    Carrega um arquivo HTML, encontra a primeira tag <a> e retorna
    seu texto junto com um boolean indicando se possui atributo href
    
    Esta função implementa um pipeline completo de análise:
    1. Leitura segura de arquivo com encoding UTF-8
    2. Parsing do conteúdo HTML em estrutura navegável
    3. Busca pela primeira ocorrência de tag <a>
    4. Extração e limpeza do texto interno
    5. Validação da presença do atributo href
    6. Tratamento de todos os casos de erro possíveis
    
    Args:
        arquivo_html (str): Caminho relativo ou absoluto para arquivo HTML
                           Deve ser um arquivo texto válido
    
    Returns:
        tuple: (texto_da_tag, possui_href)
            - texto_da_tag (str): Conteúdo textual da tag ou mensagem de erro
            - possui_href (bool): True se a tag possui atributo href, False caso contrário
            
    Examples:
        >>> analisar_primeira_tag_a('pagina.html')
        ('Clique aqui', True)
        
        >>> analisar_primeira_tag_a('sem_links.html') 
        ('Nenhuma tag <a> encontrada', False)
    """
    try:
        # === LEITURA SEGURA DO ARQUIVO ===
        with open(arquivo_html, 'r', encoding='utf-8') as file:
            html_content = file.read()
        # Context manager (with) garante:
        # - Abertura segura do arquivo
        # - Fechamento automático mesmo em caso de erro
        # - Encoding UTF-8 para suporte a acentos/caracteres especiais
        # - Leitura completa do conteúdo em string
        
        # === PARSING DO CONTEÚDO HTML ===
        soup = BeautifulSoup(html_content, "html.parser")
        # Cria árvore DOM navegável que:
        # - Corrige HTML malformado automaticamente
        # - Permite busca e navegação eficiente
        # - Normaliza a estrutura do documento
        
        # === BUSCA PELA PRIMEIRA TAG <A> ===
        primeira_tag_a = soup.find('a')
        # find() retorna:
        # - Primeira ocorrência da tag especificada
        # - None se nenhuma tag <a> for encontrada
        # - Elemento Tag navegável se encontrada
        
        # Métodos alternativos de busca:
        # soup.a                    # Acesso direto (mesmo resultado)
        # soup.select_one('a')      # Seletor CSS
        # soup.find(name='a')       # Parâmetro explícito
        
        # === VALIDAÇÃO DE EXISTÊNCIA ===
        if primeira_tag_a is None:
            return ("Nenhuma tag <a> encontrada", False)
        # Retorno antecipado para caso onde não há links no documento
        
        # === EXTRAÇÃO E LIMPEZA DO TEXTO ===
        texto = primeira_tag_a.get_text().strip()
        # get_text(): extrai todo texto interno (sem tags HTML)
        # strip(): remove espaços/quebras de linha no início/fim
        
        # Métodos alternativos para texto:
        # primeira_tag_a.string     # Apenas texto direto (não de sub-elementos)
        # primeira_tag_a.text       # Alias para get_text()
        # ' '.join(primeira_tag_a.stripped_strings)  # Texto limpo com espaços normalizados
        
        # === VALIDAÇÃO DE ATRIBUTO HREF ===
        possui_href = 'href' in primeira_tag_a.attrs
        # primeira_tag_a.attrs: dicionário com todos os atributos
        # Operador 'in': verifica presença da chave no dicionário
        
        # Métodos alternativos para verificar href:
        # primeira_tag_a.get('href') is not None
        # primeira_tag_a.has_attr('href')
        # bool(primeira_tag_a.get('href'))
        
        return (texto, possui_href)
        
    except FileNotFoundError:
        # === TRATAMENTO DE ARQUIVO NÃO ENCONTRADO ===
        return ("Arquivo não encontrado", False)
        # Erro específico: arquivo não existe no caminho especificado
        
    except UnicodeDecodeError:
        # === TRATAMENTO DE PROBLEMAS DE ENCODING ===
        return ("Erro de codificação do arquivo", False)
        # Erro específico: arquivo não é UTF-8 ou tem caracteres inválidos
        
    except PermissionError:
        # === TRATAMENTO DE PROBLEMAS DE PERMISSÃO ===
        return ("Sem permissão para ler o arquivo", False)
        # Erro específico: usuário não tem permissão de leitura
        
    except Exception as e:
        # === TRATAMENTO GENÉRICO DE OUTROS ERROS ===
        return (f"Erro inesperado: {e}", False)
        # Captura qualquer outro erro não previsto

# === DEMONSTRAÇÃO E TESTE ===
# Comentado para não executar com arquivo real que pode não existir
# resultado = analisar_primeira_tag_a('uvv.html')
# print(f"Texto: '{resultado[0]}'")
# print(f"Possui href: {resultado[1]}")

# === CRIAÇÃO DE DADOS DE TESTE ===
# HTML de exemplo para demonstrar diferentes cenários
html_exemplo = """
<html>
<body>
<p>Visite nosso <a href="https://uvv.br">site oficial</a> para mais informações.</p>
<a>Link sem href</a>
</body>
</html>
"""
# Este HTML contém:
# - Primeira tag <a>: tem href e texto "site oficial"
# - Segunda tag <a>: não tem href, apenas texto "Link sem href"
# - A função deve encontrar a primeira (com href)

# === CRIAÇÃO DE ARQUIVO DE TESTE ===
# Salvando exemplo para teste da função
with open('exemplo_teste.html', 'w', encoding='utf-8') as f:
    f.write(html_exemplo)
# Cria arquivo temporário para testar a função

# === EXECUÇÃO DO TESTE ===
resultado = analisar_primeira_tag_a('exemplo_teste.html')
print(f"Texto extraído: '{resultado[0]}'")
print(f"Possui atributo href: {resultado[1]}")

# Resultado esperado:
# Texto extraído: 'site oficial'
# Possui atributo href: True