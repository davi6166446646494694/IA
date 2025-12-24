from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

ARQ_MEMORIA = "memoria.json"

# Base de conhecimento inicial
base_conhecimento = [
    "Meu nome é IA.",
    "Sou uma inteligência artificial.",
    "Posso conversar com você.",
    "Tenho memória das mensagens.",
    "Fui criada em Python.",
    "Respondo perguntas gerais."
]

# Carregar memória
if os.path.exists(ARQ_MEMORIA):
    with open(ARQ_MEMORIA, "r", encoding="utf-8") as f:
        memoria = json.load(f)
else:
    memoria = []

class Entrada(BaseModel):
    mensagem: str

def salvar_memoria():
    with open(ARQ_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memoria, f, indent=2, ensure_ascii=False)

def pensar(pergunta):
    textos = base_conhecimento + [m["mensagem"] for m in memoria]
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(textos + [pergunta])

    similaridades = cosine_similarity(X[-1], X[:-1])
    melhor = similaridades.argmax()
    score = similaridades[0][melhor]

    if score > 0.25:
        return textos[melhor]
    else:
        return "Ainda não sei responder isso, mas posso aprender com o tempo."

@app.post("/chat")
def chat(dados: Entrada):
    resposta = pensar(dados.mensagem)

    memoria.append({
        "mensagem": dados.mensagem,
        "resposta": resposta
    })

    salvar_memoria()

    return {
        "resposta": resposta,
        "memoria": len(memoria)
    }
