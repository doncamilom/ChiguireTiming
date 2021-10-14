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
b1 = dcc.Upload(html.Button("Subir archivo"),id="upload",multiple=False,style={"margin-left":"15px"})
upload_fb = html.Div("",id="upload-fb") # Feedback for upload button, in case load fails

# Include button for uploading preobtained results
spacing = "21px"
b2 = html.Button("CARGAR RESULTADOS PREVIOS",id="load-preobt",style={"margin-left":spacing})

# Include button for reseting last entered number
b3 = html.Button("Reset ultimo ingreso",id="go-back-one",style={"margin-left":spacing})


# Row for buttons
Butt_row = dbc.Row([b1,b2,b3])

# Create column with the rows of input boxes and the upload button
BoxesCol = dbc.Col(Rows,style={"margin-left":"0px","margin-bottom":"30px"})
BoxesCol = dbc.Col([BoxesCol,Butt_row],style={"margin-bottom":"40px"})

sz="30%"
img = html.Img(src="../assets/chigui.jpg",style={"width":sz,"height":sz,"margin-right":"12px"})

Row = dbc.Row([BoxesCol,img])

component = dbc.Col([Row,DataTable.fig])
