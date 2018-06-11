import json
import dash
import auth
import urllib2
import simplejson as simplejs
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

key = auth.key

with open('/home/sameer/Desktop/learn_plotly/token.txt','r') as tk:
	access = tk.read()

default = 'http://ip-api.com/json'
open_d = urllib2.urlopen(default)
default_js = json.load(open_d)
default_city = default_js['city']

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

	weather = open_w['weather'][0]['description']

	temp = open_w['main']['temp']
	temp_c = temp - 273
	temp_c = round(temp_c, 2)

	ws = open_w['wind']['speed']

	return weather, temp_c, ws

def climate_info(name):
	url = 'http://api.openweathermap.org/data/2.5/weather?q='+str(name)+'&appid='+key
	open_url = urllib2.urlopen(url)
	open_w = json.load(open_url)

	_, temp_c, ws = get_stuff(name)
	temp_f = temp_c * 9/5 + 32

	hum = open_w['main']['humidity']
	press = open_w['main']['pressure'] / 100.0

	all_clouds = open_w['clouds']['all']

	temp_dict = {}
	temp_dict['celsius'] = round(temp_c, 2)
	temp_dict['farenheit'] = round(temp_f, 2)
	temp_dict['humidity'] = hum
	temp_dict['pressure'] = press
	temp_dict['windspeed-(mph)'] = ws
	temp_dict['clouds'] = all_clouds

	x_details = temp_dict.keys()
	y_details = temp_dict.values()

	return x_details, y_details

app.layout = html.Div([
	#html.Hr(),
	#html.Div(id='output-graph'),
	html.Div([
		html.H4('Global Weather'),
		dcc.Input(id='input', value=default_city, type='text', placeholder='City name: ', size=40),
		html.Div([
			html.Div([
				dcc.Graph(id='geo_graph'),
			], className='eight columns'),
			html.Div([
				dcc.Graph(id='weather-graph')
			], className='four columns')
		], className='row'),
	], style={'textAlign' : 'center'}),
])

@app.callback(
	Output('geo_graph', 'figure'),
	[Input('input', 'value')]
)
def update_location(name):
	try:
		weather_type, celsius, wind_speed = get_stuff(name)
		lat, lon = get_location(name)
		lat = str(lat)
		lon = str(lon)
		data = go.Data([
	    go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode='markers',
        marker=go.Marker(
          size=11
        ),
        text=[str(name).title() + '  ' + str(weather_type) + '  ' + str(celsius) + ' C  ' + str(wind_speed) + ' mph'],
        #hoverlabel=dict(bgcolor='rgba(188, 20, 26, 0.5)'),
        hoverinfo='text'
	    )
		])

		layout = go.Layout(
			#width=600,
			height=580,
	    autosize=True,
	    showlegend=False,
	    hovermode='closest',
	    mapbox=dict(
        accesstoken=access,
        bearing=1,
        center=dict(
          lat=int(lat.split('.')[0]),
          lon=int(lon.split('.')[0])
        ),
        pitch=0,
        zoom=6,
        style='basic'
	    ),
		)

		return {'data' : data, 'layout' : layout}

	except Exception as e:
		print(str(e))
		return html.Div([
			html.P('There is no access, sorry')
		])

@app.callback(
	Output('weather-graph', 'figure'),
	[Input('input', 'value')]
)
def weather_graph(name):
	try:
		x_details, y_details = climate_info(name)

		graphs = []
		graphs.append(
			go.Scatter(
				x=x_details,
				y=y_details,
				name='Description',
				mode='markers+lines'
			)
		)

		layout={'title' : str(name).title()}

		return {'data' : graphs, 'layout' : layout}
	except Exception as e:
		print(str(e))

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)