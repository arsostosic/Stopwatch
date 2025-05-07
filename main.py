# Python PyQt5 Stopwatch
import sys
from PyQt5.QtWidgets import (QApplication,
                             QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import QTime, QTimer, Qt
from PyQt5.QtGui import QIcon


class Stopwatch(QWidget):
    def __init__(self):
        super().__init__()
        self.time = QTime(0,0,0,0) # Design of our stopwatch
        self.time_label = QLabel("00:00:00:00", self)
        self.start_button = QPushButton("start", self)
        self.stop_button = QPushButton("stop", self)
        self.reset_button = QPushButton("reset", self)
        self.timer = QTimer(self)
        self.setWindowIcon(QIcon("chronometer.png"))
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Stopwatch")

        vbox = QVBoxLayout()

        vbox.addWidget(self.time_label)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.stop_button)
        vbox.addWidget(self.reset_button)

        self.setLayout(vbox)

        self.time_label.setAlignment(Qt.AlignCenter)

        hbox = QHBoxLayout()

        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        hbox.addWidget(self.reset_button)

        vbox.addLayout(hbox)

        # difference between setLayout and addLayout
        # first is used to just get the first initial layout
        # the second one is used to add new layouts in an organized way to existing window
        # without colliding with other layouts
        # so we added hbox layout to our existing vbox layout

        # STYLESHEET

        self.setStyleSheet(""" 
        QPushButton, QLabel{
            padding: 20px;
            font-weight: bold;
            font-family: calibri;
        }
        QPushButton{
        font-size: 50px;
        }
        QLabel{
        font-size: 120px;
        background-color: hsl(46, 79%, 51%);
        border-radius: 15px;
        }
        """)
        # CONNECTING SIGNALS WITH A SLOTS FOR EACH BUTTON
        # No parentheses () when connecting a signal to a slot
        # because we pass the function reference, not call it immediately.
        # Adding () would execute the function right away and pass its return value to connect,
        # which is not desired.

        self.start_button.clicked.connect(self.start_stopwatch)
        self.stop_button.clicked.connect(self.stop_stopwatch)
        self.reset_button.clicked.connect(self.reset_stopwatch)

        # 10ms interval: Ensures smooth and precise updates for the stopwatch.
        # timeout signal: Triggers actions (e.g., updating the display) every time the interval elapses.
        # Prevents freezing: Keeps the stopwatch responsive and real-time by refreshing regularly.

        self.timer.timeout.connect(self.update_display) # To update our display after given time, ensure that stopwatch display doesn't freeze


    def start_stopwatch(self):
        self.timer.start(10) # Our timer will give timeout signal every 10 milliseconds so that way we can manage what to do with a stopwatch after that (i.eg. update screen for current time)

    def stop_stopwatch(self):
        self.timer.stop() # stops the time from creating a timeout signal

    def reset_stopwatch(self):
        self.timer.stop()
        self.time = QTime(0,0,0,0)
        self.time_label.setText(self.format_time(self.time))

    def format_time(self, time):
        hours = time.hour()
        minutes = time.minute()
        seconds = time.second()
        milliseconds = time.msec() // 10 # for showing only 2 digits instead of 3 dividing by 10 // integer division in this case no decimals
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"
    # 02: Ensures the number is displayed with at least 2 digits, padding with leading zeros if necessary.
    # If the value has fewer than 2 digits, it will add zeros to the left.
    # If the value already has 2 or more digits, it will display the number as-is.

    def update_display(self):
        self.time = self.time.addMSecs(10) # We are updating the time with +10ms
        self.time_label.setText(self.format_time(self.time))

def main():
    app = QApplication(sys.argv)
    window = Stopwatch()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()