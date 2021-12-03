import os
import requests
from pprint import pprint


class VK:
    url = 'https://api.vk.com/method/'

    def __init__(self, id_users):
        self.id_users = id_users
        self.params = {
            'access_token': '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            'v': '5.131',
        }

    def server_responses(self, response):
        """Ответы сервера"""
        code = response.status_code
        codes = {
            1: 'Ошибка сервера',
            5: 'Авторизация пользователя не удалась',
            7: 'Нет прав для выполнения этого действия',
            10: 'Ошибка сервера',
            15: 'Доступ запрещен',
            17: 'Требуется валидация пользователя',
            24: 'Требуется подтверждение со стороны пользователя',
            30: 'Профиль является приватным',
            37: 'Пользователь заблокирован',
            113: 'Неверный идентификатор пользователя',
            200: 'Данные получены'
        }
        if code in codes:
            response_text = codes[code]
        else:
            response_text = f'Код ответа {code}'
        print(response_text)
        return response_text

    def users_photo(self, method='photos.get', count=5):
        """получение списка фотографий пользователя"""
        full_url = self.url + method
        params = {
            'owner_id': self.id_users,
            'album_id': 'profile',
            'extended': '1',
            'count': count
        }
        params.update(self.params)
        print('Отправляем запрос для получения списка фотографий')
        res = requests.get(full_url, params=params)
        self.server_responses(res)
        return res.json()

    def max_users_photo(self):
        """Определение фотографий максимального размера"""
        json_dict = self.users_photo()
        big_photos = []
        for group in json_dict['response']['items']:
            date = group['date']
            likes = group['likes']['count']
            number = 0
            for size in group['sizes']:
                size_photo = int(size['height']) * int(size['width'])
                if size_photo > number:
                    temp_list = []
                    temp_list += [{'size_photo': size_photo, 'date': date, 'likes': likes, 'url': size['url'],
                                   'type': size['type']}]
            big_photos += temp_list
        return big_photos

    def download_photos(self):
        """Скачивание и переименование фотографий"""
        big_photos = self.max_users_photo()
        directory = os.getcwd()
        name_folder = 'download_folder'
        path = os.path.join(directory, name_folder)
        if not os.path.exists(path):
            os.mkdir(path)
            print(f'Папка "{name_folder}" создана в текущей директории')
        else:
            list_files = os.listdir(path)
            [os.remove(f'{path}/{photo}') for photo in list_files]
        list_likes = []
        list_downloaded_photos = []
        for photo_parameters in big_photos:
            if photo_parameters['likes'] in list_likes:
                new_name_photo = f"{photo_parameters['likes']}_{photo_parameters['date']}.jpg"
                list_likes.append(photo_parameters['likes'])
            else:
                new_name_photo = f"{photo_parameters['likes']}.jpg"
                list_likes.append(photo_parameters['likes'])
            url = photo_parameters['url']
            print(f'Отправка запроса на скачивание фотографии "{new_name_photo}"')
            r = requests.get(url)
            self.server_responses(r)
            path_to_photo = f'{path}/{new_name_photo}'
            with open(path_to_photo, 'wb') as file:
                file.write(r.content)
            print(f'Фотография "{new_name_photo}" загружена в папку "{path}"')
            list_downloaded_photos += [{'file_name': new_name_photo, 'size': photo_parameters['type']}]
        print('Список скаченных фотографий:')
        pprint(list_downloaded_photos)
        return list_downloaded_photos
