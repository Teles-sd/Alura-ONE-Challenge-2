#!/usr/bin/env python
# coding: utf-8

# # Alura+ONE Challenge 2: Alura Store

# ## Análise de Dados

# ### Importação de dados
# 
# 

# In[ ]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# In[ ]:


url1 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja1 = pd.read_csv(url1)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)

lojas = [loja1, loja2, loja3, loja4]
lojas_str = [ f"Loja {n}" for n in range(1, 5) ]


# In[ ]:


loja1


# In[ ]:


print([len(loja) for loja in lojas])


# In[ ]:


print(loja1.info())


# ### 1\. Análise do faturamento
# 

# In[ ]:


faturamentos = [ loja['Preço'].sum() for loja in lojas ]

print( "Faturamentos:\n{}".format( ("\n".join( ( f'Loja {n}: R$ {val:_.2f}' for n,val in enumerate(faturamentos,start=1) ) )).replace(".",",").replace("_",".") ) )


# ### 2\. Vendas por Categoria
# 

# In[ ]:


# loja1[ ['Categoria do Produto','Preço'] ].groupby("Categoria do Produto").describe()
# loja1[ ['Categoria do Produto','Preço'] ].groupby("Categoria do Produto").count()


# In[ ]:


vendas_pCategoria = pd.concat([ loja[ ['Categoria do Produto','Produto'] ].groupby("Categoria do Produto").count().rename(columns={'Produto':f"Loja {n}"}) for n,loja in enumerate(lojas,start=1) ], axis=1)

print("Vendas de cada loja, por categoria:\n")
vendas_pCategoria


# ### 3\. Média de Avaliação das Lojas

# In[ ]:


avaliacao_media = pd.DataFrame(
    ((loja['Avaliação da compra'].mean(),loja['Avaliação da compra'].std()) for loja in lojas ),
    index=lojas_str,
    columns="media dp".split(),
)

# print( "Avaliação:\n{}".format( "\n".join( f"{loja:s}:  Média={media:.2f}  Desvio Padrão={dp:.2f}" for loja,media,dp in zip(avaliacao_media.index,avaliacao_media['media'],avaliacao_media['dp']) ) ) )
print( "Avaliação:")
avaliacao_media


# ### 4\. Produtos Mais e Menos Vendidos

# In[ ]:


produtos_nVendas = pd.concat([ loja[['Produto','Preço']].groupby("Produto").count().rename(columns={'Preço':f"Loja {n}"}) for n,loja in enumerate(lojas,start=1) ], axis=1)
produtos_nVendas["Total"] = produtos_nVendas.sum(axis=1)
produtos_nVendas.head(20).tail(10)


# In[ ]:


produto_maiorNumVendas = {loja:produtos_nVendas[loja].max() for loja in produtos_nVendas}
produtos_maisVendidos = { loja:list(produtos_nVendas[loja][ produtos_nVendas[loja] == produto_maiorNumVendas[loja] ].index) for loja in produtos_nVendas }

print("Produto(s) mais vendidos, por loja:")
print("\n".join(f"{loja :6s}: vendas={produto_maiorNumVendas[loja] :3d}  produto(s)={produtos_maisVendidos[loja]}" for loja in produtos_maisVendidos.keys()))


# In[ ]:


produto_menorNumVendas = {loja:produtos_nVendas[loja].min() for loja in produtos_nVendas}
produtos_menosVendidos = { loja:list(produtos_nVendas[loja][ produtos_nVendas[loja] == produto_menorNumVendas[loja] ].index) for loja in produtos_nVendas }

print("Produto(s) menos vendidos, por loja:")
print("\n".join(f"{loja :6s}: vendas={produto_menorNumVendas[loja] :3d}  produto(s)={produtos_menosVendidos[loja]}" for loja in produtos_menosVendidos.keys()))


# ### 5\. Frete Médio por Loja
# 

# In[ ]:


frete_medio = pd.DataFrame(
    ((loja['Frete'].mean(),loja['Frete'].std()) for loja in lojas ),
    # index=[f"Loja {n}" for n in range(1,5)],
    index=lojas_str,
    columns="media dp".split(),
)

print( "Frete:\n{}".format( "\n".join( f"{loja}   Média: R$ {frete_medio['media'].loc[loja]:.2f}   Desvio Padrão: {frete_medio['dp'].loc[loja]:.2f}" for loja in frete_medio.index ) ) )


# ### Outros dados

# #### Faturamento por categoria

# In[ ]:


faturamento_pCategoria = pd.concat([ loja[['Categoria do Produto','Preço']].groupby("Categoria do Produto").sum().rename(columns={'Preço':loja_s}) for loja,loja_s in zip(lojas, lojas_str) ], axis=1)
faturamento_pCategoria['Total'] = faturamento_pCategoria.sum(axis=1)
# faturamento_pCategoria.sort_values(by=['Total'], inplace=True)
faturamento_pCategoria.sort_values(by=['Total'], inplace=True, ascending=False)
faturamento_pCategoria


# In[ ]:


faturamentoPctg_pCategoria = faturamento_pCategoria[lojas_str].copy()
for loja in lojas_str:
    faturamentoPctg_pCategoria[loja] /= faturamento_pCategoria['Total']
faturamentoPctg_pCategoria = faturamentoPctg_pCategoria.apply(lambda x: round(x, ndigits=4), )
faturamentoPctg_pCategoria


# #### Avaliação por loja

# In[ ]:


avaliacao_pLoja = pd.concat( ( loja[['Produto','Avaliação da compra']].groupby("Avaliação da compra").count().rename(columns={'Produto':loja_s}) for loja,loja_s in zip(lojas,lojas_str) ), axis=1 )
avaliacao_pLoja


# In[ ]:


avaliacao_pLoja_all = pd.concat( ( loja['Avaliação da compra'].rename(loja_s) for loja,loja_s in zip(lojas,lojas_str) ), axis=1 )
# avaliacao_pLoja_all = pd.concat( ( loja['Avaliação da compra'].rename(loja_s) for loja,loja_s in zip(lojas,lojas_str) ), axis=1 ).fillna(3).astype(int)
avaliacao_pLoja_all


# #### Rendimento por produto em cada loja

# In[ ]:


produtos = pd.concat([ loja['Produto'] for loja in lojas]).unique()
# Counter(produtos)
# produtos


# In[ ]:


import random


# In[ ]:


# prod = random.choice(produtos)
# prod


# In[ ]:


prod = random.choice(produtos)

for loja in lojas:
    print(loja[loja['Produto'] == prod][['Produto','Preço']].head(3))


# In[ ]:


renda_pProduto = pd.concat([ loja[['Produto','Preço']].groupby("Produto").sum().rename(columns={'Preço':loja_s}) for loja,loja_s in zip(lojas, lojas_str) ], axis=1)
renda_pProduto['Total'] = renda_pProduto.sum(axis=1)
# renda_pProduto.sort_values(by=['Total'], inplace=True)
renda_pProduto.sort_values(by=['Total'], inplace=True, ascending=False)
renda_pProduto.head()


# In[ ]:


for loja in renda_pProduto.columns:
    print(loja, renda_pProduto.sort_values(by=loja, ascending=False).index[0:3])


# ## Visualização

# ### Gráfico 1
# 
# Porcentagem do Faturamento por Categoria

# In[ ]:


fig1, ax1 = plt.subplots(1, 3, figsize=(15,7))

fig1.suptitle("Porcentagem do Faturamento por Categoria\n(valores menores que 1.5% ocultados)")

ax1[1].pie(
    faturamento_pCategoria['Total'],
    labels=faturamento_pCategoria.index,
    # startangle=-46,
    startangle=90 - faturamento_pCategoria['Total'].iloc[0]/faturamento_pCategoria['Total'].sum() * 360,
    radius=1.7,
    wedgeprops=dict(width=0.7),
    # autopct=lambda pctg: f"{pctg :.2f} %",
    autopct=lambda pctg: f"{pctg :.2f} %" if pctg > 1.5 else "",
    pctdistance=0.87,
    explode=[ (0.09 if n <= 2 else 0) for n in range(len(faturamento_pCategoria.index)) ],
    shadow={'ox': -0.02, 'oy': 0.02, 'edgecolor': 'black', 'shade': 0.9},
    # textprops={'size': 'smaller'},
)

ax1[0].remove()
ax1_0up = fig1.add_subplot(2, 3, 1)
ax1_0dn = fig1.add_subplot(2, 3, 4)

for i,ax in enumerate([ ax1[2], ax1_0up, ax1_0dn ]):

    currBottom = 1
    barWidth = 0.25
    for k, (loja,pctg) in enumerate(faturamentoPctg_pCategoria.iloc[i].sort_values(ascending=False).items()):
        currBottom -= pctg
        barContnr = ax.bar(
            0, pctg,
            width=barWidth,
            bottom=currBottom,
            color=f'C{i}',
            label=loja,
            alpha=1 - 0.25*k
        )
        ax.bar_label(barContnr, labels=[f"{pctg :.2%}"], label_type='center')

    ax.set_title(faturamentoPctg_pCategoria.index[i])
    ax.legend(loc="center left" if i > 0 else 'center right')
    ax.axis('off')
    ax.set_xlim(-2.5*barWidth, 2.5*barWidth)

fig1.show()


# https://matplotlib.org/stable/users/explain/colors/colors.html#colors-def
# 
# > "CN" color spec where 'C' precedes a number acting as an index into the default property cycle.
# >
# > Example:
# > - `'C0'`
# > - `'C1'`
# >
# > > [!NOTE]
# > >
# > > Matplotlib indexes color at draw time and defaults to black if cycle does not include color.

# ### Gráfico 2
# 
# Quantidade de vendas por Categoria

# In[ ]:


fig2, ax2 = plt.subplots(1,1, figsize=(13,7))

fig2.suptitle("Quantidade de vendas por Categoria\n(categorias em ordem decrescente de faturamento)")

barWidth = 0.25
x = np.arange(len(vendas_pCategoria.index)) * 1.3
for n,loja in enumerate(lojas_str):
    # barContnr = ax2.bar(x + (barWidth * n), vendas_pCategoria[loja].to_numpy(), barWidth*0.9, label=loja)
    barContnr = ax2.bar(x + (barWidth * n), vendas_pCategoria[loja].loc[faturamento_pCategoria.index].to_numpy(), barWidth*0.9, label=loja)
    # ax2.bar_label(barContnr, padding=3)
    ax2.bar_label(barContnr)

ax2.set_ylabel("Número de vendas")

ax2.set_xlabel("Categorias")
# ax2.set_xticks(x + 1.5*barWidth, vendas_pCategoria.index)
ax2.set_xticks(x + 1.5*barWidth, faturamento_pCategoria.index)
ax2.tick_params(axis="x", rotation=7)

ax2.legend()
ax2.grid()
ax2.set_axisbelow(True)

fig2.show()


# ### Gráfico 3
# 
# Avaliações por Loja

# In[ ]:


# fig3, (ax3_1,ax3_2,ax3s) = plt.subplots(1,3, figsize=(18,7))
fig3, ax3 = plt.subplots(1,1, figsize=(13,7))

fig3.suptitle("Avaliações por Loja")

# ax3_1.remove()
# ax3_2.remove()
# ax3 = fig3.add_subplot(1,3,(1,2))

aval_colors = plt.colormaps['RdYlGn'](np.linspace(0.15, 0.85, 5))

for loja in lojas_str:

    barContnr = ax3.barh(
        loja, avaliacao_pLoja[loja],
        left=avaliacao_pLoja[loja].cumsum() - avaliacao_pLoja[loja],
        height=0.5,
        label="1 - muito ruim,2 - ruim,3 - regular,4 - bom,5 - muito bom".split(",") if loja == "Loja 1" else None,
        color=aval_colors,
    )

    ax3.bar_label(barContnr, label_type='center', color="black")

ax3.invert_yaxis()

ax3.xaxis.set_visible(False)
ax3.set_xlim(0, avaliacao_pLoja.sum().max())

ax3.legend(
    ncols=5,
    bbox_to_anchor=(0.03, 1),
    loc='lower left',
    fontsize='large',
)

# ax3s.set_title("Média")

# ax3s.errorbar(avaliacao_media.index,avaliacao_media['media'], yerr=avaliacao_media['dp'], barsabove = True)
# ax3s.violinplot(avaliacao_pLoja_all)
# ax3s.boxplot(avaliacao_pLoja_all)

# ax3s.set_ylim(0.9, 5.1)

fig3.show()


# ## Relatório

# 
