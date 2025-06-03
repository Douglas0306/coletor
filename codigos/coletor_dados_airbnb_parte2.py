#Bibliotemas usadas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import re
import numpy as np

#Abre o site do Airbnb
navegador = webdriver.Chrome()
time.sleep(1)
navegador.get('https://www.airbnb.com.br/')
navegador.maximize_window()

time.sleep(5)

# Clicar no botão de busca ao abrir o site
try:
        botao =  navegador.find_element(By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[1]/div[2]/div[1]/div/div/header/form/div[1]/div/div[2]/div[3]')
        botao.click()
except:
        botao = navegador.find_element(By.XPATH, '//*[@id="search-tabpanel"]/div/div[5]/div[2]/div[2]/button/div')
        botao.click()

#Espera para clicar em filtro
time.sleep(2)


# Caso aparece um pop-up na tela, ele clica em fechar.
try:
        fechar = navegador.find_element(By.XPATH, '/html/body/div[9]/div/div/section/div/div/div[2]/div/div[1]/button/span')
        fechar.click()
except:
        pass

time.sleep(1)

#Clica em filtros
filtro = navegador.find_element(By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[1]/div[2]/header/div/div/div/div/div/form/div[1]/div/div[2]/div[2]/div/div/button/span/span')
filtro.click()

#printa a tela pra conseguir encontrar algum erro
#navegador.save_screenshot('antes_do_clique.png') 

#Realiza o filtro desejado(Espaço Inteiro) e o aplicar
acomodacao = navegador.find_elements(By.CSS_SELECTOR,'.osvx7gw.atm_mk_h2mmj6.atm_wq_egatvm.dir.dir-ltr')
for i in acomodacao:
        if 'Espaço inteiro' in i.text:
                i.click()
                break
time.sleep(2)

resultado = navegador.find_element(By.CSS_SELECTOR, '.p13966et.atm_7l_1p8m8iw.dir.dir-ltr')
resultado.click()
time.sleep(2)

pop = navegador.find_element(By.XPATH, '//*[@id="react-application"]/div/div/div[1]/div/div[2]/section/div/div[2]/div[1]/button')
pop.click()

time.sleep(2)

local = navegador.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[1]')
descricao = navegador.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[3]')
resumo = navegador.find_element(By.XPATH,'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[4]')
data = navegador.find_element(By.XPATH,'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[5]')
valor = navegador.find_element(By.XPATH,'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[6]')
avl = navegador.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[7]')
noite = navegador.find_element(By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[1]/div/div[2]/div/div/div/div/div/div[2]/div[6]/div[2]/div/div/span/div[2]/span')


# Listas para armazenar os dados
lista_loc = []
lista_desc = []
lista_res = []
lista_date = []
lista_noi = []
lista_valor = []
lista_avl = []

contador = 0
pagina_atual = 1
max_paginas = 15
MAX_RESULTADOS = 300

while pagina_atual <= max_paginas and contador < MAX_RESULTADOS:
    print(f"\nProcessando página {pagina_atual}...")
    
    # Determinar número de cards na página até o momento sempre 18, mais pode variar
    num_cards = len(navegador.find_elements(By.XPATH, '//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div'))
    print(f"Encontrados {num_cards} cards nesta página")
    
    for i in range(1, num_cards + 1):
        if contador >= MAX_RESULTADOS:
            break
            
        try:
            # Localização
            dado_loc = navegador.find_element(By.XPATH, 
                f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[1]').text
            lista_loc.append(dado_loc)
            
            # Descrição
            dado_desc = navegador.find_element(By.XPATH,
                f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[3]').text
            lista_desc.append(dado_desc)
            
            # Detalhaes
            dado_res = navegador.find_element(By.XPATH,
                f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[4]').text
            lista_res.append(dado_res)
            
            # Datas
            dado_date = navegador.find_element(By.XPATH,
                f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[5]').text
            lista_date.append(dado_date)
            
            # Quantidade de noites
            try:
                try:
                    dado_noi = navegador.find_element(By.XPATH,
                        f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[6]/div[2]/div/div/span/div[2]/span').text
                except NoSuchElementException:
                    dado_noi = navegador.find_element(By.XPATH, 
                        f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[6]/div[2]/div/div/span/div/span').text
                lista_noi.append(dado_noi)
            except NoSuchElementException:
                print(f'O valor não foi encontrado no car {i} - desconhecido')
                
            # VALOR (com tentativa para ambos os formatos)
            try:
                # Primeiro tenta o formato sem desconto
                try:
                    dado_valor = navegador.find_element(By.XPATH,
                        f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[6]/div[2]/div/div/span/div[1]/div/span/div/button/span[1]').text
                except NoSuchElementException:
                    # Se não encontrar, tenta o formato com desconto
                    dado_valor = navegador.find_element(By.XPATH,
                        f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[6]/div[2]/div/div/span/span/span[1]/span[2]/div/button/span[1]').text                
                lista_valor.append(dado_valor)
            except NoSuchElementException:
                print(f"Valor não encontrado no card {i} - formato desconhecido")
                lista_valor.append("N/A")
            
            # Avaliações
            try:
                dado_avl = navegador.find_element(By.XPATH,
                    f'//*[@id="site-content"]/div/div[2]/div/div/div/div/div/div[{i}]/div/div[2]/div/div/div/div/div/div[2]/div[7]').text
                lista_avl.append(dado_avl)
            except NoSuchElementException:
                lista_avl.append("N/A")
            
            contador += 1
            print(f"Card {i} processado com sucesso (Total: {contador})")
            
        except Exception as e:
            print(f"Erro ao processar card {i}: {str(e)}")
            continue
    
    if contador >= MAX_RESULTADOS:
        print(f"\nLimite de {MAX_RESULTADOS} resultados atingido!")
        break
        
    # Paginação
    try:
        proxima_pagina = navegador.find_element(By.XPATH, '//a[@aria-label="Próximo" or @aria-label="Next"]')
        proxima_pagina.click()
        time.sleep(3)  # Espera para carregar nova página
        pagina_atual += 1
    except NoSuchElementException:
        print("\nNão há mais páginas disponíveis")
        break
    except Exception as e:
        print(f"\nErro ao mudar de página: {str(e)}")
        break

print("\n--- COLETA FINALIZADA ---")
print(f"Total de itens coletados: {contador}")
print(f"Localizações: {len(lista_loc)} | Valores: {len(lista_valor)} | Avaliações: {len(lista_avl)}")


# Tranformando listas em Tabelas
tabela1 = pd.DataFrame(lista_loc, columns=['localizacao'])
tabela1

tabela2 = pd.DataFrame(lista_desc, columns=['descricao'])
tabela2

tabela3 = pd.DataFrame(lista_res, columns=['detalhe_segundario'])
tabela3

tabela4 = pd.DataFrame(lista_date, columns=['data'])
tabela4

tabela5 = pd.DataFrame(lista_noi, columns=['qtd_noites'])
tabela5

tabela6 = pd.DataFrame(lista_valor, columns=['valor'])
tabela6

tabela7 = pd.DataFrame(lista_avl, columns=['avaliacao'])
tabela7

# Concatenação das Tabelas
df = pd.concat([tabela1, tabela2, tabela3, tabela4, tabela5, tabela6, tabela7], axis=1)

# Não Mecher, pode dar erro lá na frente
#Faz a exportação do DataFrame não tratado pro arquivo base_original
df.to_csv('../base_original/base_original.csv', index=False)

# Extrai a nota média, considerando vírgula ou ponto decimal
df['nota_media'] = df['avaliacao'].str.extract(r'(\d+,\d+|\d+\.\d+)')[0]
df['nota_media'] = df['nota_media'].str.replace(',', '.', regex=False).astype(float)

# Extrai quantidade de avaliações e trata valores ausentes usando tipo nullable Int64
df['qtd_avaliacoes'] = df['avaliacao'].str.extract(r'(\d+)\s+avaliações')[0]
df['qtd_avaliacoes'] = df['qtd_avaliacoes'].astype('Int64')

# Limpa o valor, removendo 'R$' e espaços extras e o '.', para vazio
df['valor'] = df['valor'].str.replace('R$', '', regex=False).str.strip()
df['valor'] = df['valor'].str.replace('.', '', regex=False).str.strip()
df['valor'] = df['valor'].astype(float)

# Extrai a quantidade de noites assumindo formato "X noites"
df['qtd_noites'] = df['qtd_noites'].str.extract(r'(\d+)')[0]  # Extrai número
df['qtd_noites'] = df['qtd_noites'].fillna('0')             # Substitui NaN por '0'
df['qtd_noites'] = df['qtd_noites'].astype(int)      
 
df['detalhe_segundario'] = df['detalhe_segundario'].str.split('\n').str[0]
df['data'] = df['data'].str.split('\n').str[0]

#Exclusão da coluna avaliação
df.drop('avaliacao', axis=1, inplace=True)

# Define o número máximo de linhas e colunas exibidas
pd.set_option('display.max_rows', 200)  # Você pode ajustar esse valor como quiser
pd.set_option('display.max_columns', 20)


# Usando a coluna 'valor' do DataFrame df
valores = df['valor'].dropna()  # Remove valores nulos para cálculo correto

# Cálculo de BoxPlot
mediana = np.median(valores)
Q1 = np.percentile(valores, 25, method='midpoint')
Q3 = np.percentile(valores, 75, method='midpoint')
IQR = Q3 - Q1
MAXIMO = Q3 + 1.5 * IQR
MINIMO = Q1 - 1.5 * IQR

# Identificador de outliers
OUTLIER = [] 

for i in valores:
    if i < MINIMO or i > MAXIMO:
        OUTLIER.append(i) 

# TRATAMENTO DE NULOS
df['valor'].fillna(0, inplace=True)
df['nota_media'].fillna(0, inplace=True)
df['qtd_avaliacoes'].fillna(0, inplace=True)

# TRATAMENTO DE OUTLIERS 
# Definir limites

df.loc[df['valor'] > MAXIMO, 'valor'] = MAXIMO
df.loc[df['valor'] < MINIMO, 'valor'] = MINIMO

df = df.drop_duplicates()

#Faz a exportação do DataFrame já tratado pro arquivo base_original
df.to_csv('../base_tratada/base_tratada.csv', index=False)


