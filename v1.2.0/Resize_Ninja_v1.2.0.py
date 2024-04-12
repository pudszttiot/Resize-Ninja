import os
import sys

from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QPixmap
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
        self.setGeometry(600, 150, 450, 500)
        self.setWindowIcon(QIcon(r"../Images/ResizeNinjaIconC.ico"))

        # Load custom font files
        font_id = QFontDatabase.addApplicationFont(r"../Fonts/mouser.ttf")
        QFontDatabase.applicationFontFamilies(font_id)[0]

        font_id = QFontDatabase.addApplicationFont(r"../Fonts/doergon(2).ttf")
        font_family_2 = QFontDatabase.applicationFontFamilies(font_id)[0]

        font_id = QFontDatabase.addApplicationFont(r"../Fonts/znikomitsc.otf")
        font_family_3 = QFontDatabase.applicationFontFamilies(font_id)[0]

        font_id = QFontDatabase.addApplicationFont(r"../Fonts/bellerose(2).ttf")
        font_family_4 = QFontDatabase.applicationFontFamilies(font_id)[0]

        # Set background color using style sheet
        self.setStyleSheet("background-color: #f0f0f0;")  # Light gray background color

        self.create_menu_bar()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Set a white background for the main widget
        self.central_widget.setStyleSheet("background-color: #0465b0;")

        self.background_label = QLabel()
        self.layout.addWidget(self.background_label)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)
        self.load_image()

        self.choose_button = QPushButton("Choose Image")
        self.choose_button.clicked.connect(self.choose_image)
        self.choose_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border: 1px solid gray;"
        )
        self.choose_button.setFont(QFont(font_family_2, 14))  # Set font style and size
        self.layout.addWidget(self.choose_button)

        self.entry = QLineEdit()
        self.entry.setFont(QFont("Arial", 10))  # Set font style and size
        self.entry.setStyleSheet("color: white;")  # Set font color
        self.layout.addWidget(self.entry)

        self.choose_output_button = QPushButton("Save Folder")
        self.choose_output_button.clicked.connect(self.choose_output_destination)
        self.choose_output_button.setStyleSheet(
            "background-color: #4CAF50; color: white; border: 1px solid gray;"
        )
        self.choose_output_button.setFont(
            QFont(font_family_2, 14)
        )  # Set font style and size
        self.layout.addWidget(self.choose_output_button)

        self.output_entry = QLineEdit()
        self.output_entry.setFont(QFont("Arial", 10))  # Set font style and size
        self.output_entry.setStyleSheet("color: white;")  # Set font color
        self.layout.addWidget(self.output_entry)

        self.dimension_frame = QHBoxLayout()
        self.layout.addLayout(self.dimension_frame)

        self.dimension_label = QLabel("Choose Dimensions:")
        self.dimension_label.setStyleSheet("color: white;")
        self.dimension_label.setFont(
            QFont(font_family_3, 10)
        )  # Set font style, size, and weight
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
        self.dimension_var.setStyleSheet(
            "background-color: white; color: black; border: 1px solid gray;"
        )
        self.dimension_var.setFont(
            QFont(font_family_3, 9, QFont.Bold)
        )  # Set font style and size
        self.dimension_var.setFixedWidth(305)  # Set the width of the combo box
        self.dimension_frame.addWidget(self.dimension_var)

        self.custom_dimension_frame = QHBoxLayout()
        self.layout.addLayout(self.custom_dimension_frame)

        self.custom_width_label = QLabel("Custom Width:")
        self.custom_width_label.setStyleSheet("color: white;")
        self.custom_width_label.setFont(
            QFont(font_family_3, 10)
        )  # Set font style and size
        self.custom_dimension_frame.addWidget(self.custom_width_label)

        self.custom_width_entry = QLineEdit()
        self.custom_width_entry.setStyleSheet(
            "background-color: white; color: black; border: 1px solid gray;"
        )
        self.custom_width_entry.setFont(QFont("Arial", 10))  # Set font style and size
        self.custom_dimension_frame.addWidget(self.custom_width_entry)

        self.custom_height_label = QLabel("Custom Height:")
        self.custom_height_label.setStyleSheet("color: white;")
        self.custom_height_label.setFont(
            QFont(font_family_3, 10)
        )  # Set font style and size
        self.custom_dimension_frame.addWidget(self.custom_height_label)

        self.custom_height_entry = QLineEdit()
        self.custom_height_entry.setStyleSheet(
            "background-color: white; color: black; border: 1px solid gray;"
        )
        self.custom_height_entry.setFont(QFont("Arial", 10))  # Set font style and size
        self.custom_dimension_frame.addWidget(self.custom_height_entry)

        self.format_frame = QHBoxLayout()
        self.layout.addLayout(self.format_frame)

        self.format_label = QLabel("Choose Format:")
        self.format_label.setStyleSheet("color: white;")
        self.format_label.setFont(
            QFont(font_family_3, 10)
        )  # Set font style, size, and weight
        self.format_frame.addWidget(self.format_label)

        self.format_var = QComboBox()
        self.format_var.addItems(["png", "gif", "ico", "jpeg", "jpg"])
        self.format_var.setStyleSheet(
            "background-color: white; color: black; border: 1px solid gray;"
        )
        self.format_var.setFont(
            QFont(font_family_4, 9, QFont.Bold)
        )  # Set font style and size
        self.format_frame.addWidget(self.format_var)

        self.resize_button = QPushButton("Resize Images")
        self.resize_button.clicked.connect(self.confirm_resize)
        self.resize_button.setStyleSheet(
            "background-color: #f44336; color: white; border: 1px solid gray;"
        )
        self.resize_button.setFont(QFont(font_family_2, 12))  # Set font style and size
        self.layout.addWidget(self.resize_button)

        # Create the progress bar
        self.progress_bar = QProgressBar()

        # Set the style sheet to enhance the appearance of the progress bar
        self.progress_bar.setStyleSheet(
            "QProgressBar::chunk { background-color: #39ff14; }"
            + "QProgressBar { border: 2px solid #39ff14; border-radius: 5px; text-align: center; }"
            + "QProgressBar::chunk:disabled { background-color: #bbb; }"
            + "QProgressBar::chunk:disabled:alternate { background-color: #ddd; }"
            + "QProgressBar { color: black; }"
        )

        # Wrap the progress bar inside a QWidget and add spacing to the left
        self.progress_bar_container = QWidget()
        self.progress_bar_layout = QVBoxLayout(self.progress_bar_container)
        self.progress_bar_layout.setContentsMargins(
            30, 0, 30, 0
        )  # Add spacing to the left
        self.progress_bar_layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.progress_bar_container)

    def create_menu_bar(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        help_menu = menubar.addMenu("Help")
        how_to_use_action = QAction("How To Use...", self)
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

        # How to Use Resize Ninja:

    # Step 1: Select an Image
    #    - Click on the "Choose Image" button.
    #    - A file dialog will open.
    #    - Select one or more image files you want to resize.
    #    - Click "Open" or "Choose" in the file dialog.

    # Step 2: Choose Output Folder
    #    - Click on the "Save Folder" button.
    #    - Another dialog will appear.
    #    - Choose the folder where you want to save the resized images.
    #    - Click "Select Folder" or "Save" in the dialog.

    # Step 3: Select Dimensions and Format
    #    - Choose the desired dimensions from the dropdown menu.
    #    - If you select "Custom", enter the custom width and height in the provided fields.
    #    - Select the output format from the format dropdown menu.

    # Step 4: Resize Images
    #    - Once you've chosen your settings, click on the "Resize Images" button.
    #    - A confirmation dialog will pop up.
    #    - Click "Yes" to proceed with the resizing or "No" to cancel.

    # Step 5: Monitor Progress
    #    - You can monitor the progress of the resizing operation in the console window.
    #    - The progress bar at the bottom of the GUI will also show the progress visually.

    # Step 6: View Resized Images
    #    - After the resizing process is complete, resized images will be saved in the chosen output folder.
    #    - You can navigate to the output folder to view the resized images.

    def about(self):
        version_info = "Resize Ninja v1.2\nDeveloped by pudszTTIOT"
        QMessageBox.information(self, "About", version_info)

    def load_image(self):
        pixmap = QPixmap(r"../Images/ResizeNinjafolder1.png")
        scaled_pixmap = pixmap.scaled(
            300, 400, Qt.KeepAspectRatio
        )  # Adjust dimensions as needed
        self.image_label.setPixmap(scaled_pixmap)
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

    def confirm_resize(self):
        confirmation = QMessageBox.question(
            self,
            "Confirmation",
            "Are you sure you want to resize the images?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirmation == QMessageBox.Yes:
            self.resize_images()
        else:
            QMessageBox.information(self, "Confirmation", "Resize operation canceled.")

    def resize_images(self):
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
