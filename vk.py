class VK:
    """В контакте"""
    url = 'https://api.vk.com/method/'

    def __init__(self, id_users, token):
        self.id_users = id_users
        self.token = token
        self.params = {
            'access_token': self.token,
            'v': '5.131',
        }

    def server_responses(self, response):
        """Ответы сервера"""
        import requests
        if isinstance(response, requests.Response):
            code = response.status_code
            codes = {
                200: 'Данные получены',
                301: 'Затребованный URI перемешен',
                302: 'Затребованный URI временно перемешен',
                400: 'В запросе обнаружена ошибка',
                401: 'Требуется авторизация',
                404: 'Документ по указанному URI не существует',
                410: 'Затребованный URI больше не существует',
                500: 'Ошибка сервера',
                503: 'Данная служба временно недоступна'
            }
        elif isinstance(response, dict):
            code = response['error']['error_code']
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
                200: 'Доступ к альбому запрещён.'
            }
        if code in codes:
            response_text = codes[code]
        else:
            response_text = f'Код ответа {code}'
        print(response_text)
        return response_text

    def users_photo(self, album_id='profile', method='photos.get', count=5):
        """получение списка фотографий пользователя"""
        import requests
        full_url = self.url + method
        params = {
            'owner_id': self.id_users,
            'album_id': album_id,
            'extended': '1',
            'count': count
        }
        params.update(self.params)
        print('Отправляем запрос для получения списка фотографий')
        res = requests.get(full_url, params=params)
        respon = self.server_responses(res)
        if respon != 'Данные получены':
            print('Программа прервана')
            return False
        elif 'error' in res.json():
            self.server_responses(res.json())
            print('Программа прервана')
            return False
        else:
            return res.json()

    def max_users_photo(self, album_id='profile'):
        """Определение фотографий максимального размера"""
        json_dict = self.users_photo(album_id=album_id)
        if not json_dict:
            return False
        else:
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

    def download_photos(self, album_id='profile'):
        """Скачивание и переименование фотографий"""
        import os
        import requests
        from pprint import pprint
        big_photos = self.max_users_photo(album_id=album_id)
        if not big_photos:
            return False
        else:
            directory = os.getcwd()
            name_folder = 'download_folder'
            path = os.path.join(directory, name_folder)
            if not os.path.exists(path):
                os.mkdir(path)
                print(f'Папка "{name_folder}" создана в текущей директории')
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

    def user_albums(self):
        """Получение списка альбомов пользователя"""
        import requests
        URL = 'https://api.vk.com/method/photos.getAlbums'
        params = {
            'owner_id': self.id_users,
        }
        params.update(self.params)
        print('Отправка запроса получения списка альбомов пользователя')
        server_res = requests.get(URL, params=params)
        respon = self.server_responses(server_res)
        if respon != 'Данные получены':
            print('Программа прервана')
            return False
        elif 'error' in server_res.json():
            self.server_responses(server_res.json())
            print('Программа прервана')
            return False
        else:
            server_res = server_res.json()
            if server_res['response']['count'] != 0:
                album_list = []
                for album in server_res['response']['items']:
                    if album['size'] != 0:
                        album_list += [[f"Название альбома: {album['title']}", f"Идентификатор альбома: {album['id']}",
                                       f"Количество фотографий в альбоме: {album['size']}"]]
                if len(album_list) == 0:
                    result = 'В доступных альбомах фотографии отсутствуют'
                    print(result)
                else:
                    result = album_list
            else:
                result = 'Доступные альбомы отсутствуют'
                print(result)
            return result

    def clear_download_folder(self, name_folder='download_folder'):
        """Очистка папки для загрузки файлов"""
        import os
        directory = os.getcwd()
        name_folder = name_folder
        path = os.path.join(directory, name_folder)
        if not os.path.exists(path):
            print(f'Папка "{name_folder}" отсутсвует в текущей директории')
        else:
            list_files = os.listdir(path)
            [os.remove(f'{path}/{photo}') for photo in list_files]
            print(f'Папка "{name_folder}" очищена от файлов')
