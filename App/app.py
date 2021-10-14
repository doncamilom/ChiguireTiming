#!/usr/bin/env python3

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State, ClientsideFunction

import plotly.express as px
import plotly.graph_objects as go 
import base64
import os
import io

import pandas as pd
from numpy import isnan,random,nan
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

### Update values on the dataframe and re-sort

@app.callback(
    Output('mainTable','data'),
    [Input(f"InputBox_{box}","n_submit") for box in range(NumBoxes)] + [Input("upload","contents"), 
         Input("upload","filename"), Input("load-preobt","n_clicks"),
         Input("go-back-one","n_clicks")],

    [State('mainTable','data')] + [State(f'InputBox_{box}','value') for box in range(NumBoxes)]
)
def update_dataframe(*vals):
    n_extra_inps = len(vals) - NumBoxes*2 - 1

    ## First to do: when Upload button is activated
    ctx_trig = dash.callback_context.triggered
    filename = vals[NumBoxes+1]

    # Upload datafile when upload button is activated
    if ctx_trig[0]["prop_id"] == "upload.contents":
        contents = ctx_trig[0]["value"]
        content_str = contents.split(",")[1]
        decoded = base64.b64decode(content_str)
        try: # In case user selects a non-excel file, do nothing!
            if 'xls' in filename:
                df = LoadData.LoadData(io.BytesIO(decoded))
                return df.to_dict("records")
        except: pass
            
    # Load saved results file (in case of refresh to stop loss of data)
    if ctx_trig[0]["prop_id"] == "load-preobt.n_clicks":
        return LoadData.LoadPrerecordedResults()[0].to_dict("records")    

    data = vals[NumBoxes+n_extra_inps] # Data is the input in the middle of the list
    df = pd.DataFrame(data)

    # Remove entered timings for last runner entered (in case of missentered number)
    if ctx_trig[0]["prop_id"] == "go-back-one.n_clicks":
        # Select entry with max HORA LLEGADA and reset entered data for that person.
        df["HORA LLEGADA"] = pd.to_datetime(df["HORA LLEGADA"])

        max_dt = df["HORA LLEGADA"].max()
        df.loc[df["HORA LLEGADA"]==max_dt,["HORA LLEGADA","TOTAL","POSICIÓN"]] = nan 
    
        df['HORA LLEGADA'] = df['HORA LLEGADA'].dt.time 
        return df.sort_values("TOTAL").to_dict("records")


    ############################
    # Input data through boxes #
    ############################

    # Tell which Input box was activated
    if ctx_trig: # If there's an activation
        activd_b = int(ctx_trig[0]['prop_id'].split("_")[1].split(".")[0])
    else:     return data

    value = vals[NumBoxes+1+n_extra_inps+activd_b] # Select the value inside the InputBox that was triggered

    try:        val = int(value)  # If there's a number in InputBox (and n_submit was activated)
    except:     val = None
    if val == None or val not in df['NÚMERO'].values: return data

    # If a runner has a time already, don't change it's time again
    curr_time_val = df.loc[df['NÚMERO'] == val,'HORA LLEGADA'].values[0]
    if curr_time_val is None:
        df.loc[df['NÚMERO'] == val,'HORA LLEGADA'] = datetime.now()

    df['HORA LLEGADA'] = pd.to_datetime(df['HORA LLEGADA']).dt.round('10ms')
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



### TODO: make a tab for each type of race
### TODO: text to voice: Name, number, time, delta time from first place, etc. as runner goes through goal

###################################################### Run app server ###################################################    
    
if __name__ == "__main__":
    app.run_server(debug=True)
