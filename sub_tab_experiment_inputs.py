from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QInputDialog, QMessageBox
import pandas as pd
class sub_Tab_Experiment_inputs(QWidget):
    def __init__(self):
        super().__init__()
        
        # variables
        self.max_cycle = 100000
        self.max_cycle_min = 1000
        self.max_cycle_max = 1000000
        self.cycle_between_res = 100
        self.cycle_between_res_min = 100
        self.cycle_between_res_max = 1000
        self.temp = 120
        self.temp_min = 20
        self.temp_max = 120
        
        # create Labels
        label_max_cycle = QLabel("Maximale Anzahl an Steckzyklen:")
        self.value_max_cycle = QLabel(str(self.max_cycle))
        label_cycle_between_res = QLabel("Steckzyklen zwischen Messungen:")
        self.value_cycle_between_res = QLabel(str(self.cycle_between_res))
        label_temp = QLabel("Temperatur:")
        self.value_Temp = QLabel(str(self.temp))

        # create Inputs
        self.change_max_cycle = QPushButton("Ändern",self)
        self.change_cycle_between_res = QPushButton("Ändern",self)
        self.change_Temp = QPushButton("Ändern",self)

        # add functions
        self.change_max_cycle.clicked.connect(self.change_value_max_cycle)
        self.change_cycle_between_res.clicked.connect(self.change_value_cycle_between_res)
        self.change_Temp.clicked.connect(self.change_value_temp)

        # create Layout
        label = QVBoxLayout()
        inputs_value = QVBoxLayout()
        inputs_change = QVBoxLayout()
        inputs = QHBoxLayout()
        layout = QVBoxLayout()

        # merge Layouts
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
        
        # set Layout
        self.setLayout(layout)
    
    # change value of max cycle, called when klicked on change_max_cycle
    def change_value_max_cycle(self):
        value_input, ok = QInputDialog.getInt(self,"Maximale Anzahl an Steckzyklen",f"Maximale Anzahl an Steckzyklen [{self.max_cycle_min} ; {self.max_cycle_max}]:",self.max_cycle,self.max_cycle_min,self.max_cycle_max)
        if ok and value_input > self.cycle_between_res:
            self.max_cycle = value_input
            self.value_max_cycle.setText(str(self.max_cycle))
        elif not ok:
            pass
        else:
            QMessageBox.warning(self, "Invalid Input", f"Die Zahl muss größer als {self.cycle_between_res} sein")
            
    # change value of how many cycles between resistance measuring, called when klicked on change_cycle_between_res
    def change_value_cycle_between_res(self):
        value_input, ok = QInputDialog.getInt(self,"Anzahl zwischen Widerstandsmessung",f"Anzahl an Steckzyklen zwischen den Widerstandsmessungen [{self.cycle_between_res_min} ; {self.cycle_between_res_max}]:",self.cycle_between_res,self.cycle_between_res_min,self.cycle_between_res_max)
        if ok and value_input < self.max_cycle:
            self.cycle_between_res = value_input
            self.value_cycle_between_res.setText(str(self.cycle_between_res))
        elif not ok:
            pass            
        else:
            QMessageBox.warning(self, "Invalid Input", f"Die Zahl muss kleiner als {self.max_cycle} sein")
    
    # change value of the theoretical Temperatur, called, when clicked on change_Temp
    def change_value_temp(self):
        value_input, ok = QInputDialog.getInt(self,"Temperatur",f"Betriebstemperatur in °C [{self.temp_min} ; {self.temp_max}]:",self.temp,self.temp_min,self.temp_max)
        if ok:
            self.temp = value_input
            self.value_Temp.setText(str(self.temp))