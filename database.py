"""
Database File to navigate CSV file and pull events for concert_scan.py
Updated 10/9/2024

Run: 
python3 database.py
"""

import re
import datetime
import pandas as pd

def find_artist(artist_name: str):
    """
    Functionality for "Find Artist" button on GUI
    Input: 
        - artist_name: str - user-entered artist
    Find any artist in the list with a name in the entered artist's name
    Return 
        - False if rows is empty 
        or 
        - rows: list of artist info
    """

    # Check if artist's name is empty
    if artist_name.strip() == '':
        return False

    # Read CSV file with artist names
    df = pd.read_csv("concert_file.csv")
    df = pd.DataFrame(df)

    # Get artist names from dataframe to match
    list_of_artists = df['Artist'].to_list()
    rows = []
    added_to_rows = False

    for artist in list_of_artists:

        # If artist_name matches entered artist name, add to rows
        if artist_name.lower() in artist.lower():
            rows.extend(df[df["Artist"] == artist].to_dict(orient="records"))
            added_to_rows = True # Rows is not empty

    # Sends a False back if no matching artists
    if added_to_rows is False:
        return False

    return rows

def check_date_format(date_string):
    """
    Functionality for "Enter Date" button on GUI
    Checks if a date is properly formatted as dd/dd/dddd
    Input: 
        - date_string: str
    Find any artist in the list with a name in the entered artist's name
    Return 
        - True if str matches
        or 
        - False if str does not match
    """

    pattern = r'^\d{2}/\d{2}/\d{4}$' # This is pattern to check for

    if re.match(pattern, date_string): # If pattern matches, return True
        return True
    else:
        return False # If not, False

def standardize_date(date: str):
    """
    Functionality for "Enter Date" button on GUI
    Checks what form a date is in and converts to datetime object.
    Input: 
        - date: str
    Return 
        - standardized_date: datetime object 
    """

    current_year = datetime.datetime.now().year # Get the current year
    try:
        # Attempt to parse input_date as MM/DD/YYYY format
        standardized_date = datetime.datetime.strptime(date, '%m/%d/%Y')
    except ValueError:
        try:
            # Attempt to parse input_date as YYYY/MM/DD format
            standardized_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            try:
                # Attempt to parse input_date as Month Day Year
                standardized_date = datetime.datetime.strptime(date, '%B %d %Y')
            except ValueError:
                try:
                    # Attempt to parse input_date as Weekday Mon Date
                    standardized_date = datetime.datetime.strptime(date, '%a %b %d')
                except ValueError:
                    try:
                        # Attempt to parse input_date as Mon Day Year after adding year
                        standardized_date = datetime.datetime.strptime(date + ' ' + str(current_year), 
                                                                    '%b %d %Y')
                    except ValueError:
                # If all formats fail, return None
                        standardized_date = None

    return standardized_date

def find_dates(start_date: str, end_date:str):
    """
    Functionality for "Search by Date" button on GUI
    Takes a start and end date and finds events happening in the time period
    Input: 
        - start_date: str - starting date
        - end_date: str - ending date
    Return 
        - False if no events
        or
        - rows: list of events
    """

    # Standardized the entered start and end dates
    standardized_start = standardize_date(start_date)
    standardized_end = standardize_date(end_date)

    # Read in CSV file of events
    df = pd.read_csv("concert_file.csv")
    df = pd.DataFrame(df)

    # Get dates for each event
    list_of_dates = df['Date'].to_list()

    rows = []
    added_to_rows = False

    for dates in list_of_dates: # Cycle through dates

        split_one = dates.split("—") # Split the current date to remove "-"
        date_fix = split_one[0]
        date_fix = " ".join(date_fix.split(", ")) # Join dates, removing "," and "-"
        new_date = standardize_date(date_fix) # Standardize the date

        # Check if the current date fits in the time frame
        if standardized_start < new_date and standardized_end > new_date: 
            rows.extend(df[df["Date"] == dates].to_dict(orient="records")) # Add to rows if it fits
            added_to_rows = True

    if not added_to_rows: # If row is empty, return False
        return False

    else:
        return rows
    
def search_by_venue(venue_list: list):
    """
    Functionality for "Search by Venue" button on GUI
    Takes a list of venues and pulls their events
    Input: 
        - venue_list: list - names of venues to search for
    Return
        - ev_list: list - list of events for all selected venues

    """

    df = pd.read_csv("concert_file.csv") # Read CSV file
    df = pd.DataFrame(df)
    ev_list = []

    for venue in venue_list:
        # Get all of the events in the dataframe with that venue
        venue_rows = df[df['Venue'] == venue].to_dict(orient="records")
        ev_list.append(venue_rows)

    print(ev_list) # Print list to console

    return ev_list

if __name__ == "__main__":
    ### Testing ###
    find_dates("05/11/2024", "2025-11-20")
