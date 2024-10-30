import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(page_icon=':bar_chart', page_title='Aruodas_analitika', layout='centered')
st.title('NT rinkos analizė')

# Funkcija, kuri gauna duomenis iš SQLite duomenų bazės
def query_to_dataframe(db_path, query):
    import sqlite3
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Nuskaitome duomenis iš duomenų bazės
db_path = '../../../web_scrap.db'
query = 'SELECT * from aruodas;'
df = query_to_dataframe(db_path, query)

def sildymas(x):
    if x == None:
        return x
    else:
        if len(x.split(',')) == 1:
            return x.split(',')[0]
        else: 
            return 'Hibridinis'

def amzius(x):
    if x == None:
        return x
    else:
        if int(x)>=2024:
            return 0
        else:
            return 2024-int(x)

# Duomenų apdorojimas
aruodas_df = df
aruodas_df['Plotas_n'] = aruodas_df['Plotas'].apply(lambda x: x.replace(',','.').split()[0] if x!=None else x)
aruodas_df['Miestas_n'] = aruodas_df['Miestas'].apply(lambda x: x.split(',')[0])
aruodas_df['Mikrorajonas'] = aruodas_df['Adresas'].apply(lambda x: x.split(',')[1])
aruodas_df['Adresas_n'] = aruodas_df['Adresas'].apply(lambda x: ', '.join(x.split(',')[:-1])+' ')+aruodas_df['Namo numeris'].apply(lambda x: x if x!= None else ' ')
aruodas_df['X'] = aruodas_df['Coord'].apply(lambda x: float(x.replace('(','').replace(')','').split(',')[0]) if x!='None' else np.nan)
aruodas_df['Y'] = aruodas_df['Coord'].apply(lambda x: float(x.replace('(','').replace(')','').split(',')[1]) if x!='None' else np.nan)
aruodas_df['Kaina_n'] = aruodas_df['Kaina'].apply(lambda x: float(x) if x != None else x)
aruodas_df['Šildymo_tipas'] = aruodas_df['Šildymas'].apply(sildymas)
miestai = ['Kaunas', 'Vilnius', 'Klaipėda', 'Šiauliai', 'Palanga']
df_anal = aruodas_df[aruodas_df['Miestas_n'].isin(miestai)]
df_anal['Plotas_group'] = df_anal['Plotas_n'].apply(lambda x: np.ceil(float(x)/5)*5 if x != None else x)
df_anal['Metai_n'] = df_anal['Metai'].apply(lambda x: int(x[:4]) if x != None else x)
df_anal['Amžius'] = df_anal['Metai_n'].apply(amzius)
df_anal['Amžius_group'] = df_anal['Amžius'].apply(lambda x: np.ceil(float(x)/50)*50 if x != None else x)
df_anal['Aukštas'] = df_anal['Aukštas'].apply(lambda x: int(x) if x != None else x)
df_anal['Aukštų sk.'] = df_anal['Aukštų sk.'].apply(lambda x: int(x) if x != None else x)
klasės = ['A','A+','A++']
df_class = df_anal[df_anal['Pastato energijos suvartojimo klasė'].isin(klasės)]
df_miestas = df_anal[df_anal['Miestas_n'] == 'Kaunas']


# Pasirinkimas grafiko iš sąrašo
options = [
    'Koks NT plotas yra dažniausiai pasitaikantis lyginamuose miestuose?',
    'Koks vidutinis amžius/statybos metai NT objektų?',
    'Kaip priklauso vidutinė kaina nuo NT objektų energetinės klasės?',
    'Kaip priklauso vidutinė kaina nuo NT objektų energetinės klasės? (A, A+, A++)?',
    'Ar yra priklausomybė tarp vidutinės kainos ir įrengto šildymo (kolektorinis, centrinis, grindinis ...)?',
    'Kuriuose lyginamuose miestuose didžiausias/mažiausias kainų išsibarstymas?',
    'Ar yra kokia nors priklausomybė tarp kainos ir pastato tipo (Mūrinis, blokinis)?',
    'Ar yra kokia nors priklausomybė tarp kainos ir pastato amžiaus?',
    'Ar yra priklausomybė tarp pastato aukščio (aukštais) ir buto kainos?',
    'Ar yra priklausomybė tarp buto padėties pastate (kuriame aukšte jis yra) ir buto kainos?',
    'Kauno butų pardavimui ir nuomai kiekis pagal mikrorajoną',
    'Kauno butų pardavimui ir nuomai kaina pagal mikrorajoną',
    'Kauno butų pardavimui plotas pagal mikrorajoną',
    'Kauno butų pardavimui amžius pagal mikrorajoną',
    'Kauno butų pardavimui kainos išsibarstymas pagal mikrorajoną',
    'Kauno butų pardavimui kiekis pagal mikrorajoną ir pasikartojantį plotą',
    'MAP Pardavimai',
    'MAP Nuoma'
]

# Vartotojas gali pasirinkti grafiką
selected_option = st.selectbox('Pasirinkite grafiką:', options)

# Funkcija grafiko rodymui pagal pasirinkimą
def show_chart(selected_option):
    fig, axes = plt.subplots(1,2,figsize=(20, 15))

    if selected_option == 'Koks NT plotas yra dažniausiai pasitaikantis lyginamuose miestuose?':
        dfx = df_anal[df_anal['Tipas'] == 'Butai pardavimui'].groupby(['Plotas_group'])['Kaina'].count().reset_index().sort_values(by= 'Kaina', ascending=False)[:20]
        dfy = df_anal[df_anal['Tipas'] == 'Butai nuomai'].groupby(['Plotas_group'])['Kaina'].count().reset_index().sort_values(by= 'Kaina', ascending=False)[:20]
        axes[0].set_title(f'{miestai} miestų butai pardavimui pagal plotą')
        axes[1].set_title(f'{miestai} miestų butai nuomai pagal plotą')
        ax = sns.barplot(data=dfx,x = 'Plotas_group', y='Kaina', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Plotas_group', y='Kaina', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Plotas',ylabel='Kiekis')
        axes[1].set(xlabel='Plotas',ylabel='Kiekis')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)

    elif selected_option == 'Koks vidutinis amžius/statybos metai NT objektų?':
        dfx = list(df_anal[df_anal['Tipas'] == 'Butai pardavimui']['Amžius'])
        dfy = list(df_anal[df_anal['Tipas'] == 'Butai nuomai']['Amžius'])
        x_avg = []
        y_avg = []
        x_avg.append(sum(dfx)/len(dfx))
        y_avg.append(sum(dfy)/len(dfy))
        ndf = pd.DataFrame()
        ndf['Pav'] = pd.DataFrame(data=['Butai'])
        ndf['AVG'] = pd.DataFrame(data=x_avg)
        ndf['AVG_n'] = pd.DataFrame(data=y_avg)
        axes[0].set_title(f'{miestai} miestų butai pardavimui vidutinis amžius')
        axes[1].set_title(f'{miestai} miestų butai nuomai vidutinis amžius')
        ax = sns.barplot(data=ndf, x='Pav', y='AVG', ax=axes[0])
        ay = sns.barplot(data=ndf, x='Pav', y='AVG_n', ax=axes[1])
        axes[0].set(xlabel='Butai pardavimui',ylabel='Amžius')
        axes[1].set(xlabel='Butai nuomai',ylabel='Amžius')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)

    elif selected_option == 'Kaip priklauso vidutinė kaina nuo NT objektų energetinės klasės?':
        dfx = df_anal[df_anal['Tipas'] == 'Butai pardavimui'].groupby(['Pastato energijos suvartojimo klasė'])['Kaina_n'].mean().reset_index()
        dfy = df_anal[df_anal['Tipas'] == 'Butai nuomai'].groupby(['Pastato energijos suvartojimo klasė'])['Kaina_n'].mean().reset_index()
        axes[0].set_title(f'{miestai} miestų butų pardavimui kaina pagal klasę')
        axes[1].set_title(f'{miestai} miestų butų nuomai kaina pagal klasę')
        ax = sns.barplot(data=dfx,x = 'Pastato energijos suvartojimo klasė', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Pastato energijos suvartojimo klasė', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Klasė',ylabel='Kaina')
        axes[1].set(xlabel='Klasė',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)

    elif selected_option == 'Kaip priklauso vidutinė kaina nuo NT objektų energetinės klasės? (A, A+, A++)?':
        dfx = df_class[df_class['Tipas'] == 'Butai pardavimui'].groupby(['Pastato energijos suvartojimo klasė'])['Kaina_n'].mean().reset_index()
        dfy = df_class[df_class['Tipas'] == 'Butai nuomai'].groupby(['Pastato energijos suvartojimo klasė'])['Kaina_n'].mean().reset_index()
        axes[0].set_title(f'{miestai} miestų butų pardavimui kaina pagal klasę')
        axes[1].set_title(f'{miestai} miestų butų nuomai kaina pagal klasę')
        ax = sns.barplot(data=dfx,x = 'Pastato energijos suvartojimo klasė', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Pastato energijos suvartojimo klasė', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Klasė',ylabel='Kaina')
        axes[1].set(xlabel='Klasė',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)

    elif selected_option == 'Ar yra priklausomybė tarp vidutinės kainos ir įrengto šildymo (kolektorinis, centrinis, grindinis ...)?':
        dfx = df_anal[df_anal['Tipas'] == 'Butai pardavimui'].groupby(['Šildymo_tipas'])['Kaina_n'].mean().reset_index()
        dfy = df_anal[df_anal['Tipas'] == 'Butai nuomai'].groupby(['Šildymo_tipas'])['Kaina_n'].mean().reset_index()
        axes[0].set_title(f'{miestai} miestų butų pardavimui kaina pagal šildymo tipą')
        axes[1].set_title(f'{miestai} miestų butų nuomai kaina pagal šildymo tipą')
        ax = sns.barplot(data=dfx,x = 'Šildymo_tipas', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Šildymo_tipas', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Šildymo tipas',ylabel='Kaina')
        axes[1].set(xlabel='Šildymo tipas',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)

    elif selected_option == 'Kuriuose lyginamuose miestuose didžiausias/mažiausias kainų išsibarstymas?':
        dfx = df_anal[df_anal['Tipas'] == 'Butai pardavimui']
        dfy = df_anal[df_anal['Tipas'] == 'Butai nuomai']
        axes[0].set_title(f'{miestai} miestų butų pardavimui kainos išsibarstymas pagal miestą')
        axes[1].set_title(f'{miestai} miestų butų nuomai kainos išsibarstymas pagal miestą')
        ax = sns.boxplot(data=dfx,x = 'Miestas_n', y='Kaina_n', ax=axes[0], showmeans=True, showfliers=False)
        ay = sns.boxplot(data=dfy,x = 'Miestas_n', y='Kaina_n', ax=axes[1], showmeans=True, showfliers=False)
        axes[0].set(xlabel='Miestas',ylabel='Kaina')
        axes[1].set(xlabel='Miestas',ylabel='Kaina')

    elif selected_option == 'Ar yra kokia nors priklausomybė tarp kainos ir pastato tipo (Mūrinis, blokinis)?':
        dfx = df_anal[df_anal['Tipas'] == 'Butai pardavimui'].groupby(['Pastato tipas'])['Kaina_n'].mean().reset_index().sort_values(by='Kaina_n')
        dfy = df_anal[df_anal['Tipas'] == 'Butai nuomai'].groupby(['Pastato tipas'])['Kaina_n'].mean().reset_index().sort_values(by='Kaina_n')
        axes[0].set_title(f'{miestai} miestų butų pardavimui kaina pagal pastato tipą')
        axes[1].set_title(f'{miestai} miestų butų nuomai kaina pagal pastato tipą')
        ax = sns.barplot(data=dfx,x = 'Pastato tipas', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Pastato tipas', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Pastato tipas',ylabel='Kaina')
        axes[1].set(xlabel='Pastato tipas',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)

    elif selected_option == 'Ar yra kokia nors priklausomybė tarp kainos ir pastato amžiaus?':
        dfx = df_anal[df_anal['Tipas'] == 'Butai pardavimui'].groupby(['Amžius_group'])['Kaina_n'].mean().reset_index()
        dfy = df_anal[df_anal['Tipas'] == 'Butai nuomai'].groupby(['Amžius_group'])['Kaina_n'].mean().reset_index()
        axes[0].set_title(f'{miestai} miestų butų pardavimui kaina pagal pastato tipą')
        axes[1].set_title(f'{miestai} miestų butų nuomai kaina pagal pastato tipą')
        ax = sns.barplot(data=dfx,x = 'Amžius_group', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Amžius_group', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Amžius',ylabel='Kaina')
        axes[1].set(xlabel='Amžius',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)

    elif selected_option == 'Ar yra priklausomybė tarp pastato aukščio (aukštais) ir buto kainos?':
        dfx = df_anal[df_anal['Tipas'] == 'Butai pardavimui'].groupby(['Aukštų sk.'])['Kaina_n'].mean().reset_index()
        dfy = df_anal[df_anal['Tipas'] == 'Butai nuomai'].groupby(['Aukštų sk.'])['Kaina_n'].mean().reset_index()
        axes[0].set_title(f'{miestai} miestų butų pardavimui kaina pagal pastato aukštį')
        axes[1].set_title(f'{miestai} miestų butų nuomai kaina pagal pastato aukštį')
        ax = sns.barplot(data=dfx,x = 'Aukštų sk.', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Aukštų sk.', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Aukštų sk.',ylabel='Kaina')
        axes[1].set(xlabel='Aukštų sk.',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)
            
    elif selected_option == 'Ar yra priklausomybė tarp buto padėties pastate (kuriame aukšte jis yra) ir buto kainos?':
        dfx = df_anal[df_anal['Tipas'] == 'Butai pardavimui'].groupby(['Aukštas'])['Kaina_n'].mean().reset_index()
        dfy = df_anal[df_anal['Tipas'] == 'Butai nuomai'].groupby(['Aukštas'])['Kaina_n'].mean().reset_index()
        axes[0].set_title(f'{miestai} miestų butų pardavimui kaina pagal aukštą')
        axes[1].set_title(f'{miestai} miestų butų nuomai kaina pagal aukštą')
        ax = sns.barplot(data=dfx,x = 'Aukštas', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Aukštas', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Aukštas',ylabel='Kaina')
        axes[1].set(xlabel='Aukštas',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)
        
    elif selected_option == 'Kauno butų pardavimui ir nuomai kiekis pagal mikrorajoną':
        fig, axes = plt.subplots(2,1,figsize=(20,30))
        dfx = df_miestas[df_miestas['Tipas'] == 'Butai pardavimui'].groupby(['Mikrorajonas'])['Kaina_n'].count().reset_index().sort_values(by='Kaina_n')
        dfy = df_miestas[df_miestas['Tipas'] == 'Butai nuomai'].groupby(['Mikrorajonas'])['Kaina_n'].count().reset_index().sort_values(by='Kaina_n')
        axes[0].set_title(f'Kauno butų pardavimui kiekis pagal mikrorajoną')
        axes[1].set_title(f'Kauno butų nuomai kiekis pagal mikrorajoną')
        ax = sns.barplot(data=dfx,x = 'Mikrorajonas', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Mikrorajonas', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Mikrorajonas',ylabel='Kiekis')
        axes[1].set(xlabel='Mikrorajonas',ylabel='Kiekis')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)
        
    elif selected_option == 'Kauno butų pardavimui ir nuomai kaina pagal mikrorajoną':
        fig, axes = plt.subplots(2,1,figsize=(20,30))
        dfx = df_miestas[df_miestas['Tipas'] == 'Butai pardavimui'].groupby(['Mikrorajonas'])['Kaina_n'].mean().reset_index().sort_values(by='Kaina_n')
        dfy = df_miestas[df_miestas['Tipas'] == 'Butai nuomai'].groupby(['Mikrorajonas'])['Kaina_n'].mean().reset_index().sort_values(by='Kaina_n')
        axes[0].set_title(f'Kauno butų pardavimui kaina pagal mikrorajoną')
        axes[1].set_title(f'Kauno butų nuomai kaina pagal mikrorajoną')
        ax = sns.barplot(data=dfx,x = 'Mikrorajonas', y='Kaina_n', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Mikrorajonas', y='Kaina_n', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Mikrorajonas',ylabel='Kaina')
        axes[1].set(xlabel='Mikrorajonas',ylabel='Kaina')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)
        
    elif selected_option == 'Kauno butų pardavimui plotas pagal mikrorajoną':
        dfx = df_miestas[df_miestas['Tipas'] == 'Butai pardavimui'].groupby(['Mikrorajonas'])['Plotas_group'].mean().reset_index().sort_values(by='Plotas_group')
        dfy = df_miestas[df_miestas['Tipas'] == 'Butai nuomai'].groupby(['Mikrorajonas'])['Plotas_group'].mean().reset_index().sort_values(by='Plotas_group')
        axes[0].set_title(f'Kauno butų pardavimui plotas pagal mikrorajoną')
        axes[1].set_title(f'Kauno butų nuomai plotas pagal mikrorajoną')
        ax = sns.barplot(data=dfx,x = 'Mikrorajonas', y='Plotas_group', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Mikrorajonas', y='Plotas_group', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Mikrorajonas',ylabel='Plotas')
        axes[1].set(xlabel='Mikrorajonas',ylabel='Plotas')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)
        
    elif selected_option == 'Kauno butų pardavimui amžius pagal mikrorajoną':
        dfx = df_miestas[df_miestas['Tipas'] == 'Butai pardavimui'].groupby(['Mikrorajonas'])['Amžius'].mean().reset_index().sort_values(by='Amžius')
        dfy = df_miestas[df_miestas['Tipas'] == 'Butai nuomai'].groupby(['Mikrorajonas'])['Amžius'].mean().reset_index().sort_values(by='Amžius')
        axes[0].set_title(f'Kauno butų pardavimui amžius pagal mikrorajoną')
        axes[1].set_title(f'Kauno butų nuomai amžius pagal mikrorajoną')
        ax = sns.barplot(data=dfx,x = 'Mikrorajonas', y='Amžius', ax=axes[0])
        ay = sns.barplot(data=dfy,x = 'Mikrorajonas', y='Amžius', ax=axes[1])
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Mikrorajonas',ylabel='Amžius')
        axes[1].set(xlabel='Mikrorajonas',ylabel='Amžius')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)
        
    elif selected_option == 'Kauno butų pardavimui kainos išsibarstymas pagal mikrorajoną':
        dfx = df_miestas[df_miestas['Tipas'] == 'Butai pardavimui']
        dfy = df_miestas[df_miestas['Tipas'] == 'Butai nuomai']
        axes[0].set_title(f'Kauno butų pardavimui kainos išsibarstymas pagal mikrorajoną')
        axes[1].set_title(f'Kauno butų nuomai kainos išsibarstymas pagal mikrorajoną')
        ax = sns.boxplot(data=dfx,x = 'Mikrorajonas', y='Kaina_n', ax=axes[0], showmeans=True, showfliers=False)
        ay = sns.boxplot(data=dfy,x = 'Mikrorajonas', y='Kaina_n', ax=axes[1], showmeans=True, showfliers=False)
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Mikrorajonas',ylabel='Kaina')
        axes[1].set(xlabel='Mikrorajonas',ylabel='Kaina')
        
    elif selected_option == 'Kauno butų pardavimui kiekis pagal mikrorajoną ir pasikartojantį plotą':
        dfx = df_miestas[df_miestas['Tipas'] == 'Butai pardavimui'].groupby(['Mikrorajonas', 'Plotas_group'])['Kaina_n'].count().reset_index().sort_values(by='Kaina_n')
        dfy = df_miestas[df_miestas['Tipas'] == 'Butai nuomai'].groupby(['Mikrorajonas', 'Plotas_group'])['Kaina_n'].count().reset_index().sort_values(by='Kaina_n')
        axes[0].set_title(f'Kauno butų pardavimui kiekis pagal mikrorajoną ir pasikartojantį plotą')
        axes[1].set_title(f'Kauno butų nuomai kiekis pagal mikrorajoną ir pasikartojantį plotą')
        ax = sns.barplot(data=dfx,x = 'Mikrorajonas', y='Kaina_n', ax=axes[0], hue='Plotas_group')
        ay = sns.barplot(data=dfy,x = 'Mikrorajonas', y='Kaina_n', ax=axes[1], hue='Plotas_group')
        axes[0].set_xticklabels(axes[0].get_xticklabels(), rotation=90)
        axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=90)
        axes[0].set(xlabel='Mikrorajonas',ylabel='Kiekis')
        axes[1].set(xlabel='Mikrorajonas',ylabel='Kiekis')
        for container in ax.containers:
            ax.bar_label(container)
        for container in ay.containers:
            ay.bar_label(container)
    
    elif selected_option == 'MAP Pardavimai':
        dfx = df_miestas[df_miestas['Tipas'] == 'Butai pardavimui']
        dfy = df_miestas[df_miestas['Tipas'] == 'Butai nuomai']
        fig = px.scatter_mapbox(data_frame=dfx, lon='Y', lat='X', zoom=10)
        fig.update_layout(mapbox_style='open-street-map')
        fig.update_layout(width=800, height=600)
        fig.show()
        
    elif selected_option == 'MAP Nuoma':
        dfx = df_miestas[df_miestas['Tipas'] == 'Butai pardavimui']
        dfy = df_miestas[df_miestas['Tipas'] == 'Butai nuomai']
        fig = px.scatter_mapbox(data_frame=dfy, lon='Y', lat='X', zoom=10)
        fig.update_layout(mapbox_style='open-street-map')
        fig.update_layout(width=800, height=600)
        fig.show()

    st.pyplot(fig)

# Parodyti grafiką pagal vartotojo pasirinkimą
show_chart(selected_option)
