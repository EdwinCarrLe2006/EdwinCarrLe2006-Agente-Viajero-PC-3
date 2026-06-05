import pandas as pd
import pulp
import time

# 1. Cargar la matriz de distancias desde el Excel
archivo_excel = r"c:\Users\Edwin CL\Desktop\ING SISTEMAS\CICLO[5]\IO\PC3\matriz_distancias(25).xlsx"
df = pd.read_excel(archivo_excel, index_col=0)

# Obtener el número de ciudades (n) y sus nombres
ciudades = list(df.index)
n = len(ciudades)

# Convertir el DataFrame en un diccionario de distancias CORREGIDO
c = df.to_dict(orient='index')

# Definimos la ciudad de origen
ciudad_origen = ciudades[0]

# 2. Registrar el tiempo de inicio
tiempo_inicio = time.time()

# 3. Crear el problema de optimización
prob = pulp.LpProblem("TSP_Modelo_Finke_Regularizado", pulp.LpMinimize)

# 4. Declarar las Variables de Decisión
x = pulp.LpVariable.dicts("x", (ciudades, ciudades), cat='Binary')
y = pulp.LpVariable.dicts("y", (ciudades, ciudades), lowBound=0, upBound=n-1, cat='Continuous')
z = pulp.LpVariable.dicts("z", (ciudades, ciudades), lowBound=0, upBound=n-1, cat='Continuous')

# 5. Definir la Función Objetivo con REGULACIÓN ÉPSILON
epsilon = 0.00001
prob += pulp.lpSum(
    (c[i][j] if c[i][j] > 0 else epsilon) * x[i][j] 
    for i in ciudades for j in ciudades if i != j
)

# 6. Configurar las Restricciones Generales
for i in ciudades:
    prob += pulp.lpSum(x[i][j] for j in ciudades if i != j) == 1

for j in ciudades:
    prob += pulp.lpSum(x[i][j] for i in ciudades if i != j) == 1

for i in ciudades:
    prob += x[i][i] == 0

# 7. Restricciones de Eliminación de Subtours (Flujo de Dos Productos de Finke)
# CORRECCIÓN AQUÍ: z[i][j] fluye en el mismo sentido que y[i][j]
for i in ciudades:
    for j in ciudades:
        if i != j:
            prob += y[i][j] + z[i][j] == (n - 1) * x[i][j]

# Restricciones de conservación de flujo para las mercancías
for j in ciudades:
    if j != ciudad_origen:
        prob += pulp.lpSum(y[i][j] for i in ciudades if i != j) - pulp.lpSum(y[j][k] for k in ciudades if k != j) == 1
        prob += pulp.lpSum(z[j][k] for k in ciudades if k != j) - pulp.lpSum(z[i][j] for i in ciudades if i != j) == 1

# Restricción de exclusión mutua de tamaño 2
for i in ciudades:
    for j in ciudades:
        if i != j:
            prob += x[i][j] + x[j][i] <= 1

# 8. Invocar al Solver
pulp.LpSolverDefault.msg = False
prob.solve()

# 9. Calcular el tiempo total de ejecución
tiempo_final = time.time()
tiempo_total = tiempo_final - tiempo_inicio
resultado_status = prob.status

# 10. Mostrar los resultados
print("--- RESULTADOS DEL MODELO FINKE, CLAUS & GUNN ---")
print(f"Estado del Solver: {pulp.LpStatus[resultado_status]}")

if pulp.LpStatus[resultado_status] == "Optimal":
    distancia_real_total = sum(c[i][j] * pulp.value(x[i][j]) for i in ciudades for j in ciudades if i != j)
    print(f"Distancia Total Óptima: {distancia_real_total:.1f} km")
else:
    print("Distancia Total Óptima: N/A")

print(f"Tiempo de Ejecución: {tiempo_total:.4f} segundos")
print(f"Número de ciudades: {n}\n")

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
    ruta.append(ciudad_origen) # Retorno al origen
    print(" -> ".join(ruta))
else:
    print("No se pudo encontrar una solución óptima.")