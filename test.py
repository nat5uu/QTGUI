import sys
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageResizerWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()

        # Load the image
        self.pixmap = QPixmap(image_path)

        # Create a QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create a layout and add the QLabel to it
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)

    def resizeEvent(self, event):
        # Resize the image when the window is resized
        self.resize_image()
        super().resizeEvent(event)

    def resize_image(self):
        # Get the current size of the widget
        size = self.image_label.size()
        if not size.isEmpty():
            # Resize the pixmap to fit the QLabel size while maintaining aspect ratio
            scaled_pixmap = self.pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Path to the image file
    image_path = "./Bilder/pin.png"

    main_window = ImageResizerWidget(image_path)
    main_window.show()

    sys.exit(app.exec())
