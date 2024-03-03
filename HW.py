# Выполнить скрейпинг данных в веб-сайта
# http://books.toscrape.com/ и извлечь информацию
# о всех книгах на сайте во всех категориях: название,
# цену, количество товара в наличии
# (In stock (19 available)) в формате integer,
# описание.
#
# Затем сохранить эту информацию в JSON-файле.
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re
import json
print(__name__)

def join_func():
    global value
    url = "http://books.toscrape.com"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.prettify()) # для красоты вывода в консоли претиф

    release_link = []
    for link in soup.find_all("li",{"class": "col-xs-6 col-sm-4 col-md-3 col-lg-3"}):
        etag = link.find("a")
        if etag:
            release_link.append(etag.get("href")) # циклом фор проходим по каждой книге на странице
    print(release_link)
    url_join = [urllib.parse.urljoin("http://books.toscrape.com", link) for link in release_link]
    # генераторным выражением передаем ссылки на каждую книгу и запоминаем в новый список ссылок
    data = []
    # Теперь через фор переходим по ссылкам по книжкам
    for url in url_join:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_= "table table-striped")
        if not table:
            continue
    # вошли в таблицу и идeм по рядам в этой таблице вниз и если нету ее то пропускаем и идем дальше
        rows = table.find_all("tbody", {"class": "table table-striped"})
        row_data = {}
        for row in rows:
            key = row.find("tr").text.strip()
            span = row.find_all("tr").text.strip()
            if len(span) > 1:
                value = span[1].text.strip()
            if key == "Price (excl. tax)":
                value = int(re.sub('[^0-9]', '', value))
            elif key == "Price (incl. tax)":
                value = value
            elif key == "Tax":
                try:
                    time_parts = re.findall(r'\d+', value)
                    hours, minutes = map(int, time_parts)
                    value = hours * 3600 + minutes * 60
                except ValueError:
                    continue
            elif key == "Number of reviews":
                value = value
            elif key == "Availability":
                value = value
            elif key == "Product Type":
                value = value
            row_data[key] = value
        if row_data:
            data.append(row_data)
    return data

def save_data_to_json(data, filename='HW.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    data = join_func()
    save_data_to_json(data)

if __name__ == '__main__':
    main()




