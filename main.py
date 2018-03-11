# coding: utf-8
# version:1.0
#python 3
# ftp://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/

"""
version:1.0
author: José Ivan Silva Vegiani
Automacao de download e deploy de dados do rbmc (Ibge)
rbmc: Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS
Script de código aberto e livre, cedido gratuitamente pelo autor.
Parâmetros para download:
Locais: Cascavel, Maringá, Curitiba e Guarapuava
Horário de disponibilização dos arquivos no host: 18:35
Horário agendado para download: 23:00
Referência de dia atual -1 em gnss calendar
"""

import os
import time
import datetime
import zipfile
import ftplib
from pathlib import PurePath
from pathlib import PurePosixPath
from pathlib import Path


#variaveis globais
baseFolder='Cascavel','Maringá','Curitiba','Guarapuava'
paths_bases_globais_list=[]
paths_extracts=[]


def date2doy(date):
    """Convert date to day of year, return int doy.
    Example:
    >>> from datetime import date
    >>> date2doy(date(2017, 5, 17))
    137
    """
    first_day = datetime.date(date.year, 1, 1)
    delta = date - first_day
    return delta.days + 1

def folderYearFunction():

    now = datetime.datetime.now()
    today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
    day_target=today_gnss-1
    if  day_target == 0:
        folderYear =str(int(now.year)-1)
    else:
        folderYear =str(now.year)
    return folderYear

def bissexto(folderYear):
    if int(folderYear) % 100 != 0 and int(folderYear) % 4 == 0 or int(folderYear) % 400 == 0:
        return True
    else:
        return False

def id_target_function(day_delay):
    """ Retorna id_target (identificação do dia alvo)
    """
    now = datetime.datetime.now()
    today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
    day_target=today_gnss-day_delay
    #caso seja virada de ano
    if day_target == 0 and bissexto(folderYear):
        day_target=366
    if day_target==0:
        day_target=365
    #adicionando o 0 antes de 100
    if day_target<100:
        id_target="0"+str(day_target)
    else:
        id_target=str(day_target)
    return id_target

def folder_root(folderYear):
    # estruturando pasta raiz
    path1=os.path.join('..','IBGE','rmbc',folderYear)
    if not os.path.exists(os.path.join(path1)):
        os.makedirs(path1)

def local_Bases_Folders(folderYear):
    if not os.path.exists(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[0])):
        os.makedirs(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[0]))
    if not os.path.exists(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[1])):
        os.makedirs(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[1]))
    if not os.path.exists(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[2])):
        os.makedirs(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[2]))
    if not os.path.exists(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[3])):
        os.makedirs(os.path.join('..','IBGE','rmbc',folderYear,baseFolder[3]))

def names_File_Target(id_target):
    # Cascavel: prcv , Maringá: prma, Curitiba:ufpr e Guarapuava:prgu
    sufix_file=id_target+"1"+".zip"
    file_target=["prcv"+sufix_file,"prma"+sufix_file,"ufpr"+sufix_file,"prgu"+sufix_file]
    return file_target

def download_ftp(address,paths_bases_globais_list):

    site_address=address
    ftp=ftplib.FTP(site_address)
    ftp.login()
    dir_cwd = str("informacoes_sobre_posicionamento_geodesico/rbmc/dados/"+'/'+folderYear+"/"+id_target)
    print(ftp.dir())
    print(dir_cwd)
    ftp.cwd(str(dir_cwd))
    i=0
    for p in baseFolder:
        p = open(str(paths_bases_globais_list[i])+"/"+file_target[i], "wb")
        ftp.retrbinary("RETR " + file_target[i], p.write)
        i=i+1
    ftp.quit()

def paths_bases_globais(folderYear):
    paths_bases_globais=[]
    i=0
    for p in baseFolder:
        paths_bases_globais0=os.path.join("..",'IBGE','rmbc',folderYear,baseFolder[i])
        p1 = Path(paths_bases_globais0)
        paths_bases_globais_list.append(p1.resolve())
        i=i+1
    return paths_bases_globais_list

def extracts(paths_bases_globais_list):
    j=0
    for b in baseFolder:
        if not os.path.exists(os.path.join(str(paths_bases_globais_list[j]),"extracts")):
            os.makedirs(os.path.join(str(paths_bases_globais_list[j]),"extracts"))
        paths_extracts.append(os.path.join(str(paths_bases_globais_list[j]),"extracts"))
        j=j+1
    i=0
    for c in baseFolder:
        zip1 = zipfile.ZipFile(str(paths_bases_globais_list[i])+"/"+file_target[i])
        zip1.extractall(str(paths_extracts[i]))
        i=i+1
    zip1.close()


# ----------------------------------------------------main ---------------------------------------------------------#
a=True
day=0
while a:
    day=day+1
    folderYear=folderYearFunction()
    local_Bases_Folders(folderYear)
    id_target=id_target_function(day)
    folder_root(folderYear)
    file_target=names_File_Target(id_target)
    paths_bases_globais_list=paths_bases_globais(folderYear)
    try:
        download_ftp("geoftp.ibge.gov.br",paths_bases_globais_list)
        a=False
    except ftplib.error_perm:
        a=True
try:
    extracts(paths_bases_globais_list)
except FileNotFoundError:
    time.sleep(60*3)
    try:
        extracts(paths_bases_globais_list)
    except FileNotFoundError:
        print('se chegou aqui deu algum erro')
