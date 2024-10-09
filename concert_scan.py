"""
Main concert_scan.py file to open GUI
Updated 10/9/2024

Run: 
python3 concert_scan.py
"""

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, QLabel, QVBoxLayout, QFormLayout, QTextEdit, QScrollArea, QSpacerItem, QSizePolicy, QHBoxLayout, QCheckBox

import sys
import database

class MainWindow(QWidget):
    """
    Main Window of Widget
    """

    def __init__(self):

        super().__init__()

        # Set window dimensions
        self.title = "Concert Scan"
        self.left = 20
        self.top = 75
        self.width = 200
        self.height = 130

        # Set style sheet with background color and font color
        self.setStyleSheet("background-color: #8eb3e6; color: black")
        self.setWindowTitle("Color")

        # Add logo to main window 
        self.logo = QLabel()
        pixmap = QPixmap('test logo.png')
        self.logo.setPixmap(pixmap)

        # Write out buttons and Concert Scan information
        self.main_label = QLabel("Concert Scan is a personal app designed to pull \nconcert information from all across the Eugene area.")
        self.main_label.setStyleSheet("color: black")
        layout = QVBoxLayout()
        layout.addWidget(self.logo)
        layout.addWidget(self.main_label)

        # Add search by artist button and set fixed width
        self.artist_button = QPushButton("Search by Artist", self)
        self.artist_button.setFixedWidth(150)
        self.artist_button.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
        layout.addWidget(self.artist_button, 0)
        layout.addSpacing(10)

        # Add search by date button and set fixed width
        self.date_button = QPushButton("Search by Date", self)
        self.date_button.setFixedWidth(150)
        self.date_button.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
        layout.addWidget(self.date_button, 1)
        layout.addSpacing(10)

        # Add search by venue button and set fixed width
        self.venue_button = QPushButton("Search by Venue", self)
        self.venue_button.setFixedWidth(150)
        self.venue_button.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
        layout.addWidget(self.venue_button, 2)
        layout.addSpacing(10)

        # Connect clicking each button with a new unique window
        self.artist_button.clicked.connect(self.artist_window)
        self.date_button.clicked.connect(self.date_window)
        self.venue_button.clicked.connect(self.venue_window)

        # Add information on the bottom of the page about the creation of the project
        self.info_label = QLabel("This app was created by Kylie Griffiths for CS 407\nWinter Term (2024) - University of Oregon")
        self.info_label.setStyleSheet("color: black")

        layout.addWidget(self.info_label)

        layout.addWidget(self.venue_button)

        self.setLayout(layout) # Set layout

        self.initUI() # Initiate the UI

    def initUI(self):
        """
        Initiate the UI function
        """
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def artist_window(self):
        """
        Open the "Search by Artist" window
        """
        self.artist_w = ArtistWindow()
        self.artist_w.show()

    def date_window(self):
        """
        Open the "Search by Date" window
        """
        self.date_w = DateWindow()
        self.date_w.show()

    def venue_window(self):
        """
        Open the "Search by Venue" window
        """
        self.date_w = VenueWindow()
        self.date_w.show()

class ArtistWindow(QWidget):
    """
    Define the "Search by Artist" window and give functionality
    """

    def __init__(self):

        super().__init__()
        self.error_msg = Artist_Failure_Window()

        # Set dimensions, title, and look for the pop-out window
        self.title = "Artist Selection"
        self.left = 200
        self.top = 100
        self.width = 400
        self.height = 200
        self.setStyleSheet("background-color: #8eb3e6; color: black")
        self.setWindowTitle("Color")

        # Add search bar with typing functionality
        outer_layout = QVBoxLayout()
        top_layout = QFormLayout()
        self.artist_write = QLineEdit()
        self.artist_write.setPlaceholderText("ex: Symphony")
        self.artist_write.setStyleSheet("QLineEdit { background-color: #6f97d9; color: #abc7f5;} QLineEdit:hover { background-color: #85a4d6; } QLineEdit:focus { color: black; }")

        # Add submit button to submit the typed text
        self.artist_submit = QPushButton("Submit")
        self.artist_submit.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
        self.artist_submit.setFixedWidth(135)
        top_layout.addRow("Enter the name of a band or performer:", self.artist_write) # Line above search bar

        # Add spacing
        spacer_item = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # Connect the clicked button with submitting the artist name
        self.artist_submit.clicked.connect(self.submit_artist_name)
        top_layout.addWidget(self.artist_submit)

        top_layout.addItem(spacer_item)
        outer_layout.addLayout(top_layout)

        # Add display box for displaying results of artist
        self.result_display = QTextEdit()  # QTextEdit for displaying results
        self.result_display.setReadOnly(True)  # Make the QTextEdit read-only
        outer_layout.addWidget(self.result_display)

        self.link_scroll_area = QScrollArea()  # Scrollable area for link buttons
        self.link_scroll_area.setWidgetResizable(True)

        self.link_label = QLabel("Link(s):")
        outer_layout.addWidget(self.link_label)
        outer_layout.addWidget(self.link_scroll_area)

        self.link_widget = QWidget()  # Widget to contain link buttons
        self.link_layout = QVBoxLayout(self.link_widget)  # Layout for link buttons
        self.link_widget.setStyleSheet("QWidget { background-color: #6f97d9; }")
        self.link_scroll_area.setWidget(self.link_widget)

        self.setLayout(outer_layout)
        self.initUI() # Show the UI

    def submit_artist_name(self):
        """
        Connect the submit artist button with database.py
        Display results in textbox
        """

        text = self.artist_write.text() # Get artist name
        self.artist_write.clear()
        self.result_display.clear()

        # Empty the textbox widget of links after submitting a new artist
        for i in reversed(range(self.link_layout.count())):
            widget = self.link_layout.itemAt(i).widget()
            if widget is not None:
                self.link_layout.removeWidget(widget)
                widget.deleteLater()

        # If text is empty, show the Artist Failure error message window
        if text.strip() == "":
            self.error_msg.show()
            return

        # Send the artist name into database and get a list of artists back or False
        result = database.find_artist(text)

        if not result: # result == False means no artists matching this name were found
            display_string = "No Eugene events were found for this performer in the upcoming months."
            self.result_display.append(display_string)

        else:
            index = 1 # Use index to number the list

            # Cycle through all found events
            for event in result:

                # Create display string to standardize how they appear
                display_string = str(index)+": "+event.get("Artist")+" on "+event.get("Date")+" at "+event.get("Venue")
                self.result_display.append(display_string)
                artist_name = (event.get("Artist"))

                # Remove ampersand and add "and"
                if '&' in artist_name:
                    artist_name = artist_name.replace("&", "and")

                # Make a clickable button out of the artists name
                button_text = str(index)+": "+artist_name.strip()

                link_text = event.get("Link")
                link_button = QPushButton(button_text)  # Create link button
                link_button.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")

                # Connect button click with URL
                link_button.clicked.connect(lambda _, 
                                        link=link_text: QDesktopServices.openUrl(QUrl(link)))
                self.link_layout.addWidget(link_button) # Add button to the read-only textbox
                index = index + 1

    def initUI(self):
        """
        Initialize Artist Window
        """
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

class Artist_Failure_Window(QWidget):
    """
    Create the Failure window for not entering an artist
    """
    def __init__(self):

        super().__init__()

        # Create proportions and look of error message 
        self.title = "Error Message"
        self.left = 300
        self.top = 150
        self.width = 175
        self.height = 60
        self.setStyleSheet("background-color: #8eb3e6; color: black")
        self.setWindowTitle("Color")
        layout = QVBoxLayout()
        
        # Add text to error message
        self.error_message = QLabel("No artist was written.")
        layout.addWidget(self.error_message)
        self.setLayout(layout) # Set layout into window
        self.initUI() # Initialize the error window

    def initUI(self):
        """ 
        Initialize artist error messgae
        """
        #resize windowx
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
class DateWindow(QWidget):
    """
    Define the "Search by Date" window and give functionality
    """

    def __init__(self):
            
        super().__init__()

        # Set window dimensions  for Date Selection 
        self.title = "Date Selection"
        self.left = 200
        self.top = 100
        self.width = 400
        self.height = 120
        self.setStyleSheet("background-color: #8eb3e6; color: black")
        self.setWindowTitle("Color")

        # Set boxes for window
        top_layout = QVBoxLayout()
        outer_layout = QVBoxLayout()

        # Add first text box for start date
        self.start_date = QLineEdit()
        self.start_date.setPlaceholderText("ex: 05/11/2024") # Example date
        self.start_date.setStyleSheet("QLineEdit { background-color: #6f97d9; color: #abc7f5;} QLineEdit:hover { background-color: #85a4d6; } QLineEdit:focus { color: black; }")

        # Add second text box for end date
        self.end_date = QLineEdit()
        self.end_date.setPlaceholderText("ex: 07/11/2024") # Example date
        self.end_date.setStyleSheet("QLineEdit { background-color: #6f97d9; color: #abc7f5;} QLineEdit:hover { background-color: #85a4d6; } QLineEdit:focus { color: black; }")

        # Add button to submit the date
        self.date_submit = QPushButton("Submit")
        self.date_submit.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
        self.date_submit.setFixedSize(80,20)
        self.date_start_text = QLabel("Enter a starting date:") # Instructions above first textbox
        self.date_end_text = QLabel("Enter an ending date:") # Instructions above second textbox

        # Add widgets to layout
        top_layout.addWidget(self.date_start_text)
        top_layout.addWidget(self.start_date)
        top_layout.addWidget(self.date_end_text)
        top_layout.addWidget(self.end_date)

        self.date_submit.clicked.connect(self.submit_dates) # Connect button to submit dates

        top_layout.addSpacing(12)
        top_layout.addWidget(self.date_submit)

        # Add box to display results
        outer_layout.addLayout(top_layout)
        self.result_label = QLabel("Upcoming Event(s):", self)
        outer_layout.addWidget(self.result_label)

        self.result_display = QTextEdit()  # QTextEdit for displaying results
        self.result_display.setPlaceholderText("Events will appear once dates are submitted.")
        self.result_display.setReadOnly(True)  # Make the QTextEdit read-only
        self.result_display.setFixedSize(360, 180)
        outer_layout.addWidget(self.result_display)

        # Set scrollable area for links to click
        self.link_scroll_area = QScrollArea()  # Scrollable area for link buttons
        self.link_scroll_area.setFixedSize(360, 150)
        self.link_scroll_area.setWidgetResizable(True)

        # Add text to scrollable area for links
        self.link_label = QLabel("Link(s):", self)
        outer_layout.addWidget(self.link_label)
        outer_layout.addWidget(self.link_scroll_area)

        self.link_widget = QWidget()  # Widget to contain link buttons
        self.link_layout = QVBoxLayout(self.link_widget)  # Layout for link buttons
        self.link_widget.setStyleSheet("QWidget { background-color: #6f97d9; }")
        self.link_scroll_area.setWidget(self.link_widget)

        self.setLayout(outer_layout) # Set layout
        self.initUI() # Initiate the date window

    def initUI(self):
        """
        Initalize Date Window UI
        """
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
    def submit_dates(self):
        """
        Functionality to connect Submit Dates to database.py
        """

        # Get start and end date strings and clear display
        start_text = self.start_date.text()
        end_text = self.end_date.text()
        self.start_date.clear()
        self.end_date.clear()
        self.result_display.clear()

        # Remove links from the widget
        for i in reversed(range(self.link_layout.count())):
            widget = self.link_layout.itemAt(i).widget()
            if widget is not None:
                self.link_layout.removeWidget(widget)
                widget.deleteLater()

        # Check if the dates have been entered
        if not database.check_date_format(start_text) or not database.check_date_format(end_text):
            self.fail_window = Date_Failure_Window() # Show failure window if no date entered
            self.fail_window.show()
        else:
            result = database.find_dates(start_text, end_text) # Connect to database and get events

            if not result: # If no events, display string 
                display_string = "No events found in this time period.\nTry entering a new date range."
                self.result_display.append(display_string)

            else:
                index = 1 # Index for counting links

                for event in result:
                    
                    # Write display string using event data
                    display_string = str(index)+": "+event.get("Artist")+" on "+event.get("Date")+" at "+event.get("Venue")

                    # Add text to display
                    self.result_display.append(display_string)
                    link_text = event.get("Link")
                    artist_name = (event.get("Artist"))

                    # Remove ampersand
                    if '&' in artist_name:
                        artist_name = artist_name.replace("&", "and")

                    # Add text to the link button with the artist name
                    button_text = str(index)+": "+artist_name
                    link_button = QPushButton(button_text)  # Create link button
                    link_button.setStyleSheet("QPushButton { color: #0e4282; text-decoration: underline; }")

                    # Connect URL to button click
                    link_button.clicked.connect(lambda _, link=link_text: QDesktopServices.openUrl(QUrl(link)))
                    self.link_layout.addWidget(link_button)

                    index = index + 1

        self.start_date.clear() # Clear start and end date
        self.end_date.clear()
        
class Date_Failure_Window(QWidget):
    """
    Create window to be displayed when date entering is empty
    """

    def __init__(self):
        super().__init__()

        # Set window dimensions
        self.title = "Error Message"
        self.left = 300
        self.top = 150
        self.width = 300
        self.height = 150
        self.setStyleSheet("background-color: #8eb3e6; color: black")
        self.setWindowTitle("Color")

        # Add box for error message 
        layout = QVBoxLayout()
        self.error_message = QLabel("Date was entered incorrectly. \nPlease ensure it is written in the form MM/DD/YYYY.")
        layout.addWidget(self.error_message)

        self.setLayout(layout)
        self.initUI() # Initialize error message window

    def initUI(self):
        """
        Initialize the error window
        """
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
   
class VenueWindow(QWidget):
    """
    Define the "Search by Venue" window and give functionality
    """

    def __init__(self):

        super().__init__()
        self.venue_error = Venue_Failure_Window()

        # Set window dimensions and look
        self.title = "Venue Selection"
        self.left = 200
        self.top = 100
        self.width = 300
        self.height = 200
        self.setStyleSheet("background-color: #8eb3e6; color: black")
        self.setWindowTitle("Color")

        # Set box layouts
        outer_layout = QVBoxLayout()
        top_layout = QFormLayout()
        optionsLayout = QVBoxLayout()

        # Add text above options
        text_widget = QLabel("Select your venue(s) to view")
        top_layout.addWidget(text_widget)

        # Set checkbox options of current event locations
        self.knight = QCheckBox("Matthew Knight Arena")
        optionsLayout.addWidget(self.knight)
        self.hult = QCheckBox("Hult Center")
        optionsLayout.addWidget(self.hult)
        self.mcdonald = QCheckBox("McDonald Theatre")
        optionsLayout.addWidget(self.mcdonald)
        self.cuthbert = QCheckBox("Cuthbert Amphitheater")
        optionsLayout.addWidget(self.cuthbert)

        # Add the layouts
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(optionsLayout)

        # Create a submit button and fix size
        self.venue_submit = QPushButton("Submit")
        self.venue_submit.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
        self.venue_submit.setFixedSize(80,20)

        outer_layout.addWidget(self.venue_submit)

        # Connect clicking submit with submit_venues
        self.venue_submit.clicked.connect(self.submit_venues)
        self.venue_submit.clicked.connect(self.unclick)

        self.result_label = QLabel("Upcoming Event(s):", self)
        outer_layout.addWidget(self.result_label)
        self.result_display = QTextEdit()  # QTextEdit for displaying results
        self.result_display.setPlaceholderText("Events will appear once dates are submitted.")
        self.result_display.setReadOnly(True)  # Make the QTextEdit read-only

        # Set size of scrollable event widget
        self.result_display.setFixedSize(500, 100)
        outer_layout.addWidget(self.result_display)

        self.link_scroll_area = QScrollArea()  # Scrollable area for link buttons
        self.link_scroll_area.setFixedSize(500, 300)
        self.link_scroll_area.setWidgetResizable(True)

        # Add text for links
        self.link_label = QLabel("Link(s):", self)
        outer_layout.addWidget(self.link_label)
        outer_layout.addWidget(self.link_scroll_area)

        self.link_widget = QWidget()  # Widget to contain link buttons
        self.link_layout = QVBoxLayout(self.link_widget)  # Layout for link buttons
        self.link_widget.setStyleSheet("QWidget { background-color: #6f97d9; }")
        self.link_scroll_area.setWidget(self.link_widget)

        self.setLayout(outer_layout) # Set the layout

        self.initUI() # Initialize the Venue UI

    def initUI(self):
        """
        Initialize Venue UI
        """
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
    def submit_venues(self):
        """
        Connect submit button press with database.py
        Get list of events
        """

        # Clear list of events
        self.result_display.clear()

        # Clear any links left on the link box
        for i in reversed(range(self.link_layout.count())):
            widget = self.link_layout.itemAt(i).widget()
            if widget is not None:
                self.link_layout.removeWidget(widget)
                widget.deleteLater()

        # Get list of locations that were clicked
        locations = []
        if self.knight.isChecked():
            locations.append("Matthew Knight Arena")
        if self.hult.isChecked():
            locations.append("Hult Center")
        if self.mcdonald.isChecked():
            locations.append("McDonald Theatre")
        if self.cuthbert.isChecked():
            locations.append("Cuthbert Amphitheater")

        # If no locations selected, show error window
        if len(locations) == 0:
            # Show error window
            self.venue_error.show()

        else:
            # Connect to database with list of locations
            result = database.search_by_venue(locations)
            index = 1
            
            # Cycle through list of events from each location
            for events in result:

                for event in events:

                    # Get standardized display string
                    display_string = str(index)+": "+event.get("Artist")+" on "+event.get("Date")+" at "+event.get("Venue")
                    self.result_display.append(display_string)
                    link_text = event.get("Link")
                    artist_name = (event.get("Artist"))

                    # Remove ampersand
                    if '&' in artist_name:
                        artist_name = artist_name.replace("&", "and")

                    # Add button text for the link in the scrollable link area
                    button_text = str(index)+": "+artist_name
                    link_button = QPushButton(button_text)  # Create link button
                    link_button.setStyleSheet("QPushButton { color: #0e4282; text-decoration: underline; }")

                    # Connect link clicking with URL
                    link_button.clicked.connect(lambda _, link=link_text: QDesktopServices.openUrl(QUrl(link)))
                    self.link_layout.addWidget(link_button)
                    index = index + 1

    def unclick(self):
        """
        Once Location button is pressed, unclick all the boxes
        """
        self.knight.setChecked(False)
        self.hult.setChecked(False)
        self.mcdonald.setChecked(False)
        self.cuthbert.setChecked(False)

class Venue_Failure_Window(QWidget):
    """
    Initialize Venue Failure window
    """

    def __init__(self):
        super().__init__()

        # Set window dimensions and look
        self.title = "Error Message"
        self.left = 300
        self.top = 150
        self.width = 200
        self.height = 75
        self.setStyleSheet("background-color: #8eb3e6; color: black")
        self.setWindowTitle("Color")
        layout = QVBoxLayout()

        # Write text for error message
        self.error_message = QLabel("No venue was selected.")
        layout.addWidget(self.error_message)

        # Set layout and initialize window
        self.setLayout(layout)
        self.initUI()

    def initUI(self):
        """
        Initialize error window for venue
        """
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

if __name__ == "__main__":
    # Run concert_scan.py
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show() # Show the window
    sys.exit(app.exec()) # Exit the system when the window is closed
