import pandas as pd
import json

# Reemplaza esto con el nombre de tu archivo exacto:
nombre_archivo = "data/respuesta_02012024_20261002_201723.json"
with open(nombre_archivo, "r", encoding="utf-8") as archivo:
    datos_brutos = json.load(archivo)
# 2. La API guarda las ordenes dentro de una seccion llamada "Listado"
lista_ordenes = datos_brutos["Listado"]
# 3. Convertimos esa lista real a nuestra tabla de Pandas
df = pd.DataFrame(lista_ordenes)
# 4. Exploramos lo que trajo
print("\n--- DATOS REALES DE MERCADO PUBLICO ---")
print(f"Total de ordenes descargadas (del 2 de enero de 2024): {len(df)}")
print(f"Columnas disponibles: {list(df.columns)}")
# Veamos los primeros 3 registros
print("\nPrimeras 3 ordenes:")
print(df.head(3))