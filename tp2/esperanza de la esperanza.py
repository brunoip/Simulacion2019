import random as rdm
import matplotlib.pyplot as plt

n = 0               # valor mínimo del espacio muestral
m = 36              # valor máximo del espacio muestral
i = 100             # cantidad de ocurrencias
vt = (m - n)/2      # valor teórico de la esperanza
array_ES = []       # esperanza de la esperanza
array_VT = []       # esperanza de la esperanza
count_2 = 0
acumulado = 0
sumatoriaE = 0

for j in range(i):          #iteracion sobre los resultados de la esperanza
    sumatoria = 0
    esperanza = 0
    count = 0
    for x in range(i):                      # en cada iteracion i calculo la media aritmetica
        count += 1
        sumatoria += rdm.randint(n, m)
        esperanza += (sumatoria/count)
    esperanza = esperanza /count

    count_2 += 1
    sumatoriaE += esperanza
    array_ES.append(sumatoriaE/count_2)
    array_VT.append(vt)

print(array_ES)

plt.title('Esperanza (E)')
plt.plot(array_VT, label = "Valor Teorico")
plt.plot(array_ES, label = "Valor muestral")
#plt.axis([0, i, vt - 5, vt + 5])
plt.legend(loc="upper left")
plt.show()
