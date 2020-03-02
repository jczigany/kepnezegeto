from PySide2.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QTextEdit, QLabel

import sys


class PhotoViewer(QWidget):
    def __init__(self):
        super(PhotoViewer, self).__init__()
        self.setWindowTitle("Képnézegető")
        self.resize(1000, 600)

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
        self.image_viewer = QLabel("Itt lesz a kép")
        h_layout.addWidget(self.image_viewer)


app = QApplication(sys.argv)
win = PhotoViewer()
win.show()
app.exec_()
