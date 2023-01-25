from datetime import date
from librus_scraper import get_cookies
import bs4
import sys
import requests

# login i password to librus
login_password = get_cookies("10366405", "slaWik2014.")


def get_date_librus(cookies: dict) -> list:
    day = str(date.today())
    response = bs4.BeautifulSoup(
        requests.get(url="https://synergia.librus.pl/ogloszenia", cookies=cookies).text, "html.parser")
    head = ["_", "temat", "data", "tresc"]
    announcements = [dict(zip(head, map(lambda x: x.text, anouncement.find_parent("table"))))
                     for anouncement in response.find_all("td", string=day)]
    return announcements

get_date_librus(login_password)

def get_content(cookies: dict) -> list:
    content_in = get_date_librus(cookies)
    contents = []
    if not content_in:
        sys.exit()
    else:
        for cont in content_in:
            theme = cont.get("temat").replace("\n\n", "").strip()
            temp_content_list = cont.get("tresc").split('\n\n\n')[2:]
            content_temp = [_ for _ in temp_content_list if _]
            pure_content = " ".join(content_temp[0].split()[1:])
            contents.append({"theme": theme, "content": pure_content})
            print(contents)
    return contents


def librus_ads(user_data):
    id_user = tuple(user_data.keys())
    secret_data = user_data.get(id_user[0])
    print(user_data)
    login_password = get_cookies(secret_data[0], secret_data[1])
    content = get_content(login_password)
    print(content)
    return ["<b> Тема:</b> \n"+cont['theme']+".\n<b>Подробнее:</b>\n"+ cont['content']+"." for cont in content]
