import pandas as pd
import pulp
import time

# 1. Cargar la matriz de distancias 
archivo_excel = r"c:\Users\Edwin CL\Desktop\ING SISTEMAS\CICLO[5]\IO\PC3\matriz_distancias(43).xlsx"
df = pd.read_excel(archivo_excel, index_col=0)

# Obtener el número de ciudades y sus nombres
ciudades = list(df.index)
n = len(ciudades)

# Convertir el DataFrame en un diccionario de distancias
c = df.to_dict()

# Definir el conjunto de etapas
etapas = list(range(1, n + 1))

# 2. Registrar el tiempo de inicio
tiempo_inicio = time.time()

# 3. Crear el problema de optimización 
prob = pulp.LpProblem("TSP_Modelo_Diaby_Corregido", pulp.LpMinimize)

# 4. Declarar las Variables de Decisión Binarias
x = pulp.LpVariable.dicts("x", (ciudades, ciudades, etapas), cat='Binary')

# 5. Definir la Función Objetivo: Minimizar la distancia total recorrida
prob += pulp.lpSum(c[i][j] * x[i][j][s] for i in ciudades for j in ciudades if i != j for s in etapas)

# 6. Configurar las Restricciones Lineales del Enfoque de Diaby

# Restricción A: 
for s in etapas:
    prob += pulp.lpSum(x[i][j][s] for i in ciudades for j in ciudades if i != j) == 1

# Restricción B: 
for i in ciudades:
    prob += pulp.lpSum(x[i][j][s] for j in ciudades if i != j for s in etapas) == 1

# Restricción C: 
for j in ciudades:
    prob += pulp.lpSum(x[i][j][s] for i in ciudades if i != j for s in etapas) == 1

# Restricción D: 
for j in ciudades:
    for s in etapas:
        s_siguiente = s + 1 if s < n else 1  
        
        flujo_entrada = pulp.lpSum(x[i][j][s] for i in ciudades if i != j)
        flujo_salida = pulp.lpSum(x[j][k][s_siguiente] for k in ciudades if k != j)
        
        prob += flujo_entrada == flujo_salida

# Restricción E: 
for i in ciudades:
    for s in etapas:
        prob += x[i][i][s] == 0

# 7. Traer al Solver
pulp.LpSolverDefault.msg = False
resultado_status = prob.solve()

# 8. Calcular el tiempo total de ejecución
tiempo_final = time.time()
tiempo_total = tiempo_final - tiempo_inicio

# 9. Mostrar los resultados en consola
print("--- RESULTADOS DEL MODELO MOUSTAPHA DIABY ---")
print(f"Estado del Solver: {pulp.LpStatus[resultado_status]}")

distancia_final = pulp.value(prob.objective)
if distancia_final is not None:
    print(f"Distancia Total Óptima: {distancia_final:.1f} km")
else:
    print("Distancia Total Óptima: N/A")

print(f"Tiempo de Ejecución: {tiempo_total:.4f} segundos")
print(f"numero de ciudades: {n}\n")

if pulp.LpStatus[resultado_status] == "Optimal":
    print("Ruta óptima encontrada:")
    ciudad_origen = ciudades[0]
    ruta = []
    
    for s in etapas:
        for i in ciudades:
            for j in ciudades:
                if pulp.value(x[i][j][s]) is not None and pulp.value(x[i][j][s]) > 0.9:
                    if i not in ruta:
                        ruta.append(i)
                    if s == n and j not in ruta:
                        ruta.append(j)
                        
    # Forzar alineación visual para que comience en la Ciudad de origen
    if len(ruta) > 0:
        if ruta[0] != ciudad_origen:
            idx = ruta.index(ciudad_origen)
            ruta = ruta[idx:] + ruta[:idx]
        ruta.append(ciudad_origen)
        print(" -> ".join(ruta))
    else:
        print("No se pudo estructurar la secuencia de la ruta.")
else:
    print("No se pudo encontrar una solución óptima.")
