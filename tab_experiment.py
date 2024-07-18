from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget
from sub_tab_experiment_inputs import sub_Tab_Experiment_inputs
from sub_tab_experiment_graph import sub_Tab_Experiment_graph
from sub_tab_experiment_force import sub_Tab_Experiment_force

class Tab_Experiment(QWidget):
    def __init__(self, mainwindow):
        super().__init__()

        self.mainwindow = mainwindow

        self.tabs = QTabWidget()
        self.tab_ex_input = sub_Tab_Experiment_inputs()
        self.tab_ex_graph = sub_Tab_Experiment_graph(self.tab_ex_input, self)
        self.tab_ex_force = sub_Tab_Experiment_force(self.tab_ex_graph)

        self.tabs.addTab(self.tab_ex_input, "Werte")
        self.tabs.addTab(self.tab_ex_graph, "Überwachung")
        self.tabs.addTab(self.tab_ex_force, "Kraft-Diagramm")

        layout = QVBoxLayout(self)
        layout.addWidget(self.tabs)
        self.setLayout(layout)
