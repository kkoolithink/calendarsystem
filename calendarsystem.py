import calendar
import datetime
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QComboBox, QLineEdit
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon

class Calendar(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Calendar')
        self.setFixedSize(self.size())

        self.today = datetime.date.today()
        

        self.UI()

    def UI(self):
        self.current_month = self.today.month
        self.current_year = self.today.year

        self.month = QLabel(f"{calendar.month_name[self.current_month]}, {self.current_year}")
        left_arrow = QPushButton("<")
        right_arrow = QPushButton(">")
        double_left_arrow = QPushButton("<<")
        double_right_arrow = QPushButton(">>")
        event_number = QLabel("Events: nil")
        home = QPushButton()
        settings = QPushButton()
        help = QPushButton()
        self.specific_month = QComboBox()
        self.specific_year = QLineEdit()
        specific_label = QLabel("Specific date:")

        hbox1 = QHBoxLayout()
        hbox1.addWidget(double_left_arrow)
        hbox1.addWidget(left_arrow)
        hbox1.addWidget(self.month)
        hbox1.addWidget(right_arrow)
        hbox1.addWidget(double_right_arrow)

        self.hbox2 = QHBoxLayout()
        self.bottom_button_setup(help, "questionmark.png")
        self.bottom_button_setup(home, "home.png")
        self.hbox2.addWidget(event_number)
        self.bottom_button_setup(settings, "settings.png")

        hbox3 = QHBoxLayout()
        hbox3.addWidget(specific_label)
        hbox3.addWidget(self.specific_month)
        hbox3.addWidget(self.specific_year)

        self.gbox = QGridLayout()
        self.fix_calendar()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(self.gbox)
        vbox.addLayout(self.hbox2)
        vbox.addLayout(hbox3)
        self.setLayout(vbox)

        self.month.setAlignment(Qt.AlignmentFlag.AlignCenter)
        event_number.setAlignment(Qt.AlignmentFlag.AlignCenter)
        specific_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.specific_year.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.specific_month.addItem("Month:")
        self.specific_month.addItems(calendar.month_name[1:])
        self.specific_year.setPlaceholderText("Year:")
        self.specific_month.setFixedSize(160, 50)
        self.specific_year.setFixedSize(100, 50)
        help.setFixedSize(40, 40)

        self.hbox2.setSpacing(20)
        self.hbox2.setContentsMargins(0, 20, 0, 0)

        left_arrow.clicked.connect(lambda: self.back_month(False))
        double_left_arrow.clicked.connect(lambda: self.back_month(True))
        right_arrow.clicked.connect(lambda: self.forward_month(False))
        double_right_arrow.clicked.connect(lambda: self.forward_month(True))

        self.specific_month.currentIndexChanged.connect(lambda: self.go_to_date(False))
        self.specific_year.editingFinished.connect(lambda: self.go_to_date(False))
        home.clicked.connect(lambda: self.go_to_date(True))

        self.setStyleSheet("""
            QWidget{
                font-weight: bold;
                font-family: Helvetica;
                font-size: 20px;
                padding: 10px;
            }
            QLabel#Weekday{
                font-size: 15px;
                padding: 9px;
            }
        """)
        
    def fix_calendar(self):
        self.month.setText(f"{calendar.month_name[self.current_month]}, {self.current_year}")

        for i in reversed(range(self.gbox.count())):
            widget = self.gbox.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
            
            self.gbox.takeAt(i)

        for col in range(7):
            weekday = calendar.day_abbr[col]
            weekday_label = QLabel(weekday)
            weekday_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            weekday_label.setObjectName("Weekday")
            self.gbox.addWidget(weekday_label, 0, col)

            if col < 6:
                spacer = QSpacerItem(10, 20)
                self.gbox.addItem(spacer, 0, col + 1)

        start_weekday = calendar.weekday(self.current_year, self.current_month, 1)
        cal = calendar.Calendar(firstweekday=start_weekday)
        monthdays = cal.monthdayscalendar(self.current_year, self.current_month)
        row = 1
        col = start_weekday

        for week in monthdays:
            for day in week:
                if day:
                    button = QPushButton(str(day))
                    button.setObjectName("DayButton")
                    button.setFixedSize(50, 50)
                    self.gbox.addWidget(button, row, col)

                col += 1

                if col >= 7:
                    col = 0
                    row += 1
    
    def back_month(self, back_year):
        if back_year:
            self.current_year -= 1
        else:
            if self.current_month == 1:
                self.current_month = 12
                self.current_year -= 1
            else: 
                self.current_month -= 1

        self.fix_calendar()

    def forward_month(self, forward_year):
        if forward_year:
            self.current_year += 1
        else:
            if self.current_month == 12:
                self.current_month = 1
                self.current_year += 1
            else: 
                self.current_month += 1
        
        self.fix_calendar()

    def bottom_button_setup(self, button, direc):
        button.setFixedSize(40, 40)
        button.setIcon(QIcon(direc))
        button.setIconSize(QSize(30, 30))
        self.hbox2.addWidget(button)

    def go_to_date(self, home):
        try:
            if home:
                self.current_month = self.today.month
                self.current_year = self.today.year
            else:
                self.current_month = list(calendar.month_name).index(self.specific_month.currentText())
                self.current_year = int(self.specific_year.text())
                self.fix_calendar()

            self.fix_calendar()
        except ValueError: return
            
    def help_button(self):
        help_window = Help()
        help_window.show()

class Help(QWidget):
    def __init__(self):
        super().__init__()

        year_left_button = QLabel("<< - Back one year")
        month_left_button = QLabel("< - Back one month")
        year_right_button = QLabel(">> - Forward one year")
        month_right_button = QLabel("> - Forward one month")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calendar_app = Calendar()
    calendar_app.show()
    sys.exit(app.exec())