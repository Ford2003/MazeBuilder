from PySide6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy,
                               QSlider, QHBoxLayout, QRadioButton, QButtonGroup)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QPoint
from maze import Maze


class MazeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maze Generator")
        # Vertical layout to hold everything inside
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # Use a QLabel for the maze image
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        label_size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.label.setSizePolicy(label_size_policy)
        self.label.setStyleSheet("background-color: lightblue")
        self.layout.addWidget(self.label, stretch=1)
        # QButton to generate the maze
        self.button = QPushButton("Generate Maze")
        self.layout.addWidget(self.button)
        self.button.clicked.connect(self.generate_and_show_maze)
        # A QHBoxLayout containing a QSlider to control the size of the maze and a QLabel to display the value.
        self.slider_layout = QHBoxLayout()
        # Create a QLabel which says "Size:"
        self.slider_label = QLabel("Size:")
        self.slider_layout.addWidget(self.slider_label)
        # Create a horizontal QSlider which goes from 3 to 100
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(5)
        self.slider.setTickInterval(1)
        self.slider.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.slider_layout.addWidget(self.slider)
        # Create a QLabel to display the value of the slider.
        self.slider_value_label = QLabel(str(self.slider.value()))
        self.slider_layout.addWidget(self.slider_value_label)
        # Connect the slider value to the label
        self.slider.valueChanged.connect(lambda value: self.slider_value_label.setText(str(value)))
        # Add the slider layout to the main layout
        self.layout.addLayout(self.slider_layout, stretch=0)
        # Now we create another QHBoxLayout to contain some radio buttons to select the generation method.
        self.method_layout = QHBoxLayout()
        # Add a label for the buttons.
        self.method_label = QLabel("Generation Method:")
        self.method_layout.addWidget(self.method_label)
        # Add the buttons.
        self.method1_radio = QRadioButton("Depth First 1")
        self.method1_radio.setChecked(True)
        self.method_layout.addWidget(self.method1_radio)
        self.method2_radio = QRadioButton("Depth First 2")
        self.method_layout.addWidget(self.method2_radio)
        # Use a button group to ensure only one button is selected at a time.
        self.method_group = QButtonGroup()
        self.method_group.addButton(self.method1_radio)
        self.method_group.addButton(self.method2_radio)
        # Add the layout to the main layout.
        self.layout.addLayout(self.method_layout, stretch=0)
        # Show the initial maze.
        self.generate_and_show_maze()
        # Display the widget.
        self.show()

    def generate_and_show_maze(self):
        # Create and generate our maze, the size given by the slider.
        maze = Maze(self.slider.value())
        # Get the method from the radio buttons.
        method = self._get_generation_method()
        maze.generate(method=method)
        data = maze.display()
        # We create a Monotone image and set the pixels from the data.
        image = QImage(len(data), len(data), QImage.Format_Mono)
        for i in range(len(data)):
            for j in range(len(data)):
                # QImage pixels are given by (column, row) so we need to swap i and j.
                # In a mono QImage, 0 = black and 1 = white, so we invert each pixel.
                image.setPixel(QPoint(j, i), not data[i][j])
        # Convert the image to a QPixmap and display it in the QLabel.
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap.scaled(402, 402, Qt.KeepAspectRatio))

    def _get_generation_method(self):
        selected = self.method_group.checkedButton()
        if selected:
            return selected.text().lower().replace(" ", "-")
        else:
            print('No method selected, using default.')
            return 'depth-first-1'
