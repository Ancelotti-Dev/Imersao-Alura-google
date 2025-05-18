import os
from datetime import date
from dotenv import load_dotenv
import google.generativeai as genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Carregar chave
load_dotenv(dotenv_path='backend/chave.env')
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Modelo padrão
model = genai.GenerativeModel('gemini-2.0-flash')

# Configurações de segurança (opcional)
safety_settings = [
    {"category": "HARM_CATEGORY_DEROGATORY", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_VIOLENCE", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUAL", "threshold": "BLOCK_HIGH_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]

# --- Função genérica para gerar resposta com modelo --- #
def gerar_resposta(prompt, model_name='gemini-2.0-flash'):
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)
    return response.text

# --- Execução de agente com estado --- #
def call_agent(agent: Agent, message_text: str) -> str:
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text:
                    final_response += part.text + "\n"
    return final_response

# --- Funções dos agentes --- #
def mentor_futuro(vocacao, data_de_hoje):
    prompt = f"""
    Você é um mentor de carreira com 20 anos de experiência em tendências profissionais.
    Hoje é {data_de_hoje}. O usuário descreveu sua vocação e interesses assim: "{vocacao}".
    
    Faça 2 a 3 perguntas abertas para entender melhor o perfil do usuário e, com base nisso,
    recomende 1 ou 2 profissões do futuro que combinem com esse perfil.

    Deixe tudo separadinho bonito, quero nada junto, para cada topico pula uma linha e coloque em negrito todas palavras importes

    Finalize perguntando se o usuário gostaria de receber uma sugestão de curso.
    """
    return gerar_resposta(prompt)

def curador_cursos(profissao, contexto_anterior):
    prompt = f"""
    Baseado neste contexto: {contexto_anterior}

    Você é um curador de trilhas de aprendizado.
    Sugira 3 cursos (iniciante, intermediário e avançado) para a profissão '{profissao}'.
    Deixe tudo separadinho bonito, quero nada junto, para cada topico pula uma linha e coloque em negrito todas palavras importes
    Você é um especialista e vendedor dos cursos da Alura ou gratuitos de alta qualidade. Descreva cada curso de forma atrativa e clara.
    """
    return gerar_resposta(prompt)

def psicologo_perfil(contexto_anterior):
    prompt = f"""
    Com base neste histórico de conversa: {contexto_anterior}

    Você é um especialista em perfil vocacional.
    Deixe tudo separadinho bonito, quero nada junto, para cada topico pula uma linha e coloque em negrito todas palavras importes
    Faça uma análise comportamental destacando traços como: criativo, analítico, executor, empático.
    Seja acolhedor, empático e profissional.
    """
    return gerar_resposta(prompt)

def radar_profissional(profissao, contexto_anterior):
    prompt = f"""
    Profissão: '{profissao}'
    Histórico: {contexto_anterior}
    Deixe tudo separadinho bonito, quero nada junto, para cada topico pula uma linha e coloque em negrito todas palavras importes
    Apresente dados atualizados de mercado:
    - Salário médio
    - Áreas com mais contratações
    - Remoto ou presencial
    - Regiões com maior demanda

    Seja claro e objetivo.
    """
    return gerar_resposta(prompt)

def coach_trajetoria(profissao, contexto_anterior):
    prompt = f"""
    Usuário deseja seguir carreira em '{profissao}'. Contexto: {contexto_anterior}

    Crie um plano com 3 a 5 etapas práticas:
    - Habilidade essencial para desenvolver
    - Como criar portfólio/currículo
    - Dicas de networking
    - Etapas para estágio ou primeiro emprego
    Deixe tudo separadinho bonito, quero nada junto, para cada topico pula uma linha e coloque em negrito todas palavras importes
    Seja inspirador e direto.
    """
    return gerar_resposta(prompt)

# 🔁 Fluxo da Mentoria com vocação primeiro
def mentoria_completa_encadeada(vocacao):
    data_hoje = date.today().strftime("%d/%m/%Y")
    print("🚀 Iniciando mentoria com IA...\n")

    etapa1 = mentor_futuro(vocacao, data_hoje)
    print("\n🧭 Mentor Futuro:\n", etapa1)

    # Suponha que o modelo retorne as profissões sugeridas na etapa1
    # Vamos extrair uma profissão de exemplo para seguir o fluxo (em produção use NLP para extrair com precisão)
    profissao = input("\n💼 Com base nisso, digite uma das profissões sugeridas que te interessou: ").strip()

    if not profissao:
        print("⚠️ Nenhuma profissão informada, encerrando.")
        return

    etapa2 = curador_cursos(profissao, etapa1)
    print("\n📘 Curador de Cursos:\n", etapa2)

    etapa3 = psicologo_perfil(etapa1 + etapa2)
    print("\n🧠 Psicólogo de Perfil:\n", etapa3)

    etapa4 = radar_profissional(profissao, etapa1 + etapa2 + etapa3)
    print("\n📊 Radar Profissional:\n", etapa4)

    etapa5 = coach_trajetoria(profissao, etapa1 + etapa2 + etapa3 + etapa4)
    print("\n🎯 Coach de Trajetória:\n", etapa5)

# 🎯 Roda o sistema
if __name__ == "__main__":
    print("🧠 Bem-vindo à Mentoria de Carreira com IA")
    vocacao = input("Descreva brevemente sua vocação, talentos ou paixões: ").strip()

    if not vocacao:
        print("⚠️ Nenhuma vocação informada!")
    else:
        mentoria_completa_encadeada(vocacao)
