import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout,QHBoxLayout, QWidget, QTabWidget, QLabel,QFormLayout,QPushButton,QSpacerItem

class Tab_Test(QWidget):
    def __init__(self):
        super().__init__()
        #create Layout
        layout = QVBoxLayout()
        information = QHBoxLayout()
        pins = QVBoxLayout()
        resistance = QFormLayout()
        force = QFormLayout()  
        # Add spacer item
        spacer_item = QSpacerItem(0, 40)
        
        
        #starting values
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

        #fill Layouts
        for i in range(1,4):
            pin_id = QLabel(f"Pin_{i}")
            pins.addWidget(pin_id)
            pins.addItem(spacer_item)

        for pin_id,pin_value in information_resistance.items():
            pin = QLabel(pin_id)
            value = QLabel(str(pin_value))
            value.setStyleSheet("background-color: lightgray;")
            resistance.addRow(pin,value)
            resistance.addItem(spacer_item)
        for pin_id,pin_value in information_force.items():
            pin = QLabel(pin_id)
            value = QLabel(str(pin_value))
            value.setStyleSheet("background-color: lightgray;")
            force.addRow(pin,value)
            force.addItem(spacer_item)
        start_ex = QPushButton()

        #merge Layouts
        information.addStretch()
        information.addLayout(pins)
        information.addLayout(resistance)
        information.addItem(spacer_item)
        information.addLayout(force)
        information.addStretch()
        
        layout.addStretch()
        layout.addLayout(information)
        layout.addWidget(start_ex)
        layout.addStretch()
        
        self.setLayout(layout)

class Tab_Experiment(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QTabWidget
        self.tabs = QTabWidget()

        # Create sub-tabs (you need to add the self.tabs to the layout of this widget)
        self.tab_ex_input = sub_Tab_Experiment_inputs()
        self.tab_ex_graph = sub_Tab_Experiment_graph()

        self.tabs.addTab(self.tab_ex_input, "Werte")
        self.tabs.addTab(self.tab_ex_graph, "Überwachung")

        # Set layout for this widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

class sub_Tab_Experiment_inputs(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Inputs Tab Content")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class sub_Tab_Experiment_graph(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Graph Tab Content")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_size = 0.7

        self.setWindowTitle("Main Window")
        self.center_window()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.tab_test = Tab_Test()
        self.tab_experiment = Tab_Experiment()

        self.tabs.addTab(self.tab_test, "Test")
        self.tabs.addTab(self.tab_experiment, "Experiment")

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_width = int(screen_geometry.width() * self.window_size)
        window_height = int(screen_geometry.height() * self.window_size)
        x = (screen_geometry.width() - window_width) // 2
        y = (screen_geometry.height() - window_height) // 2
        self.setGeometry(x, y, window_width, window_height)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
