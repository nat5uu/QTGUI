import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget
from tab_test import Tab_Test
from tab_experiment import Tab_Experiment

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # set Window size and center window
        self.window_size = 0.7
        self.setWindowTitle("Main Window")
        self.center_window()

        # create Widgets
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.tab_test = Tab_Test(self)
        self.tab_experiment = Tab_Experiment(self)

        self.tabs.addTab(self.tab_test, "Test")
        self.tabs.addTab(self.tab_experiment, "Experiment")
        self.tabs.setTabEnabled(1, True) ##########################################

    #override close Event so the Serial port closes correctly
    def closeEvent(self, event):
        try:
            if hasattr(self.tab_experiment.tab_ex_graph, 'ser') and self.tab_experiment.tab_ex_graph.ser.is_open:
                self.tab_experiment.tab_ex_graph.ser.close()
                print("Serial connection closed")
        except Exception as e:
            print(f"Error closing serial connection: {e}")

        event.accept()

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
