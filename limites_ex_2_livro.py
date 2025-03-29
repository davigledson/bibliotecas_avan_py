import numpy as np
import matplotlib.pyplot as plt

# Configurações básicas
plt.figure(figsize=(8, 6))
plt.title("Limite de y = 4x - 5 quando x → 3", fontsize=14)
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True, linestyle='--', alpha=0.7)

# Função
def f(x):
    return 4*x - 5

# Ponto do limite
x0 = 3
y0 = 7

# Valores de ε e δ (exemplo)
epsilon = 0.5
delta = epsilon/4

# Criando os dados
x = np.linspace(2, 4, 100)
y = f(x)

# Plotando a função
plt.plot(x, y, 'b-', linewidth=2, label='y = 4x - 5')

# Linhas de ε (horizontal)
plt.axhline(y0 + epsilon, color='r', linestyle=':', label=f'7 + ε (ε = {epsilon})')
plt.axhline(y0 - epsilon, color='r', linestyle=':', label=f'7 - ε')

# Linhas de δ (vertical)
plt.axvline(x0 + delta, color='g', linestyle=':', label=f'3 + δ (δ = {delta:.3f})')
plt.axvline(x0 - delta, color='g', linestyle=':', label=f'3 - δ')

# Ponto do limite
plt.plot(x0, y0, 'ro', label=f'Ponto (3, 7)')

# Área entre ε
plt.fill_between(x, y0 - epsilon, y0 + epsilon,
                where=(x >= x0 - delta) & (x <= x0 + delta),
                color='yellow', alpha=0.3,
                label='|y - 7| < ε quando |x - 3| < δ')

# Ajustes finais
plt.legend(loc='upper left')
plt.xlim(2, 4)
plt.ylim(5, 9)
plt.tight_layout()
plt.show()