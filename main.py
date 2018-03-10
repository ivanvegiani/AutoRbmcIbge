# coding: utf-8
# version:1.0
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

baseFolder='Cascavel','Maringá','Curitiba','Guarapuava'

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

def folderYear():

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

def id_target(day_delay):
    """ Retorna id_target (identificação do dia alvo)
    """
    now = datetime.datetime.now()
    today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
    day_target=today_gnss-day_delay
    #caso seja virada de ano
    if day_target == 0 and bissexto():
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

def download_ftp(address,paths_bases_globais):
    site_address=address
    ftp=ftplib.FTP(site_address)
    ftp.login()
    dir_cwd = PurePath("informacoes_sobre_posicionamento_geodesico/rbmc/dados/"+folderYear+"/"+id_target)
    ftp.cwd(str(dir_cwd))
    i=0
    for p in paths_bases_globais:
        p = open(str(paths_bases_globais[i])+"/"+file_target[i], "wb")
        ftp.retrbinary("RETR " + file_target[i], p.write)
        i=i+1
    ftp.quit()

def paths_bases_globais(folderYear):
    paths_bases_globais=[]
    for p in range(4):
        paths_bases_globais0=os.path.join("..",'IBGE','rmbc',folderYear,baseFolder[p])
        p1 = Path(paths_bases_globais0)
        paths_bases_globais.append(p1.resolve())
    return paths_bases_globais

# -----------------------------main ------------------------------#
folderYear=folderYear()
id_target=id_target(1)
folder_root(folderYear)
file_target=names_File_Target(id_target)
download_ftp("geoftp.ibge.gov.br",paths_bases_globais(folderYear))
