from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, \
    QLabel, QFileDialog
from PySide2.QtGui import QPainter, QPen, QBrush, QColor
from PySide2.QtCore import Qt
from PIL import Image, ExifTags
import sys, os


class PhotoViewer(QWidget):
    def __init__(self):
        super(PhotoViewer, self).__init__()
        self.setWindowTitle("Képnézegető")
        self.resize(1000, 600)

        # objektum változók
        self.current_dir = ""
        self.file_list = []

        # Main layout with "Open folder" button
        main_layout = QVBoxLayout(self)

        self.open_button = QPushButton("Open foler...")
        main_layout.addWidget(self.open_button)

        # hLayout for file list / details / image
        h_layout = QHBoxLayout()
        main_layout.addLayout(h_layout)

        # vLayout for file list / details
        file_list_layout = QVBoxLayout()
        h_layout.addLayout(file_list_layout)

        # File list view
        self.file_list_view = QListWidget()
        self.file_list_view.setMaximumWidth(200)
        file_list_layout.addWidget(self.file_list_view)

        # image details view
        self.photo_details = QTextEdit()
        self.photo_details.setReadOnly(True)
        self.photo_details.setMaximumWidth(200)
        self.photo_details.setMaximumHeight(80)
        file_list_layout.addWidget(self.photo_details)

        # image view
        self.image_viewer = ImageViewer()
        h_layout.addWidget(self.image_viewer)

        # Connect signals
        self.open_button.clicked.connect(self.open_folder_action)
        self.file_list_view.currentItemChanged.connect(self.photo_changed_action)
        self.file_list_view.itemDoubleClicked.connect(self.open_file_action)

    def getExif(self, filePath):
        exif_string = ""

        exif_string += f"File: {filePath}\n"

        img = Image.open(filePath)
        exif = img._getexif()
        if exif:
            for k, v in exif.items():
                if k in ExifTags.TAGS:
                    exifLabel = ExifTags.TAGS[k]

                    if exifLabel == "DateTimeOriginal":
                        exif_string += f"Date: {v}\n"

                    if exifLabel == "Model":
                        exif_string += f"Camera: {v}\n"

                    if exifLabel == "ISOSpeedRatings":
                        exif_string += f"ISO: {v}\n"

        return exif_string

    def open_file_action(self, item):
        os.startfile(os.path.join(self.current_dir, item.text()))

    def photo_changed_action(self, item):
        # print(item.text())
        current_photo = os.path.join(self.current_dir, item.text())
        exif_data = self.getExif(current_photo)
        self.photo_details.setText(exif_data)

        # self.image_viewer.set_pixmap(current_photo)
        self.image_viewer.set_pixmap(current_photo)

    def refresh_file_list_view(self):
        self.file_list_view.clear()
        for f in self.file_list:
            self.file_list_view.addItem(f)

    def collect_files(self):
        self.file_list = [i for i in os.listdir(self.current_dir) if i.lower().endswith(".jpg")]

    def open_folder_action(self):
        directory = QFileDialog.getExistingDirectory(self, "Könyvtár választás", "C:\\Users\\jcigi\\Pictures\\gdc")

        if len(directory):
            self.current_dir = directory.replace("/", "\\")
            self.open_button.setText(self.current_dir)
            self.collect_files()
            self.refresh_file_list_view()


class ImageViewer(QWidget):
    def __init__(self):
        super(ImageViewer, self).__init__()

        self.painter = QPainter()
        self.my_pen = QPen(QColor("red"))
        self.my_pen.setWidth(5)
        self.my_brush = QBrush(QColor("blue"))


    def set_pixmap(self, image_path):
        print(image_path)

    def paintEvent(self, event):
        self.painter.begin(self)
        self.draw()
        self.painter.end()

    def draw(self):
        rect = self.rect()

        self.painter.setPen(self.my_pen)
        self.painter.setBrush(self.my_brush)
        self.painter.drawRect(rect)


app = QApplication(sys.argv)
win = PhotoViewer()
win.show()
app.exec_()
