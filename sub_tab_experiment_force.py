from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton,QGridLayout,QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import pandas as pd
import pyqtgraph as pg
import random
import numpy as np


class sub_Tab_Experiment_force(QWidget):
    def __init__(self,tab_ex_graph):
        super().__init__()
        self.tab_ex_graph = tab_ex_graph
        self.tab_ex_graph.thread_exp.update_theo_cycle.connect(self.update_graph)

        self.pins = {}
        for i in range(1,7):
            self.pins[i] = QLabel(f"Pin_{i}")

        self.dataframes = {
                'Plot_1': pd.DataFrame({
                    "Messungsschritt": [],
                    "Kraft": []
                }),
                'Plot_2': pd.DataFrame({
                    "Messungsschritt": [],
                    "Kraft": []
                }),
                'Plot_3': pd.DataFrame({
                    "Messungsschritt": [],
                    "Kraft": []
                }),
                'Plot_4': pd.DataFrame({
                    "Messungsschritt": [],
                    "Kraft": []
                }),
                'Plot_5': pd.DataFrame({
                    "Messungsschritt": [],
                    "Kraft": []
                }),
                'Plot_6': pd.DataFrame({
                    "Messungsschritt": [],
                    "Kraft": []
                }),
            }
        self.plots = {}

        layout = QVBoxLayout()
        buttons = QHBoxLayout()
        pins_1_3 = QVBoxLayout()
        pins_4_6 = QVBoxLayout()
        diagramms = QGridLayout()

        pin_image = QLabel()
        pixmap = QPixmap("./Bilder/pin.png")
        scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        pin_image.setPixmap(scaled_pixmap)


        self.emergency_button = QPushButton("Not-Aus")
        self.emergency_button.clicked.connect(self.set_emergency)
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
        for i in range(1,4):
            pins_1_3.addWidget(self.pins[i])
        for i in range(4,7):
            pins_4_6.addWidget(self.pins[i])
        buttons.addStretch()
        buttons.addLayout(pins_1_3)
        buttons.addWidget(pin_image)
        buttons.addLayout(pins_4_6)
        buttons.addStretch()
        buttons.addWidget(self.emergency_button)

        for i, (name, df) in enumerate(self.dataframes.items()):
            plot_widget = pg.PlotWidget()
            self.setup_plot(plot_widget, df)
            self.plots[name] = plot_widget
            # Add the plot widget to the layout in a 2x3 grid
            diagramms.addWidget(plot_widget, i // 3, i % 3)

        layout.addLayout(buttons)
        layout.addLayout(diagramms)

        self.setLayout(layout)

    def setup_plot(self, plot_widget, df):
        plot_widget.setBackground('w')
        pen = pg.mkPen(color='k')

        # Plot the data
        plot_widget.plot(x=df["Messungsschritt"], y=df["Kraft"], pen=pen)

        # Change style of axes
        plot_widget.getAxis('bottom').setPen('k')  # X-Achse in Schwarz
        plot_widget.getAxis('left').setPen('k')    # Y-Achse in Schwarz
        plot_widget.getAxis('bottom').setTextPen('k')  # X-Achsenbeschriftung in Schwarz
        plot_widget.getAxis('left').setTextPen('k')    # Y-Achsenbeschriftung in Schwarz

        # Set axis labels
        plot_widget.getAxis('bottom').setLabel(text='Messung', color='k')  # X-Achse
        plot_widget.getAxis('left').setLabel(text='Kraft', color='k')  # Y-Achse
    
    def set_emergency(self):
        self.tab_ex_graph.thread_exp.emergency = True
        QMessageBox.warning(self, "Emergency", "Der Notaus wurde gedrückt")
    
    def update_graph(self,i):
        # actually a serial connection, now dummy
        self.update_values(i)
        print(f"{i=}")
        for name, plot_widget in self.plots.items():
            plot_widget.clear()
            df = self.dataframes[name]
            pen = pg.mkPen(color='k')
            plot_widget.plot(x=df["Messungsschritt"], y=df["Kraft"], pen=pen)

    def update_values(self,i):
        for name,df in self.dataframes.items():
            new_row = pd.DataFrame({"Messungsschritt": [i], "Kraft": [np.sin(i)]})
            self.dataframes[name] = pd.concat([df, new_row], ignore_index=True)
            