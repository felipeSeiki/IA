"""
WorkTree AI - API Flask para Análise de Compatibilidade
Integração com Google Gemini 2.0 Flash
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import os
import logging
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configurar Gemini API
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.warning("⚠️ GOOGLE_API_KEY não configurada!")
else:
    logger.info("✅ GOOGLE_API_KEY configurada")

# Modelo Gemini 2.0 Flash
MODEL_NAME = 'gemini-2.0-flash'
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1/models/{MODEL_NAME}:generateContent"

# Configuração do modelo
GENERATION_CONFIG = {
    'temperature': 0.7,
    'topP': 0.95,
    'topK': 40,
    'maxOutputTokens': 2048,
}


def create_compatibility_prompt(candidate, job):
    """Cria prompt otimizado para análise de compatibilidade"""
    prompt = f"""
Você é um especialista em Recursos Humanos e Recrutamento Técnico com 15 anos de experiência.

**CONTEXTO:**
Plataforma WorkTree - análise de compatibilidade candidato-vaga.

**DADOS DA VAGA:**
Cargo: {job.get('title', 'N/A')}
Empresa: {job.get('company', 'N/A')}
Habilidades Requeridas: {', '.join(job.get('required_skills', []))}
Salário: {job.get('salary', 'N/A')}

**DADOS DO CANDIDATO:**
Nome: {candidate.get('name', 'N/A')}
Cargo Atual: {candidate.get('title', 'N/A')}
Experiência: {candidate.get('experience_years', 0)} anos
Habilidades: {', '.join(candidate.get('skills', []))}

**IMPORTANTE: Retorne APENAS um JSON válido no seguinte formato:**

{{
  "compatibility_score": <número de 0 a 100>,
  "compatibility_level": "<Alto|Médio|Baixo>",
  "summary": "<resumo executivo de 2-3 linhas>",
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": ["skill1", "skill2"],
  "strengths": ["ponto forte 1", "ponto forte 2", "ponto forte 3"],
  "areas_for_improvement": ["área 1", "área 2"],
  "recommendations": ["recomendação 1", "recomendação 2"],
  "next_steps": "<próximo passo para o candidato>"
}}

Analise agora e retorne APENAS o JSON, sem texto adicional, sem markdown.
"""
    return prompt


def analyze_compatibility_ai(candidate, job):
    """Analisa compatibilidade entre candidato e vaga usando Gemini"""
    try:
        logger.info(f"🔍 Analisando: {candidate.get('name')} → {job.get('title')}")
        
        # Criar prompt
        prompt = create_compatibility_prompt(candidate, job)
        
        # Chamar Gemini API
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": GENERATION_CONFIG
        }
        
        response = requests.post(
            f"{GEMINI_API_URL}?key={GOOGLE_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        
        # Extrair resposta
        result = response.json()
        response_text = result['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Limpar markdown
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        # Parse JSON
        analysis = json.loads(response_text)
        
        # Adicionar metadados
        analysis['metadata'] = {
            'candidate_id': candidate.get('id'),
            'candidate_name': candidate.get('name'),
            'job_id': job.get('id'),
            'job_title': job.get('title'),
            'analyzed_at': datetime.now().isoformat(),
            'model': MODEL_NAME
        }
        
        logger.info(f"✅ Score: {analysis.get('compatibility_score')}%")
        return analysis
        
    except Exception as e:
        logger.error(f"❌ Erro na análise: {e}")
        raise


@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se a API está online"""
    return jsonify({
        'status': 'online',
        'api_key_configured': GOOGLE_API_KEY is not None,
        'model': MODEL_NAME,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/analyze-compatibility', methods=['POST'])
def analyze_compatibility():
    """
    Analisa compatibilidade entre candidato e vaga
    
    Body: { "candidate": {...}, "job": {...} }
    """
    try:
        data = request.get_json()
        
        # Validar dados
        if not data or 'candidate' not in data or 'job' not in data:
            return jsonify({'error': 'Campos "candidate" e "job" são obrigatórios'}), 400
        
        # Analisar
        result = analyze_compatibility_ai(data['candidate'], data['job'])
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Erro: {e}")
        return jsonify({'error': 'Erro ao processar análise', 'details': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    """Rota não encontrada"""
    return jsonify({
        'error': 'Endpoint não encontrado',
        'endpoints_disponiveis': [
            'GET  /api/health',
            'POST /api/analyze-compatibility'
        ]
    }), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("\n" + "=" * 50)
    print("🚀 WorkTree AI API")
    print("=" * 50)
    print(f"\n📡 Endpoints:")
    print(f"   GET  /api/health")
    print(f"   POST /api/analyze-compatibility")
    print(f"\n🤖 Modelo: {MODEL_NAME}")
    print(f"🔑 API Key: {'Configurada ✅' if GOOGLE_API_KEY else 'Não configurada ⚠️'}")
    print(f"🌐 Porta: {port}")
    print("=" * 50 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
