import random
import time
from datetime import datetime, timedelta, timezone
from pymongo import MongoClient
from faker import Faker
import re
import os
from dotenv import load_dotenv

# 🔧 CONFIGURAÇÕES
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
NOME_DB = os.getenv("MONGO_DB_NAME", "EKKO_database")

if not MONGO_URI:
    raise ValueError("MONGO_URI não encontrada no arquivo .env")
QUANTIDADE_USUARIOS = 5
INTERVALO_ENVIO_SEGUNDOS = 5
NUM_ITERACOES_SENSOR = 10
NUM_ANALISES_HISTORICAS = 10 

fake = Faker('pt_BR')

# 🌱 DADOS REALISTAS PARA AGRICULTURA
TIPOS_CULTIVO = [
    "Soja", "Milho", "Café", "Cana-de-açúcar", "Algodão", 
    "Feijão", "Arroz", "Trigo", "Tomate", "Batata"
]

REGIOES_BRASIL = [
    {"estado": "São Paulo", "cidade": "Ribeirão Preto", "regiao": "Sudeste"},
    {"estado": "Minas Gerais", "cidade": "Uberlândia", "regiao": "Sudeste"},
    {"estado": "Mato Grosso", "cidade": "Sorriso", "regiao": "Centro-Oeste"},
    {"estado": "Goiás", "cidade": "Rio Verde", "regiao": "Centro-Oeste"},
    {"estado": "Paraná", "cidade": "Cascavel", "regiao": "Sul"},
    {"estado": "Rio Grande do Sul", "cidade": "Passo Fundo", "regiao": "Sul"},
    {"estado": "Bahia", "cidade": "Barreiras", "regiao": "Nordeste"},
    {"estado": "Maranhão", "cidade": "Balsas", "regiao": "Nordeste"}
]

def conectar_mongo(uri, nome_db):
    client = None
    try:
        client = MongoClient(uri)
        client.admin.command('ping')
        print("✅ Conexão com o MongoDB estabelecida.")
        return client[nome_db]
    except Exception as e:
        print(f"❌ Erro ao conectar com o MongoDB: {e}")
        if client:
            client.close()
        raise

def gerar_usuario_fake():
    """Gera dados fictícios realistas de usuário agricultor."""
    nome_completo = fake.name()
    primeiro_nome = nome_completo.split()[0].lower()
    
    # Remover acentos para email
    email_nome = re.sub(r'[àáâãäå]', 'a', primeiro_nome)
    email_nome = re.sub(r'[èéêë]', 'e', email_nome)
    email_nome = re.sub(r'[ìíîï]', 'i', email_nome)
    email_nome = re.sub(r'[òóôõö]', 'o', email_nome)
    email_nome = re.sub(r'[ùúûü]', 'u', email_nome)
    email_nome = re.sub(r'[ç]', 'c', email_nome)
    
    localizacao = random.choice(REGIOES_BRASIL)
    cultivo_principal = random.choice(TIPOS_CULTIVO)
    
    return {
        "nome": nome_completo,
        "email": f"{email_nome}.{random.randint(100, 999)}@fazenda.com.br",
        "senha_hash": fake.sha256(),
        "papel": "agricultor",
        "cpf": fake.cpf(),
        "telefone": fake.phone_number(),
        "data_nascimento": fake.date_of_birth(minimum_age=25, maximum_age=70).isoformat(),
        "nome_fazenda": f"Fazenda {fake.last_name()}",
        "localizacao": {
            "endereco": fake.street_address(),
            "cidade": localizacao["cidade"],
            "estado": localizacao["estado"],
            "regiao": localizacao["regiao"],
            "cep": fake.postcode(),
            "coordenadas": {
                "latitude": float(fake.latitude()),
                "longitude": float(fake.longitude())
            }
        },
        "propriedade": {
            "area_total_hectares": round(random.uniform(50, 2000), 2),
            "area_cultivada_hectares": round(random.uniform(30, 1500), 2),
            "cultivo_principal": cultivo_principal,
            "cultivos_secundarios": random.sample([c for c in TIPOS_CULTIVO if c != cultivo_principal], random.randint(1, 3)),
            "tipo_solo": random.choice(["Latossolo", "Argissolo", "Neossolo", "Cambissolo", "Gleissolo"]),
            "sistema_irrigacao": random.choice(["Gotejamento", "Aspersão", "Pivô Central", "Sulcos", "Sem irrigação"])
        },
        "dados_tecnicos": {
            "experiencia_anos": random.randint(5, 40),
            "nivel_tecnologia": random.choice(["Básico", "Intermediário", "Avançado"]),
            "certificacoes": random.sample(["Orgânico", "Rainforest", "UTZ", "Fair Trade"], random.randint(0, 2))
        },
        "data_cadastro": datetime.now(timezone.utc),
        "status": "ativo"
    }

def gerar_leitura_solo_fake(usuario_id, cultivo_tipo="Soja"):
    """Gera leitura de solo com valores realistas baseados no tipo de cultivo."""
    
    # Valores ideais por tipo de cultivo
    parametros_cultivo = {
        "Soja": {"ph": (6.0, 7.0), "umidade": (60, 80), "temp": (20, 30)},
        "Milho": {"ph": (5.8, 7.0), "umidade": (65, 85), "temp": (18, 32)},
        "Café": {"ph": (5.5, 6.5), "umidade": (55, 75), "temp": (18, 25)},
        "Cana-de-açúcar": {"ph": (5.0, 6.5), "umidade": (70, 90), "temp": (22, 35)}
    }
    
    params = parametros_cultivo.get(cultivo_tipo, parametros_cultivo["Soja"])
    
    # Adicionar variação natural (+/- 15%)
    ph_base = random.uniform(*params["ph"])
    umidade_base = random.uniform(*params["umidade"])
    temp_base = random.uniform(*params["temp"])
    
    # Variação sazonal/diária
    variacao = random.uniform(0.85, 1.15)
    
    return {
        "usuario_id": usuario_id,
        "dispositivo": f"EKKO-Sensor-{random.randint(1000, 9999)}",
        "localizacao_sensor": {
            "setor": f"Setor {random.choice(['A', 'B', 'C', 'D'])}",
            "profundidade_cm": random.choice([10, 20, 30])
        },
        "umidade": round(max(10, min(100, umidade_base * variacao)), 2),
        "temperatura": round(max(5, min(45, temp_base * variacao)), 2),
        "pH": round(max(3.0, min(9.0, ph_base * variacao)), 2),
        "condutividade_eletrica": round(random.uniform(0.2, 3.5), 2),
        "salinidade": round(random.uniform(0.1, 2.0), 2),
        "NPK": {
            "nitrogenio": round(random.uniform(10, 150), 1),
            "fosforo": round(random.uniform(5, 80), 1),
            "potassio": round(random.uniform(20, 200), 1)
        },
        "micronutrientes": {
            "calcio": round(random.uniform(200, 2000), 1),
            "magnesio": round(random.uniform(50, 500), 1),
            "enxofre": round(random.uniform(5, 50), 1)
        },
        "materia_organica_pct": round(random.uniform(1.5, 6.0), 2),
        "densidade_solo": round(random.uniform(1.1, 1.6), 2),
        "data_leitura": datetime.now(timezone.utc),
        "qualidade_sinal": random.choice(["Excelente", "Boa", "Regular"]),
        "bateria_sensor_pct": random.randint(20, 100)
    }

def gerar_dado_sensor_continuo(usuario_id, ultimo_dado=None, cultivo_tipo="Soja"):
    """Gera leituras contínuas com variações suaves e realistas."""
    def variar(valor, min_, max_, delta=0.8):
        novo = valor + random.uniform(-delta, delta)
        return round(max(min_, min(max_, novo)), 2)
    
    if not ultimo_dado:
        return gerar_leitura_solo_fake(usuario_id, cultivo_tipo)

    # Manter estrutura NPK como objeto
    npk_anterior = ultimo_dado.get("NPK", {"nitrogenio": 50, "fosforo": 30, "potassio": 100})
    if isinstance(npk_anterior, (int, float)):
        npk_anterior = {"nitrogenio": 50, "fosforo": 30, "potassio": 100}

    return {
        "usuario_id": usuario_id,
        "dispositivo": ultimo_dado.get("dispositivo", "EKKO-Sensor-1000"),
        "localizacao_sensor": ultimo_dado.get("localizacao_sensor", {"setor": "Setor A", "profundidade_cm": 20}),
        "umidade": variar(ultimo_dado["umidade"], 10, 95, 2.0),
        "temperatura": variar(ultimo_dado["temperatura"], 5, 45, 1.5),
        "pH": variar(ultimo_dado["pH"], 3.0, 9.0, 0.2),
        "condutividade_eletrica": variar(ultimo_dado["condutividade_eletrica"], 0.1, 4.0, 0.1),
        "salinidade": variar(ultimo_dado["salinidade"], 0.1, 3.0, 0.1),
        "NPK": {
            "nitrogenio": variar(npk_anterior["nitrogenio"], 5, 200, 5),
            "fosforo": variar(npk_anterior["fosforo"], 2, 100, 3),
            "potassio": variar(npk_anterior["potassio"], 10, 300, 8)
        },
        "micronutrientes": ultimo_dado.get("micronutrientes", {"calcio": 500, "magnesio": 150, "enxofre": 20}),
        "materia_organica_pct": variar(ultimo_dado.get("materia_organica_pct", 3.0), 1.0, 8.0, 0.1),
        "densidade_solo": ultimo_dado.get("densidade_solo", 1.3),
        "data_leitura": datetime.now(timezone.utc),
        "qualidade_sinal": random.choice(["Excelente", "Boa", "Regular"]),
        "bateria_sensor_pct": max(10, ultimo_dado.get("bateria_sensor_pct", 100) - random.randint(0, 2))
    }

def simular_dados_continuos(db, usuario_id, cultivo_tipo="Soja"):
    """Envia leituras contínuas simuladas de sensores para um usuário."""
    print(f"📡 Iniciando simulação de {NUM_ITERACOES_SENSOR} leituras contínuas...")
    ultimo = gerar_leitura_solo_fake(usuario_id, cultivo_tipo)
    dados_batch = []
    
    for i in range(NUM_ITERACOES_SENSOR):
        dado = gerar_dado_sensor_continuo(usuario_id, ultimo, cultivo_tipo)
        dados_batch.append(dado)
        ultimo = dado
        
        # Status mais detalhado
        status_ph = "🟢" if 6.0 <= dado["pH"] <= 7.0 else "🟡" if 5.5 <= dado["pH"] <= 7.5 else "🔴"
        status_umidade = "🟢" if 60 <= dado["umidade"] <= 80 else "🟡" if 40 <= dado["umidade"] <= 90 else "🔴"
        
        print(f"[{i+1}/{NUM_ITERACOES_SENSOR}] 🌱 pH: {dado['pH']:.1f} {status_ph} | Umidade: {dado['umidade']:.1f}% {status_umidade}")
        time.sleep(INTERVALO_ENVIO_SEGUNDOS)
    
    # Inserção em lote para melhor performance
    if dados_batch:
        db.leituras_solo.insert_many(dados_batch)
        print(f"✅ {len(dados_batch)} leituras inseridas com sucesso")

def main():
    db = conectar_mongo(MONGO_URI, NOME_DB)
    usuarios_ids = []

    print("🌱 Iniciando geração de dados realistas do EKKO...\n")

    for i in range(QUANTIDADE_USUARIOS):
        usuario = gerar_usuario_fake()
        usuario_id = db.usuarios.insert_one(usuario).inserted_id
        usuarios_ids.append(usuario_id)
        
        cultivo = usuario["propriedade"]["cultivo_principal"]
        print(f"👤 Usuário {i+1}: {usuario['nome']} - {usuario['nome_fazenda']}")
        print(f"   📍 {usuario['localizacao']['cidade']}/{usuario['localizacao']['estado']}")
        print(f"   🌾 Cultivo: {cultivo} - {usuario['propriedade']['area_total_hectares']}ha")

        # Gerar leituras históricas (últimos 7 dias)
        dados_historicos = []
        for j in range(7):
            leitura = gerar_leitura_solo_fake(usuario_id, cultivo)
            # Usar timedelta para calcular datas anteriores
            leitura["data_leitura"] = datetime.now(timezone.utc) - timedelta(
                days=j,
                hours=random.randint(0, 12),
                minutes=random.randint(0, 59)
            )
            dados_historicos.append(leitura)
        
        if dados_historicos:
            db.leituras_solo.insert_many(dados_historicos)
            print(f"   ✅ 7 leituras históricas inseridas\n")

    print(f"🌿 Simulação concluída: {QUANTIDADE_USUARIOS} usuários com dados realistas.")
    print(f"📊 Total de leituras: {QUANTIDADE_USUARIOS * 7}")
    
    # Simular dados contínuos para o primeiro usuário
    if usuarios_ids:
        primeiro_usuario = db.usuarios.find_one({"_id": usuarios_ids[0]})
        cultivo_principal = primeiro_usuario["propriedade"]["cultivo_principal"]
        print(f"\n🔄 Iniciando simulação contínua para {primeiro_usuario['nome']} ({cultivo_principal})...")
        simular_dados_continuos(db, usuarios_ids[0], cultivo_principal)

if __name__ == "__main__":
    main()