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

## Hito 4: Analítica de Datos y SQL
**Fecha:** 4 de octubre de 2026
- **Tarea completada:** Exploración de base de datos utilizando la herramienta estándar de la industria (DBeaver).
- **Consultas realizadas:** Uso de `SELECT`, `GROUP BY` y lógica condicional `CASE WHEN` para traducir y agregar estados de órdenes de compra, generando nuestro primer indicador de negocio.

## Hito 5: Tableros Visuales y Business Intelligence
**Fecha:** 4 de octubre de 2026
- **Tarea completada:** Implementación de Metabase en el ecosistema Docker para creación de Dashboards.
- **Arquitectura:** Se integró Metabase a `docker-compose.yml` para lectura en vivo desde PostgreSQL sin duplicar datos.
- **Visualización:** Creación del primer panel interactivo (Dashboard) traduciendo consultas SQL a gráficos de negocio para tomadores de decisiones.

## Hito 6: Transformacion Profesional de Datos (dbt)
**Fecha:** 13 de octubre de 2026

Para llevar la calidad de los datos al nivel de produccion y automatizar la limpieza, implemente dbt (Data Build Tool), el estandar actual de Analytics Engineering.

### 1. Inicializacion y Conexion
Instale el adaptador `dbt-postgres` en mi entorno virtual. Con `dbt init`, genere la estructura base del proyecto y configure el perfil para conectar con el contenedor de PostgreSQL en Docker. Valide la conectividad exitosamente mediante `dbt debug`.

### 2. Modelado de Datos y Estandarizacion Snake_Case
Cree el modelo `models/ordenes_transformadas.sql` trasladando la logica condicional (`CASE WHEN`). 
Durante las pruebas enfrente un desafio tecnico real: PostgreSQL convierte identificadores no entrecomillados a minusculas, causando incompatibilidad con los nombres originales de la API que tenian mayusculas (`Codigo`, `CodigoEstado`). Aplique la mejor practica de la industria: estandarice todas las columnas a `snake_case` (`codigo`, `nombre`, `codigo_estado`, `descripcion_estado`), eliminando la necesidad de usar comillas dobles.

### 3. Compilacion y Ejecucion
Al ejecutar `dbt run`, dbt compilo el codigo y PostgreSQL construyo automaticamente una Vista (`public.ordenes_transformadas`). Esto permite que herramientas analiticas como Metabase consuman la capa limpia directamente sin recalcular reglas de negocio al vuelo.

### 4. Pruebas de Calidad de Datos (Data Quality Tests)
Cree el archivo `models/schema.yml` para auditar la integridad de la vista. Defini pruebas de unicidad (`unique`) y no nulidad (`not_null`) sobre la clave primaria `codigo`, asi como validaciones de presencia en los estados.
Al correr `dbt test`, el sistema ejecuto 4 consultas de asercion sobre PostgreSQL, pasando exitosamente con `PASS=4 WARN=0 ERROR=0`, garantizando que no existan duplicados ni datos huerfanos.