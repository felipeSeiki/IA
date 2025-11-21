# WorkTree AI - Análise de Compatibilidade com IA Generativa

**Global Solution FIAP - 2º Semestre 2024**

**Equipe 2TDSPY:**
- Felipe Seiki Hashiguti - RM: 98985
- Lucas Corradini Silveira - RM: 555118  
- Matheus Gregorio Mota - RM: 557254

---

## 🎯 Duas Formas de Usar

### 1️⃣ Google Colab (Recomendado para Avaliação Acadêmica)

**Vantagens:**
- ✅ Execução imediata sem instalação
- ✅ Visualizações interativas
- ✅ Ambiente pré-configurado
- ✅ Ideal para demonstração

**Como usar:**
1. Acesse: https://colab.research.google.com/
2. Faça upload do `WorkTree_IA_Compatibility_Analysis.ipynb`
3. Obtenha API Key gratuita: https://makersuite.google.com/app/apikey
4. Configure a API Key na primeira célula
5. Execute: **Runtime → Run all**

---

### 2️⃣ API REST Python (Deploy para Integração com Mobile/Web)

**Vantagens:**
- ✅ **Integração com outros projetos** (Mobile, Web, Backend)
- ✅ **Processamento assíncrono** (até 50 candidatos em paralelo)
- ✅ **Pronto para deploy** em Render/Heroku/Railway
- ✅ **Endpoints REST profissionais**

#### 🚀 Instalação Local

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar API Key
cp .env.example .env
# Edite .env e adicione sua GOOGLE_API_KEY

# 3. Executar API
python app.py
```

#### 📡 Endpoints Disponíveis

```bash
# Health Check
GET http://localhost:5000/health

# Análise Individual
POST http://localhost:5000/api/analyze-compatibility
{
  "candidate": {...},
  "job": {...}
}

# Análise em Lote (até 50 candidatos em paralelo)
POST http://localhost:5000/api/batch-analyze
{
  "job": {...},
  "candidates": [...]
}
```

#### 🌐 Deploy (5 minutos)

Siga o guia completo em **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)**

**Resumo:**
1. Push do código no GitHub
2. Conecte repositório no Render
3. Configure `GOOGLE_API_KEY` nas variáveis de ambiente
4. Deploy automático!

Sua API estará em: `https://worktree-ia.onrender.com`

#### 📱 Exemplo de Integração (JavaScript/React Native)

```javascript
// Análise em lote assíncrona
async function analyzeCandidates(job, candidates) {
  const response = await fetch('https://worktree-ia.onrender.com/api/batch-analyze', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ job, candidates })
  });
  
  const data = await response.json();
  console.log(`${data.successful_analyses} candidatos analisados!`);
  
  // Resultados já ordenados por score (maior primeiro)
  return data.results;
}
```

---

## 🚀 Funcionalidades

### IA Generativa (Google Gemini 1.5 Flash)
- **Prompt Engineering** otimizado para RH (2000+ tokens)
- **Análise semântica** de habilidades e experiências
- **Score de compatibilidade** (0-100)
- **Recomendações personalizadas**

### Processamento Assíncrono (API)
- **Thread Pool** com 10 workers
- **Análise paralela** de múltiplos candidatos
- **10x mais rápido** que processamento sequencial
- **Escalável** para alta demanda

### Visualizações (Notebook)
- Gráficos de compatibilidade
- Heatmaps de habilidades
- Ranking de candidatos

---

## 📋 Requisitos de Entrega Atendidos

✅ **Código Funcional:** Notebook + API REST  
✅ **IA Generativa:** Google Gemini integrado  
✅ **Prompt Engineering:** Prompts estruturados e otimizados  
✅ **Deep Learning:** Transformer (Gemini 1.5 Flash)  
✅ **Análise de Dados:** Processamento e visualização  
✅ **Documentação:** README + Guia de Deploy  
✅ **Deploy:** Instruções completas para produção

---

## 📊 Estrutura do Projeto

```
IA/
├── WorkTree_IA_Compatibility_Analysis.ipynb  # Notebook completo
├── app.py                                    # API Flask
├── requirements.txt                          # Dependências
├── Procfile                                  # Config deploy
├── DEPLOY_GUIDE.md                           # Guia de deploy completo
├── README.md                                 # Este arquivo
└── .env.example                              # Template de variáveis
```

---

## 🎓 Para Avaliadores

**Recomendamos testar no Google Colab primeiro** para uma experiência completa com visualizações.

A **API REST demonstra capacidade de integração real** com o projeto Mobile (React Native) e outros sistemas.

**Ambas as implementações compartilham a mesma lógica de IA e Prompt Engineering.**

---

## 📚 Documentação

- **[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)** - Deploy completo (Render/Heroku/Railway)
- **Notebook** - Documentação inline em Markdown
- **API** - Docstrings em todas as funções

---

## 🔗 Integração com Projeto Mobile

Repositório Mobile: https://github.com/felipeSeiki/GS2-Mobile

A API foi desenvolvida para **integração direta com o app React Native**, permitindo:
- Análise em tempo real de candidatos
- Processamento em lote para ranking
- Requisições assíncronas do mobile

---

**Desenvolvido para FIAP Global Solution 2024 - 2TDSPY**

