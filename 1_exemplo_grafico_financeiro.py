import matplotlib.pyplot as plt

meses = ['casa', 'ventilador', 'carro', 'moto', 'celular', 'roupa']

valores = [550, 17, 30, 130, 200, 1000]
movel = float(input("Digite o valor do novo móvel: "))
meses.insert(0, 'Novo Móvel')
valores.insert(0, movel)

plt.plot(meses, valores, marker='o')
plt.title('Valores dos Móveis')
plt.xlabel('Categorias')
plt.ylabel('Valores (em R$)')
plt.grid(True)


plt.show()
