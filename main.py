# coding: utf-8
# version:1.0
# Copyright © 2001-2018 Python Software Foundation https://docs.python.org/3/license.html
#author: José Ivan Silva Vegiani

"""
version:1.0
Copyright © 2001-2018 Python Software Foundation https://docs.python.org/3/license.html
author: José Ivan Silva Vegiani
Automacao de download e gerenciamento de dados do rbmc (Ibge)
rbmc: Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS
Script de código aberto e livre, cedido gratuitamente pelo autor.
Parâmetros para download:
Locais: Cascavel, Maringá, Curitiba e Guarapuava
Horário para download: 23:00
Referência de dia atual -1 em gnss calendar
"""

import os
import datetime
import zipfile
import ftplib
from pathlib import PurePath
import gnsscal

#agora é
now = datetime.datetime.now()

# dia de hoje em Gnss Calendar
today_gnss=int(gnsscal.date2doy(datetime.date(now.year,now.month,now.day)))
# today_gnss=1 # simulando 1 de janeiro

#atribui pasta alvo um dia anterior
day_target=today_gnss-1

#caso o dia alvo for 0 (data atual sendo 1 de janeiro )
if  day_target == 0:
    folderYear =str(int(now.year)-1)
else:
    folderYear =str(now.year)


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


# parei aqui, implementar solução para virada do ano 
# if day_target == 0:


if day_target<100:
    id_folder_target="0"+str(day_target)
else:
    id_folder_target=str(day_target)

#prefixo dos arquivos de bases do Paraná
# Cascavel: prcv , Maringá: prma, Curitiba:ufpr e Guarapuava:prgu

#nomenando arquivos alvo
sufix_file=id_folder_target+"1"+".zip"
Cascavel_zip="prcv"+sufix_file
Maringa_zip="prma"+sufix_file
Curitiba_zip="ufpr"+sufix_file
Guarapuava_zip="prgu"+sufix_file


#trabalhando com ftp
#ftp://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/

site_address="geoftp.ibge.gov.br"
ftp=ftplib.FTP(site_address)
ftp.login()
# print(ftp.getwelcome())
# print(ftp.dir())
dir_cwd0 = PurePath("informacoes_sobre_posicionamento_geodesico/rbmc/dados")
dir_cwd=dir_cwd0.joinpath(folderYear)
print(dir_cwd)
#ftp.cwd('informacoes_sobre_posicionamento_geodesico/rbmc/dados/2018/062')
# print(ftp.dir())
# ftp.retrbinary('RETR ufpr0621.zip',open('ufpr0621.zip','w').write)
