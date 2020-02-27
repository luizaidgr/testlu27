import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
#from Laminas_Comercial import fidcv1,pag_prin
#from Laminas import help
#from Laminas import fidc_concent,fidc_eventos
#from Laminas import fidc_perf
import plotly.graph_objs as go
from datetime import date
import pathlib
#from FIDC import callback_fidc
from datetime import datetime
#from Laminas import ret
import pandas as pd
import flask
day=date.today().strftime("%Y-%m-%d")
from flask import Flask
df_fund_facts = pd.read_csv("C:\\Users\\Hemerson de Villa\\Desktop\\lop\\static\\data\\df_fund_facts.csv")

server = flask.Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,server=server, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True
app.layout =html.Div([dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df_fund_facts.columns],
        data=df_fund_facts.to_dict('records'),
        style_as_list_view=True,
        style_cell={'fontSize': 12.5, 'font-family': 'calibri'},
        style_header={'backgroundColor': 'white',
                      'color': 'white',
                      'border': 'white'},
        style_cell_conditional=[
            {

                'textAlign': 'left'
            }
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }],
        style_header_conditional=None
    )
    ])

server = app.server

@server.route('/')
def create_layout(app):
    return html.Div([
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df_fund_facts.columns],
        data=df_fund_facts.to_dict('records'),
        style_as_list_view=True,
        style_cell={'fontSize': 12.5, 'font-family': 'calibri'},
        style_header={'backgroundColor': 'white',
                      'color': 'white',
                      'border': 'white'},
        style_cell_conditional=[
            {

                'textAlign': 'left'
            }
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }],
        style_header_conditional=None
    )
    ])

if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_hot_reload=True)