#################### Projeto - Obesidade no Mundo ####################

'''
Link para o dataset:
[Obesity among adults by country, 1975-2016 (https://www.kaggle.com/amanarora/obesity-among-adults-by-country-19752016/)]
'''


# %%
#################### Importando Bibliotecas ####################
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go


# %%
#################### Importando dataset ####################
df = pd.read_csv('Dataset/obesity.csv', index_col=0)


# %%
#################### Limpando o dataset ####################

# Criando uma coluna de nome 'Obesity' que conterá os valores de obesidade
df['Variation'] = df['Obesity (%)'].apply(lambda x: x.split(' ')[1])
df['Obesity'] = df['Obesity (%)'].apply(lambda x: x.split(' ')[0])

# Removendo entrada de dados sem informações sobre a obesidae
df.loc[df['Obesity'] == 'No', 'Obesity'] = np.nan
df.dropna(inplace=True)

# Transformando em float as colunas que foram importadas como string.
df['Obesity'] = df['Obesity'].str.replace(',','.').astype(float)

df.info()

# %%
#################### Insights Sobre os Dados ####################


# Percentual médio de obesidade por sexo no mundo em 2016 (último ano registrado)
print('\nPercentual médio de obesidade por sexo no mundo em 2016 (último ano registrado):')
print('Feminino: ', end='')
print('{:.3f}' .format(df[(df['Year'] == 2016) & (df['Sex'] == 'Female')]['Obesity'].mean()))

print('Masculino: ', end='')
print('{:.3f}' .format(df[(df['Year'] == 2016) & (df['Sex'] == 'Male')]['Obesity'].mean()))

# df[df['Year'] == 2016].groupby('Sex').mean()


# %%
# Os 5 países com maior e a menor taxa de aumento nos índices de obesidade em todo período observado
dif = df.groupby(['Country', 'Sex'])[['Obesity']].last() - df.groupby(['Country', 'Sex'])[['Obesity']].first()
dif.reset_index(inplace=True)

# %%
# Os 5 países com maior taxa de aumento nos índices de obesidade em todo período observado

print('\nOs 5 países com maior taxa de aumento nos índices de obesidade em todo período observado para ambos os sexos são:')
maiores = dif[dif['Sex'] == 'Both sexes'].nlargest(5, 'Obesity')
print(maiores.reset_index())

# %%
# Os 5 países com menor taxa de aumento nos índices de obesidade em todo período observado

print('\nOs 5 países com menor taxa de aumento nos índices de obesidade em todo período observado para ambos os sexos são:')
menores = dif[dif['Sex'] == 'Both sexes'].nsmallest(5, 'Obesity')
print(menores.reset_index())


# %%
# Países com maiores e menores níveis percentuais de obesidade em 2016

print('\nPaíses com maiores e menores níveis percentuais de obesidade em 2016:')

print('Maiores:')
print(df[(df['Year'] == 2016) & (df['Sex'] == 'Both sexes')][['Country', 'Year', 'Sex', 'Obesity']].sort_values(['Obesity'], ascending=False).head(5).reset_index())

print('\nMenores:')
print(df[(df['Year'] == 2016) & (df['Sex'] == 'Both sexes')][['Country', 'Year', 'Sex', 'Obesity']].sort_values(['Obesity']).head(5).reset_index())


# %%
# Diferença média percentual de obesidade entre sexos ao longo do período observado para o Brasil

male = df[(df['Country'] == 'Brazil') & (df['Sex'] == 'Male')][['Year', 'Obesity']].set_index('Year')
female = df[(df['Country'] == 'Brazil') & (df['Sex'] == 'Female')][['Year', 'Obesity']].set_index('Year')
difper = female[['Obesity']] - male[['Obesity']]

print('\nDiferença média percentual de obesidade entre os sexos ao longo dos anos no Brasil (Obs: o sexo feminimo obtém maior média ao longo dos anos):')

print(difper)

difper.plot(figsize=(15, 10), title='Diferença média percentual de obesidade entre os sexos ao longo dos anos no Brasil (Obs: o sexo feminimo obtém maior média ao longo dos anos)', xlabel='Anos', ylabel='Diferença percentual')


# %%
# Gráfico com a evolução da obesidade para ambos sexos no mundo

df_ambos = df[df['Sex'] == 'Both sexes'].groupby('Year').mean().reset_index()

df_ambos.plot('Year', 'Obesity', title='Gráfico com a evolução da obesidade para ambos sexos no mundo', xlabel='Anos', ylabel='Porcentagem', figsize=(10, 5))


# %%
# Mapa com a evolução da obesidade para ambos os sexos no mundo ao longo do tempo

df_mapa = df.groupby(['Country', 'Year'])['Obesity'].mean().sort_values().reset_index()

df_temp = px.data.gapminder()
dict_iso_alpha = df_temp.set_index('country').to_dict()['iso_alpha']
dict_num = {j: i for i, j in enumerate(df_mapa['Country'].unique())}

df_mapa['iso_alpha'] = df_mapa['Country'].map(dict_iso_alpha)

df_mapa['iso_num'] = df_mapa['Country'].map(dict_num)

fig = px.choropleth(df_mapa.reset_index(drop=True), locations='iso_alpha', color='Obesity', hover_name='Country', animation_frame='Year', title='Mapa com a evolução da obesidade no mundo')

fig.update_layout(height=600)
fig.show()


# %%
# Mapa com a porcentagem de obesidade no mundo

x = df.groupby('Country')['Obesity'].mean().sort_values()
data = dict(type = 'choropleth',
            locations = x.index,
            locationmode = 'country names',
            colorscale= 'Portland',
            text= x.index,
            z=x,
            colorbar = {'title':'Obesidade %', 'len':200,'lenmode':'pixels' })
layout = dict(geo = {'scope':'world'}, title='Obesidade % no mundo')
col_map = go.Figure(data = [data],layout = layout)
col_map.show()
