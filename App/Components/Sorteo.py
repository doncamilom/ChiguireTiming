#! /usr/bin/env python3

from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import plotly.express as px
import pandas as pd

from Components import DataTable


box = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Button("Selección",id="sort-button",n_clicks=0),
                html.Div("Premio es para:"),
                html.Div("",id='output-random-name')]
        )
    ]
)

component = box

