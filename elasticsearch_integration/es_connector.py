import os
from dotenv import dotenv_values
from elasticsearch import Elasticsearch

env_vars = dotenv_values()

def create_es_connection():
    es = Elasticsearch(
        hosts=[{
            'host': env_vars["ELASTICSEARCH_HOST"],
            'port': int(env_vars["ELASTICSEARCH_PORT"]),
            'scheme': 'https'
        }],
        http_auth=(env_vars["ELASTICSEARCH_USERNAME"], env_vars["ELASTICSEARCH_PASSWORD"]),
        verify_certs=bool(env_vars.get("ELASTICSEARCH_VERIFY_CERTS", "True").lower() == "true"),
    )
    return es
