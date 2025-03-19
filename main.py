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

    def _log(self, message):
        """Función para imprimir mensajes de depuración"""
        if self.debug:
            print(message)

    def _random_delay(self, min_time=2, max_time=5):
        """Añade un retraso aleatorio para evitar bloqueos por detección de bots"""
        # delay = random.uniform(min_time, max_time)
        delay = 0
        self._log(f"Esperando {delay:.2f} segundos...")
        time.sleep(delay)

    def search_ieee(self, query, max_pages=2):
        """Realiza búsquedas en IEEE Xplore (versión optimizada)"""
        self._log(f"Buscando en IEEE Xplore: {query}")

        try:
            # Inicializar WebDriver con manejador automático
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)

            # Especificar el tiempo de espera implícito
            driver.implicitly_wait(0)

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
                                time.sleep(1)
                    except:
                        pass

                    # Intentar encontrar los resultados con varios selectores
                    article_selectors = [
                        ".List-results-items",
                        ".article-list-item",
                        ".search-results-item",
                        ".List-results li",
                        ".results-container .article",
                        "div[data-testid='results-item']"
                    ]

                    articles = []
                    for selector in article_selectors:
                        try:
                            found_articles = driver.find_elements(By.CSS_SELECTOR, selector)
                            if found_articles:
                                articles = found_articles
                                self._log(f"Encontrados artículos con el selector: {selector}")
                                break
                        except:
                            continue

                    if not articles:
                        self._log("No se encontraron artículos en IEEE con ningún selector conocido.")
                        # Guardar la página para análisis
                        driver.save_screenshot(f"ieee_no_results_page_{page}.png")
                        with open(f"ieee_debug_page_{page}.html", "w", encoding="utf-8") as f:
                            f.write(driver.page_source)
                        continue

                    # Procesar los artículos encontrados
                    for article in articles:
                        try:
                            # Buscar título con varios selectores
                            title = "No disponible"
                            title_selectors = [
                                "h3.result-item-title",
                                ".title",
                                ".article-title",
                                "h2 a",
                                "h3 a",
                                ".detail-item-title"
                            ]

                            for selector in title_selectors:
                                try:
                                    title_elem = article.find_element(By.CSS_SELECTOR, selector)
                                    if title_elem:
                                        title = title_elem.text.strip()
                                        break
                                except:
                                    continue

                            # Buscar enlace
                            link = "No disponible"
                            try:
                                # Si encontramos título con un elemento <a>
                                for selector in title_selectors:
                                    try:
                                        link_elem = article.find_element(By.CSS_SELECTOR, selector)
                                        if 'href' in link_elem.get_attribute("outerHTML"):
                                            link = link_elem.get_attribute("href")
                                            break
                                    except:
                                        continue

                                # Si no, buscar cualquier enlace que apunte a un documento
                                if link == "No disponible":
                                    link_selectors = [
                                        "a[href*='/document/']",
                                        "a[href*='/abstract/']",
                                        "a.result-item-title"
                                    ]
                                    for selector in link_selectors:
                                        try:
                                            link_elem = article.find_element(By.CSS_SELECTOR, selector)
                                            link = link_elem.get_attribute("href")
                                            break
                                        except:
                                            continue
                            except:
                                pass

                            # Buscar autores
                            authors = "No disponible"
                            author_selectors = [
                                "p.author",
                                ".authors",
                                ".author-names",
                                ".author-list",
                                ".details-authors"
                            ]

                            for selector in author_selectors:
                                try:
                                    authors_elem = article.find_element(By.CSS_SELECTOR, selector)
                                    authors = authors_elem.text.strip()
                                    break
                                except:
                                    continue

                            # Buscar fecha
                            date = "No disponible"
                            date_selectors = [
                                "div.publisher-info-container",
                                ".publication-year",
                                ".meta-date",
                                ".details-pub-date",
                                ".year"
                            ]

                            for selector in date_selectors:
                                try:
                                    date_elem = article.find_element(By.CSS_SELECTOR, selector)
                                    date = date_elem.text.strip()
                                    # Si encontramos una fecha, intentar extraer solo el año si es extenso
                                    if len(date) > 4:
                                        year_match = re.search(r'\b(19|20)\d{2}\b', date)
                                        if year_match:
                                            date = year_match.group(0)
                                    break
                                except:
                                    continue

                            self.results.append({
                                'Título': title,
                                'Autores': authors,
                                'Fecha': date,
                                'URL': link,
                                'Fuente': 'IEEE Xplore'
                            })
                        except Exception as e:
                            self._log(f"Error al procesar artículo individual de IEEE: {str(e)}")
                            continue

                    self._log(
                        f"Página {page + 1} de IEEE completada. Artículos encontrados en total: {len(self.results)}")
                    self._random_delay(3, 6)

                except Exception as e:
                    self._log(f"Error al procesar la página {page + 1} de IEEE: {str(e)}")
                    continue

        except Exception as e:
            self._log(f"Error general al procesar IEEE Xplore: {str(e)}")
            import traceback
            self._log(traceback.format_exc())
        finally:
            driver.quit()

    def search_arxiv(self, query, max_results=50):
        """Búsqueda en arXiv usando la API"""
        self._log(f"Buscando en arXiv: {query}")

        try:
            # Preparar la consulta
            encoded_query = query.replace(' ', '+')
            base_url = "http://export.arxiv.org/api/query"

            params = {
                'search_query': f'all:{encoded_query}',
                'start': 0,
                'max_results': max_results,
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }

            response = requests.get(base_url, params=params, headers=self.headers)

            if response.status_code == 200:
                # arXiv devuelve resultados en formato XML
                soup = BeautifulSoup(response.content, 'xml')

                # Si no encuentra el parser XML, intentar con html.parser
                if not soup.find('entry'):
                    soup = BeautifulSoup(response.content, 'html.parser')

                entries = soup.find_all('entry')

                if not entries:
                    self._log("No se encontraron resultados en arXiv o formato de respuesta inesperado.")
                    with open("arxiv_debug.xml", "w", encoding="utf-8") as f:
                        f.write(response.text)
                    return

                for entry in entries:
                    try:
                        title_tag = entry.find('title')
                        title = title_tag.text.strip() if title_tag else "No disponible"

                        # arXiv puede tener múltiples autores
                        authors = []
                        author_tags = entry.find_all('author')
                        for author_tag in author_tags:
                            name_tag = author_tag.find('name')
                            if name_tag:
                                authors.append(name_tag.text.strip())
                        authors_text = ", ".join(authors) if authors else "No disponible"

                        # Fecha de publicación
                        published_tag = entry.find('published')
                        published = published_tag.text.strip() if published_tag else "No disponible"
                        if published != "No disponible":
                            # Convertir formato ISO a año
                            published = published[:4]  # Extraer solo el año

                        # URL del artículo
                        link_tag = entry.find('id')
                        link = link_tag.text.strip() if link_tag else "No disponible"

                        self.results.append({
                            'Título': title,
                            'Autores': authors_text,
                            'Fecha': published,
                            'URL': link,
                            'Fuente': 'arXiv'
                        })
                    except Exception as e:
                        self._log(f"Error al procesar entrada de arXiv: {str(e)}")
                        continue

                self._log(f"Búsqueda en arXiv completada. Artículos encontrados: {len(self.results)}")
            else:
                self._log(f"Error al acceder a arXiv. Código: {response.status_code}")
        except Exception as e:
            self._log(f"Error general al procesar arXiv: {str(e)}")
            import traceback
            self._log(traceback.format_exc())

    def search_dblp(self, query, max_pages=2):
        """Búsqueda en DBLP (base de datos de ciencias de la computación)"""
        self._log(f"Buscando en DBLP: {query}")

        try:
            # Preparar la URL de búsqueda
            encoded_query = query.replace(' ', '+')
            base_url = f"https://dblp.org/search?q={encoded_query}"

            for page in range(max_pages):
                # DBLP usa f para paginación
                page_url = f"{base_url}&f={page * 10}"
                self._log(f"Accediendo a: {page_url}")

                response = requests.get(page_url, headers=self.headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # DBLP usa una estructura de lista para los resultados
                    articles = soup.select('li.entry')

                    if not articles:
                        self._log("No se encontraron artículos en DBLP o estructura de página diferente.")
                        break

                    for article in articles:
                        try:
                            # Obtener título
                            title_tag = article.select_one('.title')
                            title = title_tag.text.strip() if title_tag else "No disponible"

                            # Obtener autores
                            author_tags = article.select('.authors > a')
                            authors = ", ".join(
                                [author.text.strip() for author in author_tags]) if author_tags else "No disponible"

                            # Obtener año
                            year_tag = article.select_one('.year')
                            year = year_tag.text.strip() if year_tag else "No disponible"

                            # Obtener enlace
                            link_tag = article.select_one('nav.publ > ul > li > a')
                            link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No disponible"

                            self.results.append({
                                'Título': title,
                                'Autores': authors,
                                'Fuente': 'DBLP'
                            })
                        except Exception as e:
                            self._log(f"Error al procesar artículo de DBLP: {str(e)}")
                            continue

                    self._log(
                        f"Página {page + 1} de DBLP completada. Artículos encontrados en total: {len(self.results)}")
                    self._random_delay()
                else:
                    self._log(f"Error al acceder a DBLP. Código: {response.status_code}")
                    break
        except Exception as e:
            self._log(f"Error general al procesar DBLP: {str(e)}")
            import traceback
            self._log(traceback.format_exc())

    def search_all(self, query, max_pages=2):
        """Realiza búsquedas en bases de datos que han demostrado ser más estables"""
        # Limpiar resultados anteriores
        self.results = []

        # IEEE Xplore (ha funcionado según los registros de errores)
        try:
            self.search_ieee(query, max_pages)
        except Exception as e:
            self._log(f"Error completo en IEEE: {str(e)}")

        # arXiv (es estable y tiene una API)
        try:
            if len(self.results) < 10:  # Solo si IEEE no devolvió suficientes resultados
                self.search_arxiv(query, max_results=20)
        except Exception as e:
            self._log(f"Error completo en arXiv: {str(e)}")

        # DBLP (otra fuente estable para ciencias de la computación)
        try:
            if len(self.results) < 20:  # Solo si necesitamos más resultados
                self.search_dblp(query, max_pages=1)
        except Exception as e:
            self._log(f"Error completo en DBLP: {str(e)}")

        return self.results

    def save_results(self, filename="resultados_academicos.csv"):
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
    resultados = scraper.search_all(query, max_pages=200)

    # Guardar resultados
    archivo = scraper.save_results(f"{query.replace(' ', '_')}_resultados.csv")

    # Mostrar muestra de resultados
    scraper.print_sample_results()