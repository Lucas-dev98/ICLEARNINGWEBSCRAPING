"""
Exemplo 01: Requisição HTTP e Análise de Resposta

Este script demonstra como fazer uma requisição HTTP básica usando Python,
incluindo resolução DNS, análise de cabeçalhos e exibição do status da resposta.

Funcionalidades:
- Resolução manual de DNS para obter o endereço IP do servidor
- Requisição HTTP GET para um website
- Análise e exibição dos cabeçalhos de resposta
- Verificação do status code da resposta HTTP

Bibliotecas utilizadas:
- requests: Para fazer requisições HTTP de forma simplificada
- socket: Para operações de rede de baixo nível (resolução DNS)
- urllib.parse: Para análise e manipulação de URLs
"""

# Importação das bibliotecas necessárias
import requests      # Biblioteca principal para requisições HTTP
import socket       # Biblioteca para operações de rede (DNS, sockets)
from urllib.parse import urlparse  # Função para fazer parsing de URLs

# Definição da URL alvo para a requisição
url = 'https://uvv.br'  # URL da Universidade Vila Velha

# === RESOLUÇÃO DNS MANUAL ===
# Fazendo o parsing da URL para extrair componentes
parsed_url = urlparse(url)  # Quebra a URL em componentes (esquema, host, caminho, etc.)
host = parsed_url.hostname  # Extrai apenas o hostname (uvv.br)

# Resolvendo o hostname para endereço IP usando DNS
ip = socket.gethostbyname(host)  # Consulta DNS para obter o IP do servidor

# Exibindo informações de DNS
print(f"Host: {host}")
print(f"IP resolvido via DNS: {ip}")

# === REQUISIÇÃO HTTP ===
# Fazendo uma requisição HTTP GET para a URL especificada
response = requests.get(url)  # O requests cuida automaticamente de:
                             # - Resolução DNS
                             # - Conexão TCP
                             # - Handshake TLS/SSL (para HTTPS)
                             # - Envio da requisição HTTP
                             # - Recebimento da resposta

# === ANÁLISE DA RESPOSTA ===
# Exibindo o status code e reason phrase da resposta HTTP
print(f"\nStatus HTTP: {response.status_code} {response.reason}")
# status_code: código numérico (200, 404, 500, etc.)
# reason: texto explicativo ("OK", "Not Found", "Internal Server Error", etc.)

# Exibindo todos os cabeçalhos da resposta HTTP
print("\n == Cabecalhos da RESPOSTA ==")
for k, v in response.headers.items():  # response.headers é um dicionário-like
    print(f"{k}: {v}")  # Formato: "Nome-do-Cabeçalho: Valor"
    
# Cabeçalhos comuns que podem aparecer:
# - Content-Type: tipo de conteúdo (text/html, application/json, etc.)
# - Content-Length: tamanho do corpo da resposta em bytes
# - Server: software do servidor web
# - Date: data e hora da resposta
# - Set-Cookie: cookies definidos pelo servidor
# - Cache-Control: instruções de cache
# - Location: usado em redirecionamentos