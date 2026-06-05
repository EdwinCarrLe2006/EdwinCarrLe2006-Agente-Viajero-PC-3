import random
import pandas as pd
n = random.randint(5, 200)
print(f"Número de ciudades generado aleatoriamente (n): {n}")
D = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(i + 1, n):
        valor = 0 if random.random() < 0.05 else random.randint(1, 100)
        D[i][j] = valor
        D[j][i] = valor

nombres_ciudades = [f"Ciudad_{i+1}"  for i in range(n)]
df_matriz = pd.DataFrame(D, index=nombres_ciudades, columns=nombres_ciudades)

nombre_archivo = "matriz_distancias.xlsx"
df_matriz.to_excel(nombre_archivo)

print(f"¡Éxito! La matriz de {n}x{n} ha sido exportada correctamente a '{nombre_archivo}'.")
