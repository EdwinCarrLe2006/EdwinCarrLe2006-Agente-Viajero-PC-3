import pandas as pd
import pulp
import time

# 1. Cargar la matriz de distancias
archivo_excel = r"c:\Users\Edwin CL\Desktop\ING SISTEMAS\CICLO[5]\IO\PC3\MATRIZ_DIST[80].xlsx"
df = pd.read_excel(archivo_excel, index_col=0)

# Obtener el número de ciudades (n) y sus nombres
ciudades = list(df.index)
n = len(ciudades)

# Convertir el DataFrame en un diccionario de distancias
c = df.to_dict()

# Definimos la ciudad de origen
ciudad_origen = ciudades[0]

# 2. Registrar el tiempo de inicio
tiempo_inicio = time.time()

# 3. Crear el problema de optimización
prob = pulp.LpProblem("TSP_Modelo_Gavish_Graves", pulp.LpMinimize)

# 4. Declarar las Variables de Decisión
x = pulp.LpVariable.dicts("x", (ciudades, ciudades), cat='Binary')
y = pulp.LpVariable.dicts("y", (ciudades, ciudades), lowBound=0, upBound=n-1, cat='Continuous')

# 5. Definir la Función Objetivo: Minimizar la distancia total recorrida
prob += pulp.lpSum(c[i][j] * x[i][j] for i in ciudades for j in ciudades if i != j)

# 6. Configurar las Restricciones Generales

# Restricción A: 
for i in ciudades:
    prob += pulp.lpSum(x[i][j] for j in ciudades if i != j) == 1

# Restricción B: 
for j in ciudades:
    prob += pulp.lpSum(x[i][j] for i in ciudades if i != j) == 1

# Restricción C: 
for i in ciudades:
    prob += x[i][i] == 0

# 7. Restricciones de Eliminación de Subtours
for j in ciudades:
    if j != ciudad_origen:
        flujo_entrada = pulp.lpSum(y[i][j] for i in ciudades if i != j)
        flujo_salida = pulp.lpSum(y[j][k] for k in ciudades if k != j)
        prob += (flujo_entrada - flujo_salida) == 1

# Restricción de acoplamiento:
for i in ciudades:
    for j in ciudades:
        if i != j:
            prob += y[i][j] <= (n - 1) * x[i][j]

# 8. Traer al Solver:
pulp.LpSolverDefault.msg = False
prob.solve()

# 9. Calcular el tiempo total de ejecución
tiempo_final = time.time()
tiempo_total = tiempo_final - tiempo_inicio
resultado_status = prob.status

# 10. Mostrar los resultados en consola
print("--- RESULTADOS DEL MODELO GAVISH & GRAVES ---")
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
