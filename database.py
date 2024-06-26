"""Functions to navigate CSV file and pull events"""

import pandas as pd
import re
import datetime

def find_artist(artist_name: str):

    if artist_name.strip() == '':
        return False
    
    df = pd.read_csv("concert_file.csv")
    df = pd.DataFrame(df)

    list_of_artists = df['Artist'].to_list()
    rows = []
    added_to_rows = False
    row_list = []

    for artist in list_of_artists:
        if artist_name.lower() in artist.lower():
            rows.extend(df[df["Artist"] == artist].to_dict(orient="records"))
            added_to_rows = True
    
    if added_to_rows is False:
        return False
    return rows

def check_date_format(date_string):
    pattern = r'^\d{2}/\d{2}/\d{4}$'
    if re.match(pattern, date_string):
        return True
    else:
        return False
    
def standardize_date(date: str):
    current_year = datetime.datetime.now().year
    try:
        # Attempt to parse input_date as MM/DD/YYYY format
        standardized_date = datetime.datetime.strptime(date, '%m/%d/%Y')
    except ValueError:
        try:
            # Attempt to parse input_date as a different format
            standardized_date = datetime.datetime.strptime(date, '%B %d %Y')
        except ValueError:
            try:
                standardized_date = datetime.datetime.strptime(date, '%a %b %d')
            except ValueError:
                try:
                    standardized_date = datetime.datetime.strptime(date + ' ' + str(current_year), '%b %d %Y')
                except ValueError:
            # If both formats fail, return None
                    standardized_date = None
    return standardized_date

def find_dates(start_date: str, end_date:str):
    standardized_start = standardize_date(start_date)
    standardized_end = standardize_date(end_date)

    df = pd.read_csv("concert_file.csv")
    df = pd.DataFrame(df)

    list_of_dates = df['Date'].to_list()

    rows = []
    added_to_rows = False

    for dates in list_of_dates:
        split_one = dates.split("—")
        date_fix = split_one[0]
        date_fix = " ".join(date_fix.split(", "))
        new_date = standardize_date(date_fix)
        if standardized_start < new_date and standardized_end > new_date:
            rows.extend(df[df["Date"] == dates].to_dict(orient="records"))
            added_to_rows = True
    if added_to_rows == False:
        return False
    else:
        return rows
    
def search_by_venue(venue_list: list):

    df = pd.read_csv("concert_file.csv")
    df = pd.DataFrame(df)
    list = []
    
    for venue in venue_list:
        venue_rows = df[df['Venue'] == venue].to_dict(orient="records")
        list.append(venue_rows)

    print(list)

    return list
   
if __name__ == "__main__":
    find_dates("05/11/2024", "05/11/2025")