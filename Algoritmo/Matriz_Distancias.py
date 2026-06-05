import random
import pandas as pd

# 1. Definir el número aleatorio de ciudades entre 5 y 200 según la guía
n = random.randint(5, 200)
print(f"Número de ciudades generado aleatoriamente (n): {n}")

# 2. Inicializar la matriz de ceros
D = [[0] * n for _ in range(n)]

# 3. Llenar la matriz asegurando simetría y las probabilidades solicitadas
for i in range(n):
    for j in range(i + 1, n):
        # 5% de probabilidad de ser 0 km, 95% de ser un entero entre 1 y 100 km
        valor = 0 if random.random() < 0.05 else random.randint(1, 100)
        
        # Al ser un grafo no direccionado/simétrico, el viaje i->j es igual al j->i
        D[i][j] = valor
        D[j][i] = valor

# 4. Convertir la matriz a un formato de DataFrame de Pandas para manejarlo fácilmente
# Nombramos las filas y columnas como Ciudad_1, Ciudad_2, etc.
nombres_ciudades = [f"Ciudad_{i+1}"  for i in range(n)]
df_matriz = pd.DataFrame(D, index=nombres_ciudades, columns=nombres_ciudades)

# 5. Exportar los datos a un archivo de Excel (Entregable 4 de la guía)
nombre_archivo = "matriz_distancias.xlsx"
df_matriz.to_excel(nombre_archivo)

print(f"¡Éxito! La matriz de {n}x{n} ha sido exportada correctamente a '{nombre_archivo}'.")