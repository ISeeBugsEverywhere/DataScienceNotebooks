import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_icon=':bar_chart', page_title='Autoplius_analitika', layout='wide')
st.title('Automobilių kainų analizė')

# Funkcija, kuri gauna duomenis iš SQLite duomenų bazės
def query_to_dataframe(db_path, query):
    import sqlite3
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Nuskaitome duomenis iš duomenų bazės
db_path = '../../../web_scrap.db'
query = 'SELECT * FROM autopliuslt2;'
df = query_to_dataframe(db_path, query)

# Duomenų apdorojimas
dft = df.copy()
dft['Kaina'] = dft['Kaina'].apply(lambda x: float(x))
dft['Rida'] = dft['Rida'].apply(lambda x: x[:-3].replace(' ','') if x != None else x)
dft['Rida'] = dft['Rida'].apply(lambda x: float(x) if x != None and x != '' else x)
dft['Rida_group'] = dft['Rida'].apply(lambda x: np.ceil(x/50000)*50000)
dft['Amžius'] = dft['Pirma registracija'].apply(lambda x: (np.ceil((2024-int(x[:4]))/5))*5 if x != None else x)
dft['Amžius2'] = dft['Pirma registracija'].apply(lambda x: int(2024-int(x[:4])) if x != None else x)

def kw(x):
    if x != None:
        if 'kW' in x:
            return int((np.ceil(int(x.split('(')[1].replace('kW)',''))/20))*20)
        else:
            return None
    else:
        return None
    
def kw2(x):
    if x != None:
        if 'kW' in x:
            return int(x.split('(')[1].replace('kW)',''))
        else:
            return None
    else:
        return None

dft['Galingumas'] = dft['Variklis'].apply(kw)
dft['Galingumas2'] = dft['Variklis'].apply(kw2)
dft['Tik Miestas'] = dft['Miestas'].apply(lambda x: x.split(',')[0] if x!=None else None)
dft['TA'] = dft['Tech. apžiūra iki'].apply(lambda x: int(x[:4]) if x != None else None)
dft['Galioja_TA'] = dft['TA'].apply(lambda x: "Taip" if x>2024 else 'Ne')
dft['TA_m'] = dft['TA'].apply(lambda x: str(int(x)) if x>2024 else 'Negalioja')
dfpop = dft[dft['Markė'] != np.nan].groupby(['Markė'])['Kaina'].count().reset_index().sort_values(by= 'Kaina',ascending=False)[:10]
pop_markes = list(set(list(dfpop['Markė'])))
dfret = dft[dft['Markė'] != np.nan].groupby(['Markė'])['Kaina'].count().reset_index().sort_values(by= 'Kaina',ascending=True)
dfret['Retas'] = dfret['Kaina'].apply(lambda x: True if x>5 and x<15 else False)
dfreti = dfret[dfret['Retas'] == True].sort_values(by= 'Kaina',ascending=True)[:10]
ret_auto = list(set(list(dfreti['Markė'])))
dfe = dft[dft['Kuro tipas'] == 'Elektra']
dfe['Talpa'] = dfe['Baterijos talpa, kWh'].apply(lambda x: (np.ceil(int(x.replace(' kWh',''))/5))*5 if x!= None else None)
dft['El'] = dft['Kuro tipas'].apply(lambda x: "Elektra" if x == 'Elektra' else "VDV")
dft['Def'] = dft['Defektai'].apply(lambda x: "Be defektų" if x == None else "Su defektais")

# Pasirinkimas grafiko iš sąrašo
options = [
    'Kainos priklausomybė nuo ridos',
    'Kainos priklausomybė nuo amžiaus',
    'Kainos priklausomybė nuo galingumo',
    'Kainos priklausomybė nuo kėbulo tipo',
    'Kainos priklausomybė nuo pavarų dėžės',
    'Kainos priklausomybė nuo miesto',
    'Kainos priklausomybė nuo pirmosios registracijos šalies',
    'Kainos priklausomybė nuo TA galiojimo',
    'Populiariausi automobilių markės',
    'Kainos priklausomybė nuo ridos TOP10',
    'Kainos priklausomybė nuo galingumo TOP10',
    'Kainos priklausomybė nuo amžiaus TOP10',
    'Kainos kritimas nuo amžiaus TOP10',
    'Kainos kritimas nuo ridos TOP10',
    'Rečiausi auto',
    'TOP10 auto galingumai',
    'TOP10 auto ridos',
    'TOP10 auto ridos',
    'Elektromobilių kainos priklausomybė nuo baterijos talpos',
    'Elektromobilių kainos priklausomybė nuo galingumo',
    'Elektromobilių nuvertėjimas pagal amžių',
    'Elektromobilių nuvertėjimas pagal gamintoją ir amžių',
    'Elektromobilių nuvertėjimas pagal kūro tipą ir ridą',
    'Kokia dalis yra defektuotų auto',
    'Defektuoti auto pagal gamintoją'
]

# Vartotojas gali pasirinkti grafiką
selected_option = st.selectbox('Pasirinkite grafiką:', options)

# Funkcija grafiko rodymui pagal pasirinkimą
def show_chart(selected_option):
    fig, axes = plt.subplots(figsize=(25, 7))

    if selected_option == 'Kainos priklausomybė nuo ridos':
        dfx = dft.groupby(['Rida_group'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Rida_group', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Kainos priklausomybė nuo ridos')
        axes.set(xlabel='Rida', ylabel='Kaina')
        for container in axes.containers:
            axes.bar_label(container)


    elif selected_option == 'Kainos priklausomybė nuo amžiaus':
        dfx = dft.groupby(['Amžius'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Amžius', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Kainos priklausomybė nuo amžiaus')
        axes.set(xlabel='Amžius', ylabel='Kaina')
        for container in axes.containers:
            axes.bar_label(container)

    elif selected_option == 'Kainos priklausomybė nuo galingumo':
        dfx = dft[dft['Galingumas'].notna()].groupby(['Galingumas'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Galingumas', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Kainos priklausomybė nuo galingumo')
        axes.set(xlabel='Galingumas (kW)', ylabel='Kaina')
        for container in axes.containers:
            axes.bar_label(container)

    elif selected_option == 'Kainos priklausomybė nuo kėbulo tipo':
        dfx = dft.groupby(['Kėbulo tipas'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Kėbulo tipas', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Kainos priklausomybė nuo kėbulo tipo')
        axes.set(xlabel='Kėbulo tipas', ylabel='Kaina')
        for container in axes.containers:
            axes.bar_label(container)

    elif selected_option == 'Kainos priklausomybė nuo pavarų dėžės':
        dfx = dft.groupby(['Pavarų dėžė'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Pavarų dėžė', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Kainos priklausomybė nuo pavarų dėžės')
        axes.set(xlabel='Pavarų dėžė', ylabel='Kaina')
        for container in axes.containers:
            axes.bar_label(container)

    elif selected_option == 'Kainos priklausomybė nuo miesto':
        dfx = dft.groupby(['Tik Miestas'])['Kaina'].mean().reset_index().sort_values(by='Kaina', ascending=True)
        sns.lineplot(data=dfx, x='Tik Miestas', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Kainos priklausomybė nuo miesto')
        axes.set(xlabel='Miestas', ylabel='Kaina')

    elif selected_option == 'Kainos priklausomybė nuo pirmosios registracijos šalies':
        dfx = dft.groupby(['Pirmosios registracijos šalis'])['Kaina'].mean().reset_index().sort_values(by='Kaina', ascending=True)
        sns.barplot(data=dfx, x='Pirmosios registracijos šalis', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Kainos priklausomybė nuo pirmosios registracijos šalies')
        axes.set(xlabel='Pirmosios registracijos šalis', ylabel='Kaina')
        for container in axes.containers:
            axes.bar_label(container)

    elif selected_option == 'Kainos priklausomybė nuo TA galiojimo':
        dft['TA'] = dft['Tech. apžiūra iki'].apply(lambda x: int(x[:4]) if x != None else None)
        dft['Galioja_TA'] = dft['TA'].apply(lambda x: "Taip" if x > 2024 else 'Ne')
        dfx = dft.groupby(['Galioja_TA'])['Kaina'].mean().reset_index()
        sns.barplot(data=dfx, x='Galioja_TA', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Kainos priklausomybė nuo TA galiojimo')
        axes.set(xlabel='Ar galioja TA?', ylabel='Kaina')
        for container in axes.containers:
            axes.bar_label(container)

    elif selected_option == 'Populiariausi automobilių markės':
        dfx = dft.groupby(['Markė'])['Kaina'].count().reset_index().sort_values(by='Kaina', ascending=False)[:10]
        sns.barplot(data=dfx, x='Markė', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set_title('Populiariausi automobilių markės')
        axes.set(xlabel='Markė', ylabel='Kiekis')
        for container in axes.containers:
            axes.bar_label(container)
            
    elif selected_option == 'Kainos priklausomybė nuo ridos TOP10':
        dfx = dft[dft['Markė'].isin(pop_markes)].groupby(['Rida_group', 'Markė'])['Kaina'].mean().reset_index()
        axes.set_title(f'Kainos priklausomybė nuo ridos TOP10')
        ax =sns.barplot(data=dfx,x = 'Rida_group', y='Kaina', ax=axes, hue= 'Markė')
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Rida',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        axes.legend()
        
    elif selected_option == 'Kainos priklausomybė nuo galingumo TOP10':
        dfx = dft[dft['Markė'].isin(pop_markes)].groupby(['Galingumas', 'Markė'])['Kaina'].mean().reset_index()
        axes.set_title(f'Kainos priklausomybė nuo galingumo TOP10')
        ax =sns.barplot(data=dfx,x = 'Markė', y='Kaina', ax=axes, hue= 'Galingumas')
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Markės',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        axes.legend()
        
    elif selected_option == 'Kainos priklausomybė nuo amžiaus TOP10':
        dfx = dft[dft['Markė'].isin(pop_markes)].groupby(['Amžius', 'Markė'])['Kaina'].mean().reset_index()
        dfx['Amžius'] = dfx['Amžius'].apply(lambda x: int(x))
        axes.set_title(f'Kainos priklausomybė nuo amžiaus TOP10')
        ax =sns.lineplot(data=dfx,x = 'Amžius', y='Kaina', ax=axes, hue= 'Markė')
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Amžius',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        axes.legend()
        
    elif selected_option == 'Kainos kritimas nuo amžiaus TOP10':
        dfx = dft[dft['Markė'].isin(pop_markes)].groupby(['Amžius', 'Rida_group', 'Markė'])['Kaina'].mean().reset_index()
        dfx['Amžius'] = dfx['Amžius'].apply(lambda x: int(x))
        axes.set_title(f'Kainos kritimas nuo amžiaus TOP10')
        ax =sns.lineplot(data=dfx,x = 'Amžius', y='Kaina', ax=axes, hue= 'Markė')
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Amžius',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        axes.legend()
        
    elif selected_option == 'Kainos kritimas nuo ridos TOP10':
        dfx = dft[dft['Markė'].isin(pop_markes)].groupby(['Amžius', 'Rida_group', 'Markė'])['Kaina'].mean().reset_index()
        dfx['Amžius'] = dfx['Amžius'].apply(lambda x: int(x))
        axes.set_title(f'Kainos kritimas nuo ridos TOP10')
        ax =sns.barplot(data=dfx,x = 'Markė', y='Kaina', ax=axes, hue= 'Rida_group')
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Markė',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        axes.legend()
        
    elif selected_option == 'Rečiausi auto':
        dfx = dft[dft['Markė'].isin(ret_auto)].groupby(['Markė'])['Kaina'].count().reset_index().sort_values(by= 'Kaina', ascending=True)
        axes.set_title(f'Rečiausi auto')
        ax =sns.barplot(data=dfx,x = 'Markė', y='Kaina', )
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Markė',ylabel='Kiekis')
        for container in ax.containers:
            ax.bar_label(container)
        
    elif selected_option == 'TOP10 auto galingumai':
        dfx = dft[dft['Markė'].isin(pop_markes)]
        axes.set_title(f'TOP10 auto galingumai')
        ax =sns.boxplot(data=dfx,x = 'Markė', y='Galingumas2', showmeans=True, showfliers=False)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Markė',ylabel='Galingumas')
        
    elif selected_option == 'TOP10 auto ridos':
        dfx = dft[dft['Markė'].isin(pop_markes)]
        axes.set_title(f'TOP10 auto ridos')
        ax =sns.boxplot(data=dfx,x = 'Markė', y='Amžius2', showmeans=True, showfliers=False)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Markė',ylabel='Amžius')
        
    elif selected_option == 'TOP10 auto ridos':
        dfx = dft[dft['Kuro tipas'] == 'Elektra']
        axes.set_title(f'TOP10 auto ridos')
        ax =sns.boxplot(data=dfx,x = 'Markė', y='Amžius2', showmeans=True, showfliers=False)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Markė',ylabel='Amžius')
        
    elif selected_option == 'Elektromobilių kainos priklausomybė nuo baterijos talpos':
        dfx = dfe[dfe['Talpa'] != np.nan].groupby(['Talpa'])['Kaina'].mean().reset_index()
        axes.set_title(f'Elektromobilių kainos priklausomybė nuo baterijos talpos')
        ax =sns.barplot(data=dfx,x = 'Talpa', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Talpa kWh',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
            
    elif selected_option == 'Elektromobilių kainos priklausomybė nuo galingumo':
        dfx = dfe[dfe['Galingumas'] != np.nan].groupby(['Galingumas'])['Kaina'].mean().reset_index()
        axes.set_title(f'Elektromobilių kainos priklausomybė nuo galingumo')
        ax =sns.barplot(data=dfx,x = 'Galingumas', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Galingumas kW',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
            
    elif selected_option == 'Elektromobilių nuvertėjimas pagal amžių':
        dfx = dfe[dfe['Amžius'] != np.nan].groupby(['Amžius', 'Rida_group'])['Kaina'].mean().reset_index()
        axes.set_title(f'Elektromobilių nuvertėjimas pagal amžių')
        ax =sns.barplot(data=dfx,x = 'Amžius', y='Kaina', ax=axes, hue='Rida_group')
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Amžius',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        axes.legend()
            
    elif selected_option == 'Elektromobilių nuvertėjimas pagal gamintoją ir amžių':
        dfx = dfe[dfe['Amžius'] != np.nan].groupby(['Amžius', 'Markė'])['Kaina'].mean().reset_index()
        axes.set_title(f'Elektromobilių nuvertėjimas pagal gamintoją ir amžių')
        ax =sns.barplot(data=dfx,x = 'Markė', y='Kaina', ax=axes, hue='Amžius')
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Markė',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        axes.legend()
        
    elif selected_option == 'Elektromobilių nuvertėjimas pagal kūro tipą ir ridą':
        dfx = dft.groupby(['El', 'Rida_group'])['Kaina'].mean().reset_index()
        axes.set_title(f'Elektromobilių nuvertėjimas pagal kūro tipą ir ridą')
        ax =sns.barplot(data=dfx,x = 'Rida_group', y='Kaina', ax=axes, hue='El')
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Rida',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        axes.legend()
        
    elif selected_option == 'Kokia dalis yra defektuotų auto':
        dfx = dft.groupby(['Def'])['Kaina'].count().reset_index()
        axes.set_title(f'Kokia dalis yra defektuotų auto')
        ax =sns.barplot(data=dfx,x = 'Def', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Stadija',ylabel='Kiekis')
        for container in ax.containers:
            ax.bar_label(container)
            
    elif selected_option == 'Defektuoti auto pagal gamintoją':
        dfx = dft[dft['Def'] == 'Su defektais'].groupby(['Markė'])['Kaina'].count().reset_index().sort_values(by='Kaina', ascending=False)
        axes.set_title(f'Defektuoti auto pagal gamintoją')
        ax =sns.barplot(data=dfx,x = 'Markė', y='Kaina', ax=axes)
        axes.set_xticklabels(axes.get_xticklabels(), rotation=90)
        axes.set(xlabel='Gamintojas',ylabel='Kiekis')
        for container in ax.containers:
            ax.bar_label(container)

    st.pyplot(fig)

# Parodyti grafiką pagal vartotojo pasirinkimą
show_chart(selected_option)
