from flask import Flask, request, jsonify
from main import mentor_futuro, curador_cursos, psicologo_perfil, radar_profissional, coach_trajetoria
from datetime import date
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/gerar_post", methods=["POST"])
def gerar_post():
    data = request.json
    profissao = data.get("profissao")
    data_de_hoje = date.today().strftime("%d/%m/%Y")

    if not profissao:
        return jsonify({"erro": "Profissão não fornecida"}), 400

   # Etapa 1: Iniciar com mentor de carreira
    lancamentos = mentor_futuro(profissao, data_de_hoje)

    contexto_anterior = lancamentos  # Definindo contexto_anterior como resultado do mentor

# Etapa 2: Curador de cursos com base na profissão E contexto do mentor
    plano_estudos = curador_cursos(profissao, contexto_anterior)

# Etapa 3: Psicólogo comportamental – refina perfil com base no contexto anterior
    rascunho_perfil = psicologo_perfil(lancamentos + plano_estudos)

# Etapa 4: Radar profissional baseado na mesma profissão e contexto anterior
    dados_mercado = radar_profissional(profissao, lancamentos + plano_estudos + rascunho_perfil)

# Etapa 5: Coach de trajetória com base em todo o processo anterior
    plano_acao = coach_trajetoria(profissao, lancamentos + plano_estudos + rascunho_perfil + dados_mercado)

    # Retorno estruturado
    return jsonify({
        "mentor": lancamentos,
        "cursos": plano_estudos,
        "perfil": rascunho_perfil,
        "mercado": dados_mercado,
        "trajetoria": plano_acao
    })

if __name__ == "__main__":
    app.run(debug=True)