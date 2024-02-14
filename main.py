import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog
from PyQt5.QtCore import QCoreApplication
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.request import urlretrieve
from datetime import datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Скачивание изображений")
        self.setGeometry(100, 100, 300, 200)

        self.button = QPushButton("Выбрать файл", self)
        self.button.setGeometry(50, 50, 200, 50)
        self.button.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Выбрать файл", "", "Текстовые файлы (*.txt)", options=options)
        if file_name:
            self.download_images(file_name)

    def download_images(self, file_name):
        with open(file_name, 'r') as file:
            urls = file.readlines()

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

                img_count = 1  # Счетчик изображений

                for img_tag in img_tags:
                    img_url = img_tag.get('src')
                    if img_url:
                        if not urlparse(img_url).netloc:
                            img_url = urljoin(url, img_url)
                        img_ext = os.path.splitext(img_url)[1]  # Получаем расширение изображения
                        img_name = f"{img_count}{img_ext}"  # Формируем имя файла с порядковым номером
                        img_path = os.path.join(folder_path, img_name)
                        urlretrieve(img_url, img_path)
                        print(f'Изображение сохранено: {img_path}')
                        img_count += 1  # Увеличиваем счетчик изображений

        # Завершаем работу приложения только после загрузки всех изображений
        QCoreApplication.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
