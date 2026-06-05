import pandas as pd
import pulp
import time

# 1. Cargar la matriz de distancias desde el Excel generado por el Integrante B
# Se utiliza la misma matriz de 12 ciudades para mantener la consistencia
archivo_excel = r"c:\Users\Edwin CL\Desktop\ING SISTEMAS\CICLO[5]\IO\PC3\MATRIZ_DIST[80].xlsx"
df = pd.read_excel(archivo_excel, index_col=0)

# Obtener el número de ciudades (n) y sus nombres
ciudades = list(df.index)
n = len(ciudades)

# Convertir el DataFrame en un diccionario de distancias para facilitar el acceso
c = df.to_dict()

# Definimos la ciudad de origen (la primera de la lista, ej: Ciudad_1)
ciudad_origen = ciudades[0]

# 2. Registrar el tiempo de inicio para el cuadro de indicadores
tiempo_inicio = time.time()

# 3. Crear el problema de optimización (Minimización)
prob = pulp.LpProblem("TSP_Modelo_Gavish_Graves", pulp.LpMinimize)

# 4. Declarar las Variables de Decisión
# x[i][j] = Variable binaria (1 si se viaja de i a j, 0 de lo contrario)
x = pulp.LpVariable.dicts("x", (ciudades, ciudades), cat='Binary')

# y[i][j] = Variable continua que representa las toneladas que lleva el camión en el tramo i -> j
# La carga máxima al salir no superará n - 1
y = pulp.LpVariable.dicts("y", (ciudades, ciudades), lowBound=0, upBound=n-1, cat='Continuous')

# 5. Definir la Función Objetivo: Minimizar la distancia total recorrida
prob += pulp.lpSum(c[i][j] * x[i][j] for i in ciudades for j in ciudades if i != j)

# 6. Configurar las Restricciones Generales

# Restricción A: Salir exactamente una vez de cada ciudad i
for i in ciudades:
    prob += pulp.lpSum(x[i][j] for j in ciudades if i != j) == 1

# Restricción B: Llegar exactamente una vez a cada ciudad j
for j in ciudades:
    prob += pulp.lpSum(x[i][j] for i in ciudades if i != j) == 1

# Restricción C: Impedir que una ciudad viaje a sí misma (diagonal nula)
for i in ciudades:
    prob += x[i][i] == 0

# 7. Restricciones de Eliminación de Subtours (Balance de Flujo de Gavish & Graves)
for j in ciudades:
    if j != ciudad_origen:
        # Carga que entra a 'j' menos la carga que sale de 'j' debe ser exactamente igual a 1 tonelada
        flujo_entrada = pulp.lpSum(y[i][j] for i in ciudades if i != j)
        flujo_salida = pulp.lpSum(y[j][k] for k in ciudades if k != j)
        prob += (flujo_entrada - flujo_salida) == 1

# Restricción de acoplamiento: El camión solo lleva carga por los arcos que efectivamente decide recorrer
for i in ciudades:
    for j in ciudades:
        if i != j:
            prob += y[i][j] <= (n - 1) * x[i][j]

# 8. Invocar al Solver (Usa CBC deshabilitando logs internos)
pulp.LpSolverDefault.msg = False
prob.solve()

# 9. Calcular el tiempo total de ejecución
tiempo_final = time.time()
tiempo_total = tiempo_final - tiempo_inicio
resultado_status = prob.status

# 10. Mostrar los resultados en consola con la estructura exacta solicitada
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
    ruta.append(ciudad_origen) # Retorno al origen
    print(" -> ".join(ruta))
else:
    print("No se pudo encontrar una solución óptima.")