import os
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd

GOOGLE_APPLICATION_CREDENTIALS = 'GOOGLE_APPLICATION_CREDENTIALS'

GOOGLE_APPLICATION_CREDENTIALS_PATH = os.environ.get(GOOGLE_APPLICATION_CREDENTIALS)
BQ_CREDENTIALS = service_account.Credentials.from_service_account_file(GOOGLE_APPLICATION_CREDENTIALS_PATH)

client = bigquery.Client(credentials=BQ_CREDENTIALS)
table_id = "p2p-data-warehouse.solana.all_stSOL_pools"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("blocktime", bigquery.enums.SqlTypeNames.STRING),  # todo:change datatype to datetime (useanother unix timestamp reading method)
        bigquery.SchemaField("token", bigquery.enums.SqlTypeNames.STRING),
        bigquery.SchemaField("balance", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("Price", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("usd_price", bigquery.enums.SqlTypeNames.FLOAT64),
        bigquery.SchemaField("pool_id", bigquery.enums.SqlTypeNames.STRING)
    ],

)

all_pools_data=pd.read_csv('All_pools_file.csv')

job = client.load_table_from_dataframe(all_pools_data, table_id, job_config=job_config)

print(job.result())