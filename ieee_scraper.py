from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Configuración
IEEE_URL = "https://ieeexplore-ieee-org.crai.referencistas.com/search/searchresult.jsp?newsearch=true&queryText=computational%20thinking"
DOWNLOAD_DIR = os.path.abspath("descargas_ieee")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configuración de Chrome con descarga automática
chrome_options = Options()
chrome_options.add_argument(r"--user-data-dir=C:\Users\Camilo\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument("--profile-directory=Default")  # o "Profile 1", según tu caso
# No usar headless para permitir sesión activa
prefs = {
    "download.default_directory": DOWNLOAD_DIR,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# Iniciar búsqueda con sesión iniciada en CRAI
print("Abriendo IEEE Xplore con sesión CRAI...")
driver.get(IEEE_URL)
time.sleep(10)

pagina = 1
while True:
    print(f"Procesando página {pagina}...")

    # Cambiar a 100 artículos por página si es posible
    try:
        items_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Items Per Page')]"))
        )
        items_button.click()
        option_100 = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'100')]"))
        )
        option_100.click()
        time.sleep(5)
    except:
        print("No se pudo cambiar la cantidad de ítems por página.")

    # Seleccionar todos los resultados de la página
    try:
        checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox' and @aria-label='Select all search results']")
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(2)
    except:
        print("No se pudo seleccionar todos los resultados.")

    # Hacer clic en Export
    try:
        export_button = driver.find_element(By.XPATH, "//button[contains(text(),'Export')]")
        export_button.click()
        time.sleep(2)

        download_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "stats-SearchResults_Download"))
        )
        download_button.click()
        print(f"CSV exportado para página {pagina}.")
        time.sleep(10)
    except Exception as e:
        print(f"Error al exportar CSV: {e}")

    # Verificar si hay botón "Next"
    try:
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Next')]" )
        if next_btn.is_enabled():
            next_btn.click()
            pagina += 1
            time.sleep(8)
        else:
            print("No hay más páginas.")
            break
    except:
        print("Botón siguiente no encontrado. Fin del recorrido.")
        break

print("\n✅ Proceso terminado. Los archivos .csv fueron descargados en:", DOWNLOAD_DIR)
driver.quit()
