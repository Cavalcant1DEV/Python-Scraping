from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import datetime

options = Options()
dados_gerais = []
contador = 1
#options.add_argument('--headless')
#Deixa o código para rodar tudo de fundo, sem abrir o navegador

options.add_argument('window-size=1280,720')
nav = webdriver.Chrome(options=options)

#nav.get('https://www.linkedin.com/jobs/search?keywords=&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0')
#Buscando a página desejada

nav.get('https://www.linkedin.com/jobs/search?keywords=Marketing%20E%20Publicidade&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_JT=F&f_E=1&position=1&pageNum=0')
sleep(4)
#LINK DIRETO

# nav.find_element("xpath",'//*[@id="job-search-bar-keywords"]').send_keys('Marketing e Publicidade')
# nav.find_element("xpath",'//*[@id="jobs-search-panel"]/form/button').click()
# sleep(4)
# #Realizando a pesquisa por "Marketing e publicidade"

# nav.find_element("xpath",'//*[@id="jserp-filters"]/ul/li[4]/div/div/button').click()
# sleep(4)
# nav.find_element("xpath",'//*[@id="f_JT-0"]').click()
# sleep(4)
# nav.find_element("xpath",'//*[@id="jserp-filters"]/ul/li[4]/div/div/div/button').click()
# #Selecionando e aplicando o primeiro filtro de conteúdo

# nav.find_element("xpath",'//*[@id="jserp-filters"]/ul/li[5]/div/div/button').click()
# sleep(4)
# nav.find_element("xpath",'//*[@id="f_E-0"]').click()
# sleep(4)
# nav.find_element("xpath",'//*[@id="jserp-filters"]/ul/li[5]/div/div/div/button').click()
# sleep(6)
# #Selecionando e aplicando o segundo filtro

while(nav.find_element('xpath', '//*[@id="main-content"]/section[2]/ul/li['+str(contador) +']/div')):
    janela_1 = nav.current_window_handle
    
    dados = nav.find_element('xpath', '//*[@id="main-content"]/section/ul/li['+str(contador)+']/div/a')
    links = dados.get_attribute('href')
    #Armazenando as URLS
        
    nom_vagas = dados.find_element(By.CLASS_NAME, 'sr-only').text
    #Armazenando o Nome da Vaga
    
    try:
        candidaturas = nav.find_element(By.CLASS_NAME, 'num-applicants__caption').text
    #Buscando número de candidaturas
    
    except:
        candidaturas = 'Não informado'
    #Realizando tratamento caso não existam valores
    
    
    info_vagas = nav.find_elements(By.CSS_SELECTOR, 'span.description__job-criteria-text')
    contador_interno = 0
    for elementos in info_vagas:
        contador_interno += 1
        if(contador_interno == 1):
            tipo_contrato = elementos.text
            
        if (contador_interno == 2):
            jornada_contrato = elementos.text
            
        if(contador_interno > 2):
            break
    #Fazendo a varredura dos elementos
    
    url_emp = nav.find_element('xpath', '//*[@id="main-content"]/section[2]/ul/li['+str(contador)+']/div/div[2]/h4/a')
    link_emp = url_emp.get_attribute('href')
    #Armazenando o link da empresa
    
    tempo = nav.find_element(By.CSS_SELECTOR, 'time.job-search-card__listdate')
    hora_postagem = tempo.get_attribute('datetime')
    #Armazanendo horário da postagem
    
    nav.find_element(By.CSS_SELECTOR, 'a.topcard__org-name-link').click()
    #Acessando a página da empresa
    
    for windows_handle in nav.window_handles:
        if (windows_handle != janela_1):
            nav.switch_to.window(windows_handle)
            sleep(2)
            try:
                nome_da_emp = nav.find_element(By.CLASS_NAME,'top-card-layout__title').text
                #Armazenando o nome da empresa
                
                quant_fun_emp = nav.find_element(By.CSS_SELECTOR,'[data-test-id="about-us__size"]').text
                #Armazenando o número de funcionários
                sede_emp = nav.find_element(By.CSS_SELECTOR,'[data-test-id="about-us__headquarters"]').text
                try: 
                    num_seg_emp = nav.find_element(
                    By.CSS_SELECTOR, '.top-card-layout__first-subline').text
                    #Armazenando o número de seguidores
                except:
                    num_seg_emp = 'Não informado'
            except:
                nav.close()
                nav.switch_to.window(janela_1)
                nav.find_element(By.CSS_SELECTOR, 'a.topcard__org-name-link').click()

            nav.close()
            #Fecha a nova janela
            
            nav.switch_to.window(janela_1)
            #Retorna o foco para a main page
            try:
                nav.find_element('xpath','//*[@id="main-content"]/section[2]/button').click()
                
            except:
                print('Ignora')
    #Entrando na página da empresa e coletando dados
    
    dados_gerais.append({'Url_da_Vaga':links,'Nome_das_Vagas':nom_vagas,'Candidaturas':candidaturas,'Tipo_de_contrato':tipo_contrato, 'Estilo_de_contrato':jornada_contrato,'Url_da_empresa':link_emp,'Data_da_postagem':hora_postagem,'Nome_da_empresa':nome_da_emp,'Número_de_seguidores':num_seg_emp,'Quantidade_de_funcionários':quant_fun_emp,'Sede_da_emp':sede_emp})
    contador += 1
    #Aplicando o append nos dados
    
    arquivo = pd.DataFrame(dados_gerais)
    arquivo.to_csv('Scraping - Victor Hugo da Silva Cavalcanti.csv', index=False)
    #Salvando a execução
    
    print('ainda funcional')
    dados.click()
    #Selencionando o próximo elemento da varredura
    sleep(4)