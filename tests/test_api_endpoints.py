import pytest
import requests
from unittest.mock import patch, MagicMock
import json

BASE_URL = "http://127.0.0.1:8000"

class TestAPIEndpoints:
    """Testes para endpoints da API"""
    
    def test_root_endpoint(self):
        """Testa endpoint raiz"""
        response = requests.get(f"{BASE_URL}/")
        assert response.status_code == 200
        data = response.json()
        assert "mensagem" in data
        assert "online" in data["mensagem"]
    
    def test_listar_usuarios_success(self):
        """Testa listagem de usuários com sucesso"""
        response = requests.get(f"{BASE_URL}/usuarios")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_obter_usuario_id_invalido(self):
        """Testa busca com ID inválido"""
        response = requests.get(f"{BASE_URL}/usuarios/id_invalido")
        assert response.status_code == 400
        data = response.json()
        assert "ID inválido" in data["detail"]
    
    def test_obter_usuario_inexistente(self):
        """Testa busca de usuário inexistente"""
        id_fake = "507f1f77bcf86cd799439011"  # ObjectId válido mas inexistente
        response = requests.get(f"{BASE_URL}/usuarios/{id_fake}")
        assert response.status_code == 404
        data = response.json()
        assert "não encontrado" in data["detail"]
    
    def test_criar_usuario_dados_validos(self):
        """Testa criação de usuário com dados válidos"""
        usuario_data = {
            "nome": "Teste Agricultor",
            "email": "teste@fazenda.com.br",
            "papel": "agricultor"
        }
        response = requests.post(f"{BASE_URL}/usuarios", json=usuario_data)
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == usuario_data["nome"]
        assert "_id" in data
    
    def test_criar_usuario_email_invalido(self):
        """Testa criação com email inválido"""
        usuario_data = {
            "nome": "Teste",
            "email": "email_invalido",
            "papel": "agricultor"
        }
        response = requests.post(f"{BASE_URL}/usuarios", json=usuario_data)
        assert response.status_code == 422  # Validation error
    
    def test_leituras_solo_id_invalido(self):
        """Testa leituras de solo com ID inválido"""
        response = requests.get(f"{BASE_URL}/leituras_solo/id_invalido")
        assert response.status_code == 400
    
    def test_diagnostico_id_invalido(self):
        """Testa diagnóstico com ID inválido"""
        response = requests.get(f"{BASE_URL}/diagnostico/id_invalido")
        assert response.status_code == 400

if __name__ == "__main__":
    pytest.main([__file__, "-v"])