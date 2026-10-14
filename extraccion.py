import sys
import json
import os
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# Cargo las variables de entorno para no exponer mi ticket publicamente en el repositorio
load_dotenv()
ticket = os.getenv("TICKET_MERCADO_PUBLICO")

# Verifico si se paso una fecha por argumento (ddmmyyyy); de lo contrario uso la fecha de ayer
if len(sys.argv) > 1:
    fecha = sys.argv[1]
else:
    fecha = (datetime.now() - timedelta(days=1)).strftime("%d%m%Y")

# URL de extraccion con la fecha correspondiente
url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?fecha={fecha}&ticket={ticket}"

# Ejecuto la peticion y valido que el servicio este operando normalmente (status 200)
respuesta = requests.get(url, timeout=30)

if respuesta.status_code == 200:
    datos = respuesta.json()

    # Aseguro que exista el directorio de destino
    os.makedirs("data", exist_ok=True)

    # Genero un timestamp para el nombre del archivo.
    # Esto asegura que guardemos un historico inmutable en la capa raw sin sobreescribir datos.
    momento_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"data/respuesta_{fecha}_{momento_actual}.json"

    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo)

    print(f"Extraccion exitosa para fecha {fecha}. Archivo crudo guardado en {nombre_archivo}")
else:
    print(f"Fallo en la peticion HTTP para fecha {fecha}. Codigo de estado: {respuesta.status_code}")