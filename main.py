import requests
from bs4 import BeautifulSoup

product_description = dict()
products = list()
urls = list()
soup = list()
# série de loops para armazenar as urls na lista
for c in range(1, 4):
    url = 'https://www.marykay.com.br/pt-br/products/new-products?page=' + str(c)
    urls.append(url)
for c in range(1, 5):
    url = 'https://www.marykay.com.br/pt-br/products/skincare?page=' + str(c)
    urls.append(url)
for c in range(1, 14):
    url = 'https://www.marykay.com.br/pt-br/products/makeup?page=' + str(c)
    urls.append(url)
for c in range(1, 3):
    url = 'https://www.marykay.com.br/pt-br/products/fragrance?page=' + str(c)
    urls.append(url)
url = 'https://www.marykay.com.br/pt-br/products/body-and-sun'
urls.append(url)

# laço para fazer o request das páginas
for item in urls:
    page = requests.get(item)
    soup.append(BeautifulSoup(page.text, 'html.parser'))

# laço principal para extrair os dados específicos
for x in range(len(soup)):
    product_all = soup[x].find(class_='container main')
    product_name = product_all.find_all_next(class_='product-name')
    product_details = product_all.find_all_next(class_='name')
    product_price = product_all.find_all_next(class_='price')
    product_sup = product_all.find_all_next('sup')

    for c in range(0, len(product_name)):
        description = product_name[c].contents[0]
        product_description['Produto'] = description
        try:
            tones = product_details[c].contents[0]
            product_description['Tom'] = tones
        except IndexError:
            product_description['Tom'] = ''
        price = product_price[c].contents[2]

        sup = product_sup[c].contents[0]
        product_description['Preço'] = str(price) + ',' + str(sup)

        products.append(product_description.copy())

for p in products:
    for k, v in p.items():
        print(f'\033[31m{k}\033[m => \033[35m{v}\033[m', end=' ')
    print()
