import os
import requests
from dotenv import load_dotenv

# 1. Cargar el ticket
load_dotenv()
ticket = os.getenv("TICKET_MERCADO_PUBLICO", "")

# 2. Los 3 códigos reales que sacamos de tu exploración anterior
codigos_prueba = ["1002588-584-SE23", "1002588-603-SE23", "1002588-643-AG23"]

print("--- EXTRAYENDO DETALLES DE COMPRAS ---")

# 3. El ciclo "for" (Bucle): Repetimos la accion por cada codigo en la lista
for codigo in codigos_prueba:
    
    # OJO AQUI: Ahora la URL usa "?codigo=" en vez de "?fecha="
    url_detalle = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?codigo={codigo}&ticket={ticket}" 
    
    respuesta = requests.get(url_detalle)
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        
        # El nivel de detalle viene escondido dentro de "Listado" en la posicion 0
        orden_detalle = datos["Listado"][0]
        
        # Extraemos lo que nos importa
        comprador = orden_detalle["Comprador"]["NombreOrganismo"]
        monto = orden_detalle["TotalNeto"]
        
        print(f"Orden: {codigo} | Comprador: {comprador} | Monto Neto: ${monto}")
    else:
        print(f"Error al buscar la orden {codigo}")