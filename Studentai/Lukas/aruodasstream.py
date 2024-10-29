import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
import sqlite3
import requests
import plotly.express as px

#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')


SDB = sqlite3.connect('aruodas.db')
Cs = SDB.cursor()

sql="""select * from Aruodas;"""
df_with_dubs = pd.read_sql_query(sql, con=SDB)
df = df_with_dubs.drop_duplicates()

miestai = ['Vilnius', 'Kaunas', 'Klaipėda', 'Palanga', 'Panevėžys']

def plotas(x):
    # if 'm²' in x:
    if x is not None:
        return float(x.replace(' m²', '',).replace(',', '.'))
    else:
        return np.nan
    
df['plotas'] = df['Plotas:'].apply(plotas)
df['plotas5'] = df[df['plotas'] != None]['plotas'].apply(lambda x: float(np.ceil(x/5) * 5))

# nuoma
sql="""select * from Nuoma;"""
dfn_with_dubs = pd.read_sql_query(sql, con=SDB)
dfn = dfn_with_dubs.drop_duplicates()

dfn['plotas'] = dfn['Plotas:'].apply(plotas)
dfn['plotas5'] = dfn[dfn['plotas'] != None]['plotas'].apply(lambda x: float(np.ceil(x/5) * 5))


#############################################################################
st.header('Vidutinis būtų plotas 5-iuose mietuose')

left, right = st.columns(2)

df_plotas = df[df['miestas'].isin(miestai)][['miestas', 'plotas']]
df_plotas_gr = df_plotas.groupby('miestas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=df_plotas_gr, x='miestas', y='plotas')
ax.set_title('Parduodami butai')
for container in ax.containers:
    ax.bar_label(container)
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_plotas = dfn[dfn['miestas'].isin(miestai)][['miestas', 'plotas']]
dfn_plotas_gr = dfn_plotas.groupby('miestas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=dfn_plotas_gr, x='miestas', y='plotas')
ax.set_title('Butų nuoma')
for container in ax.containers:
    ax.bar_label(container)
right.pyplot(fig, use_container_width=True)

######################################################
st.header('Butų pasisirstymas pagal plotą')

left, right = st.columns(2)

df_vln = df[df['miestas'] == 'Vilnius'].groupby(['plotas5']).size().reset_index(name='Count')
df_kns = df[df['miestas'] == 'Kaunas'].groupby(['plotas5']).size().reset_index(name='Count')
df_klp = df[df['miestas'] == 'Klaipėda'].groupby(['plotas5']).size().reset_index(name='Count')
df_pal = df[df['miestas'] == 'Palanga'].groupby(['plotas5']).size().reset_index(name='Count')
df_pan = df[df['miestas'] == 'Panavėžys'].groupby(['plotas5']).size().reset_index(name='Count')

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1,figsize=(8, 20))

sns.barplot(data=df_vln, x='plotas5', y='Count', ax=ax1)
ax1.tick_params(axis='x', rotation=90, labelsize=8)
ax1.set_ylabel('Butų kiekis')
ax1.set_xlabel('plotas')
ax1.set_title('Vilniaus būtų pasiskirtysmas pagal plotą (parduodami)')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_kns, x='plotas5', y='Count', ax=ax2)
ax2.tick_params(axis='x', rotation=90, labelsize=8)
ax2.set_ylabel('Butų kiekis')
ax2.set_xlabel('plotas')
ax2.set_title('Kauno būtų pasiskirtysmas pagal plotą (parduodami)')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_klp, x='plotas5', y='Count', ax=ax3)
ax3.tick_params(axis='x', rotation=90, labelsize=8)
ax3.set_ylabel('Butų kiekis')
ax3.set_xlabel('plotas')
ax3.set_title('Klaipėdos būtų pasiskirtysmas pagal plotą (parduodami)')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_pal, x='plotas5', y='Count', ax=ax4)
ax4.tick_params(axis='x', rotation=90, labelsize=8)
ax4.set_ylabel('Butų kiekis')
ax4.set_xlabel('plotas')
ax4.set_title('Palangos būtų pasiskirtysmas pagal plotą (parduodami)')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_pal, x='plotas5', y='Count', ax=ax5)
ax5.tick_params(axis='x', rotation=90, labelsize=8)
ax5.set_ylabel('Butų kiekis')
ax5.set_xlabel('plotas')
ax5.set_title('Panevėžio būtų pasiskirtysmas pagal plotą (parduodami)')
# for container in ax1.containers:
#     ax1.bar_label(container)


fig.tight_layout()
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_vln = dfn[dfn['miestas'] == 'Vilnius'].groupby(['plotas5']).size().reset_index(name='Count')
dfn_kns = dfn[dfn['miestas'] == 'Kaunas'].groupby(['plotas5']).size().reset_index(name='Count')
dfn_klp = dfn[dfn['miestas'] == 'Klaipėda'].groupby(['plotas5']).size().reset_index(name='Count')
dfn_pal = dfn[dfn['miestas'] == 'Palanga'].groupby(['plotas5']).size().reset_index(name='Count')
dfn_pan = dfn[dfn['miestas'] == 'Panavėžys'].groupby(['plotas5']).size().reset_index(name='Count')


# Find the most common apartment area in each city
# most_common = df_miestai.loc[df_miestai.groupby('miestas')['Count'].idxmax()]

# print(most_common)

# # Optional: Visualize the results
fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5,1,figsize=(8, 20))

sns.barplot(data=dfn_vln, x='plotas5', y='Count', ax=ax1)
ax1.tick_params(axis='x', rotation=90, labelsize=8)
ax1.set_ylabel('Butų kiekis')
ax1.set_xlabel('plotas')
ax1.set_title('Vilniaus būtų pasiskirtysmas pagal plotą (nuoma)')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=dfn_kns, x='plotas5', y='Count', ax=ax2)
ax2.tick_params(axis='x', rotation=90, labelsize=8)
ax2.set_ylabel('Butų kiekis')
ax2.set_xlabel('plotas')
ax2.set_title('Kauno būtų pasiskirtysmas pagal plotą (nuoma)')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=dfn_klp, x='plotas5', y='Count', ax=ax3)
ax3.tick_params(axis='x', rotation=90, labelsize=8)
ax3.set_ylabel('Butų kiekis')
ax3.set_xlabel('plotas')
ax3.set_title('Klaipėdos būtų pasiskirtysmas pagal plotą (nuoma)')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=dfn_pal, x='plotas5', y='Count', ax=ax4)
ax4.tick_params(axis='x', rotation=90, labelsize=8)
ax4.set_ylabel('Butų kiekis')
ax4.set_xlabel('plotas')
ax4.set_title('Palangos būtų pasiskirtysmas pagal plotą (nuoma)')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=dfn_pal, x='plotas5', y='Count', ax=ax5)
ax5.tick_params(axis='x', rotation=90, labelsize=8)
ax5.set_ylabel('Butų kiekis')
ax5.set_xlabel('plotas')
ax5.set_title('Panevėžio būtų pasiskirtysmas pagal plotą (nuoma)')
# for container in ax1.containers:
#     ax1.bar_label(container)


fig.tight_layout()
right.pyplot(fig, use_container_width=True)


#############################################

st.header('Vidutinis pastatų amžius')

left, right = st.columns(2)

def amzius(x):
    return  2024 - int(x[:4])

df['amzius'] = df['Metai:'].apply(amzius)


df_amzius= df[df['miestas'].isin(miestai)][['miestas', 'amzius']]
df_amzius_gr = df_amzius.groupby('miestas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=df_amzius_gr, x='miestas', y='amzius')
ax.set_title('Vidutinos pastatų amžius (parduodami butai)')
for container in ax.containers:
    ax.bar_label(container)
left.pyplot(fig, use_container_width=True)

# nuoma
dfn['amzius'] = dfn['Metai:'].apply(amzius)


dfn_amzius= dfn[dfn['miestas'].isin(miestai)][['miestas', 'amzius']]
dfn_amzius_gr = dfn_amzius.groupby('miestas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=dfn_amzius_gr, x='miestas', y='amzius')
ax.set_title('Vidutinis pastatų amžius (nuoma)')
for container in ax.containers:
    ax.bar_label(container)
right.pyplot(fig, use_container_width=True)

###########################################

st.header('Vidutinė kainos prikklausomybė nuo pastato energetinės klasės')

left, right = st.columns(2)

df_energija= df[(df['miestas'].isin(miestai))][['miestas', 'Pastato energijos suvartojimo klasė:', 'kaina']]
df_energija_gr = df_energija.groupby(['miestas','Pastato energijos suvartojimo klasė:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_energija_gr, x='miestas', y='kaina', hue='Pastato energijos suvartojimo klasė:')
ax.set_title('Vidutinė kainos prikklausomybė nuo pastato energetinės klasės (parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_energija= dfn[(dfn['miestas'].isin(miestai))][['miestas', 'Pastato energijos suvartojimo klasė:', 'kaina']]
dfn_energija_gr = dfn_energija.groupby(['miestas','Pastato energijos suvartojimo klasė:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=dfn_energija_gr, x='miestas', y='kaina', hue='Pastato energijos suvartojimo klasė:')
ax.set_title('Vidutinė kainos priklausomybė nuo pastato energetinės klasės (nuoma)')
# for container in ax.containers:
#     ax.bar_label(container)
right.pyplot(fig, use_container_width=True)

#############################################

st.header('Vidutinė kainos priklausomybė nuo šildymo būdo')

left, right = st.columns(2)

sildymas = df[df['miestas'].isin(miestai)]['Šildymas:'].value_counts()
top10s = sildymas.head(10).index.to_list()

df_sildymas= df[(df['miestas'].isin(miestai)) & (df['Šildymas:'].isin(top10s))][['miestas', 'Šildymas:', 'kaina']]
df_sildymas_gr = df_sildymas.groupby(['miestas','Šildymas:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_sildymas_gr, x='miestas', y='kaina', hue='Šildymas:')
ax.set_title('Vidutinė kainos prikklausomybė nuo šildymo būdo (parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
sildymasn = dfn[dfn['miestas'].isin(miestai)]['Šildymas:'].value_counts()
top10sn = sildymasn.head(10).index.to_list()

dfn_sildymas= dfn[(dfn['miestas'].isin(miestai)) & (dfn['Šildymas:'].isin(top10sn))][['miestas', 'Šildymas:', 'kaina']]
dfn_sildymas_gr = dfn_sildymas.groupby(['miestas','Šildymas:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=dfn_sildymas_gr, x='miestas', y='kaina', hue='Šildymas:')
ax.set_title('Vidutinė kainos prikklausomybė nuo šildymo būdo (nuoma)')
# for container in ax.containers:
#     ax.bar_label(container)
right.pyplot(fig, use_container_width=True)


###################################################

st.header('Kainų išsibarstymas pasirinktuose miestuose')

left, right = st.columns(2)

df_x = df[(df['miestas'].isin(miestai))]

fig, axes = plt.subplots(figsize=(8, 4.5))


sns.boxplot(data=df_x,x = 'miestas', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Miestai',ylabel='kaina')
axes.set_title('Parduodami butai')
# for container in ax.containers:
#     ax.bar_label(container)
# axes.legend()
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_x = dfn[(dfn['miestas'].isin(miestai))]

fig, axes = plt.subplots(figsize=(8, 4.5))


sns.boxplot(data=dfn_x,x = 'miestas', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Miestai',ylabel='kaina')
axes.set_title('Nuomuojami butai')
# for container in ax.containers:
#     ax.bar_label(container)
# axes.legend()
right.pyplot(fig, use_container_width=True)

####################################################

st.header('Vidutinė kainos priklausomybė nuo pastato tipo')

left, right = st.columns(2)

df_tipas= df[(df['miestas'].isin(miestai))][['miestas', 'Pastato tipas:', 'kaina']]
df_tipas_gr = df_tipas.groupby(['miestas','Pastato tipas:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_tipas_gr, x='miestas', y='kaina', hue='Pastato tipas:')
ax.set_title('Vidutinė kainos priklausomybė nuo pastato tipo (Parduodami)')
# for container in ax.containers:
#     ax.bar_label(container)
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_tipas= dfn[(dfn['miestas'].isin(miestai))][['miestas', 'Pastato tipas:', 'kaina']]
dfn_tipas_gr = dfn_tipas.groupby(['miestas','Pastato tipas:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=dfn_tipas_gr, x='miestas', y='kaina', hue='Pastato tipas:')
ax.set_title('Vidutinė kainos priklausomybė nuo pastato tipo (Nuoma)')
# for container in ax.containers:
#     ax.bar_label(container)
right.pyplot(fig, use_container_width=True)

###########################################################

st.header('kainos priklausomybė nuo pastato tipo ir amžiaus')

left, right = st.columns(2)

df_k = df[df['miestas'].isin(miestai)][['amzius', 'kaina', 'Pastato tipas:']].groupby(['amzius', 'Pastato tipas:']).mean(numeric_only=True).reset_index()

fig, axis = plt.subplots(figsize=(8,4.5))
#plotting code:

sns.scatterplot(data=df_k, x='amzius', y='kaina', hue='Pastato tipas:', ax=axis)
axis.set_xlim(0, 180)
axis.set_ylim(0, 800000)

axis.legend(loc='best')
plt.title('kainos priklausomybė nuo pastato tipo ir amžiaus (Parduodami)')

left.pyplot(fig, use_container_width=True)

# nuoma
dfn_k = dfn[dfn['miestas'].isin(miestai)][['amzius', 'kaina', 'Pastato tipas:']].groupby(['amzius', 'Pastato tipas:']).mean(numeric_only=True).reset_index()

fig, axis = plt.subplots(figsize=(8,4.5))
#plotting code:

sns.scatterplot(data=dfn_k, x='amzius', y='kaina', hue='Pastato tipas:', ax=axis)
axis.set_xlim(0, 180)
axis.set_ylim(0, 2000)

axis.legend(loc='best')
plt.title('kainos priklausomybė nuo pastato tipo ir amžiaus (Nuoma)')

right.pyplot(fig, use_container_width=True)


##########################################

st.header('Kainos pasiskirstymas nuo pastato tipo')

left, right = st.columns(2)

df_x = df[(df['miestas'].isin(miestai))]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'miestas', y='kaina', hue='Pastato tipas:', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Miestai',ylabel='kaina')
plt.title('kainos pasiskirstymas nuo pastato tipo (Parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_x = dfn[(dfn['miestas'].isin(miestai))]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=dfn_x,x = 'miestas', y='kaina', hue='Pastato tipas:', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Miestai',ylabel='kaina')
plt.title('kainos priklausomybė nuo pastato (Nuoma)')
right.pyplot(fig, use_container_width=True)


#######################################

st.header('Kainos pasiskirtymas nuo buto aukšto')

left, right = st.columns(2)

df_x = df[(df['miestas'].isin(miestai))]

order_str = sorted(df_x['Aukštas:'].unique())
order = sorted([int(x) for x in order_str])
order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False, order=order_str2)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='aukštas',ylabel='kaina')
plt.title('Kainos pasiskirtymas nuo buto aukšto (Parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_x = dfn[(dfn['miestas'].isin(miestai))]

ordern_str = sorted(dfn_x['Aukštas:'].unique())
ordern = sorted([int(x) for x in ordern_str])
ordern_str2 = [str(x) for x in ordern]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=dfn_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False, order=ordern_str2)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='aukštas',ylabel='kaina')
plt.title('Kainos priklausomybė buto aukšto (Nuoma)')
right.pyplot(fig, use_container_width=True)


#######################################

st.header('Kainos pasiskirtymas pastato aukštų skaičiaus')

left, right = st.columns(2)

df_x = df[(df['miestas'].isin(miestai))]

order_str = sorted(df_x['Aukštų sk.:'].unique())
order = sorted([int(x) for x in order_str])
order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'Aukštų sk.:', y='kaina', showmeans=True, showfliers=False, order=order_str2)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='aukštas',ylabel='kaina')
plt.title('kainos pasiskirtymas pastato aukštų skaičiaus (Parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_x = dfn[(dfn['miestas'].isin(miestai))]

ordern_str = sorted(dfn_x['Aukštų sk.:'].unique())
ordern = sorted([int(x) for x in ordern_str])
ordern_str2 = [str(x) for x in ordern]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=dfn_x,x = 'Aukštų sk.:', y='kaina', showmeans=True, showfliers=False, order=ordern_str2)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='aukštas',ylabel='kaina')
plt.title('kainos priklausomybė pastato aukštų skaičiaus (Nuoma)')
right.pyplot(fig, use_container_width=True)

#############################################

st.header('Butų kiekis Vilniaus rajonuose')

left, right = st.columns(2)

rajonas = df[(df['miestas'] == 'Vilnius')]['rajonas'].value_counts()
fig, ax = plt.subplots(figsize=(8, 10))
B1 = ax.barh(rajonas.index, rajonas.values)
ax.bar_label(B1)
# ax.tick_params(axis='x', label='butų kiekis')
ax.set_xlabel('butų kiekis')
plt.title('Butų kiekis Vilniaus rajonuose (Parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
rajonasn = dfn[(dfn['miestas'] == 'Vilnius')]['rajonas'].value_counts()
fig, ax = plt.subplots(figsize=(8, 10))
B1 = ax.barh(rajonasn.index, rajonasn.values)
ax.bar_label(B1)
# ax.tick_params(axis='x', label='butų kiekis')
ax.set_xlabel('butų kiekis')
plt.title('Butų kiekis Vilniaus rajonuose (Nuoma)')
right.pyplot(fig, use_container_width=True)


##############################################

st.header('Vidutinis pastatų amžius rajonuose')

left, right = st.columns(2)

rajonas_amz= df[(df['miestas'] == 'Vilnius')][['rajonas', 'amzius']]
rajonas_amz_gr = rajonas_amz.groupby('rajonas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(12, 4.5))
sns.barplot(data=rajonas_amz_gr, x='rajonas', y='amzius')
ax.set_title('Vidutinis pastatų amžius rajonuose (Parduodami butai)')
ax.tick_params(axis='x', rotation=90)
# for container in ax.containers:
#     ax.bar_label(container)
left.pyplot(fig, use_container_width=True)

# nuoma
rajonasn_amz= dfn[(dfn['miestas'] == 'Vilnius')][['rajonas', 'amzius']]
rajonasn_amz_gr = rajonasn_amz.groupby('rajonas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(12, 4.5))
sns.barplot(data=rajonasn_amz_gr, x='rajonas', y='amzius')
ax.set_title('Vidutinis pastatų amžius rajonuose (Nuoma)')
ax.tick_params(axis='x', rotation=90)
# for container in ax.containers:
#     ax.bar_label(container)
right.pyplot(fig, use_container_width=True)

#################################################

st.header('Pastatų amžiaus pasiskirstymas Vilniaus rajonuose')

left, right = st.columns(2)

df_x = df[(df['miestas'] == 'Vilnius')][['rajonas', 'amzius']]

# order_str = sorted(df_x['Aukštų sk.:'].unique())
# order = sorted([int(x) for x in order_str])
# order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'rajonas', y='amzius', showmeans=True, showfliers=False)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='amžius',ylabel='kaina')
axes.tick_params(axis='x', rotation=90)
plt.title('Pastatų amžiaus pasiskirstymas Vilniaus rajonuose (Parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_x = dfn[(dfn['miestas'] == 'Vilnius')][['rajonas', 'amzius']]

# order_str = sorted(df_x['Aukštų sk.:'].unique())
# order = sorted([int(x) for x in order_str])
# order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=dfn_x,x = 'rajonas', y='amzius', showmeans=True, showfliers=False)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='amžius',ylabel='kaina')
axes.tick_params(axis='x', rotation=90)
plt.title('Pastatų amžiaus pasiskirstymas Vilniaus rajonuose (Nuoma)')
right.pyplot(fig, use_container_width=True)

##################################################

st.header('Vidutinė būtų kaina Vilniaus rajonuose')

left, right = st.columns(2)

rajonas_amz= df[(df['miestas'] == 'Vilnius')][['rajonas', 'kaina']]
rajonas_amz_gr = rajonas_amz.groupby('rajonas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(12, 4.5))
sns.barplot(data=rajonas_amz_gr, x='rajonas', y='kaina')
ax.set_title('Vidutinė būtų kaina rajonuose (parduodami butai)')
ax.tick_params(axis='x', rotation=90)
# for container in ax.containers:
#     ax.bar_label(container)
left.pyplot(fig, use_container_width=True)

#nuoma
rajonasn_amz= dfn[(dfn['miestas'] == 'Vilnius')][['rajonas', 'kaina']]
rajonasn_amz_gr = rajonasn_amz.groupby('rajonas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(12, 4.5))
sns.barplot(data=rajonasn_amz_gr, x='rajonas', y='kaina')
ax.set_title('Vidutinė būtų kaina rajonuose (Nuoma)')
ax.tick_params(axis='x', rotation=90)
# for container in ax.containers:
#     ax.bar_label(container)
right.pyplot(fig, use_container_width=True)


#######################################################

st.header('Kainos pasiskirstymas Vilniaus rajonuose')

left, right = st.columns(2)

df_x = df[(df['miestas'] == 'Vilnius')][['rajonas', 'kaina']]

# order_str = sorted(df_x['Aukštų sk.:'].unique())
# order = sorted([int(x) for x in order_str])
# order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'rajonas', y='kaina', showmeans=True, showfliers=False)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='rajonai',ylabel='kaina')
axes.tick_params(axis='x', rotation=90)
plt.title('Kainos pasiskirstymas Vilniaus rajonuose (Parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_x = dfn[(dfn['miestas'] == 'Vilnius')][['rajonas', 'kaina']]

# order_str = sorted(df_x['Aukštų sk.:'].unique())
# order = sorted([int(x) for x in order_str])
# order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=dfn_x,x = 'rajonas', y='kaina', showmeans=True, showfliers=False)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='rajonai',ylabel='kaina')
axes.tick_params(axis='x', rotation=90)
plt.title('Kainos pasiskirstymas Vilniaus rajonuose (Nuoma)')
right.pyplot(fig, use_container_width=True)


###########################################################

st.header('Butų ploto pasiskirstymas Vilniaus rajonuose')

left, right = st.columns(2)

df_x = df[(df['miestas'] == 'Vilnius')][['rajonas', 'plotas']]

# order_str = sorted(df_x['Aukštų sk.:'].unique())
# order = sorted([int(x) for x in order_str])
# order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'rajonas', y='plotas', showmeans=True, showfliers=False)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='rajonai',ylabel='plotas')
axes.tick_params(axis='x', rotation=90)
plt.title('Butų ploto pasiskirstymas Vilniaus rajonuose (Parduodami)')
left.pyplot(fig, use_container_width=True)

# nuoma
dfn_x = dfn[(dfn['miestas'] == 'Vilnius')][['rajonas', 'plotas']]

# order_str = sorted(df_x['Aukštų sk.:'].unique())
# order = sorted([int(x) for x in order_str])
# order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=dfn_x,x = 'rajonas', y='plotas', showmeans=True, showfliers=False)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='rajonai',ylabel='plotas')
axes.tick_params(axis='x', rotation=90)
plt.title('Butų ploto pasiskirstymas Vilniaus rajonuose (Nuoma)')
right.pyplot(fig, use_container_width=True)

##################################################################

st.header('Butai Vilniuje')

left, right = st.columns(2)

def get_city_coordinates(city_name, country_name=None):
    # Construct the Nominatim API URL
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': city_name,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    
    if country_name:
        params['country'] = country_name

    # Make the request
    response = requests.get(base_url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        if results:
            # Extract the coordinates
            lat = results[0]['lat']
            lon = results[0]['lon']
            return [lat, lon]
        else:
            print("No results found.")
            return None
    else:
        print("Error:", response.status_code)
        return None
    

rajonai = list(set(df[df['miestas'] == 'Vilnius']['rajonas'].values.tolist()))
# print(rajonai)
# print(len(rajonai))
rajonai_dict = {}

for i in rajonai:
    vieta = f'Vilnius {i}'
    coordinates = get_city_coordinates(vieta)
    rajonai_dict[i] = coordinates
    
# print(rajonai_dict)

vilnius = df[df['miestas'] == 'Vilnius']

def get_lat(x):
    return float(rajonai_dict[x][0])

def get_lon(x):
    return float(rajonai_dict[x][1])

vilnius['lat'] = vilnius['rajonas'].apply(get_lat)
vilnius['lon'] = vilnius['rajonas'].apply(get_lon)

# kiek kartų pasikartoja rajonas
from collections import Counter
count_rajonai = df[df['miestas'] == 'Vilnius']['rajonas'].values.tolist()
counts = Counter(count_rajonai)

def get_count(x):
    return counts[x]

vilnius['count'] = vilnius['rajonas'].apply(get_count)

fig = px.scatter_mapbox(data_frame=vilnius, lon='lon', lat='lat', zoom=5,
                        size='count',  # Use 'count' to determine marker size
                        hover_name='count',  # Display count on hover
                        size_max=30, # Maximum size of markers 
                        title='Parduodami butai Vilniuje') 
fig.update_layout(mapbox_style='open-street-map')
fig.update_layout(width=800, height=600)
# fig.update_traces(cluster=dict(enabled=True))
# st.pyplot(fig, use_container_width=True)
left.plotly_chart(fig)

# nuoma

rajonain = list(set(dfn[dfn['miestas'] == 'Vilnius']['rajonas'].values.tolist()))
# print(rajonai)
# print(len(rajonai))
rajonain_dict = {}

for i in rajonain:
    vieta = f'Vilnius {i}'
    coordinates = get_city_coordinates(vieta)
    rajonain_dict[i] = coordinates


vilniusn = dfn[dfn['miestas'] == 'Vilnius']

def getn_lat(x):
    if x is not None:
        return float(rajonain_dict[x][0])

def getn_lon(x):
    if x is not None:
        return float(rajonain_dict[x][1])

vilniusn['lat'] = vilniusn['rajonas'].apply(getn_lat)
vilniusn['lon'] = vilniusn['rajonas'].apply(getn_lon)


count_rajonain = dfn[dfn['miestas'] == 'Vilnius']['rajonas'].values.tolist()
countsn = Counter(count_rajonain)


vilniusn['count'] = vilniusn['rajonas'].apply(get_count)

fig = px.scatter_mapbox(data_frame=vilniusn, lon='lon', lat='lat', zoom=5,
                        size='count',  # Use 'count' to determine marker size
                        hover_name='count',  # Display count on hover
                        size_max=30, # Maximum size of markers 
                        title='Nuomuojami butai Vilniuje') 
fig.update_layout(mapbox_style='open-street-map')
fig.update_layout(width=800, height=600)
# fig.update_traces(cluster=dict(enabled=True))
right.plotly_chart(fig)

##################################################################################