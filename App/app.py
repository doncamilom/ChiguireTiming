#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ClientsideFunction

import plotly.express as px
import plotly.graph_objects as go 
import os

import pandas as pd
from time import time
from datetime import datetime

from Components import MainPage, LoadData, SecondaryPage

#Create the app
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP]) #USING BOOTSTRAP'S CSS LIBRARY


Crosscountry = dbc.Card(
            dbc.CardBody(
                [MainPage.component],
                        )
                  )

Formato2 = dbc.Card(
            dbc.CardBody(
                [SecondaryPage.component],
                        )
                  )
tabs = dbc.Tabs(
    [
        dbc.Tab(Crosscountry, label="Crosscountry"),
        dbc.Tab(Formato2, label="Otro formato holi"),
    ],
    className="header",
)

title = dbc.Container([ html.H1("CARRERITAS", className="ml-3 mt-3")])  #,html.Hr()])
app.layout =  html.Div([tabs])



###################################################### Callbacks ###################################################


## Update text box so it shows what you're writing
@app.callback(
    Output("OutBox","children"),
    [Input("InputBox","value")]
)
def write(*vals):
    return vals

## Submit runner time when hiting Enter
global runner_list
runner_list = []

@app.callback(
    Output('some-log','children'),
    [Input("InputBox","n_submit"),],
    [State('InputBox','value')]
)
def submit_runner(n_submit,value):
    if value not in runner_list:
        runner_list.append(value)
    return value

## Clear text box when submitting runner
@app.callback(
    Output('InputBox','value'),
    [Input("InputBox","n_submit"),],
)
def submit_runner(n_submit):
    return ""

## Present time of runner when they are submitted
@app.callback(
    Output('RunnerList','children'),
    [Input("InputBox","n_submit"),Input('start_button','n_clicks')],
    [State('InputBox','value')]
)
def text_submit_runner(clk_runner,n_clicks,value):
    if n_clicks==0 and clk_runner>0: # If runner submited without starting race
        return 'No has comenzado a contar el tiempo!!'
    
    if n_clicks==1 and clk_runner>0:
        dt = datetime.now()
        return "Participante {0} llega el {1} a las {2}".format(value,dt.date(),dt.time())

    if n_clicks==2 and clk_runner>0:
        return 'Ya se acabó la carrera!'


## Change START button description when clicking on it
@app.callback(
    Output('start_butt_text','children'),
    [Input('start_button','n_clicks')],
    [State('start_butt_text','children')]
)
def timer_text(n_clicks,value):
    if n_clicks==0:
        return 'Pulse INICIAR para iniciar el contador'
    if n_clicks==1:  
        t0 = time() # Start counting time
        return 'CORRIENDO. Pulse el botón para terminar.'
    if n_clicks>=2:
        return 'CARRERA TERMINADA'

## Change START button text when click
@app.callback(
    Output('start_button','children'),
    [Input('start_button','n_clicks')],
    [State('start_butt_text','children')]
)
def timer_button(n_clicks,value):
    if n_clicks==0:
        return 'INICIAR'
    if n_clicks==1:  
        return 'TERMINAR'
    if n_clicks>=2:
        return ':)'


## When hitting START, reset n_submit 
@app.callback(
    Output('InputBox','n_submit'),
    [Input('start_button','n_clicks')],
    [State('InputBox','n_submit')]
)
def timer_text(n_clicks,curr_n_submit):
    # If not clicked, or clicked once, reset whatever value was set on n_submit
    if n_clicks==1 or n_clicks==0:        return 0  
    # Else, just leave it as it was
    if n_clicks>=2:   return curr_n_submit

############### Callbacks for updating the table

from numpy import nan
### Update values on the dataframe and re-sort
@app.callback(
    Output('mainTable','data'),
    [Input("InputBox","n_submit")],
    [State('mainTable','data'),State('InputBox','value')]
)

def update_dataframe(n_submit, data, value):
    df = pd.DataFrame(data)
    try:        val = int(value)  # If there's a number in InputBox (and n_submit was activated)
    except:     val = None
    if val == None or val not in df['Numero'].values: return data

    # If a runner has a time already, don't change it's time again
    curr_time_val = df.loc[df['Numero'] == val,'Hora de llegada'].values[0]
    if curr_time_val is None:
        df.loc[df['Numero'] == val,'Hora de llegada'] = datetime.now()

    df['Hora de llegada'] = pd.to_datetime(df['Hora de llegada'])
    df['Hora de salida'] = pd.to_datetime(df['Hora de salida'])

    # Calculate total time spent for those runners that already crossed the line
    df['Tiempo de carrera'] = (df['Hora de llegada'] - df['Hora de salida'])

    df['Tiempo de carrera'] = df['Tiempo de carrera'].dt.seconds

    df['Hora de llegada'] = df['Hora de llegada'].dt.time 
    df['Hora de salida'] = df['Hora de salida'].dt.time 


    # Now calc. time difference from first place by category
    

    df = df.sort_values('Tiempo de carrera')
    
    # Write to file as new entries come, so data isn't lost
    

    return df.to_dict('records')



### TODO write to a file each time a new entry arrives
### make the script try to load the partially filled database, in case it exists.
###      That way we can restart an unfinished race in case the program crashes or whatever

### TODO: make a tab for each possible type of race

### TODO: text to voice: Name, number, time, delta time from first place, etc. as runner goes through goal


###################################################### Run app server ###################################################    
    
if __name__ == "__main__":
    app.run_server(debug=True)
