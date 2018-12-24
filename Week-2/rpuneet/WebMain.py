"""
This is the driver program it runs the app and updates it accordingly.
"""

# All the dash packages used in the program.
import dash
from dash.dependencies import Input , Output     # For user interactions.
import dash_core_components as dcc               # For making graphs and other components.
import dash_html_components as html              # For html related components.
import plotly.graph_objs as go                   # For making bar graphs.


import os            # To get the current working directory and for other os funtions.

import Directory     # This package is used to store the directories' information.

import webbrowser    # To open the app in a web browser.


app = dash.Dash()           # Dash object.

current_path = os.getcwd()  # Stores the path of the current directory.
number_of_clicks = 0    # Stores the number of clicks on go-back button.        


details_template = '''
### Directory Details

Name : {}\n
Size : {:0.2f} {}\n
Number of Sub Directories : {}\n
Number of Sub Directories (Recursively) : {}\n
Number of Files : {}\n
Number of Files (Recursively) : {}\n
'''


# Layout of the app is defined here.
app.layout = html.Div(children=[
        html.H1(
                children="Distribution of Disk Space.",
                style={
                'textAlign':'center',
                }),   
        html.H2(
                children="Current Directory : "
                ),
        html.Div(children=[
                html.Button(
                        id='go-back',
                        children="Up"),
                dcc.Input(
                        id="directory-path",
                        value=os.getcwd(),
                        type="text",
                        style={"width":"100%"}
                    ),
                html.H3(
                        children="Sub Directories"
                        ),
                html.Div( children = [
                    dcc.Dropdown(
                        id="subdirectory-list",
                        value="Select"
                        )],
                    style={"width":"50%"}
                        )
                ]),
        html.Div(children=[
                dcc.Markdown( 
                            id="details" 
                        ),
                dcc.Graph(
                            id='subdirectories-bar-graph'
                         ),
                dcc.Graph(
                           id='files-bar-graph'
                        )
            ])
    ])
        
        
        
        

'''
This function is used to update the sub directory bar graph whenever the value in the input field changes.

Parameters - 
    (string) directory_path - Contains the path of the directory which is present in directory-path field.
Return-
    (figure) Returns a figure object which contains the bar graph for sub directories.
'''
@app.callback(  
        Output("subdirectories-bar-graph" , "figure"),
        [Input("directory-path" , "value")])
def update_directory_graph(directory_path):
    global current_path
    current_path = directory_path     # Every time the graph is updated we update the current path.
    
    current_directory = Directory.Directory(directory_path)
    subDirectories , files = current_directory.get_children_list()

    return dict(
                data=[go.Bar(
                            x = [dr.name for dr in subDirectories[1:]], 
                            y = [dr.get_stats()[0] for dr in subDirectories[1:]],
                            )],
                layout=go.Layout(
                            title="Sub-Directories",
                            )
                )
                
                

'''
This function is used to update the files bar graph whenever the value in the input field changes.

Parameters - 
    (string) directory_path - Contains the path of the directory which is present in directory-path field.
Return-
    (figure) Returns a figure object which contains the bar graph for files.
'''
@app.callback(
        Output("files-bar-graph" , "figure"),
        [Input("directory-path" , "value")])
def update_files_graph(directory_path):

    current_directory = Directory.Directory(directory_path)
    subDirectories , files = current_directory.get_children_list()

    return dict(
                data=[go.Bar(
                            x = [file.name for file in files[1:]], 
                            y = [file.get_size() for file in files[1:]],
                            )],
                layout=go.Layout(
                            title="Files",
                            )
                )
                
                
'''
This function is used to update the details of the current directory.

Parameters - 
    (string) directory_path - Contains the path of the directory which is present in directory-path field.
Return-
    (figure) Returns a children object which contains the markdown text of the details.
'''
@app.callback(  
        Output("details" , "children"),
        [Input("directory-path" , "value")])
def update_directory_details(directory_path):
    global details_template
    
    current_directory = Directory.Directory(directory_path) 
    sub_directories , files = current_directory.get_children_list()

    dr_name = current_directory.name
    dr_size = current_directory.get_stats()
    dr_all_files = dr_size[2]
    dr_all_subdr = dr_size[1]
    dr_size , size_type = get_readable_size(dr_size[0])
    dr_files = files[0]
    dr_subdr = sub_directories[0]

    return details_template.format(dr_name , dr_size , size_type , dr_subdr , dr_all_subdr , dr_files , dr_all_files)
                

"""
This function assigns a appropriate size type like KB , GB , etc. according to the size in bytes.

Parameters-
    (int) size_bytes - Size in bytes.
Return -
    (int) , (string) - Size after converting to appropriate unit and the unit.
"""
def get_readable_size(size_byte):
    unit = "bytes"
    current_size = size_byte
    if(current_size > 1024):
        unit = "KB"
        current_size /= 1024.0
    if(current_size > 1024):
        unit = "MB"
        current_size /= 1024.0
    if(current_size > 1024):
        unit = "GB"
        current_size /= 1024.0
    if(current_size > 1024):
        unit = "TB"
        current_size /= 1024.0
    return current_size , unit

'''
This function is used to update the sub directory dropdown. It gets the directory path from the directory-path field
and updates the dropdown menu accordingly.

Parameters - 
    (string) directory_path - Contains the path of the directory which is present in directory-path field.
Return-
    (figure) Returns a list which contains the labels and values of each option in the sub directory.
'''
@app.callback(
        Output("subdirectory-list" , "options"),
        [Input("directory-path" , "value")])
def update_dropdown_options(directory_path):
    
    current_directory = Directory.Directory(directory_path)
    subDirectories , files = current_directory.get_children_list()
    
    return [{'label': dr.name, 'value': dr.path} for dr in subDirectories[1:]]
                


'''
This function is used to change the path of the current directory to either a subdirectory or the parent directory
according to where the input is from. It returns the path of the directory as 'value' field in directory-path which triggers the callback 
for update_directory_graph and update_files_graph.

Parameters - 
    (string) sub_directory_path - Contains the path of the sub directory selected from the sub directory dropdown menu.
    (int) n_clicks - Stores the number of clicks on the back button. This is used to check if the back button is pressed or not.
Return-
    (string) Path of the directory
'''
@app.callback(
        Output("directory-path" , "value"),
        [Input("subdirectory-list" , "value"),
         Input("go-back" , "n_clicks")])
def change_directory(sub_directory_path , n_clicks):
    global current_path , number_of_clicks
    
    if number_of_clicks == n_clicks:    # Check if back button is pressed or not.
        return sub_directory_path      
    
    number_of_clicks = n_clicks     
    os.chdir(current_path)              # Change the current directory to the current path.
    os.chdir("..")                      # Go back to the parent directory.
    return os.getcwd()                  # return its path.



webbrowser.open("http://127.0.0.1:8050/")       # Opens local server on a browser.
app.run_server()                                # Runs the app.
    
    
    
    