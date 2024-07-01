import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Resistance Values')

        # Create central widget and set layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create a QFormLayout
        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)

        # Example resistances and their values (replace with actual data)
        resistances = {
            "R1": "10 Ω",
            "R2": "20 Ω",
            "R3": "30 Ω",
            "R4": "40 Ω"
        }

        # Add labels and values to the form layout
        for resistance, value in resistances.items():
            label = QLabel(resistance)
            value_label = QLabel(value)
            value_label.setStyleSheet("background-color: lightgray;")  # Example styling for read-only values
            self.form_layout.addRow(label, value_label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
