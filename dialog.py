from PyQt6.QtWidgets import QDialog,QDialogButtonBox,QLabel,QVBoxLayout
class ValueDialog(QDialog):
    def __init__(self, values):
        super().__init__()
        
        # set Window title
        self.setWindowTitle('Werte anzeigen')
        
        # create layout
        layout = QVBoxLayout(self)
        
        # create Widgets and add them to the layout
        text = QLabel("Das Experiment wird mit Folgenden Werten gestartet:")
        layout.addWidget(text)
        
        # show the values as label
        for key, value in values.items():
            label = QLabel(f"{key}: {value}")
            layout.addWidget(label)
        
        # Dialog-Buttons (OK und Abbrechen)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addWidget(buttons)