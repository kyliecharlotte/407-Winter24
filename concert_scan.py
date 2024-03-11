import sys
import re
import database
import web_scraper
from PyQt5.QtCore import pyqtSlot, QUrl
from PyQt5.QtGui import QDesktopServices, QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QToolTip, QLineEdit, QMessageBox, QLabel, QVBoxLayout, QFormLayout, QTextEdit, QScrollArea, QSpacerItem, QSizePolicy, QHBoxLayout, QCheckBox

class MainWindow(QWidget):

    def __init__(self):
            super().__init__()
            self.title = "Entertain Eugene"
            self.left = 20
            self.top = 75
            self.width = 200
            self.height = 140

            self.setStyleSheet("background-color: #8eb3e6; color: black") 
            self.setWindowTitle("Color") 

            self.logo = QLabel()
            pixmap = QPixmap('test logo.png')
            self.logo.setPixmap(pixmap)


            self.main_label = QLabel("Entertain Eugene is a personal app designed to pull \nconcert information from all across the Eugene area.")
            self.main_label.setStyleSheet("color: black")
            layout = QVBoxLayout()
            layout.addWidget(self.logo)
            layout.addWidget(self.main_label)
            self.artist_button = QPushButton("Search by Artist", self)
            self.artist_button.setFixedWidth(150)
            self.artist_button.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
            layout.addWidget(self.artist_button, 0)
            layout.addSpacing(10)
            self.date_button = QPushButton("Search by Date", self)
            self.date_button.setFixedWidth(150)
            self.date_button.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
            layout.addWidget(self.date_button, 1)
            layout.addSpacing(10)
            self.venue_button = QPushButton("Search by Venue", self)
            self.venue_button.setFixedWidth(150)
            self.venue_button.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
            layout.addWidget(self.venue_button, 2)
            layout.addSpacing(10)

            self.artist_button.clicked.connect(self.artist_window)
            self.date_button.clicked.connect(self.date_window)
            self.venue_button.clicked.connect(self.venue_window)

            self.info_label = QLabel("This app was created by Kylie Griffiths for CS 407\nWinter Term (2024) - University of Oregon")
            self.info_label.setStyleSheet("color: black")
 
            layout.addWidget(self.info_label)

            self.setLayout(layout)

            self.initUI()

    def initUI(self):
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def artist_window(self):
        self.artist_w = ArtistWindow()
        self.artist_w.show()

    def date_window(self):
        self.date_w = DateWindow()
        self.date_w.show()

class ArtistWindow(QWidget):
    def __init__(self):
            super().__init__()
            self.title = "Artist Selection"
            self.left = 200
            self.top = 100
            self.width = 400
            self.height = 200
            self.setStyleSheet("background-color: #8eb3e6; color: black") 
            self.setWindowTitle("Color") 

            outer_layout = QVBoxLayout()
            top_layout = QFormLayout()
            self.artist_write = QLineEdit()
            self.artist_write.setPlaceholderText("ex: Selena Gomez")
            self.artist_write.setStyleSheet("QLineEdit { background-color: #6f97d9; color: #abc7f5;} QLineEdit:hover { background-color: #85a4d6; } QLineEdit:focus { color: black; }")

            self.artist_submit = QPushButton("Submit")
            self.artist_submit.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
            self.artist_submit.setFixedWidth(135)
            top_layout.addRow("Enter the name of a band or performer:", self.artist_write)

            spacer_item = QSpacerItem(100, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

            self.artist_submit.clicked.connect(self.submit_artist_name)
            top_layout.addWidget(self.artist_submit)
            top_layout.addItem(spacer_item)
            outer_layout.addLayout(top_layout)

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
            self.initUI()

    def submit_artist_name(self):
        text = self.artist_write.text()
        self.artist_write.clear()
        self.result_display.clear()

        for i in reversed(range(self.link_layout.count())):
            widget = self.link_layout.itemAt(i).widget()
            if widget is not None:
                self.link_layout.removeWidget(widget)
                widget.deleteLater()

        if text.strip() == "":
            self.error_msg = Artist_Failure_Window()
            self.error_msg.show()
            return

        result = database.find_artist(text)

        if result == False:
            display_string = "No Eugene events were found for this performer in the upcoming months."
            self.result_display.append(display_string)

        else:
            index = 1
            for event in result:
                display_string = str(index)+": "+event.get("Artist")+" on "+event.get("Date")+" at "+event.get("Venue")
                self.result_display.append(display_string)
                artist_name = (event.get("Artist"))
                if '&' in artist_name:
                    artist_name = artist_name.replace("&", "and")
                button_text = str(index)+": "+artist_name.strip()
                link_text = event.get("Link")
                link_button = QPushButton(button_text)  # Create link button
                link_button.setStyleSheet("QPushButton { color: blue; text-decoration: underline; }")
                link_button.clicked.connect(lambda _, link=link_text: QDesktopServices.openUrl(QUrl(link)))
                self.link_layout.addWidget(link_button)
                index = index + 1

    def initUI(self):
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

class Artist_Failure_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Error Message"
        self.left = 300
        self.top = 150
        self.width = 175
        self.height = 60
        self.setStyleSheet("background-color: #8eb3e6; color: black") 
        self.setWindowTitle("Color") 
        layout = QVBoxLayout()
        self.error_message = QLabel("No artist was selected.")
        layout.addWidget(self.error_message)
        self.setLayout(layout)
        self.initUI()

    def initUI(self):
        #resize windowx
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
class DateWindow(QWidget):
    def __init__(self):
            super().__init__()
            self.title = "Date Selection"
            self.left = 200
            self.top = 100
            self.width = 400
            self.height = 120
            self.setStyleSheet("background-color: #8eb3e6; color: black") 
            self.setWindowTitle("Color")

            top_layout = QVBoxLayout()
            outer_layout = QVBoxLayout()

            self.start_date = QLineEdit()
            self.start_date.setPlaceholderText("ex: 05/11/2024")
            self.start_date.setStyleSheet("QLineEdit { background-color: #6f97d9; color: #abc7f5;} QLineEdit:hover { background-color: #85a4d6; } QLineEdit:focus { color: black; }")

            self.end_date = QLineEdit()
            self.end_date.setPlaceholderText("ex: 07/11/2024")
            self.end_date.setStyleSheet("QLineEdit { background-color: #6f97d9; color: #abc7f5;} QLineEdit:hover { background-color: #85a4d6; } QLineEdit:focus { color: black; }")

            self.date_submit = QPushButton("Submit")
            self.date_submit.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
            self.date_submit.setFixedSize(80,20)
            self.date_start_text = QLabel("Enter a starting date:")
            self.date_end_text = QLabel("Enter an ending date:")
            top_layout.addWidget(self.date_start_text)
            top_layout.addWidget(self.start_date)
            top_layout.addWidget(self.date_end_text)
            top_layout.addWidget(self.end_date)

            self.date_submit.clicked.connect(self.submit_dates)

            top_layout.addSpacing(12)
            top_layout.addWidget(self.date_submit)

            outer_layout.addLayout(top_layout)
            self.result_label = QLabel("Upcoming Event(s):", self)
            outer_layout.addWidget(self.result_label)
            self.result_display = QTextEdit()  # QTextEdit for displaying results
            self.result_display.setPlaceholderText("Events will appear once dates are submitted.")
            self.result_display.setReadOnly(True)  # Make the QTextEdit read-only
            self.result_display.setFixedSize(360, 180)
            outer_layout.addWidget(self.result_display)

            self.link_scroll_area = QScrollArea()  # Scrollable area for link buttons
            self.link_scroll_area.setFixedSize(360, 150)
            self.link_scroll_area.setWidgetResizable(True)
            
            self.link_label = QLabel("Link(s):", self)
            outer_layout.addWidget(self.link_label)
            outer_layout.addWidget(self.link_scroll_area)

            self.link_widget = QWidget()  # Widget to contain link buttons
            self.link_layout = QVBoxLayout(self.link_widget)  # Layout for link buttons
            self.link_widget.setStyleSheet("QWidget { background-color: #6f97d9; }")
            self.link_scroll_area.setWidget(self.link_widget)

            self.setLayout(outer_layout)
            self.initUI()

    def initUI(self):
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
    def submit_dates(self):
        start_text = self.start_date.text()
        end_text = self.end_date.text()
        self.start_date.clear()
        self.end_date.clear()
        self.result_display.clear()

        for i in reversed(range(self.link_layout.count())):
            widget = self.link_layout.itemAt(i).widget()
            if widget is not None:
                self.link_layout.removeWidget(widget)
                widget.deleteLater()

        if database.check_date_format(start_text) == False or database.check_date_format(end_text) == False:
            self.fail_window = Date_Failure_Window()
            self.fail_window.show()
        else:
            result = database.find_dates(start_text, end_text)
            if result == False:
                display_string = "No events found in this time period.\nCheck your dates for accurate numbers."
                self.result_display.append(display_string)
            else:
                index = 1
                for event in result:
                    display_string = str(index)+": "+event.get("Artist")+" on "+event.get("Date")+" at "+event.get("Venue")
                    self.result_display.append(display_string)
                    link_text = event.get("Link")
                    artist_name = (event.get("Artist"))
                    if '&' in artist_name:
                        artist_name = artist_name.replace("&", "and")
                    button_text = str(index)+": "+artist_name
                    link_button = QPushButton(button_text)  # Create link button
                    link_button.setStyleSheet("QPushButton { color: #0e4282; text-decoration: underline; }")
                    link_button.clicked.connect(lambda _, link=link_text: QDesktopServices.openUrl(QUrl(link)))
                    self.link_layout.addWidget(link_button)
                    index = index + 1

        self.start_date.clear()
        self.end_date.clear()
        
class Date_Failure_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Error Message"
        self.left = 300
        self.top = 150
        self.width = 300
        self.height = 150
        self.setStyleSheet("background-color: #8eb3e6; color: black") 
        self.setWindowTitle("Color") 
        layout = QVBoxLayout()
        self.error_message = QLabel("Date was entered incorrectly. \nPlease ensure it is written in the form MM/DD/YYYY.")
        layout.addWidget(self.error_message)
        self.setLayout(layout)
        self.initUI()

    def initUI(self):
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
         
class VenueWindow(QWidget):

    def __init__(self):
            super().__init__()
            self.title = "Venue Selection"
            self.left = 200
            self.top = 100
            self.width = 300
            self.height = 200
            self.setStyleSheet("background-color: #8eb3e6; color: black") 
            self.setWindowTitle("Color") 
            outer_layout = QVBoxLayout()
            top_layout = QFormLayout()
            optionsLayout = QVBoxLayout()
            text_widget = QLabel("Select your venue(s) to view")
            top_layout.addWidget(text_widget)
            self.knight = QCheckBox("Matthew Knight Arena")
            optionsLayout.addWidget(self.knight)
            self.hult = QCheckBox("Hult Center")
            optionsLayout.addWidget(self.hult)
            self.mcdonald = QCheckBox("McDonald Theatre")
            optionsLayout.addWidget(self.mcdonald)
            self.cuthbert = QCheckBox("Cuthbert Amphitheater")
            optionsLayout.addWidget(self.cuthbert)
            outer_layout.addLayout(top_layout)
            outer_layout.addLayout(optionsLayout)

            self.venue_submit = QPushButton("Submit")
            self.venue_submit.setStyleSheet("QPushButton { background-color: #6f97d9; } QPushButton:hover { background-color: #a2c0e8; }")
            self.venue_submit.setFixedSize(80,20)

            outer_layout.addWidget(self.venue_submit)

            self.venue_submit.clicked.connect(self.submit_venues)
            self.venue_submit.clicked.connect(self.unclick)

            self.result_label = QLabel("Upcoming Event(s):", self)
            outer_layout.addWidget(self.result_label)
            self.result_display = QTextEdit()  # QTextEdit for displaying results
            self.result_display.setPlaceholderText("Events will appear once dates are submitted.")
            self.result_display.setReadOnly(True)  # Make the QTextEdit read-only
            self.result_display.setFixedSize(500, 100)
            outer_layout.addWidget(self.result_display)

            self.link_scroll_area = QScrollArea()  # Scrollable area for link buttons
            self.link_scroll_area.setFixedSize(500, 300)
            self.link_scroll_area.setWidgetResizable(True)
            
            self.link_label = QLabel("Link(s):", self)
            outer_layout.addWidget(self.link_label)
            outer_layout.addWidget(self.link_scroll_area)

            self.link_widget = QWidget()  # Widget to contain link buttons
            self.link_layout = QVBoxLayout(self.link_widget)  # Layout for link buttons
            self.link_widget.setStyleSheet("QWidget { background-color: #6f97d9; }")
            self.link_scroll_area.setWidget(self.link_widget)

            self.setLayout(outer_layout)

            self.initUI()

    def initUI(self):
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
    def submit_venues(self):
        self.result_display.clear()

        for i in reversed(range(self.link_layout.count())):
            widget = self.link_layout.itemAt(i).widget()
            if widget is not None:
                self.link_layout.removeWidget(widget)
                widget.deleteLater()
    
        locations = []
        if self.knight.isChecked():
            locations.append("Matthew Knight Arena")
        if self.hult.isChecked():
            locations.append("Hult Center")
        if self.mcdonald.isChecked():
            locations.append("McDonald Theatre")
        if self.cuthbert.isChecked():
            locations.append("Cuthbert Amphitheater")
    
        
        if len(locations) == 0:
            self.venue_error = Venue_Failure_Window()
            self.venue_error.show()

        else:
            result = database.search_by_venue(locations)
            index = 1
            for events in result:
                for event in events:
                    display_string = str(index)+": "+event.get("Artist")+" on "+event.get("Date")+" at "+event.get("Venue")
                    self.result_display.append(display_string)
                    link_text = event.get("Link")
                    artist_name = (event.get("Artist"))
                    if '&' in artist_name:
                        artist_name = artist_name.replace("&", "and")
                    button_text = str(index)+": "+artist_name
                    link_button = QPushButton(button_text)  # Create link button
                    link_button.setStyleSheet("QPushButton { color: #0e4282; text-decoration: underline; }")
                    link_button.clicked.connect(lambda _, link=link_text: QDesktopServices.openUrl(QUrl(link)))
                    self.link_layout.addWidget(link_button)
                    index = index + 1

    def unclick(self):
        self.knight.setChecked(False)
        self.hult.setChecked(False)
        self.mcdonald.setChecked(False)
        self.cuthbert.setChecked(False)
        
class Venue_Failure_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Error Message"
        self.left = 300
        self.top = 150
        self.width = 200
        self.height = 75
        self.setStyleSheet("background-color: #8eb3e6; color: black") 
        self.setWindowTitle("Color") 
        layout = QVBoxLayout()
        self.error_message = QLabel("No venue was selected.")
        layout.addWidget(self.error_message)
        self.setLayout(layout)
        self.initUI()

    def initUI(self):
        #resize window
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())