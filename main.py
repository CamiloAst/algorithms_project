import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Configuración de Selenium para Edge
options = webdriver.EdgeOptions()
options.add_argument('--headless')  # Ejecutar en segundo plano
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_experimental_option("prefs", {"download.default_directory": os.path.abspath("downloads")})

# Inicializar WebDriver para Edge
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)


# Función para realizar scraping en ScienceDirect
def scrape_sciencedirect(query, max_articles=10000):
    url = f"https://www.sciencedirect.com/search?qs={query.replace(' ', '%20')}"
    driver.get(url)
    time.sleep(5)  # Aumentar tiempo de espera para carga completa

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = []

    for article in soup.select('.result-item-content')[:max_articles]:
        title_elem = article.find('h2')
        link_elem = article.find('a')

        title = title_elem.get_text(strip=True) if title_elem else 'N/A'
        link = 'https://www.sciencedirect.com' + link_elem['href'] if link_elem else 'N/A'

        if title != 'N/A' and link != 'N/A':
            articles.append({'Title': title, 'Link': link, 'Source': 'ScienceDirect'})

    return pd.DataFrame(articles)


# Función para realizar scraping en IEEE Xplore
def scrape_ieee(query, max_articles=10000):
    url = f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={query.replace(' ', '%20')}"
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    articles = []

    for article in soup.select('.List-results-items')[:max_articles]:
        title_elem = article.find('h3')
        link_elem = article.find('a')

        title = title_elem.get_text(strip=True) if title_elem else 'N/A'
        link = 'https://ieeexplore.ieee.org' + link_elem['href'] if link_elem else 'N/A'

        if title != 'N/A' and link != 'N/A':
            articles.append({'Title': title, 'Link': link, 'Source': 'IEEE Xplore'})

    return pd.DataFrame(articles)


# Función para descargar PDFs con Selenium
def download_pdfs(df, download_path='downloads'):
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    for index, row in df.iterrows():
        pdf_page_url = row['Link']
        driver.get(pdf_page_url)
        time.sleep(5)

        try:
            # Esperar que el botón de descarga aparezca
            download_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Download PDF')]"))
            )

            pdf_url = download_button.get_attribute("href")
            if pdf_url and 'pdf' in pdf_url:
                response = requests.get(pdf_url, timeout=10)
                if response.status_code == 200:
                    file_path = os.path.join(download_path, f"{index}.pdf")
                    with open(file_path, 'wb') as file:
                        file.write(response.content)
                    print(f"Descargado: {file_path}")
                else:
                    print(f"No se pudo descargar el PDF desde: {pdf_url}")
            else:
                print(f"No se encontró enlace directo al PDF en: {pdf_page_url}")
        except Exception as e:
            print(f"Error al descargar PDF de {pdf_page_url}: {str(e)}")


# Ejecutar scraping
query = "computational thinking"
df_science = scrape_sciencedirect(query, max_articles=10000)
df_ieee = scrape_ieee(query, max_articles=10000)

df_all = pd.concat([df_science, df_ieee], ignore_index=True)

df_unique = df_all.drop_duplicates(subset=['Title', 'Link'], keep='first')
df_duplicates = df_all[df_all.duplicated(subset=['Title', 'Link'], keep=False)]

# Descargar PDFs
download_pdfs(df_unique)

# Guardar en CSV
df_unique.to_csv('articles.csv', index=False)
df_duplicates.to_csv('duplicates.csv', index=False)

# Cerrar WebDriver
driver.quit()

print("Datos extraídos y guardados en articles.csv y duplicates.csv")
