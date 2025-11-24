# /agent-data-engineer

Expert data engineer for pipelines and infrastructure.

## ETL Pipeline
```python
# Airflow DAG
from airflow import DAG
from airflow.operators.python import PythonOperator

with DAG('etl_pipeline', schedule='@daily') as dag:

    def extract():
        return fetch_from_source()

    def transform(data):
        return clean_and_transform(data)

    def load(data):
        write_to_warehouse(data)

    extract_task = PythonOperator(task_id='extract', python_callable=extract)
    transform_task = PythonOperator(task_id='transform', python_callable=transform)
    load_task = PythonOperator(task_id='load', python_callable=load)

    extract_task >> transform_task >> load_task
```

## dbt Model
```sql
-- models/users_daily.sql
{{ config(materialized='incremental') }}

SELECT
    user_id,
    DATE(created_at) as date,
    COUNT(*) as actions
FROM {{ ref('raw_events') }}
{% if is_incremental() %}
WHERE created_at > (SELECT MAX(date) FROM {{ this }})
{% endif %}
GROUP BY 1, 2
```

## Spark
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ETL").getOrCreate()
df = spark.read.parquet("s3://bucket/data/")
result = df.groupBy("category").agg({"value": "sum"})
result.write.parquet("s3://bucket/output/")
```
