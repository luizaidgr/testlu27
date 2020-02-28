import pandas as pd
import pathlib
import plotly.graph_objs as go
import dash_table
import dash_core_components as dcc
from datetime import date
from pages import ret
from App.Laminas.FIDC import FIDC_Estoques

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../FIDC/data").resolve()

def fund_facts():
    df_fund_facts = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_fund_facts.csv",sep=',')
    return df_fund_facts

def price_perf():
    df_price_perf = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela1.csv",sep=',')
    return df_price_perf
def series_pl():
    df_series_pl = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_PL.csv",sep=',')
    return df_series_pl
def resumo():
    resumo = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/text_resumo.csv",sep=',').iloc[0,0]
    return resumo
def graph_lamina2():
    df_series_pl=series_pl()

    df_series_pl['Date'] = pd.to_datetime(df_series_pl.Date, format="%Y%m%d")
    figure = dcc.Graph(
        id="graph_lamina2",
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
                width=340,
                height=200,
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
    )
    return figure

def nome_fundo():
    dfund_facts= fund_facts()
    nome = dfund_facts.iloc[0, 1]
    return nome

def data_hje():
    df_series = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Series.csv",sep=',')
    df_series['Date'] = pd.to_datetime(df_series.Date, format="%Y%m%d")
    data_hje = df_series['Date'].max().strftime('%d/%b/%Y')
    return data_hje

def cedentes():
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../FIDC/data").resolve()
    df_tabela_ced = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela_ced.csv",sep=',')
    df_tabela_ced['Yield_hje'] = df_tabela_ced['Yield_hje'].apply('{:.2%}'.format)
    df_tabela_ced['Dias_Hoje'] = df_tabela_ced['Dias_Hoje'].apply('{:20,.2f}'.format)
    df_tabela_ced['VALOR_NOMINAL_Medio'] = df_tabela_ced['VALOR_NOMINAL_Medio'].apply('{:20,.2f}'.format)
    df_tabela_ced['Atraso_pct'] = df_tabela_ced['Atraso_pct'].apply('{:.2%}'.format)
    df_tabela_ced['PDD_pct'] = df_tabela_ced['PDD_pct'].apply('{:.2%}'.format)

    df_teste = pd.DataFrame({'NOME_CEDENTE': ['NOME CEDENTE'],
                             'Yield_hje': ['Yield Medio'],
                             'Dias_Hoje': ['Prazo Medio'],
                             'VALOR_NOMINAL_Medio': ['Ticket Medio'],
                             'PDD_pct': ['PDD %'],
                             'Atraso_pct': ['Atraso %'],
                             'Quantidade': ["Num Operações"]})
    df_teste2 = df_teste.append(df_tabela_ced, ignore_index=True)[df_teste.columns.tolist()]

    tabela = dash_table.DataTable(
        id='cedentes_tabela',
        columns=[{"name": i, "id": i} for i in df_teste2.head(10).columns],
        data=df_teste2.head(10).to_dict('records'),
        style_as_list_view=True,
        style_cell={'fontSize': 13, 'font-family': 'calibri'},
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
    return tabela

def cedentes_pie():
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../FIDC/data").resolve()
    df_tabela_ced_at = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela_ced_at.csv",sep=',')
    pie = dcc.Graph(id='cedentes_pie',
                                              figure=go.Figure(
                                                  data=[go.Pie(labels=df_tabela_ced_at["NOME_CEDENTE"],
                                                               values=df_tabela_ced_at["VALOR_PRESENTE"])],
                                                  layout=go.Layout(
                                                      showlegend=False,
                                                      autosize=True,
                                                      width=340,
                                                      height=340,
                                                  )
                                              ))

    return pie

def sacado_conc():
    df_serie_psac = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_psac.csv",sep=',')


    df_serie_psac['Date'] = pd.to_datetime(df_serie_psac.Date, format="%Y%m%d")



    graph = dcc.Graph(
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
    )

    return graph

def yield_prazo():
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../FIDC/data").resolve()
    df_series_yp = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_Y_P.csv",sep=',')
    df_series_yp['Date'] = pd.to_datetime(df_series_yp.Date, format="%Y%m%d")
    yield_prazo = dcc.Graph(
        id="graph-1_y_p",
        figure={
            "data": [
                go.Scatter(
                    x=df_series_yp["Date"],
                    y=df_series_yp["Yield_Medio"],
                    line={"color": "#56679d"},
                    mode="lines",
                    name="Yield Medio",
                ),
                go.Scatter(
                    x=df_series_yp["Date"],
                    y=df_series_yp[
                        "Prazo_Medio"
                    ],
                    line={"color": "#b5b5b5"},
                    mode="lines",
                    name="Prazo Medio",
                    yaxis='y2'
                ),
            ],
            "layout": go.Layout(
                autosize=True,
                width=340,
                height=280,
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
    )
    return yield_prazo

def ret_graph():
    cota = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_graph.csv',sep=',', index_col=0)
    cota.index = pd.to_datetime(cota.index, format='%Y%m%d')
    cdi = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/CDI.csv',sep=',', index_col=0)
    cdi.index = pd.to_datetime(cdi.index)




    cota.index = pd.to_datetime(cota.index)
    df_series_pl3 = pd.DataFrame(columns=['Date', 'Cota', 'CDI'])
    df_series_pl3['Date'] = cota.reset_index()['Date']
    df_series_pl3['Cota'] = cota.reset_index()[list(cota.columns)[0]]
    df_series_pl3['Cota'] = df_series_pl3['Cota'].apply(lambda x: (x / df_series_pl3.iloc[0, 1]) * 100)

    df_series_pl3['Date'] = pd.to_datetime(df_series_pl3.Date, format="%Y%m%d")

    df_series_pl3 = pd.merge_asof(df_series_pl3, cdi.reset_index().rename(columns={'index': 'Date'}), on='Date').drop(
        ['CDI_x', 'CDI_y', 'SELIC'], 1)
    df_series_pl3['CDI_ACUM'] = df_series_pl3['CDI_ACUM'].apply(lambda x: (x / df_series_pl3.iloc[0, 2]) * 100)

    graph = dcc.Graph(
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
                height=280,
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
    return graph

def atraso_pdd():
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../FIDC/data").resolve()

    df_series = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Series.csv",sep=',')

    df_series['Date'] = pd.to_datetime(df_series.Date, format="%Y%m%d")
    df_series['at'] = (df_series['Atraso_PDD']) / df_series['Atraso']
    df_series['at_pdd'] = (df_series['Atraso'] - df_series['Atraso_PDD']) / df_series['PL']

    atraso_pdd = dcc.Graph(
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

    )
    return atraso_pdd

def pdd_fat():
    DATA_PATH = PATH.joinpath("../FIDC/data").resolve()

    df_series = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Series.csv",sep=',')
    df_series['Date'] = pd.to_datetime(df_series.Date, format="%Y%m%d")

    df_series['at_pdd'] = (df_series['Atraso'] - df_series['Atraso_PDD']) / df_series['PL']

    chart=  dcc.Graph(
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

    return chart

def varpdd():
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../FIDC/data").resolve()

    df_series = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Series.csv",sep=',')
    df_series['Date'] = pd.to_datetime(df_series.Date, format="%Y%m%d")

    df_series['_21PDD'] = df_series['PDD 30 Dias'].pct_change(21)
    df_series['_21ATR'] = df_series['Atraso'].pct_change(21)
    chart =  dcc.Graph(
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
            )
    return chart

def pddpl():
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../FIDC/data").resolve()

    df_series = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Series.csv",sep=',')
    df_series['Date'] = pd.to_datetime(df_series.Date, format="%Y%m%d")
    df_series['pdd_pl'] = (df_series['PDD 30 Dias'] - df_series['Atraso_PDD']) / (df_series['PL'] - df_series['Atraso'])

    chart = dcc.Graph(
        id="pddpl",
        figure={
            "data": [
                go.Scatter(
                    x=df_series['Date'],
                    y=df_series['pdd_pl'],
                    line={"color": "#56679d"},
                    mode="lines",
                    name="PDDn/PLn",
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
    return chart

def update_table(value=date.today().year):
    cota = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_graph.csv',sep=',', index_col=0)
    cota.index = pd.to_datetime(cota.index, format='%Y%m%d')

    if value> cota.index[-1].year:
        value = cota.index[-1].year


    reto_mes = ret.ret_mes(cota)
    reto_ano = ret.ret_ano(cota)

    reto_ano['Year'] = reto_ano.index.year
    reto_mes['Year'] = reto_mes.index.year
    reto_mes['Month'] = reto_mes.index.month

    YY = reto_ano['Year']


    Year = value

    params = [str(Year),
              'Jan', 'Fev', 'Mar', 'Abr',
              'Mai', 'Jun', 'Jul', 'Ago',
              'Set', 'Out', 'Nov', 'Dez', 'Ano', 'Inicio']

    ret_y = reto_ano.loc[reto_ano['Year'] == Year].drop('Year', 1)
    ret_y['pct_cdi'] = ret_y[list(cota.columns)[0]] / ret_y['CDI_ACUM']

    ret_m = reto_mes.loc[reto_mes['Year'] == Year].drop('Year', 1)
    ret_m['pct_cdi'] = ret_m[list(cota.columns)[0]] / ret_m['CDI_ACUM']
    ret_m = ret_m.set_index('Month')

    # completar meses vazils
    j = ret_m.index.max()
    i = j
    j = j + 1
    for x in range(12 - i):
        ret_m.loc[j] = 0
        j = j + 1

    if ret_m.index.min() != 1:
        for x in range(ret_m.index.min() - 1):
            ret_m.loc[x + 1] = 0

    ret_ini = ret.ret_ini(cota, Year)-1
    ret_ini['pct_cdi'] = ret_ini[list(cota.columns)[0]] / ret_ini['CDI_ACUM']

    Table = ret_m.T
    Table['Ano'] = ret_y.T
    Table['Inicio'] = ret_ini.T
    Table = Table.rename(
        columns={1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out',
                 11: 'Nov', 12: 'Dez'})
    Table['Jan'] = Table['Jan'].apply('{:.2%}'.format)
    Table['Fev'] = Table['Fev'].apply('{:.2%}'.format)
    Table['Mar'] = Table['Mar'].apply('{:.2%}'.format)
    Table['Abr'] = Table['Abr'].apply('{:.2%}'.format)
    Table['Mai'] = Table['Mai'].apply('{:.2%}'.format)
    Table['Jun'] = Table['Jun'].apply('{:.2%}'.format)
    Table['Jul'] = Table['Jul'].apply('{:.2%}'.format)
    Table['Ago'] = Table['Ago'].apply('{:.2%}'.format)
    Table['Set'] = Table['Set'].apply('{:.2%}'.format)
    Table['Out'] = Table['Out'].apply('{:.2%}'.format)
    Table['Nov'] = Table['Nov'].apply('{:.2%}'.format)
    Table['Dez'] = Table['Dez'].apply('{:.2%}'.format)
    Table['Ano'] = Table['Ano'].apply('{:.2%}'.format)
    Table['Inicio'] = Table['Inicio'].apply('{:.2%}'.format)
    Table[str(Year)] = ['Fundo', 'CDI', '% CDI']
    data = Table.to_dict('records')

    columns = ([{'id': p, 'name': p} for p in params])
    return data, columns

def slider():
    cota = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_graph.csv',sep=',', index_col=0)
    cota.index = pd.to_datetime(cota.index, format='%Y%m%d')
    reto_ano = ret.ret_ano(cota)
    reto_ano['Year'] = reto_ano.index.year
    YY = reto_ano['Year']

    slider = dcc.Slider(
        id='slider_perf',
        min=YY.min(),
        max=YY.max(),
        value=YY.max(),
        marks={str(year): str(year) for year in YY.unique()},
        step=None
    )
    return slider


def datepicker_fidc(date, cnpj):
    day=int(date.strftime("%Y%m%d"))

    FIDC_Estoques.estoque_fidc(jj=1, CNPJ=cnpj, dia=date)
    FIDC_Estoques.cota_fidc(cnpj,cnpj,Month=False)
    df_graph = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/df_graph.csv',sep=',', index_col=False)
    df_serie_pl = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/Serie_PL.csv',sep=',', index_col=False)
    df_series = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/Series.csv',sep=',',index_col=False)
    df_serie_psac = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/Serie_psac.csv',sep=',',encoding='utf-8',index_col=False)
    df_serie_psac=df_serie_psac.loc[df_serie_psac['Date']<= day]
    df_series = df_series.loc[df_series['Date'] <= day]
    #df_tabela_ced_at = pd.read_csv('Z:\\Credito Privado\\16_BASE\\Dados_Fundos\\' + str(cnpj) + '\\tabela_ced_at.csv', encoding='utf-8',index_col=False)
    df_tabela_ced = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/tabela_ced.csv',sep=',',encoding='utf-8',index_col=False)
    #df_tabela_ced_at = df_tabela_ced_at.loc[df_tabela_ced_at['Date'] <= day]
    df_graph = df_graph.loc[df_graph['Date'] <= day]
    df_serie_pl = df_serie_pl.loc[df_serie_pl['Date'] <= day]
    df_tabela_ced.to_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/tabela_ced.csv',sep=',', index=False)
    df_graph.to_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/df_graph.csv',sep=',', index=False)
    df_serie_pl.to_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/Serie_PL.csv',sep=',' ,index=False)
    df_serie_psac.to_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/Serie_psac.csv',sep=',', index=False)
    #df_tabela_ced_at.to_csv('Z:\\Credito Privado\\16_BASE\\Dados_Fundos\\' + str(cnpj) + '\\df_tabela_ced_at.csv',index_col=False)
    df_series.to_csv('https://raw.githubusercontent.com/luizaidgr/daqui/master/'+str(cnpj)+'/Series.csv',sep=',', index=False)
