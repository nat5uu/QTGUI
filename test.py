import sys
from PyQt6.QtWidgets import QApplication, QWidget, QFormLayout, QSpinBox, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Input Example')

        # Create a form layout
        layout = QFormLayout()

        # Create a label to display the value
        self.label = QLabel(self)

        # Create a QSpinBox
        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(0, 120)
        self.spin_box.setValue(0)

        # Connect the spin box value change to a function
        self.spin_box.valueChanged.connect(self.on_value_change)

        # Add widgets to the layout
        layout.addRow('Select a value between 0 and 120:', self.spin_box)
        layout.addRow('Selected value:', self.label)

        # Set the layout to the main window
        self.setLayout(layout)

    def on_value_change(self, value):
        self.label.setText(f'{value}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
