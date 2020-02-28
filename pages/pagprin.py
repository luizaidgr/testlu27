import dash_core_components as dcc
import dash_html_components as html
from datetime import date
import dash
import datetime as dt
import pandas as pd
#df_series_pl['Date'] = pd.to_datetime(df_series_pl.Date, format = "%Y%m%d")
#reto_mes['Month'] = reto_mes.index.month
day=date.today().strftime("%Y-%m-%d")
colors = {
    'text': '#7FDBFF'}
def create_layout(app):
    return html.Div([ html.Div(id="ff"),
# represents the URL bar, doesn't render anything

    html.H1(children='Gerar Laminas',
            style={
                    'textAlign': 'center',

                   }
                   ),


    html.Div(id='dlinl1'),
        dcc.Dropdown(
            id='demo-dropdown',
            options=[

                {'label': 'ZEUS', 'value': '34691362000198'},
                {'label': 'FENIX', 'value': '26631527000108'},

            ],
            placeholder='selecione o fundo'),

        html.Div(id='datepickerr'),
            dcc.DatePickerSingle(
                id='datepicker',
                date=day,
                display_format='MMM Do, YY',


        ),
        html.Div(id='dlinl1link'),
        dcc.Link('SUBMIT', href='/gerarlamina'),
                      html.Div(id='lala')





])

