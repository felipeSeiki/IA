"""
WorkTree AI - API Flask para Deploy
Versão otimizada para produção com suporte a requisições assíncronas
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configurar Gemini API via variável de ambiente
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    logger.warning("GOOGLE_API_KEY não configurada! Configure antes do deploy.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={
        'temperature': 0.7,
        'top_p': 0.95,
        'top_k': 40,
        'max_output_tokens': 2048,
    }
)

# Thread pool para processamento paralelo
executor = ThreadPoolExecutor(max_workers=10)


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


def analyze_single(candidate, job):
    """
    Analisa compatibilidade entre um candidato e uma vaga
    Função otimizada para execução em thread pool
    """
    try:
        prompt = create_compatibility_prompt(candidate, job)
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Limpar possíveis marcadores de código
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        analysis = json.loads(response_text)
        
        # Adicionar metadados
        analysis['metadata'] = {
            'candidate_id': candidate.get('id'),
            'candidate_name': candidate.get('name'),
            'job_id': job.get('id'),
            'job_title': job.get('title'),
            'analyzed_at': datetime.now().isoformat(),
            'model': 'gemini-1.5-flash'
        }
        
        return {
            'success': True,
            'data': analysis
        }
        
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao fazer parse do JSON: {e}")
        return {
            'success': False,
            'error': 'Failed to parse AI response',
            'details': str(e),
            'candidate_id': candidate.get('id'),
            'job_id': job.get('id')
        }
        
    except Exception as e:
        logger.error(f"Erro na análise: {e}")
        return {
            'success': False,
            'error': 'Analysis failed',
            'details': str(e),
            'candidate_id': candidate.get('id'),
            'job_id': job.get('id')
        }


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'online',
        'service': 'WorkTree AI Compatibility Analysis',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'api_key_configured': GOOGLE_API_KEY is not None
    }), 200


@app.route('/api/analyze-compatibility', methods=['POST'])
def analyze_compatibility():
    """
    Endpoint principal para análise de compatibilidade
    
    Request Body:
    {
        "candidate": {
            "id": "c1",
            "name": "João Silva",
            "title": "Desenvolvedor",
            "experience_years": 5,
            "skills": ["Python", "JavaScript"]
        },
        "job": {
            "id": "j1",
            "title": "Desenvolvedor Full Stack",
            "company": "Tech Corp",
            "required_skills": ["Python", "JavaScript", "SQL"],
            "salary": "R$ 10.000"
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No data provided',
                'message': 'Request body must contain JSON data'
            }), 400
        
        if 'candidate' not in data or 'job' not in data:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Both "candidate" and "job" are required'
            }), 400
        
        # Validar estrutura básica
        candidate = data['candidate']
        job = data['job']
        
        if not isinstance(candidate, dict) or not isinstance(job, dict):
            return jsonify({
                'error': 'Invalid data format',
                'message': 'Both candidate and job must be objects'
            }), 400
        
        # Processar análise
        result = analyze_single(candidate, job)
        
        if result['success']:
            return jsonify(result['data']), 200
        else:
            return jsonify({
                'error': result['error'],
                'details': result.get('details')
            }), 500
        
    except Exception as e:
        logger.error(f"Erro no endpoint analyze-compatibility: {e}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500


@app.route('/api/batch-analyze', methods=['POST'])
def batch_analyze():
    """
    Análise em lote - processa múltiplos candidatos em paralelo
    
    Request Body:
    {
        "job": {...},
        "candidates": [{...}, {...}, ...]
    }
    
    Retorna lista de análises ordenadas por score
    """
    try:
        data = request.get_json()
        
        if not data or 'job' not in data or 'candidates' not in data:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Both "job" and "candidates" array are required'
            }), 400
        
        job = data['job']
        candidates = data['candidates']
        
        if not isinstance(candidates, list):
            return jsonify({
                'error': 'Invalid data format',
                'message': 'Candidates must be an array'
            }), 400
        
        if len(candidates) == 0:
            return jsonify({
                'error': 'Empty candidates list',
                'message': 'At least one candidate is required'
            }), 400
        
        # Limitar a 50 candidatos por request para evitar timeout
        if len(candidates) > 50:
            return jsonify({
                'error': 'Too many candidates',
                'message': 'Maximum 50 candidates per request'
            }), 400
        
        # Processar em paralelo usando thread pool
        futures = [
            executor.submit(analyze_single, candidate, job)
            for candidate in candidates
        ]
        
        # Coletar resultados
        results = [future.result() for future in futures]
        
        # Separar sucessos e erros
        successful = [r['data'] for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        # Ordenar por score (maior primeiro)
        successful.sort(
            key=lambda x: x.get('compatibility_score', 0),
            reverse=True
        )
        
        return jsonify({
            'job_id': job.get('id'),
            'job_title': job.get('title'),
            'total_candidates': len(candidates),
            'successful_analyses': len(successful),
            'failed_analyses': len(failed),
            'analyzed_at': datetime.now().isoformat(),
            'results': successful,
            'errors': failed if failed else None
        }), 200
        
    except Exception as e:
        logger.error(f"Erro no endpoint batch-analyze: {e}")
        return jsonify({
            'error': 'Batch analysis failed',
            'details': str(e)
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handler para rotas não encontradas"""
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': [
            'GET /health',
            'POST /api/analyze-compatibility',
            'POST /api/batch-analyze'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handler para erros internos"""
    logger.error(f"Internal server error: {e}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("=" * 60)
    print("WorkTree AI API - Iniciada")
    print("=" * 60)
    print("\nEndpoints disponíveis:")
    print(f"  GET  http://localhost:{port}/health")
    print(f"  POST http://localhost:{port}/api/analyze-compatibility")
    print(f"  POST http://localhost:{port}/api/batch-analyze")
    print("\nRecursos:")
    print(f"  - Thread Pool: {executor._max_workers} workers")
    print(f"  - Processamento paralelo: Habilitado")
    print(f"  - API Key configurada: {'Sim' if GOOGLE_API_KEY else 'Não'}")
    print("=" * 60)
    
    # Produção: use gunicorn/waitress ao invés do servidor Flask de desenvolvimento
    app.run(host='0.0.0.0', port=port, debug=False)
