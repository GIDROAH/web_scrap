import requests
from bs4 import BeautifulSoup as bs
import time 
import logging
import csv 

logging.basicConfig(
    filename = 'web_scrp_log_v1.log',
    level = logging.INFO,
    format = '%(asctime)s - %(levelname)s - %(message)s'
)

def get_safe_text(item, selector, attribute=None):
    found = item.select_one(selector)
    if found:
        if attribute:
            return found.get(attribute, 'N/A').strip()
        return found.get_text(strip = True)
    logging.warning(f'Selector "{selector}" not found.')    
    return 'N/A'



url = "https://en.wikipedia.org/wiki/Public_holidays_in_India"
headers ={
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f'Error fetching the URL: {e}')
    exit()

time.sleep(2)  # Be polite and avoid overwhelming the server
soup = bs(response.content, 'html.parser')

file = open('web_scrp_data_v1.csv', 'w' , encoding='utf-8')
writer = csv.writer(file)
writer.writerow(['Date', 'Name'])

table = soup.select_one('table.wikitable')

if table:
    rows = table.select('tr')

    for row in rows[1:]:
        cells = row.select('td')
        if len(cells) >= 2:
            date = cells[0].get_text(strip=True)
            name = cells[1].get_text(strip=True)

            print(f'Saving: {date}-{name}')
            writer.writerow([date, name])
else:
    logging.error("Table not found!")
file.close()

print("Process completed successfully.")