import numpy as np
import matplotlib.pyplot as plt

# Definição da função f(x) = 3x + 1
def f(x):
    return 3*x + 1

# Intervalo de x ao redor de x = 2
x_vals = np.linspace(0, 4, 100)
y_vals = f(x_vals)

# Valor do limite
x_limite = 2
y_limite = f(x_limite)

# Criando o gráfico
plt.figure(figsize=(8, 5))
plt.plot(x_vals, y_vals, label=r'$f(x) = 3x + 1$', color='b')

# Destacando o ponto (2,7)
plt.scatter(x_limite, y_limite, color='r', zorder=3, label=r'$(2,7)$')
plt.axvline(x_limite, linestyle="--", color="gray", alpha=0.6)
plt.axhline(y_limite, linestyle="--", color="gray", alpha=0.6)

# Configurações do gráfico
plt.xlabel("x")
plt.ylabel("f(x)")
plt.title("Gráfico da função f(x) = 3x + 1 e seu limite em x → 2")
plt.legend()
plt.grid(True)
plt.show()
