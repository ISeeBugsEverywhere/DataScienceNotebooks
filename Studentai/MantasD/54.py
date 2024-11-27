import streamlit as st
import pandas as pd
from Skriptai.manofunkcijos import *
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
st.set_page_config(page_icon=':bar_chart', page_title='Kainos skaičiuoklė', layout='wide')
def turis(x):
    if x != None:
        if 'cm³' in x:
            return float(x.replace(' cm³',''))
        
def galia(x):
    if x != None:
        if 'kW' in x:
            return float(x.split('(')[1].replace('kW)', ''))


db_path = '../../../web_scrap.db'
query = 'SELECT * FROM autopliuslt2;'  
df_auto = query_to_dataframe(db_path,query)
df_auto['JS']= df_auto['Kaina'].apply(lambda x: float(x)*1.5)
df_auto['Kaina']= df_auto['Kaina'].apply(lambda x: float(x))
df_auto['Rida'] = df_auto['Rida'].apply(lambda x: int(x.replace(' ','').replace('km','')) if x != None else x)
df_auto['Amzius'] = df_auto['Pirma registracija'].apply(lambda x: 2024-int(x[:4]) if x != None else x)
df_auto['Turis'] = df_auto['Variklis'].apply(lambda x: x.split(',')[0] if x != None else None)
df_auto['Turis'] = df_auto['Turis'].apply(turis)
df_auto['Galia'] = df_auto['Variklis'].apply(galia)
df_auto['Miestas'] = df_auto['Miestas'].apply(lambda x: x.split(',')[0])
df_auto['Baterijos talpa, kWh'] = df_auto['Baterijos talpa, kWh'].apply(lambda x: float(x.replace(' kWh','')) if x != None else x)
df_auto['Elektra nuvažiuojamas atstumas'] = df_auto['Elektra nuvažiuojamas atstumas'].apply(lambda x: float(x.replace(' km','')) if x != None else x)
df_auto['Rida_group'] = df_auto['Rida'].apply(lambda x: np.ceil(x/5000)*5000 if x != None else x )
df_auto = df_auto[df_auto['Pavarų dėžė'] != 'Oldsmobile']
df = df_auto[df_auto['Rida'].notna()  & df_auto['Galia'].notna() & df_auto['Amzius'].notna() ][['Markė', 'Modelis', 'Kuro tipas', 'Rida', 'Amzius', 'Galia', 'Baterijos talpa, kWh','Elektra nuvažiuojamas atstumas',  'Kaina', 'Kėbulo tipas', 'Pavarų dėžė','Miestas']]


df2 = pd.read_csv('C:/Users/manta/OneDrive/Dokumentai/Python projektai/atlyginimai.csv', delimiter=',')
df_new = df2
city_dict = {
    'Rokiškio': 'Rokiškis',
    'Šilutės': 'Šilutė',
    'Molėtų': 'Molėtai',
    'Plungės': 'Plungė',
    'Visagino': 'Visaginas',
    'Vilniaus': 'Vilnius',
    'Kalvarijos': 'Kalvarija',
    'Akmenės': 'Akmenė',
    'Lazdijų': 'Lazdijai',
    'Palangos': 'Palanga',
    'Kėdainių': 'Kėdainiai',
    'Kretingos': 'Kretinga',
    'Kazlų': 'Kazlų Rūda',
    'Marijampolės': 'Marijampolė',
    'Vilkaviškio': 'Vilkaviškis',
    'Kauno': 'Kaunas',
    'Mažeikių': 'Mažeikiai',
    'Jonavos': 'Jonava',
    'Utenos': 'Utena',
    'Neringos': 'Neringa',
    'Kelmės': 'Kelmė',
    'Kaišiadorių': 'Kaišiadorys',
    'Šiaulių': 'Šiauliai',
    'Raseinių': 'Raseiniai',
    'Birštono': 'Birštonas',
    'Širvintų': 'Širvintos',
    'Skuodo': 'Skuodas',
    'Ukmergės': 'Ukmergė',
    'Radviliškio': 'Radviliškis',
    'Kupiškio': 'Kupiškis',
    'Alytaus': 'Alytus',
    'Šakių': 'Šakiai',
    'Pagėgių': 'Pagėgiai',
    'Prienų': 'Prienai',
    'Zarasų': 'Zarasai',
    'Trakų': 'Trakai',
    'Pasvalio': 'Pasvalys',
    'Ignalinos': 'Ignalina',
    'Telšių': 'Telšiai',
    'Šalčininkų': 'Šalčininkai',
    'Pakruojo': 'Pakruojis',
    'Šilalės': 'Šilalė',
    'Rietavo': 'Rietavas',
    'Biržų': 'Biržai',
    'Tauragės': 'Tauragė',
    'Anykščių': 'Anykščiai',
    'Elektrėnų': 'Elektrėnai',
    'Druskininkų': 'Druskininkai',
    'Švenčionių': 'Švenčionys',
    'Joniškio': 'Joniškis',
    'Jurbarko': 'Jurbarkas',
    'Klaipėdos':'Klaipėda',
    'Varėnos':'Varėna',
    'Panevėžio':'Panevėžys'
}
def change_city(x):
    x = x.replace('\xa0', ' ')
    m = x.split()[0]
    if m in city_dict.keys():
        return city_dict[m]

df_miestai = df_new[df_new['sort'] != 'None'][1:]
df_miestai['Miestas'] = df_miestai['sort'].apply(change_city)
df_miestai = df_miestai[['Miestas', 'Neto, EUR']]
# st.dataframe(df_miestai)

df = pd.merge(df, df_miestai, how='left', on='Miestas')
df['Neto, EUR'] = df['Neto, EUR'].apply(lambda x: str(x).replace(' ','') if x != None else x)
df['Neto, EUR'] = df['Neto, EUR'].apply(lambda x: x.replace(',','.') if x != None else x)
df['Neto, EUR'] = df['Neto, EUR'].apply(lambda x: float(x) if x != None else x)
# st.dataframe(df)
st.title("Automobilio kainos skaičiuoklė")

filtered_df = df.copy()

option1 = st.selectbox(
    "Markė:",
    options=['Visos'] + list(df['Markė'].unique())
)

if option1 != 'Visos':
    filtered_df = filtered_df[filtered_df['Markė'] == option1]

if option1 != 'Visos':
    option2 = st.selectbox(
        "Modelis:",
        options=['Visi'] + list(filtered_df['Modelis'].unique())
    )

    if option2 != 'Visi':
        filtered_df = filtered_df[filtered_df['Modelis'] == option2]
        
option3 = st.selectbox(
    "Kuro tipas:",
    options=['Visi'] + list(df['Kuro tipas'].unique())
)

if option3 != 'Visi':
    filtered_df = filtered_df[filtered_df['Kuro tipas'] == option3]

# Jai parinkta elektra
if option3 == 'Elektra':
    # Baterijos talpos parinkimas
    talpa_min, talpa_max = st.slider(
    "Pasirinkite baterijos talpos intervalą:",
    min_value=int(filtered_df['Baterijos talpa, kWh'].min()),
    max_value=int(filtered_df['Baterijos talpa, kWh'].max()),
    value=(int(filtered_df['Baterijos talpa, kWh'].min()), int(filtered_df['Baterijos talpa, kWh'].max()))
    )
    if talpa_min == talpa_max:
        talpa_max = talpa_min + 1

    filtered_df = filtered_df[
    (filtered_df['Baterijos talpa, kWh'] >= talpa_min) & (filtered_df['Baterijos talpa, kWh'] <= talpa_max)
    ]
    # Nuvažiuojamo atstumo parinkimas
    ats_min, ats_max = st.slider(
    "Pasirinkite nuvažiuojamo atstumo intervalą:",
    min_value=int(filtered_df['Elektra nuvažiuojamas atstumas'].min()),
    max_value=int(filtered_df['Elektra nuvažiuojamas atstumas'].max()),
    value=(int(filtered_df['Elektra nuvažiuojamas atstumas'].min()), int(filtered_df['Elektra nuvažiuojamas atstumas'].max()))
    )
    if ats_min == ats_max:
        ats_max = ats_min + 10

    filtered_df = filtered_df[
    (filtered_df['Elektra nuvažiuojamas atstumas'] >= ats_min) & (filtered_df['Elektra nuvažiuojamas atstumas'] <= ats_max)
    ]


option4 = st.selectbox(
    'Kėbulo tipas:',
    options=['Visi'] + list(df['Kėbulo tipas'].unique())
)

if option4 != 'Visi':
    filtered_df = filtered_df[filtered_df['Kėbulo tipas'] == option4]


option5 = st.selectbox(
    'Pavarų dėžė:',
    options=['Visos'] + list(df['Pavarų dėžė'].unique())
)

if option5 != 'Visos':
    filtered_df = filtered_df[filtered_df['Pavarų dėžė'] == option5]

# Amžius
col1, col2 = st.columns(2)

with col1:
    min_value = st.number_input(
        "Amžius nuo:",
        min_value=int(df['Amzius'].min()),
        max_value=int(df['Amzius'].max()),
        value=int(df['Amzius'].min())
    )

with col2:
    max_value = st.number_input(
        "Amžius iki:",
        min_value=int(df['Amzius'].min()),
        max_value=int(df['Amzius'].max()),
        value=int(df['Amzius'].max())
    )

filtered_df = filtered_df[
    (filtered_df['Amzius'] >= min_value) & (filtered_df['Amzius'] <= max_value)
]

# Galia
col3, col4 = st.columns(2)

with col3:
    min_power = st.number_input(
        "Galia nuo:",
        min_value=int(df['Galia'].min()),
        max_value=int(df['Galia'].max()),
        value=int(df['Galia'].min())
    )

with col4:
    max_power = st.number_input(
        "Galia iki:",
        min_value=int(df['Galia'].min()),
        max_value=int(df['Galia'].max()),
        value=int(df['Galia'].max())
    )

filtered_df = filtered_df[
    (filtered_df['Galia'] >= min_power) & (filtered_df['Galia'] <= max_power)
]


# Rida
rida_min, rida_max = st.slider(
    "Pasirinkite ridos intervalą",
    min_value=int(filtered_df['Rida'].min()),
    max_value=int(filtered_df['Rida'].max()),
    value=(int(filtered_df['Rida'].min()), int(filtered_df['Rida'].max()))
)

if rida_min == rida_max:
    rida_max = rida_min + 1000

filtered_df = filtered_df[
    (filtered_df['Rida'] >= rida_min) & (filtered_df['Rida'] <= rida_max)
]

amzius = round(sum(list(filtered_df['Amzius']))/len(list(filtered_df['Amzius'])),0)
rida = round(sum(list(filtered_df['Rida']))/len(list(filtered_df['Rida'])),0)
galia = round(sum(list(filtered_df['Galia']))/len(list(filtered_df['Galia'])),0)

X = filtered_df[['Amzius', 'Rida','Galia']].values  
y = filtered_df['Kaina'].values 

if len(X) > 1:
    degree = 1  
    coeffs = np.polyfit(X.T[0], y, degree) 

    filtered_df['Apskaičiuota_Kaina'] = np.polyval(coeffs, X.T[0])

    predicted_price = np.polyval(coeffs, np.array([amzius, rida, galia]))
else:
    st.warning("Norint apskaičiuoti kainą reikia daugiau duomenų pagal pasirinktus filtrus.")
    predicted_price = None

st.write("Filtruoti duomenys su apskaičiuota kaina pagal polinomą:")
st.dataframe(filtered_df)

if predicted_price is not None:
    st.subheader(f"Numatoma kaina pagal nustatytus kriterijus (Amžius: {amzius}, Rida: {rida}:, Galia: {galia})")
    if isinstance(predicted_price, np.ndarray):
        predicted_price = predicted_price[0]

    st.subheader(f"Prognozuojama kaina: {predicted_price:.0f} EUR")

    variables = ['Amzius', 'Rida', 'Galia']
    titles = ["Kaina pagal Amžių", "Kaina pagal Ridą", "Kaina pagal Galią"]
    values = [amzius, rida, galia]

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    for i, var in enumerate(variables):
        x = filtered_df[var]
        y = filtered_df['Kaina']
        
        coeffs = np.polyfit(x, y, 1) 
        x_pred = np.linspace(x.min(), x.max(), 100)
        y_pred = np.polyval(coeffs, x_pred)
        
        axs[i].scatter(x, y, color='blue', label="Esami duomenys")
        axs[i].plot(x_pred, y_pred, color='red', label="1-ojo laipsnio polinomas")
        
        axs[i].scatter(values[i], predicted_price, color='green', s=100, zorder=5, label="Numatoma kaina")
        
        axs[i].set_title(titles[i])
        axs[i].set_xlabel(var)
        axs[i].set_ylabel("Kaina")
        axs[i].legend()
    st.pyplot(fig)
    
figure, ax = plt.subplots( figsize=(18, 5))    
x = filtered_df.corr(numeric_only=True)
ax = sns.heatmap(data=x,annot=True)
st.pyplot(figure)





# Kita logika


ndf = df.copy()
ndf = ndf[ndf['Neto, EUR'].notna()]
options1 = st.multiselect(
    "Markės:",
    options=list(ndf['Markė'].unique())
)
fil_df = ndf[ndf['Markė'].isin(options1)]

options2 = st.multiselect(
    "Modeliai:",
    options=list(fil_df['Modelis'].unique())
)
fil_df = ndf[ndf['Modelis'].isin(options2)]
fil_df['Mašina'] = fil_df['Markė']+' '+fil_df['Modelis']
st.dataframe(fil_df)

dfx = fil_df.groupby(['Miestas', 'Mašina'])[['Kaina','Neto, EUR']].mean().reset_index().sort_values(by='Neto, EUR', ascending=True)
st.dataframe(dfx)

figure2, ax = plt.subplots( figsize=(18, 5))    
ax = sns.lineplot(data=dfx,x='Miestas', y='Kaina', hue='Mašina')
plt.xticks(rotation = 90)
st.pyplot(figure2)

figure3, ax = plt.subplots( figsize=(18, 5))    
x = dfx.corr(numeric_only=True)
ax = sns.heatmap(data=x,annot=True)
st.pyplot(figure3)