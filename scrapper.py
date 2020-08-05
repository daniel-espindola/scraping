import requests
from bs4 import BeautifulSoup as bs
from time import sleep

site = 'https://www.amazon.com.br'
product = 'iphone'
url = site+'/s?k='+product
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0",
    "X-Amzn-Trace-Id": "Root=1-5f2a62b3-f7813d376f210b633c895e34"
}


def getProduct(html):
    """
    Receives a string containing a html document of an Amazon.com.br search result
    Returns a list of tuples containing the name and price of all the products in the page
    """
    soup = bs(html, 'html.parser')
    products = []

    items = soup.find_all('div', class_='s-result-item')
    for item in items[:-2]:
        item_price = ""
        item_name = ""
        try:
            item_title = item.find('h2')
            item_name = item_title.a.span.text
            print(item_name)
        except:
            print("Nome não encontrado")

        try:
            item_price = item.find(class_="a-price").span.text
        except:
            print("Preço não encontrado")
            item_price = "Preço indisponível"

        products.append((item_name, item_price))

    return products


def productsToCSV(products):
    """
    Receives a list of tuples containing names and prices
    Writes a csv file using semicolon as delimiter
    Saves the file in the program directory
    """
    file = open('products.csv', 'w')
    file.write('Nome do produto;Preço\n')

    for product in products:
        file.write(str(product[0]) + ";" + str(product[1])+'\n')

    file.close()


print('Requisitando dados de: '+url)
req = requests.get(url, headers=headers)

while (req.status_code != 200):
    print("Falha na requisição, nova tentativa em 2s " +
          " | status code = "+str(req.status_code))
    sleep(2)
    req = requests.get(url, headers=headers)

print('Requisição bem sucedida!')
print('Extraindo informações...')
products = getProduct(req.content)

productsToCSV(products)
