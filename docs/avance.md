# Registro de Avance

## Hito 0: Problema, alcance y repositorio
**Fecha:** 2 de octubre de 2026
- **Tarea completada:** Creación del repo en GitHub, redacción de README inicial y registro de avance.

## Hito 1: Python y exploración de una muestra
**Fecha:** 2 de octubre de 2026
- **Tarea completada:** Creación de entorno virtual (`venv`), script de exploración inicial con Pandas filtrando datos ficticios y creación del diccionario de datos.

## Hito 2: Extracción y conservación de datos originales
**Fecha:** 2 de octubre de 2026
- **Tarea completada:** Conexión a la API real de Mercado Público mediante el uso de variables de entorno ocultas (`.env`). Descarga exitosa de más de 10.000 órdenes diarias.
- **Descubrimiento:** La API sigue un patrón Resumen-Detalle. Exploramos el detalle de 3 órdenes usando bucles `for` y logramos extraer el comprador y los montos netos.

## Hito 3: PostgreSQL y carga repetible
**Fecha:** 2 de octubre de 2026
- **Tarea completada:** Creación de archivo `docker-compose.yml` para levantar un servidor PostgreSQL local. Desarrollo del script `carga.py` usando SQLAlchemy para inyectar más de 10.000 registros mediante Pandas (`to_sql`).
- **Verificación:** Ejecución exitosa de una consulta SQL validando que el total de filas coincide exactamente con los códigos únicos de las órdenes, confirmando una carga sin duplicados.