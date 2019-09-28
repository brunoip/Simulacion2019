import random

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import math
from numpy import *

media=[]
varianza=[]
frelativa=[]
tiradas=[]
maxTiradas = 1000

def Mean(x):
    sum=0
    for i in x:
        sum+=i
    return sum / len(x)

def Variance(x):
    sum = 0
    m = Mean(x)
    for i in x:
        sum += (i-m)**2
    return sum / (len(x)-1)

def Count(x,y):
    sum = 0
    for i in x:
        if (i==y):
            sum+=1
    return sum

sumatoria=0
for i in range(36):
    sumatoria = sumatoria+i

m=(0.027)*sumatoria

sumatoria2 = 0
for i in range(36):
    sumatoria2 += ((i-m)*(i-m))

v=(0.027)*sumatoria2

f = 0.027  # 1/37

print("m " + repr(m))
print("v " + repr(v))
print("f " + repr(f))

tiradas.append(random.randint(0, 36))
media.append(Mean(tiradas))
frelativa.append(Count(tiradas, 16)/1)

for i in range(1, maxTiradas):
    tiradas.append(random.randint(0, 36))
    media.append(Mean(tiradas))
    varianza.append(Variance(tiradas))
    frelativa.append(Count(tiradas, 16) / float(i))


print(media)
print(varianza)
print(frelativa)

#datos dobles


histograma=[]
tiradas=[]
tiradas.append(random.randint(0, 36))
histograma.append(Count(tiradas, 16)/1)

for i in range(1, 36):
    tiradas = []
    frelativa=[]
    tiradas.append(random.randint(0, 36))
    frelativa.append(Count(tiradas, 16) / 1)
    for j in range(1, maxTiradas):
        tiradas.append(random.randint(0, 36))
        frelativa.append(Count(tiradas, i) / float(j))
    histograma.append(frelativa[maxTiradas-1])


print (histograma)


