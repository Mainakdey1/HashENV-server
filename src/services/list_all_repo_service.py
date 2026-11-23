from psycopg2 import OperationalError, InterfaceError
from psycopg2.extras import execute_values
from ..services.db_connection_service import get_connection, release_connection

def list_all_repositories():

    conn =  get_connection()
    discard = False
    try:
        with conn.cursor() as cursor:

            cursor.execute( 
                           """
                            SELECT DISTINCT project_name
                            from test_envs;
                           """)
            repositories = cursor.fetchall()
            return [row[0] for row in repositories]

    except (OperationalError, InterfaceError):
        discard = True
        raise
    finally:
        release_connection(conn, discard=discard)