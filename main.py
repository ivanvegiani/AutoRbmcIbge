# coding: utf-8
# version:1.0
#python 3
# ftp://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/

"""
version:1.0
author: Jose Ivan Silva Vegiani
Automacao de download e deploy de dados do rbmc (IBGE)
rbmc: Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS
Script de código aberto e livre, cedido gratuitamente pelo autor.
Parâmetros para download:
Locais: Cascavel, Maringá, Curitiba e Guarapuava
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
from socket import gethostbyname, gaierror
import logging
import sys
import subprocess


#variaveis globais
baseFolder='Cascavel','Maringá','Curitiba','Guarapuava'
paths_bases_globais_list=[]
paths_extracts=[]
folderYear=''
id_target=''
file_target=[]
path_root='c:\IBGE'
today_gnss=0
day=0

now1 = datetime.datetime.now()
year=str(now1.year)
format0='%(asctime)s - %(message)s'
logging.basicConfig(filename='log'+year+'.txt',level=logging.DEBUG, format=format0,datefmt='%d/%m/%y %I:%M:%S %p')


def logs_info(mensagem):
   
    logging.info(mensagem)
    
def logs_bug(nome_variavel,variavel):  
    
    logging.debug('debug '+nome_variavel+': '+variavel)

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

def folderYearFunction(day_delay):

    now = datetime.datetime.now()
    today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
    logs_bug('today_gnss',str(today_gnss))
    day_target=today_gnss-day_delay
    
    if  day_target <= 0  :
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

# definindo o id_target
    if day_target<100 and day_target>=10 and day_target>0:
        id_target="0"+str(day_target)
    elif day_target>=100:
        id_target=str(day_target)
    else:
        id_target="00"+str(day_target)


    # em casos de virada de ano
    if day_target == 0:
        if bissexto(folderYear):
            day_target=366
            id_target=str(day_target)
        else:
            day_target=365
            id_target=str(day_target)


    if day_target<0:
        if bissexto(folderYear):
            day_target=366+day_target

        else:
            day_target=366+day_target


    if day_target<100 and day_target>=10 and day_target>0:
        id_target="0"+str(day_target)
    elif day_target>=100:
        id_target=str(day_target)
    else:
        id_target="00"+str(day_target)

    return id_target


def local_Bases_Folders(path_root,folderYear):
    i=0
    for paths in baseFolder:
        if not os.path.exists(os.path.join(path_root,folderYear,baseFolder[i])):
            os.makedirs(os.path.join(path_root,folderYear,baseFolder[i]))
        i=i+1

def names_File_Target(id_target):
    # Cascavel: prcv , Maringá: prma, Curitiba:ufpr e Guarapuava:prgu
    sufix_file=id_target+"1"+".zip"
    file_target=["prcv"+sufix_file,"prma"+sufix_file,"ufpr"+sufix_file,"prgu"+sufix_file]
    return file_target

def download_ftp(address,paths_bases_globais_list,folderYear,id_target,file_target):
    site_address=address
    ftp=ftplib.FTP(site_address)
    ftp.login()
    dir_cwd = str("informacoes_sobre_posicionamento_geodesico/rbmc/dados"+'/'+folderYear+"/"+id_target)
    print (str(dir_cwd))
    print('\nConectado em ftp://geoftp.ibge.gov.br \n')
    ftp.cwd(str(dir_cwd))
    i=0
    for p in file_target:
        p = open(str(os.path.join(paths_bases_globais_list[i],file_target[i])), "wb")
        print('Downloading file '+file_target[i]+' para '+str(paths_bases_globais_list[i]))
        ftp.retrbinary("RETR " + file_target[i], p.write)
        print('Download file '+file_target[i]+' sucess\n')
        logs_info('Download file '+file_target[i]+' sucess')
        logs_bug('file_target[i]',file_target[i])
        i=i+1
    print(file_target)
    
    ftp.quit()

def paths_bases_globais(path_root,folderYear):
    i=0
    for p in baseFolder:
        paths_bases_globais0=os.path.join(path_root,folderYear,baseFolder[i])
        p1 = Path(paths_bases_globais0)
        paths_bases_globais_list.append(p1.resolve())
        i=i+1
    return paths_bases_globais_list

def extracts(paths_extracts,paths_bases_globais_list,file_target):
    j=0
    for b in range(4):
        if not os.path.exists(os.path.join(str(paths_bases_globais_list[j]),"extracts")):
            os.makedirs(os.path.join(str(paths_bases_globais_list[j]),"extracts"))
        paths_extracts.append(os.path.join(str(paths_bases_globais_list[j]),"extracts"))
        j=j+1
    i=0
    for z in range(4):
        print('Extraindo para '+str(paths_extracts[i]))
        zip1 = zipfile.ZipFile(str(os.path.join(paths_bases_globais_list[i],file_target[i])))
        zip1.extractall(str(paths_extracts[i]))
        logs_info('Extraido '+file_target[i]+' com sucesso')
        i=i+1
    i=0
    zip1.close()
    
def dia_de_hoje():
    now = datetime.datetime.now()
    today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
    return today_gnss

def conversao_dia(dia,mes,ano):
    var=datetime.date(ano,mes,dia)
    alvo=int(date2doy(datetime.date(var.year,var.month,var.day)))
    logs_bug('alvo',str(alvo))
    return alvo

    
def rotina_auto(day):
    paths_bases_globais_list=[]
    paths_extracts=[]
    folderYear=''
    id_target=''
    file_target=[]
    folderYear=folderYearFunction(day)
    local_Bases_Folders(path_root,folderYear)
    id_target=id_target_function(day)
    file_target=names_File_Target(id_target)
    paths_bases_globais_list=paths_bases_globais(path_root,folderYear)
    i=-1
    for exist in range(4):
        i=i+1
        if not os.path.isfile(os.path.join(paths_bases_globais_list[i],file_target[i])):
            try:
                download_ftp("geoftp.ibge.gov.br",paths_bases_globais_list,folderYear,id_target,file_target)
            except gaierror:
                print('Sem conexão com o servidor ftp://geoftp.ibge.gov.br')
                logs_info('Sem conexão com servidor ftp://geoftp.ibge.gov.br')
            except ftplib.error_perm:
                logs_info('Arquivo '+file_target[i]+' não encontrado')
                print('Arquivo '+file_target[i]+' não encontrado')
                aa=True
            try:
                extracts(paths_extracts,paths_bases_globais_list,file_target)
                paths_extracts.clear()
            except FileNotFoundError:
                print('Erro de extração de dados, FileNotFoundError')
                logs_info('Arquivo '+file_target[i]+' não encontrado para extraçao')
            except zipfile.BadZipFile:
                logs_info('Arquivo '+file_target[i]+' não encontrado para extraçao')
                print('Erro de extração de dados, FileNotFoundError')
        msn='Arquivo da base '+file_target[i]+' já existente em '+str(paths_bases_globais_list[i])
        print(msn)
        logs_info(msn)
    
    
    del paths_bases_globais_list
    del folderYear
    del id_target
    del file_target
    
    
def rotina_manual(dia,mes,ano):
    
    paths_bases_globais_list=[]
    paths_extracts=[]
    folderYear=''
    id_target=''
    file_target=[]
    folderYear=str(ano)
    local_Bases_Folders(path_root,folderYear)
    id_target=str(conversao_dia(dia,mes,ano))
    file_target=names_File_Target(id_target)
    paths_bases_globais_list=paths_bases_globais(path_root,folderYear)
    i=-1
    for exist in paths_bases_globais_list:
        i=i+1
        if not os.path.isfile(os.path.join(paths_bases_globais_list[i],file_target[i])):
            try:
                download_ftp("geoftp.ibge.gov.br",paths_bases_globais_list,folderYear,id_target,file_target)
            except gaierror:
                print('Sem conexão com o servidor ftp://geoftp.ibge.gov.br')
                logs_info('Sem conexão com servidor ftp://geoftp.ibge.gov.br')
            except ftplib.error_perm:
                logs_info('Arquivo '+file_target[i]+' não encontrado')
                print('Arquivo '+file_target[i]+' não encontrado')
                aa=True
            try:
                extracts(paths_extracts,paths_bases_globais_list,file_target)
                paths_extracts.clear()
            except FileNotFoundError:
                print('Erro de extração de dados, FileNotFoundError')
                logs_info('Arquivo '+file_target[i]+' não encontrado para extraçao')
            except zipfile.BadZipFile:
                logs_info('Arquivo '+file_target[i]+' não encontrado para extraçao')
                print('Erro de extração de dados, FileNotFoundError')    
        print('Arquivo da base '+file_target[i]+' já existente em '+str(paths_bases_globais_list[i]))
    
    del paths_bases_globais_list
    del folderYear
    del id_target
    del file_target
    
    
# ----------------------------------------------------fluxo principal ---------------------------------------------------------#


r=False
l1=True
while l1:
    print('Deseja escolher alguma data específica para baixar a base? (30)segundos para responder')
    print('digite "yes" para escolher uma data')
    print('digite "no" para deixar baixar automaticamente')
    resp=input()
    if resp == 'yes':
        r=True
        l1=False
    elif resp =='no':
        r=False
        l1=False
    else:
        print('Favor inserir uma resposta válida yes ou no')
        l1=True

if r:
    l5=True
    while l5:
        l2=True
        while l2:
            try:
                dia=int(input('Qual dia?\n'))
                if dia >31 or dia<=0:
                    print('favor inserir valor entre 1 a 31')
                    raise ValueError   
                l2=False
            except ValueError: 
                print('Favor inserir apenas número correspondendo ao dia da base a ser baixada')
                l2=True
        l3=True
        while l3:        
            try:
                mes=int(input('Qual mês?\n'))
                if mes >12 or mes<=0:
                    print('favor inserir valor entre 1 a 12')
                    raise ValueError
                l3=False
            except ValueError: 
                print('Favor inserir apenas número correspondendo o mês')
                l3=True
        l4=True
        while l4:        
            try:
                ano=int(input('Qual ano\n'))
                if ano<2015 or ano>now1.year :
                    print('favor inserir valor entre 2015 a ',now1.year)
                    raise ValueError  
                l4=False
            except ValueError:
                print('Favor inserir apenas número correspondendo o ano')
                l4=True       
        try:
            alvo=conversao_dia(dia,mes,ano)
            l5=False
        except ValueError: 
            print('Data não existente, favor digitar uma data existente')
            l5=True
    rotina_manual(dia,mes,ano)
    
else:
    pass

aa=True
day=0
bb=0
while aa and bb<=5 and not r: # variável bb determina quantos arquivos para trás podem ser baixados em modo automático
    day=day+1
    bb=bb+1 #evita loop infinito, caso o site esteja off-line
    rotina_auto(day)
    
