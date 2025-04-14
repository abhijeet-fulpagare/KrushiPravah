import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver
import time
import os
import json
from datetime import datetime, timedelta
import logging
import re

from convert import unit_marathi_to_english, item_marathi_to_english

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

BASE_URL = "http://www.puneapmc.org/"
LOOKUP_COUNT = 100

# Get the parent directory path
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PARENT_DIR, 'Data')

# Ensure Data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

FILE_NAME = os.path.join(DATA_DIR, "original.csv")
JSON_FILE = os.path.join(DATA_DIR, "data.json")

# Marathi to English number mapping
marathi_to_english_numbers = {
    '०': '0', '१': '1', '२': '2', '३': '3', '४': '4',
    '५': '5', '६': '6', '७': '7', '८': '8', '९': '9'
}

def convert_marathi_numbers(text):
    """Convert Marathi numbers to English numbers"""
    return ''.join(marathi_to_english_numbers.get(c, c) for c in text)

def setup_driver():
    """Setup and return a Chrome WebDriver instance"""
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)

def get_links(BASE_URL):
    """Get all rate links from the main page"""
    logging.info("Fetching links from main page")
    driver = setup_driver()
    
    try:
        driver.get(BASE_URL + "rates.aspx")
        time.sleep(3)  # Give JS time to load data
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        anchors = soup.find_all('a')
        
        links = []
        for anchor in anchors:
            if anchor.get_text() == "View Rates":
                links.append(BASE_URL + anchor["href"])
        
        logging.info(f"Found {len(links)} rate links")
        return links
    except Exception as e:
        logging.error(f"Error getting links: {str(e)}")
        return []
    finally:
        driver.quit()

def get_date_for_page(page_number):
    """Get date for the current page (decreasing by one day for each page)"""
    current_date = datetime.now()
    days_to_subtract = page_number - 1  # First page (0) is today, second page (1) is yesterday, etc.
    target_date = current_date - timedelta(days=days_to_subtract)
    return target_date.strftime('%Y-%m-%d')

def generateData(link, page_number):
    """Generate data from a rate link"""
    logging.info(f"Fetching: {link}")
    
    try:
        r = requests.get(link, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {link}: {str(e)}")
        return 0

    soup = BeautifulSoup(r.content, 'html.parser')
    tables = soup.find_all("table")
    logging.info(f"Found {len(tables)} tables")

    # Get date for this page
    date = get_date_for_page(page_number)
    logging.info(f"Using date: {date}")

    file_exists = os.path.isfile(FILE_NAME)
    is_empty = not file_exists or os.path.getsize(FILE_NAME) == 0

    row_count = 0
    data = []

    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            tds = row.find_all("td")
            if len(tds) != 6:
                continue

            row_data = []
            for idx, td in enumerate(tds):
                strong_tag = td.find("strong")
                text = strong_tag.get_text(strip=True) if strong_tag else td.get_text(strip=True)

                if not text:
                    break

                if idx == 1:
                    row_data.append(item_marathi_to_english.get(text, text))
                elif idx == 2:
                    row_data.append(unit_marathi_to_english.get(text, text))
                elif idx in [4, 5]:
                    try:
                        price = text.split(" ")[1].split("/")[0]
                        row_data.append(float(price))
                    except (IndexError, ValueError):
                        row_data.append(None)
                else:
                    row_data.append(text)

            if len(row_data) == 6:
                data.append(row_data)
                row_count += 1

    # Save to CSV
    with open(FILE_NAME, mode="a", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        if is_empty:
            writer.writerow(["Code No", "Item", "Unit", "Quantity", "Min", "Max", "Date"])
        for row in data:
            writer.writerow(row + [date])

    # Save to JSON
    json_data = []
    for row in data:
        json_data.append({
            "code_no": row[0],
            "item": row[1],
            "unit": row[2],
            "quantity": row[3],
            "min_price": row[4],
            "max_price": row[5],
            "date": date
        })
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    logging.info(f"Appended {row_count} rows")
    return row_count

def deleteFiles():
    """Delete existing data files"""
    for file in [FILE_NAME, JSON_FILE]:
        if os.path.exists(file):
            os.remove(file)
            logging.info(f"Deleted {file}")

def main():
    """Main function to orchestrate the scraping process"""
    logging.info("Starting scraping process")
    deleteFiles()
    
    try:
        links = get_links(BASE_URL)
        if not links:
            logging.error("No links found. Exiting.")
            return
            
        total_rows = 0
        
        for idx, link in enumerate(links):
            if idx == LOOKUP_COUNT:
                break
            logging.info(f"Processing link {idx + 1}/{min(len(links), LOOKUP_COUNT)}")
            total_rows += generateData(link, idx)
        
        logging.info(f"Scraping completed. Total rows collected: {total_rows}")
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
    