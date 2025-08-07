import pytest
from unittest.mock import patch, MagicMock
from EkkoPython.dataGenerator import (
    gerar_usuario_fake, 
    gerar_leitura_solo_fake,
    gerar_dado_sensor_continuo
)
from bson import ObjectId

class TestDataGenerator:
    """Testes para gerador de dados"""
    
    def test_gerar_usuario_fake_estrutura(self):
        """Testa estrutura do usuário gerado"""
        usuario = gerar_usuario_fake()
        
        # Campos obrigatórios
        assert "nome" in usuario
        assert "email" in usuario
        assert "papel" in usuario
        assert "cpf" in usuario
        assert "telefone" in usuario
        assert "nome_fazenda" in usuario
        
        # Estruturas aninhadas
        assert "localizacao" in usuario
        assert "propriedade" in usuario
        assert "dados_tecnicos" in usuario
        
        # Validações específicas
        assert usuario["papel"] == "agricultor"
        assert "@fazenda.com.br" in usuario["email"]
        assert "Fazenda" in usuario["nome_fazenda"]
    
    def test_gerar_usuario_localizacao_valida(self):
        """Testa se localização gerada é válida"""
        usuario = gerar_usuario_fake()
        loc = usuario["localizacao"]
        
        assert "cidade" in loc
        assert "estado" in loc
        assert "regiao" in loc
        assert "coordenadas" in loc
        
        # Coordenadas devem ser números
        assert isinstance(loc["coordenadas"]["latitude"], float)
        assert isinstance(loc["coordenadas"]["longitude"], float)
    
    def test_gerar_usuario_propriedade_valida(self):
        """Testa se propriedade gerada é válida"""
        usuario = gerar_usuario_fake()
        prop = usuario["propriedade"]
        
        assert "area_total_hectares" in prop
        assert "cultivo_principal" in prop
        assert "tipo_solo" in prop
        
        # Área deve ser positiva
        assert prop["area_total_hectares"] > 0
        assert prop["area_cultivada_hectares"] > 0
        
        # Cultivo deve estar na lista válida
        cultivos_validos = ["Soja", "Milho", "Café", "Cana-de-açúcar", "Algodão", 
                           "Feijão", "Arroz", "Trigo", "Tomate", "Batata"]
        assert prop["cultivo_principal"] in cultivos_validos
    
    def test_gerar_leitura_solo_estrutura(self):
        """Testa estrutura da leitura de solo"""
        usuario_id = ObjectId()
        leitura = gerar_leitura_solo_fake(usuario_id, "Soja")
        
        # Campos obrigatórios
        assert "usuario_id" in leitura
        assert "pH" in leitura
        assert "umidade" in leitura
        assert "temperatura" in leitura
        assert "NPK" in leitura
        assert "data_leitura" in leitura
        
        # Validações de tipo
        assert leitura["usuario_id"] == usuario_id
        assert isinstance(leitura["pH"], float)
        assert isinstance(leitura["umidade"], float)
        assert isinstance(leitura["temperatura"], float)
        assert isinstance(leitura["NPK"], dict)
    
    def test_gerar_leitura_valores_realistas(self):
        """Testa se valores gerados são realistas"""
        usuario_id = ObjectId()
        leitura = gerar_leitura_solo_fake(usuario_id, "Soja")
        
        # pH entre 3.0 e 9.0
        assert 3.0 <= leitura["pH"] <= 9.0
        
        # Umidade entre 10% e 100%
        assert 10 <= leitura["umidade"] <= 100
        
        # Temperatura entre 5°C e 45°C
        assert 5 <= leitura["temperatura"] <= 45
        
        # NPK com valores positivos
        npk = leitura["NPK"]
        assert npk["nitrogenio"] > 0
        assert npk["fosforo"] > 0
        assert npk["potassio"] > 0
    
    def test_gerar_leitura_cultivos_diferentes(self):
        """Testa geração para diferentes cultivos"""
        usuario_id = ObjectId()
        
        leitura_soja = gerar_leitura_solo_fake(usuario_id, "Soja")
        leitura_cafe = gerar_leitura_solo_fake(usuario_id, "Café")
        
        # Ambas devem ter estrutura válida
        assert "pH" in leitura_soja
        assert "pH" in leitura_cafe
        
        # Valores podem ser diferentes (teste estatístico básico)
        # Executar múltiplas vezes para verificar variação
        phs_soja = [gerar_leitura_solo_fake(usuario_id, "Soja")["pH"] for _ in range(10)]
        assert len(set(phs_soja)) > 1  # Deve haver variação
    
    def test_gerar_sensor_continuo_sem_historico(self):
        """Testa geração contínua sem histórico"""
        usuario_id = ObjectId()
        dado = gerar_dado_sensor_continuo(usuario_id, None, "Soja")
        
        # Deve gerar leitura inicial
        assert "pH" in dado
        assert "umidade" in dado
        assert "temperatura" in dado
    
    def test_gerar_sensor_continuo_com_historico(self):
        """Testa geração contínua com histórico"""
        usuario_id = ObjectId()
        ultimo_dado = {
            "pH": 6.5,
            "umidade": 70,
            "temperatura": 25,
            "condutividade_eletrica": 2.0,
            "salinidade": 1.0,
            "NPK": {"nitrogenio": 80, "fosforo": 35, "potassio": 130},
            "dispositivo": "EKKO-Sensor-1000",
            "bateria_sensor_pct": 85
        }
        
        novo_dado = gerar_dado_sensor_continuo(usuario_id, ultimo_dado, "Soja")
        
        # Valores devem ser próximos (variação suave)
        assert abs(novo_dado["pH"] - ultimo_dado["pH"]) < 1.0
        assert abs(novo_dado["umidade"] - ultimo_dado["umidade"]) < 10
        assert abs(novo_dado["temperatura"] - ultimo_dado["temperatura"]) < 5
        
        # Bateria deve diminuir ou manter
        assert novo_dado["bateria_sensor_pct"] <= ultimo_dado["bateria_sensor_pct"]
    
    def test_email_sem_acentos(self):
        """Testa se emails gerados não têm acentos"""
        for _ in range(10):
            usuario = gerar_usuario_fake()
            email = usuario["email"]
            
            # Não deve conter acentos comuns
            acentos = ['á', 'à', 'ã', 'â', 'é', 'ê', 'í', 'ó', 'ô', 'õ', 'ú', 'ç']
            for acento in acentos:
                assert acento not in email

if __name__ == "__main__":
    pytest.main([__file__, "-v"])