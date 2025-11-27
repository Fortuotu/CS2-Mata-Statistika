import requests
import time
import string
from bs4 import BeautifulSoup

http_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i'
}

def parse_skin_name(name: str):
    def remove_unsupported(s: str):
        out = []

        allowed = string.ascii_letters + string.digits

        parts = s.split(' ')
        for part in parts:
            part = part.replace("'", '')
            part = part.replace("-", ' ')

            fixed = ''.join([c if c in allowed or c == ' ' else '' for c in part]).strip()
            if not fixed:
                continue

            out.append(fixed + ' ')
        
        return ''.join(out).strip()

    weapon, skin_name = name.split('|')

    weapon = remove_unsupported(weapon.strip().lower()).replace(' ', '-')
    skin_name = remove_unsupported(skin_name.strip().lower()).replace(' ', '-')

    return f'{weapon}-{skin_name}'

def get_html(skin_name):
    response = requests.get(f'https://csgoskins.gg/items/{parse_skin_name(skin_name)}', headers=http_headers)

    return response.text

def find_prices(html):
    out = {}

    try:
        soup = BeautifulSoup(html, features='lxml')

        soup = soup.find('div', class_='order-1')
        soup = soup.find_next()
        soup = soup.find_next()
        soup = soup.find_next_siblings()
        
        for sibling in soup:
            spans = sibling.find_all('span')
            if not spans:
                continue
            
            wear = ''.join([i.get_text(strip=True) + ' ' for i in spans[:-1]]).strip()
            price = spans[-1].get_text(strip=True)

            out[wear] = price
                
        return out
    except:
        return None

def find_rarity(html):
    try:
        soup = BeautifulSoup(html, features='lxml')
        soup = soup.find('div', class_='order-14')
        soup = soup.find_next('a')

        return soup.get_text(strip=True)
    except:
        return None

def scrape_data_with_html(html):
    rarity = find_rarity(html)
    prices = find_prices(html)
    
    if rarity is None or prices is None:
        return {'error': 'Bad document'}

    return {
        'rarity': rarity,
        'prices': prices
    }

def try_get_skin_data(skin_name, attempts: int = 3):
    rate_limit = 2

    for _ in range(attempts):
        time.sleep(rate_limit)
        data = scrape_data_with_html(get_html(skin_name))

        if 'error' in data:
            print(data)
            rate_limit += 1

            continue

        return data
    
    return None
