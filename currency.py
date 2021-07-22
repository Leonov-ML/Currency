import requests
import datetime
from xml.etree import ElementTree


class CurrencyAnalizer:
    def __init__(self, day_numbers=90):
        self.url = 'http://www.cbr.ru/scripts/XML_daily_eng.asp'
        self.day_numbers = day_numbers
        self.date_values = {}

        def data_structure(self):
            date = datetime.date.today()
            for i in range(self.day_numbers):
                self.date_values[str(date)] = {}
                y = str(date.year)
                m = str(date.month)
                d = str(date.day)
                if len(m) < 2:
                    m = '0' + m
                if len(d) < 2:
                    d = '0' + d
                params = {'date_req': f'{d}/{m}/{y}'}
                res = requests.get(self.url, params=params)
                root = ElementTree.fromstring(res.text)
                for child in root:
                    self.date_values[str(date)][child[3].text] = float(child[4].text.replace(",", "."))
                date = date - datetime.timedelta(1)
            # print(self.date_values)
            return self.date_values

        data_structure(self)

    def statistic(self):
        min_dict = {}
        date_minimum = {}
        max_dict = {}
        date_maximum = {}
        average_dict = {}
        data_dict = self.date_values
        for date in data_dict.keys():
            for currency_name in data_dict[date].keys():
                if currency_name in min_dict:
                    if data_dict[date][currency_name] < min_dict[currency_name]:
                        min_dict[currency_name] = data_dict[date][currency_name]
                        date_minimum[currency_name] = date
                else:
                    min_dict[currency_name] = data_dict[date][currency_name]
                    date_minimum[currency_name] = date
                if currency_name in max_dict:
                    if data_dict[date][currency_name] > max_dict[currency_name]:
                        max_dict[currency_name] = data_dict[date][currency_name]
                        date_maximum[currency_name] = date
                else:
                    max_dict[currency_name] = data_dict[date][currency_name]
                    date_maximum[currency_name] = date
                if currency_name in average_dict:
                    average_dict[currency_name] += data_dict[date][currency_name]
                else:
                    average_dict[currency_name] = data_dict[date][currency_name]
        for key in average_dict.keys():
            average_dict[key] /= self.day_numbers
        for currency_name in max_dict.keys() and min_dict.keys():
            print(f' Курс {currency_name} достигал максимум {date_maximum[currency_name]} '
                  f'числа и составлял {round(max_dict[currency_name], )} рублей')
            print(f' Курс {currency_name} средний за {self.day_numbers} дней составляет'
                  f' {round(average_dict[currency_name], 2)} рублей')
            print(f' Курс {currency_name} был минимальным {date_minimum[currency_name]}'
                  f' числа и составлял {round(min_dict[currency_name], 2)} рублей')


if __name__ == "__main__":
    data_currency = CurrencyAnalizer()
    data_currency.statistic()
