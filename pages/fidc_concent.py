# -*- coding: utf-8 -*-Messerschmitt
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from pages.utils import Header
import pandas as pd
import pathlib
import dash_table


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()



df_serie_psac = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_psac.csv', sep=',',encoding='utf-8')
df_serie_pced = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_pced.csv',sep=',',encoding='utf-8')
df_tabela_ced= pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela_ced.csv',sep=',',encoding='utf-8')
df_tabela_ced_at= pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela_ced_at.csv',sep=',',encoding='utf-8')
df_serie = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Series.csv',sep=',',encoding='utf-8')



df_serie_psac['Date'] = pd.to_datetime(df_serie_psac.Date, format = "%Y%m%d")
df_serie_pced['Date'] = pd.to_datetime(df_serie_pced.Date, format = "%Y%m%d")
df_serie['Date'] = pd.to_datetime(df_serie_pced.Date, format = "%Y%m%d")

V1 = df_tabela_ced_at["VALOR_NOMINAL"].to_numpy()




df_tabela_ced['Yield_hje'] = df_tabela_ced['Yield_hje'].apply('{:.2%}'.format)
df_tabela_ced['Dias_Hoje'] = df_tabela_ced['Dias_Hoje'].apply('{:20,.2f}'.format)
df_tabela_ced['VALOR_NOMINAL_Medio'] = df_tabela_ced['VALOR_NOMINAL_Medio'].apply('{:20,.2f}'.format)
df_tabela_ced['Atraso_pct'] = df_tabela_ced['Atraso_pct'].apply('{:.2%}'.format)
df_tabela_ced['PDD_pct'] = df_tabela_ced['PDD_pct'].apply('{:.2%}'.format)

df_teste = pd.DataFrame({'NOME_CEDENTE':['NOME CEDENTE'],
                         'Yield_hje': ['Yield Medio'],
                         'Dias_Hoje': ['Prazo Medio'],
                         'VALOR_NOMINAL_Medio':['Ticket Medio'],
                         'PDD_pct': ['PDD %'],
                         'Atraso_pct':['Atraso %'],
                         'Quantidade': ["Num Operações"]})
df_teste2 = df_teste.append(df_tabela_ced, ignore_index = True)[df_teste.columns.tolist()]

params = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril',
    'Maio', 'Junho', 'Julho', 'Agosto',
    'Setembro', 'Outubro', 'Novembro', 'Dezembro', ' ', 'Ano', 'Inicio'
]



def create_layout(app):
    # Page layouts
    return html.Div(
        [
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [

                    # Row 4
                    html.Div(
                        [html.Div(id="idcon"),
                            html.Div(
                                [
                                    html.H6(
                                        ["Visão geral:Cedentes"], className="subtitle padded"
                                    ),
                                    dash_table.DataTable(
                                        id='tableconc',
                                        columns=[{"name": i, "id": i} for i in df_teste2.columns],
                                        data=df_teste2.to_dict('records'),
                                        style_as_list_view=True,
                                        style_cell={'fontSize': 9, 'font-family': 'verdana'},
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
                                    ,

                                ],
                                className="row",

                            ),


                            html.Div(
                                [
                                    html.H6(
                                        ["Exposição Cedentes"], className="subtitle padded"
                                    ),
                                    dcc.Graph(id='pie',
                                              figure=go.Figure(
                                                  data=[go.Pie(labels=df_tabela_ced_at["NOME_CEDENTE"],
                                                               values=df_tabela_ced_at["VALOR_PRESENTE"])],
                                                  layout=go.Layout(
                                                      showlegend=False,
                                                      autosize=True,
                                                      width=340,
                                                      height=340,
                                                  )
                                              )),

                                ],
                                className="six columns",

                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Concentração de Sacado",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graphic-sac",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_serie_psac["Date"],
                                                    y=df_serie_psac["psac1"],
                                                    line={"color": "#56679d"},
                                                    mode="lines",
                                                    name="0% - 1%",
                                                ),
                                                go.Scatter(
                                                    x=df_serie_psac["Date"],
                                                    y=df_serie_psac["psac2"],

                                                    line={"color": "#b5b5b5"},
                                                    mode="lines",
                                                    name="1% - 10%",
                                                ),
                                                go.Scatter(
                                                    x=df_serie_psac["Date"],
                                                    y=df_serie_psac["psac3"],
                                                    line={"color": "#000b2e"},
                                                    mode="lines",
                                                    name="11% - 30%",
                                                ),
                                                go.Scatter(
                                                    x=df_serie_psac["Date"],
                                                    y=df_serie_psac["psac4"],

                                                    line={"color": "#82a0ff"},
                                                    mode="lines",
                                                    name="31% - 100%",
                                                ),
                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=340,
                                                height=300,
                                                font={"family": "Raleway", "size": 10},
                                                margin={
                                                    "r": 30,
                                                    "t": 30,
                                                    "b": 30,
                                                    "l": 30,
                                                },
                                                showlegend=True,
                                                legend=dict(orientation="h"),
                                                titlefont={
                                                    "family": "Raleway",
                                                    "size": 10,
                                                },
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        "2019-09-01",
                                                        "2020-01-01",
                                                    ],
                                                    "rangeselector": {
                                                        "buttons": [
                                                            {
                                                                "count": 1,
                                                                "label": "1Y",
                                                                "step": "year",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 3,
                                                                "label": "3Y",
                                                                "step": "year",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "count": 5,
                                                                "label": "5Y",
                                                                "step": "year",
                                                            },
                                                            {
                                                                "count": 10,
                                                                "label": "10Y",
                                                                "step": "year",
                                                                "stepmode": "backward",
                                                            },
                                                            {
                                                                "label": "All",
                                                                "step": "all",
                                                            },
                                                        ]
                                                    },
                                                    "showline": True,
                                                    "type": "date",
                                                    "zeroline": False,
                                                },
                                                yaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        18.6880162434,
                                                        278.431996757,
                                                    ],
                                                    "showline": True,
                                                    "type": "linear",
                                                    "zeroline": False,
                                                    "linecolor": '#56679d',
                                                    "linewidth": 2,
                                                },

                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5

                    # Row 6
                    html.Div(
                        [
                            html.Div(
                                [






                                ],
                                    className="six columns",
                            ),

                        ],
                        className="six columns",
                    ),


                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
