from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class Pergunta(BaseModel):
    pergunta: str

respostas_genericas = [
    "Interessante pergunta.",
    "Pode explicar melhor?",
    "Isso depende de vários fatores.",
    "Boa pergunta!",
    "Ainda estou aprendendo sobre isso.",
    "Posso te ajudar com mais detalhes."
]

@app.post("/chat")
def chat(dados: Pergunta):
    resposta = random.choice(respostas_genericas)
    return {
        "pergunta": dados.pergunta,
        "resposta": resposta
    }
