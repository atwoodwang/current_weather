import datetime
import json
import sys
from urllib import request
from os import path

base_url = "http://api.worldweatheronline.com/free/v2/weather.ashx"

codes = {'113': ['clear-day.txt', 'clear-night.txt'],
         '116': ['clouds.txt', 'clous-night.txt'],
         "119": 'cloudy.txt',
         '122': 'cloudy.txt',
         '143': 'mist.txt',
         '176': 'rain.txt',
         '179': 'sleet.txt',
         '182': 'sleet.txt',
         '185': 'sleet.txt',
         '200': 'thunderstorm.txt',
         '227': 'snow.txt',
         '230': 'snow.txt',
         '248': 'fog.txt',
         '260': 'fog.txt',
         '263': 'rain.txt',
         '266': 'rain.txt',
         '281': 'sleet.txt',
         '284': 'sleet.txt',
         '293': 'rain.txt',
         '296': 'rain.txt',
         '299': 'rain.txt',
         '302': 'rain.txt',
         '305': 'rain.txt',
         '308': 'rain.txt',
         '311': 'sleet.txt',
         '314': 'sleet.txt',
         '317': 'sleet.txt',
         '320': 'snow.txt',
         '323': 'snow.txt',
         '326': 'snow.txt',
         '329': 'snow.txt',
         '332': 'snow.txt',
         '335': 'snow.txt',
         '338': 'snow.txt',
         '350': 'sleet.txt',
         '353': 'rain.txt',
         '356': 'rain.txt',
         '359': 'rain.txt',
         '362': 'sleet.txt',
         '365': 'sleet.txt',
         '368': 'snow.txt',
         '371': 'snow.txt',
         '374': 'sleet.txt',
         '377': 'sleet.txt',
         '386': 'thunderstorm.txt',
         '389': 'thunderstorm.txt',
         '392': 'snow.txt',
         '395': 'snow.txt'
         }


class Query(object):
    def __init__(self, location):
        self.location = location.replace(' ', '+')
        self.city=location
        self.key = "fa8b581c7f4845fe8b0213648161203"

    def query(self):
        url = base_url + "?key=%s&q=%s&num_of_days=3&format=json&lang=us&extra=localObsTime" % (
            self.key, self.location)
        with request.urlopen(url) as f:
            if f.status != 200:
                return
            parsed_json = json.loads(f.read().decode('utf8'))
        data = parsed_json['data']

        try:
            # Acquire the weather data. The number in [] represent the
            # day you want to query. '0' means today, and '1' means
            # tomorrow.
            self.weather = data['current_condition'][0]
        except KeyError:
            print("\033[1;31;49m" + "Please enter the correct city name or zip code！" + "\033[0m")
            sys.exit()

    def output(self):
        print('\n')
        code = self.weather['weatherCode']
        weatherCondition = codes[code]
        if code == '113' or code == '116':
            hour = datetime.datetime.now().hour
            weatherCondition=weatherCondition[1] if (hour<6 or hour>20) else weatherCondition[0]
        rel_path = path.join('icons', weatherCondition)
        file_path = path.relpath(rel_path)
        with open(file_path) as f:
            print(f.read())
        print('\n')
        print("\tCurrent weather is\033[36m %s \033[0min \033[33m%s\033[0m. Last observation "
              "time(locale) "
              "is \033[35m%s\033[0m." %(
            self.weather[
                                                                                'weatherDesc'][0][
                                                                                  'value'],
                                                                            self.city,
                                                                            self.weather[
                                                                                'localObsDateTime']))
        print('\tThe temperature is \033[32m%d°C\033[0m, but it feels like \033[32m%d°C\033[0m.\n'%(
            int(self.weather['temp_C']),int(self.weather['FeelsLikeC'])))
        print('\tThe humidity is %d.'%int(self.weather['humidity']))
        print('\tThe visibility is %d miles.'%int(self.weather['visibility']))
        print('\tThe wind speed is %d miles/hour, direction is %s.'%(int(self.weather[
                                                                         'windspeedMiles']),
                                                                     self.weather[
                                                                         'winddir16Point']))
        print('\tThe precipitation is %.1f in millimeters.'%(float(self.weather['precipMM'])))
        print('\tHava a nice day!!')

def main(argv):
    try:
        city = argv[1]
        city = ' '.join(argv[1:])
    except IndexError:
        print("\033[1;31;49m" + "Enter city name or US zip code:" + "\033[0m")
        city = input()
        if city == '':
            sys.exit()
    query = Query(city)
    query.query()
    query.output()


if __name__ == '__main__':
    main(sys.argv)
