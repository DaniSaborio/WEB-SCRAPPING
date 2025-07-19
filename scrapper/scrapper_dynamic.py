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

# ChromeDriverManager!
from webdriver_manager.chrome import ChromeDriverManager


#PATH TO THE BINARY CHROME
CHROME_BINARY_PATH = '/opt/google/chrome/google-chrome'
STEAM_URL = "https://store.steampowered.com"




#INITIALIZE THE WEBDRIVER/OPTIONS AND SERVICE

service = ChromeService(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=Options())


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

except Exception as e:
    print(f"Ocurrió un error: {e}")
finally:
    if driver:
        driver.quit()
        print("Navegador cerrado.")
  