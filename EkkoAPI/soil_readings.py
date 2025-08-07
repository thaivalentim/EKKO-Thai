from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
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
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    db = client[MONGO_DB_NAME]
    soil_collection = db["leituras_solo"]
except Exception as e:
    print(f"Erro ao conectar com MongoDB: {e}")
    raise

router = APIRouter()

class LeituraSolo(BaseModel):
    data_leitura: str
    ph: float = Field(0, ge=0)
    umidade: float = Field(..., ge=0)
    temperatura: float = Field(...)
    dispositivo: str = ""
    condutividade_eletrica: float = 0
    salinidade: float = 0
    NPK: dict = {}

def serialize_soil_reading(reading) -> dict:
    reading["_id"] = str(reading["_id"])
    reading["usuario_id"] = str(reading.get("usuario_id", ""))

    timestamp = reading.get("timestamp") or reading.get("data_leitura")
    if timestamp and hasattr(timestamp, "isoformat"):
        reading["data_leitura"] = timestamp.isoformat()
    elif isinstance(timestamp, str):
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            reading["data_leitura"] = dt.isoformat()
        except ValueError:
            reading["data_leitura"] = str(timestamp)
    else:
        reading["data_leitura"] = ""

    reading["dispositivo"] = reading.get("dispositivo", "")
    reading["umidade"] = reading.get("umidade", 0)
    reading["temperatura"] = reading.get("temperatura", 0)
    reading["ph"] = reading.get("pH", reading.get("ph", 0))
    reading["condutividade_eletrica"] = reading.get("condutividade_eletrica", 0)
    reading["salinidade"] = reading.get("salinidade", 0)
    reading["NPK"] = reading.get("NPK", {})
    return reading

@router.get("/leituras_solo/{usuario_id}")
def obter_leituras_solo(usuario_id: str):
    try:
        if not ObjectId.is_valid(usuario_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        leituras = list(soil_collection.find({"usuario_id": ObjectId(usuario_id)}).sort("data_leitura", -1))
        return [serialize_soil_reading(l) for l in leituras]

    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro interno: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@router.get("/leituras_solo")
def obter_todas_leituras_solo():
    try:
        leituras = list(soil_collection.find().sort("data_leitura", -1))
        return [serialize_soil_reading(l) for l in leituras]
    except Exception as e:
        print(f"Erro interno: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")