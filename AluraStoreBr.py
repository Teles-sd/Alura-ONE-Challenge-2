#!/usr/bin/env python
# coding: utf-8

# # Alura+ONE Challenge 2: Alura Store

# ## Análise de Dados

# ### Importação de dados
# 
# 

# In[1]:


import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


# In[2]:


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


# In[3]:


loja1


# In[4]:


print([len(loja) for loja in lojas])


# In[5]:


print(loja1.info())


# ### 1\. Análise do faturamento
# 

# In[6]:


faturamentos = [ loja['Preço'].sum() for loja in lojas ]
faturamento_total = sum(faturamentos)

print( "Faturamentos:\n{}".format( ("\n".join( ( f'Loja {n}: R$ {val:_.2f}' for n,val in enumerate(faturamentos,start=1) ) )).replace(".",",").replace("_",".") ) )

print(f"\nTotal : R$ {faturamento_total:_.2f}".replace(".",",").replace("_","."))


# In[7]:


print( "Porcentagem do faturamentos:\n{}".format( ("\n".join( ( f'{loja_s}: {val/faturamento_total :.1%}' for loja_s,val in zip(lojas_str,faturamentos) ) )) ) )


# ### 2\. Vendas por Categoria
# 

# In[8]:


# loja1[ ['Categoria do Produto','Preço'] ].groupby("Categoria do Produto").describe()
# loja1[ ['Categoria do Produto','Preço'] ].groupby("Categoria do Produto").count()


# In[9]:


vendas_pCategoria = pd.concat([ loja[ ['Categoria do Produto','Produto'] ].groupby("Categoria do Produto").count().rename(columns={'Produto':f"Loja {n}"}) for n,loja in enumerate(lojas,start=1) ], axis=1)

print("Vendas de cada loja, por categoria:\n")
vendas_pCategoria


# ### 3\. Média de Avaliação das Lojas

# In[10]:


avaliacao_media = pd.DataFrame(
    ((loja['Avaliação da compra'].mean(),loja['Avaliação da compra'].std()) for loja in lojas ),
    index=lojas_str,
    columns="media dp".split(),
)

# print( "Avaliação:\n{}".format( "\n".join( f"{loja:s}:  Média={media:.2f}  Desvio Padrão={dp:.2f}" for loja,media,dp in zip(avaliacao_media.index,avaliacao_media['media'],avaliacao_media['dp']) ) ) )
print( "Avaliação:")
avaliacao_media


# ### 4\. Produtos Mais e Menos Vendidos

# In[11]:


produtos_nVendas = pd.concat([ loja[['Produto','Preço']].groupby("Produto").count().rename(columns={'Preço':f"Loja {n}"}) for n,loja in enumerate(lojas,start=1) ], axis=1)
produtos_nVendas["Total"] = produtos_nVendas.sum(axis=1)
produtos_nVendas.head(20).tail(10)


# In[12]:


produto_maiorNumVendas = {loja:produtos_nVendas[loja].max() for loja in produtos_nVendas}
produtos_maisVendidos = { loja:list(produtos_nVendas[loja][ produtos_nVendas[loja] == produto_maiorNumVendas[loja] ].index) for loja in produtos_nVendas }

print("Produto(s) mais vendidos, por loja:")
print("\n".join(f"{loja :6s}: vendas={produto_maiorNumVendas[loja] :3d}  produto(s)={produtos_maisVendidos[loja]}" for loja in produtos_maisVendidos.keys()))


# In[13]:


produto_menorNumVendas = {loja:produtos_nVendas[loja].min() for loja in produtos_nVendas}
produtos_menosVendidos = { loja:list(produtos_nVendas[loja][ produtos_nVendas[loja] == produto_menorNumVendas[loja] ].index) for loja in produtos_nVendas }

print("Produto(s) menos vendidos, por loja:")
print("\n".join(f"{loja :6s}: vendas={produto_menorNumVendas[loja] :3d}  produto(s)={produtos_menosVendidos[loja]}" for loja in produtos_menosVendidos.keys()))


# ### 5\. Frete Médio por Loja
# 

# In[14]:


frete_medio = pd.DataFrame(
    ((loja['Frete'].mean(),loja['Frete'].std()) for loja in lojas ),
    # index=[f"Loja {n}" for n in range(1,5)],
    index=lojas_str,
    columns="media dp".split(),
)

print( "Frete:\n{}".format( "\n".join( f"{loja}   Média: R$ {frete_medio['media'].loc[loja]:.2f}   Desvio Padrão: {frete_medio['dp'].loc[loja]:.2f}" for loja in frete_medio.index ) ) )


# ### Outros dados

# #### Faturamento por categoria

# In[15]:


faturamento_pCategoria = pd.concat([ loja[['Categoria do Produto','Preço']].groupby("Categoria do Produto").sum().rename(columns={'Preço':loja_s}) for loja,loja_s in zip(lojas, lojas_str) ], axis=1)
faturamento_pCategoria['Total'] = faturamento_pCategoria.sum(axis=1)
# faturamento_pCategoria.sort_values(by=['Total'], inplace=True)
faturamento_pCategoria.sort_values(by=['Total'], inplace=True, ascending=False)
faturamento_pCategoria


# In[16]:


faturamentoPctg_pCategoria = faturamento_pCategoria[lojas_str].copy()
for loja_s in lojas_str:
    faturamentoPctg_pCategoria[loja_s] /= faturamento_pCategoria['Total']
faturamentoPctg_pCategoria = faturamentoPctg_pCategoria.apply(lambda x: round(x, ndigits=4), )
faturamentoPctg_pCategoria


# #### Avaliação por loja

# In[17]:


avaliacao_pLoja = pd.concat( ( loja[['Produto','Avaliação da compra']].groupby("Avaliação da compra").count().rename(columns={'Produto':loja_s}) for loja,loja_s in zip(lojas,lojas_str) ), axis=1 )
avaliacao_pLoja


# In[18]:


avaliacao_pLoja_all = pd.concat( ( loja['Avaliação da compra'].rename(loja_s) for loja,loja_s in zip(lojas,lojas_str) ), axis=1 )
# avaliacao_pLoja_all = pd.concat( ( loja['Avaliação da compra'].rename(loja_s) for loja,loja_s in zip(lojas,lojas_str) ), axis=1 ).fillna(3).astype(int)
avaliacao_pLoja_all


# #### Preço por produto

# In[19]:


produtos = pd.concat([ loja['Produto'] for loja in lojas]).unique()
# Counter(produtos)
len(produtos)
# np.sort(produtos)


# In[20]:


import random


# In[21]:


# prod = random.choice(produtos)
# prod


# In[22]:


prod = random.choice(produtos)
# prod = "TV Led UHD 4K"

for loja in lojas:
    print(loja[loja['Produto'] == prod][['Produto','Preço']].head(3))


# In[23]:


preco_pProduto = pd.concat([ loja[['Produto','Preço']] for loja in lojas ], axis=0).groupby("Produto").describe()["Preço"][["mean", "std"]]
preco_pProduto.head(20).tail(10)


# In[24]:


preco_pProduto_pLoja = pd.concat([ loja[['Produto','Preço']].groupby("Produto").sum().rename(columns={'Preço':loja_s}) for loja,loja_s in zip(lojas, lojas_str) ], axis=1)
preco_pProduto_pLoja['Total'] = preco_pProduto_pLoja.sum(axis=1)
# preco_pProduto_pLoja.sort_values(by=['Total'], inplace=True)
preco_pProduto_pLoja.sort_values(by=['Total'], inplace=True, ascending=False)
preco_pProduto_pLoja.head()


# In[25]:


for loja in preco_pProduto_pLoja.columns:
    print(loja, preco_pProduto_pLoja.sort_values(by=loja, ascending=False).index[0:3])


# ## Visualização

# ### Gráfico 1
# 
# Porcentagem do Faturamento por Categoria

# In[26]:


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
# fig1.savefig('Gráfico-1.png')


# [Relatório](#scrollTo=Relat_rio)

# ### Gráfico 2
# 
# Quantidade de vendas por Categoria

# In[27]:


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
# fig1.savefig('Gráfico-2.png')


# [Relatório](#scrollTo=Relat_rio)

# ### Gráfico 3
# 
# Avaliações por Loja

# In[28]:


# fig3, (ax3_1,ax3_2,ax3s) = plt.subplots(1,3, figsize=(18,7))
fig3, ax3 = plt.subplots(1,1, figsize=(13,7))

fig3.suptitle("Avaliações por Loja")

# ax3_1.remove()
# ax3_2.remove()
# ax3 = fig3.add_subplot(1,3,(1,2))

aval_colors = plt.colormaps['RdYlGn'](np.linspace(0.15, 0.85, 5))

for loja_s in lojas_str:

    barContnr = ax3.barh(
        loja_s, avaliacao_pLoja[loja_s],
        left=avaliacao_pLoja[loja_s].cumsum() - avaliacao_pLoja[loja_s],
        height=0.5,
        label="1 - muito ruim,2 - ruim,3 - regular,4 - bom,5 - muito bom".split(",") if loja_s == "Loja 1" else None,
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
# fig1.savefig('Gráfico-3.png')


# [Relatório](#scrollTo=Relat_rio)

# ### Gráfico 4
# 
# Preço médio e Produtos mais vendidos

# In[29]:


fig4 = plt.figure(figsize=(15,8))

# fig4.suptitle("Preço médio por Produto\n(em ordem crescente de número de vendas totais)")

ax41 = fig4.add_subplot(4,4, (1,11))

ax42 = fig4.add_subplot(444)
ax43 = fig4.add_subplot(448)
ax44 = fig4.add_subplot(4,4, 12)
ax45 = fig4.add_subplot(4,4, 16)

preco_sorted = preco_pProduto.loc[produtos_nVendas['Total'].sort_values().index]

ax41.errorbar(
    preco_sorted.index, preco_sorted["mean"], yerr=preco_sorted["std"],
    ecolor="C1",
    lw=3,
    elinewidth=2,
    capthick=2,
    capsize=4,
    barsabove=False,
)

ax41.set_title("Preço médio por Produto\n(em ordem crescente de número de vendas totais)")
ax41.grid()

ax41.set_xlim(-1, len(preco_sorted.index))
ax41.tick_params(axis="x", labelrotation=90)

# ax41.set_ylabel("Preço (R$)")
# ax41.set_yticklabels( [ f"R$ {t:.2f}" if t>0 else "" for t in ax41.get_yticks()] )
ax41.set_yticks(ax41.get_yticks()[1:-1], labels=[ f"R$ {t:.2f}" if t>0 else "" for t in ax41.get_yticks()[1:-1]] )

for c, (ax,loja_s) in enumerate(zip([ax42,ax43,ax44,ax45],lojas_str), start=2):

    produtos_sorted = produtos_nVendas[loja_s].sort_values().iloc[np.r_[0:3, -4:0]]

    barContnr = ax.barh(produtos_sorted.index, produtos_sorted.values, color=f"C{c}", label=loja_s, height=0.9)

    # ax.bar_label(barContnr, label_type="center", labels=[l + f" ({n})" for l,n in produtos_sorted.items()])
    ax.bar_label(barContnr, label_type="center", labels=produtos_sorted.index, color="lightgray")
    ax.grid()
    ax.set_axisbelow(True)


    # ax.tick_params(axis="x", labelsize="smaller")
    # ax.tick_params(axis='x', bottom=False, labelbottom=False)

    ax.tick_params(axis='y', left=False, labelleft=False)

    ax.legend()


ax42.set_title("Produtos mais e menos\nvendido de cada loja")

# fig4.tight_layout()
fig4.show()
# fig1.savefig('Gráfico-4.png')


# ## Relatório

# ### Métricas
# 
# Levando em conta que o Senhor João precisa vender uma das 4 lojas da Alura Store para iniciar um novo empreendimento, essa análise se baseia em identificar a loja que irá ter o menor impacto nas vendas, faturamento e avaliação dos clientes.

# ### Análise
# 
# Vemos pelo [Gráfico 1](#scrollTo=Gr_fico_1) que as categorias que mais contribuem para o faturamento total são: **eletrônicos**, **eletrodomésticos** e **móveis**; que somados compõem $85\%$ do faturamento. Dentre essas categorias, a **Loja 4** possui a menor contribuição para o faturamento, estando em último lugar em eletrônicos e eletrodomésticos e em segundo lugar em móveis, contribuindo com $24.66/%$, $21.38\%$ e $25.41\%$ respectivamente. **Loja 2** também fica em último lugar em uma categoria (móveis), com $23.29\%$, mas fica em segundo lugar nas outras duas.
# 
# Considerando a quantidade de vendas por categoria, vista no [Gráfico 2](#scrollTo=Gr_fico_2); **Loja 1** teve menos produtos vendidos nas categorias _utilidades domésticas_ e _livros_, as duas categorias com menor impacto no faturamento; **Loja 2** tem menos produtos vendidos nas categorias _eletrônicos_, _móveis_, _esporte e lazer_ e _brinquedos_; **Loja 3** não fica em último em nenhuma das 8 categorias; e **Loja 4** teve menos produtos vendidos nas categorias _eletrodomésticos_ e _instrumentos musicais_. Neste quesito, Lojas 2 e 4 ficam nas piores posições novamente.
# 
# Olhando para avaliações dos clientes de cada loja, no [Gráfico 3](#scrollTo=Gr_fico_3), todas as lojas têm médias muito próximas, com variações pequenas; mas dentre elas, as Lojas 2 e 3 ficam na frente: Loja 3 com maior quantidade de notas 5, seguida da Loja 2; e Loja 2 com menor quantidade de notas 1, seguida da Loja 3. Por outro lado, **Loja 1** possui tanto a maior quantidade de notas 1 quanto a menor quantidade de notas 5, seguida da **Loja 4**.
# 
# No [Gráfico 4](#scrollTo=Gr_fico_4), vemos que os 4 produtos mais vendidos pelas Lojas 1 não só têm em média preço mais alto que outros produtos, como também estão entre os produtos mais vendidos no geral, o que indica um alto impacto da Loja 1. Já alguns dos produtos mais vendidos pela **Loja 4** (como _Faqueiro_ e _Dashboards com Power BI_) têm valor relativamente baixo e não estão entre os mais vendidos no geral.

# ### Conclusão
# 
# Levando todos esses pontos em consideração, é certo afirmar que a Loja 1, apesar de uma média um pouco mais abaixo que as outras na avaliação dos clientes, possui um alto impacto no geral no faturamento e no número de vendas dos produtos e categorias de produtos mais relevantes. Lojas 2 e 3 ficam mais próximas da média na maioria dessas métricas, com a Loja 2 um pouco mais atrás. Isso deixa a **Loja 4** como a indicada para a venda, de forma a gerar o menor impacto no empreendimento do Seu João.

# ## Extra

# ### Análise de Desempenho Geográfico

# #### Folium
# 
# [Folium - Getting started](https://python-visualization.github.io/folium/latest/getting_started.html)
# 
# [Folium - Using `GeoJson`](https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson.html)
# 
# [Folium - Using `Choropleth`](https://python-visualization.github.io/folium/latest/user_guide/geojson/choropleth.html)
# 
# [Folium - API reference](https://python-visualization.github.io/folium/latest/reference.html)
# 
# <!-- [Folium - Getting started]() -->

# In[30]:


import folium
from branca.colormap import linear


# #### geoBoundaries
# 
# Os arquivos [GeoJSON](https://en.wikipedia.org/wiki/GeoJSON) necessários para uso do **Folium** foram adquiridos do banco de dados **geoBoundaries**:
# 
# > - [geoBoundaries](https://www.geoboundaries.org): An open database of political administrative boundaries.
# > - [geoBoundaries - Github](https://github.com/wmgeolab/geoBoundaries)

# A [geoboundaries API](https://www.geoboundaries.org/api.html) determina que qualquer informação pode ser requisitada no endereço:
# 
# ```text
# https://www.geoboundaries.org/api/current/[RELEASE-TYPE]/[3-LETTER-ISO-CODE]/[BOUNDARY-TYPE]/
# ```
# 
# Onde:
# 
# - `[RELEASE-TYPE]`: para a maioria dos usuários, é sugerido usar `gbOpen`
# - `[3-LETTER-ISO-CODE]`: código ISO-3166-1 (Alpha 3) do país, por exemplo:
#     - `USA`, United States
#     - `GBR`, United Kingdom
#     - `CHN`, China
#     - `BRA`, Brazil, etc.
#     - O código especial `ALL` também é aceito.
# - `[ADM-LEVEL]`: tipo de fronteira, isto é, nível administrativo:
#     - `ADM0`, país
#     - `ADM1`, primeiro nível de fronteiras subnacionais (regiões, no Brasil; _states_, no EUA)
#     - `ADM2`, primeiro nível de fronteiras subnacionais (estados, no Brasil; _county_, no EUA)
#     - `ADM3`, ...
#     - `ADM4`, ...
#     - `ALL`
# 
# Se em dúvida de quais dados usar, é possível compara dados em [geoboundaries - Visualize Data: Visualize & Compare Boundaries](https://www.geoboundaries.org/visualize.html).
# 
# Para os estados do Brasil, se usa o endereço "https://www.geoboundaries.org/api/current/gbOpen/BRA/ADM1/" e um JSON é retornado, onde o endereço para o GeoJSON está disponível nos campos `gjDownloadURL` ou `simplifiedGeometryGeoJSON`.
# 
# <!-- https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/BRA/ADM1/geoBoundaries-BRA-ADM1.geojson -->

# In[31]:


import requests
import geopandas


# In[32]:


br_states_gb_json = requests.get( "https://www.geoboundaries.org/api/current/gbOpen/BRA/ADM1/" ).json()
br_states_gb_json["gjDownloadURL"]


# In[33]:


br_states = geopandas.read_file(br_states_gb_json["gjDownloadURL"])
br_states = br_states.rename(columns={"shapeISO":"id", "shapeName":"estado"})[["id","estado","geometry"]]
br_states['id'] = br_states['id'].map(lambda s: s[3:])
br_states.set_index('id', inplace=True)

br_states.head(10)


# #### Dados das lojas

# ##### Compra por estado

# In[34]:


compra_pEstado = pd.concat([ loja[['Produto','Local da compra']].groupby("Local da compra").count().rename(columns={'Produto':loja_s}) for loja,loja_s in zip(lojas,lojas_str) ], axis=1).fillna(0).astype(int)
compra_pEstado["Total"] = compra_pEstado.sum(axis=1)
# compra_pEstado.index.name = "id"
compra_pEstado["Estado"] = compra_pEstado.index
compra_pEstado = compra_pEstado[['Estado', 'Loja 1', 'Loja 2', 'Loja 3', 'Loja 4', 'Total']]
compra_pEstado.sort_values(by='Total').iloc[np.r_[0:5,-5:0]]
# compra_pEstado


# ##### Faturamento total, Frete médio e número de Produtos comprados por Localização (lat, lon) por loja

# In[35]:


# loja1['lat_lon'] = list(zip(loja1['lat'], loja1['lon']))
# loja1[['Produto', 'Categoria do Produto', 'Preço', 'Frete', 'Local da compra', 'lat', 'lon', 'lat_lon']].head()


# In[36]:


loja1.groupby(['lat', 'lon']).agg({"Local da compra":"nunique"})["Local da compra"].nunique()


# In[37]:


# data_pLoc_pLoja = { loja_s:loja.groupby(['lat', 'lon']).agg({
data_pLoc_pLoja = { loja_s:loja.groupby(['lon', 'lat']).agg({
    "Preço":"sum",
    "Frete":"mean",
    "Produto": "count",
    "Local da compra":"first"
}).rename(columns={
    "Preço":"Faturamento total",
    "Frete":"Frete médio",
    "Produto": "Produtos comprados",
    "Local da compra":"Estado",
}) for loja,loja_s in zip(lojas,lojas_str) }

for loja in data_pLoc_pLoja.values():
    # loja["geometry"] = loja.index
    loja["geometry"] = geopandas.points_from_xy( *zip(*loja.index) )
    loja.reset_index(inplace=True, drop=True)

data_pLoc_pLoja = { loja_s:geopandas.GeoDataFrame(loja).set_crs(br_states.crs) for loja_s,loja in data_pLoc_pLoja.items() }

data_pLoc_pLoja["Loja 1"].head()


# In[38]:


# Problems indexing and with NaN
pd.concat( [ loja.groupby(['lon', 'lat']).agg({
    "Preço":"sum",
    "Frete":"mean",
    "Produto": "count",
    "Local da compra":"first"
}).rename(columns={
    "Preço":"Faturamento total",
    "Frete":"Frete médio",
    "Produto": "Produtos comprados",
    "Local da compra":"Estado",
}) for loja in lojas ], axis=1, keys=lojas_str ).head()


# #### Mapa
# 
# Utilize os dados de **latitude** (`lat`) e **longitude** (`lon`) para mapear as vendas de cada loja e analisar a distribuição geográfica dos produtos vendidos.

# In[39]:


br_states.head()


# In[40]:


br_states.to_json()[:300]


# {'id': '0', 'type': 'Feature', 'properties': {'estado': 'Roraima'}, 'geometry': {'type': 'Polygon', 'coordinates': [[[-60.018789227999946, 0.249984785000038], ...

# {'id': 'RR', 'type': 'Feature', 'properties': {'id': 'RR', 'estado': 'Roraima'}, 'geometry': {'type': 'Polygon', 'coordinates': [[[-60.018789227999946, 0.249984785000038], ...

# In[41]:


compra_pEstado.head()


# In[42]:


data_pLoc_pLoja["Loja 1"].head()


# In[43]:


m = folium.Map(
    location=[-22.19, -48.79],
    width="70%", height="70%",

    zoom_start=4,
    min_zoom=4, max_zoom=7,

    min_lat=10, max_lat=-37,
    min_lon=-85, max_lon=-25,
    max_bounds=True,

    control=False,
)

fcp = folium.Choropleth(
    geo_data=br_states,
    key_on="feature.id",

    name="Total de compras por Estado",
    show=True,
    # show=False,

    legend_name="Número de compras",
    bins=8,

    data=compra_pEstado,
    # If the data is a Pandas DataFrame, the columns of data to be bound. Must pass column 1 as the key, and column 2 the values.
    columns=['Estado', 'Total'],

    # fill_color="YlGn",
    fill_opacity=0.7,
    line_weight=2,
    line_opacity=0.5,

    highlight=True,

    # nan_fill_color="black",
    nan_fill_color="purple",
    nan_fill_opacity=0.5,

).add_to(m)

# looping thru the geojson object and adding a new property(Total)
# and assigning a value from our dataframe
for s in fcp.geojson.data['features']:
    s['properties']['Total'] = int(compra_pEstado['Total'].loc[s['id']])

# and finally adding a tooltip/hover to the choropleth's geojson
# folium.GeoJsonTooltip(fields=["Total"], aliases=["Total de compras no estado: "]).add_to(fcp.geojson)
folium.GeoJsonTooltip(fields=["Total"], aliases=["Total de compras no estado: "]).add_to(fcp.geojson)

for loja_s in lojas_str:
    folium.GeoJson(
        data=data_pLoc_pLoja[loja_s],

        name=loja_s,
        show=False,

        # When hovering
        # tooltip=folium.GeoJsonTooltip(fields=["Estado", "Produtos comprados"]),
        tooltip=folium.GeoJsonTooltip(
            fields=["Produtos comprados"],
            aliases=[f"Produtos comprados na {loja_s}: "]
        ),
        # When clicking
        popup=folium.GeoJsonPopup(
            fields=["Produtos comprados", "Faturamento total","Frete médio"],
            aliases=[f"Produtos comprados na {loja_s}: ", "Faturamento: ","Frete médio: "]
        ),

        marker=folium.Circle(
            # radius=400000,
            fill_color="orange",
            fill_opacity=0.4,
            color="black",
            weight=2
        ),
        style_function=lambda feature: {
            "fillColor": "orange", #colors[x['properties']['service_level']],
            # "radius": 4000 * feature['properties']['Produtos comprados'],
            "radius": 4000 * np.interp ( feature['properties']['Produtos comprados'], (compra_pEstado['Total'].min(), compra_pEstado['Total'].max()), (5, 100) ),
        },

        highlight_function=lambda feature: {
            "fillOpacity": 0.8
        },

        zoom_on_click=False,

    ).add_to(m)

folium.LayerControl(collapsed=False).add_to(m)
# folium.LayerControl().add_to(m)

m


# # Bottom text
