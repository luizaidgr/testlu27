# -*- coding: utf-8 -*-Messerschmitt
import os,sys
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from pages.utils import Header
from pages import callbackfidc,ret

import pandas as pd
import pathlib

# get relative data folder
cota = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_graph.csv',sep=',', index_col=0)
cdi = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/CDI.csv',sep=',', index_col=0)
cdi.index = pd.to_datetime(cdi.index, format='%m/%d/%Y')
cota.index = pd.to_datetime(cota.index, format='%Y%m%d')
cota.index = pd.to_datetime(cota.index)
df_series_pl3 = pd.DataFrame(columns=['Date', 'Cota', 'CDI'])
df_series_pl3['Date'] = cota.reset_index()['Date']
df_series_pl3['Cota'] = cota.reset_index()[list(cota.columns)[0]]
df_series_pl3['Cota'] = df_series_pl3['Cota'].apply(lambda x: (x/df_series_pl3.iloc[0,1])*100)

df_series_pl3['Date'] = pd.to_datetime(df_series_pl3.Date, format = "%Y%m%d")


df_series_pl3 = pd.merge_asof(df_series_pl3,cdi.reset_index().rename(columns={'index': 'Date'}), on='Date').drop(['CDI_x','CDI_y', 'SELIC'], 1)
df_series_pl3['CDI_ACUM'] = df_series_pl3['CDI_ACUM'].apply(lambda x: (x/df_series_pl3.iloc[0,2])*100)


reto_mes = ret.ret_mes(cota)
reto_ano = ret.ret_ano(cota)

reto_ano['Year'] = reto_ano.index.year
reto_mes['Year'] = reto_mes.index.year
reto_mes['Month'] = reto_mes.index.month


df_fund_facts = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_fund_facts.csv",sep=',')
df_price_perf = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela1.csv",sep=',')
df_price_perf=df_price_perf
dfinha=df_price_perf.iloc[:,0:2]
oi=dfinha.rename( columns={" .1":'value',' ':'label'})
dftudo=pd.concat([df_fund_facts,oi])
df_series_pl = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_PL.csv",sep=',')
df_series_yp = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_Y_P.csv",sep=',')
df_series_C_S = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_C_S.csv",sep=',')

df_series_pl['Date'] = pd.to_datetime(df_series_pl.Date, format = "%Y%m%d")


df_series_yp['Date'] = pd.to_datetime(df_series_yp.Date, format = "%Y%m%d")
df_series_C_S['Date'] = pd.to_datetime(df_series_C_S.Date, format = "%Y%m%d")


name = df_fund_facts.iloc[0,1]

df_series = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Series.csv",sep=',')
#df_series=df_series.drop([30],axis=0)
df_series['Date'] = pd.to_datetime(df_series.Date, format = "%Y%m%d")
data_hje = df_series['Date'].max().strftime('%d/%b/%Y')



def create_layout(app):
    # Page layouts
    return html.Div(
        [html.Div(id="oi"),
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Resumo do Produto"),
                                    html.Br([]),
                                    html.Div(id="mark",
                                             children=callbackfidc.algumacoisa(),
                                        style={"color": "#ffffff"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Caracteristicas"], className="subtitle padded"
                                    ),

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

                                ],
                                className="six columns",
                            ),

                            html.Div(
                                [html.H6(
                                        "PL do Fundo",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graph-2",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_series_pl["Date"],
                                                    y=df_series_pl["PL"],
                                                    line={"color": "#56679d"},
                                                    mode="lines",
                                                    name="PL",
                                                ),

                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=400,
                                                height=280,
                                                font={"family": "Raleway", "size": 10},
                                                margin={
                                                    "r": 30,
                                                    "t": 30,
                                                    "b": 30,
                                                    "l": 30,
                                                },
                                                showlegend=False,
                                                legend=dict(orientation="h"),
                                                titlefont={
                                                    "family": "Raleway",
                                                    "size": 10,
                                                },
                                                xaxis={
                                                    "autorange": True,
                                                    "range": [
                                                        "2019-01-01",
                                                        "2029-01-01",
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
                                                },
                                            ),
                                        },
                                        config={"displayModeBar": False},

                                    ),
                                    html.H6(
                                        "Rentabilidade",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="graphic-ret",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_series_pl3['Date'],
                                                    y=df_series_pl3['Cota'],
                                                    line={"color": "#56679d"},
                                                    mode="lines",
                                                    name="Fundo",
                                                ),
                                                go.Scatter(
                                                    x=df_series_pl3['Date'],
                                                    y=df_series_pl3['CDI_ACUM'],

                                                    line={"color": "#b5b5b5"},
                                                    mode="lines",
                                                    name="CDI",
                                                ),

                                            ],
                                            "layout": go.Layout(
                                                autosize=True,
                                                width=340,
                                                height=250,
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
                                        config={"displayModeBar": False})





                                ],
                                className="six columns",
                            ),


                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [



                                ],
                                    className="six columns",
                            ),
                                        html.Div(
                                            [

                                            ],
                                    className="six columns",
                            ),

                        ],
                        className="row ",
                    ),
                    #Row 6
                    html.Div(
                        [
                            html.Div(
                                [

                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Img(
                                                        src=app.get_asset_url("Selo-adesao-provisoria-Colorido-01.png"),
                                                        className="logo",
                                                    )
                                                ],
                                                className="three columns right-aligned",
                                            ),
                                            html.Div(
                                                [

                                                    html.P(
                                                        [
                                                            "As informações no presente material são exclusivamente informativas. Rentabilidade passada não representa garantia de rentabilidade futura. Ao investidor é recomendada a leitura cuidadosa do prospecto e do regulamento dos fundos de investimento ao aplicar seus recursos. Fundos de investimentos não contam com a garantia do administrador, do gestor, do consultor de crédito ou ainda do fundo garantidor de crédito - FGC. Este fundo utiliza títulos privados de crédito como parte integrante de sua política de investimento. Tal estratégia pode resultar em significativas perdas patrimoniais para seus cotistas. Para avaliação da performance de um FI, é recomendável uma análise de no mínimo doze meses. Lei o propsecto antes de aceitar a oferta."
                                                        ],
                                                        style={"color": "#7a7a7a", "fontSize": 9},
                                                    ),
                                                    html.Br([]),
                                                ],
                                                className="nine columns",
                                            ),
                                        ],
                                        className="row",
                                        style={

                                            "padding-bottom": "30px",
                                        },
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    )

                ],
                className="sub_page",
            ),
        ],
        className="page",
    )



