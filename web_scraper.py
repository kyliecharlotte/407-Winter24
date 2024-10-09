"""
Web Scraping Module for concert_scan.py
Updated 10/9/2024

Run:
python3 web_scraper.py
"""

import csv
import json
from urllib.request import urlopen, Request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class CSV_concert_file:
    """
    Class for concert CSV file
    - init: Sets filename
    - create_csv: writes headers to CSV
    - append_to_csv: add rows to CSV
    """

    def __init__(self, filename):
        self.filename = filename

    def create_csv(self, headers):
        """
        Create a new CSV file and write headers
        """
        with open(self.filename, 'w', newline='', encoding="UTF-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

    def append_to_csv(self, data: list):
        """
        Write rows to CSV file
        """
        with open(self.filename, 'a', newline = '', encoding="UTF-8")as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data)

def Matthew_Knight_Arena_scraper():
    """
    Scraper for Matthew Knight Arena
    No Input
    - Opens webpage with content
    - Pulls all events and gets artist, date, and link
    - Appends new events to CSV file
    Return
    """

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

    find_events = soup.find_all("script", type="application/ld+json") # Find all events into list

    for event in find_events: # Cycle through events

        if event:

            csv_data = [] # New csv data list for each event
            event = json.loads(event.text)

            artist = event["name"] # Get artist name
            csv_data.append(artist.strip())

            date = event["startDate"] # Get date (startDate if multiple)

            csv_data.append(date.split("T")[0].strip())
            csv_data.append("Matthew Knight Arena")

            link = event["url"] # Get URL
            csv_data.append(link)

            CSV_concerts.append_to_csv(csv_data)

    driver.quit()

    return

def Hult_Center_Scraper():
    """
    Scraper for Hult Center
    No Input
    - Opens webpage with content
    - Pulls all events and gets artist, date, and link
    - Appends new events to CSV file
    Return
    """

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
 
        for event in find_events: # Cycle through events

            csv_data = []
            event_artist = event.find("a", class_="c-event-card__permalink").text.strip() # Get artist
            event_time = " ".join(event.find("time",
                                            class_="c-event-card__daterange u-highlight").text.split(", ")[0:2]).strip()
            csv_data.append(event_artist)
            csv_data.append(event_time)
            csv_data.append("Hult Center")
            ticket_link = event.find("div", class_="c-event-card__actions").find("a").get("href") # Get link
            csv_data.append(ticket_link.strip())

            CSV_concerts.append_to_csv(csv_data)

        driver.quit()

        return

def Cuthbert_Amphitheater_Scraper():
    """
    Scraper for the Cuthbert Amphitheater
    No Input
    - Opens webpage with content
    - Pulls all events and gets artist, date, and link
    - Appends new events to CSV file
    Return
    """

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Initialize Chrome WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)

    link = "https://thecuthbert.com/events/"

    driver.get(link)
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")

    list_of_concerts = soup.find_all("article", id) # Get a list of upcoming events

    for concert in list_of_concerts: # Cycle through events

        csv_data = []
        concert_name_and_date = concert.find("div",
                                            class_="fusion-post-content post-content").find("a").text
        concert_name_and_date = concert_name_and_date.strip().split("–") # Split name and date of show

        concert_name = concert_name_and_date[1] # Get name from list of split name, date
        csv_data.append(concert_name.strip())
        concert_date = concert_name_and_date[0] # Get date from split
        csv_data.append(concert_date.strip())
        csv_data.append("Cuthbert Amphitheater")

        # Get link to concert
        concert_link = concert_name_and_date = concert.find("div",
                                                    class_="fusion-post-content post-content").find("a").get("href")
        csv_data.append(concert_link.strip())

        CSV_concerts.append_to_csv(csv_data)
 
    driver.quit()

def McDonald_Theatre_Scraper():
    """
    Scraper for the McDonald Theatre
    No Input
    - Opens webpage with content
    - Pulls all events and gets artist, date, and link
    - Appends new events to CSV file
    Return
    """

    link = "https://mcdonaldtheatre.com/events/"

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode

    # Initialize Chrome WebDriver with the configured options
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(link)
    html_content = driver.page_source

    soup = BeautifulSoup(html_content, "html.parser")

    list_of_events = soup.find_all("div", class_="fusion-post-content-wrapper") # Get event list

    for event in list_of_events:

        csv_data = []

        # Get event name and date as one string split into list
        event_date_name = event.find("div", class_="fusion-post-content post-content").find("a").text.strip().split("–")
        event_name = event_date_name[1].strip() # Get name from split list

        csv_data.append(event_name)

        event_date = event_date_name[0].strip() # Get date from split list
        csv_data.append(event_date)

        event_link = event.find("div", 
                            class_="fusion-post-content post-content").find("a").get("href") # Get link
        csv_data.append("McDonald Theatre")
        csv_data.append(event_link)

        CSV_concerts.append_to_csv(csv_data)

if __name__ == "__main__":

    CSV_concerts = CSV_concert_file("concert_file.csv")
    CSV_concerts.create_csv(["Artist", "Date", "Venue", "Link"])

    ### Web Scraping Calls ###
    Matthew_Knight_Arena_scraper()
    Hult_Center_Scraper()
    Cuthbert_Amphitheater_Scraper()
    McDonald_Theatre_Scraper()
