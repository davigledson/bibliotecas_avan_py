import pandas as pd
#pip install matplotlib
import matplotlib.pyplot
meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho']
valores = [105235, 107697, 110256, 109236, 108859, 109986]



df = pd.DataFrame(valores) / 2
print(df)
matplotlib.pyplot.plot(meses, df)
matplotlib.pyplot.show()
