import json
import pandas as pd
from sqlalchemy import create_engine

# 1. Configurar la conexion a nuestra base de datos Docker
# El formato universal es: postgresql://usuario:contraseña@servidor:puerto/base_de_datos
url_conexion = "postgresql://admin:password123@localhost:5432/compras_publicas"
motor = create_engine(url_conexion)

# 2. Leer nuestro archivo crudo (Reemplaza con tu nombre de archivo exacto)
nombre_archivo = "data/respuesta_02012024_20261002_201723.json"

print(f"Leyendo datos desde {nombre_archivo}...")
with open(nombre_archivo, "r", encoding="utf-8") as archivo:
    datos_brutos = json.load(archivo)

# Convertir la lista de ordenes a una tabla Pandas
df = pd.DataFrame(datos_brutos["Listado"])

print("Iniciando inyeccion de datos a PostgreSQL (esto puede tomar unos segundos)...")

# 3. Enviar toda la tabla a PostgreSQL magicamente
# if_exists="replace" significa que si la tabla ya existe, la sobreescribe (reemplaza)
df.to_sql("ordenes_brutas", con=motor, if_exists="replace", index=False)

print("¡Carga exitosa! Se creo la tabla 'ordenes_brutas' con todos los registros.")

# 4. Verificar ejecutando SQL real
print("\n--- VERIFICACION EN POSTGRESQL ---")

# Esta es una consulta SQL estandar: 
# Cuenta todo (COUNT(*)) y cuenta codigos unicos (COUNT(DISTINCT "Codigo"))
consulta_sql = """
    SELECT 
        COUNT(*) AS total_filas, 
        COUNT(DISTINCT "Codigo") AS ordenes_unicas 
    FROM ordenes_brutas;
"""

# pd.read_sql() ejecuta nuestro texto SQL en la base de datos y nos trae el resultado
df_verificacion = pd.read_sql(consulta_sql, con=motor)
print(df_verificacion)