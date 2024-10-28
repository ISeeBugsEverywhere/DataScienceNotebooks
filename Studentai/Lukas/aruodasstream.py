import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
import sqlite3

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

#############################################################################
st.header('Vidutinis būtų plotas 5-iuose mietuose')

df_plotas = df[df['miestas'].isin(miestai)][['miestas', 'plotas']]
df_plotas_gr = df_plotas.groupby('miestas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=df_plotas_gr, x='miestas', y='plotas')
for container in ax.containers:
    ax.bar_label(container)
st.pyplot(fig, use_container_width=True)

######################################################
st.header('Butų pasisirstymas pagal plotą')

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
ax1.set_title('Vilniaus būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_kns, x='plotas5', y='Count', ax=ax2)
ax2.tick_params(axis='x', rotation=90, labelsize=8)
ax2.set_ylabel('Butų kiekis')
ax2.set_xlabel('plotas')
ax2.set_title('Kauno būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_klp, x='plotas5', y='Count', ax=ax3)
ax3.tick_params(axis='x', rotation=90, labelsize=8)
ax3.set_ylabel('Butų kiekis')
ax3.set_xlabel('plotas')
ax3.set_title('Klaipėdos būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_pal, x='plotas5', y='Count', ax=ax4)
ax4.tick_params(axis='x', rotation=90, labelsize=8)
ax4.set_ylabel('Butų kiekis')
ax4.set_xlabel('plotas')
ax4.set_title('Palangos būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)

sns.barplot(data=df_pal, x='plotas5', y='Count', ax=ax5)
ax5.tick_params(axis='x', rotation=90, labelsize=8)
ax5.set_ylabel('Butų kiekis')
ax5.set_xlabel('plotas')
ax5.set_title('Panevėžio būtų pasiskirtysmas pagal plotą')
# for container in ax1.containers:
#     ax1.bar_label(container)


fig.tight_layout()
st.pyplot(fig, use_container_width=True)


#############################################

st.header('Vidutinos pastatų amžius (parduodami butai)')

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
st.pyplot(fig, use_container_width=True)

###########################################

st.header('Vidutinė kainos prikklausomybė nuo pastato energetinės klasės')

df_energija= df[(df['miestas'].isin(miestai))][['miestas', 'Pastato energijos suvartojimo klasė:', 'kaina']]
df_energija_gr = df_energija.groupby(['miestas','Pastato energijos suvartojimo klasė:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_energija_gr, x='miestas', y='kaina', hue='Pastato energijos suvartojimo klasė:')
ax.set_title('Vidutinė kainos prikklausomybė nuo pastato energetinės klasės')
st.pyplot(fig, use_container_width=True)

#############################################

st.header('Vidutinė kainos prikklausomybė nuo šildymo būdo')

sildymas = df[df['miestas'].isin(miestai)]['Šildymas:'].value_counts()
top10s = sildymas.head(10).index.to_list()

df_sildymas= df[(df['miestas'].isin(miestai)) & (df['Šildymas:'].isin(top10s))][['miestas', 'Šildymas:', 'kaina']]
df_sildymas_gr = df_sildymas.groupby(['miestas','Šildymas:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_sildymas_gr, x='miestas', y='kaina', hue='Šildymas:')
ax.set_title('Vidutinė kainos prikklausomybė nuo šildymo būdo')
st.pyplot(fig, use_container_width=True)

###################################################

st.header('Kainų išsibarstymas pasirinktuose miestuose')

df_x = df[(df['miestas'].isin(miestai))]

fig, axes = plt.subplots(figsize=(8, 4.5))


sns.boxplot(data=df_x,x = 'miestas', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Miestai',ylabel='kaina')
# for container in ax.containers:
#     ax.bar_label(container)
# axes.legend()
st.pyplot(fig, use_container_width=True)

####################################################

st.header('Vidutinė kainos priklausomybė nuo pastato tipo')

df_tipas= df[(df['miestas'].isin(miestai))][['miestas', 'Pastato tipas:', 'kaina']]
df_tipas_gr = df_tipas.groupby(['miestas','Pastato tipas:']).mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=df_tipas_gr, x='miestas', y='kaina', hue='Pastato tipas:')
ax.set_title('Vidutinė kainos priklausomybė nuo pastato tipo')
# for container in ax.containers:
#     ax.bar_label(container)
st.pyplot(fig, use_container_width=True)

###########################################################

st.header('kainos priklausomybė nuo pastato tipo ir amžiaus')

df_k = df[df['miestas'].isin(miestai)][['amzius', 'kaina', 'Pastato tipas:']].groupby(['amzius', 'Pastato tipas:']).mean(numeric_only=True).reset_index()

fig, axis = plt.subplots(figsize=(8,4.5))
#plotting code:

sns.scatterplot(data=df_k, x='amzius', y='kaina', hue='Pastato tipas:', ax=axis)
axis.set_xlim(0, 180)
axis.set_ylim(0, 800000)

axis.legend(loc='best')
plt.title('kainos priklausomybė nuo pastato tipo ir amžiaus')

st.pyplot(fig, use_container_width=True)

##########################################

st.header('kainos pasiskirstymas nuo pastato tipo')

df_x = df[(df['miestas'].isin(miestai))]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'miestas', y='kaina', hue='Pastato tipas:', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='Miestai',ylabel='kaina')
plt.title('kainos pasiskirstymas nuo pastato tipo')
st.pyplot(fig, use_container_width=True)

#######################################

st.header('kainos pasiskirtymas nuo buto aukšto')

df_x = df[(df['miestas'].isin(miestai))]

order_str = sorted(df_x['Aukštas:'].unique())
order = sorted([int(x) for x in order_str])
order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False, order=order_str2)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='aukštas',ylabel='kaina')
plt.title('kainos pasiskirtymas nuo buto aukšto')
st.pyplot(fig, use_container_width=True)


#######################################

st.header('kainos pasiskirtymas pastato aukštų skaičiaus')

df_x = df[(df['miestas'].isin(miestai))]

order_str = sorted(df_x['Aukštų sk.:'].unique())
order = sorted([int(x) for x in order_str])
order_str2 = [str(x) for x in order]

fig, axes = plt.subplots(figsize=(12, 4.5))


sns.boxplot(data=df_x,x = 'Aukštų sk.:', y='kaina', showmeans=True, showfliers=False, order=order_str2)
# sns.boxplot(data=df_x,x = 'Aukštas:', y='kaina', showmeans=True, showfliers=False)
# axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
axes.set(xlabel='aukštas',ylabel='kaina')
plt.title('kainos pasiskirtymas pastato aukštų skaičiaus')
st.pyplot(fig, use_container_width=True)

#############################################

st.header('Butų kiekis Vilniaus rajonuose')

rajonas = df[(df['miestas'] == 'Vilnius')]['rajonas'].value_counts()
fig, ax = plt.subplots(figsize=(8, 10))
B1 = ax.barh(rajonas.index, rajonas.values)
ax.bar_label(B1)
# ax.tick_params(axis='x', label='butų kiekis')
ax.set_xlabel('butų kiekis')
plt.title('Butų kiekis Vilniaus rajonuose')
st.pyplot(fig, use_container_width=True)

##############################################

st.header('Vidutinis pastatų amžius rajonuose (parduodami butai)')

rajonas_amz= df[(df['miestas'] == 'Vilnius')][['rajonas', 'amzius']]
rajonas_amz_gr = rajonas_amz.groupby('rajonas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(12, 4.5))
sns.barplot(data=rajonas_amz_gr, x='rajonas', y='amzius')
ax.set_title('Vidutinis pastatų amžius rajonuose (parduodami butai)')
ax.tick_params(axis='x', rotation=90)
# for container in ax.containers:
#     ax.bar_label(container)
st.pyplot(fig, use_container_width=True)

#################################################

st.header('Pastatų amžiaus pasiskirstymas Vilniaus rajonuose')

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
plt.title('Pastatų amžiaus pasiskirstymas Vilniaus rajonuose')
st.pyplot(fig, use_container_width=True)

##################################################

st.header('vidutinė būtų kaina Vilniaus rajonuose (parduodami butai)')

rajonas_amz= df[(df['miestas'] == 'Vilnius')][['rajonas', 'kaina']]
rajonas_amz_gr = rajonas_amz.groupby('rajonas').mean(numeric_only=True)

fig, ax = plt.subplots(figsize=(12, 4.5))
sns.barplot(data=rajonas_amz_gr, x='rajonas', y='kaina')
ax.set_title('vidutinė būtų kaina rajonuose (parduodami butai)')
ax.tick_params(axis='x', rotation=90)
# for container in ax.containers:
#     ax.bar_label(container)
st.pyplot(fig, use_container_width=True)

#######################################################

st.header('Kainos pasiskirstymas Vilniaus rajonuose')

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
plt.title('Kainos pasiskirstymas Vilniaus rajonuose')
st.pyplot(fig, use_container_width=True)

###########################################################

st.header('Butų ploto pasiskirstymas Vilniaus rajonuose')

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
plt.title('Butų ploto pasiskirstymas Vilniaus rajonuose')
st.pyplot(fig, use_container_width=True)