from django.shortcuts import render, redirect
from django.views import View
from django.templatetags.static import static
from helpers import fetch_image, fetch_weather, Weather, Image

# Create your views here.
class IndexView(View):

    def get(self, request):
        print(request.GET.get('city'))
        city = request.GET.get('city', 'Sopron')
        units = request.GET.get('units', 'metric')
        image_link = None
        image_pct = None
        error = False
        try:
            weather = fetch_weather(city, units)
        except:
            weather = Weather(current='', feels_like='', max='', min='', description='', icon='')
            error = 'Error fetching/parsing weather data. Please try later'

        try:
            image_link = fetch_image(city)
        except:
            image_pct = static('rainy.jpeg')


        return render(request, 'weather_app/index.html', {
            'image_link':image_link,
            'image_pct': image_pct,
            'city': city,
            'weather': weather,
            'units': units,
            'error': error
        })