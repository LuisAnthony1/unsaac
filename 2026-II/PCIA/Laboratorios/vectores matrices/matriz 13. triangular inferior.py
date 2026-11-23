# matriz 13: transformar matriz 4x4 en triangular inferior (ceros arriba)

import random

matriz = [[random.randint(1, 20) for j in range(4)] for i in range(4)]
print("matriz original:")
for f in matriz:
    print(f)

for i in range(4):
    for j in range(4):
        if j > i:
            matriz[i][j] = 0

print("matriz triangular inferior:")
for f in matriz:
    print(f)
