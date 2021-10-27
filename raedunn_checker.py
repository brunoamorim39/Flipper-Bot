from bs4 import BeautifulSoup
import requests
import time
import numpy
import random

user_agent_desktop = 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp, image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip',
'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

class RAEDUNN:
    def __init__(self, title, price, link, source):
        self.title = title
        self.price = price
        self.link = link
        self.source = source

def getSoup(url, header):
    reqCount = 0
    while True:
        if reqCount > 4:
            return
        try:
            resp = requests.get(url, timeout=10, headers=header)
            soup = BeautifulSoup(resp.content, "html.parser")
            return soup
        except:
            reqCount += 1
            print('Trying again...')
            # traceback.print_exc()
            # headerCookie = getCookie()
            pass

def trim_price(price):
    int_price = price.replace('\n', '')
    trimmed_price = int_price.replace('\t', '')
    if trimmed_price.count('$') > 1:
        trimmed_price = trimmed_price[trimmed_price.find('$', 1)::]
    return trimmed_price

def remove_dollar_sign(price):
    num_price = float(price.replace('$', ''))
    return num_price

def homegoods_checker():
    urls_to_check = [
        'https://www.homegoods.com/us/store/shop/new-arrivals/_/N-842114098?Nr=AND%28product.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&tn=0#/us/store/products/new-arrivals/_/N-842114098?Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Ns=brand%7C1&tag=srt',
        'https://www.homegoods.com/us/store/shop/new-arrivals/_/N-842114098?Nr=AND%28product.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&tn=0#/us/store/products/new-arrivals/_/N-842114098?No=180&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/new-arrivals/_/N-842114098?Nr=AND%28product.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&tn=0#/us/store/products/new-arrivals/_/N-842114098?No=360&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',

        'https://www.homegoods.com/us/store/shop/gifts/_/N-3340154571?tn=1#/us/store/products/gifts/_/N-3340154571?Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Ns=brand%7C1&tag=srt',
        'https://www.homegoods.com/us/store/shop/gifts/_/N-3340154571?tn=1#/us/store/products/gifts/_/N-3340154571?No=180&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/gifts/_/N-3340154571?tn=1#/us/store/products/gifts/_/N-3340154571?No=360&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/gifts/_/N-3340154571?tn=1#/us/store/products/gifts/_/N-3340154571?No=540&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1'

        'https://www.homegoods.com/us/store/shop/seasonal/_/N-1145120965?tn=2#/us/store/products/seasonal/_/N-1145120965?Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Ns=brand%7C1&tag=srt',
        'https://www.homegoods.com/us/store/shop/seasonal/_/N-1145120965?tn=2#/us/store/products/seasonal/_/N-1145120965?No=180&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1'

        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Ns=brand%7C1&tag=srt',
        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?No=180&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?No=360&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?No=540&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?No=720&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?No=900&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?No=1080&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?No=1260&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/decor-pillows/_/N-3997050369?tn=3#/us/store/products/decor-pillows/_/N-3997050369?No=1440&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1'

        'https://www.homegoods.com/us/store/shop/bed-bath/_/N-3449061438?tn=4#/us/store/products/bed-bath/_/N-3449061438?Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Ns=brand%7C1&tag=srt',
        'https://www.homegoods.com/us/store/shop/bed-bath/_/N-3449061438?tn=4#/us/store/products/bed-bath/_/N-3449061438?No=180&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/bed-bath/_/N-3449061438?tn=4#/us/store/products/bed-bath/_/N-3449061438?No=360&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/bed-bath/_/N-3449061438?tn=4#/us/store/products/bed-bath/_/N-3449061438?No=540&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/bed-bath/_/N-3449061438?tn=4#/us/store/products/bed-bath/_/N-3449061438?No=720&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1'

        'https://www.homegoods.com/us/store/shop/kitchen/_/N-3838325203?tn=5#/us/store/products/kitchen/_/N-3838325203?Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Ns=brand%7C1&tag=srt',
        'https://www.homegoods.com/us/store/shop/kitchen/_/N-3838325203?tn=5#/us/store/products/kitchen/_/N-3838325203?No=180&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/kitchen/_/N-3838325203?tn=5#/us/store/products/kitchen/_/N-3838325203?No=360&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://www.homegoods.com/us/store/shop/kitchen/_/N-3838325203?tn=5#/us/store/products/kitchen/_/N-3838325203?No=540&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',

        'https://www.homegoods.com/us/store/shop/pet/_/N-3231320984?tn=6#/us/store/products/pet/_/N-3231320984?Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Ns=brand%7C1&tag=srt',
        'https://www.homegoods.com/us/store/shop/pet/_/N-3231320984?tn=6#/us/store/products/pet/_/N-3231320984?No=180&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1',

        'https://www.homegoods.com/us/store/shop/clearance/_/N-3951437597?Nr=AND%28product.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&tn=8#/us/store/products/clearance/_/N-3951437597?Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Ns=brand%7C1&tag=srt',
        'https://www.homegoods.com/us/store/shop/clearance/_/N-3951437597?Nr=AND%28product.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&tn=8#/us/store/products/clearance/_/N-3951437597?No=180&Nr=AND%28isEarlyAccess%3Afalse%2Cproduct.siteId%3Ahomegoods%2COR%28product.catalogId%3Atjmaxx%29%29&Nrpp=180&Ns=brand%7C1&&next=1'
        ]
    
    items_of_interest = []
    
    for url in urls_to_check:
        url_soup = getSoup(url, headers)
        products = url_soup.find_all('div', class_='product-details')
        for product in products:
            product_brand = product.find('span', class_='product-brand')
            if product_brand.text == 'RAE DUNN':
                product_title = product.find('span', class_='product-title').text

                product_price = product.find('span', class_='product-price')
                product_price = trim_price(product_price.text)

                product_link = product.find('a', class_='product-link', href=True)['href']
                product_link = f'https://www.homegoods.com{product_link}'

                product_data = RAEDUNN(product_title, product_price, product_link, 'HOMEGOODS')

                if len(items_of_interest) == 0:
                    print('CHECKING HOMEGOODS')
                    
                print(f'{product_data.source} | {product_data.title} | {product_data.price}')
                print(product_data.link)
                print('---------------------------------------------------------------')
                items_of_interest.append(product_data)
            else:
                continue

        time.sleep(random.uniform(30, 60))

    return items_of_interest

def tjmaxx_checker():
    urls_to_check = [
        'https://tjmaxx.tjx.com/store/shop/new-arrivals/_/N-842114098?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&ln=1:1#/store/products/new-arrivals/_/N-842114098?Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Ns=brand%7C1&tag=srt',
        'https://tjmaxx.tjx.com/store/shop/new-arrivals/_/N-842114098?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&ln=1:1#/store/products/new-arrivals/_/N-842114098?No=176&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/new-arrivals/_/N-842114098?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&ln=1:1#/store/products/new-arrivals/_/N-842114098?No=356&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/new-arrivals/_/N-842114098?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&ln=1:1#/store/products/new-arrivals/_/N-842114098?No=536&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/new-arrivals/_/N-842114098?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&ln=1:1#/store/products/new-arrivals/_/N-842114098?No=716&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/new-arrivals/_/N-842114098?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&ln=1:1#/store/products/new-arrivals/_/N-842114098?No=896&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/new-arrivals/_/N-842114098?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&ln=1:1#/store/products/new-arrivals/_/N-842114098?No=1076&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',

        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Ns=brand%7C1&tag=srt',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=179&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=359&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=539&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=719&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=899&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=1079&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=1259&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=1439&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=1619&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/gifts/_/N-3094159741+0?ln=1:1#/store/products/gifts/_/N-3094159741+0?No=1799&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',

        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Ns=brand%7C1&tag=srt',
        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?No=179&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?No=359&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?No=539&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?No=719&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?No=899&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?No=1079&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?No=1259&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/home/_/N-2179804981?tn=6#/store/products/home/_/N-2179804981?No=1439&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',

        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Ns=brand%7C1&tag=srt',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=176&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=356&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=536&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=716&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=896&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=1076&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=1256&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=1436&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=1616&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=1796&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=1976&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1',
        'https://tjmaxx.tjx.com/store/shop/clearance/_/N-3951437597?Nr=AND%28OR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&tn=8#/store/products/clearance/_/N-3951437597?No=2156&Nr=AND%28isEarlyAccess%3Afalse%2COR%28product.catalogId%3Atjmaxx%29%2Cproduct.siteId%3Atjmaxx%29&Nrpp=180&Ns=brand%7C1&&next=1'
        ]
    
    items_of_interest = []
    
    for url in urls_to_check:
        url_soup = getSoup(url, headers)
        products = url_soup.find_all('div', class_='product-details')
        for product in products:
            product_brand = product.find('span', class_='product-brand')
            if product_brand.text == 'RAE DUNN':
                product_title = product.find('span', class_='product-title').text

                product_price = product.find('span', class_='product-price')
                product_price = trim_price(product_price.text)

                product_link = product.find('a', class_='product-link', href=True)['href']
                product_link = f'https:///tjmaxx.tjx.com{product_link}'

                product_data = RAEDUNN(product_title, product_price, product_link, 'TJMAXX')

                if len(items_of_interest) == 0:
                    print('CHECKING TJMAXX')
                    
                print(f'{product_data.source} | {product_data.title} | {product_data.price}')
                print(product_data.link)
                print('---------------------------------------------------------------')
                items_of_interest.append(product_data)
            else:
                continue

        time.sleep(random.uniform(30, 60))

    return items_of_interest

def get_price_comps(rae_dunn_items):
    items_to_analyze = []
    for i in range(1, 50):
        ebay_url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw=rae+dunn&_sacat=0&LH_TitleDesc=0&_fsrp=1&_ipg=200&LH_Sold=1&_oac=1&_pgn={str(i)}'
        ebay_soup = getSoup(ebay_url, headers)

        listings = ebay_soup.find_all('div', class_='s-item__info')[1::]
        for listing in listings:
            listing_title = listing.find('h3', class_='s-item__title').text
            listing_price = listing.find('span', class_='s-item__price').text

            for item in rae_dunn_items:
                if item.title.lower() in listing_title.lower().replace('"', ''):
                    print(f'{item.title} | {item.price}')
                    print(f'{listing_title} | {listing_price}')
                    print(f'{item.link}')
                    print('---------------------------------------------------------------')
                    items_to_analyze.append((item.title, item.price, listing_price, item.link))

        time.sleep(random.uniform(30, 60))
    
    return items_to_analyze

def item_analysis(price_comps):
    sendable_items = []

    sales_tax = 0.07
    listing_fee = 0.35
    sales_price_adjust = 0.90 # Adjust our sales price to 90% of what the recently sold price is to adjust for demand fluctuations
    final_value_mult = 0.1255
    final_value_fee = 0.30

    target_profit_margin = 0.35

    for comp in price_comps:
        item = comp[0]
        link = comp[3]
        buy_price = remove_dollar_sign(comp[1])
        previously_sold_price = remove_dollar_sign(comp[2])

        sales_price_target = round(previously_sold_price * sales_price_adjust, 2)

        cost_to_list = round(buy_price * (1 + sales_tax) + listing_fee, 2)
        cost_to_sell =  round(final_value_mult * sales_price_target + final_value_fee, 2)
        realizable_profit = round(sales_price_target - cost_to_list - cost_to_sell, 2)

        profit_margin =  realizable_profit / sales_price_target

        if profit_margin >= target_profit_margin:
            print(f'Purchase: ${round(buy_price, 2)} | Reasonable Sell: ${round(sales_price_target, 2)} | Potential Profit: ${round(realizable_profit, 2)} (%{round(profit_margin * 100, 2)})')
            print(f'Item {item} appears to have adequate margins')
            print(f'{link}')
            print('---------------------------------------------------------------')
        elif profit_margin >= target_profit_margin - 0.15:
            print(f'Purchase: ${round(buy_price, 2)} | Reasonable Sell: ${round(sales_price_target, 2)} | Potential Profit: ${round(realizable_profit, 2)} (%{round(profit_margin * 100, 2)})')
            print(f'Item {item} profit margins require risk analysis')
            print(f'{link}')
            print('---------------------------------------------------------------')
        else:
            print(f'Purchase: ${round(buy_price, 2)} | Reasonable Sell: ${round(sales_price_target, 2)} | Potential Profit: ${round(realizable_profit, 2)} (%{round(profit_margin * 100, 2)})')
            print(f'Item {item} has inadequate margins to make reasonable profit')
            print(f'{link}')
            print('---------------------------------------------------------------')

    return sendable_items

if __name__ == '__main__':
    # Testing purposes
    # rae_dunn_items = []
    # rae_dunn_items.append(homegoods_checker())
    # rae_dunn_items.append(tjmaxx_checker())
    # price_comps = get_price_comps(rae_dunn_items)
    # item_analysis(price_comps)

    test_case = [
        ('Cookie Jar', '$10', '$25', 'blahblahblah'),
        ('Table Runner', '$8', '$16', 'kitchenkitchenkitchen'),
        ('Dog Bowl', '$12', '$15', 'blahpetblah')
        ]
    item_analysis(test_case)

    # while True:
    #     t = time.localtime()
    #     current_time = time.strftime('%H:%M:%S', t)
    #     if current_time == '04:12:49':
    #         rae_dunn_items = []
    #         rae_dunn_items.append(homegoods_checker())
    #         rae_dunn_items.append(tjmaxx_checker())
    #         price_comps = get_price_comps()