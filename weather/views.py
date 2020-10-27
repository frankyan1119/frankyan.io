from django.shortcuts import render
from django.http import JsonResponse

import requests
from plotly.offline import plot
from plotly.graph_objs import Scatter, Layout, Figure

from datetime import datetime


def index(request):
  search_location = 'Waterloo, ON, Canada'

  if request.method == 'POST':
    search_location = request.POST['search_location']

  weather_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units={}&appid={}'
  geo_url = 'https://nominatim.openstreetmap.org/search?q={}&format=json'

  
  password_token = '1168b0688d3ac2cb67342aaff4f30e96'

  geo = requests.get(geo_url.format(search_location)).json()[0]

  #location info
  city = (',').join(geo["display_name"].split(',')[:2])
  lat = geo['lat']
  lon = geo['lon']

  unit = 'metric'   # Celsius: metric, Fahrenheit: imperial

  weather = requests.get(weather_url.format(lat, lon, unit, password_token)).json()

  current = weather['current']
  hourly = weather['hourly']
  time_offset = weather['timezone_offset']
  cur_time = datetime.utcfromtimestamp(current['dt'] + time_offset)

  #*************Hourly forcasts************

  hourly = hourly[1:25][::3]

  x = [datetime.utcfromtimestamp(h['dt'] + time_offset).strftime('%H %p') for h in hourly]
  y = [h['temp'] for h in hourly]

  layout = Layout(
    yaxis={'visible': False, 'showticklabels': False},
    autosize=False,
    height=100,
    width=550,
    margin=dict(t=0,b=0,l=0,r=0),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
  )

  p = plot(Figure([Scatter(x=x, y=y, mode='lines+markers+text', opacity=0.8, text=y, marker_color='#fc9803')], layout), 
               output_type='div')

  #*************Hourly forecasts************

  #*************Weekly forecasts************
  
  weekly = weather['daily'][1:]

  forecast = [{'day_of_week': datetime.utcfromtimestamp(day['dt'] + time_offset).strftime('%A')[:3] + '.', 
              'hi': int(day['temp']['max']), 
              'low': int(day['temp']['min']), 
              'icon': day['weather'][0]['icon'],} for day in weekly]

  
  #*************Weekly forecasts************

  weather = {
    'city': city,
    'today': cur_time.strftime('%A'),
    'current_time': cur_time.strftime('%H:%M %p'),
    'temperature': current['temp'],
    'humidity': current['humidity'],
    'feels_like': current['feels_like'],
    'wind_speed': current['wind_speed'],
    'description': current['weather'][0]['description'],
    'icon': current['weather'][0]['icon'],
    'plot': p,
    'forecasts': forecast,
  }

  return render(request, 'weather/weather.html', weather)