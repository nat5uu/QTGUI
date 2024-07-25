import serial
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout,QFormLayout,QSpacerItem,QSizePolicy,QProgressBar,QDialog
from PyQt6.QtCore import QThread, pyqtSignal
from dialog import ValueDialog
import random
import pandas as pd
import pyqtgraph as pg
import re
import time

# Thread class for the experiment execution
class Thread_Experiment(QThread):
    
    # create Signals to communicate with main thread
    finished_exp = pyqtSignal()
    update_graph = pyqtSignal()
    update_theo_cycle = pyqtSignal(int)
    update_Progress_bar = pyqtSignal(int)
    get_temp_and_hum_signal = pyqtSignal()

    
    def __init__(self,tab_exp):
        super().__init__()
        self.tab_exp = tab_exp
        self.emergency = False
        
    def run(self):
        # create new row for pandas Dataframe and append it via concat
        new_row = pd.DataFrame({"Messungsschritt": [0], "Widerstand": [random.randint(0, 1000)]})
        self.tab_exp.dataframe = pd.concat([self.tab_exp.dataframe, new_row], ignore_index=True)
        for i in range(1, self.tab_exp.inputs_widget.max_cycle+1):
            if not self.emergency:
                time.sleep(1)
                print(i)
                self.update_theo_cycle.emit(i)
                self.get_temp_and_hum_signal.emit()

                
                # measure if the current cycle is  n * cycle_between_res
                if i % self.tab_exp.inputs_widget.cycle_between_res == 0:
                    
                    # create new row for pandas Dataframe and append it via concat
                    new_row = pd.DataFrame({"Messungsschritt": [i], "Widerstand": [random.randint(0, 1000)]})
                    self.tab_exp.dataframe = pd.concat([self.tab_exp.dataframe, new_row], ignore_index=True)
                    
                    # calculate the value for the Prograssbar
                    progressbar_value = int(i/self.tab_exp.inputs_widget.max_cycle*100)
                    print(progressbar_value)
                    self.update_Progress_bar.emit(progressbar_value)
                    self.update_graph.emit()
                elif i == 1000:
                    # create new row for pandas Dataframe and append it via concat
                    new_row = pd.DataFrame({"Messungsschritt": [i], "Widerstand": [random.randint(0, 1000)]})
                    self.tab_exp.dataframe = pd.concat([self.tab_exp.dataframe, new_row], ignore_index=True)
                    
                    # calculate the value for the Prograssbar
                    progressbar_value = int(100)
                    print(progressbar_value)
                    self.update_Progress_bar.emit(progressbar_value)
                    self.update_graph.emit()
                    
            else:
                break
        if not self.emergency:
            self.finished_exp.emit()


class sub_Tab_Experiment_graph(QWidget):
    def __init__(self, inputs_widget,tab_exp,):
        super().__init__()
        
        # set variables
        self.inputs_widget = inputs_widget
        
        self.tab_exp = tab_exp
        self.ser = None
        self.df_value = {"Messungsschritt": [], "Widerstand": []}
        self.dataframe = pd.DataFrame(self.df_value)
        
        # regular expressions to search fpr humidity and temp
        self.humidity_pattern = re.compile(r"Relative Humidity : (\d+\.\d+) %RH")
        self.temperature_pattern = re.compile(r"Temperature in Celsius : (\d+\.\d+) C")
        
               
        # layouts
        layout_temp_humidity = QFormLayout()
        layout_cycle_layout = QFormLayout()
        layout_temp_cycle = QHBoxLayout()
        information = QHBoxLayout()
        pins = QVBoxLayout()
        resistance = QFormLayout()
        force = QFormLayout()
        emergency_layout = QHBoxLayout()
        layout = QVBoxLayout()
        
        # spaceritem
        spacer_item = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        
        
        information_resistance = {
            "Widerstand1 [µΩ]:": 0,
            "Widerstand2 [µΩ]:": 0,
            "Widerstand3 [µΩ]:": 0, 
        }

        
        #set Widgets
        self.theo_cycle_label = QLabel("Soll - Zyklus:")
        self.theo_cycle_value = QLabel(str(0))
        self.exp_cycle_label = QLabel("Ist - Zyklus:")
        self.exp_cycle_value = QLabel(str(0))
        self.theo_temp_label = QLabel("Soll -Temperatur:")
        self.theo_temp_value = QLabel(str(0))
        self.exp_temp_label = QLabel("Ist - Temperatur:")
        self.exp_temp_value = QLabel(str(0))
        self.exp_humidity_label = QLabel("Ist - Luftfeuchtigkeit:")
        self.exp_humidity_value = QLabel(str(0))
        layout_cycle_layout.addRow(self.theo_cycle_label,self.theo_cycle_value)
        layout_cycle_layout.addRow(self.exp_cycle_label,self.exp_cycle_value)
        layout_temp_humidity.addRow(self.theo_temp_label,self.theo_temp_value)
        layout_temp_humidity.addRow(self.exp_temp_label,self.exp_temp_value)
        layout_temp_humidity.addRow(self.exp_humidity_label,self.exp_humidity_value)
        

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

        start_experiment = QPushButton("Start Experiment")
        
        self.emergency_button = QPushButton("Not-Aus")
        self.emergency_button.setFixedSize(200, 200)  # Set a fixed size to make it a circle
        self.emergency_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                font-weight: bold;
                border-radius: 100px;  /* Half of the button's height/width */
            }
            QPushButton:pressed {
                background-color: darkred;
            }
        """)
        
        # create Graph
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
        
        # button clicks handling
        start_experiment.clicked.connect(self.values_experiment_start)
        self.emergency_button.clicked.connect(self.set_emergency)

        # Thread handling
        self.thread_exp = Thread_Experiment(self)
        self.thread_exp.finished_exp.connect(self.on_exp_finished)
        self.thread_exp.update_graph.connect(self.draw_graph)
        self.thread_exp.update_theo_cycle.connect(self.update_theo_cycle_value)
        self.thread_exp.update_Progress_bar.connect(self.update_PB)
        # self.thread_exp.get_temp_and_hum_signal.connect(self.get_temp_and_humidity)           Serial Port wieder rein
        
    # update Progressbar
    def update_PB(self,value):
        self.progress_bar.setValue(value)
        
    # # get value of temp and humidity from serial port       Serial Port wieder rein
    # def get_temp_and_humidity(self):
        
    #     # read line of data from serial port -> convert it into a string -> Removing Trailing Whitespace
    #     self.line = self.ser.readline().decode('utf-8').rstrip()
        
    #     # set value of theoretical temp
    #     self.theo_temp_value.setText(str(self.inputs_widget.temp))
        
    #     #set humidity and temperature
    #     if self.line:
    #         self.humidity_match = self.humidity_pattern.search(self.line)
    #         self.temperature_match = self.temperature_pattern.search(self.line)
    #         if self.humidity_match:
    #             humidity_value = self.humidity_match.group(1)
    #             self.exp_humidity_value.setText(str(humidity_value))
    #         if self.temperature_match:
    #             temperature_value = self.temperature_match.group(1)
    #             self.exp_temp_value.setText(str(temperature_value))
                
    def update_theo_cycle_value(self, value):
        self.theo_cycle_value.setText(str(value))

    def values_experiment_start(self):
        values = {
            "Maximale Anzahl an Stackzyklen": self.inputs_widget.max_cycle,
            "Anzahl an Steckzyklen zwischen Widerstandsmessung": self.inputs_widget.cycle_between_res,
            "Temperatur": self.inputs_widget.temp
        }
        
        # create dialog and execute it
        dialog = ValueDialog(values)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.startExp()
        else:
            pass
    
    # create graph
    def draw_graph(self):
        # if plot doesnt exist create it
        if not hasattr(self, 'graph') or self.graph is None:
            self.graph = pg.plot()
            self.graph.setBackground('w')
        # clear graph
        self.graph.clear()  
        
        # set pen colour to black
        pen = pg.mkPen(color='k')
        
        # draw graph
        self.graph.plot(x=self.dataframe["Messungsschritt"], y=self.dataframe["Widerstand"], pen=pen)

        self.graph.setTitle("Widerstand")

        # change style of axes
        self.graph.getAxis('bottom').setPen('k')  # X-Achse in Schwarz
        self.graph.getAxis('left').setPen('k')    # Y-Achse in Schwarz
        self.graph.getAxis('bottom').setTextPen('k')  # X-Achsenbeschriftung in Schwarz
        self.graph.getAxis('left').setTextPen('k')    # Y-Achsenbeschriftung in Schwarz

        # set Text
        self.graph.getAxis('bottom').setLabel(text='Messung', color='k')  # X-Achse
        self.graph.getAxis('left').setLabel(text='Widerstand', color='k')  # Y-Achse
        
    def on_exp_finished(self):
        print("Done")
        print(self.dataframe)
        QMessageBox.information(self, "Done", "Erfolgreich abgeschlossen")

    def set_emergency(self):
        self.thread_exp.emergency = True
        QMessageBox.warning(self, "Emergency", "Der Notaus wurde gedrückt")
        
    def startExp(self):
        # disable Tabs and buttons
        self.inputs_widget.change_cycle_between_res.setEnabled(False)
        self.inputs_widget.change_max_cycle.setEnabled(False)
        self.inputs_widget.change_Temp.setEnabled(False)
        self.tab_exp.mainwindow.tabs.setTabEnabled(0, False)
        
        # connect to arduino via port 9600 (can change on different usb - input)           Serial Port wieder rein
        # if self.ser is None or not self.ser.is_open:
        #     try:
        #         self.ser = serial.Serial('COM8', 9600, timeout=1)
        #         time.sleep(2)
        #         print("connected")
        #     except Exception as e:
        #         QMessageBox.critical(self, "Error", f"Could not open serial port: {e}")
        #         return
        
        # Clear the existing dataframe and reset the plot
        self.dataframe = pd.DataFrame(self.df_value)        
        self.thread_exp.emergency = False
        self.thread_exp.start()