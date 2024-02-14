import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QCoreApplication
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Скачивание изображений")
        self.setGeometry(100, 100, 400, 250)

        self.button_file = QPushButton("Выбрать файл", self)
        self.button_file.setGeometry(50, 50, 150, 30)
        self.button_file.clicked.connect(self.open_file_dialog)

        self.button_url = QPushButton("Скачать через URL", self)
        self.button_url.setGeometry(210, 50, 150, 30)
        self.button_url.clicked.connect(self.download_images_from_url)

        self.url_lineedit = QLineEdit(self)
        self.url_lineedit.setGeometry(50, 100, 310, 30)

        self.progress_label = QLabel(self)
        self.progress_label.setGeometry(50, 150, 300, 100)
        self.progress_label.setAlignment(Qt.AlignTop)
        self.progress_label.setWordWrap(True)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Текстовые файлы (*.txt)", options=options)
        if file_name:
            self.download_images(file_name)

    def download_images_from_url(self):
        url = self.url_lineedit.text().strip()
        if url:
            self.download_images(url)

    def download_images(self, source):
        if os.path.isfile(source):
            with open(source, 'r') as file:
                urls = file.readlines()
        else:
            urls = [source]

        images_folder = 'images'
        os.makedirs(images_folder, exist_ok=True)

        for url in urls:
            url = url.strip()
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                img_tags = soup.find_all('img')

                folder_name = datetime.now().strftime("%d.%m.%Y-%H.%M.%S")
                folder_path = os.path.join(images_folder, folder_name)
                os.makedirs(folder_path)

                for i, img_tag in enumerate(img_tags, start=1):
                    img_url = img_tag.get('src')
                    if img_url:
                        if not urlparse(img_url).netloc:
                            img_url = urljoin(url, img_url)
                        img_name = f"{i}.jpg"
                        img_path = os.path.join(folder_path, img_name)
                        urlretrieve(img_url, img_path)
                        self.progress_label.setText(f'Изображение сохранено: {img_path}')
                        QCoreApplication.processEvents()

        # Завершаем работу приложения только после загрузки всех изображений
        self.progress_label.setText("Загрузка изображений завершена!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
