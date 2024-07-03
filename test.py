import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)

class NumberInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        # Set the window title
        self.setWindowTitle("Number Input Dialog")

        # Create a QVBoxLayout instance
        layout = QVBoxLayout()

        # Create a QLabel instance
        self.label = QLabel("Please enter a number between 0 and 120:")
        
        # Add the QLabel to the layout
        layout.addWidget(self.label)

        # Create a QLineEdit instance
        self.line_edit = QLineEdit()
        
        # Add the QLineEdit to the layout
        layout.addWidget(self.line_edit)

        # Create a QPushButton instance
        self.button = QPushButton("OK")
        self.button.clicked.connect(self.validate_input)  # Connect the button to the validate_input method
        
        # Add the button to the layout
        layout.addWidget(self.button)

        # Set the layout for the dialog
        self.setLayout(layout)
    
    def validate_input(self):
        try:
            # Get the text from QLineEdit and convert it to an integer
            value = int(self.line_edit.text())
            
            # Check if the value is within the desired range
            if 0 <= value <= 120:
                QMessageBox.information(self, "Success", f"Valid number entered: {value}")
                self.accept()
            else:
                QMessageBox.warning(self, "Invalid Input", "Please enter a number between 0 and 120.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = NumberInputDialog()
    if dialog.exec() == QDialog.DialogCode.Accepted:
        print(f"Number entered: {dialog.line_edit.text()}")
    sys.exit(app.exec())
