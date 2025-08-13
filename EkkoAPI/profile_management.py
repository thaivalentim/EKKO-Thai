from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from typing import Optional
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "EKKO_database")

if not MONGO_URI:
    raise ValueError("MONGO_URI não encontrada no arquivo .env")

try:
    client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
    # Teste de conexão opcional - não bloqueia a inicialização
    try:
        client.admin.command('ping')
        print("✅ MongoDB conectado com sucesso")
    except Exception as ping_error:
        print(f"⚠️ Aviso: Problema na conexão MongoDB: {ping_error}")
        print("API iniciará mesmo assim - conexão será testada nas requisições")
    
    db = client[MONGO_DB_NAME]
    usuarios_collection = db["usuarios"]
except Exception as e:
    print(f"❌ Erro crítico ao configurar MongoDB: {e}")
    # Não levanta exceção para permitir que a API inicie
    client = None
    db = None
    usuarios_collection = None

router = APIRouter()

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1)
    email: Optional[EmailStr] = None
    papel: Optional[str] = Field(None, min_length=1)

def serialize_user(user) -> dict:
    user["_id"] = str(user["_id"])
    return user

@router.get("/perfil/{usuario_id}")
def visualizar_perfil(usuario_id: str):
    if not client:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível")
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        perfil = serialize_user(usuario)

        soil_collection = db["leituras_solo"]
        leituras = list(soil_collection.find({"usuario_id": ObjectId(usuario_id)}).sort("data_leitura", -1).limit(50))
        
        for leitura in leituras:
            leitura["_id"] = str(leitura["_id"])
            leitura["usuario_id"] = str(leitura["usuario_id"])
            
            timestamp = leitura.get("timestamp") or leitura.get("data_leitura")
            if timestamp and hasattr(timestamp, "isoformat"):
                leitura["data_leitura"] = timestamp.isoformat()
            elif isinstance(timestamp, str):
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    leitura["data_leitura"] = dt.isoformat()
                except ValueError:
                    leitura["data_leitura"] = str(timestamp)
            else:
                leitura["data_leitura"] = ""
            
            leitura["umidade"] = leitura.get("umidade", 0)
            leitura["temperatura"] = leitura.get("temperatura", 0)
            leitura["ph"] = leitura.get("pH", leitura.get("ph", 0))
            leitura["condutividade_eletrica"] = leitura.get("condutividade_eletrica", 0)
            leitura["dispositivo"] = leitura.get("dispositivo", "")
            leitura["salinidade"] = leitura.get("salinidade", 0)
            leitura["NPK"] = leitura.get("NPK", {})

        perfil["leituras_solo"] = leituras
        return perfil
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter perfil: {str(e)}")

@router.put("/perfil/{usuario_id}")
def atualizar_perfil(usuario_id: str, dados: UsuarioUpdate):
    if not client:
        raise HTTPException(status_code=503, detail="Banco de dados indisponível")
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")
        
        update_data = {k: v for k, v in dados.dict().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="Nenhum dado para atualizar")
        
        result = usuarios_collection.update_one({"_id": ObjectId(usuario_id)}, {"$set": update_data})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        usuario = usuarios_collection.find_one({"_id": ObjectId(usuario_id)})
        return serialize_user(usuario)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar perfil: {str(e)}")