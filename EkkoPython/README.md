# 🎲 EkkoPython - Gerador de Dados

Módulo para geração de dados realistas de teste para o sistema EKKO.

## 🚀 Uso

```bash
python EkkoPython/dataGenerator.py
```

## 📊 Dados Gerados

### Usuários (5 por padrão)
- **Pessoais**: Nome, email, CPF, telefone, nascimento
- **Fazenda**: Nome, localização (8 regiões do Brasil)
- **Propriedade**: Área, cultivos, tipo de solo, irrigação
- **Técnicos**: Experiência, tecnologia, certificações

### Leituras de Solo (7 dias histórico + 10 contínuas)
- **Básicos**: pH, umidade, temperatura
- **Avançados**: Condutividade, salinidade, densidade
- **Nutrientes**: NPK (N, P, K) + micronutrientes
- **Sensores**: Qualidade sinal, bateria, localização

## 🌾 Cultivos Suportados

Soja, Milho, Café, Cana-de-açúcar, Algodão, Feijão, Arroz, Trigo, Tomate, Batata

## ⚙️ Configuração

- `QUANTIDADE_USUARIOS = 5` - Número de usuários
- `NUM_ITERACOES_SENSOR = 10` - Leituras contínuas
- `INTERVALO_ENVIO_SEGUNDOS = 5` - Intervalo entre leituras

## 🎯 Características

- **Dados Realistas**: Baseados em parâmetros agronômicos
- **Variação Natural**: Flutuações suaves entre leituras
- **Localização BR**: Regiões agrícolas brasileiras
- **Performance**: Inserção em lote no MongoDB

## ✅ **Testado & Validado**

- Estrutura de dados validada
- Valores dentro de faixas realistas
- Compatibilidade com frontend
- Geração contínua funcional