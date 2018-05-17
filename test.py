import main

# testes unitários


def test_rotina_auto(day):

    main.rotina_auto(1,True,False,day,False)


def test_rotina_manual(dia,mes,ano):
    main.rotina_manual(dia,mes,ano)


# testes rotina auto    

# print(test_rotina_auto(1)) # sucess
# print(test_rotina_auto(9)) # sucess
# print(test_rotina_auto(10)) # sucess
# print(test_rotina_auto(100)) # sucess
# print(test_rotina_auto(102)) # sucess
# print(test_rotina_auto(301)) #sucess

# testes rotina manual

dt=[1,28,31,1,1,10,29] 
mt=[2,2,2,12,1,10,2]
at=[2016,2016,2017,2017,2018,2016,2016]
i=-1
for test in at:
    i = i+1
    print("teste dia %d, mes %d , ano %d." %(dt[i],mt[i],at[i]))
    main.time.sleep(3)
    print(test_rotina_manual(dt[i], mt[i], at[i]))
    

# teste dia 1, mes 2 , ano 2016. sucess
# teste dia 28, mes 2 , ano 2016. sucess
# teste dia 31, mes 2 , ano 2017. sucess 
# teste dia 1, mes 12 , ano 2017. sucess
# teste dia 10, mes 10, ano 2016. sucess
# teste dia 29, mes 2, ano 2016. sucess

def test_check():
    pass


def primeira_etapa():
    pass


def segunda_etapa():
    pass
