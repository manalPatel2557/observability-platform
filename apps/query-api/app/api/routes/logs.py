from datetime import datetime
from typing import Optional

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


@router.get("/search")
def search_logs(
    service: Optional[str] = None,
    level: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    message: Optional[str] = None,
):

    filters = []
    must_clauses = []

    if service:
        filters.append(
            {
                "term": {
                    "service.keyword": service
                }
            }
        )

    if level:
        filters.append(
            {
                "term": {
                    "level.keyword": level
                }
            }
        )

    range_filter = {}

    if start_time:
        range_filter["gte"] = start_time.isoformat()

    if end_time:
        range_filter["lte"] = end_time.isoformat()

    if range_filter:
        filters.append(
            {
                "range": {
                    "timestamp": range_filter
                }
            }
        )

    if message:
        must_clauses.append(
            {
                "match": {
                    "message": message
                }
            }
        )

    query = {
        "bool": {
            "filter": filters,
            "must": must_clauses
        }
    }

    response = es.search(
        index="logs",
        query=query,
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
