#! /usr/bin/env python3

from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import plotly.express as px
import pandas as pd

from Components import MainTable


InputBox = dbc.Card(
    [
        dbc.CardBody(
        [html.Div(
            dcc.Input(id='InputBox2',placeholder='Numero de participante', n_submit=0, value=""),
            className='div-inputbox'
                )]
        ),
    ],
)

Col1 = dbc.Col([InputBox],width='6')

box4 = dbc.Card(
    [
        dbc.CardBody(
        [html.Div(id='some-log2')]
        )
    ]
)

## New row for the whole table with results


component = dbc.Row([Col1,dbc.Col(box4)])


