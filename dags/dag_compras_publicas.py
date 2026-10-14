from datetime import datetime, timedelta
import json
import os
from dotenv import load_dotenv
import pandas as pd
import requests
from sqlalchemy import create_engine, text

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Argumentos por defecto del pipeline
default_args = {
    'owner': 'daniel_melej',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# Definicion del Grafo Aciclico Dirigido (DAG)
with DAG(
    dag_id='pipeline_observatorio_compras',
    default_args=default_args,
    description='Pipeline ETL y de modelado de datos para Compras Publicas de Chile',
    schedule='@daily',
    catchup=False,
    tags=['ingenieria_de_datos', 'mercado_publico', 'dbt']
) as dag:

    # 1. Extraccion desde la API
    def extraer_datos_mercado_publico():
        load_dotenv('/opt/airflow/.env')
        ticket = os.getenv("TICKET_MERCADO_PUBLICO")
        
        # Fecha de prueba para el flujo diario
        url = f"https://api.mercadopublico.cl/servicios/v1/publico/ordenesdecompra.json?fecha=02012024&ticket={ticket}"
        respuesta = requests.get(url, timeout=30)
        
        if respuesta.status_code == 200:
            ruta_archivo = "/opt/airflow/data/respuesta_airflow.json"
            with open(ruta_archivo, "w", encoding="utf-8") as archivo:
                json.dump(respuesta.json(), archivo)
            print(f"Extraccion exitosa. Archivo guardado en {ruta_archivo}")
        else:
            raise Exception(f"Fallo en la API de Mercado Publico. Status: {respuesta.status_code}")

    # 2. Inyeccion hacia PostgreSQL
    def cargar_datos_a_postgres():
        ruta_archivo = "/opt/airflow/data/respuesta_airflow.json"
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
            
        df = pd.DataFrame(datos["Listado"])
        
        motor = create_engine('postgresql://admin:password123@base_de_datos:5432/compras_publicas')
        
        # Vaciamos los registros anteriores con TRUNCATE y transaccion asegurada (begin)
        # Esto evita borrar la tabla completa y mantiene intacta la vista de dbt
        with motor.begin() as conexion:
            conexion.execute(text("TRUNCATE TABLE ordenes_brutas;"))
        
        # Insertamos los nuevos datos sobre la tabla existente
        df.to_sql('ordenes_brutas', con=motor, if_exists='append', index=False)
        print(f"Carga exitosa de {len(df)} registros en ordenes_brutas")

    # Declaracion de Tareas
    tarea_extraccion = PythonOperator(
        task_id='extraer_datos_api',
        python_callable=extraer_datos_mercado_publico
    )

    tarea_carga = PythonOperator(
        task_id='cargar_datos_postgres',
        python_callable=cargar_datos_a_postgres
    )

    tarea_dbt_run = BashOperator(
        task_id='transformar_con_dbt',
        bash_command='dbt run --project-dir /opt/airflow/transformacion --profiles-dir /opt/airflow/transformacion'
    )

    tarea_dbt_test = BashOperator(
        task_id='validar_calidad_con_dbt',
        bash_command='dbt test --project-dir /opt/airflow/transformacion --profiles-dir /opt/airflow/transformacion'
    )

    # Definicion del flujo de dependencias
    tarea_extraccion >> tarea_carga >> tarea_dbt_run >> tarea_dbt_test