# Vamos criar o código inicial que contém:
# - Um grafo com 22 cidades reais brasileiras.
# - Arestas com distâncias aproximadas em km.
# - Algoritmo de Dijkstra.
# - Visualização gráfica com Tkinter.
# - Exportação do grafo com caminho mais curto para Graphviz (.dot).

import tkinter as tk
import heapq
import time
import os

# Bibliotecas para exportar com Graphviz
from graphviz import Digraph

# Cidades (22 vértices)
city_positions = {
    "Natal": (100, 100),
    "João Pessoa": (200, 130),
    "Recife": (300, 120),
    "Maceió": (400, 150),
    "Aracaju": (500, 180),
    "Salvador": (600, 210),
    "Feira de Santana": (650, 260),
    "Petrolina": (500, 100),
    "Teresina": (300, 30),
    "Parnaíba": (250, 10),
    "Fortaleza": (150, 30),
    "Sobral": (130, 10),
    "São Luís": (100, -20),
    "Caxias": (180, -40),
    "Palmas": (100, 250),
    "Barreiras": (400, 300),
    "Brasília": (200, 350),
    "Goiânia": (250, 400),
    "Belo Horizonte": (400, 400),
    "Vitória da Conquista": (500, 300),
    "Ilhéus": (550, 250),
    "Serra da Capivara": (350, 50)  # Destino turístico
}

# Arestas com pesos aproximados (em km)
edges = {
    "Natal": {"João Pessoa": 180, "Fortaleza": 530},
    "João Pessoa": {"Recife": 120},
    "Recife": {"Maceió": 260},
    "Maceió": {"Aracaju": 280},
    "Aracaju": {"Salvador": 350},
    "Salvador": {"Feira de Santana": 120, "Ilhéus": 310},
    "Feira de Santana": {"Petrolina": 500},
    "Petrolina": {"Serra da Capivara": 300},
    "Teresina": {"Serra da Capivara": 530, "Parnaíba": 340},
    "Parnaíba": {"Sobral": 360},
    "Sobral": {"Fortaleza": 230},
    "São Luís": {"Caxias": 360},
    "Caxias": {"Teresina": 70},
    "Palmas": {"Brasília": 970},
    "Barreiras": {"Brasília": 600},
    "Brasília": {"Goiânia": 210},
    "Goiânia": {"Belo Horizonte": 840},
    "Belo Horizonte": {"Vitória da Conquista": 670},
    "Vitória da Conquista": {"Ilhéus": 200}
}

# Algoritmo de Dijkstra
def dijkstra(start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if node == end:
            return path, cost
        visited.add(node)
        for neighbor, weight in edges.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))
    return [], 0

# Exporta o grafo para Graphviz com destaque para o caminho
def export_to_graphviz(path):
    dot = Digraph()
    for city in city_positions:
        dot.node(city)

    for city, neighbors in edges.items():
        for dest, weight in neighbors.items():
            if (city in path and dest in path and abs(path.index(city) - path.index(dest)) == 1):
                dot.edge(city, dest, label=f"{weight} km", color="red", penwidth="3")
            else:
                dot.edge(city, dest, label=f"{weight} km", color="gray")

    dot.render("grafo_turistico", format="png", cleanup=True)

# Interface Tkinter
class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Roteiros Turísticos - Dijkstra")
        self.canvas = tk.Canvas(root, width=800, height=500, bg="white")
        self.canvas.pack()

        self.draw_graph()
        self.root.after(1000, self.animate_path)

    def draw_graph(self):
        self.canvas.delete("all")
        drawn = set()
        for city, neighbors in edges.items():
            x1, y1 = city_positions[city]
            for neighbor, weight in neighbors.items():
                x2, y2 = city_positions[neighbor]
                if (city, neighbor) in drawn or (neighbor, city) in drawn:
                    continue
                self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                self.canvas.create_text(mid_x, mid_y, text=f"{weight} km", font=("Arial", 8))
                drawn.add((city, neighbor))

        for city, (x, y) in city_positions.items():
            self.canvas.create_oval(x-8, y-8, x+8, y+8, fill="lightblue", outline="black")
            self.canvas.create_text(x, y, text=city, font=("Arial", 7), anchor="nw")

    def animate_path(self):
        path, total = dijkstra("Natal", "Serra da Capivara")
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            x1, y1 = city_positions[a]
            x2, y2 = city_positions[b]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=4)
            self.canvas.update()
            time.sleep(1)
        export_to_graphviz(path)

# Executa app
root = tk.Tk()
app = GraphApp(root)
root.mainloop()

