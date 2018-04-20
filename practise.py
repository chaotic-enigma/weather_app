import json
import urllib2
import auth

key = auth.key
'''
def get_location(*args):
	if len(args) == 2:
		locations = []
		for i in args:
			i = i.lower()
			url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(i)+'&appid='+key

			open_url = urllib2.urlopen(url)
			open_w = json.load(open_url)
			ll = [i[1] for i in open_w['coord'].items()]
			locations.append(ll)
		first = locations[0]
		second = locations[1]
		return first, second
	else:
		return 'nope'
print(get_location('paradise', 'hindupur'))
'''

def get_location(name1, name2):
	lst = [name1, name2]
	locations = []
	for i in lst:
		i = i.lower()
		url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(i)+'&appid='+key

		open_url = urllib2.urlopen(url)
		open_w = json.load(open_url)
		ll = [i[1] for i in open_w['coord'].items()]
		locations.append(ll)
	return locations
#print(get_location('hindupur', 'bangalore')) #[[13.83, 77.49], [12.98, 77.6]]

loc1 = get_location('hindupur', 'bangalore')[0]
loc2 = get_location('hindupur', 'bangalore')[1]

lats = []
lats.append(loc1[0])
lats.append(loc2[0])

lons = []
lons.append(loc1[1])
lons.append(loc2[1])

print lats
print lons

'''
def get_stuff(*args):
	if len(args) == 2:
		description = []
		for i in args:
			i = i.lower()
			url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(i)+'&appid='+key
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

			description.append([weather, temp_c, ws])
		return tuple(description)
	else:
		return 'nope'
print(get_stuff('paradise', 'hindupur'))
'''

def get_stuff(name1, name2):
	lst = [name1, name2]
	description = []
	for i in lst:
		i = i.lower()
		url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(i)+'&appid='+key
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

		description.append([weather, temp_c, ws])
	return description
loc1, loc2 = (get_stuff('paradise', 'hindupur'))
print loc1, loc2