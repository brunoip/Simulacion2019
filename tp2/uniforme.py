import numpy as np
import matplotlib.pyplot as plt

i = 2000

a=0
b=10
data = []
python = []

for x in range(i):
    z = np.random.uniform(a,b)
    r = np.random.uniform(0, 1)
    y = 0
    y = a + (b-a)*r
    data.append(y)
    python.append(z)
    print(r, y)

bins = 20
plt.hist(python, bins, edgecolor='black', alpha=0.5, label="Generador de Python")
plt.hist(data, bins, edgecolor='black', alpha=0.5, label="Algoritmo Generador")

plt.plot([0, 10], [i/20, i/20], color='black', label='Uniforme teorica (0,10)', linewidth=4)
plt.legend()
plt.legend(loc="lower center")
plt.show()
