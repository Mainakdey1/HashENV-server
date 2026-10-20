from psycopg2 import OperationalError, InterfaceError
from psycopg2.extras import execute_values
from ..services.db_connection_service import get_connection, release_connection

def check_device_token(device_token_id) -> bool:

    conn =  get_connection()
    discard = False
    try:
        with conn.cursor() as cursor:

            cursor.execute(
                """
                SELECT EXISTS (
                    SELECT 1
                    FROM device_tokens
                    WHERE device_token = %s
                )
                """,
                (device_token_id,)
            )
            return cursor.fetchone()[0]

    except (OperationalError, InterfaceError):
        conn.rollback()
        discard = True
        raise
    finally:
        release_connection(conn, discard=discard)