import pandas as pd
#pip install matplotlib
import matplotlib.pyplot
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']
valores = [105235, 107697, 110256, 109236, 108859, 109986]
dados = [10,20,30,40,50]

df = pd.DataFrame(dados)
print(df)
matplotlib.pyplot.plot(meses, valores)
matplotlib.pyplot.show()
