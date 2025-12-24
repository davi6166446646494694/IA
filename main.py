from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS liberado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    memoria = []

    while True:
        msg = await ws.receive_text()
        memoria.append(msg)

        # lógica simples de resposta (pode evoluir depois)
        if "oi" in msg.lower():
            resposta = "Olá! Eu detectei sua mensagem 😊"
        elif "nome" in msg.lower():
            resposta = "Sou uma IA com detector de chat em tempo real."
        else:
            resposta = f"Mensagem detectada. Você disse: {msg}"

        await ws.send_text(resposta)
