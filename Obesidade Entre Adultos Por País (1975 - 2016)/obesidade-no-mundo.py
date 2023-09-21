
####################################   Projeto - Obesidade no Mundo   ####################################


'''
Link para o dataset:
[Obesity among adults by country, 1975-2016](https://www.kaggle.com/amanarora/obesity-among-adults-by-country-19752016/)
'''

# %%
#################### Importando Bibliotecas ####################
import pandas as pd
import numpy as np


# %%
#################### Importando dataset ####################
df = pd.read_csv('Datasets/obesity.csv', index_col=0)


# %%
#################### Limpando o dataset ####################

# Criando uma coluna de nome 'Obesity' que conterá os valores de obesidade
df['Variation'] = df['Obesity (%)'].apply(lambda x: x.split(' ')[1])
df['Obesity'] = df['Obesity (%)'].apply(lambda x: x.split(' ')[0])


df.loc[df['Obesity'] == 'No', 'Obesity'] = np.nan
df.dropna(inplace=True)

# Transformando em float as colunas que foram importadas como string.
df['Obesity'] = df['Obesity'].str.replace(',','.').astype(float)
# df['Obesity'] = df['Obesity'].apply(lambda x: float(x))

df.info()

# %%
##############################################################################################

# Qual o percentual médio de obesidade por sexo no mundo no ano de 2015?

print('\nPercentual médio de obesidade por sexo no mundo em 2015:')
print('Feminino: ', end='')
print('{:.3f}' .format(df[(df['Year'] == 2015) & (df['Sex'] == 'Female')]['Obesity'].mean()))

print('Masculino: ', end='')
print('{:.3f}' .format(df[(df['Year'] == 2015) & (df['Sex'] == 'Male')]['Obesity'].mean()))

print('\n', df[df['Year'] == 2015].groupby('Sex').mean())


##############################################################################################

# Quais são os 5 países com a maior e a menor taxa de aumento nos índices de obesidade no período observado?

dif = df.groupby(['Country', 'Sex'])[['Obesity']].last() - df.groupby(['Country', 'Sex'])[['Obesity']].first()
dif.reset_index(inplace=True)

print('\nOs 5 países com maior taxa de aumento nos índices de obesidade no período observado para ambos os sexos são:')
maiores = dif[dif['Sex'] == 'Both sexes'].nlargest(5, 'Obesity')
print(maiores.reset_index())

print('\nOs 5 países com menor taxa de aumento nos índices de obesidade no período observado para ambos os sexos são:')
menores = dif[dif['Sex'] == 'Both sexes'].nsmallest(5, 'Obesity')
print(menores.reset_index())

# df_start = df[df['Year'] == 2016]
# df_end = df[df['Year'] == 1975]

# df_start.set_index(inplace=True)
# df_end.set_index(inplace=True)

# df_ev = df_end[df_end['Sex'] == 'Both sexes']['Obesity'] - df_start[df_start['Sex'] == 'Both sexes']['Obesity']

# df_ev.sort_values().dropna().head(5)
# df_ev.sort_values().dropna().tail(5)


##############################################################################################

# Quais os países com maiores e menores níveis percetuais de obesidade em 2015?

print('\nPaíses com maiores e menores níveis percentuais de obesidade em 2015:')
print('Maiores:')
print(df[(df['Year'] == 2015) & (df['Sex'] == 'Both sexes')][['Country', 'Year', 'Sex', 'Obesity']].sort_values(['Obesity'], ascending=False).head(5).reset_index())
print('\nMenores:')
print(df[(df['Year'] == 2015) & (df['Sex'] == 'Both sexes')][['Country', 'Year', 'Sex', 'Obesity']].sort_values(['Obesity']).head(5).reset_index())

'''
df_2015 = df[df['Country'] == 2015]
df_2015[df_2015['Obesity'] == df_2015['Obesity'].max()]
df_2015[df_2015['Obesity'] == df_2015['Obesity'].min()]
'''


##############################################################################################

# Qual a diferença média percentual de obesidade entre sexos ao longo dos anos para o Brasil?

male = df[(df['Country'] == 'Brazil') & (df['Sex'] == 'Male')][['Year', 'Obesity']].set_index('Year')
female = df[(df['Country'] == 'Brazil') & (df['Sex'] == 'Female')][['Year', 'Obesity']].set_index('Year')
difper = female[['Obesity']] - male[['Obesity']]

print('\nDiferença média percentual de obesidade entre os sexos ao longo dos anos no Brasil (Obs: o sexo feminimo obtém maior média ao longo dos anos):')
difper.plot(figsize=(15, 10))
print(difper)

'''
df_brazil = df[df['Country'] == 'Brazil']
df_brazil[df_brazil['Sex'] == 'Female']['Obesity'] - df_brazil[df_brazil['Sex'] == 'Male']['Obesity']
'''


##############################################################################################

# Você conseguiria plotar um gráfico mostrando a evolução da obesidade para ambos sexos no mundo?

df_ambos = df[df['Sex'] == 'Both sexes'].groupby('Year').mean().reset_index()
df_ambos.plot('Year', 'Obesity')
df_ambos.boxplot('Year', 'Obesity')

'''
df_both = df[df['Sex'] == 'Both sexes']
df_both.groupby('Year')['Obesity'].mean().plot()
'''

# %%
