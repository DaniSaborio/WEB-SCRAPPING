# scheduler.py (extracto conceptual)
# Asegúrate de importar lo necesario para la BD
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
    # ... (tu función get_db_connection existente) ...
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

# Ejemplo de cómo lo usarías en tu scheduler/scraper:

def run_scraping_job():
    print("Iniciando trabajo de scraping...")
    try:
        # Aquí iría tu lógica real de scraping y guardado en DB
        # ... (llama a tu scraper_dynamic.py, scraper_static.py, etc.) ...

        # Después de que el scraping termine exitosamente:
        log_event('Scraping Completado', 'El proceso de scraping de Steam ha finalizado exitosamente.')
        # Puedes añadir lógica para contar nuevos/modificados/eliminados y pasarlos en la descripción
        # Por ejemplo:
        # new_items = count_newly_added_items()
        # log_event('Nuevo Producto', f'{new_items} nuevos productos detectados.', related_table='scrapped_steam')

    except Exception as e:
        print(f"Error en el trabajo de scraping: {e}")
        log_event('Error en Scraping', f'Ocurrió un error durante el scraping: {e}')

# Ejemplo de cómo se llamaría en tu scheduler
# from apscheduler.schedulers.blocking import BlockingScheduler
# scheduler = BlockingScheduler()
# scheduler.add_job(run_scraping_job, 'interval', hours=1)
# scheduler.start()