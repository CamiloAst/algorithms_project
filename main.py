import pandas as pd
import requests
import matplotlib.pyplot as plt

# Configuración de las APIs
SCIENCEDIRECT_API_KEY = '612aaafc590a9e81ffa39c1583078cb6'
IEEE_API_KEY = '4cspzswadt62jh7f6dbkcq3z'
BASE_URL_SCIENCEDIRECT = 'https://api.elsevier.com/content/search/scopus'
BASE_URL_IEEE = 'https://ieeexploreapi.ieee.org/api/v1/search/articles'
BASE_URL_CROSSREF = 'https://api.crossref.org/works'


# Función para buscar artículos en ScienceDirect
def search_sciencedirect(query, count=10):
    headers = {'X-ELS-APIKey': SCIENCEDIRECT_API_KEY, 'Accept': 'application/json'}
    params = {'query': query, 'count': count}
    response = requests.get(BASE_URL_SCIENCEDIRECT, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code} en ScienceDirect: {response.text}")
        return None


# Función para buscar artículos en IEEE Xplore
def search_ieee(query, count=10):
    if IEEE_API_KEY == 'TU_API_KEY_IEEE':
        print("Error: La API Key de IEEE Xplore está inactiva o no es válida.")
        return None

    params = {'apikey': IEEE_API_KEY, 'querytext': query, 'max_records': count, 'format': 'json'}
    response = requests.get(BASE_URL_IEEE, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code} en IEEE Xplore: {response.text}")
        return None


# Función para buscar artículos en CrossRef (incluye artículos de SAGE)
def search_crossref(query, count=10):
    params = {'query': query, 'rows': count}
    response = requests.get(BASE_URL_CROSSREF, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code} en CrossRef: {response.text}")
        return None


# Función para extraer datos relevantes de ScienceDirect
def extract_articles_sciencedirect(data):
    articles = []
    if 'search-results' in data and 'entry' in data['search-results']:
        for entry in data['search-results']['entry']:
            articles.append({
                'Title': entry.get('dc:title', 'N/A'),
                'Authors': entry.get('dc:creator', 'N/A'),
                'Year': entry.get('prism:coverDate', 'N/A')[:4],
                'DOI': entry.get('prism:doi', 'N/A'),
                'Journal': entry.get('prism:publicationName', 'N/A'),
                'Abstract': entry.get('dc:description', 'N/A'),
                'Source': 'ScienceDirect'
            })
    return pd.DataFrame(articles)


# Función para extraer datos relevantes de CrossRef
def extract_articles_crossref(data):
    articles = []
    if 'message' in data and 'items' in data['message']:
        for entry in data['message']['items']:
            authors = entry.get('author', [])
            author_names = ', '.join([
                (author.get('given', '') + ' ' + author.get('family', '')).strip()
                for author in authors if 'family' in author
            ])

            articles.append({
                'Title': entry.get('title', ['N/A'])[0],
                'Authors': author_names if author_names else 'N/A',
                'Year': entry.get('published-print', {}).get('date-parts', [['N/A']])[0][0],
                'DOI': entry.get('DOI', 'N/A'),
                'Journal': entry.get('container-title', ['N/A'])[0],
                'Abstract': entry.get('abstract', 'N/A'),
                'Source': 'CrossRef'
            })
    return pd.DataFrame(articles)


# Consulta de ejemplo
query = "computational thinking"

science_direct_data = search_sciencedirect(query, count=20)
ieee_data = search_ieee(query, count=20)
crossref_data = search_crossref(query, count=20)

df_science = extract_articles_sciencedirect(science_direct_data) if science_direct_data else pd.DataFrame()
df_crossref = extract_articles_crossref(crossref_data) if crossref_data else pd.DataFrame()

df_all = pd.concat([df_science, df_crossref], ignore_index=True)
df_clean, df_duplicates = df_all.drop_duplicates(subset=['Title', 'DOI'], keep='first'), df_all[
    df_all.duplicated(subset=['Title', 'DOI'], keep=False)]

df_clean.to_csv('articles.csv', index=False)
df_duplicates.to_csv('duplicates.csv', index=False)

print("Datos extraídos y guardados en articles.csv y duplicates.csv")
