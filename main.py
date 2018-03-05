# coding: utf-8
# version:1.0
# Copyright © 2001-2018 Python Software Foundation https://docs.python.org/3/license.html
#author: José Ivan Silva Vegiani

"""
AutoBaseIbge:
version:1.0
Copyright © 2001-2018 Python Software Foundation https://docs.python.org/3/license.html
author: José Ivan Silva Vegiani
Automacao de download e gereciado de bases do IBGE
Código aberto e livre, cedido gratuitamente e voluntáriamente pelo autor.
ftp://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/
Destinado a todos interessados a utilizar a aplicação, em forma live e gratuita.
"""

import os
import datetime
import zipfile
import ftplib
import gnsscal

#manipulando  as datas
now = datetime.datetime.now()
print(gnsscal.date2doy(datetime.date(2017,5,17)))



#variáveis globais
folderYear=str(now.year)




# estruturando pasta raiz
path1=os.path.join('..','IBGE','rmbc',folderYear)
if not os.path.exists(os.path.join(path1)):
    os.makedirs(path1)


# bases Paraná: Cascavel, Maringá, Curitiba e Guarapuava
path1=os.path.join('..','IBGE','rmbc',folderYear)
baseFolder=[]
baseFolder='Cascavel','Maringá','Curitiba','Guarapuava'
# estruturando as pastas dos locais das bases
if not os.path.exists(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[0])):
    os.makedirs(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[0]))
if not os.path.exists(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[1])):
    os.makedirs(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[1]))
if not os.path.exists(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[2])):
    os.makedirs(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[2]))
if not os.path.exists(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[3])):
    os.makedirs(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[3]))

# estruturando os nomes dos arquivos



#trabalhando com ftp
#ftp://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/

# site_address="geoftp.ibge.gov.br"
# ftp=ftplib.FTP(site_address)
# ftp.login()
# print(ftp.getwelcome())
# print(ftp.dir())
# ftp.cwd('informacoes_sobre_posicionamento_geodesico/rbmc/dados/2018/062')
# print(ftp.dir())
# ftp.retrbinary('RETR ufpr0621.zip',open('ufpr0621.zip','w').write)
