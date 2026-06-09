from elasticsearch import Elasticsearch

from app.core.config import settings


es = Elasticsearch(
    f"http://{settings.elastic_host}:{settings.elastic_port}"
)
