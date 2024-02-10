
import airflow
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta
from pendulum import date
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json

# Grab the current date
current_date = datetime.today().strftime('%Y-%m-%d')

# Default settings for all the dags in the pipeline
default_args = {
    "owner": "Airflow",
    "start_date": datetime(2024, 2, 10),
    "retries": 1,
    "retry_delay": timedelta(minutes=15)
}

with DAG('forex_pipeline', default_args=default_args, schedule_interval=timedelta(minutes=60), catchup=False) as dag:
    # Dag #1 - Check if the API is available 
    # https://data.fixer.io/api/latest?access_key=ab0595c54ddd27a18727b106e22896a5
    is_api_available = HttpSensor(
        task_id='is_api_available',
        method='GET',
        http_conn_id='is_api_available',
        endpoint='/api/latest?access_key=ab0595c54ddd27a18727b106e22896a5',
        response_check=lambda response: 'EUR' in response.text,
        poke_interval=5
    )

  # Dag #2 - Create a table
    create_table = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id='postgres',
        sql='''
            drop table if exists rates;
            create table rates(
                rate float not null,
                symbol text not null
            );
        '''
    )


    # DAG #3 - Extract Data
    extract_data = SimpleHttpOperator(
            task_id = 'extract_user',
            http_conn_id='is_api_available',
            method='GET',
            endpoint='/api/latest?access_key=ab0595c54ddd27a18727b106e22896a5',
            response_filter=lambda response: json.loads(response.text),
            log_response=True
    )

    
    # Dependencies
    is_api_available >> create_table >> extract_data
