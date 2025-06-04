import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
df = pd.read_csv('base_tratada/base_tratada.csv', sep=',')

#lista_colunas = df.columns.tolist() Tentativa falha de definir 'Choose an option' como valor padrão no Streamlit para não selecionar automaticamente a localização (já que é o primeiro valor da coluna) 
#Eu até consegui, mais fica aparecendo como ops pro usuário. 😿
#lista_colunas.insert(0, 'Choose an option')
#if cl1 == 'Choose an option':
#    st.info("Por favor, selecione uma coluna para ver as análises univariadas.")'''

#Grafico de Histograma da coluna escolhida pelo usuário

st.title('Estatisticas Gerais')
lista_colunas = df.columns
gr = st.selectbox('Selecine uma coluna para ver seus dados ***Estatisticos***.', lista_colunas)
if gr in ('qtd_noites', 'valor', 'qtd_avaliacoes', 'nota_media'):
    media = df[gr].mean()
    desvio = df[gr].std()
    mediana = df[gr].quantile(0.5)
    maximo = df[gr].max()
    st.write(
    f"A coluna {gr}, possui uma média de {media:.2f}. \n"
    f"Seu desvio padrão indica que, quando há desvio, desvia em média {desvio:.2f}. \n"
    f"E 50% dos dados vão até o valor {mediana:.2f}. E seu máximo é de {maximo:.2f}.")

else:
    st.write(f'A coluna **{gr}** não possui dados numéricos e, portanto, não é possível gerar dados estatísticos.')

lista_colunas = df.columns
st.title('Gráficos Univariados')
cl1 = st.selectbox('Escolha a coluna desejada:',lista_colunas, key='grafico_histograma')


# Verifica se a coluna selecionada está na lista de colunas esperadas
    # Se sim, mostra na tela do usuario os valores estátisticos
    # Se não, informa que não há dados numeros na coluna selecionada
if cl1 in ('qtd_noites', 'valor', 'qtd_avaliacoes', 'nota_media'):
    media = df[cl1].mean()
    desvio = df[cl1].std()
    mediana = df[cl1].quantile(0.5)
    maximo = df[cl1].max()
    minimo = df[cl1].min()
    num_cln = len(df[cl1])
    st.write(f"Este histograma apresenta a distribuição de frequência da coluna '{cl1}', \n"
             f"revelando a forma dos dados e suas faixas de valores \n"
             f"predominantes.\nTotalizando {num_cln} observações, os valores exibidos variam \n"
             f"de {minimo:.2f} a {maximo:.2f}")

else:
    st.write(f'A coluna **{cl1}** não possui dados numéricos e, portanto, não é possível gerar dados estatísticos.')
st.write('Histograma')
fig = px.histogram(df,x=[cl1])
st.plotly_chart(fig)

#Gráficco de Caixa da coluna escolhida pelo usuário
cl2 = st.selectbox('Escolha a coluna desejada:',lista_colunas, key='grafico_boxplot')
if cl2 in ('qtd_noites', 'valor', 'qtd_avaliacoes', 'nota_media'):
    q1 = df[cl2].quantile(0.25)
    mediana = df[cl2].quantile(0.5)
    q3 = df[cl2].quantile(0.75)
    iqr = q3 - q1
    #Identificação de Outliers
    maximo = q3 + 1.5 * iqr
    minimo = q1 - 1.5 * iqr
    outliers = df[cl2][(df[cl2] < minimo) | (df[cl2] > maximo)]
    total_out = len(outliers)
    st.write(
    f"O boxplot abaixo fornece uma visão concisa da **distribuição dos dados** de '{cl2}'.\n"
    f"- A **linha central** dentro da caixa representa a **mediana**: **{mediana:.2f}**.\n"
    f"- A caixa em si delimita o **intervalo interquartil (IQR)**, indo do **1º Quartil (Q1)** em **{q1:.2f}** ao **3º Quartil (Q3)** em **{q3:.2f}**. Isso significa que 50% dos dados centrais estão dentro desta faixa.\n"
    f"- Os 'bigodes' (whiskers) se estendem para mostrar a amplitude dos dados não atípicos.\n"
    f"- Pontos individuais fora dos bigodes são **valores atípicos (outliers)**. Foram identificados **{total_out}** outliers, indicando valores que se desviam significativamente do padrão da maioria dos dados.")
else:
    st.write(f'A coluna **{cl2}** não possui dados numéricos e, portanto, não é possível gerar dados estatísticos.')

st.write('BoxPlot')
fig2 = px.box(df, x=[cl2])
st.plotly_chart(fig2)

cl3 = st.selectbox('Escolha a coluna desejada:',lista_colunas, key='grafico_linhas')

if cl3 in ('qtd_noites', 'valor', 'qtd_avaliacoes', 'nota_media'):
    media = df[cl3].mean()
    desvio = df[cl3].std()
    mediana = df[cl3].quantile(0.5)
    maximo = df[cl3].max()
    minimo = df[cl3].min()
    qtd_obs = len(df[cl3])
    st.write(
            f"Este gráfico de linha mostra a **sequência individual dos valores** da coluna '{cl3}'."
            f"Os valores na linha variam de **{minimo:.2f}** a **{maximo:.2f}**, representando **{qtd_obs}** observações.\n"
            f"Observe as flutuações para entender a **variabilidade ou padrão de sequência** dos dados."
        )
else:
    st.write(f'A coluna **{cl3}** não possui dados numéricos e, portanto, não é possível gerar dados estatísticos.')

st.write('Graficos de Linhas')
st.line_chart(df[cl3])

# Grafico de Dispersão
st.title("Gráficos Multivariados")
lista_colunas_numericas = df.select_dtypes(include=np.number).columns.tolist()
lc1 = st.multiselect(
    'Selecione as colunas desejadas para o gráfico de dispersão (2 colunas):',
    lista_colunas_numericas, # <-- AQUI! Só colunas numéricas são mostradas.
    max_selections=2
)
if  len(lc1) == 2:
    eixo_x = lc1[0]
    eixo_y = lc1[1]
    qtd_obs2 = len(df)
    correlacao = df[eixo_x].corr(df[eixo_y])
    st.write('Gráfico de Dispersão')
    f"Este gráfico de dispersão visualiza a **relação entre '{eixo_x}' (eixo X) e '{eixo_y}' (eixo Y)**. "
    f"Cada ponto representa uma das **{qtd_obs2}** observações no seu conjunto de dados.\n"
    f"A **correlação de Pearson** entre estas duas variáveis é de **{correlacao:.2f}**."
    graf4 = px.scatter(df, x=lc1[0], y=lc1[1])
    st.plotly_chart(graf4)
elif len(lc1) > 2:
    st.error('Escolha apenas duas colunas')
lc2 = st.multiselect('Faça a escolha das colunas desejadas para ver o Gráfico de Colunas|Histograma',lista_colunas,  key='grafico_hitograma2')

if  len(lc2) == 2:
    eixo_x2 =  lc2[0]
    eixo_y2 = lc2[1]
    total_obs = len(df)
    st.write(
            f"Este histograma mostra a **distribuição da coluna '{eixo_x2}'**, "
            f"onde a altura das barras (eixo Y) representa a **soma dos valores de '{eixo_y2}'** "
            f"para cada faixa de '{eixo_x2}'.\n"
            f"Ele representa um total de **{total_obs}** observações. "
            f"Observe como os valores de '{eixo_y2}' se acumulam ou se distribuem em relação a diferentes faixas de '{eixo_x2}'."
        )
    st.write('Histograma')
    graf5 = px.histogram(df,x=lc2[0], y=lc2[1])
    st.plotly_chart(graf5)
elif len(lc2) > 2:
    st.error('Escolha apenas duas colunas.')


lc3 = st.multiselect('Faça a escolha das colunas desejadas para ver o grafico de Caixa|BoxPlot',lista_colunas,  key='grafico_caixa_categorico')
if  len(lc3) == 2:
    st.write('Grafico de Caixa Categorico')
    col_categorica_para_plot = lc3[0]
    col_numerica_para_plot = lc3[1]  
    
    num_obs_total = len(df) 
    st.write(
        f"Este gráfico de caixa (boxplot) compara a **distribuição da coluna numérica '{col_numerica_para_plot}'** "
        f"em relação às **diferentes categorias da coluna '{col_categorica_para_plot}'**.\n\n"
        f"Para cada categoria, a caixa exibe a **mediana (linha central)**, os **quartis (25% e 75%)** "
        f"e a **amplitude dos dados**; os pontos fora dos 'bigodes' indicam **valores atípicos (outliers)**.\n"
        f"O gráfico considera um total de **{num_obs_total}** observações.\n\n"
        f"Observe as variações na altura das caixas, na posição das medianas e na presença de outliers para "
        f"entender como a distribuição de '{col_numerica_para_plot}' difere entre os grupos de '{col_categorica_para_plot}'."
    )
    graf6 = px.box(df,x=lc3[0], y=lc3[1])
    st.plotly_chart(graf6)
elif len(lc3) > 2:
    st.error('Escolha apenas duas colunas.')








#st.title('1, 2, 3 | Testando 🤖 Gráficos')

#st.line_chart(df.sort_values('qtd_avaliacoes')[['valor']].set_index(df['qtd_avaliacoes']))
#st.line_chart(df.sort_values('qtd_avaliacoes')[['nota_media']].set_index(df['qtd_avaliacoes']))
