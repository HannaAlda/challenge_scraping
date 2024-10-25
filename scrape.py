from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup

def scrape(url):
    # Configura las opciones de Edge
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')

    # Inicia el WebDriver
    driver = webdriver.Edge(options=options)
    driver.get(url)
    page_content = driver.page_source
    driver.quit()

    # Analiza el HTML con BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')
    products = []
    for i, elem in enumerate(soup.select('.vtex-store-components-3-x-productBrand'), start=1):
        if i > 15:
            break
        name = elem.get_text(strip=True)
        price_elem = elem.find_next('div', class_='tiendasjumboqaio-jumbo-minicart-2-x-price')
        promo_price_elem = elem.find_next('div', class_='tiendasjumboqaio-jumbo-minicart-2-x-price')
        price = price_elem.get_text(strip=True) if price_elem else 'N/A'
        promo_price = promo_price_elem.get_text(strip=True) if promo_price_elem else 'N/A'

        products.append({'name': name, 'price': price, 'promo_price': promo_price})
    
    return {"products": products, "url": url}
