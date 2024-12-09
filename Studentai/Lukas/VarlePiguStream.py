import streamlit as st
import seaborn as sns
import pandas as pd
import numpy as np
# import plotly.express as px
import mysql.connector as cnt
import matplotlib.pyplot as plt
import sqlite3

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
    st.write('Labiausiai tikėtina dronas Varle.lt')
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
    
    # top 15
    SDB = sqlite3.connect('VarlePigu.db')
    C = SDB.cursor()
    sql="""select kaina,
    gamintojas
    from PlanseteVarle;"""
    df = pd.read_sql_query(sql, con=SDB)

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
    df_brand = df_gamintojas[df_gamintojas['gamintojas'].isin(top_brands)]
    df_brand.head()
    fig, axis = plt.subplots()
    sns.boxplot(data=df_brand, x='gamintojas', y='kaina', showmeans=True, showfliers=False)
    plt.tick_params(axis='x', rotation=90)
    plt.title('Top gamintojai kainos pasiskirstymas (Varle.lt)')
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



        
if selected_option == 'Televizoriai':
    st.write('Informacija ruošiama')
if selected_option == 'Dviračiai':
    st.write('Informacija ruošiama')