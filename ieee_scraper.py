from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pandas as pd
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
import requests

SEARCH_TERM = "computational thinking"
IEEE_URL = f"https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={SEARCH_TERM}"
PDF_DIR = "articulos/ieee"

options = Options()
# Desactivamos headless para usar sesión autenticada manual
# options.add_argument("--headless")
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
os.makedirs(PDF_DIR, exist_ok=True)

print("Iniciando búsqueda en IEEE Xplore...")
driver.get(IEEE_URL)
time.sleep(10)

datos = []

pagina = 1
while True:
    print(f"Procesando página {pagina}...")
    time.sleep(5)
    articles = driver.find_elements(By.CLASS_NAME, "List-results-items")
    print(f" - Artículos encontrados: {len(articles)}")

    for idx, art in enumerate(articles):
        try:
            title_elem = art.find_element(By.CLASS_NAME, "text-md-md-lh")
            link_elem = title_elem.find_element(By.TAG_NAME, "a")
            title = link_elem.text.strip()
            partial_link = link_elem.get_attribute("href")
            if not partial_link:
                raise ValueError("Artículo sin enlace")
            link = "https://ieeexplore.ieee.org" + partial_link if partial_link.startswith("/") else partial_link

            try:
                authors = art.find_element(By.CLASS_NAME, "author").text.strip()
            except:
                authors = "N/A"

            try:
                pub_info = art.find_element(By.CLASS_NAME, "publisher-info-container").text
                year_line = [x for x in pub_info.split("\n") if "Year:" in x]
                year = year_line[0].replace("Year:", "").strip() if year_line else "N/A"
            except:
                year = "N/A"

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])
            driver.get(link)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(3)

            try:
                doi = driver.find_element(By.CLASS_NAME, "stats-document-abstract-doi").text.replace("DOI: ", "")
            except:
                doi = "N/A"

            try:
                abstract = driver.find_element(By.CLASS_NAME, "abstract-text").text.strip()
            except:
                abstract = "N/A"

            try:
                pdf_elem = driver.find_element(By.CSS_SELECTOR, "a.stats_PDF_")
                pdf_href = pdf_elem.get_attribute("href")
                if pdf_href:
                    pdf_url = "https://ieeexplore.ieee.org" + pdf_href if pdf_href.startswith("/") else pdf_href
                    pdf_response = requests.get(pdf_url, headers={"User-Agent": "Mozilla/5.0"})
                    pdf_path = os.path.join(PDF_DIR, f"ieee_p{pagina}_{idx + 1}.pdf")
                    with open(pdf_path, "wb") as f:
                        f.write(pdf_response.content)
                else:
                    pdf_url = "N/A"
            except:
                pdf_url = "N/A"

            datos.append({
                "title": title,
                "authors": authors,
                "year": year,
                "doi": doi,
                "abstract": abstract,
                "url": link,
                "pdf": pdf_url
            })

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except Exception as e:
            print(f"Error en artículo {idx + 1} (página {pagina}): {e}")
            continue

    # Ir a la siguiente página
    try:
        next_btn = driver.find_element(By.XPATH, "//button[contains(text(),'>')]" )
        if next_btn.is_enabled():
            next_btn.click()
            pagina += 1
            time.sleep(5)
        else:
            break
    except NoSuchElementException:
        print("No hay más páginas.")
        break

# Cerrar navegador
driver.quit()

# Guardar CSV
df = pd.DataFrame(datos)
df.to_csv("ieee_articles.csv", index=False)

# Guardar BibTeX
bib_db = BibDatabase()
bib_db.entries = []
for i, row in df.iterrows():
    bib_db.entries.append({
        'ENTRYTYPE': 'article',
        'ID': f"ieee_{i + 1}",
        'title': row['title'],
        'author': row['authors'],
        'year': row['year'],
        'doi': row['doi'],
        'url': row['url'],
        'abstract': row['abstract']
    })

with open("ieee_articles.bib", "w", encoding="utf-8") as bibfile:
    writer = BibTexWriter()
    bibfile.write(writer.write(bib_db))

print("\n✅ Proceso completado: ieee_articles.csv y ieee_articles.bib generados.")