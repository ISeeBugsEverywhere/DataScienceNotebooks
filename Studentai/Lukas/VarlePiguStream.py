import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
# import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
import sqlite3
import re

#streamlit page config: :streamlit
st.set_page_config(page_icon=':bar_chart', page_title='DEMO STREAMLIT MAP', layout='centered')


options = [
    'Šaldytuvai',
    'Dronai',
    'Planšetiniai kompiuteriai',
    'Televizoriai',
    'Dviračiai'
]

selected_option = st.selectbox('Pasirinkite prekių kategoriją:', options)

if selected_option == 'Šaldytuvai':
    # Saldytuvai
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()
    
    sql="""SELECT kaina, `montavimo tipas`
    FROM "SaldytuvaiVarle";
    """
    df = pd.read_sql_query(sql, con=SDB)

    SDB.close()

    df.dropna(subset='montavimo tipas', inplace=True)
    def set_saldytuvo_tipas(x):
        if 'stat' in x:
            return 'Laivai pastatomi'
        elif 'montuo' in x:
            return 'Įmontuojami'
        elif 'ntegruo' in x:
            return 'Integruojami'
        else:
            return 'Kita'
        
    df['mtipas'] =df['montavimo tipas'].apply(set_saldytuvo_tipas)
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    c =df['mtipas'].value_counts()
    fig, (axis1, axis2) = plt.subplots(1,2, figsize=(10.5, 4.5))
    axis1.pie(c.values, labels=c.index, autopct='%.2f%%')
    sns.boxplot(data=df, x='mtipas', y='kaina', showmeans=True, showfliers=False, ax=axis2)
    axis1.set_title('Šaldytuvų pasiskirstymas pagal montavimo tipą (Varle.lt)')
    axis2.set_title('Kainų pasiskirstymas pagal šaldytuvų  montavimo tipą (Varle.lt)')
    axis2.set_xlabel('Tipas')
    axis2.set_ylabel('Kaina')
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)


    # Saldytuvai Pigu montavimo tipas
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina,
    `Montavimo tipas:`
    FROM "SaldytuvaiPigu";
    """
    df = pd.read_sql_query(sql, con=SDB)
    SDB.close()
    c = df['Montavimo tipas:'].value_counts()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5))
    ax1.pie(c.values, labels=c.index, autopct='%.2f%%', startangle=90)
    sns.boxplot(data=df, x='Montavimo tipas:', y='kaina', ax=ax2, showmeans=True, showfliers=False)
    ax1.set_title('Šaldytuvai pagal montavimo tipą (Pigu.lt)')
    ax2.set_title('Šaldytuvų kainos pasiskirtymas pagal montavimo tipą (Pigu.lt)')
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)


    # Saldytuvai Varle tipas
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina, tipas
    FROM "SaldytuvaiVarle";
    """
    df = pd.read_sql_query(sql, con=SDB)
    SDB.close()
    df.dropna(subset='tipas', inplace=True)

    def set_saldytuvo_tipas(x):
        if 'apa' in x:
            return 'Šaldytuvas su šaldikliu apačioje'
        elif 'virš' in x or 'with top' in x:
            return 'Šaldytuvas su šaldikliu viršuje'
        elif 'Mini' in x:
            return 'Mini'
        elif 'without' in x or 'Be k' in x:
            return 'Šaldytuvas be šaldiklio'
        elif 'kamera' in x or 'inside' in x:
            return 'Šaldytuvas su šaldikliu viduje'
        elif 'Dvid'in x or 'Double' in x:
            return 'Dviduriai šaldytuvai'
        elif 'stat' in x:
            return 'Laisvai pastatomas'
        else:
            return x
        
    df['stipas'] =df['tipas'].apply(set_saldytuvo_tipas)
    top = df['stipas'].value_counts().head(10).index.tolist()
    df['stipas'] = df['stipas'].apply(lambda x: x if x in top else 'Kita')
    c = df['stipas'].value_counts()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.pie(c.values, labels=c.index, autopct='%.1f%%')
    plt.title('Šaldytuvų pasiskirstymas pagal tipą (Varle.lt)')
    st.pyplot(fig, use_container_width=True)


    # Saldytuvai Pigu tipas
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina,
    `Šaldytuvo tipas:`
    FROM "SaldytuvaiPigu";
    """
    df = pd.read_sql_query(sql, con=SDB)
    SDB.close()
    c = df['Šaldytuvo tipas:'].value_counts()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.pie(c.values, labels=c.index, autopct='%.2f%%', startangle=33, pctdistance=0.7, labeldistance = 0.9, textprops={'fontsize':8, 'color': 'black'})
    sns.boxplot(data=df, x='Šaldytuvo tipas:', y='kaina', ax=ax2, showmeans=True, showfliers=False)
    ax1.set_title('Šaldytuvai pagal  tipą (Pigu.lt)')
    ax2.set_title('Šaldytuvų kainos pasiskirtymas pagal tipą (Pigu.lt)')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)


    # saldytuvai talpa
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql1="""SELECT kaina, `talpa (l)`, `naudinga šaldytuvo talpa`, `šaldytuvo talpa [l]`,
    `bendra talpa neto`, `šaldytuvo talpa neto`, `šaldytuvo talpa`, `bendros grynosios talpos`, `bendra talpa`, `šaldymo talpa`,
    `šaldytuvo neto talpa`, `bendra neto talpa`, `bendroji talpa neto`, `šaldytuvo talpa (neto)`,
    `talpa (neto)`, `šaldytuvo talpa (l)`, `grynoji talpa`, `bendroji talpa neto (l)`, `šaldytuvo talpa neto (l)`
    FROM "SaldytuvaiVarle";
    """
    df = pd.read_sql_query(sql1, con=SDB)

    sql2="""SELECT kaina,
    `Bendra talpa:`
    FROM "SaldytuvaiPigu";
    """
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    for col in df.columns:
        if col != 'kaina':
            df['V'] = df['talpa (l)'].fillna(df[col])
        
    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    df.dropna(subset='V', inplace=True)
    dfv = df[['kaina', 'V']]
    dfv['V'] = df['V'].apply(lambda x: float(x))
    dfv['Vgr'] = dfv['V'].apply(lambda x: int(np.ceil(x/10) * 10))

    dfv_gr = dfv[dfv['V'] < 700].groupby('Vgr').mean(numeric_only=True).round().reset_index()
    dfv_gr.head()

    # pigu
    def set_talpa(x):
        if x is not None:
            return float(x.replace('l', ''))
        
    dfp['talpa'] = dfp['Bendra talpa:'].apply(set_talpa)
    dfp.dropna(subset='talpa', inplace=True)
    dfp['talpa2'] = dfp['talpa'].apply(lambda x: int(np.ceil(x/10) * 10))
    dfpv = dfp[['kaina', 'talpa2']]

    dfpv_gr = dfpv.groupby('talpa2').mean(numeric_only=True).round().reset_index()
    dfpv_gr.head()

    fig, axis = plt.subplots()
    sns.regplot(data=dfv_gr[dfv_gr['Vgr'] > 10], x='Vgr', y='kaina', order=2, ax=axis, label='Varle.lt')
    sns.regplot(data=dfpv_gr, x='talpa2', y='kaina', order=2, ax=axis, label='Pigu.lt')
    plt.title('Šaldytuvo kainos priklausomybė nuo talpos')
    plt.ylabel('Kaina')
    plt.xlabel('Šaldytuvo talpa (l)')
    plt.legend()
    st.pyplot(fig, use_container_width=True)
    
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina, 
    `energijos klasė`, 
    `energijos vartojimo efektyvumo klasė (reglamentas (es) 2017/1369)`,
    `energijos efektyvumo klasė`
    FROM "SaldytuvaiVarle";
    """
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""SELECT kaina,
    `Energijos klasė:`
    FROM "SaldytuvaiPigu";
    """
    dfp = pd.read_sql_query(sql2, con=SDB)
    SDB.close()


    for col in df.columns:
        if col != 'kaina':
            df['energijos klasė'] = df['energijos klasė'].fillna(df[col])
    

        
    df['energijos klasė'] = df['energijos klasė'].apply(lambda x: x.upper() if x is not None else x)
    df['eklase'] = df['energijos klasė']
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    df.dropna(subset='eklase', inplace=True)

    # klases_v = sorted(list(set(df['energijos klasė'].tolist())))
    dfe = df[['kaina', 'eklase']]
    dfe['saltinis'] = 'Varle.lt'


    # pigu
    dfp['eklase'] = dfp['Energijos klasė:']
    dfp.dropna(subset='eklase', inplace=True)
    # klases = sorted(list(set(dfp['Energijos klasė:'].tolist())))
    dfpe = dfp[['kaina', 'eklase']]
    dfpe['saltinis'] = 'Pigu.lt'

    # sujungiam dataframus
    df_combined = pd.concat([dfe, dfpe])
    klases = sorted(list(set(df_combined['eklase'].tolist())))

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined, x='eklase', y='kaina',hue='saltinis', showmeans=True, showfliers=False, order=klases)

    plt.title('Šaldytuvų kainos pasiskirstymas pagal energijos klasę')
    st.pyplot(fig, use_container_width=True)
    
    # Energijos sanaudos

    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina, 
    `vidutinės metinės energijos sąnaudos kilovatvalandėmis per metus (kwh/m.)`,
    `metinės energijos sąnaudos`,
    `metinis energijos suvartojimas (kwh)`,
    `energijos suvartojimas per metus`,
    `energijos sąnaudos`,
    `metinis energijos suvartojimas`,
    `suvartojama energija`,
    `bendras suvartojamos energijos kiekis per metus`,
    `energijos sąnaudos (kwh/metus)`,
    `suvartojama energija (kwh)`,
    `bendras suvartojamos energijos kiekis per metus (kwh)`,
    `energijos sąnaudos per metus`
    FROM "SaldytuvaiVarle";
    """
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""SELECT kaina,
    `Energijos sąnaudos per metus:`
    FROM "SaldytuvaiPigu";
    """
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    for col in df.columns:
        if col != 'kaina':
            df['energija'] = df['metinės energijos sąnaudos'].fillna(df[col])

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    dfe = df[['kaina', 'energija']]
    dfe.dropna(subset='energija', inplace=True)
    dfe['energija'] = dfe['energija'].apply(lambda x: x.replace('kWh/metus', '').replace('kWh', '').replace(',', '.'))
    dfe['energija'] = dfe['energija'].apply(lambda x: float(x))
    dfe['E'] = dfe['energija'].apply(lambda x: int(np.ceil(x/5) * 5))
    dfe_gr = dfe.groupby('E').mean(numeric_only=True).round().reset_index()

    # Pigu
    dfp['sanaudos'] = dfp['Energijos sąnaudos per metus:'].str.extract('(\d+)')
    dfp.dropna(subset='sanaudos', inplace=True)
    dfp['sanaudos'] = dfp['sanaudos'].apply(lambda x: int(x))
    dfpe = dfp[['kaina', 'sanaudos']]

    dfpe['E'] = dfpe['sanaudos'].apply(lambda x: int(np.ceil(x/5) * 5))

    dfpe_gr = dfpe.groupby('E').mean(numeric_only=True).round().reset_index()
    dfpe_filtered = dfpe_gr[(dfpe_gr['E'] > 0) & (dfpe_gr['E'] < 500)]

    fig, axis = plt.subplots()
    sns.regplot(data=dfe_gr[dfe_gr['E'] < 500], x='E', y='kaina', order=3, ax=axis, label='Varle.lt')
    sns.regplot(data=dfpe_filtered, x='E', y='kaina', order=3, ax=axis, label='Pigu.lt')
    plt.title('Šaldytuvo kainos priklausomybė nuo energijos suvartojimo')
    plt.ylabel('Kaina')
    plt.xlabel('Energijos suvartojimas kWh/metus')
    plt.legend()
    st.pyplot(fig, use_container_width=True)
    
    # garsas/triuksmas
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina, 
    `ore skleidžiamas akustinis triukšmas`,
    `triukšmo lygis [db]`,
    `maksimalus triukšmo lygis`,
    `triukšmo lygis (db)`,
    `triukšmo lygis`,
    `triukšmo galia`,
    `triukšmo lygis, db`,
    `triukšmingumo lygis`,
    `triukšmo lygis (db (a) re 1 pw)`,
    `garso lygis`
    FROM "SaldytuvaiVarle";
    """
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""SELECT kaina,
    `Maksimalus triukšmo lygis:`
    FROM "SaldytuvaiPigu";
    """
    dfp = pd.read_sql_query(sql2, con=SDB)
    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    for col in df.columns:
        if col != 'kaina':
            df['garsas'] = df['ore skleidžiamas akustinis triukšmas'].fillna(df[col])

    df.dropna(subset='garsas', inplace=True)
    df['garsas'] = df['garsas'].apply(lambda x: int(x[:2]))

    dfg = df[['kaina', 'garsas']]
    dfg['g2'] = dfg['garsas'].apply(lambda x: int(np.ceil(x/2) * 2))

    dfg_gr = dfg.groupby('g2').mean(numeric_only=True).round().reset_index()
    # dfg_gr['saltinis'] = 'Varle.lt'
    # dfg_gr_1 = dfg_gr[['kaina', 'g2', 'saltinis']]


    # Pigu
    dfp['garsas'] = dfp['Maksimalus triukšmo lygis:'].str.extract('(\d+)')
    dfp.dropna(subset='garsas', inplace=True)
    dfp['garsas'] = dfp['garsas'].apply(lambda x: int(x))

    dfpg = dfp[['kaina', 'garsas']]
    dfpg['g2'] = dfpg['garsas'].apply(lambda x: int(np.ceil(x/2) * 2))

    dfpg_gr = dfpg.groupby('g2').mean(numeric_only=True).round().reset_index()
    # dfpg_gr['saltinis'] = 'Pigu.lt'

    fig, axis = plt.subplots()
    sns.regplot(data=dfg_gr, x='g2', y='kaina', order=1, ax=axis, label='Varle.lt')
    sns.regplot(data=dfpg_gr, x='g2', y='kaina', order=1, ax=axis, label='Pigu.lt')
    axis.set_xlabel('Triukšmo lygis (db)')
    axis.set_ylabel('Kaina')
    plt.title('Šaldytuvų kainų priklausomybė nuo triukšmo lygio')
    plt.legend()
    st.pyplot(fig, use_container_width=True)
    
    # Gamintojai #######################
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina, 
    gamintojas,
    spalva,
    `gaminio spalva`,
    `produkto spalva`,
    `korpuso spalva`
    FROM "SaldytuvaiVarle";
    """
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""SELECT kaina, 
    `Prekės ženklas:`,
    `Spalva:`
    FROM "SaldytuvaiPigu";
    """
    dfp = pd.read_sql_query(sql2, con=SDB)
    SDB.close()
    # duomenys Varle
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    top_v = df['gamintojas'].value_counts().head(10).index.tolist()
    df_gamintojas = df[df['gamintojas'].isin(top_v)][['kaina', 'gamintojas']]
    df_gamintojas['saltinis'] = 'Varle.lt'
    # duomenys Pigu
    dfp['gamintojas'] = dfp['Prekės ženklas:']
    top_p = dfp['gamintojas'].value_counts().head(10).index.tolist()
    dfp_gamintojas = dfp[dfp['gamintojas'].isin(top_p)][['kaina', 'gamintojas']]
    dfp_gamintojas['saltinis'] = 'Pigu.lt'

    # sujungiame df
    df_combined = pd.concat([df_gamintojas, dfp_gamintojas])

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined, y='kaina', x='gamintojas', hue='saltinis', showfliers=False, showmeans=True)
    plt.title('Šaldytuvų kainos pasiskirtymas pagal gamintoją')
    plt.tick_params(axis='x', rotation=90)
    plt.xlabel('')
    plt.ylabel('Kaina')
    st.pyplot(fig, use_container_width=True)
    
    # Gamintojai Varle
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina, 
    gamintojas,
    spalva,
    `gaminio spalva`,
    `produkto spalva`,
    `korpuso spalva`
    FROM "SaldytuvaiVarle";
    """
    df = pd.read_sql_query(sql, con=SDB)
    SDB.close()
    for col in df.columns:
        if col not in ['kaina', 'gamintojas']:
            df['spalva'] = df['spalva'].fillna(df[col])

    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    def set_spalva(x):
        if x is not None:
            if 'Balt' in x or 'balt' in x:
                return 'Balta'
            elif 'Pilk' in x or 'pilk' in x:
                return 'Pilka'
            elif 'Juod' in x or 'juod' in x:
                return 'Juoda'
            else:
                return x

    df['spalva'] = df['spalva'].apply(set_spalva)
    colors_counts = df['spalva'].value_counts()
    colors_to_plot = colors_counts[colors_counts > 40].index
    brand_counts = df['gamintojas'].value_counts()
    brands_to_plot = brand_counts[brand_counts > 40].index

    df_gamintojas = df[(df['gamintojas'].isin(brands_to_plot)) & df['spalva'].isin(colors_to_plot)][['kaina', 'gamintojas', 'spalva']]
    df_gamintojas_gr = df_gamintojas.groupby(['gamintojas', 'spalva']).mean().round()
    fig, ax = plt.subplots()
    sns.barplot(data=df_gamintojas_gr, x='kaina', y='gamintojas', orient='h', hue='spalva')
    # sns.boxplot(data=df_gamintojas, x='kaina', y='gamintojas', hue='spalva', showmeans=True, showfliers=False)
    plt.title('Vidutinė šaldytuvų kaina pagal gamintoją (Varle.lt)')
    plt.ylabel('')
    plt.xlabel('Kaina')
    st.pyplot(fig, use_container_width=True)
    
    # Gamintojai Pigu
    SDB = sqlite3.connect('VarlePigu.db')
    Cs = SDB.cursor()

    sql="""SELECT kaina, 
    `Prekės ženklas:`,
    `Spalva:`
    FROM "SaldytuvaiPigu";
    """
    df = pd.read_sql_query(sql, con=SDB)
    SDB.close()
    def set_spalva(x):
        if x is not None:
            if 'Juod' in x:
                return 'Juoda'
            elif 'Balt' in x:
                return 'Balta'
            else:
                return x
            
    df['spalva'] = df['Spalva:'].apply(set_spalva)
    colors_counts = df['spalva'].value_counts()
    colors_to_plot = colors_counts[colors_counts > 20].index
    brand_counts = df['Prekės ženklas:'].value_counts()
    brands_to_plot = brand_counts[brand_counts > 40].index

    df_gamintojas = df[(df['Prekės ženklas:'].isin(brands_to_plot)) & df['spalva'].isin(colors_to_plot)][['kaina', 'Prekės ženklas:', 'spalva']]
    df_gamintojas_gr = df_gamintojas.groupby(['Prekės ženklas:', 'spalva']).mean().round()
    fig, ax = plt.subplots()
    sns.barplot(data=df_gamintojas_gr, x='kaina', y='Prekės ženklas:', orient='h', hue='spalva')
    # sns.boxplot(data=df_gamintojas, x='kaina', y='gamintojas', hue='spalva', showmeans=True, showfliers=False)
    plt.title('Vidutinė šaldytuvų kaina pagal gamintoją (Pigu.lt)')
    plt.ylabel('')
    plt.xlabel('Kaina')
    st.pyplot(fig, use_container_width=True)
        
if selected_option == 'Dronai':
    # Varle gamintojai
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina, Gamintojas from DronaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    top = df['Gamintojas'].value_counts().head(9).index.tolist()

    df['brand'] = df['Gamintojas'].apply(lambda x: x if x in top else 'Kita')
    c = df['brand'].value_counts()
    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
    # ax.pie(c.values, labels=c.index, autopct='%.f%%')
    ax1.pie(c.values, 
            labels=c.index, 
            autopct='%.f%%',
            textprops={'fontsize':8, 'color': 'black'},
            startangle=45,
            # move the percentage inside the arcs
            pctdistance=0.75,
            # add spaces between the arcs
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
            )
    ax1.set_title('Dronų gamintojai (Varle.lt)')
    sns.boxplot(data=df, x='brand', y='kaina', ax=ax2, showmeans=True, showfliers=False)
    ax2.tick_params(axis='x', rotation=90)
    ax2.set_title('Dronų kainos pasiskirtysmas pagal gamintoją (Varle.lt)')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    st.header('')
    
    def set_kaina(x):
        return float(x)
    df['kaina'] = df['kaina'].apply(set_kaina)

    df_gr = df.groupby('brand').mean(numeric_only=True).round()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(data=df_gr, x='brand', y='kaina')
    ax.tick_params(axis='x', rotation=90)
    for container in ax.containers:
        ax.bar_label(container)
    st.pyplot(fig, use_container_width=True)
    
    st.header('')
    
    # Pigu gamintojai
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina, 
    `Prekės ženklas:`,
    `Tipas:`
    from DronaiPigu;"""
    df_ivairus = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    df_ivairus.head() 
    df = df_ivairus[(df_ivairus['Tipas:'] == 'Dronas') | (df_ivairus['Tipas:'] == 'Komplektas')]

    top = df['Prekės ženklas:'].value_counts().head(10).index.tolist()

    fig, axis = plt.subplots()
    sns.boxplot(data=df[df['Prekės ženklas:'].isin(top)], y='Prekės ženklas:', x='kaina', showmeans=True, showfliers=False)
    axis.set_title('Dronų kainos pagal gamintoją (Pigu.lt)')
    st.pyplot(fig, use_container_width=True)
    df['gamintojas'] = df['Prekės ženklas:'].apply(lambda x: x if x  in top else 'Kita')
    c = df['gamintojas'].value_counts()

    fig, axis = plt.subplots()
    axis.pie(c.values, 
            labels=c.index, 
            autopct='%.f%%',
            textprops={'fontsize':8, 'color': 'black'},
            startangle=45,
            # move the percentage inside the arcs
            pctdistance=0.75,
            # add spaces between the arcs
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
            )
    axis.set_title('Dronai (Pigu.lt)')
    st.pyplot(fig, use_container_width=True)
    
    # skrydzio trukme Varle
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina, 
    `Veikimo laikas (min)`,
    `Didžiausias skrydžio laikas`
    from DronaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    df['Didžiausias skrydžio laikas'] = df['Didžiausias skrydžio laikas'].fillna(df['Veikimo laikas (min)'])
    df.dropna(subset=('Didžiausias skrydžio laikas'), inplace=True)
    df['laikas'] = df['Didžiausias skrydžio laikas'].str.extract('(\d+)')
    df['laikas'] = df['laikas'].apply(lambda x: float(x))

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    df_laikas = df[['kaina', 'laikas']]
    df_laikas_gr = df_laikas.groupby('laikas').mean(numeric_only=True).round().reset_index()
    fig, axis = plt.subplots()
    sns.scatterplot(data=df_laikas_gr, x='laikas', y='kaina')
    plt.title('Dronų kaina nuo skrydimo laiko (Varle.lt)')
    st.pyplot(fig, use_container_width=True)
    
    
    # skrydzio laikas/atstumas
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina, 
    `Veikimo atstumas:`,
    `Skraidymo laikas:`,
    `Tipas:`
    from DronaiPigu;"""
    df_ivairus = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    df = df_ivairus[(df_ivairus['Tipas:'] == 'Dronas') | (df_ivairus['Tipas:'] == 'Komplektas')]
    df['laikas'] = df['Skraidymo laikas:'].str.extract('(\d+)')
    df['veikimoAtstumas'] = df['Veikimo atstumas:'].str.extract('(\d+)')
    df.dropna(subset=['laikas', 'veikimoAtstumas'], inplace=True)
    df['laikas'] = df['laikas'].apply(lambda x: float(x))
    df['veikimoAtstumas'] = df['veikimoAtstumas'].apply(lambda x: float(x))
    pairplot = sns.pairplot(data=df)
    st.pyplot(pairplot)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    sns.regplot(data=df[df['kaina'] < 15000], x='laikas', y='kaina', order=1, ax=ax1)
    sns.regplot(data=df[df['kaina'] < 15000], x='veikimoAtstumas', y='kaina', order=1, ax=ax2)
    ax1.set_title('Kainos priklausomybė nuo veikimo laiko (Pigu.lt)')
    ax2.set_title('Kainos priklausomybė nuo veikimo atstumo (Pigu.lt)')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    
    # GPS, kamera, stabilizacija
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina, 
    `GPS:`,
    `Skrydžio stabilizacija:`,
    `Kamera:`,
    `Tipas:`
    from DronaiPigu;"""
    df_ivairus = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    df = df_ivairus[(df_ivairus['Tipas:'] == 'Dronas') | (df_ivairus['Tipas:'] == 'Komplektas')]
    df_stab = df[['kaina', 'Skrydžio stabilizacija:']]
    df_stab_gr = df.groupby('Skrydžio stabilizacija:').mean(numeric_only=True).round().reset_index()

    df_kam = df[['kaina', 'Kamera:']]
    df_kam_gr = df.groupby('Kamera:').mean(numeric_only=True).round().reset_index()

    df_gps = df[['kaina', 'Kamera:']]
    df_gps_gr = df.groupby('GPS:').mean(numeric_only=True).round().reset_index()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4.5))
    sns.barplot(data=df_stab_gr, x='Skrydžio stabilizacija:', y='kaina', ax=ax1)
    sns.barplot(data=df_kam_gr, x='Kamera:', y='kaina', ax=ax2)
    sns.barplot(data=df_gps_gr, x='GPS:', y='kaina', ax=ax3)
    for container in ax1.containers:
        ax1.bar_label(container)
    for container in ax2.containers:
        ax2.bar_label(container)
    for container in ax3.containers:
        ax3.bar_label(container)
    plt.tight_layout()
    ax1.set_title('Vidutinė drono kaina (Pigu.lt)')
    ax2.set_title('Vidutinė drono kaina (Pigu.lt)')
    ax3.set_title('Vidutinė drono kaina (Pigu.lt)')
    st.pyplot(fig, use_container_width=True)
    
    # Varle lentele
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    Gamintojas,
    `Veikimo laikas (min)`,
    `Didžiausias skrydžio laikas`,
    `Svoris (kg)`,
    `Baterijos talpa (mAh)`,
    Talpa,
    Stabilizavimas,
    Tipas
    from DronaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    # df.head()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    df['Didžiausias skrydžio laikas'] = df['Didžiausias skrydžio laikas'].fillna(df['Veikimo laikas (min)'])
    df['Talpa'] = df['Talpa'].fillna(df['Baterijos talpa (mAh)'])
    # # df.dropna(subset=('Didžiausias skrydžio laikas'), inplace=True)
    df['laikas'] = df['Didžiausias skrydžio laikas'].str.extract('(\d+)')
    df['laikas'] = df['laikas'].apply(lambda x: float(x))
    df['Baterija'] = df['Talpa'].str.extract('(\d+)')
    df['Baterija'] = df['Baterija'].apply(lambda x: float(x))

    price_bins = [0, 100, 200, 400, 600,30000]
    price_labels = ['iki 100', '101-200', '201-400', '401-600', ' nuo 600']
    df_data = df[['kaina', 'Gamintojas', 'laikas', 'Baterija', 'Stabilizavimas', 'Tipas']]

    df_data['price_range'] = pd.cut(df_data['kaina'], bins=price_bins, labels=price_labels, right=True)

    grouped = df_data.groupby('price_range')
    def safe_mode(x):
        mode = x.mode()
        return mode.iloc[0] if not mode.empty else None

    # # find most comman
    most_common_drone = grouped.agg({
        # 'kaina': safe_mode,
        'Gamintojas': safe_mode,
        'laikas': safe_mode,
        'Baterija': safe_mode,
        'Stabilizavimas': safe_mode,
        'Tipas': safe_mode
    }).reset_index()
    st.write('Labiausiai tikėtinas dronas Varle.lt')
    st.write(most_common_drone)
    
    # lentele pigu
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina, 
    `Prekės ženklas:`,
    `Veikimo atstumas:`,
    `Skraidymo laikas:`,
    `GPS:`,
    `Skrydžio stabilizacija:`,
    `Kamera:`,
    `Tipas:`
    from DronaiPigu;"""
    df_ivairus = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    df = df_ivairus[(df_ivairus['Tipas:'] == 'Dronas') | (df_ivairus['Tipas:'] == 'Komplektas')]

    df['laikas'] = df['Skraidymo laikas:'].str.extract('(\d+)')
    df['veikimoAtstumas'] = df['Veikimo atstumas:'].str.extract('(\d+)')
    # df.dropna(subset=['laikas', 'veikimoAtstumas'], inplace=True)
    df['laikas'] = df['laikas'].apply(lambda x: float(x))
    df['veikimoAtstumas'] = df['veikimoAtstumas'].apply(lambda x: float(x))

    price_bins = [0, 100, 200, 400, 600,30000]
    price_labels = ['iki 100', '101-200', '201-400', '401-600', ' nuo 600']
    df_data = df[['kaina', 'Prekės ženklas:', 'GPS:', 'Skrydžio stabilizacija:', 'Kamera:', 'laikas', 'veikimoAtstumas']]

    df_data['price_range'] = pd.cut(df_data['kaina'], bins=price_bins, labels=price_labels, right=True)

    grouped = df_data.groupby('price_range')
    def safe_mode(x):
        mode = x.mode()
        return mode.iloc[0] if not mode.empty else None

    # # find most comman
    most_common_drone = grouped.agg({
        # 'kaina': safe_mode,
        'Prekės ženklas:': safe_mode,
        'GPS:': safe_mode,
        'Skrydžio stabilizacija:': safe_mode,
        'Kamera:': safe_mode,
        'laikas': safe_mode,
        'veikimoAtstumas': safe_mode
    }).reset_index()
    st.write('Labiausiai tikėtinas dronas Pigu.lt')
    st.write(most_common_drone)
    
    
if selected_option == 'Planšetiniai kompiuteriai':
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas
    from PlanseteVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    top = df['gamintojas'].value_counts().head(9).index.tolist()

    df['brand'] = df['gamintojas'].apply(lambda x: x if x in top else 'Kita')
    c = df['brand'].value_counts()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
    # ax.pie(c.values, labels=c.index, autopct='%.f%%')
    ax1.pie(c.values, 
            labels=c.index, 
            autopct='%.f%%',
            textprops={'fontsize':8, 'color': 'black'},
            startangle=45,
            # move the percentage inside the arcs
            pctdistance=0.75,
            # add spaces between the arcs
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
            )
    ax1.set_title('Planšetinių kompiuterių gamintojai (Varle.lt)')
    sns.boxplot(data=df, x='brand', y='kaina', ax=ax2, showmeans=True, showfliers=False)
    ax2.tick_params(axis='x', rotation=90)
    ax2.set_title('Kainos pasiskirtysmas pagal gamintoją (Varle.lt)')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    # plansete gamintojai pigu
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    `Prekės ženklas:`
    from PlansetePigu;"""
    df = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    top = df['Prekės ženklas:'].value_counts().head(9).index.tolist()

    df['brand'] = df['Prekės ženklas:'].apply(lambda x: x if x in top else 'Kita')
    c = df['brand'].value_counts()
    # df['kaina'] = df['kaina'].str.extract('(\d+)')
    # df['kaina'] = df['kaina'].apply(lambda x: float(x))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
    # ax.pie(c.values, labels=c.index, autopct='%.f%%')
    ax1.pie(c.values, 
            labels=c.index, 
            autopct='%.f%%',
            textprops={'fontsize':8, 'color': 'black'},
            startangle=45,
            # move the percentage inside the arcs
            pctdistance=0.75,
            # add spaces between the arcs
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
            )
    ax1.set_title('Planšetinių kompiuteriu gamintojai (Pigu.lt)')
    sns.boxplot(data=df, x='brand', y='kaina', ax=ax2, showmeans=True, showfliers=False)
    ax2.tick_params(axis='x', rotation=90)
    ax2.set_title('Kainos pasiskirtysmas pagal gamintoją (Pigu.lt)')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    
    
    # top 15
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas
    from PlanseteVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`
    from PlansetePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    brand_counts = df['gamintojas'].value_counts()
    brands_to_plot = brand_counts[brand_counts > 5].index

    df_gamintojas = df[df['gamintojas'].isin(brands_to_plot)][['kaina', 'gamintojas']]
    # Calculate the average price per brand
    average_price_per_brand = df_gamintojas.groupby('gamintojas')['kaina'].mean().reset_index()
    avg_price_sorted = average_price_per_brand.sort_values(by='kaina', ascending=True)
    top5_low = avg_price_sorted['gamintojas'].head(5).tolist()
    avg_price_sorted = average_price_per_brand.sort_values(by='kaina', ascending=False)
    top5_high = avg_price_sorted['gamintojas'].head(5).tolist()
    # print(top5_high)
    # print(top5_low)
    # # Find the median of the average prices
    median_avg_price = average_price_per_brand['kaina'].median()
    # print(median_avg_price)

    # Find the 5 brands whose average prices are closest to the median
    average_price_per_brand['price_diff_from_median'] = (average_price_per_brand['kaina'] - median_avg_price).abs()
    top_5_middle_avg = average_price_per_brand.sort_values(by='price_diff_from_median').head(5)
    top5_middle = top_5_middle_avg['gamintojas'].head(5).tolist()
    # print(top5_middle)
    top_brands = top5_high + top5_middle + top5_low
    # print(top_brands)

    # Pigu
    dfp['gamintojas'] = dfp['Prekės ženklas:']
    brand_counts_p = dfp['gamintojas'].value_counts()
    brands_to_plot_p = brand_counts_p[brand_counts_p > 5].index

    df_gamintojas_p = dfp[dfp['gamintojas'].isin(brands_to_plot_p)][['kaina', 'gamintojas']]
    # Calculate the average price per brand
    average_price_per_brand_p = df_gamintojas_p.groupby('gamintojas')['kaina'].mean().reset_index()
    avg_price_sorted_p = average_price_per_brand_p.sort_values(by='kaina', ascending=True)
    top5_low_p = avg_price_sorted_p['gamintojas'].head(5).tolist()
    avg_price_sorted_p = average_price_per_brand_p.sort_values(by='kaina', ascending=False)
    top5_high_p = avg_price_sorted_p['gamintojas'].head(5).tolist()
    # print(top5_high)
    # print(top5_low)
    # # Find the median of the average prices
    median_avg_price_p = average_price_per_brand_p['kaina'].median()
    # print(median_avg_price)

    # Find the 5 brands whose average prices are closest to the median
    average_price_per_brand_p['price_diff_from_median'] = (average_price_per_brand_p['kaina'] - median_avg_price_p).abs()
    top_5_middle_avg_p = average_price_per_brand_p.sort_values(by='price_diff_from_median').head(5)
    top5_middle_p = top_5_middle_avg_p['gamintojas'].head(5).tolist()
    # print(top5_middle)
    top_brands_p = top5_high_p + top5_middle_p + top5_low_p

    df_brand_p = df_gamintojas_p[df_gamintojas_p['gamintojas'].isin(top_brands_p)]
    df_brand = df_gamintojas[df_gamintojas['gamintojas'].isin(top_brands)]

    df_brand['saltinis'] = 'Varle.lt'
    df_brand_p['saltinis'] = 'Pigu.lt'


    df_combined = pd.concat([df_brand, df_brand_p])
    df_combined.dropna(subset='gamintojas', inplace=True)
    fig, ax =plt.subplots()
    sns.boxplot(data=df_combined, x='gamintojas', y='kaina', showmeans=True, showfliers=False, hue='saltinis')
    plt.tick_params(axis='x', rotation=90)
    plt.title('Top (high/middle/low) gamintojai kainos pasiskirstymas (Varle.lt)')
    st.pyplot(fig, use_container_width=True)
    
    st.write(f'Brangiausi planšetinių kompiuterių gamintojai Varle.lt : {top5_high}')
    st.write(f'Vidutinės kainos planšetinių kompiuterių gamintojai Varle.lt : {top5_middle}')
    st.write(f'Pigiausi planšetinių kompiuterių gamintojai Varle.lt : {top5_low}')
    st.write(f'Brangiausi dviračių gamintojai Pigu.lt : {top5_high_p}')
    st.write(f'Vidutinės kainos planšetinių kompiuterių gamintojai Pigu.lt : {top5_middle_p}')
    st.write(f'Pigiausi planšetinių kompiuterių gamintojai Pigu.lt : {top5_low_p}')
    
    # top gamintojai isskaidyti
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas
    from PlanseteVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`
    from PlansetePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    dfp['gamintojas'] = dfp['Prekės ženklas:']

    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'

    # max
    df_remas_max = df[df['gamintojas'].isin(top5_high)][['kaina', 'gamintojas', 'saltinis']]
    dfp_remas_max = dfp[dfp['gamintojas'].isin(top5_high_p)][['kaina', 'gamintojas', 'saltinis']]
    # mid
    df_remas_mid = df[df['gamintojas'].isin(top5_middle)][['kaina', 'gamintojas', 'saltinis']]
    dfp_remas_mid = dfp[dfp['gamintojas'].isin(top5_middle_p)][['kaina', 'gamintojas', 'saltinis']]
    # min
    df_remas_min = df[df['gamintojas'].isin(top5_low)][['kaina', 'gamintojas', 'saltinis']]
    dfp_remas_min = dfp[dfp['gamintojas'].isin(top5_low_p)][['kaina', 'gamintojas', 'saltinis']]
    # sujungiam
    df_combined_max = pd.concat([df_remas_max, dfp_remas_max]).reset_index()
    df_combined_mid = pd.concat([df_remas_mid, dfp_remas_mid]).reset_index()
    df_combined_min = pd.concat([df_remas_min, dfp_remas_min]).reset_index()


    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_max, x='gamintojas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Brangiausių gamintojų kainos pasiskirstymas')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_mid, x='gamintojas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Vidutinės kainos gamintojų kainos pasiskirstymas')
    plt.tick_params(axis='x', rotation=90)
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_min, x='gamintojas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Pigiausių gamintojų kainos pasiskirstymas')
    st.pyplot(fig, use_container_width=True)

    # ekrano size palyginimas
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    `ekrano įstrižainė`,
    `ekrano dydis`,
    `ekrano dydis (coliais)`,
    `ekranas – įstrižainė (")`,
    `įstrižainės ekranas`,
    `ekrano dydis [coliais]`
    from PlanseteVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Ekrano įstrižainė:`,
    `Prekės ženklas:`
    from PlansetePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    # varle
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    for col in df.columns:
        if col != 'kaina':
            df['ekrano įstrižainė'] = df['ekrano įstrižainė'].fillna(df[col])

    df.dropna(subset='ekrano įstrižainė', inplace=True)

    def set_size(x):
        if 'cm' in x:
            size_cm = float(x.split(' ')[0].replace(',', '.'))
            coliai = round(size_cm /2.54, 1)
            return coliai
        else:
            return x
        
    df['ekrano įstrižainė'] = df['ekrano įstrižainė'].apply(set_size)

    df['ekrano įstrižainė'] = df['ekrano įstrižainė'].str.extract('(\d+)')
    df['ekrano įstrižainė'] = df['ekrano įstrižainė'].apply(lambda x: float(x))
    dfe = df[['kaina','ekrano įstrižainė' ]]
    dfe_gr = dfe.groupby('ekrano įstrižainė').mean(numeric_only=True).reset_index()

    # pigu
    dfp.dropna(subset='Ekrano įstrižainė:', inplace=True)
    dfp['Ekrano įstrižainė:'] = dfp['Ekrano įstrižainė:'].str.extract('(\d+)')
    dfp['Ekrano įstrižainė:'] = dfp['Ekrano įstrižainė:'].apply(lambda x: float(x))
    dfp_gr = dfp.groupby('Ekrano įstrižainė:').mean(numeric_only=True).reset_index()

    fig, ax = plt.subplots()
    sns.regplot(data=dfe_gr[dfe_gr['ekrano įstrižainė'] < 40], x='ekrano įstrižainė', y='kaina', ax=ax, label='Varle.lt')
    sns.regplot(data=dfp_gr, x='Ekrano įstrižainė:', y='kaina', ax=ax, label='Pigu.lt')
    plt.title('Kainos priklausomybė nuo ekrano įstižainės')
    plt.legend()
    st.pyplot(fig, use_container_width=True)

    # ekrano tipai
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ekrano tipas`,
    `ekrano technologija`
    from PlanseteVarle;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Ekrano tipas:`
    from PlansetePigu;"""
    dfp_with_dubs = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    #  varle
    df = df_with_dubs.drop_duplicates()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    df['ekrano tipas'].fillna(df['ekrano technologija'])
    df['Ekranas'] = df['ekrano tipas']
    df['saltinis'] = 'Varle.lt'
    df_join = df[['kaina', 'Ekranas', 'saltinis']]
    # df_join.head()

    # pigu
    dfp = dfp_with_dubs.drop_duplicates()
    dfp['Ekranas'] = dfp['Ekrano tipas:']
    dfp['saltinis'] = 'Pigu.lt'
    dfp_join = dfp[['kaina', 'Ekranas', 'saltinis']]
    # dfp_join.head()

    # join tables
    df_combined = pd.concat([df_join, dfp_join])
    df_combined.dropna(subset='Ekranas', inplace=True)

    types_counts = df_combined['Ekranas'].value_counts()
    types_to_plot = types_counts[types_counts > 4].index

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined[df_combined['Ekranas'].isin(types_to_plot)], y='Ekranas', x='kaina', showmeans=True, showfliers=False, hue='saltinis', orient='h')
    plt.title('Kainos pasiskirstymas nuo ekrano tipo')
    st.pyplot(fig, use_container_width=True)
    
    # ekrano tipai top5 atskirai
    # ekrano tipai top5 atskirai
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ekrano tipas`,
    `ekrano technologija`
    from PlanseteVarle;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Ekrano tipas:`
    from PlansetePigu;"""
    dfp_with_dubs = pd.read_sql_query(sql2, con=SDB)
    SDB.close()

    df = df_with_dubs.drop_duplicates()
    dfp = dfp_with_dubs.drop_duplicates()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    df['ekrano tipas'].fillna(df['ekrano technologija'])
    df['tipas'] = df['ekrano tipas']
    dfp['gamintojas'] = dfp['Prekės ženklas:']        
    dfp['tipas'] = dfp['Ekrano tipas:']  
    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'


    # max
    df_remas_max = df[df['gamintojas'].isin(top5_high)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    dfp_remas_max = dfp[dfp['gamintojas'].isin(top5_high_p)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    # mid
    df_remas_mid = df[df['gamintojas'].isin(top5_middle)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    dfp_remas_mid = dfp[dfp['gamintojas'].isin(top5_middle_p)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    # min
    df_remas_min = df[df['gamintojas'].isin(top5_low)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    dfp_remas_min = dfp[dfp['gamintojas'].isin(top5_low_p)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    # sujungiam
    df_combined_max = pd.concat([df_remas_max, dfp_remas_max]).reset_index()
    df_combined_mid = pd.concat([df_remas_mid, dfp_remas_mid]).reset_index()
    df_combined_min = pd.concat([df_remas_min, dfp_remas_min]).reset_index()


    fig, ax = plt.subplots(figsize= (12, 12))
    sns.boxplot(data=df_combined_max, y='tipas', x='kaina',hue='saltinis',orient='h', showmeans=True, showfliers=False)
    plt.title('Brangiausių gamintojų kainos pasiskirstymas pagal ekrano raišką')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_mid, y='tipas', x='kaina',hue='saltinis', orient='h', showmeans=True, showfliers=False)
    plt.title('Vidutinės gamintojų kainos pasiskirstymas pagal ekrano raišką')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_min, y='tipas', x='kaina',hue='saltinis', orient='h', showmeans=True, showfliers=False)
    plt.title('Pigiausių gamintojų kainos pasiskirstymas pagal ekrano raišką')
    st.pyplot(fig, use_container_width=True)  

    # ekrano raiska
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ekrano raiška`,
    raiška,
    `ekrano raiška (pikseliais)`
    from PlanseteVarle;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Maksimali raiška:`
    from PlansetePigu;"""
    dfp_with_dubs = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    #  varle
    df = df_with_dubs.drop_duplicates()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    for col in df.columns:
        if col not in ['kaina', 'gamintojas']:
            df['ekrano raiška'] = df['ekrano raiška'].fillna(df[col])


    # Pigu
    dfp = dfp_with_dubs.drop_duplicates()
    dfp['ekrano raiška'] = dfp['Maksimali raiška:']

    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'
    df_join = df[['kaina', 'ekrano raiška', 'saltinis']]
    dfp_join = dfp[['kaina', 'ekrano raiška', 'saltinis']]

    # join tables
    df_combined = pd.concat([df_join, dfp_join])
    df_combined.dropna(subset='ekrano raiška', inplace=True)

    types_counts = df_combined['ekrano raiška'].value_counts()
    types_to_plot = types_counts[types_counts > 9].index

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined[df_combined['ekrano raiška'].isin(types_to_plot)], y='ekrano raiška', x='kaina', showmeans=True, showfliers=False, hue='saltinis', orient='h')
    plt.title('Kainos pasiskirstymas nuo ekrano raiškos')
    st.pyplot(fig, use_container_width=True)
    
    # ekrano raiska top 5 atskirai
    # ekrano raiska top5 atskirai
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ekrano raiška`,
    raiška,
    `ekrano raiška (pikseliais)`
    from PlanseteVarle;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Maksimali raiška:`
    from PlansetePigu;"""
    dfp_with_dubs = pd.read_sql_query(sql2, con=SDB)
    SDB.close()

    df = df_with_dubs.drop_duplicates()
    dfp = dfp_with_dubs.drop_duplicates()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    for col in df.columns:
        if col not in ['kaina', 'gamintojas']:
            df['ekrano raiška'] = df['ekrano raiška'].fillna(df[col])

    dfp['ekrano raiška'] = dfp['Maksimali raiška:']
    dfp['gamintojas'] = dfp['Prekės ženklas:']        
    
    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'


    # max
    df_remas_max = df[df['gamintojas'].isin(top5_high)][['kaina', 'gamintojas', 'ekrano raiška', 'saltinis']]
    dfp_remas_max = dfp[dfp['gamintojas'].isin(top5_high_p)][['kaina', 'gamintojas', 'ekrano raiška', 'saltinis']]
    # mid
    df_remas_mid = df[df['gamintojas'].isin(top5_middle)][['kaina', 'gamintojas', 'ekrano raiška', 'saltinis']]
    dfp_remas_mid = dfp[dfp['gamintojas'].isin(top5_middle_p)][['kaina', 'gamintojas', 'ekrano raiška', 'saltinis']]
    # min
    df_remas_min = df[df['gamintojas'].isin(top5_low)][['kaina', 'gamintojas', 'ekrano raiška', 'saltinis']]
    dfp_remas_min = dfp[dfp['gamintojas'].isin(top5_low_p)][['kaina', 'gamintojas', 'ekrano raiška', 'saltinis']]
    # sujungiam
    df_combined_max = pd.concat([df_remas_max, dfp_remas_max]).reset_index()
    df_combined_mid = pd.concat([df_remas_mid, dfp_remas_mid]).reset_index()
    df_combined_min = pd.concat([df_remas_min, dfp_remas_min]).reset_index()


    fig, ax = plt.subplots(figsize= (12, 10))
    sns.boxplot(data=df_combined_max, y='ekrano raiška', x='kaina',hue='saltinis',orient='h', showmeans=True, showfliers=False)
    plt.title('Brangiausių gamintojų kainos pasiskirstymas pagal erano raišką')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_mid, y='ekrano raiška', x='kaina',hue='saltinis', orient='h', showmeans=True, showfliers=False)
    plt.title('Vidutinės gamintojų kainos pasiskirstymas pagal erano raišką')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_min, y='ekrano raiška', x='kaina',hue='saltinis', orient='h', showmeans=True, showfliers=False)
    plt.title('Pigiausių gamintojų kainos pasiskirstymas pagal erano raišką')
    st.pyplot(fig, use_container_width=True)
    

    # atmintis
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `vidinė atmintis (gb)`,
    `disko atmintis`,
    `vidinės atminties dydis`,
    `vidinė atmintis`,
    `vidinės atminties dydis [gb]`
    from PlanseteVarle;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Vidinė atmintis:`,
    `Prekės ženklas:`
    from PlansetePigu;"""
    dfp_with_dubs = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    #  varle

    df = df_with_dubs.drop_duplicates()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    for col in df.columns:
        if col not in ['kaina', 'gamintojas']:
            df['vidinė atmintis (gb)'] = df['vidinė atmintis (gb)'].fillna(df[col])
    df.dropna(subset='vidinė atmintis (gb)', inplace=True)
    df['vidinė atmintis (gb)'] = df['vidinė atmintis (gb)'].str.extract('(\d+)')
    df['vidinė atmintis (gb)'] = df['vidinė atmintis (gb)'].apply(lambda x: float(x))

    # pigu

    dfp = dfp_with_dubs.drop_duplicates()
    dfp['Vidinė atmintis:'] = dfp['Vidinė atmintis:'].str.extract('(\d+)')
    dfp['Vidinė atmintis:'] = dfp['Vidinė atmintis:'].apply(lambda x: float(x))
    dfp.dropna(subset='Vidinė atmintis:', inplace=True)
    df_memory = df[['kaina', 'vidinė atmintis (gb)']]
    df_memory_gr = df_memory.groupby('vidinė atmintis (gb)').mean(numeric_only=True).reset_index()

    dfp_memory = dfp[['kaina', 'Vidinė atmintis:']]
    dfp_memory_gr = dfp_memory.groupby('Vidinė atmintis:').mean(numeric_only=True).reset_index()
    fig, ax = plt.subplots()
    sns.regplot(data=df_memory_gr, x='vidinė atmintis (gb)', y='kaina', ax=ax, label='Varle.lt')
    sns.regplot(data=dfp_memory_gr, x='Vidinė atmintis:', y='kaina', ax=ax, label='Pigu.lt')
    plt.title('Kainos priklausomybė nuo vidinės atmintis (GB)')
    plt.legend()
    st.pyplot(fig, use_container_width=True)


    #  RAM
    # atmintis
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `atmintis (ram) (gb)`,
    `operatyvioji atmintis`,
    `operatyvioji ram atmintis`,
    `įdiegta ram atmintis`,
    `darbinė atmintis (ram)`,
    `operacinės atminties dydis [gb]`,
    `atmintis (ram)`

    from PlanseteVarle;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Operatyvinė atmintis (RAM):`,
    `Prekės ženklas:`
    from PlansetePigu;"""
    dfp_with_dubs = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    #  varle

    df = df_with_dubs.drop_duplicates()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    for col in df.columns:
        if col not in ['kaina', 'gamintojas']:
            df['atmintis (ram) (gb)'] = df['atmintis (ram) (gb)'].fillna(df[col])
    df.dropna(subset='atmintis (ram) (gb)', inplace=True)
    df['atmintis (ram) (gb)'] = df['atmintis (ram) (gb)'].str.extract('(\d+)')
    df['atmintis (ram) (gb)'] = df['atmintis (ram) (gb)'].apply(lambda x: float(x))


    dfp = dfp_with_dubs.drop_duplicates()
    dfp['Operatyvinė atmintis (RAM):'] = dfp['Operatyvinė atmintis (RAM):'].str.extract('(\d+)')
    dfp['Operatyvinė atmintis (RAM):'] = dfp['Operatyvinė atmintis (RAM):'].apply(lambda x: float(x))
    dfp.dropna(subset='Operatyvinė atmintis (RAM):', inplace=True)
    dfp['ram'] = dfp['Operatyvinė atmintis (RAM):'].apply(lambda x: np.floor(x/1000))

    df_memory = df[['kaina', 'atmintis (ram) (gb)']]
    df_memory_gr = df_memory.groupby('atmintis (ram) (gb)').mean(numeric_only=True).reset_index()

    dfp_memory = dfp[['kaina', 'ram']]
    dfp_memory_gr = dfp_memory.groupby('ram').mean(numeric_only=True).reset_index()
    fig, ax = plt.subplots()
    sns.regplot(data=df_memory_gr[df_memory_gr['atmintis (ram) (gb)'] < 20], x='atmintis (ram) (gb)', y='kaina', ax=ax, label='Varle.lt')
    sns.regplot(data=dfp_memory_gr, x='ram', y='kaina', ax=ax, label='Pigu.lt')
    plt.title('Kainos priklausomybė nuo RAM atminties (GB)')
    plt.legend()
    st.pyplot(fig, use_container_width=True)


    # svoris
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    svorio,
    svoris,
    `nominalus svoris`,
    `grynas (neto) svoris`,
    `bendras svoris`,
    `prekės svoris`,
    `svoris [g]`,
    `svoris (g)`,
    `svoris, g`
    from PlanseteVarle;"""
    df_with_dubs = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Svoris:`
    from PlansetePigu;"""
    dfp_with_dubs = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    #  varle

    df = df_with_dubs.drop_duplicates()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    for col in df.columns:
        if col not in ['kaina', 'gamintojas']:
            df['svoris'] = df['svoris'].fillna(df[col])

    df.dropna(subset='svoris', inplace=True)
        
    def set_svoris(x):
        '''gausim svorį gramais'''
        if 'Wi' in x:
            return float(x.split('(')[-1].split(' ')[0])
        elif 'Nėra' in x:
            return 0
        else:
            x1 = float(x.replace('kg', '').replace('g', '').replace(',', '.'))
            if x1 != '':
                if x1 < 5:
                    return x1 *1000
                else:
                    return x1
            
    df['svoris'] = df['svoris'].apply(set_svoris)        



    dfp = dfp_with_dubs.drop_duplicates()
    dfp.dropna(subset='Svoris:', inplace=True)
    dfp['Svoris:'] = dfp['Svoris:'].apply(lambda x: x.replace('kg', '').replace('-', '0'))
    dfp['Svoris:'] = dfp['Svoris:'].apply(lambda x: float(x) * 1000)

    df_mass = df[['kaina', 'svoris']]
    df_mass_gr = df_mass.groupby('svoris').mean(numeric_only=True).reset_index()

    dfp_mass = dfp[['kaina', 'Svoris:']]
    dfp_mass_gr = dfp_mass.groupby('Svoris:').mean(numeric_only=True).reset_index()
    fig, ax = plt.subplots()
    sns.regplot(data=df_mass_gr[df_mass_gr['svoris'] > 1], x='svoris', y='kaina', ax=ax, label='Varle.lt')
    sns.regplot(data=dfp_mass_gr[(dfp_mass_gr['Svoris:'] > 1) &(dfp_mass_gr['Svoris:'] < 3000)], x='Svoris:', y='kaina', ax=ax, label='Pigu.lt')
    plt.title('Kainos priklausomybė nuo svorio (g)')
    plt.legend()
    st.pyplot(fig, use_container_width=True)
    
    #  lentele varle
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina, 
    gamintojas,
    `ekrano tipas`,
    `ekrano technologija`,
    `ekrano raiška`,
    raiška,
    `ekrano raiška (pikseliais)`,
    `vidinė atmintis (gb)`,
    `disko atmintis`,
    `vidinės atminties dydis`,
    `vidinė atmintis`,
    `vidinės atminties dydis [gb]`,
    `atmintis (ram) (gb)`,
    `operatyvioji atmintis`,
    `operatyvioji ram atmintis`,
    `įdiegta ram atmintis`,
    `darbinė atmintis (ram)`,
    `operacinės atminties dydis [gb]`,
    `atmintis (ram)`

    from PlanseteVarle;"""
    df_ivairus = pd.read_sql_query(sql, con=SDB)

    SDB.close()
    df = df_ivairus[(df_ivairus['gamintojas'] == 'Apple') | (df_ivairus['gamintojas'] == 'Samsung')]
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    df['ekrano tipas'].fillna(df['ekrano technologija'])
    df['Ekranas'] = df['ekrano tipas']

    for col in df.columns:
        if col  in ['ekrano raiška','raiška','ekrano raiška (pikseliais)']:
            df['ekrano raiška'] = df['ekrano raiška'].fillna(df[col])
            
    for col in df.columns:
        if col  in ['vidinė atmintis (gb)', 'disko atmintis','vidinės atminties dydis','vidinė atmintis','vidinės atminties dydis [gb]']:
            df['vidinė atmintis (gb)'] = df['vidinė atmintis (gb)'].fillna(df[col])
            
    df['vidinė atmintis (gb)'] = df['vidinė atmintis (gb)'].str.extract('(\d+)')
    df['vidinė atmintis (gb)'] = df['vidinė atmintis (gb)'].apply(lambda x: float(x))   

    for col in df.columns:
        if col not in ['atmintis (ram) (gb)','operatyvioji atmintis','operatyvioji ram atmintis','įdiegta ram atmintis','darbinė atmintis (ram)','operacinės atminties dydis [gb]', 'atmintis (ram)']:
            df['atmintis (ram) (gb)'] = df['atmintis (ram) (gb)'].fillna(df[col])
            
    df['atmintis (ram) (gb)'] = df['atmintis (ram) (gb)'].str.extract('(\d+)')
    df['atmintis (ram) (gb)'] = df['atmintis (ram) (gb)'].apply(lambda x: float(x))      
    df.drop_duplicates()

    price_bins = [0, 100, 200, 400, 600,30000]
    price_labels = ['iki 100', '101-200', '201-400', '401-600', ' nuo 600']
    df_data = df[['kaina', 'gamintojas', 'Ekranas', 'ekrano raiška', 'vidinė atmintis (gb)', 'atmintis (ram) (gb)' ]]

    df_data['price_range'] = pd.cut(df_data['kaina'], bins=price_bins, labels=price_labels, right=True)

    grouped = df_data.groupby('price_range')
    def safe_mode(x):
        mode = x.mode()
        return mode.iloc[0] if not mode.empty else None

    # # find most comman
    most_common_drone = grouped.agg({
        # 'kaina': safe_mode,
        'gamintojas': safe_mode,
        'Ekranas': safe_mode,
        'ekrano raiška': safe_mode,
        'vidinė atmintis (gb)': safe_mode,
        'atmintis (ram) (gb)': safe_mode
    }).reset_index()

    st.write('Labiausiai tikėtinas planšetinis kompiuteris Varle.lt')
    st.write(most_common_drone)
    
    
    #  lentele pigu
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina, 
    `Prekės ženklas:`,
    `Ekrano tipas:`,
    `Maksimali raiška:`,
    `Vidinė atmintis:`,
    `Operatyvinė atmintis (RAM):`
    from PlansetePigu;"""
    df_ivairus = pd.read_sql_query(sql, con=SDB)

    SDB.close()

    df = df_ivairus[(df_ivairus['Prekės ženklas:'] == 'Apple') | (df_ivairus['Prekės ženklas:'] == 'Samsung')]

    df['gamintojas'] = df['Prekės ženklas:']
    df['Ekranas'] = df['Ekrano tipas:']
    df['ekrano raiška'] = df['Maksimali raiška:']

    df['Vidinė atmintis:'] = df['Vidinė atmintis:'].str.extract('(\d+)')
    df['Vidinė atmintis:'] = df['Vidinė atmintis:'].apply(lambda x: float(x))
    df['vidinė atmintis (gb)'] = df['Vidinė atmintis:']

    df['Operatyvinė atmintis (RAM):'] = df['Operatyvinė atmintis (RAM):'].str.extract('(\d+)')
    df['Operatyvinė atmintis (RAM):'] = df['Operatyvinė atmintis (RAM):'].apply(lambda x: float(x))
    df['atmintis (ram) (gb)'] = df['Operatyvinė atmintis (RAM):'].apply(lambda x: np.floor(x/1000))

    price_bins = [0, 100, 200, 400, 600,30000]
    price_labels = ['iki 100', '101-200', '201-400', '401-600', ' nuo 600']
    df_data = df[['kaina', 'gamintojas', 'Ekranas', 'ekrano raiška', 'vidinė atmintis (gb)', 'atmintis (ram) (gb)' ]]

    df_data['price_range'] = pd.cut(df_data['kaina'], bins=price_bins, labels=price_labels, right=True)

    grouped = df_data.groupby('price_range')
    def safe_mode(x):
        mode = x.mode()
        return mode.iloc[0] if not mode.empty else None

    # # find most comman
    most_common_drone = grouped.agg({
        # 'kaina': safe_mode,
        'gamintojas': safe_mode,
        'Ekranas': safe_mode,
        'ekrano raiška': safe_mode,
        'vidinė atmintis (gb)': safe_mode,
        'atmintis (ram) (gb)': safe_mode
    }).reset_index()

    st.write('Labiausiai tikėtinas planšetinis kompiuteris Pigu.lt')
    st.write(most_common_drone)

        
if selected_option == 'Televizoriai':
    # tele galimtojai
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas
    from TeleVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`
    from TelePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    dfp.head()


    dfp['gamintojas'] = dfp['Prekės ženklas:']

    top = df['gamintojas'].value_counts().head(9).index.tolist()

    df['brand'] = df['gamintojas'].apply(lambda x: x if x in top else 'Kita')
    c = df['brand'].value_counts()
    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    # pigu
    top_p = dfp['gamintojas'].value_counts().head(9).index.tolist()

    dfp['brand'] = dfp['gamintojas'].apply(lambda x: x if x in top_p else 'Kita')
    c_p = dfp['brand'].value_counts()

    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'

    # sujungiam
    df_join = df[['kaina', 'brand', 'saltinis']]
    dfp_join = dfp[['kaina', 'brand', 'saltinis']]
    df_combined = pd.concat([df_join, dfp_join])
    # df_combined.dropna(subset='gamintojas', inplace=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
    # ax.pie(c.values, labels=c.index, autopct='%.f%%')
    ax1.pie(c.values, 
            labels=c.index, 
            autopct='%.f%%',
            textprops={'fontsize':8, 'color': 'black'},
            startangle=45,
            # move the percentage inside the arcs
            pctdistance=0.75,
            # add spaces between the arcs
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
            )
    ax1.set_title('Televizorių gamintojai (Varle.lt)')

    ax2.pie(c_p.values, 
            labels=c_p.index, 
            autopct='%.f%%',
            textprops={'fontsize':8, 'color': 'black'},
            startangle=45,
            # move the percentage inside the arcs
            pctdistance=0.75,
            # add spaces between the arcs
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
            )
    ax2.set_title('Televizorių gamintojai (Pigu.lt)')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined, x='brand', y='kaina',hue='saltinis', ax=ax, showmeans=True, showfliers=False)
    ax.tick_params(axis='x', rotation=90)
    ax.set_title('Kainos pasiskirtysmas pagal gamintoją')
    st.pyplot(fig, use_container_width=True)
    
    
    # tele size 
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ekrano įstrižainė`
    from TeleVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Ekrano įstrižainė:`
    from TelePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df.dropna(subset='ekrano įstrižainė', inplace=True)
    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    # Define a function to clean and extract the size in inches
    def extract_inch_size(tv_size):
        # Remove any non-numeric characters except for the quotation marks (inches)
        tv_size = str(tv_size).lower().replace("coliu", "")  # Removing unwanted words like "coliu"
        
        # Match inches (e.g., "55", "43")
        inch_match = re.search(r'(\d+)\s*(?:"|inch)', tv_size)
        if inch_match:
            return int(inch_match.group(1))
        
        # Match size in cm and convert to inches (assuming 1 inch = 2.54 cm)
        cm_match = re.search(r'(\d+)\s*cm', tv_size)
        if cm_match:
            cm_value = int(cm_match.group(1))
            return round(cm_value / 2.54)
        
        if len(tv_size) <= 2:
            return int(tv_size)
        
        

    df['size'] = df['ekrano įstrižainė'].apply(extract_inch_size)
    df.dropna(subset='size', inplace=True)

    def set_size_pigu(x):
        if x is not None:
            if '"' in x:
                return float(x.split('"')[0])
            if "''" in x:
                return float(x.split("''")[0])
            if '”'in x:
                return float(x.split('”')[0])
            

    dfp['size'] = dfp['Ekrano įstrižainė:'].apply(set_size_pigu)

    df_size = df[['kaina', 'size']]
    df_size_gr = df_size.groupby('size').mean(numeric_only=True).reset_index()
    dfp_size = dfp[['kaina', 'size']]
    dfp_size_gr = dfp_size.groupby('size').mean(numeric_only=True).reset_index()


    fig, ax = plt.subplots()
    # sns.regplot(data=df_size_gr, x='size', y='kaina', ax=ax, label='Varle.lt',order=3)
    sns.regplot(data=df_size, x='size', y='kaina', ax=ax, label='Varle.lt',order=3)
    # sns.regplot(data=dfp_size_gr, x='size', y='kaina', ax=ax, label='Pigu.lt',order=3)
    sns.regplot(data=dfp_size, x='size', y='kaina', ax=ax, label='Pigu.lt',order=3)
    plt.title('Kainos priklausomybė nuo ekrano įstižainės (coliais)')
    plt.legend()
    st.pyplot(fig, use_container_width=True)


    # tele max raiska 
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ekrano raiška`
    from TeleVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Maksimali raiška:`
    from TelePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    reso_counts = df['ekrano raiška'].value_counts()
    reso_to_plot = reso_counts[reso_counts > 5].index

    reso_counts_p = dfp['Maksimali raiška:'].value_counts()
    reso_to_plot_p = reso_counts_p[reso_counts_p > 3].index

    fig, ax = plt.subplots()
    sns.boxplot(data=df[df['ekrano raiška'].isin(reso_to_plot)], y='ekrano raiška', x='kaina', showmeans=True, showfliers=False)
    plt.title('Kainos pasiskirstymas nuo ekrano raiškos (Varle.lt)')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=dfp[dfp['Maksimali raiška:'].isin(reso_to_plot_p)], y='Maksimali raiška:', x='kaina', showmeans=True, showfliers=False)
    plt.title('Kainos pasiskirstymas nuo ekrano raiškos (Pigu.lt)')
    st.pyplot(fig, use_container_width=True)


    # tele ekrano tipas
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    Tipas
    from TeleVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Ekrano tipas:`
    from TelePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    df.drop_duplicates()
    df.dropna(subset='tipas', inplace=True)
    dfp.drop_duplicates()
    dfp.dropna(subset='Ekrano tipas:', inplace=True)
    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'
    df['Ekrano tipas'] = df['tipas']
    dfp['Ekrano tipas'] = dfp['Ekrano tipas:']

    df_join = df[['kaina', 'Ekrano tipas', 'saltinis']]
    dfp_join = dfp[['kaina', 'Ekrano tipas', 'saltinis']]

    df_combined = pd.concat([df_join, dfp_join])
    tipas_counts = df['Ekrano tipas'].value_counts()
    tipas_to_plot = tipas_counts[tipas_counts > 3].index

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined[df_combined['Ekrano tipas'].isin(tipas_to_plot)], x='Ekrano tipas', y='kaina', hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Kainos pasiskirtymas nuo ekrano tipo')
    st.pyplot(fig, use_container_width=True)


    # operacine pigu
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    `Prekės ženklas:`,
    `Operacinė sistema:`

    from TelePigu;"""
    df = pd.read_sql_query(sql, con=SDB)
    SDB.close()

    df['gamintojas'] = df['Prekės ženklas:']
    top5 = df['gamintojas'].value_counts().head(5).index.tolist()

    fig, ax = plt.subplots()
    sns.boxplot(data=df[df['gamintojas'].isin(top5)], y='Operacinė sistema:', x='kaina', hue='gamintojas', showmeans=True, showfliers=False)
    plt.title('Kainos pasiskirstymas nuo operacinės sistemos (Pigu.lt)')
    st.pyplot(fig, use_container_width=True)
    
    
    # top5 TV raiska
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ekrano raiška`
    from TeleVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Maksimali raiška:`
    from TelePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    dfp['gamintojas'] =dfp['Prekės ženklas:']
    dfp['ekrano raiška'] = dfp['Maksimali raiška:']
    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'

    top5TV = df['gamintojas'].value_counts().head(5).index.tolist()
    top5TV_p = dfp['gamintojas'].value_counts().head(5).index.tolist()
    
    st.write('Top 5 daugiausiai vienetų turinčių gamintojų Varle.lt:')
    st.write(top5TV)
    st.write()
    st.write('Top 5 daugiausiai vienetų turinčių gamintojų Pigu.lt:')
    st.write(top5TV_p)

    df_join = df[df['gamintojas'].isin(top5TV)][['kaina', 'gamintojas', 'ekrano raiška', 'saltinis']]
    dfp_join = dfp[dfp['gamintojas'].isin(top5TV_p)][['kaina', 'gamintojas', 'ekrano raiška', 'saltinis']]
    df_combined = pd.concat([df_join, dfp_join]).reset_index()

    types_counts = df_combined['ekrano raiška'].value_counts()
    types_to_plot = types_counts[types_counts > 4].index

    # fig, ax = plt.subplots(figsize= (12, 10))
    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined[df_combined['ekrano raiška'].isin(types_to_plot)], y='ekrano raiška', x='kaina',hue='saltinis',orient='h', showmeans=True, showfliers=False)
    plt.title('Top 5 gamintojų TV kainos pasiskirstymas pagal ekrano raišką')
    st.pyplot(fig, use_container_width=True)

    # fig, ax = plt.subplots(figsize= (12, 10))
    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined[df_combined['ekrano raiška'].isin(types_to_plot)], y='ekrano raiška', x='kaina',hue='gamintojas',orient='h', showmeans=True, showfliers=False)
    plt.title('Top 5 gamintojų TV kainos pasiskirstymas pagal ekrano raišką')
    st.pyplot(fig, use_container_width=True)
    
    
    #  top 5tele ekrano tipas
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    Tipas
    from TeleVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Ekrano tipas:`
    from TelePigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    dfp['gamintojas'] = dfp['Prekės ženklas:']
    df.drop_duplicates()
    df.dropna(subset='tipas', inplace=True)
    dfp.drop_duplicates()
    dfp.dropna(subset='Ekrano tipas:', inplace=True)
    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'
    df['Ekrano tipas'] = df['tipas']
    dfp['Ekrano tipas'] = dfp['Ekrano tipas:']

    df_join = df[df['gamintojas'].isin(top5TV)][['kaina', 'gamintojas', 'Ekrano tipas', 'saltinis']]
    dfp_join = dfp[dfp['gamintojas'].isin(top5TV_p)][['kaina', 'gamintojas', 'Ekrano tipas', 'saltinis']]
    df_combined = pd.concat([df_join, dfp_join]).reset_index()

    types_counts = df_combined['Ekrano tipas'].value_counts()
    types_to_plot = types_counts[types_counts > 4].index

    # fig, ax = plt.subplots(figsize= (12, 10))
    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined[df_combined['Ekrano tipas'].isin(types_to_plot)], y='Ekrano tipas', x='kaina',hue='saltinis',orient='h', showmeans=True, showfliers=False)
    plt.title('Top 5 gamintojų TV kainos pasiskirstymas pagal ekrano tipą')
    st.pyplot(fig, use_container_width=True)

    # fig, ax = plt.subplots(figsize= (12, 10))
    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined[df_combined['Ekrano tipas'].isin(types_to_plot)], y='Ekrano tipas', x='kaina',hue='gamintojas',orient='h', showmeans=True, showfliers=False)
    plt.title('Top 5 gamintojų TV kainos pasiskirstymas pagal ekrano tipą')
    st.pyplot(fig, use_container_width=True)


    # lentele varle
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ekrano įstrižainė`,
    `ekrano raiška`,
    Tipas
    from TeleVarle;"""
    df = pd.read_sql_query(sql, con=SDB)
    SDB.close()
    df.head()

    df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    # # Define a function to clean and extract the size in inches
    # def extract_inch_size(tv_size):
    #     # Remove any non-numeric characters except for the quotation marks (inches)
    #     tv_size = str(tv_size).lower().replace("coliu", "")  # Removing unwanted words like "coliu"
        
    #     # Match inches (e.g., "55", "43")
    #     inch_match = re.search(r'(\d+)\s*(?:"|inch)', tv_size)
    #     if inch_match:
    #         return int(inch_match.group(1))
        
    #     # Match size in cm and convert to inches (assuming 1 inch = 2.54 cm)
    #     cm_match = re.search(r'(\d+)\s*cm', tv_size)
    #     if cm_match:
    #         cm_value = int(cm_match.group(1))
    #         return round(cm_value / 2.54)
        
    #     if len(tv_size) <= 2:
    #         return int(tv_size)
        
        

    df['size'] = df['ekrano įstrižainė'].apply(extract_inch_size)
    price_bins = [0, 100, 200, 500,30000]
    price_labels = ['iki 100', '101-200', '201-500', 'nuo 500']
    df_data = df[['kaina', 'gamintojas', 'ekrano įstrižainė', 'ekrano raiška', 'tipas']]

    df_data['price_range'] = pd.cut(df_data['kaina'], bins=price_bins, labels=price_labels, right=True)

    grouped = df_data.groupby('price_range')
    def safe_mode(x):
        mode = x.mode()
        return mode.iloc[0] if not mode.empty else None

    # # find most comman
    most_common_tv = grouped.agg({
        'kaina': safe_mode,
        'gamintojas': safe_mode,
        'ekrano įstrižainė': safe_mode,
        'ekrano raiška': safe_mode,
        'tipas': safe_mode
    }).reset_index()
    st.write('Labiausiai tikėtinas televizorius (Varle.lt)')
    st.write(most_common_tv)


    # lentele pigu
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    `Prekės ženklas:`,
    `Ekrano įstrižainė:`,
    `Maksimali raiška:`,
    `Ekrano tipas:`,
    `Spalva:`,
    `WiFi:`,
    `Bluetooth:`,
    `Operacinė sistema:`

    from TelePigu;"""
    df = pd.read_sql_query(sql, con=SDB)
    SDB.close()

    def set_size_pigu(x):
        if x is not None:
            if '"' in x:
                return float(x.split('"')[0])
            if "''" in x:
                return float(x.split("''")[0])
            if '”'in x:
                return float(x.split('”')[0])
            

    df['size'] = df['Ekrano įstrižainė:'].apply(set_size_pigu)
    price_bins = [0, 100, 200, 500,30000]
    price_labels = ['iki 100', '101-200', '201-500', 'nuo 500']
    df_data = df[['kaina', 'Prekės ženklas:','size','Maksimali raiška:','Ekrano tipas:','Spalva:','WiFi:','Bluetooth:','Operacinė sistema:']]

    df_data['price_range'] = pd.cut(df_data['kaina'], bins=price_bins, labels=price_labels, right=True)

    grouped = df_data.groupby('price_range')
    def safe_mode(x):
        mode = x.mode()
        return mode.iloc[0] if not mode.empty else None

    # # find most comman
    most_common_tv = grouped.agg({
        'kaina': safe_mode,
        'Prekės ženklas:': safe_mode,
        'size': safe_mode,
        'Maksimali raiška:': safe_mode,
        'Ekrano tipas:': safe_mode,
        'Spalva:': safe_mode,
        'WiFi:': safe_mode,
        'Bluetooth:': safe_mode,
        'Operacinė sistema:': safe_mode,
    }).reset_index()
    st.write('Labiausiai tikėtinas televizorius (Pigu.lt)')
    st.write(most_common_tv)
    
    

    
    
    
if selected_option == 'Dviračiai':
    # gamintojai
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas
    from DviraciaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`
    from DviraciaiPigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    dfp.head()


    dfp['gamintojas'] = dfp['Prekės ženklas:']

    top = df['gamintojas'].value_counts().head(14).index.tolist()

    df['brand'] = df['gamintojas'].apply(lambda x: x if x in top else 'Kita')
    c = df['brand'].value_counts()
    # df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    # pigu
    top_p = dfp['gamintojas'].value_counts().head(14).index.tolist()

    dfp['brand'] = dfp['gamintojas'].apply(lambda x: x if x in top_p else 'Kita')
    c_p = dfp['brand'].value_counts()

    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'

    # sujungiam
    df_join = df[['kaina', 'brand', 'saltinis']]
    dfp_join = dfp[['kaina', 'brand', 'saltinis']]
    df_combined = pd.concat([df_join, dfp_join])
    # df_combined.dropna(subset='gamintojas', inplace=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4.5))
    # ax.pie(c.values, labels=c.index, autopct='%.f%%')
    ax1.pie(c.values, 
            labels=c.index, 
            autopct='%.f%%',
            textprops={'fontsize':8, 'color': 'black'},
            startangle=45,
            # move the percentage inside the arcs
            pctdistance=0.75,
            # add spaces between the arcs
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
            )
    ax1.set_title('Dviračių gamintojai (Varle.lt)')

    ax2.pie(c_p.values, 
            labels=c_p.index, 
            autopct='%.f%%',
            textprops={'fontsize':8, 'color': 'black'},
            startangle=45,
            # move the percentage inside the arcs
            pctdistance=0.75,
            # add spaces between the arcs
            # explode=[0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
            )
    ax2.set_title('Dviračių gamintojai (Pigu.lt)')
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined, y='brand', x='kaina',hue='saltinis', orient='h', ax=ax, showmeans=True, showfliers=False)
    ax.tick_params(axis='x', rotation=90)
    ax.set_title('Kainos pasiskirtysmas pagal gamintoją')
    st.pyplot(fig, use_container_width=True)
    
    
    #  top 3 max/mid/min pagal kaina
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas
    from DviraciaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`
    from DviraciaiPigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()
    # df['kaina'] = df['kaina'].str.extract('(\d+)')
    df['kaina'] = df['kaina'].apply(lambda x: float(x))

    # parenkam tik tuos gamintojus, kurie turi daugiau nei [x] gaminių
    brand_counts = df['gamintojas'].value_counts()
    brands_to_plot = brand_counts[brand_counts > 9].index

    df_gamintojas = df[df['gamintojas'].isin(brands_to_plot)][['kaina', 'gamintojas']]
    # Calculate the average price per brand
    average_price_per_brand = df_gamintojas.groupby('gamintojas')['kaina'].mean().reset_index()
    avg_price_sorted = average_price_per_brand.sort_values(by='kaina', ascending=True)
    top5_low = avg_price_sorted['gamintojas'].head(3).tolist()
    avg_price_sorted = average_price_per_brand.sort_values(by='kaina', ascending=False)
    top5_high = avg_price_sorted['gamintojas'].head(3).tolist()
    # print(top5_high)
    # print(top5_low)
    # # Find the median of the average prices
    median_avg_price = average_price_per_brand['kaina'].median()
    # print(median_avg_price)

    # Find the 5 brands whose average prices are closest to the median
    average_price_per_brand['price_diff_from_median'] = (average_price_per_brand['kaina'] - median_avg_price).abs()
    top_5_middle_avg = average_price_per_brand.sort_values(by='price_diff_from_median').head(3)
    top5_middle = top_5_middle_avg['gamintojas'].head(3).tolist()
    # print(top5_middle)
    top_brands = top5_high + top5_middle + top5_low
    # print(top_brands)

    # Pigu
    # parenkam tik tuos gamintojus, kurie turi daugiau nei [x] gaminių
    dfp['gamintojas'] = dfp['Prekės ženklas:']
    brand_counts_p = dfp['gamintojas'].value_counts()
    brands_to_plot_p = brand_counts_p[brand_counts_p > 9].index

    df_gamintojas_p = dfp[dfp['gamintojas'].isin(brands_to_plot_p)][['kaina', 'gamintojas']]
    # Calculate the average price per brand
    average_price_per_brand_p = df_gamintojas_p.groupby('gamintojas')['kaina'].mean().reset_index()
    avg_price_sorted_p = average_price_per_brand_p.sort_values(by='kaina', ascending=True)
    top5_low_p = avg_price_sorted_p['gamintojas'].head(3).tolist()
    avg_price_sorted_p = average_price_per_brand_p.sort_values(by='kaina', ascending=False)
    top5_high_p = avg_price_sorted_p['gamintojas'].head(3).tolist()
    # print(top5_high_p)
    # print(top5_low_p)
    # # Find the median of the average prices
    median_avg_price_p = average_price_per_brand_p['kaina'].median()
    # print(median_avg_price)

    # Find the 5 brands whose average prices are closest to the median
    average_price_per_brand_p['price_diff_from_median'] = (average_price_per_brand_p['kaina'] - median_avg_price_p).abs()
    top_5_middle_avg_p = average_price_per_brand_p.sort_values(by='price_diff_from_median').head(3)
    top5_middle_p = top_5_middle_avg_p['gamintojas'].head(3).tolist()
    # print(top5_middle_p)
    top_brands_p = top5_high_p + top5_middle_p + top5_low_p

    df_brand_p = df_gamintojas_p[df_gamintojas_p['gamintojas'].isin(top_brands_p)]
    df_brand = df_gamintojas[df_gamintojas['gamintojas'].isin(top_brands)]

    df_brand['saltinis'] = 'Varle.lt'
    df_brand_p['saltinis'] = 'Pigu.lt'


    df_combined = pd.concat([df_brand, df_brand_p])
    df_combined.dropna(subset='gamintojas', inplace=True)


    sns.boxplot(data=df_combined, x='gamintojas', y='kaina', showmeans=True, showfliers=False, hue='saltinis')
    plt.tick_params(axis='x', rotation=90)
    plt.title('Top (pagal vid. kaina max/mid/min) gamintojai kainos pasiskirstymas (Varle.lt)')
    st.pyplot(fig, use_container_width=True)
    
    
    # dviraciu remas

    top3_max = ['GZR', 'MMR', 'Bulls']
    top3_min = ['Dunlop', 'Adidas', 'Rockbros']
    top3_mid = ['Merida', 'Unibike', 'Laifook']
    top3_max_p = ['Bulls', 'Cube', 'Bergamont']
    top3_min_p = ['KidsPro', 'Dino bikes', 'Heart']
    top3_mid_p = ['Shimano', 'Insera', 'vidaXL']
    
    st.write(f'Brangiausi dviračių gamintojai Varle.lt : {top3_max}')
    st.write(f'Vidutinės kainos dviračių gamintojai Varle.lt : {top3_mid}')
    st.write(f'Pigiausi dviračių gamintojai Varle.lt : {top3_min}')
    st.write(f'Brangiausi dviračių gamintojai Pigu.lt : {top3_max_p}')
    st.write(f'Vidutinės kainos dviračių gamintojai Pigu.lt : {top3_mid_p}')
    st.write(f'Pigiausi dviračių gamintojai Pigu.lt : {top3_min_p}')

    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `rėmas (medžiaga)`,
    `rėmo medžiaga`,
    `dviračio rėmas (f, v)`,
    `rėmo tipas (v)`,
    `rėmas`,
    `rėmo metalas`
    from DviraciaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Rėmas:`

    from DviraciaiPigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    dfp['gamintojas'] = dfp['Prekės ženklas:']

    for col in df.columns:
        if col not in ['kaina', 'gamintojas']:
            df['rėmo medžiaga'] = df['rėmo medžiaga'].fillna(df[col])

    df['Rėmas'] = df['rėmo medžiaga']
    dfp['Rėmas'] = dfp['Rėmas:']

    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'

    def set_remas(x):
        if x is not None:
            if 'ALL' in x or 'Aliu' in x or 'aliu' in x:
                return 'Aliuminis'
            elif 'angl' in x or 'CARB' in x or 'Karb' in x or 'Angl' in x:
                return 'Karboninis'
            elif 'STEEL' in x or 'Plie' in x or 'CrMo' in x or 'Lyd' in x :
                return 'Plieninis'
            else:
                return x
            
    def set_remas_pigu(x):
        if x is not None:
            if 'Angl' in x:
                return 'Karboninis'

    df['Rėmas'] = df['Rėmas'].apply(set_remas)
    dfp['Rėmas'] = dfp['Rėmas'].apply(set_remas)

    # max
    df_remas_max = df[df['gamintojas'].isin(top3_max)][['kaina', 'gamintojas', 'Rėmas', 'saltinis']]
    dfp_remas_max = dfp[dfp['gamintojas'].isin(top3_max_p)][['kaina', 'gamintojas', 'Rėmas', 'saltinis']]
    # mid
    df_remas_mid = df[df['gamintojas'].isin(top3_mid)][['kaina', 'gamintojas', 'Rėmas', 'saltinis']]
    dfp_remas_mid = dfp[dfp['gamintojas'].isin(top3_mid_p)][['kaina', 'gamintojas', 'Rėmas', 'saltinis']]
    # min
    df_remas_min = df[df['gamintojas'].isin(top3_min)][['kaina', 'gamintojas', 'Rėmas', 'saltinis']]
    dfp_remas_min = dfp[dfp['gamintojas'].isin(top3_min_p)][['kaina', 'gamintojas', 'Rėmas', 'saltinis']]
    # sujungiam
    df_combined_max = pd.concat([df_remas_max, dfp_remas_max]).reset_index()
    df_combined_mid = pd.concat([df_remas_mid, dfp_remas_mid]).reset_index()
    df_combined_min = pd.concat([df_remas_min, dfp_remas_min]).reset_index()


    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_max, x='Rėmas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Brangiausių gamintojų kainos pasiskirstymas pagal rėmo medžiagą')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_mid, x='Rėmas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Vidutinės gamintojų kainos pasiskirstymas pagal rėmo medžiagą')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_min, x='Rėmas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Pigiausių gamintojų kainos pasiskirstymas pagal rėmo medžiagą')
    st.pyplot(fig, use_container_width=True)
    
    
    #  skirta v/m
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    skirta
    from DviraciaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Skirta:`
    from DviraciaiPigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    df['Skirta'] = df['skirta']
    dfp['gamintojas'] = dfp['Prekės ženklas:']

    dfp['Skirta'] = dfp['Skirta:']

    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'

    def set_skirta_varle(x):
        if x is not None:
            if 'Moterims\n' in x or 'Vyrams\n' in x or 'Suau' in x:
                return 'Universalus'
            elif 'gadiem' in x or 'Berniu' in x:
                return 'Vaikams'
            else:
                return x
            
    def set_skirta_pigu(x):
        if x is not None:
            if 'Univer' in x or 'Moterims,' in x:
                return 'Universalus'
            elif 'Berniukams' in x or 'Mergai' in x:
                return 'Paaugliams'
            else:
                return x
            
        
    df['Skirta'] = df['Skirta'].apply(set_skirta_varle)
    dfp['Skirta'] = dfp['Skirta'].apply(set_skirta_pigu)

    # max
    df_remas_max = df[df['gamintojas'].isin(top3_max)][['kaina', 'gamintojas', 'Skirta', 'saltinis']]
    dfp_remas_max = dfp[dfp['gamintojas'].isin(top3_max_p)][['kaina', 'gamintojas', 'Skirta', 'saltinis']]
    # mid
    df_remas_mid = df[df['gamintojas'].isin(top3_mid)][['kaina', 'gamintojas', 'Skirta', 'saltinis']]
    dfp_remas_mid = dfp[dfp['gamintojas'].isin(top3_mid_p)][['kaina', 'gamintojas', 'Skirta', 'saltinis']]
    # min
    df_remas_min = df[df['gamintojas'].isin(top3_min)][['kaina', 'gamintojas', 'Skirta', 'saltinis']]
    dfp_remas_min = dfp[dfp['gamintojas'].isin(top3_min_p)][['kaina', 'gamintojas', 'Skirta', 'saltinis']]
    # sujungiam
    df_combined_max = pd.concat([df_remas_max, dfp_remas_max]).reset_index()
    df_combined_mid = pd.concat([df_remas_mid, dfp_remas_mid]).reset_index()
    df_combined_min = pd.concat([df_remas_min, dfp_remas_min]).reset_index()


    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_max, x='Skirta', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Brangiausių gamintojų kainos pasiskirstymas pagal rėmo paskirtį')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_mid, x='Skirta', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Vidutinės gamintojų kainos pasiskirstymas pagal rėmo paskirtį')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_min, x='Skirta', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Pigiausių gamintojų kainos pasiskirstymas pagal rėmo paskirtį')
    st.pyplot(fig, use_container_width=True)
    
    
    #  dviracio tipas
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    tipas
    from DviraciaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Dviračių tipai:`
    from DviraciaiPigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    dfp['gamintojas'] = dfp['Prekės ženklas:']
    dfp['tipas'] = dfp['Dviračių tipai:']

    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'

    def set_tipas(x):
        if x is not None:
            if 'MTB' in x or 'Kaln' in x:
                return 'MTB'
            elif 'Miest' in x:
                return 'Miesto'
            elif 'Sulank' in x:
                return 'Sulankstomi'
            elif 'Hibri' in x:
                return 'Hibridiniai'
            elif 'Turist' in x:
                return 'Turistiniai'
            elif 'Trira' in x:
                return 'Triračiai'
            elif 'Fatb' in x:
                return 'Fatbike'
            elif 'BMX' in x:
                return 'BMX'
            else:
                return x
            
    # def set_tipas_pigu(x):
    #     if x is not None:

            
    df['tipas'] = df['tipas'].apply(set_tipas)
    dfp['tipas'] = dfp['tipas'].apply(set_tipas)

    # max
    df_remas_max = df[df['gamintojas'].isin(top3_max)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    dfp_remas_max = dfp[dfp['gamintojas'].isin(top3_max_p)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    # mid
    df_remas_mid = df[df['gamintojas'].isin(top3_mid)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    dfp_remas_mid = dfp[dfp['gamintojas'].isin(top3_mid_p)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    # min
    df_remas_min = df[df['gamintojas'].isin(top3_min)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    dfp_remas_min = dfp[dfp['gamintojas'].isin(top3_min_p)][['kaina', 'gamintojas', 'tipas', 'saltinis']]
    # sujungiam
    df_combined_max = pd.concat([df_remas_max, dfp_remas_max]).reset_index()
    df_combined_mid = pd.concat([df_remas_mid, dfp_remas_mid]).reset_index()
    df_combined_min = pd.concat([df_remas_min, dfp_remas_min]).reset_index()


    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_max, x='tipas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Brangiausių gamintojų kainos pasiskirstymas pagal tipą')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_mid, x='tipas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Vidutinės gamintojų kainos pasiskirstymas pagal tipą')
    plt.tick_params(axis='x', rotation=90)
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_min, x='tipas', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Pigiausių gamintojų kainos pasiskirstymas pagal tipą')
    st.pyplot(fig, use_container_width=True)
    
    
    #  dviracio ratai
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas,
    `ratų dydis (coliais)`,
    `ratų skersmuo, coliais`,
    `rato skersmuo [colis]`,
    `ratų dydis (f,v)`,
    `rato dydis`,
    `ratai`,
    `ratų dydis coliais`
    from DviraciaiVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

    sql2="""select kaina,
    `Prekės ženklas:`,
    `Ratų skersmuo:`
    from DviraciaiPigu;"""
    dfp = pd.read_sql_query(sql2, con=SDB)

    SDB.close()

    df['kaina'] = df['kaina'].apply(lambda x: float(x))
    dfp['gamintojas'] = dfp['Prekės ženklas:']
    dfp['ratai'] = dfp['Ratų skersmuo:']

    for col in df.columns:
        if col not in ['kaina', 'gamintojas']:
            df['ratai'] = df['ratai'].fillna(df[col])

    df['saltinis'] = 'Varle.lt'
    dfp['saltinis'] = 'Pigu.lt'

    def set_ratai_varle(x):
        if x is not None:
            if '28' in x:
                return '28'
            else:
                return x
            

    def set_ratai_pigu(x):
        if x is not None:
            if len(x) == 4:
                return x[:2]
            elif len(x) == 3:
                return x[0]
            elif len(x) == 6:
                return x[:4]
            elif '27 "'in x:
                return '27'
            elif '10 "'in x:
                return '10'
            elif '27.5 "'in x:
                return '27.5'
            elif '19 "'in x:
                return '19'
            elif '12 "'in x:
                return '12'
            elif '10 "'in x:
                return '10'
            elif '26 "'in x:
                return '26'
            else:
                return x
            
    def make_float(x):
        if x is not None:
            return float(x)
            
    df['ratai'] = df['ratai'].apply(set_ratai_varle)
    dfp['ratai'] = dfp['ratai'].apply(set_ratai_pigu)

    df['ratai'] = df['ratai'].apply(make_float)
    dfp['ratai'] = dfp['ratai'].apply(make_float)

    # max
    df_remas_max = df[df['gamintojas'].isin(top3_max)][['kaina', 'gamintojas', 'ratai', 'saltinis']]
    dfp_remas_max = dfp[dfp['gamintojas'].isin(top3_max_p)][['kaina', 'gamintojas', 'ratai', 'saltinis']]
    # mid
    df_remas_mid = df[df['gamintojas'].isin(top3_mid)][['kaina', 'gamintojas', 'ratai', 'saltinis']]
    dfp_remas_mid = dfp[dfp['gamintojas'].isin(top3_mid_p)][['kaina', 'gamintojas', 'ratai', 'saltinis']]
    # min
    df_remas_min = df[df['gamintojas'].isin(top3_min)][['kaina', 'gamintojas', 'ratai', 'saltinis']]
    dfp_remas_min = dfp[dfp['gamintojas'].isin(top3_min_p)][['kaina', 'gamintojas', 'ratai', 'saltinis']]
    # sujungiam
    df_combined_max = pd.concat([df_remas_max, dfp_remas_max]).reset_index()
    df_combined_mid = pd.concat([df_remas_mid, dfp_remas_mid]).reset_index()
    df_combined_min = pd.concat([df_remas_min, dfp_remas_min]).reset_index()


    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_max, x='ratai', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Brangiausių gamintojų kainos pasiskirstymas pagal ratų dydį')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_mid, x='ratai', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Vidutinės gamintojų kainos pasiskirstymas pagal ratų dydį')
    st.pyplot(fig, use_container_width=True)

    fig, ax = plt.subplots()
    sns.boxplot(data=df_combined_min, x='ratai', y='kaina',hue='saltinis', showmeans=True, showfliers=False)
    plt.title('Pigiausių gamintojų kainos pasiskirstymas pagal ratų dydį')
    st.pyplot(fig, use_container_width=True)