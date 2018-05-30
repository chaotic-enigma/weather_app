import urllib
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import simplejson as simplejs
import plotly.graph_objs as go

app = dash.Dash(__name__)

with open('/home/sameer/Desktop/learn_plotly/token.txt','r') as tk:
	access = tk.read()

def get_directions(origin, destination):

	with open('google_key.txt', 'r') as gk:
		key = gk.read()

	endpoint = 'https://maps.googleapis.com/maps/api/directions/json?origin='+str(origin)+'&destination='+str(destination)+'&key'+str(key) 

	response = urllib.urlopen(endpoint).read()
	directions = json.loads(response)

	lats = []
	lons = []

	for i in directions['routes']:
		for j, k in i.items():
			if j == 'legs':
				for l in k:
					for m, n in l.items():
						if m == 'steps':
							for o in n:
								for p, q in o.items():
									if p == 'end_location':
										for l1, l2 in q.items():
											if l1 == 'lat':
												lats.append(l2)
											if l1 == 'lng':
												lons.append(l2)

	return lats, lons

app.layout = html.Div([
	html.H5('Home city: '),
	dcc.Input(id='input1', value='', type='text', placeholder='home city: '),
	#html.Hr(),
	html.H5('Destination city: '),
	dcc.Input(id='input2', value='', type='text', placeholder='destination: '),
	#html.Hr(),
	html.Div(id='output-graph'),
	html.Div([
		html.H4('Finders and Keepers')
	], style={'textAlign' : 'center'}),
	dcc.Graph(id='graph')
])

@app.callback(
	Output('graph', 'figure'),
	[Input('input1', 'value'), Input('input2', 'value')]
)
def get_route(origin, destination):
	try:
		lats, lons = get_directions(origin, destination)
		data = go.Data([
			go.Scattermapbox(
				lat=lats,
				lon=lons,
				mode='markers+lines',
				line=dict(width=2),
				marker=go.Marker(
					size=5,
				),
				#text=[home, dest],
				#hoverlabel=dict(bgcolor='rgba(188, 20, 26, 0.5)'),
				#hoverinfo='text'
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
					lat=int(str(lats[0]).split('.')[0]),
					lon=int(str(lons[0]).split('.')[0])
				),
				pitch=0,
				zoom=3,
				style='light'
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