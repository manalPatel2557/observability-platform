from redis import Redis
from storage.log_repository import save_log

STREAM_NAME = "logs-stream"
GROUP_NAME = "log-processors"
CONSUMER_NAME = "consumer-1"

redis_client = Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    socket_timeout=None,
    socket_connect_timeout=5
)

def create_group():
    try:
        redis_client.xgroup_create(
            STREAM_NAME,
            GROUP_NAME,
            id="0",
            mkstream=True
        )
        print(f"Created group: {GROUP_NAME}")
    except Exception:
        print("Consumer group already exists")

def consume():
    while True:
        try:

            messages = redis_client.xreadgroup(
                groupname=GROUP_NAME,
                consumername=CONSUMER_NAME,
                streams={STREAM_NAME: ">"},
                count=10,
                block=5000
            )

            if not messages:
                continue

            for stream_name, stream_messages in messages:

                for message_id, data in stream_messages:

                    document_id = save_log(data)

                    print("\n===================")
                    print("MESSAGE ID:", message_id)
                    print("ELASTICSEARCH ID:", document_id)
                    print("DATA:", data)
                    print("===================\n")

                    redis_client.xack(
                        STREAM_NAME,
                        GROUP_NAME,
                        message_id
                    )

        except Exception as e:
            print("Worker error:", e)

if __name__ == "__main__":
    create_group()
    consume()
