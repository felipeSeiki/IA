# WorkTree AI - Análise de Compatibilidade com IA Generativa

**Global Solution FIAP - 2º Semestre 2024**

**Equipe 2TDSPY:**
- Felipe Seiki Hashiguti - RM: 98985
- Lucas Corradini Silveira - RM: 555118  
- Matheus Gregorio Mota - RM: 557254

---

## 🎯 Sobre o Projeto

Sistema de análise inteligente de compatibilidade entre candidatos e vagas utilizando **Google Gemini 2.0 Flash**.

**Principais recursos:**
- 🤖 Análise semântica de habilidades e experiências
- 📊 Score de compatibilidade (0-100)
- 💡 Recomendações personalizadas de desenvolvimento
- 🚀 API REST pronta para integração

---

## 🚀 Como Usar

### Opção 1: Google Colab (Demonstração)

Ideal para testes e apresentações acadêmicas.

1. Acesse: https://colab.research.google.com/
2. Faça upload do `WorkTree_IA_Compatibility_Analysis.ipynb`
3. Obtenha API Key: https://makersuite.google.com/app/apikey
4. Configure a chave na primeira célula
5. Execute: **Runtime → Run all**

### Opção 2: API REST (Produção)

API Flask integrada com React Native mobile app.

#### 📦 Instalação Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar API Key
export GOOGLE_API_KEY="sua-chave-aqui"

# Executar API
python app.py
```

#### 📡 Endpoints

**Health Check**
```bash
GET /api/health
```

**Análise de Compatibilidade**
```bash
POST /api/analyze-compatibility

Body:
{
  "candidate": {
    "id": "c1",
    "name": "João Silva",
    "title": "Desenvolvedor Python",
    "experience_years": 5,
    "skills": ["Python", "JavaScript", "SQL"]
  },
  "job": {
    "id": "j1",
    "title": "Desenvolvedor Full Stack",
    "company": "Tech Corp",
    "required_skills": ["Python", "JavaScript", "React"],
    "salary": "R$ 10.000"
  }
}
```

**Resposta:**
```json
{
  "compatibility_score": 85,
  "match_level": "Excelente",
  "key_strengths": ["Python", "JavaScript"],
  "missing_skills": ["React"],
  "recommendations": [...],
  "metadata": {...}
}
```

---

## 🌐 Deploy

### Render (Recomendado)

1. Faça push do código no GitHub
2. Acesse: https://render.com
3. New → Web Service
4. Conecte seu repositório
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment Variable:** `GOOGLE_API_KEY` = sua chave
6. Deploy!

**URL de produção:** https://ia-8xoy.onrender.com

---

## 🤖 Tecnologias

- **Python 3.11+**
- **Flask 3.0** - Framework web
- **Google Gemini 2.0 Flash** - Modelo de IA generativa
- **Gunicorn** - WSGI server para produção
- **REST API** - Integração HTTP

---

## 📊 Estrutura do Projeto

```
IA/
├── WorkTree_IA_Compatibility_Analysis.ipynb  # Notebook para demonstração
├── app.py                                    # API Flask (168 linhas)
├── requirements.txt                          # Dependências Python
├── Procfile                                  # Config para deploy
├── ROTEIRO_VIDEO_API.md                      # Script para apresentação
└── README.md                                 # Este arquivo
```

---

## 📱 Integração com Mobile

Repositório: https://github.com/felipeSeiki/GS2-Mobile

O app React Native consome a API para análise em tempo real:

```javascript
const response = await fetch('https://ia-8xoy.onrender.com/api/analyze-compatibility', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({ candidate, job })
});

const analysis = await response.json();
console.log(`Score: ${analysis.compatibility_score}%`);
```

---

## 🎓 Destaques Acadêmicos

✅ **IA Generativa:** Google Gemini 2.0 Flash (modelo transformer)  
✅ **Prompt Engineering:** Prompts estruturados para análise de RH  
✅ **API REST:** Arquitetura profissional com Flask  
✅ **Deploy em Produção:** Aplicação funcionando em cloud  
✅ **Integração Real:** Conectado com projeto Mobile  
✅ **Documentação Completa:** Código limpo e documentado

---

## 📝 Requisitos de Entrega

✅ Código funcional (Notebook + API)  
✅ IA Generativa integrada  
✅ Prompt Engineering aplicado  
✅ Deep Learning (Transformer)  
✅ Análise e processamento de dados  
✅ Documentação técnica  
✅ Instruções de deploy

---

**Desenvolvido para FIAP Global Solution 2024 - 2TDSPY**

