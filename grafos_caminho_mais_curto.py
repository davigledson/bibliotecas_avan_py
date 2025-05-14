import tkinter as tk
import heapq
import time

# Definição dos nós e posições no canvas
nodes = {
    'A': (100, 100),
    'B': (200, 80),
    'C': (300, 150),
    'D': (100, 200),
    'E': (250, 250),
    'F': (350, 100)
}

# Arestas com pesos (em km)
edges = {
    'A': {'B': 2, 'D': 1},
    'B': {'A': 2, 'C': 2, 'F': 4},
    'C': {'B': 2, 'E': 3},
    'D': {'A': 1, 'E': 1},
    'E': {'D': 1, 'C': 3, 'F': 1},
    'F': {'B': 4, 'E': 1}
}

# Função de Dijkstra
def dijkstra(start, end):
    queue = [(0, start, [])]
    visited = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node in visited:
            continue
        path = path + [node]
        if node == end:
            return path
        visited.add(node)
        for neighbor, weight in edges.get(node, {}).items():
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, neighbor, path))
    return []

# Interface principal
class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Caminho mais curto - Dijkstra (com distâncias)")
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()

        self.draw_graph()
        self.root.after(1000, self.animate_path)

    def draw_graph(self):
        # Desenha arestas com pesos
        drawn = set()
        for node, neighbors in edges.items():
            x1, y1 = nodes[node]
            for neighbor, weight in neighbors.items():
                if (node, neighbor) in drawn or (neighbor, node) in drawn:
                    continue  # Evita duplicar linhas bidirecionais
                x2, y2 = nodes[neighbor]
                self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=2)

                # Calcula o ponto médio da linha para exibir o peso
                mid_x = (x1 + x2) / 2
                mid_y = (y1 + y2) / 2
                self.canvas.create_text(mid_x, mid_y, text=f"{weight} km", font=("Arial", 10), fill="black")

                drawn.add((node, neighbor))

        # Desenha nós
        for node, (x, y) in nodes.items():
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="lightblue", outline="black")
            self.canvas.create_text(x, y, text=node, font=("Arial", 12, "bold"))

    def animate_path(self):
        path = dijkstra('A', 'F')
        for i in range(len(path) - 1):
            a, b = path[i], path[i+1]
            x1, y1 = nodes[a]
            x2, y2 = nodes[b]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=4)
            self.canvas.update()
            time.sleep(1)

# Executa o app
if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
