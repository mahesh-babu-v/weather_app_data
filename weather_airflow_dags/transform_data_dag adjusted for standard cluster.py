from datetime import datetime, timedelta
import uuid
from airflow import DAG
# from airflow.providers.google.cloud.operators.dataproc import DataprocCreateBatchOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator

# DAG default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 5, 15),
}

# Define the DAG
with DAG(
    dag_id="transformed_weather_data_to_bq",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # # Generate a unique batch ID using UUID
    # batch_id = f"weather-data-batch-{str(uuid.uuid4())[:8]}"  # Shortened UUID for brevity

    # # Submit PySpark job to Dataproc Serverless
    # batch_details = {
    #     "pyspark_batch": {
    #         "main_python_file_uri": f"gs://weather-data-gcp/script/weather_data_processing.py",
    #         "python_file_uris": [],
    #         "jar_file_uris": [],
    #         "args": []
    #     },
    #     "runtime_config": {
    #         "version": "2.2",
    #     },
    #     "environment_config": {
    #         "execution_config": {
    #             "service_account": "1083548207078-compute@developer.gserviceaccount.com",
    #             "network_uri": "projects/airy-advantage-462109-h1/global/networks/default",
    #             "subnetwork_uri": "projects/airy-advantage-462109-h1/regions/us-central1/subnetworks/default",
               
    #         }
    #     },
         
    # }

    # pyspark_task = DataprocCreateBatchOperator(
    #     task_id="spark_job_on_dataproc_serverless",
    #     batch=batch_details,
    #     batch_id=batch_id,
    #     project_id="airy-advantage-462109-h1",
    #     region="us-central1",
    #     gcp_conn_id="google_cloud_default",
    # )

    # # Task Dependencies
    # pyspark_task


    

    # Job configuration for cluster-based execution
    job_details = {
        "reference": {"project_id": "airy-advantage-462109-h1"},
        "placement": {"cluster_name": "cluster-demo"},
        "pyspark_job": {
            "main_python_file_uri": "gs://weather-data-gcp/script/weather_data_processing.py",
            "args": [],
            "python_file_uris": [],  # Additional .py files if any
            "jar_file_uris": [],     # Additional JARs if any
        },
    }

    # Airflow Task for Dataproc cluster-based job
    pyspark_task = DataprocSubmitJobOperator(
        task_id="submit_spark_job_to_cluster",
        job=job_details,
        region="us-central1",
        project_id="airy-advantage-462109-h1",
        gcp_conn_id="google_cloud_default",
    )


    # Task Dependencies
    pyspark_task