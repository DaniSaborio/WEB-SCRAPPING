import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('PG_DB')
DB_USER = os.getenv('PG_USER')
DB_PASSWORD = os.getenv('PG_PASSWORD')
DB_HOST = os.getenv('PG_HOST')
DB_PORT = os.getenv('PG_PORT')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def log_event(event_type, description, related_id=None, related_table=None):
    """Función para registrar un evento en la tabla event_logs."""
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO event_logs (event_type, description, related_id, related_table)
                VALUES (%s, %s, %s, %s);
                """,
                (event_type, description, related_id, related_table)
            )
            conn.commit()
            print(f"Evento registrado: {event_type} - {description}")
    except psycopg2.Error as e:
        print(f"Error al registrar evento: {e}")
    finally:
        if conn:
            conn.close()

def run_scraping_job():
    print("Iniciando trabajo de scraping...")
    try:
        log_event('Scraping Completado', 'El proceso de scraping de Steam ha finalizado exitosamente.')

    except Exception as e:
        print(f"Error en el trabajo de scraping: {e}")
        log_event('Error en Scraping', f'Ocurrió un error durante el scraping: {e}')
