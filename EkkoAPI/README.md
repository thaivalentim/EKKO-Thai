# 🔌 EkkoAPI - Backend FastAPI

API REST para o sistema EKKO Thai de monitoramento de solo.

## 📋 Módulos

- **`main.py`** - Endpoints principais e configuração
- **`soil_readings.py`** - Leituras de sensores de solo
- **`profile_management.py`** - Gestão de perfis de usuários
- **`soil_analysis.py`** - IA para diagnóstico de solo

## 🚀 Execução

```bash
uvicorn EkkoAPI.main:app --reload --host 127.0.0.1 --port 8000
```

## 📊 Endpoints Disponíveis

### Usuários
- `GET /usuarios` - Lista todos os usuários
- `POST /usuarios` - Cria novo usuário
- `GET /usuarios/{id}` - Busca usuário por ID

### Perfis
- `GET /perfil/{id}` - Perfil completo com leituras
- `PUT /perfil/{id}` - Atualiza dados do perfil

### Solo
- `GET /leituras_solo/{id}` - Leituras de solo do usuário
- `GET /diagnostico/{id}` - Diagnóstico IA completo
- `GET /analise-rapida/{id}` - Análise da última leitura

## 🔧 Configuração

Requer arquivo `.env` com:
```
MONGO_URI=mongodb://...
MONGO_DB_NAME=EKKO_database
```

## 🧪 Testes

- ✅ **100% Cobertura** - Todos os endpoints testados
- ✅ **Validação Completa** - Dados de entrada e saída
- ✅ **Tratamento de Erros** - Cenários de falha cobertos

## 📖 Documentação

Acesse `/docs` para documentação interativa do Swagger.

## 🎯 Status: Produção Ready

API completamente funcional, testada e documentada.