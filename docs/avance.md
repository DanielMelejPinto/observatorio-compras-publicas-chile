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

## Hito 7: Orquestacion y Automatizacion con Apache Airflow
**Fecha:** 13 de octubre de 2026

Para eliminar la ejecucion manual de scripts y simular un entorno de produccion continuo, integre Apache Airflow al ecosistema contenerizado de Docker.

### 1. Infraestructura y Redes
Incorpore el servicio de Airflow (`apache/airflow:2.8.3-python3.9`) al archivo `docker-compose.yml` en modo `standalone`. Esto permitio que el programador (Scheduler) y el servidor web corrieran en el puerto 8080 compartiendo la misma red interna de Docker con PostgreSQL y Metabase. Cree un archivo `transformacion/profiles.yml` autocontenido para que Airflow pudiera invocar dbt apuntando al host `base_de_datos`.

### 2. Diseno del Grafo Aciclico Dirigido (DAG)
Programe el pipeline en `dags/dag_compras_publicas.py` con frecuencia diaria (`@daily`) utilizando 4 tareas encadenadas:
`extraer_datos_api >> cargar_datos_postgres >> transformar_con_dbt >> validar_calidad_con_dbt`

### 3. Resolucion de Desafio Tecnico (Integridad Referencial en PostgreSQL)
Durante la ejecucion inicial, la tarea de carga fallo porque Pandas con `if_exists='replace'` ejecutaba un `DROP TABLE ordenes_brutas`. PostgreSQL impidio la eliminacion debido a que la vista de dbt (`ordenes_transformadas`) dependia de ella.
Resolvi este problema aplicando el patron estandar de ingenieria de datos: sustitui la destruccion de la tabla por una sentencia `TRUNCATE TABLE ordenes_brutas` dentro de una transaccion (`motor.begin()`) seguido de `if_exists='append'`. Esto garantizo la idempotencia sin romper las vistas dependientes ni interrumpir los dashboards de Metabase.

### 4. Resultado
El DAG completo se ejecuto exitosamente en verde. El flujo completo (Extraccion API -> Carga SQL -> Transformacion dbt -> Validacion dbt test) quedo automatizado y monitoreable desde la interfaz web de Airflow.

## Hito 8: Integracion Continua y Pruebas Automatizadas (CI/CD con GitHub Actions)
**Fecha:** 13 de octubre de 2026

Para adoptar las mejores practicas de la cultura DataOps y asegurar que ningun cambio en el codigo rompa los pipelines existentes, implemente Integracion Continua (CI) mediante GitHub Actions.

### 1. Diseno del Flujo de Trabajo
Configure el archivo `.github/workflows/ci.yml` para activarse automaticamente ante cualquier `push` o `pull request` sobre la rama `main`. El pipeline aprovisiona un entorno virtual en la nube (Ubuntu) con Python 3.9 e instala las dependencias de testing.

### 2. Bateria de Pruebas Automatizadas
El flujo ejecuta tres barreras de control de calidad secuenciales:
* **Analisis Estatico y Sintaxis (Flake8):** Examina el codigo Python para detectar errores de sintaxis critica, variables no definidas o importaciones rotas antes de la ejecucion.
* **Prueba de Integridad del DAG (Airflow DagBag):** Utiliza la clase `DagBag` para cargar el pipeline de compras publicas en memoria sin ejecutarlo, verificando mediante una asercion (`assert len(bag.import_errors) == 0`) que no existan ciclos infinitos, errores de dependencias ni fallas de sintaxis en los operadores.
* **Parseo y Compilacion de Modelos (dbt parse):** Valida que la estructura del proyecto dbt, los modelos SQL (`ordenes_transformadas.sql`) y las definiciones de pruebas (`schema.yml`) cumplan con los estandares de compilacion sin requerir una conexion a base de datos activa.

### 3. Insignia de Calidad (Build Badge)
Incorpore una insignia dinamica en el archivo `README.md` que refleja en tiempo real el estado de las pruebas (passing/failing), certificando la robustez y calidad de la plataforma.

## Nota de calidad de datos: correccion del mapeo de estados
Al revisar el dashboard, la categoria "Otro Estado" concentraba cerca del 40% de las ordenes. Contraste el `CASE WHEN` con la documentacion oficial de la API y detecte que habia mezclado los codigos de licitaciones con los de ordenes de compra (la Aceptada es el codigo 6, no el 8). Corregi el modelo de dbt y `analisis.sql`, y valide que los 19.897 registros siguieran sumando igual tras el cambio.
