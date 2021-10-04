#! /usr/bin/env python3

from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import plotly.express as px
import pandas as pd

from Components import DataTable


InputBox = dcc.Input(id='InputBox',placeholder='Numero de participante', n_submit=1, 
                        value="", className='div-inputbox',
                        style={"margin-bottom":"50px",
                               "margin-top":"40px"})

box2 = dbc.Card(
    [
        dbc.CardBody(
        [html.Div('Se aproxima participante número:',className="box-right-text"),
         html.Div('',id='OutBox', className="bigTitles"),
        ])
    ],
    className="box-right",
    style={"margin-top":"40px"})

#box21 = dbc.Card(
#    [
#        dbc.CardBody(
#            [html.Div('Pulse INICIAR para iniciar el contador',id='start_butt_text'),
#             html.Button('INICIAR',id='start_button',n_clicks=0)
#             ]
#        )
#    ]
#)

Col1 = dbc.Col([InputBox],width='6')
Col2 = dbc.Col([box2],width='6')
#Col3 = dbc.Col([box21],width='3')

component1 = dbc.Row([Col1,Col2])


## Next row

box3 = dbc.Card(
    [
        dbc.CardBody(
        [html.Div(id='RunnerList')]
        )
    ]
)
box4 = dbc.Card(
    [
        dbc.CardBody(
        [html.Div(id='some-log')]
        )
    ]
)

## New row for the whole table with results

component2 = dbc.Row([dbc.Col(box3),dbc.Col(box4)])

component = dbc.Col([component1,DataTable.fig])

