import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import QThread, pyqtSignal

class TestThread(QThread):
    finished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.emergency = False
        
    def run(self):
        for i in range(0, 100):
            if not self.emergency:
                print(i)
                time.sleep(0.1)
            else:
                print("Error")
                break
        self.finished.emit()

class Tab_Test(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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

        start_test = QPushButton("Start Test")
        start_test.clicked.connect(self.startTest)
        self.emergency_button = QPushButton("Emergency")
        self.emergency_button.clicked.connect(self.set_emergency)
        self.emergency_button.setFixedSize(200, 200)  # Set a fixed size to make it a circle
        self.emergency_button.setStyleSheet("""
            QPushButton {
                background-color: blue;
                color: white;
                font-weight: bold;
                border-radius: 100px;  /* Half of the button's height/width */
            }
            QPushButton:pressed {
                background-color: darkred;
            }
        """)
        emergency_layout.addStretch()
        emergency_layout.addWidget(self.emergency_button)

        information.addStretch()
        information.addLayout(pins)
        information.addItem(spacer_item)
        information.addLayout(resistance)
        information.addItem(spacer_item)
        information.addLayout(force)
        information.addStretch()
        
        layout.addLayout(emergency_layout)
        layout.addLayout(information)
        layout.addWidget(start_test)
        layout.addStretch()
        
        self.setLayout(layout)
        
        self.thread = TestThread()
        self.thread.finished.connect(self.onTestFinished)

    def set_emergency(self):
        self.emergency = True
        self.thread.emergency = True

    def startTest(self):
        self.thread.start()

    def onTestFinished(self):
        print("Test abgeschlossen.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Tab_Test()
    window.show()
    sys.exit(app.exec())
