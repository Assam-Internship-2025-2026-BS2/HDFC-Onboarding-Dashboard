import clickhouse_connect

def get_client():

    client = clickhouse_connect.get_client(
        host="localhost",
        port=8123,
        username="default",
        password="REstart@789"
    )

    return client