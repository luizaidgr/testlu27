# -*- coding: utf-8 -*-Messerschmitt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import pagprin,fidcv1,fidc_concent,fidc_eventos,fidc_perf,ret,callback_fidc,help
import plotly.graph_objs as go
import pathlib
from datetime import datetime
import pandas as pd

df_fund_facts = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_fund_facts.csv",sep=',')
#App que faz as laminas dos FIDCs
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True
server = app.server


# Describe the layout/ UI of the app
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content"),html.Div(id="save")],

 )


# Update page


#############################################################################
##pagina prin
@app.callback(Output("save", "children"), [Input("demo-dropdown", "value"),Input('datepicker','date')])
def dd(value,day):
    if value!=None:

        try:
            day = datetime.strptime(day, "%Y-%m-%dT%H:%M:%S")
        except:
            day = datetime.strptime(day, "%Y-%m-%d")

        callback_fidc.datepicker_fidc(day, value)
        help.fidc_mudanca_arquivo(value)
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
        if pathname=='/gerarlamina':
            return fidcv1.create_layout(app)
        elif pathname== '/Laminas/FIDC2':
            return fidc_concent.create_layout(app)
        elif pathname=="/Laminas/FIDC4":
            return fidc_perf.create_layout(app)
        elif pathname=="/Laminas/FIDC3":
            return fidc_eventos.create_layout(app)
        elif pathname=="/Laminas/FIDC":
            return fidcv1.create_layout(app)
        elif pathname == "/Laminas/FIDC6":
            return (
                fidcv1.create_layout(app),
                fidc_concent.create_layout(app),
                fidc_eventos.create_layout(app),
                fidc_perf.create_layout(app))
        elif pathname == '/Laminas/FIDC7' :
            return(fidcv1.create_layout(app),
                   fidc_perf.create_layout(app))



        else:
            return pagprin.create_layout(app)
#############################################################################
## atraso e pdd
@app.callback([Output("atpdd","figure"),Output("pdd/fat","figure"),Output("varpdd","figure")],[Input("atrpdd","children")])
def atrpdd(ap):

            df_series = pd.read_csv("https://github.com/luizaidgr/testlu27/blob/master/data/Series.csv",sep=',')
            df_series['Date'] = pd.to_datetime(df_series.Date, format = "%Y%m%d")

            df_series['at_pdd'] = (df_series['Atraso']-df_series['Atraso_PDD'])/df_series['PL']
            df_series['at'] = (df_series['Atraso_PDD'])/df_series['Atraso']

            df_series['pdd_fat'] = df_series['Atraso_PDD']/df_series['Faturamento 30 Dias']

            df_series['pdd_pl'] = (df_series['PDD 30 Dias']-df_series['Atraso_PDD'])/(df_series['PL']-df_series['Atraso'])

            df_series['_21PDD'] = df_series['PDD 30 Dias'].pct_change(21)
            df_series['_21ATR'] = df_series['Atraso'].pct_change(21)
            figurepdd1 = {
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
                 }
            figurepdd4 = {
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
            }
            figurepdd2={
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
                                        }
            figurepdd3={
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
                                        }

            return figurepdd1,figurepdd2,figurepdd3
##############################################################################
####CALLBACK PRO FENIX performance (entrar em laminas_comercial.pages fidc_perf)
@app.callback([Output('datatableperf17','data'),Output('datatableperf18','data'),Output('datatableperf19','data'),Output('datatableperf20','data')],[Input("slid","children")])
def perform(ei):
    cota = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_graph.csv',sep=',', index_col=0)
    cdi = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/CDI.csv',sep=',', index_col=0)
    cdi.index = pd.to_datetime(cdi.index, format='%m/%d/%Y')
    cota.index = pd.to_datetime(cota.index, format='%Y%m%d')

    reto_mes = ret.ret_mes(cota)
    reto_ano = ret.ret_ano(cota)

    reto_ano['Year'] = reto_ano.index.year
    reto_mes['Year'] = reto_mes.index.year
    reto_mes['Month'] = reto_mes.index.month
    loi = reto_mes['Month'].max()
    YY = reto_ano['Year']
    jop = YY.values
    rodaj = list(jop)

    for ano in rodaj:
        Year = ano
        params = [str(Year),
                  'Jan', 'Fev', 'Mar', 'Abr',
                  'Mai', 'Jun', 'Jul', 'Ago',
                  'Set', 'Out', 'Nov', 'Dez', 'Ano', 'Total'

                  ]

        names = ['Fundo', 'CDI', '% CDI']

        # -----------------------------------------------------------------------------------------------------------
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

        ret_ini = ret.ret_ini(cota, Year) - 1
        ret_ini['pct_cdi'] = ret_ini[list(cota.columns)[0]] / ret_ini['CDI_ACUM']

        Table = ret_m.T
        Table['Ano'] = ret_y.T
        Table['Total'] = ret_ini.T
        Table[str(Year)] = names
        Table = Table.rename(
            columns={1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set',
                     10: 'Out',
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
        Table['Total'] = Table['Total'].apply('{:.2%}'.format)
        table = Table
        if Year == 2017:
            table17 = table.to_dict('records')
        elif Year == 2018:
            table18 = table.to_dict('records')
        elif Year == 2019:
            table19 = table.to_dict('records')
        else:
            table20 = table.to_dict('records')

    return table17,table18,table19,table20
####CALLBACK para o zeus performance
'''@app.callback([Output('datatableperf19','data'),Output('datatableperf20','data')],[Input("slid","children")])
def perform(ei):
    cota = pd.read_csv('Z:\Gestao\Programas\Python\App\Laminas\FIDC\data\df_graph.csv', index_col=0)
    cdi = pd.read_csv('Z:\Gestao\Programas\Python\CSV\CDI.csv', index_col=0)
    cdi.index = pd.to_datetime(cdi.index, format='%m/%d/%Y')
    cota.index = pd.to_datetime(cota.index, format='%Y%m%d')

    reto_mes = ret.ret_mes(cota)
    reto_ano = ret.ret_ano(cota)

    reto_ano['Year'] = reto_ano.index.year
    reto_mes['Year'] = reto_mes.index.year
    reto_mes['Month'] = reto_mes.index.month
    loi = reto_mes['Month'].max()
    YY = reto_ano['Year']
    jop = YY.values
    rodaj = list(jop)

    for ano in rodaj:
        Year = ano
        params = [str(Year),
                  'Jan', 'Fev', 'Mar', 'Abr',
                  'Mai', 'Jun', 'Jul', 'Ago',
                  'Set', 'Out', 'Nov', 'Dez', 'Ano', 'Total'

                  ]

        names = ['Fundo', 'CDI', '% CDI']

        # -----------------------------------------------------------------------------------------------------------
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

        ret_ini = ret.ret_ini(cota, Year) - 1
        ret_ini['pct_cdi'] = ret_ini[list(cota.columns)[0]] / ret_ini['CDI_ACUM']

        Table = ret_m.T
        Table['Ano'] = ret_y.T
        Table['Total'] = ret_ini.T
        Table[str(Year)] = names
        Table = Table.rename(
            columns={1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun', 7: 'Jul', 8: 'Ago', 9: 'Set',
                     10: 'Out',
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
        Table['Total'] = Table['Total'].apply('{:.2%}'.format)
        table = Table
        if Year == 2019:
            table19 = table.to_dict('records')
        else:
            table20 = table.to_dict('records')

    return table19,table20'''
#############################################################################
##CALLBACK CONCENTRAÇÃO
@app.callback([Output('tableconc','data'),Output('pie','figure'),Output('graphic-sac','figure')],[Input('idcon','children')])
def concent(oioi):
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../data").resolve()

    df_serie_psac = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_psac.csv",sep=',', encoding='utf-8')
    df_serie_pced = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_pced.csv",sep=',', encoding='utf-8')
    df_tabela_ced = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela_ced.csv",sep=',', encoding='utf-8')
    df_tabela_ced_at = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela_ced_at.csv",sep=',', encoding='utf-8')
    df_serie=pd.read_csv("https://github.com/luizaidgr/testlu27/blob/master/data/Series.csv",sep=',', encoding='utf-8')




    df_serie_psac['Date'] = pd.to_datetime(df_serie_psac.Date, format="%Y%m%d")
    df_serie_pced['Date'] = pd.to_datetime(df_serie_pced.Date, format="%Y%m%d")
    df_serie['Date'] = pd.to_datetime(df_serie_pced.Date, format="%Y%m%d")

    V1 = df_tabela_ced_at["VALOR_NOMINAL"].to_numpy()

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

    params = [
        'Janeiro', 'Fevereiro', 'Março', 'Abril',
        'Maio', 'Junho', 'Julho', 'Agosto',
        'Setembro', 'Outubro', 'Novembro', 'Dezembro', ' ', 'Ano', 'Inicio'
    ]
    tabelaconc=df_teste2.to_dict('records')
    figureconc=go.Figure(
            data=[go.Pie(labels=df_tabela_ced_at["NOME_CEDENTE"],
                               values=df_tabela_ced_at["VALOR_PRESENTE"])],
            layout=go.Layout(
           showlegend=False,
           autosize=True,
           width=340,
           height=340,
      )
              )
    figureconc2 = {
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
    }
    return tabelaconc,figureconc,figureconc2
#############################################################################
###CALLBACKS DA PAGINA GERAL
@app.callback([Output("graph-2","figure"),Output('graphic-ret',"figure")],[Input("oi","children")])
def graficos(figure):
    df_series_pl = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_PL.csv",sep=',')
    df_series_yp = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_Y_P.csv",sep=',')
    df_series_C_S = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_C_S.csv",sep=',')
    cota = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_graph.csv',sep=',', index_col=0)
    cdi = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/CDI.csv',sep=',', index_col=0)
    cdi.index = pd.to_datetime(cdi.index, format='%m/%d/%Y')
    cota.index = pd.to_datetime(cota.index, format='%Y%m%d')

    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("../data").resolve()

    cota.index = pd.to_datetime(cota.index)
    df_series_pl3 = pd.DataFrame(columns=['Date', 'Cota', 'CDI'])
    df_series_pl3['Date'] = cota.reset_index()['Date']
    df_series_pl3['Cota'] = cota.reset_index()[list(cota.columns)[0]]
    df_series_pl3['Cota'] = df_series_pl3['Cota'].apply(lambda x: (x / df_series_pl3.iloc[0, 1]) * 100)

    df_series_pl3['Date'] = pd.to_datetime(df_series_pl3.Date, format="%Y%m%d")

    df_series_pl3 = pd.merge_asof(df_series_pl3, cdi.reset_index().rename(columns={'index': 'Date'}), on='Date').drop(
        ['CDI_x', 'CDI_y', 'SELIC'], 1)
    df_series_pl3['CDI_ACUM'] = df_series_pl3['CDI_ACUM'].apply(lambda x: (x / df_series_pl3.iloc[0, 2]) * 100)

    df_series_pl['Date'] = pd.to_datetime(df_series_pl.Date, format="%Y%m%d")
    df_series_yp['Date'] = pd.to_datetime(df_series_yp.Date, format="%Y%m%d")
    df_series_C_S['Date'] = pd.to_datetime(df_series_C_S.Date, format="%Y%m%d")
    figurea  = {"data": [
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
                      height=200,
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
                  )}

    figurec = {
        "data": [
            go.Scatter(
                x=df_series_C_S['Date'],
                y=df_series_C_S['Maior_exposicao_cedente'],
                line={"color": "#56679d"},
                mode="lines",
                name="Cedente",
            ),
            go.Scatter(
                x=df_series_C_S['Date'],
                y=df_series_C_S['Maior_exposicao_sacado'],
                line={"color": "#b5b5b5"},
                mode="lines",
                name="Sacado",
                yaxis='y2'
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
    }
    figureb = {
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
    }
    figureper = {
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
            height=240,
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
    }
    return figureb,figureper
@app.callback(Output('table',"data"),[Input("oi","children")])
def tabelas(tab):
    df_fund_facts = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_fund_facts.csv",sep=',')
    data1=df_fund_facts.to_dict('records')
    df_price_perf = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/tabela1.csv",sep=',')
    tbi = df_price_perf.rename(columns={' ': 'label', ' .1': 'value'})
    df_price_perf = pd.concat([df_fund_facts, tbi])
    data2=df_price_perf.to_dict('records')


    return data2
@app.callback(Output('nome_fundo_FIDC',"children"),[Input('idz','children')])
def nome(nomefundo):
    df_fund_facts = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_fund_facts.csv",sep=',')
    name = df_fund_facts.iloc[0, 1]
    if name == "FÊNIX FIDC NP":
        name = "FÊNIX FIDC NP"
    else:
        name = "ZEUS FIDC"
    return name

if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_hot_reload=True)
