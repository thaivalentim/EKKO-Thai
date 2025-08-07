# 🎨 Frontend - Interface Web Completa

Dashboard responsivo com visualização completa de todos os dados do sistema EKKO Thai.

## 🚀 Uso

1. Inicie a API: `python start_api.py`
2. Abra `frontend/index.html` no navegador
3. Digite um ID de usuário para ver todos os dados

## ✅ Funcionalidades Completas

### 👤 **Dados Pessoais Completos**
- Nome, email, função
- CPF, telefone, data nascimento
- Dados técnicos (experiência, tecnologia, certificações)

### 🏢 **Propriedade Detalhada**
- Nome da fazenda
- Localização completa (cidade, estado, região)
- Cultivo principal e área total

### 📊 **Leituras de Solo (13 Parâmetros)**
- **Básicos**: pH, umidade, temperatura
- **Avançados**: Condutividade, salinidade
- **Nutrientes**: NPK (Nitrogênio, Fósforo, Potássio)
- **Micronutrientes**: Cálcio, Magnésio, Enxofre
- **Propriedades**: Matéria orgânica, densidade
- **Sensores**: Qualidade sinal, bateria, localização

### 🤖 **IA & Diagnóstico**
- Status visual com cores (verde/amarelo/vermelho)
- Diagnósticos automáticos
- Sugestões personalizadas
- Score de qualidade do solo

## 🎨 **Design & UX**

- **Layout Responsivo**: Grid adaptativo para qualquer tela
- **Cards Organizados**: 4 seções de dados
- **Tabela Completa**: 13 colunas com todos os parâmetros
- **Indicadores Visuais**: Cores baseadas em faixas ideais
- **Animações Suaves**: Transições e loading states

## 📱 **Responsividade**

- Desktop: Grid 2x2 para cards
- Tablet: Grid adaptativo
- Mobile: Cards empilhados
- Tabela: Scroll horizontal

## 🔌 **Integração API**

- `GET /perfil/{id}` - Dados completos do usuário
- `GET /diagnostico/{id}` - Análise IA
- `PUT /perfil/{id}` - Atualização de dados
- Tratamento completo de erros

## 🎯 **100% dos Dados Exibidos**

Todos os campos gerados pelo `dataGenerator.py` são exibidos:
- ✅ Dados pessoais e técnicos
- ✅ Propriedade e localização
- ✅ Todas as 13 métricas de solo
- ✅ Status e diagnósticos IA