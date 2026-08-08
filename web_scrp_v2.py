import requests 
from bs4 import BeautifulSoup as bs
import csv
import time
import logging

logging.basicConfig(
    filename = "web_scrp_log_v2.log",
    level = logging.INFO,
    format = "%(asctime)s -%(levelname)s - %(message)s"
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

#----- The Worker Function -----#
def scrape_county(url, writer, county_name):
    try:
        print(f"Scraping... {county_name}")
        response = requests.get(url, headers=headers)
        response.raise_for_status(url, headers=headers, timeout=10)

        soup = bs(response.text, "html.parser")
        table = soup.select_one("wikitable")

        if table:
            rows = table.select("tr")
            count = 0

            for row in rows[1:]:
                cells = row.select("td")
                if len(cells) > 2:
                    date = cells[0].get_text(strip=True)
                    name = cells[1].get_text(strip=True)
                    country_name = cells[2].get_text(strip=True)

                    writer.writerow([date, name, country_name])
                    count += 1
                print(f" -> Found {count} holidays for {county_name}")
        else:
            logging.info(f"Scraped row for {county_name}")
    except Exception as e:
        logging.error(f"Failed to Scrap... {county_name}: {e}")

def main():
    targets = [("https://en.wikipedia.org/wiki/Public_holidays_in_India"),
               ("https://en.wikipedia.org/wiki/Public_holidays_in_the_United_States"),
               ("https://en.wikipedia.org/wiki/Public_holidays_in_Canada"),
               ("https://en.wikipedia.org/wiki/Public_holidays_in_Australia"),
               ("https://en.wikipedia.org/wiki/Public_holidays_in_the_United_Kingdom")]
    
    with open("web_scrp_data_v2.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Holiday Name", "County"])

        for county, url in targets:
            scrape_county(url, writer, county)
            time.sleep(3)

if __name__ == "__main__":
    main()