class Classmates:
    """Одноклассники"""
    url = 'https://api.ok.ru/fb.do'

    def __init__(self, fid, count=5, secret_key='',
                 application_key='',
                 access_token=''):
        self.fid = fid
        self.count = count
        self.secret_key = secret_key
        self.application_key = application_key
        self.access_token = access_token

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
            code = response['error_code']
            codes = {
                1: 'Неизвестная ошибка',
                2: 'Сервис временно недоступен',
                7: 'Запрошенное действие временно заблокировано для текущего пользователя',
                11: 'Ошибка: Достигнут предел вызовов метода',
                101: 'Ошибка: Параметр application_key не указан или указан неверно',
                103: 'Ошибка: Неверный ключ сессии',
                104: 'Ошибка: Неверная подпись',
                105: 'Ошибка: Неверная повторная подпись',
                110: 'Ошибка: Неверный идентификатор пользователя',
                200: 'Приложение не может выполнить операцию. Получения доступа к операции без авторизации'
                     ' от пользователя.',
                300: 'Информация о запросе не найдена',
                401: 'Сбой аутентификации. Неверное имя пользователя/пароль или маркер аутентификации'
                     ' или пользователь удален/заблокирован',
                402: 'Сбой аутентификации. Требуется ввести капчу для проверки пользователя',
                403: 'Сбой аутентификации',
                455: 'Невозможно выполнить операцию, так как пользователь установил на нее ограничение',
                458: 'Невозможно выполнить операцию, так как пользователь установил на нее ограничение',
                801: 'Указанный участник заблокировал текущего пользователя',
                802: 'Передан несуществующий пользователь',
                1103: 'Указанный пользователь должен быть другом',
            }
        if code in codes:
            response_text = codes[code]
        else:
            response_text = f'Код ответа {code}'
        print(response_text)
        return response_text

    def users_photo(self):
        """получение списка фотографий пользователя"""
        method = 'photos.getPhotos'
        fields = 'photo.PIC_MAX, photo.ID, photo.LIKE_COUNT, photo.MARK_AVG'
        import hashlib
        hash_text = f'application_key={self.application_key}count={self.count}fid={self.fid}fields={fields}' \
                    f'format=jsonmethod={method}{self.secret_key}'
        hash_params = hashlib.md5(hash_text.encode('utf-8'))
        sig = hash_params.hexdigest()
        import requests
        params = {'application_key': self.application_key,
                  'count': self.count,
                  'fid': self.fid,
                  'fields': fields,
                  'format': 'json',
                  'method': method,
                  'sig': sig,
                  'access_token': self.access_token}
        print('Отправляем запрос для получения списка фотографий')
        res = requests.get(self.url, params=params)
        self.server_responses(res)
        if res.status_code == 200:
            result = res.json()
        else:
            result = False
        return result

    def download_photos(self):
        """Скачивание и переименование фотографий"""
        res = self.users_photo()
        if not res:
            pass
        else:
            if 'error_code' in res:
                self.server_responses(res)
                print('Операция прервана')
                return None
            import os
            directory = os.getcwd()
            name_folder = 'download_folder'
            path = os.path.join(directory, name_folder)
            if not os.path.exists(path):
                os.mkdir(path)
                print(f'Папка "{name_folder}" создана в текущей директории')
            list_likes = []
            list_downloaded_photos = []
            for photo_parameters in res['photos']:
                if photo_parameters['like_count'] in list_likes:
                    new_name_photo = f"{photo_parameters['like_count']}_{photo_parameters['id']}.jpg"
                    list_likes.append(photo_parameters['like_count'])
                else:
                    new_name_photo = f"{photo_parameters['like_count']}.jpg"
                    list_likes.append(photo_parameters['like_count'])
                url = photo_parameters['pic_max']
                print(f'Отправка запроса на скачивание фотографии "{new_name_photo}"')
                import requests
                r = requests.get(url)
                self.server_responses(r)
                if r.status_code != 200:
                    print(f'Загрузка фотографии "{new_name_photo}" отменена')
                    continue
                path_to_photo = f'{path}/{new_name_photo}'
                with open(path_to_photo, 'wb') as file:
                    file.write(r.content)
                print(f'Фотография "{new_name_photo}" загружена в папку "{path}"')
                list_downloaded_photos += [{'Название фотографии': new_name_photo,
                                            'Средняя оценка': photo_parameters['mark_avg']}]
            from pprint import pprint
            print('Список скаченных фотографий:')
            pprint(list_downloaded_photos)

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
