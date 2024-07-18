import sys
import pandas as pd
import numpy as np
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.named_dataframes = {}

        # Grid layout to hold all the plot widgets
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.plots = {}

        # Button to add new random data
        self.add_data_button = QtWidgets.QPushButton('Add Random Data')
        self.add_data_button.clicked.connect(self.add_random_data)
        self.layout.addWidget(self.add_data_button, 0, 0, 1, 2)  # Span over two columns

        # Button to clear all plots
        self.clear_plots_button = QtWidgets.QPushButton('Clear Plots')
        self.clear_plots_button.clicked.connect(self.clear_plots)
        self.layout.addWidget(self.clear_plots_button, 0, 2, 1, 2)  # Span over two columns

        # Initial setup with random data
        self.add_random_data()

    def setup_plot(self, plot_widget, dataframe):
        plot_widget.setBackground('w')
        pen = pg.mkPen(color='k')

        # Plot the data
        plot_widget.plot(x=dataframe["Messungsschritt"], y=dataframe["Widerstand"], pen=pen)

        # Change style of axes
        plot_widget.getAxis('bottom').setPen('k')  # X-Achse in Schwarz
        plot_widget.getAxis('left').setPen('k')    # Y-Achse in Schwarz
        plot_widget.getAxis('bottom').setTextPen('k')  # X-Achsenbeschriftung in Schwarz
        plot_widget.getAxis('left').setTextPen('k')    # Y-Achsenbeschriftung in Schwarz

        # Set axis labels
        plot_widget.getAxis('bottom').setLabel(text='Messung', color='k')  # X-Achse
        plot_widget.getAxis('left').setLabel(text='Widerstand', color='k')  # Y-Achse

    def add_random_data(self):
        # Generate new random data for each plot
        for name in self.plots.keys():
            new_data = pd.DataFrame({
                "Messungsschritt": range(10),
                "Widerstand": np.random.randint(1, 10, size=10)  # Generate random integers for resistance
            })
            self.named_dataframes[name] = new_data

            # Clear the plot widget
            plot_widget = self.plots[name]
            plot_widget.clear()

            # Plot the updated data
            pen = pg.mkPen(color='k')
            plot_widget.plot(x=new_data["Messungsschritt"], y=new_data["Widerstand"], pen=pen)

            # Update axis labels (optional)
            plot_widget.getAxis('bottom').setLabel(text='Messung', color='k')  # X-Achse
            plot_widget.getAxis('left').setLabel(text='Widerstand', color='k')  # Y-Achse

    def clear_plots(self):
        # Clear all plots
        for name in list(self.plots.keys()):
            plot_widget = self.plots.pop(name)
            plot_widget.clear()
            plot_widget.deleteLater()

    def add_plot_widget(self, name):
        # Add a new plot widget with initial random data
        new_data = pd.DataFrame({
            "Messungsschritt": range(10),
            "Widerstand": np.random.randint(1, 10, size=10)  # Generate random integers for resistance
        })
        self.named_dataframes[name] = new_data

        plot_widget = pg.PlotWidget()
        self.setup_plot(plot_widget, new_data)
        self.plots[name] = plot_widget
        self.layout.addWidget(plot_widget, len(self.plots) // 2, len(self.plots) % 2 * 2, 1, 2)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
