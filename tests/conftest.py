import pytest
import requests
import time
from unittest.mock import patch

@pytest.fixture(scope="session")
def api_server():
    """Fixture para garantir que a API está rodando"""
    try:
        response = requests.get("http://127.0.0.1:8000/")
        if response.status_code == 200:
            return "http://127.0.0.1:8000"
    except requests.exceptions.ConnectionError:
        pytest.skip("API não está rodando. Execute 'python start_api.py' primeiro.")

@pytest.fixture
def sample_user_data():
    """Dados de usuário para testes"""
    return {
        "nome": "João Teste Silva",
        "email": "joao.teste@fazenda.com.br",
        "papel": "agricultor"
    }

@pytest.fixture
def sample_soil_reading():
    """Leitura de solo para testes"""
    return {
        "pH": 6.5,
        "umidade": 70.0,
        "temperatura": 25.0,
        "condutividade_eletrica": 2.0,
        "salinidade": 1.0,
        "NPK": {
            "nitrogenio": 80.0,
            "fosforo": 35.0,
            "potassio": 130.0
        },
        "dispositivo": "EKKO-Sensor-TEST",
        "data_leitura": "2024-01-01T12:00:00"
    }

@pytest.fixture
def mock_mongodb():
    """Mock para MongoDB em testes unitários"""
    with patch('pymongo.MongoClient') as mock_client:
        mock_db = mock_client.return_value.__getitem__.return_value
        mock_collection = mock_db.__getitem__.return_value
        
        # Configurar comportamentos padrão
        mock_collection.find.return_value = []
        mock_collection.find_one.return_value = None
        mock_collection.insert_one.return_value.inserted_id = "test_id"
        
        yield {
            'client': mock_client,
            'db': mock_db,
            'collection': mock_collection
        }