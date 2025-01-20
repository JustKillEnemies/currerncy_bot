import requests
import xml.etree.ElementTree as ET


# Функция для получения данных о валютах с сайта Центрального банка России
def get_currency_data():
    link = "https://www.cbr.ru/scripts/XML_daily.asp"  # URL для получения ежедневных данных о курсах валют
    response = requests.get(link)  # Отправляем GET-запрос на указанный URL
    if response.status_code != 200:  # Если код ответа не 200, то выбрасываем исключение
        raise Exception(f"API error: {response.status_code}")

    xml_data = response.text  # Извлекаем текст XML из ответа
    root = ET.fromstring(xml_data)  # Преобразуем строку XML в объект ElementTree
    valutes_list = []  # Список для хранения информации о валютах

    # Ищем все элементы "Valute" в XML-данных
    for valute in root.findall("Valute"):
        # Создаем словарь для каждой валюты, извлекая нужные данные из соответствующих тегов
        cur_dict = {
            "Num_code": valute.find("NumCode").text,  # Номерной код валюты
            "Char_code": valute.find("CharCode").text,  # Символьный код валюты
            "Nominal": valute.find('Nominal').text,  # Номинал валюты
            "Name": valute.find('Name').text,  # Название валюты
            "Value": valute.find('Value').text.replace(',', '.'),  # Курс валюты
            "VunitRate": valute.find('VunitRate').text.replace(',', '.'),  # Единичная стоимость
        }

        valutes_list.append(cur_dict)  # Добавляем информацию о валюте в список

    return valutes_list  # Возвращаем список всех валют с их данными
