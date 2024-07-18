from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

class sub_Tab_Experiment_force(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel("Force Tab")
        layout.addWidget(label)

        self.setLayout(layout)