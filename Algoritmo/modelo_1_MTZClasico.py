import pandas as pd
import pulp
import time

# 1. Cargar la matriz de distancias desde el Excel generado 


archivo_excel = r"c:\Users\Edwin CL\Desktop\ING SISTEMAS\CICLO[5]\IO\PC3\matriz_distancias(5).xlsx"
df = pd.read_excel(archivo_excel, index_col=0)

# Obtener el número de ciudades (n) y sus nombres
ciudades = list(df.index)
n = len(ciudades)

# Convertir el DataFrame en un diccionario de distancias

# 2. Registrar el tiempo de inicio 
tiempo_inicio = time.time()

# 3. Crear el problema de optimización (Minimización)
prob = pulp.LpProblem("TSP_Modelo_MTZ_Clasico", pulp.LpMinimize)

# 4. Declarar las Variables de Decisión
x = pulp.LpVariable.dicts("x", (ciudades, ciudades), cat='Binary')
u = pulp.LpVariable.dicts("u", ciudades, lowBound=1, upBound=n, cat='Continuous')

# 5. Definir la Función Objetivo: Minimizar la distancia total recorrida
prob += pulp.lpSum(c[i][j] * x[i][j] for i in ciudades for j in ciudades if i != j)

# 6. Configurar las Restricciones Generales
for i in ciudades:
    prob += pulp.lpSum(x[i][j] for j in ciudades if i != j) == 1

for j in ciudades:
    prob += pulp.lpSum(x[i][j] for i in ciudades if i != j) == 1

for i in ciudades:
    prob += x[i][i] == 0

# 7. Restricciones de Eliminación 
ciudad_origen = ciudades[0]
for i in ciudades:
    for j in ciudades:
        if i != ciudad_origen and j != ciudad_origen and i != j:
            prob += u[i] - u[j] + n * x[i][j] <= n - 1

# 8. Traer el Solver 
pulp.LpSolverDefault.msg = False
resultado_status = prob.solve()

# 9. Calcular el tiempo total de ejecución
tiempo_final = time.time()
tiempo_total = tiempo_final - tiempo_inicio

# 10. Mostrar los resultados en consola 
print("--- RESULTADOS DEL MODELO MTZ CLASICO ---")
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
    ruta = [ciudad_origen]
    actual = ciudad_origen
    while len(ruta) < n:
        for j in ciudades:
            if pulp.value(x[actual][j]) is not None and pulp.value(x[actual][j]) > 0.9:
                ruta.append(j)
                actual = j
                break
    ruta.append(ciudad_origen) 
    print(" -> ".join(ruta))
else:
    print("No se pudo encontrar una solución óptima.")
