"""
Exercício 01: Download e Persistência de Conteúdo HTML

Este script demonstra como fazer download de páginas web e salvar o conteúdo
localmente, incluindo tratamento robusto de erros e validações de segurança.

Funcionalidades implementadas:
- Download seguro de conteúdo HTML via HTTP/HTTPS
- Verificação de existência de arquivo (evita sobrescrita)
- Tratamento de exceções para requisições e I/O
- Validação de status HTTP
- Codificação adequada para caracteres especiais
- Relatório de progresso e estatísticas

Conceitos de programação abordados:
- Manipulação de arquivos com context managers (with statement)
- Tratamento de exceções específicas e hierárquicas
- Validação de condições pré-execução
- Encoding UTF-8 para suporte internacional
- Práticas de segurança em requisições web
"""

# Importações necessárias
import requests  # Biblioteca para requisições HTTP/HTTPS
import os       # Biblioteca para operações do sistema operacional

def baixar_html_uvv():
    """
    Baixa o HTML do site da UVV e salva como uvv.html
    
    Esta função implementa um processo completo de download web:
    1. Verificação de pré-condições (arquivo existente)
    2. Requisição HTTP com tratamento de erros
    3. Validação de resposta HTTP
    4. Persistência segura em arquivo local
    5. Relatório de resultado e estatísticas
    
    Returns:
        None: Função não retorna valor, mas imprime status na tela
        
    Raises:
        Captura e trata todas as exceções internamente
    """
    # === CONFIGURAÇÃO INICIAL ===
    url = 'https://www.uvv.br'  # URL da Universidade Vila Velha
    filename = 'uvv.html'       # Nome do arquivo de destino
    
    # === VALIDAÇÃO PRÉ-EXECUÇÃO ===
    # Verifica se o arquivo já existe para evitar sobrescrita acidental
    if os.path.exists(filename):
        print(f"Arquivo {filename} já existe. Não será sobrescrito.")
        print("Dica: remova o arquivo existente se quiser fazer novo download.")
        return  # Sai da função sem fazer download
    
    try:
        # === REQUISIÇÃO HTTP ===
        print(f"Iniciando download de {url}...")
        
        # Faz a requisição GET para a URL especificada
        response = requests.get(url)
        # O requests automaticamente:
        # - Resolve DNS
        # - Estabelece conexão TCP/TLS
        # - Envia headers HTTP apropriados
        # - Segue redirecionamentos (até limite)
        # - Decodifica conteúdo baseado no Content-Type
        
        # === VALIDAÇÃO DE RESPOSTA ===
        # Verifica se a resposta HTTP indica sucesso
        response.raise_for_status()  
        # raise_for_status() levanta HTTPError se:
        # - 4xx: Erro do cliente (404 Not Found, 403 Forbidden, etc.)
        # - 5xx: Erro do servidor (500 Internal Server Error, 502 Bad Gateway, etc.)
        # Códigos 2xx (sucesso) e 3xx (redirecionamento) passam sem erro
        
        # === PERSISTÊNCIA EM ARQUIVO ===
        # Salva o conteúdo HTML em arquivo local
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        # Context manager (with) garante:
        # - Abertura segura do arquivo
        # - Fechamento automático mesmo se houver erro
        # - Encoding UTF-8 para suporte a caracteres especiais/acentos
        # - response.text contém o HTML já decodificado como string
        
        # === RELATÓRIO DE SUCESSO ===
        print(f"✓ Arquivo {filename} salvo com sucesso!")
        print(f"✓ Status HTTP: {response.status_code} ({response.reason})")
        print(f"✓ Tamanho do arquivo: {len(response.text):,} caracteres")
        
        # Informações adicionais disponíveis:
        # - response.headers: cabeçalhos da resposta
        # - response.encoding: codificação detectada
        # - response.url: URL final (após redirecionamentos)
        # - response.elapsed: tempo de resposta
        
    except requests.exceptions.RequestException as e:
        # === TRATAMENTO DE ERROS DE REDE ===
        # Captura todos os erros relacionados a requisições:
        # - ConnectionError: problemas de conectividade
        # - Timeout: requisição demorou demais
        # - HTTPError: status HTTP de erro (via raise_for_status)
        # - TooManyRedirects: muitos redirecionamentos
        print(f"✗ Erro ao fazer requisição: {e}")
        print("Possíveis causas: sem internet, site fora do ar, URL inválida")
        
    except IOError as e:
        # === TRATAMENTO DE ERROS DE ARQUIVO ===
        # Captura erros de entrada/saída:
        # - PermissionError: sem permissão para escrever
        # - FileNotFoundError: diretório não existe
        # - OSError: disco cheio, problemas de sistema
        print(f"✗ Erro ao salvar arquivo: {e}")
        print("Possíveis causas: sem espaço em disco, sem permissão de escrita")

# === EXECUÇÃO DO SCRIPT ===
# Executa a função quando o script é rodado diretamente
if __name__ == "__main__":
    baixar_html_uvv()
else:
    # Se for importado como módulo, não executa automaticamente
    print("Módulo importado. Execute baixar_html_uvv() para fazer o download.")