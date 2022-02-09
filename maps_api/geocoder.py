from io import BytesIO

import requests
from PIL import Image

API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"


def geocode(address):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": API_KEY,
        "geocode": address,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()
    else:
        json_response = None
        # обработка ошибочной ситуации
        raise RuntimeError(f"""Ошибка выполнения запроса: {response.url}
        HTTP status: {response.status_code}({response.reason})""")

    # Получаем первый топоним из ответа геокодера.
    return json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_ll_spn(address):
    toponym = geocode(address)
    if not toponym:
        return None

    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([str(toponym_longitude), str(toponym_lattitude)])

    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split()
    r, t = envelope["upperCorner"].split()
    dx, dy = abs(float(l) - float(r)) / 2, abs(float(t) - float(b)) / 2
    spn = ",".join(list(map(str, [dx, dy])))
    return ll, spn


def get_nearest_object():
    pass


def show_map(ll, spn, map_type="map", add_params=None):
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": map_type,
    }
    if add_params:
        map_params.update(add_params)

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    Image.open(BytesIO(response.content)).show()
