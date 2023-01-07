from bs4 import BeautifulSoup
import pandas as pd
from requests_html import HTMLSession
import time
import datetime

data = []


class Catering:
    def __init__(self, city, diet, days, kcal, pages):

        # Diet details
        self.city = city
        self.kcal = kcal
        self.diet = diet
        self.days = days
        self.pages = pages

        for p in range(1, self.pages + 1):
            # Self generated url with diets
            url = self.url_maker(self.city, self.days, self.diet, self.kcal, p)
            print(url)

            # Url request
            session = HTMLSession()
            resp = session.get(url)
            resp.html.render(timeout=40, wait=0, sleep=0, keep_page=True, scrolldown=1)
            # print(resp.html.html)

            # Making a soup
            self.soup = BeautifulSoup(resp.html.html, 'html.parser')
            self.parse_website(self.soup)

            # print(data)
            print()
            self.df = pd.DataFrame(data, columns=['nazwa', 'cena', 'koszt_dostawy', 'godziny_dostawy', 'dostawa_weekend', 'ocena', 'opinie'])
            # df.sort_values('cena', inplace=True)
            self.df.drop_duplicates(inplace=True)

    def __str__(self):
        return self.df.to_string()

    def parse_website(self, soup):
        for name in soup.find_all(class_='company-card'):
            # Catering name
            catering_name = name.find(class_='background')
            catering_name = catering_name.get('alt')[21:]
            # print(catering_name, end=" - Cena za dzień: ")

            # Price
            price_box = name.find(class_='price')
            # print(price_box)
            if price_box:
                prices = price_box.text.strip().strip(' zł').replace('zł  ', '').split()
                price = min([float(price.replace(',', '.')) for price in prices])
                # print(price)
            else:
                price_box = name.find(class_='information')
                # print(price_box.text)

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
                # print(del_inf)
            except AttributeError:
                delivery_info = name.find(class_='not-available-delivery')
                del_inf = [delivery_info.text, '-', '-']
                # print(del_inf)

            # Rating
            rating_box = name.find(class_='rating')
            if rating_box:
                rating = float(rating_box.text)
            else:
                rating = 0
            # print(rating)

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

    def url_maker(self, url_city, url_days, url_diet, url_kcal, url_pages):
        url = r'https://cateromarket.pl/catering-dietetyczny/'
        if url_pages == 1:
            url = fr"{url}{url_city}/{url_diet}?liczba_dni={str(url_days)}&kalorycznosc={url_kcal}"
        else:
            url = fr"{url}{url_city}/{url_diet}?liczba_dni={str(url_days)}&kalorycznosc={url_kcal}&page={str(url_pages)}"
        return url


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


city = input('Podaj miasto (bez polskich znaków): ')

diet = diety[input(f'Wybierz rodzaj diety ({list(diety.keys())}): ')]

for a in kalorycznosc.items():
    print(f'{a[0]} : {a[1]}')
kcal = kalorycznosc[int(input('Podaj kaloryczność: '))]

days = input('Podaj liczbę dni: ')

start = datetime.datetime.now()
catering = Catering(city, diet, days, kcal, 5)
end = datetime.datetime.now()

print(catering)
print(end - start)
