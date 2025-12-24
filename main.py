from fastapi import FastAPI
from pydantic import BaseModel
import json, os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="IA Completa")

PASTA_MEMORIA = "memoria"
os.makedirs(PASTA_MEMORIA, exist_ok=True)

BASE_CONHECIMENTO = [
    "Sou uma inteligência artificial criada para conversar.",
    "Tenho memória e consigo aprender.",
    "Posso lembrar do que você me ensina.",
    "Analiso o significado das perguntas.",
    "Respondo usando contexto."
]

class Entrada(BaseModel):
    usuario: str
    mensagem: str

def carregar_memoria(usuario):
    caminho = f"{PASTA_MEMORIA}/{usuario}.json"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_memoria(usuario, memoria):
    with open(f"{PASTA_MEMORIA}/{usuario}.json", "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

def pensar(mensagem, memoria):
    textos = BASE_CONHECIMENTO + [m["mensagem"] for m in memoria]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(textos + [mensagem])
    similaridades = cosine_similarity(X[-1], X[:-1])
    melhor = similaridades.argmax()
    score = similaridades[0][melhor]

    if score > 0.30:
        return textos[melhor]
    else:
        return "Não tenho certeza ainda, mas posso aprender se você me explicar."

@app.post("/chat")
def chat(dados: Entrada):
    memoria = carregar_memoria(dados.usuario)
    resposta = pensar(dados.mensagem, memoria)

    # aprendizado simples
    if resposta.startswith("Não tenho certeza"):
        BASE_CONHECIMENTO.append(dados.mensagem)

    memoria.append({
        "mensagem": dados.mensagem,
        "resposta": resposta
    })

    salvar_memoria(dados.usuario, memoria)

    return {
        "resposta": resposta,
        "mensagens_memorizadas": len(memoria)
    }
