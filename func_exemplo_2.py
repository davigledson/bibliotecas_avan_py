import numpy as np
import matplotlib.pyplot as plt

# Configurações iniciais
plt.figure(figsize=(10, 6))
plt.title("Limite de y = 4x - 5 quando x → 3", fontsize=14)
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)

# Define a função
def f(x):
    return 4 * x - 5

# Ponto de interesse (x=3, y=7)
x_target = 3
y_target = 7

# Valores de ε e δ (exemplo: ε=0.5, δ=ε/4=0.125)
epsilon = 0.5 #Representava "erro" (em francês: erreur).
delta = epsilon / 4  #Representava "diferença" (em francês: différence).

# Cria os valores de x
x = np.linspace(2, 4, 400)
y = f(x)

# Plota a função
plt.plot(x, y, label="y = 4x - 5", color="blue")

# Destaca o ponto (3, 7)
plt.scatter(x_target, y_target, color="red", label=f"Ponto: ({x_target}, {y_target})")

# Linhas horizontais para y = 7 ± ε
plt.axhline(y=y_target + epsilon, color="green", linestyle="--", label=f"y = 7 ± ε (ε = {epsilon})")
plt.axhline(y=y_target - epsilon, color="green", linestyle="--")

# Linhas verticais para x = 3 ± δ
plt.axvline(x=x_target + delta, color="purple", linestyle=":", label=f"x = 3 ± δ (δ = {delta:.3f})")
plt.axvline(x=x_target - delta, color="purple", linestyle=":")

# Preenche a região entre y = 7 ± ε
plt.fill_between(x, y_target - epsilon, y_target + epsilon, where=(x >= x_target - delta) & (x <= x_target + delta), color="yellow", alpha=0.3, label="Região onde |y - 7| < ε")

# Legenda e ajustes
plt.legend()
plt.xlim(2, 4)
plt.ylim(0, 10)
plt.show()