import requests
from bs4 import BeautifulSoup

product_description = dict()
products = list()
urls = list()
soup = list()

for c in range(1, 4):
    url = 'https://www.marykay.com.br/pt-br/products/makeup/lips?page=' + str(c)
    urls.append(url)
for item in urls:
    page = requests.get(item)
    soup.append(BeautifulSoup(page.text, 'html.parser'))

for x in range(len(soup)):
    product_all = soup[x].find(class_='container main')
    product_name = product_all.find_all_next(class_='product-name')
    product_details = product_all.find_all_next(class_='name')
    product_price = product_all.find_all_next(class_='price')

    for c in range(0, len(product_name)):
        description = product_name[c].contents[0]
        product_description['Produto'] = description
        try:
            tones = product_details[c].contents[0]
            product_description['Tom'] = tones
        except IndexError:
            product_description['Tom'] = ''
        products.append(product_description.copy())

for product in product_price:
    price = product.contents[2]

for p in products:
    for k, v in p.items():
        print(f'\033[31m{k}\033[m => \033[35m{v}\033[m', end=' ')
    print()
