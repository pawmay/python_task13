from datetime import datetime
import requests
import sys


class WeatherForecast:

    BASE_URL = 'http://api.weatherapi.com/v1/history.json'

    def __init__(self, api_key, date=str(datetime.today().date())):
        self.api_key = api_key
        self.date = date
        self.data = self.get_data()

    def get_data(self):
        request_url = f'{self.BASE_URL}?key={self.api_key}&q=Warsaw&dt={self.date}'
        r = requests.get(request_url)
        content = r.json()
        return content

    def get_temperature(self):
        avg_temp = self.data['forecast']['forecastday'][0]['day']['avgtemp_c']
        return avg_temp

    def get_rain_info(self):
        totalprecip_mm = float(self.data['forecast']['forecastday'][0]['day']['totalprecip_mm'])
        return self.get_rain_chance(totalprecip_mm)

    def get_rain_chance(self, totalprecip_mm):
        if totalprecip_mm > 0.0:
            return "Będzie padać"
        elif totalprecip_mm == 0.0:
            return "Nie będzie padać"
        return "Nie wiem!"

class Result:

    def __init__(self):
        self.results = []

    def open_file(self):
        pass

    def save_file(self):
        pass


results = []

try:
    file = open('result.txt', 'r')
    for line in file.readlines():
        splitted_line = line.split(';')
        results.append([splitted_line[0], splitted_line[1].replace('\n', '')])
    file.close()
except FileNotFoundError:
    pass

for date in results:
    if date[0] == sys.argv[2]:
        # no request
        print(date[1])
        sys.exit()

weather = WeatherForecast(api_key=sys.argv[1], date=sys.argv[2])
rain_info = weather.get_rain_info()
results.append([sys.argv[2], rain_info])
print(rain_info)

with open('result.txt', 'w') as file2:
    rows = ''
    for row in results:
        rows = rows + row[0] + ';' + row[1] + '\n'
    file2.write(rows)