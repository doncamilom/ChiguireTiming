#!/usr/bin/env python3

import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ClientsideFunction

import plotly.express as px
import plotly.graph_objects as go 
import pandas as pd
import os

from Components import InputVals
from time import time

#Create the app
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP]) #USING BOOTSTRAP'S CSS LIBRARY


content = dbc.Card(
            dbc.CardBody(
                [InputVals.component]
                        )
                  )

tabs = dbc.Tabs(
    [
        dbc.Tab(content, label="Entrada de datos"),
    ],
    className="header",
)

title = dbc.Container([ html.H1("CARRERITAS", className="ml-3 mt-3")])  #,html.Hr()])
app.layout =  html.Div([tabs])


###################################################### Callbacks ###################################################

global t0
t0 = 0

## Update text box so it shows what you're writing
@app.callback(
    Output("OutBox","children"),
    [Input("InputBox","value")]
)
def write(*vals):
    return vals

## Submit runner time when clicking SUBMIT button
global runner_list
runner_list = []

@app.callback(
    Output('some-log','children'),
    [Input("submit-runner","n_clicks"),],
    [State('InputBox','value')]
)
def submit_runner(n_clicks,value):
    if value not in runner_list:
        runner_list.append(value)
    return value

## Present time of runner when they are submitted
@app.callback(
    Output('RunnerList','children'),
    [Input("submit-runner","n_clicks"),Input('start_button','n_clicks')],
    [State('InputBox','value')]
)
def text_submit_runner(clk_runner,n_clicks,value):
    if n_clicks==0 and clk_runner>0: # If runner submited without starting race
        return 'No has comenzado a contar el tiempo!!'
    
    if n_clicks==1 and clk_runner>0:
        t = time()-t0
        return "Tiempo para corredor/a {0}: {1:.0f}h {2:.0f}m {3:.2f}s.".format(value, t//3600,(t%3600)//60,t%60 )

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
        print()
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
        t0 = time()# Start time counter
        return 'TERMINAR'
    if n_clicks>=2:
        return ':)'





###################################################### Run app server ###################################################    
    
if __name__ == "__main__":
    app.run_server(debug=True)
