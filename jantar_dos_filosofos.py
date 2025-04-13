import tkinter as tk
import threading
import time
import random

# Constantes
N = 5
PENSANDO = "PENSANDO"
FAMINTO = "FAMINTO"
COMENDO = "COMENDO"

estado = [PENSANDO] * N
semaforos = [threading.Semaphore(0) for _ in range(N)]
mutex = threading.Lock()
refeicoes = [0] * N

nomes = ["Sócrates", "Platão", "Aristóteles", "Descartes", "Maquiavel"]

class JantarDosFilosofos:
    def __init__(self, root):
        self.root = root
        self.root.title("Jantar dos Filósofos")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        tk.Label(root, text="Jantar dos Filósofos", font=("Arial", 16)).pack(pady=10)

        self.canvas = tk.Canvas(root, width=700, height=450, bg="white")
        self.canvas.pack()

        self.filosofos_labels = []
        self.contador_labels = []
        self._desenhar_filosofos()

        # Botões
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(btn_frame, text="Iniciar Simulação", command=self.iniciar_simulacao)
        self.start_btn.pack(side="left", padx=10)

        self.solucao_btn = tk.Button(btn_frame, text="Mostrar Solução", command=self.mostrar_solucao)
        self.solucao_btn.pack(side="left", padx=10)

    def _desenhar_filosofos(self):
        posicoes = [
            (350, 100),
            (530, 200),
            (450, 350),
            (250, 350),
            (170, 200)
        ]
        for i in range(N):
            x, y = posicoes[i]
            label = self.canvas.create_oval(x-40, y-40, x+40, y+40, fill="yellow", tags=f"filosofo_{i}")
            texto = self.canvas.create_text(x, y, text=nomes[i], font=("Arial", 10, "bold"), tags=f"texto_{i}")
            contador = self.canvas.create_text(x, y + 55, text="🍽️ 0 refeições", font=("Arial", 9), tags=f"refeicoes_{i}")
            self.filosofos_labels.append((label, texto))
            self.contador_labels.append(contador)

    def atualizar_estado(self, i):
        cor = {
            PENSANDO: "yellow",
            FAMINTO: "red",
            COMENDO: "green"
        }[estado[i]]
        self.canvas.itemconfig(f"filosofo_{i}", fill=cor)

    def atualizar_refeicoes(self, i):
        self.canvas.itemconfig(self.contador_labels[i], text=f"🍽️ {refeicoes[i]} refeições")

    def testar(self, i):
        if estado[i] == FAMINTO and estado[(i - 1) % N] != COMENDO and estado[(i + 1) % N] != COMENDO:
            estado[i] = COMENDO
            self.root.after(0, self.atualizar_estado, i)
            semaforos[i].release()

    def pegar_garfos(self, i):
        with mutex:
            estado[i] = FAMINTO
            self.root.after(0, self.atualizar_estado, i)
            self.testar(i)
        semaforos[i].acquire()

    def devolver_garfos(self, i):
        with mutex:
            estado[i] = PENSANDO
            refeicoes[i] += 1
            self.root.after(0, self.atualizar_estado, i)
            self.root.after(0, self.atualizar_refeicoes, i)
            self.testar((i - 1) % N)
            self.testar((i + 1) % N)

    def rotina_filosofo(self, i):
        while True:
            time.sleep(random.uniform(1, 3))  # Pensando
            self.pegar_garfos(i)
            time.sleep(random.uniform(1.5, 2.5))  # Comendo
            self.devolver_garfos(i)

    def iniciar_simulacao(self):
        self.start_btn["state"] = "disabled"
        for i in range(N):
            threading.Thread(target=self.rotina_filosofo, args=(i,), daemon=True).start()

    def mostrar_solucao(self):
        solucao = tk.Toplevel(self.root)
        solucao.title("Solução para Concorrência")
        solucao.geometry("500x300")
        msg = (
            "Solução adotada:\n\n"
            "🔹 Cada filósofo tem um semáforo próprio para controlar quando ele pode comer.\n"
            "🔹 Um mutex global garante que apenas um filósofo por vez altere os estados.\n"
            "🔹 Um filósofo só pode comer se seus vizinhos não estiverem comendo.\n\n"
            " Isso evita:\n"
            " - Deadlock (travamento total)\n"
            " - Starvation (fome infinita de um filósofo)\n\n"
            " Essa estratégia garante justiça e segurança na concorrência!"
        )
        tk.Label(solucao, text=msg, justify="left", font=("Arial", 10), padx=10, pady=10, anchor="nw").pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = JantarDosFilosofos(root)
    root.mainloop()
