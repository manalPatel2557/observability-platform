from storage.elasticsearch_client import es

INDEX_NAME = "logs"


def save_log(document: dict):

    response = es.index(
        index=INDEX_NAME,
        document=document
    )

    return response["_id"]
