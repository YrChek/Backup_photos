def user_vk():
    id_users = input('Введите id пользователя:\n')
    token = input('Введите токен:\n')
    from vk import VK
    user = VK(id_users, token)
    method_selection = input('Введите любую букву для выбора альбома \n'
                             'Или просто нажмите "Enter" для выбора фотографий из профиля ')
    if method_selection:
        albums = user.user_albums()
        if isinstance(albums, list):
            print('Список альбомов пользователя')
            [print(album) for album in albums]
            album_id = input('Введите id альбома\n')
            list_downloaded_photos = user.download_photos(album_id=album_id)
            return list_downloaded_photos
        else:
            print('Загрузка фотографий из альбома не удалась.\n'
                  'Загрузить фотографии из профиля?')
            action = input('Для загрузки фотографий введите любую букву, для отмены нажмите "Enter" ')
            if action:
                list_downloaded_photos = user.download_photos()
                return list_downloaded_photos
            else:
                print('Программа завершена')
                return False
    else:
        list_downloaded_photos = user.download_photos()
        return list_downloaded_photos


def user_ok():
    fid = input('Введите ID пользователя ')
    application_key = input('Введите публичный ключ приложения\n')
    secret_key = input('Введите сессионный секретный ключ\n')
    access_token = input('Введите токен\n')
    from classmates import Classmates
    user = Classmates(fid, secret_key, application_key, access_token)
    list_downloaded_photos = user.download_photos()
    return list_downloaded_photos


def clear_folder(name_folder):
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
    return True


def user_start():
    social_network = int(input('Введите "1" для выбора фотографий из "В Контакте", \nВведите "2" для выбора фотографий'
                               ' из "Одноклассники"\n'))
    download = False
    if social_network == 1:
        download = user_vk()
    elif social_network == 2:
        download = user_ok()
    else:
        print('Неправильный ввод')
        return False
    if download:
        query = input('Загрузить фотографии на Яндекс Диск?\n'
                      'Если "нет" - введите любую букву, если "да" - нажмите "Enter" ')
        if not query:
            from yandex import Yan_disk
            token = input('Введите токен для Яндекс Диска:\n')
            upload = Yan_disk(token)
            creat = input('На Яндекс Диске будет создана папка "Фотографии"\n'
                          'Для отмены введите любую букву, для продолжения нажмите "Enter" ')
            if creat:
                result = upload.uploading_files()
            else:
                upload.creating_folder()
                result = upload.uploading_files()
        else:
            result = True
        select = input('Удалить загруженные фотографии с компьютера?\n'
                       '"ДА" - введите любую букву. "НЕТ" - нажмите "Enter" ')
        if select:
            clear_folder('download_folder')
    else:
        result = False
    if result:
        print('Выбранные операции завершены успешно')
    else:
        print('Ошибка загрузки фотографий')
    return result


if __name__ == '__main__':
    user_start()

