#!/usr/bin/env python3
"""
Configuração do PYTHONPATH para o projeto
=========================================

Este script configura o PYTHONPATH para permitir imports dos módulos
do projeto a partir de qualquer diretório.
"""

import sys
import os
from pathlib import Path

def setup_python_path():
    """Configura o PYTHONPATH para incluir o diretório do projeto."""
    
    # Detectar diretório raiz do projeto
    current_dir = Path(__file__).parent.parent.absolute()
    
    # Adicionar ao sys.path se não estiver lá
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Configurar PYTHONPATH como variável de ambiente
    python_path = os.environ.get('PYTHONPATH', '')
    
    if str(current_dir) not in python_path:
        if python_path:
            os.environ['PYTHONPATH'] = f"{current_dir}:{python_path}"
        else:
            os.environ['PYTHONPATH'] = str(current_dir)
    
    return current_dir

# Executar automaticamente quando importado
PROJECT_ROOT = setup_python_path()

if __name__ == "__main__":
    print(f"📁 Diretório do projeto: {PROJECT_ROOT}")
    print(f"🐍 PYTHONPATH configurado: {os.environ.get('PYTHONPATH')}")
    print("✅ Configuração do Python path concluída!")