import numpy as np
import matplotlib.pyplot as plt

# Função contínua: f(x) = 2x + 3
def funcao_continua(x):
    return 2 * x + 3

# Função descontínua: definida por partes
def funcao_descontinua(x):
    return np.where(x >= 1, x + 4, x - 2)

# Criando os valores de x
x = np.linspace(-2, 4, 400)  # Intervalo de -2 a 4 com 400 pontos

# Calculando os valores de y para cada função
y_continua = funcao_continua(x)
y_descontinua = funcao_descontinua(x)

# Plotando o gráfico da função contínua
plt.figure(figsize=(12, 6))

# Gráfico da função contínua
plt.subplot(1, 2, 1)  # Subplot 1
plt.plot(x, y_continua, label="f(x) = 2x + 3", color="blue")
plt.title("Função Contínua")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.legend()

# Gráfico da função descontínua
plt.subplot(1, 2, 2)  # Subplot 2
plt.plot(x, y_descontinua, label="f(x) = x + 4 (x ≥ 1)\nf(x) = x - 2 (x < 1)", color="red")
plt.title("Função Descontínua")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.legend()

# Ajustando layout e mostrando os gráficos
plt.tight_layout()
plt.show()