#!/usr/bin/env python3
"""Script para executar todos os testes do projeto EKKO"""
import subprocess
import sys
import os

def instalar_pytest():
    try:
        import pytest
        return True
    except ImportError:
        print("📦 Instalando pytest...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest", "pytest-cov"])
        return True

def executar_testes():
    if not instalar_pytest():
        return False
    
    print("🧪 Executando testes do EKKO Thai...\n")
    
    # Comandos de teste
    comandos = [
        # Testes básicos
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        
        # Testes com cobertura
        [sys.executable, "-m", "pytest", "tests/", "--cov=EkkoAPI", "--cov=EkkoPython", "--cov-report=term-missing"]
    ]
    
    for i, comando in enumerate(comandos, 1):
        print(f"\n{'='*50}")
        print(f"🔄 Executando bateria {i}/{len(comandos)}")
        print(f"{'='*50}")
        
        try:
            result = subprocess.run(comando, capture_output=False)
            if result.returncode != 0:
                print(f"⚠️ Alguns testes falharam na bateria {i}")
        except Exception as e:
            print(f"❌ Erro ao executar testes: {e}")
    
    print(f"\n{'='*50}")
    print("✅ Execução de testes concluída!")
    print("📊 Verifique os resultados acima")
    print(f"{'='*50}")

def verificar_api():
    """Verifica se a API está rodando"""
    try:
        import requests
        response = requests.get("http://127.0.0.1:8000/", timeout=2)
        if response.status_code == 200:
            print("✅ API está rodando")
            return True
    except:
        pass
    
    print("⚠️ API não está rodando")
    print("💡 Para testes de integração, execute: python start_api.py")
    return False

if __name__ == "__main__":
    print("🌱 EKKO - Execução de Testes")
    print("="*40)
    
    verificar_api()
    executar_testes()