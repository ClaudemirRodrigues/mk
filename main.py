import requests
from bs4 import BeautifulSoup

product_description = dict()
products = list()

page_makeup_lips = requests.get('https://www.marykay.com.br/pt-br/products/makeup/lips')
soup = BeautifulSoup(page_makeup_lips.text, 'html.parser')

product_all = soup.find(class_='container main')
product_name = product_all.find_all_next(class_='product-name')
product_details = product_all.find_all_next(class_='name')
product_price = product_all.find_all_next(class_='price')

for c in range(0, len(product_name)):
    description = product_name[c].contents[0]
    tones = product_details[c].contents[0]
    product_description['Produto'] = description
    product_description['Tom'] = tones
    products.append(product_description.copy())
    #print(product.prettify())

for product in product_price:
    price = product.contents[2]

for p in products:
    for k, v in p.items():
        print(f'\033[31m{k}\033[m => \033[35m{v}\033[m', end=' ')
    print()
