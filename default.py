import urllib2
import auth
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import simplejson as simplejs

app = dash.Dash(__name__)

key = auth.key

with open('token.txt','r') as tk:
	access = tk.read()

def current_location(name):
	default = 'http://ip-api.com/json'
	open_d = urllib2.urlopen(default)
	default_js = json.load(open_d)

	lat = default_js['lat']
	lon = default_js['lon']
	return lat, lon

def show_climate(name):
	lat, lon = current_location(name)
	url = 'http://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lon)+'&appid='+key
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

	return weather, temp_c, ws

app.layout = html.Div([
	html.H3('Current location tracker'),
	dcc.Input(id='input', value=''),
	html.Div(id='output-graph'),
	dcc.Graph(id='graph')
])

@app.callback(
	Output('graph', 'figure'),
	[Input('input', 'value')]
)
def location_tracker(name):	
	lat, lon = current_location(name)
	weather_type, celsius, wind_speed = show_climate(name)
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
		height=620,
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
		    style='dark'
		),
	)

	return {'data' : data, 'layout' : layout}


external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})
	
if __name__ == '__main__':
	app.run_server(debug=True)