import os
import requests


class Yan_disk:
    url = 'https://cloud-api.yandex.net/v1/'

    def __init__(self, token, folder='Фотографии'):
        self.token = token
        self.folder = folder

    def get_headers(self):
        """Прописываем заголовки"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'}

    def server_responses(self, response):
        """Ответы сервера"""
        code = response.status_code
        codes = {
            200: 'Данные получены',
            201: 'Объект создан на Яндекс диске',
            401: 'Авторизация не удалась',
            403: 'Недостаточно свободного места на вашем Яндекс диске',
            404: 'Не удалоссь найти запрошенный ресурс',
            409: 'Объект уже существует на Яндекс диске',
            423: 'Ресурс заблокирован',
            503: 'Ошибка сервера',
            507: 'Ошибка сервера'
        }
        if code in codes:
            response_text = codes[code]
        else:
            response_text = f'Код ответа {code}'
        print(response_text)
        return response_text

    def creating_folder(self):
        """Создание папки на Яндекс диске"""
        folder_creation_method = 'disk/resources'
        headers = self.get_headers()
        params = {'path': self.folder}
        requests_url = self.url+folder_creation_method
        print('Отправка запроса на создание новой папки')
        response_creation = requests.put(requests_url, headers=headers, params=params)
        self.server_responses(response_creation)
        return response_creation.json()

    def getting_download_address(self, file_name):
        """Получение ссылки для записи на Яндекс диск"""
        upload_method = 'disk/resources/upload'
        upload_url = self.url + upload_method
        headers = self.get_headers()
        params = {'path': f'{self.folder}/{file_name}',
                  'overwrite': 'true'}
        print(f'Отправка запроса на получение ссылки для загрузки файла {file_name}')
        response_url = requests.get(upload_url, headers=headers, params=params)
        self.server_responses(response_url)
        return response_url.json().get('href')

    def uploading_files(self):
        """Загрузка файлов на Яндекс диск"""
        if os.path.join('download_folder'):
            my_list_files = os.listdir('download_folder')
            if len(my_list_files) == 0:
                print('Отсутствуют файлы для загрузки')
            else:
                for file_name in my_list_files:
                    file_name_path = os.path.join('download_folder', file_name)
                    href = self.getting_download_address(file_name=file_name)
                    if href is None:
                        print(f'Ошибка загрузки, проверьте наличие папки "{self.folder}" на Яндекс диске')
                        break
                    with open(file_name_path, 'rb') as f:
                        print(f'Загрузка файла {file_name}')
                        response_uploading = requests.put(href, files={'file': f})
                        self.server_responses(response_uploading)
        else:
            print('Отсутствует исходная папка')
