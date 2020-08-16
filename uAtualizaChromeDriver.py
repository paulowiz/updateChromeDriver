import sys
import os
import io 
from datetime import datetime
import requests
import zipfile

def baixar_arquivo(url, endereco):
    resposta = requests.get(url)
    if resposta.status_code == requests.codes.OK:
        with open(endereco, 'wb') as novo_arquivo:
            novo_arquivo.write(resposta.content)
        print("Download finalizado. Arquivo salvo em: {}".format(endereco))
    else:
        resposta.raise_for_status()

def localiza_versao_chromedriver(pasta):
    subpastas = list()
    if os.path.isdir(pasta):
        items = os.listdir(pasta)
        for item in items:
            novo_item = os.path.join(pasta,item)
            if os.path.isdir(novo_item):
                subpastas.append(novo_item)
                continue
            caminho_completo = pasta+'\\'+item
            #print(pasta+'\\'+item) # Exibe o nome de todos os arquivos percorridos
            #exibe somente o arquivo com o nome da versão
            if caminho_completo.endswith(".manifest"):
                item = item.split('.')
                versao = item[0]+'.'+item[1]+'.'+item[2] 
                return versao
                
try:
    os.remove('chromedriver.zip')
except:
    pass

try:
    os.remove('chromedriver.exe')
except:
    pass
        
#Caminhos do google chrome x86 e x64
X64path = 'C:\Program Files (x86)\Google\Chrome\Application/'
X86path = 'C:\Program Files\Google\Chrome\Application/'

#Verifica nas 2 pastas se existe o google chrome para pegar a versão 
try:
    pastas = os.listdir(X86path)
    path = X86path
except:
    try:
        pastas = os.listdir(X64path)
        path = X64path
    except:
       print('Google Chrome não instalado no computador.')
       sys.exit(0)
        
#Com a function acima ele     
versao = ''
for pasta in pastas:
   if versao == '':
        versao = localiza_versao_chromedriver(path+pasta)
    
print(versao)
lastRelease = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'+versao)
print(lastRelease.text)
baixar_arquivo('https://chromedriver.storage.googleapis.com/'+lastRelease.text+'/chromedriver_win32.zip','chromedriver.zip')


with zipfile.ZipFile('chromedriver.zip', 'r') as zip_ref:
    zip_ref.extractall('')

os.remove('chromedriver.zip')

