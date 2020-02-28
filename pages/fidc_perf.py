import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dash_table
from pages import ret
from pages.utils import Header, make_dash_table
import pandas as pd
import pathlib
import dash


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
app.config['suppress_callback_exceptions']=True

df_series_pl = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/Serie_PL.csv",sep=',')
cota = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_graph.csv",sep=',', index_col=0)
cdi = pd.read_csv('https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/CDI.csv',sep=',', index_col=0)
cdi.index = pd.to_datetime(cdi.index, format='%m/%d/%Y')
cota.index = pd.to_datetime(cota.index, format='%Y%m%d')


reto_mes = ret.ret_mes(cota)
reto_ano = ret.ret_ano(cota)

reto_ano['Year'] = reto_ano.index.year
reto_mes['Year'] = reto_mes.index.year
reto_mes['Month'] = reto_mes.index.month
loi=reto_mes['Month'].max()
YY = reto_ano['Year']
jop=YY.values
rodaj=list(jop)


for ano in rodaj:
    Year=ano
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
    if Year==2017:
        table17=table.to_dict('records')
        params17=params
    elif Year==2018:
        table18=table.to_dict('records')
        params18=params
    elif Year==2019:
        table19=table.to_dict('records')
        params19=params
    else:
        table20=table.to_dict('records')
        params20=params







#-----------------------------------------------------------------------------------------------



# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()


cota.index = pd.to_datetime(cota.index)
df_series_pl3 = pd.DataFrame(columns=['Date', 'Cota', 'CDI'])
df_series_pl3['Date'] = cota.reset_index()['Date']
df_series_pl3['Cota'] = cota.reset_index()[list(cota.columns)[0]]
df_series_pl3['Cota'] = df_series_pl3['Cota'].apply(lambda x: (x/df_series_pl3.iloc[0,1])*100)

df_series_pl3['Date'] = pd.to_datetime(df_series_pl3.Date, format = "%Y%m%d")


df_series_pl3 = pd.merge_asof(df_series_pl3,cdi.reset_index().rename(columns={'index': 'Date'}), on='Date').drop(['CDI_x','CDI_y', 'SELIC'], 1)
df_series_pl3['CDI_ACUM'] = df_series_pl3['CDI_ACUM'].apply(lambda x: (x/df_series_pl3.iloc[0,2])*100)

'''dash_table.DataTable(

                                            id='datatableperf17',
                                            columns=[{"name": i, "id": i} for i in params17],
                                            data=table17,
                                            editable=True,
                                            style_table={'maxWidth': '670px'},
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }],

                                            style_cell={"fontFamily": "calibri", "font_size": 9, 'textAlign': 'center',
                                                        'minWidth': '36px', 'width': '36px', 'maxWidth': '36px'},
                                            style_as_list_view=True,
                                            style_header={
                                                'backgroundColor': 'white',
                                                'fontWeight': 'bold'
                                            }, ),
                                        dash_table.DataTable(

                                            id='datatableperf18',
                                            columns=[{"name": i, "id": i} for i in params18],
                                            data=table18,
                                            editable=True,
                                            style_table={'maxWidth': '670px'},
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }],

                                            style_cell={"fontFamily": "calibri", "font_size": 9, 'textAlign': 'center',
                                                        'minWidth': '36px', 'width': '36px', 'maxWidth': '36px'},
                                            style_as_list_view=True,
                                            style_header={
                                                'backgroundColor': 'white',
                                                'fontWeight': 'bold'
                                            }, ),'''




def create_layout(app):

    # Page layouts
    return html.Div(
        [html.Div(id="slid"),
            html.Div([Header(app)]),
            # page 1
            html.Div(
                [

                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [ html.H6(
                                        'Performance',
                                        className="subtitle padded",
                                    ),


                                    html.Div([
                                        #####inserir o texto p/17 e 18
                                        dash_table.DataTable(

                                            id='datatableperf17',
                                            columns=[{"name": i, "id": i} for i in params17],
                                            data=table17,
                                            editable=True,
                                            style_table={'maxWidth': '670px'},
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }],

                                            style_cell={"fontFamily": "calibri", "font_size": 9, 'textAlign': 'center',
                                                        'minWidth': '36px', 'width': '36px', 'maxWidth': '36px'},
                                            style_as_list_view=True,
                                            style_header={
                                                'backgroundColor': 'white',
                                                'fontWeight': 'bold'
                                            }, ),
                                        dash_table.DataTable(

                                            id='datatableperf18',
                                            columns=[{"name": i, "id": i} for i in params18],
                                            data=table18,
                                            editable=True,
                                            style_table={'maxWidth': '670px'},
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }],

                                            style_cell={"fontFamily": "calibri", "font_size": 9, 'textAlign': 'center',
                                                        'minWidth': '36px', 'width': '36px', 'maxWidth': '36px'},
                                            style_as_list_view=True,
                                            style_header={
                                                'backgroundColor': 'white',
                                                'fontWeight': 'bold'
                                            }, ),


                                    dash_table.DataTable(

                                        id='datatableperf19',
                                        columns=[{"name": i, "id": i} for i in params19],
                                        data=table19,
                                        editable=True,
                                        style_table={'maxWidth': '670px'},
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': 'rgb(248, 248, 248)'
                                            }],

                                        style_cell={"fontFamily": "calibri", "font_size": 9, 'textAlign': 'center',
                                                    'minWidth': '36px', 'width': '36px', 'maxWidth': '36px'},
                                        style_as_list_view=True,
                                        style_header={
                                            'backgroundColor': 'white',
                                            'fontWeight': 'bold'
                                        }, ),





                                        dash_table.DataTable(
                                            id='datatableperf20',
                                            columns=[{"name": i, "id": i} for i in params20],
                                            data=table20,
                                            editable=True,
                                            style_table={'maxWidth': '670px'},
                                            style_data_conditional=[
                                                {
                                                    'if': {'row_index': 'odd'},
                                                    'backgroundColor': 'rgb(248, 248, 248)'
                                                }],

                                            style_cell={"fontFamily": "calibri", "font_size": 9, 'textAlign': 'center',
                                                        'minWidth': '36px', 'width': '36px', 'maxWidth': '36px'},
                                            style_as_list_view=True,
                                            style_header={
                                                'backgroundColor': 'white',
                                                'fontWeight': 'bold'
                                            }, )
                                    ]),
                                ],
                                className="row",

                            ),
                            html.Div(
                                [
                                    html.H6(["Outras informações"], className="subtitle"),
                                    html.Br([]),
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
                                            "background-color": "#f9f9f9",
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

