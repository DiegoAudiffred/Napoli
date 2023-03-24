import random
import matplotlib.pyplot as plt

resultados = []

for i in range(100000):
    
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    suma = dado1 + dado2
    
    resultados.append(suma)


print(set(resultados))


plt.hist(resultados, bins=range(2, 14))
plt.xticks(range(2, 13))
plt.xlabel('Suma de los dados')
plt.ylabel('Frecuencia')
plt.show()