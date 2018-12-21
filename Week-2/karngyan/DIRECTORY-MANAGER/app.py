#! python3

import os, webbrowser

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

import tree

curr_path = ''

def make_folder_pie(folders):
	"""Make the folder distribution-pie.

		Argument(s):
		folders -- List of 2 lists ([folder-name],[folder-size])
	"""
	return dcc.Graph(
		id = 'folder-pie',
		figure = go.Figure(
			data = [
				go.Pie(
					labels = folders[0],
					values = folders[1],
					hoverinfo = 'label+percent'
				)

			],
			layout = go.Layout(
				title = f'Directories Distribution',
			)

		)
	)

def make_file_pie(files):
	"""Make the file distribution-pie.

		Argument(s):
		files -- List of 2 lists ([file-name],[file-size])
	"""
	return dcc.Graph(
		id = 'file-pie',
		figure = go.Figure(
			data = [
				go.Pie(
					labels = files[0],
					values = files[1],
					hoverinfo = 'label+percent'
				)

			],
			layout = go.Layout(
				title = f'File Distribution',
			)

		)
	)

def make_file_type_pie(file_types):
	"""Make the file-type distribution-pie.

		Argument(s):
		folders -- Dictionary, keys = extenstion, value = file-type-frequency 
	"""
	return dcc.Graph(
		id = 'file-type-pie',
		figure = go.Figure(
			data = [
				go.Pie(
					labels = list(file_types.keys()),
					values = list(file_types.values()),
					hoverinfo = 'label+percent'
				)
			],
			layout = go.Layout(
				title = f'File type distribution (Current Location)'
			)
		)
	)


def make_readable(size):
	"""Make the size of file/folder readable.

		Argument(s):
		size -- int (size unit: bytes)
	"""
	size = int(size)
	power = 2**10
	n = 0
	D = {0 : ' B', 1: ' KB', 2: ' MB', 3: ' GB', 4: ' TB'}
	while size > power:
		size /=  power
		n += 1

	return str(round(size,2))+D[n]

def make_pie(path):
	"""Generates three pies (file, folder, file-type).

		Argument(s):
		path -- Complete path of the folder (string)
	"""
	folder = tree.Tree(path)

	try:
		folder.make_tree()
	except OSError as e:
		return html.Div([

			html.H4(f'Location: {path}'),

			html.Label(f'{e}: Permission Denied'),
		])

	folders = folder.get_folders()
	files = folder.get_files()
	file_types = folder.get_file_types()

	if(len(file_types) != 0 and len(folders[0])==0):
		return html.Div([
			html.Label(f'Location: {path}'),
			html.Label(f'Total Size: {make_readable(folder.total_size())}'),
			html.Br(),
			html.Hr(),
			html.Label(
				children = 'No sub-folders present.',
				style = {
					'textAlign' : 'center' 
				}
			),
			html.Hr(),
			make_file_type_pie(file_types),
			html.Hr(),
			make_file_pie(files)
		])



	elif(len(file_types) == 0 and len(folders[0])!=0):
		return html.Div([
			html.Label(f'Location: {path}'),
			html.Label(f'Total Size: {make_readable(folder.total_size())}'),
			html.Br(),
			html.Hr(),
			make_folder_pie(folders),
			html.Hr(),
			html.Label(
				children = 'No files present.',
				style = {
					'textAlign' : 'center' 
				}
			)
		])


	elif(len(file_types) == 0 and len(folders[0])==0):
		return html.Div([
			html.Label(f'Location: {path}'),
			html.Label(f'Total Size: {make_readable(folder.total_size())}'),
			html.Br(),
			html.Label(
				children = 'Empty Directory',
				style = {
					'textAlign' : 'center' 
				}
			)
		])

	else:
		folders[0].append('_Other Files_')
		folders[1].append(sum(files[1]))
		return html.Div([
			html.Label(f'Location: {path}'),
			html.Label(f'Total Size: {make_readable(folder.total_size())}'),
			html.Br(),
			html.Hr(),
			make_folder_pie(folders),
			html.Hr(),
			make_file_type_pie(file_types),
			html.Hr(),
			make_file_pie(files)
		])

def make_dropdown(path):
	"""Generates dropdown menu containing folder and file list in path.

		Argument(s):
		path -- Complete path of the folder (string)
	"""
	folder = tree.Tree(path)

	try:
		folder.make_tree()
	except OSError as e:
		return dcc.Dropdown(
		    placeholder = f'Permission Denied: {e}'
		)

	folders = folder.get_folders()
	files = folder.get_files()

	dropdown_options = []
	
	for sub_folder in folders[0]:
		dropdown_options.append(
			{
				'label': f'Folder: {sub_folder}', 'value': os.path.join(path,sub_folder) 
			}
		)

	for file in files[0]:
		file_size = make_readable(tree.get_size(os.path.join(path,file)))
		dropdown_options.append(
			{
				'label': f'File: {file} ( {file_size} )', 'value': os.path.join(path,file) , 'disabled': 'True'
			}
		)

	return html.Div(children = [
			html.H4('Sub - Directories / Files'),
			dcc.Dropdown(
					id = 'my-dropdown',
				    options=dropdown_options,
				    placeholder = 'Select a sub-folder or file... '
				)
		])

#initialize app
app = dash.Dash()

#Title of the app
app.title = 'Directory Manager'

#external css style sheet
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

#Multiple Callback Exceptions
app.config['suppress_callback_exceptions']=True


#Layout
app.layout = html.Div(children = [

		html.Label('Enter the path of the folder: '),
		dcc.Input(
			id = 'input-state',
			type = 'text', 
			value = '', 
			placeholder = 'Path(Folder)...',
			style = { 'width': '100%'}
		),

		html.Div( children = [

			html.Div(
				id= 'dropdown'
			),
			
			html.Div(
				id = 'pies'
			)

		])

	]
)

@app.callback(
	Output('dropdown','children'),
	[Input('input-state','value')]
)
def update_dropdown(path):
	return make_dropdown(path)


@app.callback(
	Output('pies', 'children'),
    [Input('input-state','value')]
)
def update_pie(path):
	global curr_path
	curr_path = path

	return make_pie(path)

@app.callback(
	Output('input-state','value'),
	[Input('my-dropdown','value')]
)
def update_subfolder_pie(path):
	global curr_path
	return os.path.join(curr_path , path)


#Run Server
if __name__ == '__main__':
	webbrowser.open('http://127.0.0.1:8050/')
	app.run_server(debug = True)


