import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
# Habilitar CORS para permitir requisições do React
CORS(app)

# Inicializar Firebase
try:
    if os.path.exists("firebase-credentials.json"):
        cred = credentials.Certificate("firebase-credentials.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase inicializado com sucesso!")
    else:
        db = None
        print("Aviso: firebase-credentials.json não encontrado. Os treinos não serão salvos no banco.")
except Exception as e:
    db = None
    print(f"Erro ao inicializar Firebase: {e}")

# Configurar a API do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    model = None
    print("Aviso: GEMINI_API_KEY não foi configurada no .env.")

@app.route('/api/generate-workout', methods=['POST'])
def generate_workout():
    data = request.json
    if not data:
        return jsonify({"error": "Dados inválidos fornecidos."}), 400

    nome = data.get('nome', 'Aluno Desconhecido')
    objetivos = data.get('objetivos', 'Melhorar o condicionamento físico')
    restricoes = data.get('restricoes', 'Nenhuma')
    dias_por_semana = data.get('diasPorSemana', 3)
    nivel = data.get('nivel', 'Iniciante')

    # Se não tiver chave real configurada, retorna um mock para testes
    if not model or GEMINI_API_KEY == "SUA_CHAVE_AQUI_PEGUE_NO_AI_STUDIO_GOOGLE":
        mock_response = {
            "plano": [
                {
                    "dia": "Dia 1 - Corpo Todo",
                    "foco": "Adaptação e Resistência",
                    "exercicios": [
                        {"nome": "Agachamento Livre (Peso Corporal)", "series": 3, "repeticoes": "15", "descanso": "60s"},
                        {"nome": "Flexão de Braços (ou com joelhos)", "series": 3, "repeticoes": "10-12", "descanso": "60s"},
                        {"nome": "Remada Curvada (Halter ou Garrafa d'água)", "series": 3, "repeticoes": "12", "descanso": "60s"}
                    ]
                },
                {
                    "dia": "Dia 2 - Cardio e Core",
                    "foco": "Resistência Cardiovascular e Abdômen",
                    "exercicios": [
                        {"nome": "Polichinelos", "series": 4, "repeticoes": "45s ativo", "descanso": "15s"},
                        {"nome": "Prancha Isométrica", "series": 3, "repeticoes": "30-40s", "descanso": "45s"},
                        {"nome": "Abdominal Supra", "series": 3, "repeticoes": "20", "descanso": "45s"}
                    ]
                }
            ],
            "dicas_extras": [
                "(Simulação) Esta é uma resposta de demonstração. Você precisa colocar a sua chave do Gemini no arquivo .env para gerar treinos reais!",
                "Beba bastante água durante os exercícios.",
                "Sempre faça um aquecimento de 5 a 10 minutos antes de iniciar."
            ]
        }
        return jsonify(mock_response), 200

    prompt = f"""
    Atue como um Personal Trainer de elite. Crie um plano de treino para uma semana baseado nas informações do aluno:
    - Objetivos corporais: {objetivos}
    - Restrições médicas/físicas: {restricoes}
    - Frequência: {dias_por_semana} dias por semana
    - Nível de experiência: {nivel}
    
    Retorne o resultado EXCLUSIVAMENTE em formato JSON. O JSON deve ter a seguinte estrutura:
    {{
        "plano": [
            {{
                "dia": "Dia 1 - Treino A",
                "foco": "Peito e Tríceps",
                "exercicios": [
                    {{"nome": "Supino Reto", "series": 3, "repeticoes": "10-12", "descanso": "60s"}},
                    ...
                ]
            }},
            ...
        ],
        "dicas_extras": ["dica 1", "dica 2"]
    }}
    
    Não inclua marcações de bloco de código (```json) ou qualquer outro texto antes ou depois do JSON. Retorne apenas o objeto JSON válido.
    """

    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        workout_data = json.loads(response_text.strip())
        
        # Salvar no Firebase
        if db:
            try:
                db.collection("treinos").add({
                    "nome": nome,
                    "objetivos": objetivos,
                    "restricoes": restricoes,
                    "dias_por_semana": dias_por_semana,
                    "nivel": nivel,
                    "treino": workout_data,
                    "data": firestore.SERVER_TIMESTAMP
                })
                print(f"Treino salvo com sucesso para {nome}")
            except Exception as e:
                print(f"Erro ao salvar no Firebase: {e}")
        else:
            # Injeta o aviso no frontend de que não foi salvo
            mensagem_aviso = "⚠️ Observação: Este treino foi gerado com sucesso, mas NÃO foi salvo no banco de dados porque o arquivo de configuração (firebase-credentials.json) ainda não foi adicionado ao sistema."
            if "dicas_extras" in workout_data:
                workout_data["dicas_extras"].append(mensagem_aviso)
            else:
                workout_data["dicas_extras"] = [mensagem_aviso]
                
        return jsonify(workout_data), 200
    except Exception as e:
        print(f"Erro ao gerar treino: {e}")
        return jsonify({"error": "Falha ao gerar o plano de treino (Verifique se sua chave do Gemini é válida)."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
