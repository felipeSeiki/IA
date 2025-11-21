# 🌳 WorkTree AI - Sistema de Análise de Compatibilidade

**Global Solution - 2º Semestre FIAP**  
**Disciplina: DISRUPTIVE ARCHITECTURES: IOT, IOB & GENERATIVE IA**

---

## 👥 Equipe - 2TDSPY
- **Felipe Seiki Hashiguti** - RM: 98985
- **Lucas Corradini Silveira** - RM: 555118  
- **Matheus Gregorio Mota** - RM: 557254

---

## 📋 Sobre o Projeto

Sistema inteligente de **análise de compatibilidade candidato-vaga** usando **IA Generativa (Google Gemini API)** integrado ao aplicativo mobile WorkTree.

### 🎯 Funcionalidade Principal

Quando um candidato acessa uma vaga no app mobile, a IA analisa automaticamente a compatibilidade e fornece:

- ✅ **Score de Compatibilidade** (0-100%)
- ✅ **Habilidades Compatíveis** vs. Habilidades a Desenvolver
- ✅ **Pontos Fortes** do candidato
- ✅ **Recomendações Personalizadas** de cursos/certificações
- ✅ **Análise de Experiência** e expectativa salarial
- ✅ **Próximos Passos** acionáveis

---

## 🤖 Tecnologias

- **Google Gemini API** (gemini-1.5-flash) - IA Generativa
- **Python** 3.10+ - Backend
- **Flask** + **Flask-CORS** - REST API
- **Prompt Engineering** - Otimização de análises
- **Pandas, Matplotlib, Seaborn** - Análise de dados e visualizações

---

## 📁 Estrutura do Projeto

```
IA/
├── WorkTree_IA_Compatibility_Analysis.ipynb  # Notebook principal com modelo IA
├── README.md                                 # Documentação principal
├── INTEGRATION_GUIDE.md                      # Guia de integração mobile
├── requirements.txt                          # Dependências Python
└── .gitignore                                # Arquivos ignorados
```

---

## 🚀 Quick Start

### 1. Obter Google Gemini API Key (Gratuita)

1. Acesse: https://makersuite.google.com/app/apikey
2. Faça login e clique em "Create API Key"
3. Copie a chave gerada

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o Notebook

**Google Colab (Recomendado):**
1. Acesse: https://colab.research.google.com/
2. Upload `WorkTree_IA_Compatibility_Analysis.ipynb`
3. Configure sua API Key na seção 2
4. Execute todas as células (Runtime → Run all)

#### Opção B: Jupyter Notebook Local
```bash
jupyter notebook WorkTree_IA_Compatibility_Analysis.ipynb
```

### Passo 4: Executar a API REST (Opcional)

Depois de executar o notebook, um arquivo `worktree_api.py` será gerado:

```bash
python worktree_api.py
```

A API estará disponível em: `http://localhost:5000`

---

## 📊 Funcionalidades Implementadas

### 1. Análise de Compatibilidade Individual
```python
analysis = analyze_compatibility(candidate, job)
display_analysis(analysis)
```
**Jupyter Local:**
1. Instale Jupyter: `pip install jupyter`
2. Execute: `jupyter notebook WorkTree_IA_Compatibility_Analysis.ipynb`
3. Configure API Key e execute as células

### 4. Executar a REST API

Após executar o notebook completo, será gerado o arquivo `worktree_api.py`:

```bash
python worktree_api.py
# API disponível em: http://localhost:5000
```

---

## 📊 Funcionalidades do Notebook

### 1️⃣ Análise Individual de Compatibilidade
- Entrada: Dados do candidato + vaga
- Processamento: Google Gemini analisa via prompt engineering
- Saída: Score, habilidades compatíveis/faltantes, recomendações

### 2️⃣ Visualizações Gráficas
- **Gráfico de Barras**: Scores de compatibilidade
- **Distribuição**: Score médio por candidato
- **Heatmap**: Matriz candidatos vs vagas

### 3️⃣ REST API Flask
- `GET /health` - Status da API
- `POST /api/analyze-compatibility` - Análise individual
- `POST /api/batch-analyze` - Análise em lote

---

## 🔗 Integração Mobile

O sistema está integrado ao **app WorkTree (React Native)**. Para detalhes completos, consulte:

📄 **[INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md)** - Guia completo de integração

**Resumo da integração:**
- Service Layer TypeScript para comunicação com API
- Componente `CompatibilityAnalysis` para exibição visual
- Hook customizado `useCompatibilityAnalysis` para gerenciar estado
- Análise automática quando candidato acessa vaga

---

## 🎓 Requisitos Acadêmicos Atendidos

### ✅ IA Generativa (OBRIGATÓRIO)
- **Google Gemini 1.5 Flash** - Modelo state-of-the-art
- **Prompt Engineering** com contexto rico (2000+ tokens)
- **Geração de análises** personalizadas e estruturadas

### ✅ Deep Learning
- Modelo transformer com bilhões de parâmetros
- Compreensão contextual e análise semântica
- Recomendações baseadas em padrões aprendidos

### ✅ Integração Completa
- **Mobile**: React Native + TypeScript
- **Backend**: REST API Flask + Python
- **IA**: Google Gemini API
- **Interface funcional** com endpoints documentados

---

## 📈 Exemplo de Resultado

```json
{
  "compatibility_score": 85,
  "compatibility_level": "Alto",
  "summary": "Candidato altamente qualificado com forte experiência...",
  "matching_skills": ["React.js", "Node.js", "TypeScript"],
  "missing_skills": ["GraphQL", "Kubernetes"],
  "strengths": [
    "6 anos de experiência em desenvolvimento Full Stack",
    "Certificação AWS"
  ],
  "areas_for_development": [
    "GraphQL para APIs modernas",
    "Orquestração de containers com Kubernetes"
  ],
  "recommendations": [
    "Curso: GraphQL - The Complete Guide",
    "Certificação: CKA (Certified Kubernetes Administrator)"
  ]
}
```

---

## 🏆 Diferenciais Técnicos

1. **Prompt Engineering Avançado**
   - Context-rich prompts estruturados
   - Output em JSON validado
   - Error handling robusto

2. **Análise Multidimensional**
   - Habilidades técnicas (hard skills)
   - Experiência profissional
   - Formação acadêmica
   - Expectativa salarial vs. oferta

3. **Escalabilidade**
   - Análise individual ou em lote
   - Cache de resultados
   - Rate limiting na API

---

## 📝 Documentação Adicional

- **README.md** (este arquivo) - Documentação principal
- **INTEGRATION_GUIDE.md** - Guia completo de integração mobile
- **requirements.txt** - Dependências Python

---

## 🐛 Troubleshooting

**Problema: Erro de API Key**
```bash
# Verifique se configurou corretamente no notebook (seção 2)
GOOGLE_API_KEY = "sua-chave-aqui"
```

**Problema: Porta 5000 ocupada**
```bash
# Use outra porta no worktree_api.py
app.run(host='0.0.0.0', port=5001)
```

**Problema: CORS Error**
```bash
# Já está configurado no Flask com flask-cors
# Certifique-se que flask-cors está instalado
pip install flask-cors
```

---

## 📚 Referências

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Native - Axios](https://axios-http.com/)

---

## 📞 Contato

**Equipe WorkTree - FIAP 2TDSPY**

- Felipe Seiki Hashiguti - RM: 98985
- Lucas Corradini Silveira - RM: 555118
- Matheus Gregorio Mota - RM: 557254

**Repositório Mobile:** https://github.com/felipeSeiki/GS2-Mobile

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos - Global Solution FIAP 2024

---

<div align="center">

**🎉 Transformando recrutamento com IA Generativa!** 🚀

*Demonstrando aplicação prática de IA em problemas reais*

</div>
