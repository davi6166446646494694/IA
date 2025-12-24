from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

MEMORIA_ARQ = "memoria.json"

# Base de conhecimento
base_conhecimento = [
    "Meu nome é IA Pensante.",
    "Posso responder perguntas gerais.",
    "Tenho memória da conversa.",
    "Aprendo com o contexto da conversa.",
    "Fui criada em Python.",
    "Posso conversar sobre vários assuntos."
]

# Carregar memória
if os.path.exists(MEMORIA_ARQ):
    with open(MEMORIA_ARQ, "r") as f:
        memoria = json.load(f)
else:
    memoria = []

vectorizer = TfidfVectorizer()
vectorizer.fit(base_conhecimento)

class Entrada(BaseModel):
    mensagem: str

def salvar_memoria():
    with open(MEMORIA_ARQ, "w") as f:
        json.dump(memoria, f, indent=2)

def pensar(pergunta):
    textos = base_conhecimento + [m["mensagem"] for m in memoria]
    X = vectorizer.fit_transform(textos + [pergunta])
    similaridades = cosine_similarity(X[-1], X[:-1])

    melhor = similaridades.argmax()
    score = similaridades[0][melhor]

    if score > 0.2:
        return textos[melhor]
    else:
        return "Não tenho certeza, mas posso aprender se continuarmos conversando."

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
        "memoria_total": len(memoria)
    }
