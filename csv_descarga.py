import requests
import csv

def download_json_and_convert_to_csv(json_url, output_csv):
    response = requests.get(json_url)
    data = response.json()

    # Extrae los datos de custom_attributes
    products = data.get('custom_attributes', [])
    if not isinstance(products, list):
        print("El formato de un producto no es el esperado.")
        return
    
    # Escribe los datos en un archivo CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['allergens', 'sku', 'vegan', 'kosher', 'organic', 'vegetarian', 
                         'gluten_free', 'lactose_free', 'package_quantity', 'unit_size', 'net_weight'])

        for product in products:
            writer.writerow([
                product.get('allergens', 'N/A'),
                product.get('sku', 'N/A'),
                product.get('vegan', 'N/A'),
                product.get('kosher', 'N/A'),
                product.get('organic', 'N/A'),
                product.get('vegetarian', 'N/A'),
                product.get('gluten_free', 'N/A'),
                product.get('lactose_free', 'N/A'),
                product.get('package_quantity', 'N/A'),
                product.get('unit_size', 'N/A'),
                product.get('net_weight', 'N/A')
            ])

    print(f"Archivo CSV generado correctamente: {output_csv}")

# Ejemplo de uso
download_json_and_convert_to_csv(
    'https://storage.googleapis.com/resources-prod-shelftia/scrapers-prueba/product.json',
    'output-product.csv'
)
