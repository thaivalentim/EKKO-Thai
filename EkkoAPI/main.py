from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from EkkoAPI.profile_management import router as profile_router
from EkkoAPI.soil_readings import router as soil_router
from EkkoAPI.soil_analysis import SoilAnalysisAI
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from pymongo import MongoClient
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "EKKO_database")

if not MONGO_URI:
    raise ValueError("MONGO_URI não encontrada no arquivo .env")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    db = client[MONGO_DB_NAME]
    usuarios_collection = db["usuarios"]
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
    raise

app = FastAPI(title="API Ekko")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(profile_router)
app.include_router(soil_router)

soil_ai = SoilAnalysisAI()

def serialize_user(user) -> dict:
    user["_id"] = str(user["_id"])
    return user

class Usuario(BaseModel):
    nome: str = Field(..., min_length=1)
    email: EmailStr
    papel: str = Field(..., min_length=1)

@app.get("/")
def root():
    return {"mensagem": "API Ekko está online!"}

@app.get("/usuarios", response_model=List[dict])
def listar_usuarios():
    try:
        usuarios = list(usuarios_collection.find())
        return [serialize_user(u) for u in usuarios]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar usuários: {str(e)}")

@app.post("/usuarios", response_model=dict)
def criar_usuario(usuario: Usuario):
    try:
        novo = usuario.dict()
        result = usuarios_collection.insert_one(novo)
        novo["_id"] = str(result.inserted_id)
        return novo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar usuário: {str(e)}")

@app.get("/usuarios/{usuario_id}", response_model=dict)
def obter_usuario(usuario_id: str):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return serialize_user(usuario)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter usuário: {str(e)}")

@app.get("/diagnostico/{usuario_id}", response_model=dict)
def obter_diagnostico_solo(usuario_id: str):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        soil_collection = db["leituras_solo"]
        leituras = list(soil_collection.find({"usuario_id": ObjectId(usuario_id)}).sort("data_leitura", -1))
        
        for leitura in leituras:
            leitura["_id"] = str(leitura["_id"])
            leitura["usuario_id"] = str(leitura["usuario_id"])
        
        usuario_data = serialize_user(usuario)
        usuario_data["leituras_solo"] = leituras
        
        diagnostico = soil_ai.gerar_relatorio_completo(usuario_data)
        return diagnostico
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar diagnóstico: {str(e)}")

@app.get("/analise-rapida/{usuario_id}", response_model=dict)
def analise_rapida_solo(usuario_id: str):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        soil_collection = db["leituras_solo"]
        ultima_leitura = soil_collection.find_one(
            {"usuario_id": ObjectId(usuario_id)}, 
            sort=[("data_leitura", -1)]
        )
        
        if not ultima_leitura:
            raise HTTPException(status_code=404, detail="Nenhuma leitura encontrada")
        
        cultivo = usuario.get("propriedade", {}).get("cultivo_principal", "Soja")
        analise = soil_ai.analisar_leitura_individual(ultima_leitura, cultivo)
        
        return {
            "usuario": usuario.get("nome", ""),
            "fazenda": usuario.get("nome_fazenda", ""),
            "cultivo": cultivo,
            "analise": analise,
            "leitura_data": ultima_leitura.get("data_leitura")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na análise rápida: {str(e)}")