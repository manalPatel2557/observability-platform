from fastapi import APIRouter

from app.services.elasticsearch_service import es


router = APIRouter(
    prefix="/logs",
    tags=["logs"]
)


@router.get("")
def get_logs():

    response = es.search(
        index="logs",
        size=50,
        sort=[
            {
                "timestamp": {
                    "order": "desc"
                }
            }
        ]
    )

    return {
        "count": len(response["hits"]["hits"]),
        "logs": [
            hit["_source"]
            for hit in response["hits"]["hits"]
        ]
    }
