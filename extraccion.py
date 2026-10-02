import os
import requests
from dotenv import load_dotenv
import json
from datetime import datetime

# 1. Cargar las credenciales ocultas desde el archivo .env
load_dotenv()
ticket = os.getenv("TICKET_MERCADO_PUBLICO", "pega_aqui_tu_ticket")

# 2. Verificar si tenemos el ticket
if not ticket or ticket == "pega_aqui_tu_ticket":
    print("ADVERTENCIA: No tienes un ticket real configurado en el archivo .env")
    print("El programa intentara conectarse, pero Mercado Publico probablemente lo rechace.")
else:
    print("Ticket cargado correctamente de forma segura.")

# 3. Configurar la URL de la API (buscaremos compras de un dia especifico)
fecha_ejemplo = "02012024" # 02 de enero de 2024
url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?fecha={fecha_ejemplo}&ticket={ticket}"

# Mostramos la URL en pantalla ocultando la contrasena para mayor seguridad
print(f"\nIntentando conectar a: {url.replace(ticket, '***SECRETO***')}")

# 4. Hacer la peticion a Mercado Publico
print("\nConsultando a la API de Mercado Publico...")
respuesta = requests.get(url)

# 5. Analizar el resultado
if respuesta.status_code == 200:
    # Si el codigo es 200, significa "Todo OK"
    datos = respuesta.json()
    print("Descarga exitosa. Respuesta del servidor guardada.")
else:
    # Cualquier otro codigo (401, 404, 500) significa que hubo un error
    print(f"Error en la descarga. Codigo de estado: {respuesta.status_code}")
    print("Mensaje del servidor:", respuesta.text)

# 6. Guardar la respuesta cruda (Capa Raw / Bronce)
# Generamos un texto con la fecha y hora actual para no sobreescribir archivos
momento_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
nombre_archivo = f"data/respuesta_{fecha_ejemplo}_{momento_actual}.json"

# Abrimos un archivo nuevo y escribimos el texto exacto que nos dio la API
with open(nombre_archivo, "w", encoding="utf-8") as archivo:
    archivo.write(respuesta.text)

print(f"\nRespuesta original guardada en: {nombre_archivo}")