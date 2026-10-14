import glob
import json
import os
import pandas as pd
from sqlalchemy import create_engine, inspect, text

# Instancio el motor de conexion apuntando a mi contenedor local de PostgreSQL en Docker
url_conexion = "postgresql://admin:password123@localhost:5432/compras_publicas"
motor = create_engine(url_conexion)

# Selecciono dinamicamente el archivo mas reciente dentro de la capa cruda
archivos = glob.glob("data/respuesta_*.json")
if not archivos:
    raise FileNotFoundError("No se encontraron archivos en data/ con el patron respuesta_*.json")

nombre_archivo = max(archivos, key=os.path.getmtime)
print(f"Cargando el archivo mas reciente: {nombre_archivo}")

# Cargo el archivo JSON desde la capa raw local
with open(nombre_archivo, "r", encoding="utf-8") as archivo:
    datos_crudos = json.load(archivo)

# Aislo unicamente el nodo 'Listado' que contiene la data a tabular
lista_ordenes = datos_crudos["Listado"]

# Convierto la estructura anidada a un DataFrame para el procesamiento tabular
df = pd.DataFrame(lista_ordenes)

# Si la tabla no existe la creo; si ya existe uso TRUNCATE + append para no romper vistas de dbt
inspector = inspect(motor)
if not inspector.has_table("ordenes_brutas"):
    df.to_sql("ordenes_brutas", con=motor, if_exists="replace", index=False)
else:
    with motor.begin() as conexion:
        conexion.execute(text("TRUNCATE TABLE ordenes_brutas;"))
    df.to_sql("ordenes_brutas", con=motor, if_exists="append", index=False)

print("Datos cargados exitosamente en la tabla 'ordenes_brutas'.")

# Verificacion del total de registros cargados
consulta_sql = """
    SELECT 
        COUNT(*) AS total_filas, 
        COUNT(DISTINCT "Codigo") AS ordenes_unicas 
    FROM ordenes_brutas;
"""
df_verificacion = pd.read_sql(consulta_sql, con=motor)
print("\n--- Verificacion en PostgreSQL ---")
print(df_verificacion)