import dash_html_components as html
import dash_core_components as dcc
from pages.utils import Header
import pandas as pd
import pathlib
import plotly.graph_objs as go

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

df_series = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Series.csv",sep=',')
df_series['Date'] = pd.to_datetime(df_series.Date, format = "%Y%m%d")

df_series['at_pdd'] = (df_series['Atraso']-df_series['Atraso_PDD'])/df_series['PL']
df_series['at'] = (df_series['Atraso_PDD'])/df_series['Atraso']

df_series['pdd_fat'] = df_series['Atraso_PDD']/df_series['Faturamento 30 Dias']

df_series['pdd_pl'] = (df_series['PDD 30 Dias']-df_series['Atraso_PDD'])/(df_series['PL']-df_series['Atraso'])

df_series['_21PDD'] = df_series['PDD 30 Dias'].pct_change(21)
df_series['_21ATR'] = df_series['Atraso'].pct_change(21)





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
                        [



                            html.Div(
                                [html.Div(id="atrpdd"),
                                    html.H6(
                                        "PDD sob PL",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="atpdd",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_series["Date"],
                                                    y=df_series['at_pdd'],
                                                    line={"color": "#56679d"},
                                                    mode="lines",
                                                    name="(Atraso-PDD)/PL",
                                                ),
                                                go.Scatter(
                                                    x=df_series["Date"],
                                                    y=df_series['at'],

                                                    line={"color": "#b5b5b5"},
                                                    mode="lines",
                                                    name="PDD/Atraso",
                                                    yaxis='y2'
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
                                                yaxis2=dict(

                                                    overlaying='y',
                                                    side='right',
                                                    linecolor='#b5b5b5',
                                                    linewidth=2

                                                ),

                                            ),
                                        },

                                    ),


                                ],
                                className="six columns",

                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "PDD sob Faturamento",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="pdd/fat",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_series["Date"],
                                                    y=df_series['at_pdd'],
                                                    line={"color": "#56679d"},
                                                    mode="lines",
                                                    name="PDD/Faturamento",
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
                                    )
                                ], className="six columns",
                            )
                        ],
                        className="row",
                        style={"margin-bottom": "35px"},
                    ),

                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Variação PDD e Atraso",
                                        className="subtitle padded",
                                    ),
                                    dcc.Graph(
                                        id="varpdd",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_series["Date"].iloc[21:],
                                                    y=df_series['_21PDD'].iloc[21:],
                                                    line={"color": "#56679d"},
                                                    mode="lines",
                                                    name="Var 1m PDD",
                                                ),
                                                go.Scatter(
                                                    x=df_series["Date"].iloc[21:],
                                                    y=df_series['_21ATR'].iloc[21:],

                                                    line={"color": "#b5b5b5"},
                                                    mode="lines",
                                                    name="Var 1M Atraso",
                                                    yaxis='y2'
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
                                                yaxis2=dict(

                                                    overlaying='y',
                                                    side='right',
                                                    linecolor='#b5b5b5',
                                                    linewidth=2

                                                ),

                                            ),
                                        },
                                        config={"displayModeBar": False},
                                    ),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="six columns",
                        style={"margin-bottom": "35px"},
                    ),
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
