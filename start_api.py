#!/usr/bin/env python3
"""Script para inicializar a API EKKO"""
import subprocess
import sys
import os

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    try:
        import fastapi, uvicorn, pymongo, dotenv
        print("[OK] Dependencias verificadas")
        return True
    except ImportError as e:
        print(f"[ERRO] Dependencia faltando: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def verificar_env():
    """Verifica se o arquivo .env existe"""
    if os.path.exists('.env'):
        print("[OK] Arquivo .env encontrado")
        return True
    else:
        print("[ERRO] Arquivo .env nao encontrado")
        print("Crie um arquivo .env com MONGO_URI=sua_string_de_conexao")
        return False

def iniciar_api():
    """Inicia a API"""
    if not verificar_dependencias() or not verificar_env():
        return False
    
    print("[START] Iniciando API EKKO...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "EkkoAPI.main:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n[STOP] API interrompida")
    except Exception as e:
        print(f"[ERRO] Erro: {e}")
        return False
    
    return True

if __name__ == "__main__":
    iniciar_api()