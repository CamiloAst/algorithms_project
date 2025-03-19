import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class AcademicScraper:
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    download_path = "C:/Users/jkami/Downloads"
    def __init__(self, debug=True):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Referer': 'https://www.google.com/'
        }
        self.results = []
        self.debug = debug

        # Configuración optimizada para Selenium
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")
        # Añadir opciones adicionales para mejorar la estabilidad
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-notifications")
        self.chrome_options.add_argument("--disable-popup-blocking")
        # self.chrome_options.binary_location = self.brave_path
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        })

    def _log(self, message):
        """Función para imprimir mensajes de depuración"""
        if self.debug:
            print(message)

    def _random_delay(self, min_time=2, max_time=5):
        """Añade un retraso aleatorio para evitar bloqueos por detección de bots"""
        delay = random.uniform(min_time, max_time)
        # delay = 0
        self._log(f"Esperando {delay:.2f} segundos...")
        time.sleep(delay)

    def search_ieee(self, query, max_pages=10):
        """Realiza búsquedas en IEEE Xplore (versión optimizada)"""
        self._log(f"Buscando en IEEE Xplore: {query}")

        try:
            # Inicializar WebDriver con manejador automático
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)

            # Especificar el tiempo de espera implícito
            driver.implicitly_wait(1)

            # Preparar la URL de búsqueda adecuadamente
            encoded_query = query.replace(' ', '+')
            base_url = "https://ieeexplore.ieee.org/search/searchresult.jsp"

            for page in range(max_pages):
                page_url = f"{base_url}?queryText={encoded_query}&pageNumber={page + 1}"
                self._log(f"Accediendo a: {page_url}")

                try:
                    driver.get(page_url)

                    # Esperar a que se cargue la página
                    time.sleep(3)

                    # Verificar si hay algún tipo de modal o popup y cerrarlo si existe
                    try:
                        close_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                             "button.modal-close, button.close, .popup-close")
                        for button in close_buttons:
                            if button.is_displayed():
                                button.click()
                                time.sleep(0)
                    except:
                        pass


                    articles = driver.find_elements(By.CSS_SELECTOR, ".List-results-items")

                    if not articles:
                        self._log("No se encontraron artículos en IEEE con ningún selector conocido.")
                        # Guardar la página para análisis
                        driver.save_screenshot(f"ieee_no_results_page_{page}.png")
                        with open(f"ieee_debug_page_{page}.html", "w", encoding="utf-8") as f:
                            f.write(driver.page_source)
                        continue

                    # Procesar los artículos encontrados
                    for article in articles:
                        title_elem = article.find_element(By.CSS_SELECTOR, "h3 a")
                        title = title_elem.text.strip()

                        if 'href' in title_elem.get_attribute("outerHTML"):
                            link = title_elem.get_attribute("href")
                        else:
                            link = "No disponible"


                        # Buscar autores
                        authors = "No disponible"
                        try:
                            if article.find_element(By.CSS_SELECTOR, "p.author"):
                                authors_elem = article.find_element(By.CSS_SELECTOR, "p.author")
                                authors = authors_elem.text.strip()
                        except NoSuchElementException:
                            pass

                        # Buscar fecha
                        date = "No disponible"
                        date_elem = article.find_element(By.CSS_SELECTOR, "div.publisher-info-container")
                        date = date_elem.text.strip()

                        if len(date) > 4:
                            year_match = re.search(r'\b(19|20)\d{2}\b', date)
                            if year_match:
                                date = year_match.group(0)

                        self.results.append({
                            'Título': title,
                            'Autores': authors,
                            'Fecha': date,
                            'URL': link,
                        })

                    self._log(
                        f"Página {page + 1} de IEEE completada. Artículos encontrados en total: {len(self.results)}")
                    self._random_delay(0, 1)

                except Exception as e:
                    self._log(f"Error al procesar la página {page + 1} de IEEE: {str(e)}")
                    continue

        except Exception as e:
            self._log(f"Error general al procesar IEEE Xplore: {str(e)}")
            import traceback
            self._log(traceback.format_exc())
        finally:
            driver.quit()

    def search_scienceDirect(self, query, max_pages=20):
        self.chrome_options.binary_location = self.brave_path
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option('prefs', {
            "download.default_directory": self.download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        })
        """Realiza búsquedas en ScienceDirect (versión optimizada)"""
        self._log(f"Buscando en ScienceDirect: {query}")

        try:
            # Inicializar WebDriver con manejador automático
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)

            # Especificar el tiempo de espera implícito
            driver.implicitly_wait(1)

            # Preparar la URL de búsqueda adecuadamente
            encoded_query = query.replace(' ', '+')
            base_url = "https://www.sciencedirect.com/search"

            for page in range(max_pages):
                page_url = f"{base_url}?qs={encoded_query}&show=100&sortBy=relevance&articleTypes=FLA&offset={page + 1}"
                self._log(f"Accediendo a: {page_url}")

                try:
                    driver.get(page_url)

                    # Esperar a que se cargue la página
                    time.sleep(3)

                    # Verificar si hay algún tipo de modal o popup y cerrarlo si existe
                    try:
                        close_buttons = driver.find_elements(By.CSS_SELECTOR,
                                                             "button.modal-close, button.close, .popup-close")
                        for button in close_buttons:
                            if button.is_displayed():
                                button.click()
                                time.sleep(0)
                    except:
                        pass

                    articles = driver.find_elements(By.CSS_SELECTOR, ".ResultItem")

                    if not articles:
                        self._log("No se encontraron artículos en ScienceDirect con ningún selector conocido.")
                        # Guardar la página para análisis
                        driver.save_screenshot(f"sciencedirect_no_results_page_{page}.png")
                        with open(f"sciencedirect_debug_page_{page}.html", "w", encoding="utf-8") as f:
                            f.write(driver.page_source)
                        continue

                    # Procesar los artículos encontrados
                    for article in articles:
                        title_elem = article.find_element(By.CSS_SELECTOR, ".result-item-content h2 a")
                        title = title_elem.text.strip()

                        if 'href' in title_elem.get_attribute("outerHTML"):
                            link = title_elem.get_attribute("href")
                        else:
                            link = "No disponible"

                        # Buscar autores
                        authors = "No disponible"
                        try:
                            if article.find_element(By.CSS_SELECTOR, ".Authors"):
                                    authors_elem = article.find_element(By.CSS_SELECTOR, ".author-group")
                                    authors = authors_elem.text.strip()
                        except NoSuchElementException:
                            pass

                        date = "No disponible"
                        date_elem = article.find_element(By.CSS_SELECTOR, ".srctitle-date-fields")
                        date = date_elem.text.strip()
                        if len(date) > 4:
                            year_match = re.search(r'\b(19|20)\d{2}\b', date)
                            if year_match:
                                date = year_match.group(0)

                        self.results.append({
                            'Título': title,
                            'Autores': authors,
                            'Fecha': date,
                            'URL': link,
                        })
                        self._log(
                            f"Página {page + 1} de ScienceDirect completada. Artículos encontrados en total: {len(self.results)}")
                        self._random_delay(0, 1)
                except Exception as e:
                    self._log(f"Error al procesar la página {page + 1} de ScienceDirect: {str(e)}")
                    continue

        except Exception as e:
            self._log(f"Error general al procesar ScienceDirect: {str(e)}")
            import traceback
            self._log(traceback.format_exc())
        finally:
            driver.quit()



    def search_all(self, query, max_pages=183):
        # Limpiar resultados anteriores
        self.results = []

        # IEEE Xplore
        try:
            self.search_ieee(query, max_pages)
            # self.search_scienceDirect(query, max_pages=456)
        except Exception as e:
            self._log(f"Error completo en la base de datos: {str(e)}")
        return self.results
    def save_results(self, filename="articles.csv"):
        """Guarda los resultados en un archivo CSV"""
        if self.results:
            df = pd.DataFrame(self.results)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            self._log(f"Resultados guardados en {filename}")
            return filename
        else:
            self._log("No hay resultados para guardar.")
            return None

    def print_sample_results(self, num_samples=5):
        """Imprime una muestra de los resultados obtenidos"""
        if self.results:
            print("\nEjemplos de resultados encontrados:")
            for i, resultado in enumerate(self.results[:num_samples]):
                print(f"\nResultado {i + 1}:")
                print(f"Título: {resultado['Título']}")
                print(f"Autores: {resultado['Autores']}")
        else:
            print("\nNo se encontraron resultados.")


# Ejemplo de uso
if __name__ == "__main__":
    scraper = AcademicScraper(debug=True)

    # Buscar el término específico
    query = "computational thinking"
    resultados = scraper.search_all(query)

    # Guardar resultados
    archivo = scraper.save_results("articles.csv")

    # Mostrar muestra de resultados
    scraper.print_sample_results()