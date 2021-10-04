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
from numpy import isnan,random
from time import time
from datetime import datetime, timedelta

from Components import Crosscountry, LoadData, Sorteo

#Create the app
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP]) #USING BOOTSTRAP'S CSS LIBRARY


Crosscountry = dbc.Card(
            dbc.CardBody(
                [Crosscountry.component],
                        ), className='mainPage-card'
                  )

Formato2 = dbc.Card(
            dbc.CardBody(
                [Sorteo.component],
                        )
                  )
tabs = dbc.Tabs(
    [
        dcc.Tab(Crosscountry, label="Crosscountry"),
        dbc.Tab(Formato2, label="Sorteo"),
    ],
    className="header",
)

app.layout =  html.Div([tabs])



###################################################### Callbacks ###################################################


## Update text box so it shows what you're writing
@app.callback(
    Output("OutBox","children"),
    [Input("InputBox","value")]
)
def write(*vals):
    return vals

@app.callback(
    Output("output-random-name","children"),
    [Input("sort-button","n_clicks")],
    [State('mainTable','data')]
)
def sorteo(n_clicks,data):
    df = pd.DataFrame(data)
    if n_clicks>0:   
        number = random.choice(df["NÚMERO"])
        name = df.loc[df["NÚMERO"]==number,"NOMBRE"].values[0]
        return f"{name} con número {number}"

    

## Submit runner time when hiting Enter
#global runner_list
#runner_list = []

#@app.callback(
#    Output('some-log','children'),
#    [Input("InputBox","n_submit"),],
#    [State('InputBox','value')]
#)
#def submit_runner(n_submit,value):
#    if value not in runner_list:
#        runner_list.append(value)
#    return value

## Clear text box when submitting runner
@app.callback(
    Output('InputBox','value'),
    [Input("InputBox","n_submit"),],
)
def submit_runner(n_submit):
    return ""

## Present time of runner when they are submitted
#@app.callback(
#    Output('RunnerList','children'),
#    [Input("InputBox","n_submit"),Input('start_button','n_clicks')],
#    [State('InputBox','value')]
#)
#def text_submit_runner(clk_runner,n_clicks,value):
#    if n_clicks==0 and clk_runner>0: # If runner submited without starting race
#        return 'No has comenzado a contar el tiempo!!'
#    
#    if n_clicks==1 and clk_runner>0:
#        dt = datetime.now()
#        return "Participante {0} llega el {1} a las {2}".format(value,dt.date(),dt.time())
#
#    if n_clicks==2 and clk_runner>0:
#        return 'Ya se acabó la carrera!'


## Change START button description when clicking on it
#@app.callback(
#    Output('start_butt_text','children'),
#    [Input('start_button','n_clicks')],
#    [State('start_butt_text','children')]
#)
#def timer_text(n_clicks,value):
#    if n_clicks==0:
#        return 'Pulse INICIAR para iniciar el contador'
#    if n_clicks==1:  
#        t0 = time() # Start counting time
#        return 'CORRIENDO. Pulse el botón para terminar.'
#    if n_clicks>=2:
#        return 'CARRERA TERMINADA'

## Change START button text when click
#@app.callback(
#    Output('start_button','children'),
#    [Input('start_button','n_clicks')],
#    [State('start_butt_text','children')]
#)
#def timer_button(n_clicks,value):
#    if n_clicks==0:
#        return 'INICIAR'
#    if n_clicks==1:  
#        return 'TERMINAR'
#    if n_clicks>=2:
#        return ':)'


## When hitting START, reset n_submit 
#@app.callback(
#    Output('InputBox','n_submit'),
#    [Input('start_button','n_clicks')],
#    [State('InputBox','n_submit')]
#)
#def timer_text(n_clicks,curr_n_submit):
#    # If not clicked, or clicked once, reset whatever value was set on n_submit
#    if n_clicks==1 or n_clicks==0:        return 0  
#    # Else, just leave it as it was
#    if n_clicks>=2:   return curr_n_submit

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
    if val == None or val not in df['NÚMERO'].values: return data

    # If a runner has a time already, don't change it's time again
    curr_time_val = df.loc[df['NÚMERO'] == val,'HORA LLEGADA'].values[0]
    if curr_time_val is None:
        df.loc[df['NÚMERO'] == val,'HORA LLEGADA'] = datetime.now()

    df['HORA LLEGADA'] = pd.to_datetime(df['HORA LLEGADA']).dt.round('1s')
    df['HORA SALIDA'] = pd.to_datetime(df['HORA SALIDA'])

    # Calculate total time spent for those runners that already crossed the line
    # And convert to a nice hh:mm:ss format
    df['TOTAL'] = ((df['HORA LLEGADA'] - df['HORA SALIDA'])
                            .dt
                            .seconds
                            .apply(lambda x: str(timedelta(seconds=x)) if ~isnan(x) else None))

    df['HORA LLEGADA'] = df['HORA LLEGADA'].dt.time 
    df['HORA SALIDA'] = df['HORA SALIDA'].dt.time 

    # Now calc. time difference from first place by category

    # Calc. position within each category
    for cat in df['CATEGORIA'].unique():
        df.loc[df['CATEGORIA']==cat,'POSICIÓN'] = df.loc[df['CATEGORIA']==cat,'TOTAL'].rank()
    

    df = df.sort_values('TOTAL')
    
    # Write to file as new entries come, so data isn't lost
    with pd.ExcelWriter('Data/Results.xlsx', engine='xlsxwriter') as writer:
        for cat in df['CATEGORIA'].unique():
            df[df['CATEGORIA']==cat].to_excel(writer,sheet_name=cat[:30],index=False)
    

    return df.to_dict('records')



### TODO write to a file each time a new entry arrives
### make the script try to load the partially filled database, in case it exists.
###      That way we can restart an unfinished race in case the program crashes or whatever

### TODO: make a tab for each possible type of race

### TODO: text to voice: Name, number, time, delta time from first place, etc. as runner goes through goal


###################################################### Run app server ###################################################    
    
if __name__ == "__main__":
    app.run_server(debug=True)
