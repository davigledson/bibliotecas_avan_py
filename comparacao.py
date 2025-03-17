import matplotlib.pyplot as plt

bens = ['bem 1', 'bem 2']
valores = []
bem1 = float(input("Digite o valor do bem 1: "))
bem2 = float(input("Digite o valor do bem 2: "))
valores.append(bem1)
valores.append(bem2)
renda = int(input("Digite o valor da sua renda: "))
valores.insert(0, renda)
bens.insert(0, 'Novo Móvel')

plt.plot(bens,  marker='o')
plt.plot(bens, valores, marker='o')
plt.title('Restrição Orçamentária')
plt.xlabel('Categorias')
plt.ylabel('Valores (em R$)')
plt.grid(True)
plt.show()