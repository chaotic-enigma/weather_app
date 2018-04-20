import json
import urllib2
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import simplejson as simplejs
import auth

app = dash.Dash(__name__)

key = auth.key

with open('/home/sameer/Desktop/learn_plotly/token.txt','r') as tk:
	access = tk.read()

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
	loc1 = locations[0]
	loc2 = locations[1]
	return loc1, loc2

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
		#temp_c = str(temp_c) + 'C'

		temp_f = temp_c * 9/5 + 32
		temp_f = round(temp_f, 2)

		ws = open_w['wind']['speed']
		#ws = str(ws) + 'mph'

		description.append([weather, temp_c, ws])
	return description

app.layout = html.Div([
	html.H5('Home city: '),
	dcc.Input(id='input1', value='', type='text'),
	#html.Hr(),
	html.H5('Destination city: '),
	dcc.Input(id='input2', value='', type='text'),
	#html.Hr(),
	html.Div(id='output-graph'),
	html.Div([
		html.H4('Finders and Keepers')
	], style={'textAlign' : 'center'}),
	dcc.Graph(id='graph')
])

#app.config['suppress_callback_exceptions']=True

@app.callback(
	Output('graph', 'figure'),
	[Input('input1', 'value'), Input('input2', 'value')]
)
def update_location(name1, name2):
	try:
		loc1 = get_location(name1, name2)[0]
		loc2 = get_location(name1, name2)[1]

		lats = []
		lats.append(loc1[0])
		lats.append(loc2[0])

		lons = []
		lons.append(loc1[1])
		lons.append(loc2[1])

		home, dest = get_stuff(name1, name2)
		home.insert(0, 'Home')
		dest.insert(0, 'Destination')
		data = go.Data([
		    go.Scattermapbox(
		        lat=lats,
		        lon=lons,
		        mode='markers+lines',
		        line=dict(width=2),
		        marker=go.Marker(
		            size=11,
		        ),
		        text=[home, dest],
		        #hoverlabel=dict(bgcolor='rgba(188, 20, 26, 0.5)'),
		        hoverinfo='text'
		    )
		])

		layout = go.Layout(
			#width=600,
			height=700,
		    autosize=True,
		    showlegend=False,
		    hovermode='closest',
		    geo=dict(
			    projection = dict(type="equirectangular"),
		    ),
		    mapbox=dict(
		        accesstoken=access,
		        bearing=1,
		        center=dict(
		           lat=int(str(lats[1]).split('.')[0]),
		           lon=int(str(lons[1]).split('.')[0])
		        ),
		        pitch=0,
		        zoom=5,
		        style='outdoors'
		    ),
		)


		return {'data' : data, 'layout' : layout}

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