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

from Components import Cronoescalada, LoadData, Sorteo

#Create the app
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP]) #USING BOOTSTRAP'S CSS LIBRARY

NumBoxes = Cronoescalada.numBoxes
Cronoescalada = dbc.Card(
            dbc.CardBody(
                [Cronoescalada.component],
                        ), className='mainPage-card'
                  )

Formato2 = dbc.Card(
            dbc.CardBody(
                [Sorteo.component],
                        )
                  )
tabs = dbc.Tabs(
    [
        dcc.Tab(Cronoescalada, label="Cronoescalada"),
        dbc.Tab(Formato2, label="Sorteo"),
    ],
    className="header",
)

app.layout =  html.Div([tabs])



###################################################### Callbacks ###################################################


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

    
## Clear text box when submitting runner
for box in range(NumBoxes):
    @app.callback(
        Output(f'InputBox_{box}','value'),
        [Input(f"InputBox_{box}","n_submit"),],
        [State(f"InputBox_{box}","value")]
    )
    def submit_runner(n_submit,curr_val):
        ctx = dash.callback_context
        # Tell which Input box was activated
        if ctx.triggered: 
            # Check if box {box} is the one that was activated
            is_this_box = ctx.triggered[0]['prop_id'].split(".")[0] == f"InputBox_{box}"
            if is_this_box: return ""  # If so, clear its value
        else:     return curr_val      # Else, return same value



############### Callbacks for updating the table
from numpy import nan

### Update values on the dataframe and re-sort

@app.callback(
    Output('mainTable','data'),
    [Input(f"InputBox_{box}","n_submit") for box in range(NumBoxes)],
    [State('mainTable','data'),*[State(f'InputBox_{box}','value') for box in range(NumBoxes)]]
)
def update_dataframe(*vals):
    data = vals[NumBoxes] # Data is the input in the middle of the list

    ctx = dash.callback_context
    # Tell which Input box was activated
    if ctx.triggered: # If there's an activation
        activd_b = int(ctx.triggered[0]['prop_id'].split("_")[1].split(".")[0])
    else:     return data

    value = vals[NumBoxes+1+activd_b] # Select the value inside the InputBox that was triggered

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




### make the script try to load the partially filled database, in case it exists.
###      That way we can restart an unfinished race in case the program crashes or whatever

### TODO: make a tab for each possible type of race

### TODO: text to voice: Name, number, time, delta time from first place, etc. as runner goes through goal


###################################################### Run app server ###################################################    
    
if __name__ == "__main__":
    app.run_server(debug=True)
