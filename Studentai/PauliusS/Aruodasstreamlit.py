import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from matplotlib import ticker

# Nustatomas puslapio dizainas
st.set_page_config(page_icon=':bar_chart:', page_title='Aruodas Analysis', layout='wide')

# Antraštė
st.markdown("<h1 style='text-align: center;'>Aruodas - Webscrap</h1>", unsafe_allow_html=True)

# Prisijungimas prie duomenų bazės
SDB = sqlite3.connect('AruodasBaze4.db')

# Eilutė 1
row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    sql = """SELECT sildymas, AVG(kaina) FROM Aruodas1 GROUP BY sildymas"""
    df = pd.read_sql_query(sql, con=SDB)
    fig, ax = plt.subplots()
    ax.bar(df['sildymas'], df['AVG(kaina)'])
    ax.set_title('Vidutinė kaina pagal šildymo būdą')
    ax.set_xlabel('Šildymas')
    ax.set_ylabel('Vidutinė kaina (EUR)')
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

with row1_col2:
    sql = """SELECT miestas, kaina FROM Aruodas1 WHERE kaina < 730000"""
    df = pd.read_sql_query(sql, con=SDB)
    fig, ax = plt.subplots()
    df.boxplot(column='kaina', by='miestas', ax=ax, grid=True, showfliers=False, showmeans=True)
    ax.set_title('Kainų išsibarstymas pagal miestą')
    ax.set_xlabel('Miestas')
    ax.set_ylabel('Kaina')
    plt.suptitle('')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(fig)

# Eilutė 2
row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    sql = """SELECT miestas, plotas FROM Aruodas1;"""
    df = pd.read_sql_query(sql, con=SDB)
    df['ploto_intervalas'] = df['plotas'].apply(lambda x: 5 * round(x / 5))
    df_iki = df[df['ploto_intervalas'] <= 140]
    grouped_df = df_iki.groupby(['miestas', 'ploto_intervalas']).size().reset_index(name='kiekis')
    pivot_df = grouped_df.pivot(index='ploto_intervalas', columns='miestas', values='kiekis').fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))
    pivot_df.plot(kind='bar', width=1, ax=ax)
    ax.set_xlabel('Ploto intervalas')
    ax.set_ylabel('Kiekis')
    ax.set_title('Plotai pagal miestą ir plotą')
    ax.legend(title='Miestas', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    st.pyplot(fig)

with row2_col2:
    sql = """
    SELECT miestas, rajonas, COUNT(*) as nt_kiekis
    FROM Aruodas1 WHERE miestas = 'Vilniuje'
    GROUP BY rajonas
    ORDER BY nt_kiekis DESC
    """
    df = pd.read_sql_query(sql, con=SDB)
    fig, ax = plt.subplots(figsize=(10, 6))
    df.plot(kind='bar', x='rajonas', y='nt_kiekis', ax=ax)
    ax.set_title('NT objektų kiekis Vilniuje')
    ax.set_xlabel('Rajonas')
    ax.set_ylabel('NT kiekis')
    plt.xticks(rotation=90)
    st.pyplot(fig)

# Eilutė 3
row3_col1, row3_col2 = st.columns(2)
with row3_col1:
    sql = """SELECT tipas, AVG(kaina) FROM Aruodas1 GROUP BY tipas"""
    df = pd.read_sql_query(sql, con=SDB)
    fig, ax = plt.subplots()
    ax.bar(df['tipas'], df['AVG(kaina)'])
    ax.set_title('Vidutinė kaina pagal tipą')
    ax.set_xlabel('Tipas')
    ax.set_ylabel('Vidutinė kaina (EUR)')
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

with row3_col2:
    sql = """SELECT aukstai, aukstas, kaina FROM Aruodas1 WHERE kaina < 730000"""
    df = pd.read_sql_query(sql, con=SDB)
    fig, ax = plt.subplots()
    sns.scatterplot(data=df, x='aukstas', y='kaina', hue='aukstai', ax=ax)
    ax.set_title('Aukštai ir kainos')
    ax.set_xlabel('Aukštas')
    ax.set_ylabel('Kaina (EUR)')
    plt.legend(title='Aukštai', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    st.pyplot(fig)

# Eilutė 4
row4_col1, row4_col2 = st.columns(2)
with row4_col1:
    sql = """SELECT miestas, rajonas, kaina FROM Aruodas1 WHERE miestas LIKE '%Vilniuje%' AND kaina < 730000"""
    df = pd.read_sql_query(sql, con=SDB)
    fig, ax = plt.subplots(figsize=(16, 9))
    df.boxplot(column='kaina', by='rajonas', ax=ax, grid=True, showfliers=False, showmeans=True)
    ax.set_title('Kainų išsibarstymas Vilniuje pagal rajonus')
    ax.set_xlabel('Rajonas')
    ax.set_ylabel('Kaina')
    plt.xticks(rotation=90)
    plt.suptitle('')
    st.pyplot(fig)

with row4_col2:
    sql = """SELECT miestas, rajonas, kaina FROM Aruodas1 WHERE miestas LIKE '%Vilniuje%'"""
    df = pd.read_sql_query(sql, con=SDB)
    top_rajonai = df['rajonas'].value_counts().nlargest(10).index
    df_top_rajonai = df[df['rajonas'].isin(top_rajonai)]
    fig, ax = plt.subplots(figsize=(16, 9))
    df_top_rajonai.boxplot(column='kaina', by='rajonas', ax=ax, grid=True, showfliers=False, showmeans=True)
    ax.set_title('Kainų išsibarstymas top 10 Vilniaus rajonuose')
    plt.xticks(rotation=90)
    plt.suptitle('')
    st.pyplot(fig)

# Paskutinis grafikas per visą lango plotį
sql = """SELECT miestas, rajonas, kaina, plotas FROM Aruodas1 WHERE miestas LIKE '%Vilniuje%'"""
df = pd.read_sql_query(sql, con=SDB)
top_rajonai = df['rajonas'].value_counts().nlargest(5).index
df_duomenys = df[(df['rajonas'].isin(top_rajonai)) & (df['kaina'] < 1000000)]

fig, ax = plt.subplots(figsize=(14, 8))
scatter_plot = sns.scatterplot(data=df_duomenys, x='plotas', y='kaina', hue='rajonas', palette='Set2', s=100, alpha=0.6, ax=ax)
ax.set_title('NT kainų išsibarstymas (top 10 Vilniaus rajonai)')
ax.set_xlabel('Plotas')
ax.set_ylabel('Kaina')
ax.legend(title='Rajonas', bbox_to_anchor=(1.05, 1), loc='upper left')

# Nustatyti Y ašies formatavimą naudojant ScalarFormatter
formatter = ticker.ScalarFormatter(useOffset=False)
formatter.set_scientific(False)
ax.yaxis.set_major_formatter(formatter)
plt.grid(True)
plt.tight_layout()
plt.suptitle('')
st.pyplot(fig)

# Uždarome duomenų bazės ryšį
SDB.close()
