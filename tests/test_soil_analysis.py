import pytest
from EkkoAPI.soil_analysis import SoilAnalysisAI
from datetime import datetime

class TestSoilAnalysisAI:
    """Testes para análise de solo IA"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.ai = SoilAnalysisAI()
        self.leitura_ideal = {
            "pH": 6.5,
            "umidade": 70,
            "temperatura": 25,
            "NPK": {"nitrogenio": 80, "fosforo": 35, "potassio": 130}
        }
        self.leitura_critica = {
            "pH": 4.0,
            "umidade": 30,
            "temperatura": 40,
            "NPK": {"nitrogenio": 10, "fosforo": 5, "potassio": 20}
        }
    
    def test_parametros_carregados(self):
        """Testa se parâmetros foram carregados corretamente"""
        assert "Soja" in self.ai.parametros_ideais
        assert "Milho" in self.ai.parametros_ideais
        assert "Café" in self.ai.parametros_ideais
        
        soja_params = self.ai.parametros_ideais["Soja"]
        assert "ph" in soja_params
        assert "umidade" in soja_params
        assert "temperatura" in soja_params
    
    def test_analise_leitura_ideal(self):
        """Testa análise de leitura com valores ideais"""
        resultado = self.ai.analisar_leitura_individual(self.leitura_ideal, "Soja")
        
        assert resultado["status_geral"] == "Excelente"
        assert resultado["score"] == 100
        assert resultado["cor_indicador"] == "verde"
        assert len(resultado["diagnosticos"]) == 0
        assert "data_analise" in resultado
    
    def test_analise_leitura_critica(self):
        """Testa análise de leitura com valores críticos"""
        resultado = self.ai.analisar_leitura_individual(self.leitura_critica, "Soja")
        
        assert resultado["status_geral"] == "Crítico"
        assert resultado["score"] < 50
        assert resultado["cor_indicador"] == "vermelho"
        assert len(resultado["diagnosticos"]) > 0
        assert len(resultado["sugestoes"]) > 0
    
    def test_analise_ph_acido(self):
        """Testa detecção de solo ácido"""
        leitura = {"pH": 4.5, "umidade": 70, "temperatura": 25, "NPK": {}}
        resultado = self.ai.analisar_leitura_individual(leitura, "Soja")
        
        diagnosticos_text = " ".join(resultado["diagnosticos"])
        assert "ácido" in diagnosticos_text.lower()
        
        sugestoes_text = " ".join(resultado["sugestoes"])
        assert "calcário" in sugestoes_text.lower()
    
    def test_analise_solo_seco(self):
        """Testa detecção de solo seco"""
        leitura = {"pH": 6.5, "umidade": 30, "temperatura": 25, "NPK": {}}
        resultado = self.ai.analisar_leitura_individual(leitura, "Soja")
        
        diagnosticos_text = " ".join(resultado["diagnosticos"])
        assert "seco" in diagnosticos_text.lower()
    
    def test_analise_historico_vazio(self):
        """Testa análise histórica com lista vazia"""
        resultado = self.ai.analisar_historico([], "Soja")
        assert "erro" in resultado
    
    def test_analise_historico_tendencias(self):
        """Testa análise de tendências históricas"""
        leituras = [
            {"pH": 6.0, "umidade": 60, "temperatura": 20},
            {"pH": 6.2, "umidade": 65, "temperatura": 22},
            {"pH": 6.5, "umidade": 70, "temperatura": 25}
        ]
        resultado = self.ai.analisar_historico(leituras, "Soja")
        
        assert "medias" in resultado
        assert "tendencias" in resultado
        assert resultado["total_leituras"] == 3
        assert resultado["medias"]["ph"] > 0
    
    def test_cultivo_inexistente_usa_soja(self):
        """Testa que cultivo inexistente usa parâmetros da Soja"""
        resultado = self.ai.analisar_leitura_individual(self.leitura_ideal, "CultivoInexistente")
        # Deve funcionar usando parâmetros da Soja como fallback
        assert "status_geral" in resultado
    
    def test_relatorio_completo_sem_leituras(self):
        """Testa relatório completo sem leituras"""
        usuario_data = {"leituras_solo": []}
        resultado = self.ai.gerar_relatorio_completo(usuario_data)
        assert "erro" in resultado
    
    def test_relatorio_completo_com_dados(self):
        """Testa relatório completo com dados válidos"""
        usuario_data = {
            "nome": "João Silva",
            "nome_fazenda": "Fazenda Teste",
            "propriedade": {"cultivo_principal": "Soja"},
            "leituras_solo": [
                {**self.leitura_ideal, "data_leitura": datetime.now().isoformat()}
            ]
        }
        resultado = self.ai.gerar_relatorio_completo(usuario_data)
        
        assert "usuario" in resultado
        assert "analise_atual" in resultado
        assert "analise_historica" in resultado
        assert "recomendacoes_cultivo" in resultado
        assert resultado["usuario"]["nome"] == "João Silva"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])