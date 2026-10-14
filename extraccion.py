import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Cargo las variables de entorno para no exponer mi ticket publicamente en el repositorio
load_dotenv()
ticket = os.getenv("TICKET_MERCADO_PUBLICO")

# URL de extraccion configurada para una fecha de prueba
url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?fecha=02012024&ticket={ticket}"

# Ejecuto la peticion y valido que el servicio este operando normalmente (status 200)
respuesta = requests.get(url)

if respuesta.status_code == 200:
    datos = respuesta.json()
    
    # Genero un timestamp para el nombre del archivo. 
    # Esto asegura que guardemos un historico inmutable en la capa raw sin sobreescribir datos.
    fecha_hoy = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"data/respuesta_{fecha_hoy}.json"
    
    with open(nombre_archivo, "w") as archivo:
        json.dump(datos, archivo)
        
    print(f"Extraccion exitosa. Archivo crudo guardado en {nombre_archivo}")
else:
    print(f"Fallo en la peticion HTTP. Codigo de estado: {respuesta.status_code}")