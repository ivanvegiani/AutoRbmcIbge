# coding: utf-8
# version:1.0
# python 3
# ftp://geoftp.ibge.gov.br/informacoes_sobre_posicionamento_geodesico/rbmc/dados/
# implementado sob o paradigma procedural
# 1

"""
version:1.0
author: Jose Ivan Silva Vegiani
Automacao de download e descompactação de dados do rbmc (IBGE)
rbmc: Rede Brasileira de Monitoramento Contínuo dos Sistemas GNSS
Script de código aberto e livre, cedido gratuitamente pelo autor.
Parâmetros para download:
Estações: Cascavel, Maringá, Curitiba e Guarapuava
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
import threading
import sys
import schedule
from sys import exit
import signal

# variaveis globais
baseFolder='Cascavel','Maringá','Curitiba','Guarapuava'
path_root='c:\IBGE'
day=0
folderYear=0

# instanciando o tempo
now1 = datetime.datetime.now()
year=str(now1.year)
# configurando métodos dos logs
format0='%(asctime)s - %(message)s'
logging.basicConfig(filename='log'+year+'.txt',level=logging.DEBUG, format=format0,datefmt='%d/%m/%y %I:%M:%S %p')


def logs_info(mensagem): #log de informação
    logging.info(mensagem)

def logs_bug(nome_variavel,variavel):  # log para debug, utilizado somente em desenvolvimento
    logging.debug('debug '+nome_variavel+': '+variavel)

def date2doy(date): # biblioteca de terceiros, https://github.com/purpleskyfall/gnsscal

    """Convert date to day of year, return int doy.
    Example:
    >>> from datetime import date
    >>> date2doy(date(2017, 5, 17))
    137
    """
    first_day = datetime.date(date.year, 1, 1)
    delta = date - first_day
    return delta.days + 1

def folder_year_function(day_delay): # define a pasta local relativo ao ano
    """ day_delay é os dias subtraidos ao dia atual"""

    now = datetime.datetime.now()
    today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
    logs_bug('today_gnss',str(today_gnss))
    day_target=today_gnss-day_delay

    if  day_target <= 0  :
        folderYear =str(int(now.year)-1)
    else:
        folderYear =str(now.year)
    return folderYear

def bissexto(folderYear): # verificação para ver se o ano é bissexto
    """ retorno booleano verdadeiro se o ano é bissexto"""
    year=int(folderYear)
    if (year % 100) != 0 and (year % 4) == 0 or (year % 400) == 0:
        return True
    else:
        return False

def id_target_function(day_delay,delay=True): # define o alvo
    """ Retorna id_target (identificação do dia alvo)"""
    if delay:
        now = datetime.datetime.now()
        today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
        day_target=today_gnss-day_delay
    else:
        day_target=day_delay
   
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


def local_bases_folders(path_root,folderYear): # define as pastas locais referentes as bases
    i1=0
    for path in baseFolder:
        if not os.path.exists(os.path.join(path_root,folderYear,baseFolder[i1])):
            os.makedirs(os.path.join(path_root,folderYear,baseFolder[i1]))
        i1=i1+1

def names_file_target(id_target): # define os nomes dos arquivos para busca
    # Cascavel: prcv , Maringá: prma, Curitiba:ufpr e Guarapuava:prgu
    sufix_file=id_target+"1"+".zip"
    file_target=["prcv"+sufix_file,"prma"+sufix_file,"ufpr"+sufix_file,"prgu"+sufix_file]
    return file_target

def download_ftp(address,paths_bases_globais_list,folderYear,id_target,file_target,prin=True): # metodo para download da rbmc
    site_address=address
    ftp=ftplib.FTP(site_address)
    ftp.login()
    dir_cwd = str("informacoes_sobre_posicionamento_geodesico/rbmc/dados"+'/'+folderYear+"/"+id_target)
    if prin:
        print (str(dir_cwd))
        print('\nConectado em ftp://geoftp.ibge.gov.br \n')
    ftp.cwd(str(dir_cwd))
    i=-1
    for p in file_target:
        i=i+1
        logs_bug("In download: file target",str(file_target[i]))
        logs_bug("In download: file target list",str(file_target))
        logs_bug("In download: path_global_list ",str(paths_bases_globais_list[i]))
        p = open(str(os.path.join(paths_bases_globais_list[i],file_target[i])), "wb")
        if prin:
            print('Downloading file '+file_target[i]+' para '+str(paths_bases_globais_list[i]))
        try:    
            ftp.retrbinary("RETR " + file_target[i], p.write)
            p.close()
            if prin:
                print('Download file '+file_target[i]+' sucess\n')
        except ftplib.error_perm:
            if prin:
                print('Arquivo '+file_target[i]+' não encontrado no servidor\n')
                logs_info('Arquivo '+file_target[i]+' não encontrado no servidor\n')
            p.close()
            os.remove(os.path.join(paths_bases_globais_list[i],file_target[i]))
            logs_bug("remove: path ",str(paths_bases_globais_list[i]))
        
        logs_info('Download file '+file_target[i]+' sucess')
        
    ftp.quit()

def paths_bases_globais(path_root,folderYear,prin=True):# define os endereços locais absolutos
    paths_bases_globais_list=[]
    del paths_bases_globais_list[:]
    i=0
    logs_bug("folderYear in rotina manual: ", folderYear)
    for p in baseFolder:
        paths_bases_globais0=os.path.join(path_root,folderYear,baseFolder[i])
        logs_bug("paths_bases_globais0: ", paths_bases_globais0)
        p1 = Path(paths_bases_globais0)
        logs_bug("objeto path: ", str(p1))
        paths_bases_globais_list.append(p1.resolve())
        logs_bug("paths_bases_globais_list: ", str(paths_bases_globais_list[i]))
        logs_bug("p1 resolve ", str(p1.resolve()))
        i=i+1     
    return paths_bases_globais_list

def extracts(paths_extracts,paths_bases_globais_list,file_target,prin=True): # define a descompactação do zip
    j=0
    for b in range(4):
        if not os.path.exists(os.path.join(str(paths_bases_globais_list[j]),"extracts")):
            os.makedirs(os.path.join(str(paths_bases_globais_list[j]),"extracts"))
        paths_extracts.append(os.path.join(str(paths_bases_globais_list[j]),"extracts"))
        j=j+1
    i=0
    for z in range(4):
        
        if prin:
            print('Extraindo para '+str(paths_extracts[i]))
        try:
            zip1 = zipfile.ZipFile(str(os.path.join(paths_bases_globais_list[i],file_target[i])))
            zip1.extractall(str(paths_extracts[i]))
            logs_info('Extraido '+file_target[i]+' com sucesso')
            zip1.close()     
        except:
            logs_info('Erro '+file_target[i]+' não encontrado')
        i=i+1
    

def dia_de_hoje(): # retorna o dia atual em gnss calendar
    now = datetime.datetime.now()
    today_gnss=int(date2doy(datetime.date(now.year,now.month,now.day)))
    return today_gnss

def conversao_dia(dia,mes,ano): # converte variáveis dia, mes e ano para gnss calendar
    var=datetime.date(ano,mes,dia)
    alvo=int(date2doy(datetime.date(var.year,var.month,var.day)))
    logs_bug('alvo',str(alvo))
    return alvo

def deploy_folders(return1,day):
    paths_bases_globais_list=[]
    paths_extracts=[]
    folderYear=''
    id_target=''
    file_target=[]
    folderYear=folder_year_function(day)
    local_bases_folders(path_root,folderYear)
    id_target=id_target_function(day)
    file_target=names_file_target(id_target)
    paths_bases_globais_list=paths_bases_globais(path_root,folderYear)
    if return1=='id_target':
        return id_target
    if return1=='file_target':
        return file_target
    if return1=='paths_bases_globais_list':
        return paths_bases_globais_list



def rotina_auto(loop=31,prin=True,only_check=False,day=0): # rotina principal automatica
    if day!=0:
        day=day
    else:
        day=0
    paths_bases_globais_list=[]
    paths_extracts=[]
    folderYear=''
    id_target=''
    file_target=[]
    folderYear=folder_year_function(day)
    local_bases_folders(path_root,folderYear)
    id_target=id_target_function(day)
    file_target=names_file_target(id_target)
    paths_bases_globais_list=paths_bases_globais(path_root,folderYear)
    if only_check:
        control=True
        soma_files=0

    if prin:
        print('Entrando em modo automático')
        time.sleep(3)

    if only_check:
        i=-1
        list_file=[]

        for b1 in baseFolder:
            i=i+1
            list_dir=(os.path.join(paths_bases_globais_list[i]))
            list_dir_file=os.listdir(list_dir)
            number_files = len(list_dir_file)
            soma_files=number_files+soma_files

    else:
        for a1 in range(loop): # variável bb determina quantos arquivos para trás podem ser baixados em modo automático
            paths_bases_globais_list=[]
            paths_extracts=[]
            folderYear=''
            id_target=''
            file_target=[]
            folderYear=folder_year_function(day)
            local_bases_folders(path_root,folderYear)
            id_target=id_target_function(day)
            file_target=names_file_target(id_target)
            paths_bases_globais_list=paths_bases_globais(path_root,folderYear)
            i=-1
            for exist in range(4):

                i=i+1
                if not os.path.isfile(os.path.join(paths_bases_globais_list[i],file_target[i])):
                    if not only_check:
                        try:
                            if prin:
                                download_ftp("geoftp.ibge.gov.br",paths_bases_globais_list,folderYear,id_target,file_target)
                                extracts(paths_extracts,paths_bases_globais_list,file_target)
                            else:
                                download_ftp("geoftp.ibge.gov.br",paths_bases_globais_list,folderYear,id_target,file_target,prin=False)
                                extracts(paths_extracts,paths_bases_globais_list,file_target,prin=False)
                                paths_extracts.clear()
                        except gaierror:
                            if prin:
                                print('Sem conexão com o servidor ftp://geoftp.ibge.gov.br')
                            logs_info('Sem conexão com servidor ftp://geoftp.ibge.gov.br')
                        except ftplib.error_perm:
                            logs_info('Arquivo '+file_target[i]+' não encontrado')
                            if prin:
                                print('Arquivo '+file_target[i]+' não encontrado')
                        # try:
                        #     if prin:
                        #         extracts(paths_extracts,paths_bases_globais_list,file_target)
                        #     else:
                        #         extracts(paths_extracts,paths_bases_globais_list,file_target,prin=False)

                        except FileNotFoundError:
                            if prin:
                                print('Erro de extração de dados, FileNotFoundError')
                            logs_info('Arquivo '+file_target[i]+' não encontrado para extraçao')
                        except zipfile.BadZipFile:
                            logs_info('Arquivo '+file_target[i]+' não encontrado para extraçao')
                            if prin:
                                print('Erro de extração de dados, FileNotFoundError')
                else:
                     pass
                logs_info('Arquivo da base '+file_target[i]+' existente em: '+str(paths_bases_globais_list[i]))

            day=day+1

    del paths_bases_globais_list
    del folderYear
    del id_target
    del file_target

    if  only_check:
        return (soma_files-4) # subtraindo as 4 pastas extracts, para não aparecer na contagem
    else:
        pass

def rotina_manual(dia,mes,ano): # rotina principal manual
    paths_bases_globais_list=[]
    del paths_bases_globais_list[:]
    logs_bug(" del paths_bases_globais_list[:]",str(paths_bases_globais_list[:]))
    paths_extracts=[]
    del paths_extracts[:]
    folderYear=''
    id_target=''
    file_target=[]
    del file_target[:]
    folderYear=str(ano)
    local_bases_folders(path_root,folderYear)
    id_target=id_target_function((conversao_dia(dia,mes,ano)),delay=False)
    file_target=names_file_target(id_target)
    logs_bug("file_target in rotina manual",str(file_target))
    paths_bases_globais_list=paths_bases_globais(path_root,folderYear)
    i=-1
    for exist in range(4):
        i=i+1
        logs_bug('paths_bases_globais_list[i]',str(paths_bases_globais_list[i]))
        if not os.path.isfile(os.path.join(paths_bases_globais_list[i],file_target[i])):
            try:
                download_ftp("geoftp.ibge.gov.br",paths_bases_globais_list,folderYear,id_target,file_target)
            except gaierror:
                print('Sem conexão com o servidor ftp://geoftp.ibge.gov.br')
                logs_info('Sem conexão com servidor ftp://geoftp.ibge.gov.br')
            except ftplib.error_perm:
                logs_info('Arquivo '+file_target[i]+' não encontrado')
                print('Arquivo '+file_target[i]+' não encontrado')
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

# def thread2(name,th2):
#    schedule.every().day.at(th2).do(rotina_auto)
#    while True:
#     schedule.run_pending()
#     time.sleep(1*60)

def thread3(name,th3):
    check=rotina_auto(prin=False,only_check=True)
    t3.check=check

def interacao_user():
    print('Entrando em modo manual')
    time.sleep(3)
    l2=True
    while l2:
        try:
            dia=int(input('Qual dia?\n'))
            if dia >31 or dia<=0:
                print('favor inserir valor entre 1 a 31')
                l2=True
                raise ValueError
            else:
                l2=False
        except ValueError:
            print('Favor inserir apenas número correspondendo ao dia da base a ser baixada')
            l2=True
    l3=True
    while l3:
        try:
            mes=int(input('Qual mês?\n'))
            if mes >12 or mes<=0:
                print('favor inserir um valor que corresponde ao mês entre 1 a 12')
                raise ValueError
            else:
                l3=False
        except ValueError:
            print('Favor inserir apenas número correspondendo o mês')
            l3=True
    l4=True
    while l4:
        try:
            ano=int(input('Qual ano\n'))
            if ano <2016 or ano>now1.year:
                print('favor inserir valor entre 2015 a ',now1.year)
                raise ValueError
            else:
                l4=False
        except ValueError:
            print('Favor inserir apenas número correspondendo ao ano')
            l4=True
        try:
            #alvo=conversao_dia(dia,mes,ano)
            rotina_manual(dia,mes,ano)
        except ValueError:
            print('Data não existente, favor digitar uma data existente')
            interacao_user()
    lf=True        
    while lf:                
        print('Deseja fazer download de mais uma base?')
        resp0=input('y/n\n')
        try:
            if resp0=='y' or resp0=='n':
                if resp0=='y':
                    interacao_user()
                else:
                    lf=False
                    print('Fim da aplicação')
<<<<<<< HEAD
                    os._exit(1)     
=======
                    os._exit(1)
                    
>>>>>>> af92557ae451b8d7dd8382423c946af11d200e77
            else:
                raise ValueError
        except ValueError:
            print('Favor responda somente y para sim ou n para não')
            
def show_files():
        print('\nExibindo arquivos contidos em C:\IBGE:\n')
        time.sleep(3)
        path=[]
        paths_bases_globais_list=[]
        folderYear=''
        id_target=''
        file_target=[]
        folderYear=folder_year_function(day)
        local_bases_folders(path_root,folderYear)
        id_target=id_target_function(day)
        file_target=names_file_target(id_target)
        paths_bases_globais_list=paths_bases_globais(path_root,folderYear)
        i=-1
        for ai in range(4):
            i=i+1
            path.append(paths_bases_globais_list[i])
            print('Arquivos contidos em: '+baseFolder[i]+str(os.listdir(path[i])))
            logs_info('Arquivos contidos em: '+baseFolder[i]+str(os.listdir(path[i])))


def interrupted(signum, frame): # funciona apenas no linux
#     "called when read times out"
    print ('Aplicação finalizada')
    sys.exit()

def watchdog():
  print('Aplicação finalizada')
  # time.sleep(10)
  os._exit(1)

# ----------------------------------------------------fluxo principal ---------------------------------------------------------#

def primeira_etapa():
    pass
# Primeira etapa --------------------------------------------------------------------------------------------------------------#
# t1 = threading.Thread(target=thread1, args=('task1','none')) # verifica e baixa até 31 arquivos de bases dos dias anteriores
# t2 = threading.Thread(target=thread2, args=('task2','22:30')) # agenda para baixar automaticamente todos os dias às 23:30
t3 = threading.Thread(target=thread3, args=('task13','none')) # verifica quantos arquivos de base há no em local
t3.start()
print('As bases por este programa, serão baixadas e descompactadas automaticamente em C:\IBGE\n')
time.sleep(5)
print('Aguarde enquanto faremos algumas verificações')
time.sleep(2)
t3.join()
print('\nFoi verificado que há ao todo há %d arquivos de bases em C:\IBGE\n '%t3.check)
time.sleep(3)
print('Verificando se há arquivos recentes no servidor do IBGE para serem baixados\n')
time.sleep(3)
rotina_auto(loop=31,prin=True,only_check=False)
print('Foi verificado e atualizado os arquivos recentes com sucesso')
show_files()


def segunda_etapa():
    pass


# Segunta etapa --------------------------------------------------------------------------------------------------------------#

delay_time = 60   # delay time in seconds
alarm = threading.Timer(delay_time, watchdog)
alarm.start()
print('\nDigite qualquer coisa para entrar em modo manual, e baixar uma base que você quiser\n')
print('Em 60 segundos de ociosiadade a aplicação irá se auto desligar')
print('Digite enter para continuar e escolher uma base para download')
input()
alarm.cancel()# disable the alarm after success
interacao_user()
