import os
import sys

from PIL import Image
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ResizeNinja(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resize Ninja")
        self.setGeometry(100, 100, 550, 500)
        self.setWindowIcon(QIcon(r"../Images/ResizeNinjaIconC.ico"))

        self.create_menu_bar()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.background_label = QLabel()
        self.layout.addWidget(self.background_label)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)
        self.load_image()

        self.choose_button = QPushButton("Choose Image")
        self.choose_button.clicked.connect(self.choose_image)
        self.layout.addWidget(self.choose_button)

        self.entry = QLineEdit()
        self.layout.addWidget(self.entry)

        self.choose_output_button = QPushButton("Save Folder")
        self.choose_output_button.clicked.connect(self.choose_output_destination)
        self.layout.addWidget(self.choose_output_button)

        self.output_entry = QLineEdit()
        self.layout.addWidget(self.output_entry)

        self.dimension_frame = QHBoxLayout()
        self.layout.addLayout(self.dimension_frame)

        self.dimension_label = QLabel("Choose Dimensions:")
        self.dimension_frame.addWidget(self.dimension_label)

        self.dimension_var = QComboBox()
        self.dimension_var.addItems(
            [
                "3000 x 3000 (Album Cover Art)",
                "1920 x 1080 (Full HD)",
                "1280 x 720 (HD)",
                "256 x 256 (Icon)",
                "16 x 16 (Favicon)",
                "Custom",
            ]
        )
        self.dimension_frame.addWidget(self.dimension_var)

        self.custom_dimension_frame = QHBoxLayout()
        self.layout.addLayout(self.custom_dimension_frame)

        self.custom_width_label = QLabel("Custom Width:")
        self.custom_dimension_frame.addWidget(self.custom_width_label)

        self.custom_width_entry = QLineEdit()
        self.custom_dimension_frame.addWidget(self.custom_width_entry)

        self.custom_height_label = QLabel("Custom Height:")
        self.custom_dimension_frame.addWidget(self.custom_height_label)

        self.custom_height_entry = QLineEdit()
        self.custom_dimension_frame.addWidget(self.custom_height_entry)

        self.format_frame = QHBoxLayout()
        self.layout.addLayout(self.format_frame)

        self.format_label = QLabel("Choose Format:")
        self.format_frame.addWidget(self.format_label)

        self.format_var = QComboBox()
        self.format_var.addItems(["png", "gif", "ico", "jpeg", "jpg"])
        self.format_frame.addWidget(self.format_var)

        self.resize_button = QPushButton("Resize Images")
        self.resize_button.clicked.connect(self.resize_multiple_images_with_progress)
        self.layout.addWidget(self.resize_button)

        self.progress_bar = QProgressBar()
        self.layout.addWidget(self.progress_bar)

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        how_to_use_action = QAction("How To Use", self)
        how_to_use_action.triggered.connect(self.how_to_use)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(how_to_use_action)
        help_menu.addAction(about_action)

    def how_to_use(self):
        instructions = (
            "1. Click 'Choose Image' to select one or more image files.\n"
            "2. Click 'Save Folder' to choose the output destination folder.\n"
            "3. Select the desired dimensions and format.\n"
            "4. Click 'Resize Images' to start the resizing process.\n"
            "5. View the progress in the console window.\n"
            "6. Resized images will be saved in the chosen output folder."
        )
        QMessageBox.information(self, "How To Use", instructions)

    def about(self):
        version_info = "Resize Ninja v1.4\nDeveloped by pudszTTIOT"
        QMessageBox.information(self, "About", version_info)

    def load_image(self):
        pixmap = QPixmap(r"../Images/ResizeNinjafolder1.png")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def choose_image(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Choose Image", "", "Image files (*.png *.jpg *.jpeg)"
        )
        if file_paths:
            self.entry.setText(";".join(file_paths))

    def choose_output_destination(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Save Folder")
        if folder_path:
            self.output_entry.setText(folder_path)

    def resize_multiple_images_with_progress(self):
        file_paths = self.entry.text().split(";")
        output_folder = self.output_entry.text()

        try:
            self.progress_bar.setValue(0)
            self.progress_bar.setMaximum(len(file_paths))
            for index, file_path in enumerate(file_paths):
                image = Image.open(file_path)

                selected_dimension = self.dimension_var.currentText()
                if selected_dimension == "Custom":
                    custom_width = self.custom_width_entry.text()
                    custom_height = self.custom_height_entry.text()

                    if not custom_width.isdigit() or not custom_height.isdigit():
                        raise ValueError("Custom width and height must be numeric.")

                    width = int(custom_width)
                    height = int(custom_height)
                else:
                    dimensions = {
                        "3000 x 3000 (Album Cover Art)": (3000, 3000),
                        "1920 x 1080 (Full HD)": (1920, 1080),
                        "1280 x 720 (HD)": (1280, 720),
                        "256 x 256 (Icon)": (256, 256),
                        "16 x 16 (Favicon)": (16, 16),
                    }
                    width, height = dimensions[selected_dimension]

                resized_image = image.resize((width, height))

                file_name = os.path.split(file_path)[-1]
                output_path = os.path.join(
                    output_folder,
                    f"{file_name}_resized.{self.format_var.currentText()}",
                )
                resized_image.save(output_path)

                self.progress_bar.setValue(index + 1)

            QMessageBox.information(
                self,
                "Images Resized",
                "All images have been successfully resized and saved.",
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


app = QApplication(sys.argv)
resize_ninja = ResizeNinja()
resize_ninja.show()
sys.exit(app.exec_())
