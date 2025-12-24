import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time

# --------- FUNÇÃO DE AUTO CLICK ---------
def executar_cliques(qtd):
    time.sleep(2)  # tempo pra você posicionar o mouse
    for i in range(qtd):
        pyautogui.click()
        time.sleep(0.05)

def iniciar_autoclick():
    qtd = int(spin_cliques.get())
    threading.Thread(target=executar_cliques, args=(qtd,), daemon=True).start()

# --------- JANELA CONFIG ---------
def abrir_config():
    config = tk.Toplevel(janela)
    config.title("Configuração")
    config.geometry("250x180")
    config.resizable(False, False)

    tk.Label(config, text="Quantidade de cliques").pack(pady=10)

    global spin_cliques
    spin_cliques = tk.Spinbox(config, from_=40, to=90, width=10)
    spin_cliques.pack()

    ttk.Button(config, text="▶ Executar", command=iniciar_autoclick).pack(pady=15)
    ttk.Button(config, text="❌ Fechar", command=config.destroy).pack()

# --------- JANELA PRINCIPAL ---------
janela = tk.Tk()
janela.title("Auto Click")
janela.geometry("300x200")
janela.resizable(False, False)

tk.Label(janela, text="Auto Click", font=("Arial", 14)).pack(pady=10)

ttk.Button(janela, text="Auto Click 1", command=abrir_config).pack(pady=5)
ttk.Button(janela, text="Auto Click 2", command=abrir_config).pack(pady=5)

ttk.Button(janela, text="X Fechar", command=janela.destroy).pack(pady=10)

janela.mainloop()
