from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

app = Flask(__name__)

def scrape(url):
    # Configura las opciones de Edge
    options = Options()
    options.use_chromium = True
    options.add_argument("--headless")  # Ejecuta en modo headless
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')

    # Configura el servicio para el controlador de Edge
    service = Service()  # Puedes especificar la ruta del ejecutable si es necesario

    # Inicia el WebDriver
    driver = webdriver.Edge(service=service, options=options)
    
    # Carga la URL proporcionada
    driver.get(url)
    
    # Obtiene el contenido HTML de la página
    page_content = driver.page_source
    
    # Cierra el navegador
    driver.quit()
    
    # Analiza el HTML con BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    
    # Extrae los productos de la página
    products = []
    for elem in soup.select('.vtex-store-components-3-x-productBrand'):
        name = elem.get_text(strip=True)
        price_elem = elem.find_next('div', class_='tiendasjumboqaio-jumbo-minicart-2-x-price')
        promo_price_elem = elem.find_next('div', class_='tiendasjumboqaio-jumbo-minicart-2-x-price')

        price = price_elem.get_text(strip=True) if price_elem else 'N/A'
        promo_price = promo_price_elem.get_text(strip=True) if promo_price_elem else 'N/A'

        products.append({
            'name': name,
            'price': price,
            'promo_price': promo_price
        })
    
    # Retorna los productos encontrados
    return {"products": products, "url": url}

@app.route('/scrape', methods=['POST'])
def scrape_endpoint():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    result = scrape(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
