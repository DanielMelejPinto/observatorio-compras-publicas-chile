import pandas as pd
# 1. Muestra ficticia de órdenes de compra (lista de diccionarios)
muestra_datos = [
    {"Codigo": "1234-5-LE26", "Nombre": "Computadores", "Estado": "Aceptada", "Monto": 1500000},
    {"Codigo": "9876-1-CM26", "Nombre": "Escritorios", "Estado": "Enviada", "Monto": 800000},
    {"Codigo": "5555-2-LQ26", "Nombre": "Papelería", "Estado": "Aceptada", "Monto": 50000}
]

#2. Convertimo los datos en un DataFrame (la tabla maestra de pandas)
df = pd.DataFrame(muestra_datos)

#3. Exploramos los datos
print("--- RESUMEN DE LA MUESTRA ---")
print(f"Cantidad de órdenes: {len(df)}")
print(f"Columnas disponibles: {list(df.columns)}\n")
print("--- TABLA DE DATOS ---")
print(df)

#4. Analisis basico de los datos
print("\n--- ANÁLISIS BÁSICO ---")

#Filtrar: Nos quedamos solo con ls dilas donde el estado es "Aceptada"
ordenes_aceptadas = df[df["Estado"] == "Aceptada"]
print(f"Cantidad de ordenes Aceptadas: {len(ordenes_aceptadas)}")

#Calcular: Sumamos la columna "Monto" de esas ordenes filtradas
monto_total = ordenes_aceptadas["Monto"].sum()
print(f"Suma total de órdenes aceptadas: ${monto_total}")