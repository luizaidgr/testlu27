import shutil
import os
from git import repo
from git import util
import pandas as pd
import git
import requests
from git import util

login={
'commit': 'Sign in',
'utf8': '✓',
'authenticity_token': 'uEdhJmsKrS3L+tGBn3PavuSGwL/EcoLfIT3ph3jnA0CSZQUdY70L1pr+e29XFfGbu6oSnUS3niLVqqS1QKGz6w==',
'ga_id': '301921361.1580830010',
'login': 'luizaidgr',
'password': 'idgr1234',
'webauthn-support': 'supported',
'webauthn-iuvpaa-support': 'unsupported',
'return_to': '',
'required_field_8446': '',
'timestamp': '1582901651018',
'timestamp_secret': '767ada84e8aaff35a5ecc7c369ba5cc075c702136173ff62b1b401de58c9a70b'
}
headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
with requests.Session() as s:
    url = 'https://github.com/login'
    r = s.get(url, headers=headers)
    r = s.post(url, data=login)
    r2=s.get('https://github.com/luizaidgr/daqui')

    repo=git.Repo('https://github.com/luizaidgr/testlu27')
    repo.git.checkout('testelu27/master', b='master' )
    repo.git.add('C:/Users/Hemerson de Villa/Documentos/nutela.csv')
    repo.git.commit(m='j')
    #source = 'https://raw.githubusercontent.com/luizaidgr/daqui/master/26631527000108/nutela.csv'
    #dst = 'https://raw.githubusercontent.com/luizaidgr/testlu27/master/data'
    #git.util.stream_copy(src, dst)
    #git.add


    #git.util.stream_copy(source,dst)


    #    for files in source:
     #   if files.endswith(".csv"):
      #      src = "Z:\\Credito Privado\\16_BASE\\Dados_Fundos\\" +CNPJ+ '\\' + files
       #     shutil.copy(src, dst)
