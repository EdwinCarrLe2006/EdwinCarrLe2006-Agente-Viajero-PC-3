import random
import pandas as pd
import os

# ==============================================================================
# CONTROL MANUAL DEL TAMAÑO DE LA MATRIZ
# ==============================================================================
n = 120

print(f"Generando matriz aleatoria simétrica para n = {n} ciudades...")

D = [[0] * n for _ in range(n)]

# Llenar la matriz asegurando simetría 
for i in range(n):
    for j in range(i + 1, n):
        valor = 0 if random.random() < 0.05 else random.randint(1, 100)
        
        D[i][j] = valor
        D[j][i] = valor  


nombres_ciudades = [f"Ciudad_{i+1}" for i in range(n)]
df_matriz = pd.DataFrame(D, index=nombres_ciudades, columns=nombres_ciudades)


carpeta_script = os.path.dirname(os.path.abspath(__file__))
nombre_archivo = os.path.join(carpeta_script, f"MATRIZ_DIST[{n}].xlsx")


df_matriz.to_excel(nombre_archivo)

print(f"¡Éxito! Archivo creado correctamente con el nombre: '{nombre_archivo}'")
print(f"La matriz tiene dimensiones de {n}x{n} y está lista para ser usada en los modelos.")