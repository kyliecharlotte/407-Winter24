from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen, Request
import csv
import requests

concert_dictionary = {"Matthew Knight Arena": ""}
CSV_file = "concert_file.csv"

class CSV_concert_file:
    def __init__(self, filename):
        self.filename = filename

    def create_csv(self, headers):
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
    
    def append_to_csv(self, data: list):
        with open(self.filename, 'a', newline = '')as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)
        

def Matthew_Knight_Arena_scraper():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Initialize Chrome WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)

    link = "https://www.livenation.com/venue/KovZpZAEe1eA/matthew-knight-arena-events"

    # Use Selenium to get the dynamically loaded content
    driver.get(link)
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")
    
    find_events = soup.find_all("li", role="group") 

    for event in find_events:

        CSV_data = []

        artist = event.find("h3", class_="css-1ptng6s").text.split(" - ")[0]
        CSV_data.append(artist.strip())
        date = event.find("div", class_="css-qjpp58").text
        CSV_data.append(date.strip())
        CSV_data.append("Matthew Knight Arena")
        link = event.find("div", class_="chakra-linkbox css-5nbufm").find("a").get("href")
        CSV_data.append(link)
        CSV_concerts.append_to_csv(CSV_data)

    driver.quit()

    return

def Hult_Center_Scraper():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Initialize Chrome WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)

    link_list = ["https://hultcenter.org/events-tickets/?date=&genre=music", "https://hultcenter.org/events-tickets/page/2/?date&genre=music", "https://hultcenter.org/events-tickets/page/3/?date&genre=music", "https://hultcenter.org/events-tickets/?date=&genre=comedy"]

    for link in link_list:
        # Use Selenium to get the dynamically loaded content
        driver.get(link)
        html_content = driver.page_source

        soup = BeautifulSoup(html_content, "html.parser")

        find_events = soup.find_all("div", class_="c-event-card c-col o-grid__cell u-1/3@desktop") 
        
        for event in find_events:

            CSV_data = []
            event_artist = event.find("a", class_="c-event-card__permalink").text.strip()
            event_time = " ".join(event.find("time", class_="c-event-card__daterange u-highlight").text.split(", ")[0:2]).strip()
            CSV_data.append(event_artist)
            CSV_data.append(event_time)
            CSV_data.append("Hult Center")
            ticket_link = event.find("div", class_="c-event-card__actions").find("a").get("href")
            CSV_data.append(ticket_link.strip())

            CSV_concerts.append_to_csv(CSV_data)

        driver.quit()

        return

def Cuthbert_Amphitheater_Scraper():
    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Initialize Chrome WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)

    link = "https://thecuthbert.com/events/"

    driver.get(link)
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")

    list_of_concerts = soup.find_all("article", id)
    for concert in list_of_concerts:

        CSV_data = []
        concert_name_and_date = concert.find("div", class_="fusion-post-content post-content").find("a").text
        concert_name_and_date = concert_name_and_date.strip().split("–")

        concert_name = concert_name_and_date[1]
        CSV_data.append(concert_name.strip())
        concert_date = concert_name_and_date[0]
        CSV_data.append(concert_date.strip())
        CSV_data.append("Cuthbert Amphitheater")
        concert_link = concert_name_and_date = concert.find("div", class_="fusion-post-content post-content").find("a").get("href")
        CSV_data.append(concert_link.strip())

        CSV_concerts.append_to_csv(CSV_data)
    driver.quit()

def McDonald_Theatre_Scraper():

    link = "https://mcdonaldtheatre.com/events/"

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Initialize Chrome WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(link)
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")

    list_of_events = soup.find_all("div", class_="fusion-post-content-wrapper")
    for event in list_of_events:
        CSV_data = []
        event_date_name = event.find("div", class_="fusion-post-content post-content").find("a").text.strip().split("–")
        event_name = event_date_name[1].strip()
        CSV_data.append(event_name)
        event_date = event_date_name[0].strip()
        CSV_data.append(event_date)
        event_link = event.find("div", class_="fusion-post-content post-content").find("a").get("href")
        CSV_data.append("McDonald Theatre")
        CSV_data.append(event_link)

        CSV_concerts.append_to_csv(CSV_data)

if __name__ == "__main__":
    
    CSV_concerts = CSV_concert_file("concert_file.csv") 
    CSV_concerts.create_csv(["Artist", "Date", "Venue", "Link"])
    
    ###Web Scraping Calls###
    Matthew_Knight_Arena_scraper()
    Hult_Center_Scraper()
    Cuthbert_Amphitheater_Scraper()
    McDonald_Theatre_Scraper()