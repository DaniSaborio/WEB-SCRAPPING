from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # Seguimos importando Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import tempfile
import shutil
import os

# ¡Importa ChromeDriverManager!
from webdriver_manager.chrome import ChromeDriverManager


# --- Configuración del WebDriver ---
# Ya no necesitamos CHROMEDRIVER_PATH manual
# La ruta del binario de Chrome (la más común en Linux después de instalar con yay/pacman)
CHROME_BINARY_PATH = '/opt/google/chrome/google-chrome'
STEAM_URL = "https://store.steampowered.com"

# Configurar las opciones de Chrome
options = Options()
options.binary_location = CHROME_BINARY_PATH # Apuntamos a Chrome
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Crea un directorio temporal para el perfil de usuario de Chrome
user_data_dir = tempfile.mkdtemp()
options.add_argument(f"--user-data-dir={user_data_dir}")


# *** ¡CAMBIO CRUCIAL AQUÍ! ***
# Usamos ChromeDriverManager para descargar y obtener la ruta del ChromeDriver compatible.
# No necesitamos pasar el executable_path a Service, webdriver-manager lo maneja.
service = ChromeService(ChromeDriverManager().install())

# Inicializamos el driver, pasando tanto el servicio como las opciones.
driver = webdriver.Chrome(service=service, options=options)

# --- (el resto de tu script) ---

try:
    print(f"Yendo a {STEAM_URL}")
    driver.get(STEAM_URL)

    # Esperar hasta que el logo de Steam esté presente y hacer clic
    logo_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//img[@alt='STEAM']"))
    )
    logo_element.click()
    print("LISTO")

    # Aquí podrías añadir un tiempo de espera para depuración
    time.sleep(5)

    # Si necesitas Beautiful Soup:
    # soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup.prettify())

except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    if driver:
        driver.quit()
        print("Navegador cerrado.")
    # Limpiar el directorio temporal
    if user_data_dir and os.path.exists(user_data_dir):
        try:
            shutil.rmtree(user_data_dir)
            print(f"Directorio temporal '{user_data_dir}' eliminado.")
        except Exception as e:
            print(f"No se pudo eliminar el directorio temporal: {e}")