#!/usr/bin/env python
# coding: utf-8

# ### Importação dos dados
# 
# 

# In[ ]:


import pandas as pd

url1 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_1.csv"
url2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_2.csv"
url3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_3.csv"
url4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science/refs/heads/main/base-de-dados-challenge-1/loja_4.csv"

loja1 = pd.read_csv(url1)
loja2 = pd.read_csv(url2)
loja3 = pd.read_csv(url3)
loja4 = pd.read_csv(url4)

lojas = [loja1, loja2, loja3, loja4]


# In[ ]:


loja1


# In[ ]:


print(loja1.info())


# #1. Análise do faturamento
# 

# In[ ]:


faturamentos = [ loja['Preço'].sum() for loja in lojas ]

print( "Faturamentos:\n{}".format( ("\n".join( ( f'Loja {n}: R$ {val:_.2f}' for n,val in enumerate(faturamentos,start=1) ) )).replace(".",",").replace("_",".") ) )


# # 2. Vendas por Categoria
# 

# In[ ]:


# loja1[ ['Categoria do Produto','Preço'] ].groupby("Categoria do Produto").describe()
# loja1[ ['Categoria do Produto','Preço'] ].groupby("Categoria do Produto").count()


# In[ ]:


vendas_pCategoria = pd.concat([ loja[ ['Categoria do Produto','Produto'] ].groupby("Categoria do Produto").count().rename(columns={'Produto':f"Loja {n}"}) for n,loja in enumerate(lojas,start=1) ], axis=1)
vendas_pCategoria


# # 3. Média de Avaliação das Lojas

# In[ ]:


avaliacao_media = pd.DataFrame(
    ((loja['Avaliação da compra'].mean(),loja['Avaliação da compra'].std()) for loja in lojas ),
    index=[f"Loja {n}" for n in range(1,5)],
    columns="media dp".split(),
)

# print( "Avaliação:\n{}".format( "\n".join( f"{loja:s}:  Média={media:.2f}  Desvio Padrão={dp:.2f}" for loja,media,dp in zip(avaliacao_media.index,avaliacao_media['media'],avaliacao_media['dp']) ) ) )
print( "Avaliação:")
avaliacao_media


# # 4. Produtos Mais e Menos Vendidos

# In[ ]:


produtos_nVendas = pd.concat([ loja[['Produto','Preço']].groupby("Produto").count().rename(columns={'Preço':f"Loja {n}"}) for n,loja in enumerate(lojas,start=1) ], axis=1)
produtos_nVendas.head(10)


# In[ ]:


loja1[ loja1['Produto'] == 'Bateria' ].info()


# In[ ]:


produtos_nVendas['Loja 1'][ produtos_nVendas['Loja 1'] == produtos_nVendas['Loja 1'].max() ]


# In[ ]:


produto_maiorNumVendas = {loja:produtos_nVendas[loja].max() for loja in produtos_nVendas}
produtos_maisVendidos = { loja:list(produtos_nVendas[loja][ produtos_nVendas[loja] == produto_maiorNumVendas[loja] ].index) for loja in produtos_nVendas }

print("Produto(s) mais vendidos, por loja:")
print("\n".join(f"{loja}: vendas={produto_maiorNumVendas[loja]}  produto(s)={produtos_maisVendidos[loja]}" for loja in produtos_maisVendidos.keys()))


# In[ ]:


produto_menorNumVendas = {loja:produtos_nVendas[loja].min() for loja in produtos_nVendas}
produtos_menosVendidos = { loja:list(produtos_nVendas[loja][ produtos_nVendas[loja] == produto_menorNumVendas[loja] ].index) for loja in produtos_nVendas }

print("Produto(s) menos vendidos, por loja:")
print("\n".join(f"{loja}: vendas={produto_menorNumVendas[loja]}  produto(s)={produtos_menosVendidos[loja]}" for loja in produtos_menosVendidos.keys()))


# # 5. Frete Médio por Loja
# 

# In[ ]:


frete_medio = pd.DataFrame(
    ((loja['Frete'].mean(),loja['Frete'].std()) for loja in lojas ),
    index=[f"Loja {n}" for n in range(1,5)],
    columns="media dp".split(),
)

print( "Frete:\n{}".format( "\n".join( f"{loja}   Média: R$ {frete_medio['media'].loc[loja]:.2f}   Desvio Padrão: {frete_medio['dp'].loc[loja]:.2f}" for loja in frete_medio.index ) ) )

