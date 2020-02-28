import pandas as pd

#callback resumo do fundo
def algumacoisa ():
    df_fund_facts = pd.read_csv("https://raw.githubusercontent.com/luizaidgr/testlu27/master/data/df_fund_facts.csv",sep=',')
    name = df_fund_facts.iloc[0, 1]
    if name=='FÊNIX FIDC NP':
        gopl="\
                                        O Fundo " + name + " é um FIDC não padronizado, \
                                        que tem a maior parte das suas operações relacionada a divida de fornecedores de autopeças. "
    else:
        gopl="O FIDC ZEUS adquire direitos creditórios originários de operações realizadas no segmento comercial, preponderantemente, da cadeia de combustíveis "
    return gopl
#callback tabelas performance
