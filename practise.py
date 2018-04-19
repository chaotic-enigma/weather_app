import json
import urllib2
import auth

key = auth.key

def get_location(name):
	name = name.lower()
	url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(name)+'&appid='+key
	open_url = urllib2.urlopen(url)
	open_w = json.load(open_url)
	ll = [i[1] for i in open_w['coord'].items()]
	lat = ll[0]
	lon = ll[1]
	return lat, lon

def get_stuff(name):
	name = name.lower()
	url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(name)+'&appid='+key
	open_url = urllib2.urlopen(url)
	open_w = json.load(open_url)

	clouds = open_w['clouds']

	cloudy = clouds.values()[0]
	weather = open_w['weather'][0]['description']
	temp = open_w['main']['temp']

	temp_c = temp - 273
	temp_c = round(temp_c, 2)

	temp_f = temp_c * 9/5 + 32
	temp_f = round(temp_f, 2)

	ws = open_w['wind']['speed']

	return cloudy, weather, temp_c, temp_f, ws
print get_stuff('bangalore')