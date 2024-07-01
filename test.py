import sys
import random
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QTabWidget
from PyQt6.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window title
        self.setWindowTitle("Temperature Sensor with Emergency Button")

        # Set the window size
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QTabWidget
        self.tabs = QTabWidget(self)
        self.layout.addWidget(self.tabs)

        # Create the first tab
        self.tab1 = QWidget()
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tab1_layout = QVBoxLayout(self.tab1)

        # Create a label to display temperature in the first tab
        self.temp_label = QLabel("Temperature: --°C", self.tab1)
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab1_layout.addWidget(self.temp_label)

        # Create a button to update temperature in the first tab
        self.button = QPushButton("Update Temperature", self.tab1)
        self.button.clicked.connect(self.update_temperature)
        self.tab1_layout.addWidget(self.button)

        # Create an emergency button in the first tab
        self.emergency_button = QPushButton("Emergency", self.tab1)
        self.emergency_button.setObjectName("emergencyButton")
        self.emergency_button.setFixedSize(100, 100)  # Set a fixed size to make it a circle
        self.emergency_button.clicked.connect(self.handle_emergency)
        self.tab1_layout.addWidget(self.emergency_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Create the second tab
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab2, "Tab 2")
        self.tab2_layout = QVBoxLayout(self.tab2)
        self.tab2_label = QLabel("Welcome to Tab 2", self.tab2)
        self.tab2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tab2_layout.addWidget(self.tab2_label)

        # Disable the second tab initially
        self.tabs.setTabEnabled(1, False)

        # Set a timer to update temperature periodically (e.g., every 5 seconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_temperature)
        self.timer.start(5000)  # Update every 5000 milliseconds (5 seconds)

        # Load the external stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        with open("style.css", "r") as file:
            self.setStyleSheet(file.read())

    def update_temperature(self):
        # Simulate reading from a temperature sensor
        temperature = self.read_sensor()
        self.temp_label.setText(f"Temperature: {temperature:.2f}°C")

        # Enable or disable the second tab based on the temperature
        if temperature > 25.0:
            self.tabs.setTabEnabled(1, True)
        else:
            self.tabs.setTabEnabled(1, False)

    def read_sensor(self):
        # Replace this method with actual sensor reading code
        # For now, we simulate it with a random temperature value
        return random.uniform(20.0, 30.0)  # Simulate a temperature between 20°C and 30°C

    def handle_emergency(self):
        # Handle the emergency situation here
        # For now, we just print a message to the console
        print("Emergency button pressed! Taking appropriate actions.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
