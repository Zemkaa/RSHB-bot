import requests
from transliterate import translit
from googletrans import Translator
import datetime
from bs4 import BeautifulSoup


def vk_parsing(vk_id):
    token = '8b9f58ea8b9f58ea8b9f58eab98bf5a2d188b9f8b9f58ead767545b404b0c2293ca5e22'
    version = "5.122"
    fields = "bdate,career,city,contacts,country,education,interests,military," \
             "movies,music,nickname,personal,relation,sex,tv,universities"
    name_case = 'nom'
    full_info = []
    flag = False
    year = datetime.datetime.now().year
    translator = Translator()
    response = requests.get('https://api.vk.com/method/users.get',
                            params={
                                'access_token': token,
                                'v': version,
                                'user_ids': vk_id,
                                'fields': fields,
                                "name_case": name_case
                            }
                            )
    data = response.json()['response'][0]
    if data['is_closed'] and data['can_access_closed']:
        return 'Доступ к данной странице закрыт, пожалуйста, добавьте в друзья vk.com/zemkaxd для автоматического ' \
               'заполнения данных.'
    full_info.append(f"Имя: {translit(data['first_name'], 'ru')}")
    full_info.append(f"Имя: ")
    full_info.append(f"Фамилия: {translit(data['second_name'], 'ru')}")
    full_info.append(f"Фамилия: ")
    try:
        if data['contacts']['mobile_phone']:
            full_info.append(f"Мобильный телефон: {data['contacts']['mobile_phone']}")
        elif data['contacts']['home_phone']:
            full_info.append(f"Домашний телефон: {data['contacts']['home_phone']}")
        else:
            full_info.append(f"Мобильный телефон: ")
            full_info.append(f"Домашний телефон: ")
    except:
        full_info.append(f"Мобильный телефон: ")
        full_info.append(f"Домашний телефон: ")
    try:
        full_info.append(f'Страна: {translator.translate(data["country"]["title"], dest="ru")}')
    except:
        full_info.append(f'Страна: ')
    try:
        full_info.append(f'Город: {translator.translate(data["city"]["title"], dest="ru")}')
    except:
        full_info.append(f'Город: ')
    try:
        full_info.append(f"Дата рождения: {data['bdate']}")
        try:
            birth_year = int(data['bdate'][-1:-5])
            if 17 <= year - birth_year >= 18:
                flag = True
        except:
            flag = False
    except:
        full_info.append(f"Дата рождения: ")
    try:
        if data['sex'] == 1:
            full_info.append(f"Пол: женский")
            flag = False
        elif data['sex'] == 2:
            full_info.append(f"Пол: мужской")
            flag = True
        else:
            full_info.append(f"Пол: ")
    except:
        full_info.append(f"Пол: ")
    try:
        if len(data['career']) >= 1:
            if len(data["career"][-1]["company"]) > 0:
                full_info.append(f"Место работы: {data['career'][-1]['company']}")
                if data["career"][-1]["position"]:
                    full_info.append(f"Позиция в компании: {data['career'][-1]['position']}")
                else:
                    full_info.append(f"Позиция в компании: ")
            else:
                full_info.append(f"Место работы: ")
        else:
            full_info.append(f"Место работы: ")
    except:
        full_info.append(f"Место работы: ")
    full_info.append(f"Заработная плата(руб в месяц): ")
    if flag:
        full_info.append('Необходимость в военной службе: да')
        try:
            if data['military']:
                full_info.append('Военная служба: пройдена')
            else:
                full_info.append('Военная служба: не пройдена')
        except:
            full_info.append('Военная служба: не пройдена')
    else:
        full_info.append('Необходимость в военной службе: нет')
    return full_info


# Парсинг данных с сервиса Facebook контролируется компанией,
# для правомерного автоматического сбора данных нужно получить письменное разрешение компании
def fb_parsing(url):
    html = requests.get(url)
    soup = BeautifulSoup(html, 'lxml')
    name = soup.find('h1', class_='gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl bp9cbjyn j83agx80', dir="auto").text.split()
        

information = vk_parsing('zemkaxd')
print(1)
