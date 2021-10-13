#! /usr/bin/env python3

from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import plotly.express as px
import pandas as pd

from Components import DataTable


numBoxes = 10 # Make sure this is even
boxes = []
for box in range(numBoxes):
    InputBox = dcc.Input(id=f'InputBox_{box}',placeholder=f'Numero de participante {box+1}', n_submit=1, 
                        value="", className='div-inputbox')
    boxes.append(InputBox)

Rows = []
# Create rows of pairs of boxes
for pair in range(numBoxes//2):
    Rows.append(dbc.Row([boxes[pair*2],boxes[pair*2+1]]))

# Include button for uploading data
upload = dcc.Upload(html.Button("Subir archivo"),id="upload",multiple=False)

# Create column with the rows of input boxes and the upload button
BoxesCol = dbc.Col(Rows,style={"margin-left":"0px","margin-bottom":"30px"})
BoxesCol = dbc.Col([BoxesCol,upload],style={"margin-bottom":"40px"})

sz="30%"
img = html.Img(src="../assets/chigui.jpg",style={"width":sz,"height":sz,"margin-right":"12px"})

# Just a dummy placeholder to temporarily store df when loading
dumm_div = html.Div(id="df-load-placeholder")

Row = dbc.Row([BoxesCol,img,dumm_div])

component = dbc.Col([Row,DataTable.fig])
