# EkkoAPI/soil_analysis.py

from typing import Dict, List
from datetime import datetime
import statistics

class SoilAnalysisAI:
    """
    IA simples para análise e diagnóstico de solo baseada em regras agronômicas.
    """
    
    def __init__(self):
        self.parametros_ideais = self._carregar_parametros_cultivos()
    
    def _carregar_parametros_cultivos(self) -> Dict:
        """Carrega parâmetros ideais por cultivo de forma organizada."""
        cultivos = {
            "Soja": (6.0, 7.0, 60, 80, 20, 30, 40, 120, 15, 60, 80, 180),
            "Milho": (5.8, 7.0, 65, 85, 18, 32, 60, 150, 20, 80, 100, 200),
            "Café": (5.5, 6.5, 55, 75, 18, 25, 30, 100, 10, 50, 60, 150)
        }
        
        parametros = {}
        for cultivo, valores in cultivos.items():
            ph_min, ph_max, um_min, um_max, temp_min, temp_max, n_min, n_max, p_min, p_max, k_min, k_max = valores
            parametros[cultivo] = {
                "ph": {"min": ph_min, "max": ph_max, "ideal": (ph_min + ph_max) / 2},
                "umidade": {"min": um_min, "max": um_max, "ideal": (um_min + um_max) / 2},
                "temperatura": {"min": temp_min, "max": temp_max, "ideal": (temp_min + temp_max) / 2},
                "nitrogenio": {"min": n_min, "max": n_max, "ideal": (n_min + n_max) / 2},
                "fosforo": {"min": p_min, "max": p_max, "ideal": (p_min + p_max) / 2},
                "potassio": {"min": k_min, "max": k_max, "ideal": (k_min + k_max) / 2}
            }
        return parametros
    
    def analisar_leitura_individual(self, leitura: Dict, cultivo: str = "Soja") -> Dict:
        """Analisa uma leitura individual de solo."""
        parametros = self.parametros_ideais.get(cultivo, self.parametros_ideais["Soja"])
        diagnosticos = []
        sugestoes = []
        alertas = []
        score_geral = 0
        
        # Análise de pH
        ph = leitura.get("pH", 0)
        ph_params = parametros["ph"]
        if ph < ph_params["min"]:
            diagnosticos.append(f"Solo ácido (pH {ph:.1f})")
            sugestoes.append("Aplicar calcário para correção da acidez")
            alertas.append({"tipo": "crítico", "parametro": "pH", "valor": ph})
        elif ph > ph_params["max"]:
            diagnosticos.append(f"Solo alcalino (pH {ph:.1f})")
            sugestoes.append("Aplicar enxofre ou matéria orgânica")
            alertas.append({"tipo": "atenção", "parametro": "pH", "valor": ph})
        else:
            score_geral += 25
            
        # Análise de Umidade
        umidade = leitura.get("umidade", 0)
        umidade_params = parametros["umidade"]
        if umidade < umidade_params["min"]:
            diagnosticos.append(f"Solo seco ({umidade:.1f}%)")
            sugestoes.append("Aumentar irrigação ou aplicar mulching")
            alertas.append({"tipo": "crítico", "parametro": "umidade", "valor": umidade})
        elif umidade > umidade_params["max"]:
            diagnosticos.append(f"Solo encharcado ({umidade:.1f}%)")
            sugestoes.append("Melhorar drenagem do solo")
            alertas.append({"tipo": "atenção", "parametro": "umidade", "valor": umidade})
        else:
            score_geral += 25
            
        # Análise de Temperatura
        temperatura = leitura.get("temperatura", 0)
        temp_params = parametros["temperatura"]
        if temperatura < temp_params["min"]:
            diagnosticos.append(f"Solo frio ({temperatura:.1f}°C)")
            sugestoes.append("Considerar cobertura do solo ou estufa")
        elif temperatura > temp_params["max"]:
            diagnosticos.append(f"Solo quente ({temperatura:.1f}°C)")
            sugestoes.append("Aplicar cobertura morta ou sombreamento")
        else:
            score_geral += 25
            
        # Análise de NPK
        npk = leitura.get("NPK", {})
        if isinstance(npk, dict):
            n = npk.get("nitrogenio", 0)
            p = npk.get("fosforo", 0)
            k = npk.get("potassio", 0)
            
            if n < parametros["nitrogenio"]["min"]:
                diagnosticos.append(f"Deficiência de Nitrogênio ({n:.1f})")
                sugestoes.append("Aplicar fertilizante nitrogenado")
            elif p < parametros["fosforo"]["min"]:
                diagnosticos.append(f"Deficiência de Fósforo ({p:.1f})")
                sugestoes.append("Aplicar superfosfato simples")
            elif k < parametros["potassio"]["min"]:
                diagnosticos.append(f"Deficiência de Potássio ({k:.1f})")
                sugestoes.append("Aplicar cloreto de potássio")
            else:
                score_geral += 25
        
        # Classificação geral
        if score_geral >= 75:
            status = "Excelente"
            cor = "verde"
        elif score_geral >= 50:
            status = "Bom"
            cor = "amarelo"
        else:
            status = "Crítico"
            cor = "vermelho"
            
        return {
            "status_geral": status,
            "score": score_geral,
            "cor_indicador": cor,
            "diagnosticos": diagnosticos,
            "sugestoes": sugestoes,
            "alertas": alertas,
            "data_analise": datetime.now().isoformat()
        }
    
    def analisar_historico(self, leituras: List[Dict], cultivo: str = "Soja") -> Dict:
        """Analisa tendências no histórico de leituras."""
        if not leituras:
            return {"erro": "Nenhuma leitura disponível"}
            
        # Calcular médias e tendências
        phs = [l.get("pH", 0) for l in leituras]
        umidades = [l.get("umidade", 0) for l in leituras]
        temperaturas = [l.get("temperatura", 0) for l in leituras]
        
        tendencias = []
        
        # Análise de tendência de pH
        if len(phs) >= 3:
            if phs[-1] > phs[-3]:
                tendencias.append("pH em elevação")
            elif phs[-1] < phs[-3]:
                tendencias.append("pH em declínio")
                
        # Análise de tendência de umidade
        if len(umidades) >= 3:
            if umidades[-1] < umidades[-3] - 5:
                tendencias.append("Solo secando progressivamente")
            elif umidades[-1] > umidades[-3] + 5:
                tendencias.append("Aumento da umidade do solo")
        
        # Recomendações baseadas no histórico
        recomendacoes_historico = []
        
        ph_medio = statistics.mean(phs) if phs else 0
        parametros = self.parametros_ideais.get(cultivo, self.parametros_ideais["Soja"])
        
        if ph_medio < parametros["ph"]["min"]:
            recomendacoes_historico.append("Planejar calagem para próxima safra")
        
        umidade_media = statistics.mean(umidades) if umidades else 0
        if umidade_media < parametros["umidade"]["min"]:
            recomendacoes_historico.append("Revisar sistema de irrigação")
            
        return {
            "medias": {
                "ph": round(ph_medio, 2),
                "umidade": round(umidade_media, 2),
                "temperatura": round(statistics.mean(temperaturas), 2) if temperaturas else 0
            },
            "tendencias": tendencias,
            "recomendacoes_historico": recomendacoes_historico,
            "total_leituras": len(leituras)
        }
    
    def gerar_relatorio_completo(self, usuario_data: Dict) -> Dict:
        """Gera relatório completo de análise para um usuário."""
        leituras = usuario_data.get("leituras_solo", [])
        cultivo = usuario_data.get("propriedade", {}).get("cultivo_principal", "Soja")
        
        if not leituras:
            return {"erro": "Nenhuma leitura disponível para análise"}
            
        # Análise da leitura mais recente
        leitura_recente = max(leituras, key=lambda x: x.get("data_leitura", ""))
        analise_atual = self.analisar_leitura_individual(leitura_recente, cultivo)
        
        # Análise histórica
        analise_historica = self.analisar_historico(leituras, cultivo)
        
        # Recomendações específicas para o cultivo
        recomendacoes_cultivo = self._get_recomendacoes_cultivo(cultivo, analise_atual)
        
        return {
            "usuario": {
                "nome": usuario_data.get("nome", ""),
                "fazenda": usuario_data.get("nome_fazenda", ""),
                "cultivo_principal": cultivo
            },
            "analise_atual": analise_atual,
            "analise_historica": analise_historica,
            "recomendacoes_cultivo": recomendacoes_cultivo,
            "data_relatorio": datetime.now().isoformat()
        }
    
    def _get_recomendacoes_cultivo(self, cultivo: str, analise_atual: Dict) -> List[str]:
        """Retorna recomendações específicas para o tipo de cultivo."""
        recomendacoes = {
            "Soja": [
                "Monitorar nodulação para fixação de nitrogênio",
                "Atenção especial ao pH para absorção de nutrientes",
                "Controlar umidade durante floração"
            ],
            "Milho": [
                "Alta demanda de nitrogênio durante crescimento",
                "Manter umidade constante durante polinização",
                "Monitorar potássio para desenvolvimento de grãos"
            ],
            "Café": [
                "pH ligeiramente ácido favorece absorção de nutrientes",
                "Evitar encharcamento das raízes",
                "Matéria orgânica essencial para qualidade"
            ]
        }
        
        return recomendacoes.get(cultivo, recomendacoes["Soja"])