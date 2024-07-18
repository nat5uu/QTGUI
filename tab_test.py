from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QProgressBar, QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import time

# Thread class to handle background test execution
class Thread_Test(QThread):
    finished = pyqtSignal()
    update_progress_bar_test = pyqtSignal(int)

    def __init__(self, Tab_Test):
        super().__init__()
        self.tab_Test = Tab_Test
        self.emergency = False

    def run(self):
        for i in range(0, 101, 10):
            if not self.emergency:
                print(i)
                time.sleep(0.1)
                self.update_progress_bar_test.emit(i)
            else:
                break
        if i == 100:
            self.finished.emit()

# GUI class for the Test tab
class Tab_Test(QWidget):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow
        self.emergency = False

        layout = QVBoxLayout()
        information = QHBoxLayout()
        emergency_layout = QHBoxLayout()
        pins = QVBoxLayout()
        resistance = QFormLayout()
        force = QFormLayout()

        spacer_item = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        information_resistance = {
            "Widerstand1 [µΩ]:": 0,
            "Widerstand2 [µΩ]:": 0,
            "Widerstand3 [µΩ]:": 0,
        }
        information_force = {
            "Kraft1 [N]:": 0,
            "Kraft2 [N]:": 0,
            "Kraft3 [N]:": 0,
        }

        for i in range(1, 4):
            pin_id = QLabel(f"Pin_{i}")
            pins.addWidget(pin_id)
            pins.addItem(spacer_item)

        for pin_id, pin_value in information_resistance.items():
            pin = QLabel(pin_id)
            value = QLabel(str(pin_value))
            value.setStyleSheet("background-color: lightgray;")
            resistance.addRow(pin, value)
            resistance.addItem(spacer_item)

        for pin_id, pin_value in information_force.items():
            pin = QLabel(pin_id)
            value = QLabel(str(pin_value))
            value.setStyleSheet("background-color: lightgray;")
            force.addRow(pin, value)
            force.addItem(spacer_item)

        self.progress_bar = QProgressBar(self)
        start_test = QPushButton("Start Test")
        self.emergency_button = QPushButton("Emergency")
        self.emergency_button.setFixedSize(200, 200)
        self.emergency_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                border-radius: 100px;
            }
            QPushButton:pressed {
                background-color: darkred;
            }
        """)

        emergency_layout.addStretch()
        emergency_layout.addWidget(self.emergency_button)

        information.addStretch()
        information.addLayout(pins)
        information.addLayout(resistance)
        information.addItem(spacer_item)
        information.addLayout(force)
        information.addStretch()

        layout.addLayout(emergency_layout)
        layout.addLayout(information)
        layout.addWidget(start_test)
        layout.addWidget(self.progress_bar)
        layout.addStretch()

        self.thread_test = Thread_Test(self)
        self.thread_test.finished.connect(self.on_test_finished)
        self.thread_test.update_progress_bar_test.connect(self.update_test_progressbar)

        start_test.clicked.connect(self.startTest)
        self.emergency_button.clicked.connect(self.set_emergency)

        self.setLayout(layout)

    def update_test_progressbar(self, value):
        self.progress_bar.setValue(value)

    def on_test_finished(self):
        print("Done")
        self.mainwindow.tabs.setTabEnabled(1, True)
        QMessageBox.information(self, "Done", "Erfolgreich abgeschlossen")

    def set_emergency(self):
        self.thread_test.emergency = True
        QMessageBox.warning(self, "Emergency", "Der Notaus wurde gedrückt")

    def startTest(self):
        self.thread_test.emergency = False
        self.thread_test.start()
