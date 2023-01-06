import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

data = []


class Catering:
    def __init__(self, city, diet, days, kcal, pages):
        self.city = city
        self.kcal = kcal
        self.diet = diet
        self.days = days
        self.pages = pages

        url = self.url_maker(self.city, self.days, self.diet, self.kcal, self.pages)
        print(url)

        session = HTMLSession()
        resp = session.get(url)
        resp.html.render(timeout=40, wait=2, sleep=2, keep_page=True, scrolldown=1)
        #
        # print(resp.html.html)
        e = resp.html.find("#price")
        for h in e:
            print(h)


        # page = requests.get(url, timeout=(3.05, 27))
        # page.encoding = 'utf-8'
        # print(page)
        # data = []

        # strona2 = open('xx.htm', 'r', encoding='utf-8')
        # content2 = strona2.read()

        soup2 = BeautifulSoup(resp.html.html, 'html.parser')
        # for price in soup2.find_all(class_="price"):
        #     print(price)

        for name in soup2.find_all(class_='company-card'):
            # Catering name
            catering_name = name.find(class_='background')
            catering_name = catering_name.get('alt')[21:]
            print(catering_name, end=" - Cena za dzień: ")

            # Price
            price_box = name.find(class_='price')
            print(price_box)
            if price_box:
                prices = price_box.text.strip().strip(' zł').replace('zł  ', '').split()
                price = min([float(price.replace(',', '.')) for price in prices])
                print(price)
            else:
                price_box = name.find(class_='information')
                print(price_box.text)

            # Delivery information
            try:
                delivery_info = name.find(class_='delivery-information')
                del_inf = [line for line in delivery_info.text.split(" • ")]
                if len(del_inf) < 3:
                    if len(del_inf) == 2:
                        del_inf.append('-')
                    else:
                        del_inf.append('-')
                        del_inf.append('-')
                print(del_inf)
            except AttributeError:
                delivery_info = name.find(class_='not-available-delivery')
                del_inf = [delivery_info.text, '-', '-']
                print(del_inf)

            # Rating
            rating_box = name.find(class_='rating')
            if rating_box:
                rating = float(rating_box.text)
            else:
                rating = 0
            print(rating)

            # Opinie
            opinion_box = name.find(class_='opinions-count')
            if opinion_box:
                opinions = opinion_box.text
                # print(opinions)
                if opinions == ' brak opinii ':
                    op = 0
                else:
                    op = int(opinions.split()[0])
                # print(op)

            data.append([catering_name, price, *del_inf, rating, op])
            data.sort(key=lambda x: x[1])

        # print(data)
        print()
        df = pd.DataFrame(data, columns=['nazwa', 'cena', 'koszt_dostawy', 'godziny_dostawy', 'dostawa_weekend', 'ocena', 'opinie'])
        # df.sort_values('cena', inplace=True)
        df.drop_duplicates(inplace=True)
        print(df.to_string())

    def url_maker(self, city, days, diet, kcal, pages):
        url = r'https://cateromarket.pl/catering-dietetyczny/'
        if pages == 1:
            url = fr"{url}{city}/{diet}?liczba_dni={str(days)}&kalorycznosc={kcal}"
        else:
            url = fr"{url}{city}/{diet}?liczba_dni={str(days)}&kalorycznosc={kcal}&page={str(pages)}"
        return url


# if __name__ == '__main__':
#     catering = Catering('poznan', 'dieta-cukrzyca', 20, '1000-1100', 8)

diety = {'odchudzająca': 'dieta-odchudzajaca',
         'wegetariańska': 'dieta-wegetarianska',
         'wegańska': 'dieta-weganska',
         'sport': 'dieta-sport',
         'paleo': 'dieta-paleo',
         'bezglutenowa': 'dieta-bezglutenowa',
         'bez laktozy': 'dieta-bez-laktozy',
         'detoks sokowy': 'dieta-detoks-sokowy',
         'keto': 'dieta-ketogeniczna',
         'niski IG': 'dieta-cukrzyca',
         'hashimoto': 'dieta-hashimoto',
         'low carb': 'dieta-low-carb',
         }

kalorycznosc = {1: '1000-1500',
                2: '1500-2000',
                3: '2000-2500',
                4: '2500-3000',
                5: '3000-6000',
                }
[print(f'{a[0]} : {a[1]}') for a in kalorycznosc.items()]
# city = input('Podaj miasto (bez polskich znaków: ')
# diet = diety[input(f'Wybierz rodzaj diety ({list(diety.keys())}): ')]
# kcal = kalorycznosc[int(input(f'{[f"{a[0]} : {a[1]}" for a in kalorycznosc.items()]}\nPodaj kaloryczność: '))]
# days = input('Podaj liczbę dni: ')

# catering = Catering(city, diet, days, kcal, 5)
a,b,c = None, None, None
for n, l in enumerate([a, b, c], 2):
    l = Catering('poznan', diety['niski IG'], 15, kalorycznosc[1], n)
    time.sleep(3)
# catering = Catering('poznan', diety['niski IG'], 15, kalorycznosc[2], 3)
