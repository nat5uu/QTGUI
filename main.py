import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QLabel, QFormLayout, QPushButton, QSpacerItem, QSizePolicy,QInputDialog,QMessageBox

class Tab_Test(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        information = QHBoxLayout()
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

        information.addStretch()
        information.addLayout(pins)
        information.addLayout(resistance)
        information.addItem(spacer_item)
        information.addLayout(force)
        information.addStretch()
        
        layout.addStretch()
        layout.addLayout(information)
        layout.addWidget(start_test)
        layout.addStretch()
        
        self.setLayout(layout)

class Tab_Experiment(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tab_ex_input = sub_Tab_Experiment_inputs()
        self.tab_ex_graph = sub_Tab_Experiment_graph()

        self.tabs.addTab(self.tab_ex_input, "Werte")
        self.tabs.addTab(self.tab_ex_graph, "Überwachung")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)

class sub_Tab_Experiment_inputs(QWidget):
    def __init__(self):
        super().__init__()
        #variables
        self.max_cycle = 100000
        self.max_cycle_min = 1000
        self.max_cycle_max = 1000000
        self.cycle_between_res = 100
        self.cycle_between_res_min = 100
        self.cycle_between_res_max = 1000
        self.temp = 120
        self.temp_min = 20
        self.temp_max = 120
        #create Labels
        label_max_cycle = QLabel("Maximale Anzahl an Steckzyklen:")
        self.value_max_cycle = QLabel(str(self.max_cycle))
        label_cycle_between_res = QLabel("Steckzyklen zwischen Messungen:")
        self.value_cycle_between_res = QLabel(str(self.cycle_between_res))
        label_temp = QLabel("Temperatur:")
        self.value_Temp = QLabel(str(self.temp))

        #create Inputs
        self.change_max_cycle = QPushButton("Ändern",self)
        self.change_cycle_between_res = QPushButton("Ändern",self)
        self.change_Temp = QPushButton("Ändern",self)

        #add functions
        self.change_max_cycle.clicked.connect(self.change_value_max_cycle)
        self.change_cycle_between_res.clicked.connect(self.change_value_cycle_between_res)
        self.change_Temp.clicked.connect(self.change_value_temp)

        #create Layout
        label = QVBoxLayout()
        inputs_value = QVBoxLayout()
        inputs_change = QVBoxLayout()
        inputs = QHBoxLayout()
        layout = QVBoxLayout()

        #merge Layouts
        label.addWidget(label_max_cycle)
        label.addWidget(label_cycle_between_res)
        label.addWidget(label_temp)

        inputs_value.addWidget(self.value_max_cycle)
        inputs_value.addWidget(self.value_cycle_between_res)
        inputs_value.addWidget(self.value_Temp)

        inputs_change.addWidget(self.change_max_cycle)
        inputs_change.addWidget(self.change_cycle_between_res)
        inputs_change.addWidget(self.change_Temp)
        
        inputs.addStretch()
        inputs.addLayout(label)
        inputs.addLayout(inputs_value)
        inputs.addLayout(inputs_change)
        inputs.addStretch()

        layout.addLayout(inputs)
        self.setLayout(layout)
    
    def change_value_max_cycle(self):
        value_input, ok = QInputDialog.getInt(self,"Maximale Anzahl an Steckzyklen",f"Maximale Anzahl an Steckzyklen [{self.max_cycle_min} ; {self.max_cycle_max}]:",self.max_cycle,self.max_cycle_min,self.max_cycle_max)
        if ok and value_input > self.cycle_between_res:
            self.max_cycle = value_input
            self.value_max_cycle.setText(str(self.max_cycle))
        elif not ok:
            pass
        else:
            QMessageBox.warning(self, "Invalid Input", f"Die Zahl muss größer als {self.cycle_between_res} sein")
    def change_value_cycle_between_res(self):
        value_input, ok = QInputDialog.getInt(self,"Anzahl zwischen Widerstandsmessung",f"Anzahl an Steckzyklen zwischen den Widerstandsmessungen [{self.cycle_between_res_min} ; {self.cycle_between_res_max}]:",self.cycle_between_res,self.cycle_between_res_min,self.cycle_between_res_max)
        if ok and value_input < self.max_cycle:
            self.cycle_between_res = value_input
            self.value_cycle_between_res.setText(str(self.cycle_between_res))
        elif not ok:
            pass            
        else:
            QMessageBox.warning(self, "Invalid Input", f"Die Zahl muss kleiner als {self.max_cycle} sein")
    def change_value_temp(self):
        value_input, ok = QInputDialog.getInt(self,"Temperatur",f"Betriebstemperatur in °C [{self.temp_min} ; {self.temp_max}]:",self.temp,self.temp_min,self.temp_max)
        if ok:
            self.temp = value_input
            self.value_Temp.setText(str(self.temp))


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
