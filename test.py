import sys
import pandas as pd
from PyQt6 import QtWidgets
import pyqtgraph as pg

class MainWindow(QtWidgets.QWidget):
    def __init__(self, named_dataframes):
        super().__init__()

        # Grid layout to hold all the plot widgets
        layout = QtWidgets.QGridLayout()

        self.plots = {}

        for i, (name, dataframe) in enumerate(named_dataframes.items()):
            plot_widget = pg.PlotWidget()
            self.setup_plot(plot_widget, dataframe)
            self.plots[name] = plot_widget
            # Add the plot widget to the layout in a 2x3 grid
            layout.addWidget(plot_widget, i // 3, i % 3)

        self.setLayout(layout)

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

def main(named_dataframes):
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(named_dataframes)
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    # Example named dataframes with different values
    named_dataframes = {
        'Plot 1': pd.DataFrame({
            "Messungsschritt": range(10),
            "Widerstand": [j * 1 for j in range(10)]
        }),
        'Plot 2': pd.DataFrame({
            "Messungsschritt": range(10),
            "Widerstand": [j * 2 for j in range(10)]
        }),
        'Plot 3': pd.DataFrame({
            "Messungsschritt": range(10),
            "Widerstand": [j * 3 for j in range(10)]
        }),
        'Plot 4': pd.DataFrame({
            "Messungsschritt": range(10),
            "Widerstand": [j * 4 for j in range(10)]
        }),
        'Plot 5': pd.DataFrame({
            "Messungsschritt": range(10),
            "Widerstand": [j * 5 for j in range(10)]
        }),
        'Plot 6': pd.DataFrame({
            "Messungsschritt": range(10),
            "Widerstand": [j * 6 for j in range(10)]
        }),
    }
    
    main(named_dataframes)
