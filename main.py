import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTabWidget, QLabel, QFormLayout, QPushButton, QSpacerItem, QSizePolicy,QInputDialog,QMessageBox,QDialog,QDialogButtonBox,QProgressBar
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
import pyqtgraph as pg
import time
import random

class Thread_Test(QThread):
    finished = pyqtSignal()
    def __init__(self,Tab_Test):
        super().__init__()
        self.tab_Test = Tab_Test
        self.emergency = False
    def run(self):
        for i in range(1, 101):
            if not self.emergency:
                print(i)
                time.sleep(0.1)
                self.tab_Test.progress_bar.setValue(i)
            else:
                break
        self.finished.emit()

class Tab_Test(QWidget):
    def __init__(self):
        super().__init__()
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
        information.addLayout(resistance)
        information.addItem(spacer_item)
        information.addLayout(force)
        information.addStretch()
        
        layout.addLayout(emergency_layout)
        layout.addLayout(information)
        layout.addWidget(start_test)
        layout.addWidget(self.progress_bar)
        layout.addStretch()

        #thread handling
        self.thread_test = Thread_Test(self)
        self.thread_test.finished.connect(self.on_test_finished)
        
        self.setLayout(layout)
    def on_test_finished(self):
        print("Done")

    def set_emergency(self):
        self.thread_test.emergency = True
        QMessageBox.warning(self, "Emergency", "Der Notaus wurde gedrückt")
        
    def startTest(self):
        self.thread_test.emergency = False
        self.thread_test.start()

class Tab_Experiment(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tab_ex_input = sub_Tab_Experiment_inputs()
        self.tab_ex_graph = sub_Tab_Experiment_graph(self.tab_ex_input)

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
            

        
class ValueDialog(QDialog):
    def __init__(self, values):
        super().__init__()
        
        self.setWindowTitle('Werte anzeigen')
        
        layout = QVBoxLayout(self)
        text = QLabel("Das Experiment wird mit Folgenden Werten gestartet:")
        layout.addWidget(text)
        
        # Zeige die Werte als Labels im Dialog an
        for key, value in values.items():
            label = QLabel(f"{key}: {value}")
            layout.addWidget(label)
        
        # Dialog-Buttons (OK und Abbrechen)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)

class Thread_Experiment(QThread):
    finished_exp = pyqtSignal()
    update_graph = pyqtSignal()
    update_theo_cycle = pyqtSignal(int)
    update_Progress_bar = pyqtSignal(int)
    def __init__(self,tab_exp):
        super().__init__()
        self.tab_exp = tab_exp
        self.emergency = False
    def run(self):
        for i in range(1, self.tab_exp.inputs_widget.max_cycle+1):
            if not self.emergency:
                time.sleep(0.01)
                print(i)
                self.update_theo_cycle.emit(i)
                if i % self.tab_exp.inputs_widget.cycle_between_res == 0:
                    new_row = pd.DataFrame({"Messungsschritt": [i], "Widerstand": [random.randint(0, 1000)]})
                    self.tab_exp.dataframe = pd.concat([self.tab_exp.dataframe, new_row], ignore_index=True)
                    progressbar_value = int(i/self.tab_exp.inputs_widget.max_cycle*100)
                    print(progressbar_value)
                    self.update_Progress_bar.emit(progressbar_value)
                    self.update_graph.emit()
            else:
                break
        self.finished_exp.emit()

class sub_Tab_Experiment_graph(QWidget):
    def __init__(self, inputs_widget):
        super().__init__()
        self.inputs_widget = inputs_widget
        self.df_value = {"Messungsschritt": [], "Widerstand": []}
        self.dataframe = pd.DataFrame(self.df_value)
        
        #layouts
        layout_temp_humidity = QFormLayout()
        layout_cycle_layout = QFormLayout()
        layout_temp_cycle = QHBoxLayout()
        information = QHBoxLayout()
        pins = QVBoxLayout()
        resistance = QFormLayout()
        force = QFormLayout()
        emergency_layout = QHBoxLayout()
        layout = QVBoxLayout()
        
        #spaceritem
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
        
        self.theo_cycle_label = QLabel("Soll - Zyklus")
        self.theo_cycle_value = QLabel(str(0))
        layout_temp_humidity.addRow(self.theo_cycle_label,self.theo_cycle_value)
        
        # for item, item_value in self.information_cycle.items():
        #     text = QLabel(item)
        #     value = QLabel(str(item_value))
        #     layout_cycle_layout.addRow(text,value)

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

        start_experiment = QPushButton("Start Experiment")
        start_experiment.clicked.connect(self.values_experiment_start)
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

        self.draw_graph()

        # Progress Bar
        self.progress_bar = QProgressBar(self)

        information.addStretch()
        information.addLayout(pins)
        information.addLayout(resistance)
        information.addItem(spacer_item)
        information.addLayout(force)
        information.addStretch()

        layout_temp_cycle.addLayout(layout_temp_humidity)
        layout_temp_cycle.addStretch()
        layout_temp_cycle.addLayout(layout_cycle_layout)
        layout_temp_cycle.addStretch()
        layout_temp_cycle.addLayout(information)

        emergency_layout.addLayout(layout_temp_cycle)
        emergency_layout.addStretch()
        emergency_layout.addWidget(self.emergency_button)

        
        
        layout.addStretch()
        layout.addLayout(emergency_layout)
        layout.addWidget(start_experiment)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.graph)
        
        layout.addStretch()

        self.setLayout(layout)

        # Thread handling
        self.thread_exp = Thread_Experiment(self)
        self.thread_exp.finished.connect(self.on_exp_finished)
        self.thread_exp.update_graph.connect(self.draw_graph)
        self.thread_exp.update_theo_cycle.connect(self.update_theo_cycle_value)
        self.thread_exp.update_Progress_bar.connect(self.update_PB)
    def update_PB(self,value):
        self.progress_bar.setValue(value)

    def update_theo_cycle_value(self, value):
        self.theo_cycle_value.setText(str(value))

    def values_experiment_start(self):
        values = {
            "Maximale Anzahl an Stackzyklen": self.inputs_widget.max_cycle,
            "Anzahl an Steckzyklen zwischen Widerstandsmessung": self.inputs_widget.cycle_between_res,
            "Temperatur": self.inputs_widget.temp
        }
        
        # Dialog erstellen und ausführen
        dialog = ValueDialog(values)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.startExp()
        else:
            pass
    def draw_graph(self):
        if not hasattr(self, 'graph') or self.graph is None:
            self.graph = pg.plot()
            self.graph.setBackground('w')
        self.graph.clear()  
        pen = pg.mkPen(color='k')  # Schwarze Linienfarbe definieren
        self.graph.plot(x=self.dataframe["Messungsschritt"], y=self.dataframe["Widerstand"], pen=pen)

        # Stile der Achsen anpassen
        self.graph.getAxis('bottom').setPen('k')  # X-Achse in Schwarz
        self.graph.getAxis('left').setPen('k')    # Y-Achse in Schwarz
        self.graph.getAxis('bottom').setTextPen('k')  # X-Achsenbeschriftung in Schwarz
        self.graph.getAxis('left').setTextPen('k')    # Y-Achsenbeschriftung in Schwarz

        # Achsenbeschriftungen setzen
        self.graph.getAxis('bottom').setLabel(text='Messung', color='k')  # X-Achse
        self.graph.getAxis('left').setLabel(text='Widerstand', color='k')  # Y-Achse
    def on_exp_finished(self):
        print("Done")
        print(self.dataframe)

    def set_emergency(self):
        self.thread_exp.emergency = True
        QMessageBox.warning(self, "Emergency", "Der Notaus wurde gedrückt")
        
    def startExp(self):
        # Clear the existing dataframe and reset the plot
        self.dataframe = pd.DataFrame(self.df_value)        
        self.thread_exp.emergency = False
        self.thread_exp.start()


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
