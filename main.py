from vk import VK
from classmates import Classmates
from yandex import Yan_disk


# По условию задания для VK требуется вводить id пользователя.
# Поиск токена по ссылке - частный случай, поэтому в дальнейшую программу я эту функцию не встраивал.

def user_id(token='958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008',
            search_link='https://vk.com/begemot_korovin'):
    """Получение id по https://vk.com/begemot_korovin"""
    import requests
    URL = 'https://api.vk.com/method/users.search'
    params = {
        'access_token': token,
        'q': search_link,
        'v': '5.131',
    }
    res = requests.get(URL, params=params).json()
    id_vk = res['response']['items'][0]['id']
    return id_vk  # users_id = '552934290' (Полученный id)


if __name__ == '__main__':
    begemot = VK('552934290')
    begemot.download_photos()
    friend = Classmates('')
    friend.download_photos()
    user = Yan_disk('')
    user.uploading_files()
