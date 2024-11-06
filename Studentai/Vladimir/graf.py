import sqlite3
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil import parser
conn = sqlite3.connect('cars1.db')
df = pd.read_sql_query("SELECT * FROM car_listings", conn)
conn.close()
df = df.drop_duplicates()

def clean_and_convert(column, unit):
    return pd.to_numeric(
        df[column].str.replace(unit, '', regex=True).str.replace(' ', ''), 
        errors='coerce'
    )


df['price'] = clean_and_convert('price', '€')
df['mileage'] = clean_and_convert('mileage', 'km')


df = df.dropna(subset=['price', 'mileage'])


def extract_year(date_str):
    try:
        return parser.parse(date_str).year
    except (ValueError, TypeError):
        return None

df['registration_year'] = df['registration_year'].apply(extract_year).astype('Int64')
df = df.dropna(subset=['registration_year'])

# Calculate the car's age
current_year = datetime.now().year
df['age'] = current_year - df['registration_year']


df['kw'] = df['engine'].str.extract(r'\((\d+)kW\)')

df['kw'] = pd.to_numeric(df['kw'], errors='coerce')

df = df.dropna(subset=['kw', 'price'])
# Convert price to float
# df['price'] = pd.to_numeric(df['price'].str.replace('€', '').str.replace(' ', ''), errors='coerce')
# df = df.dropna(subset=['price'])
st.title("Car Listings Analysis")
st.dataframe(df)
# Streamlit interface
st.title("Car Price vs. Age Analysis")

st.write("This visualization shows how car prices are affected by the vehicle's age.")

# Plot: Price vs Age
fig, ax = plt.subplots()
ax.scatter(df['age'], df['price'], alpha=0.5)
ax.set_xlabel('Car Age (Years)')
ax.set_ylabel('Price (€)')
ax.set_title('Car Price vs Age')


st.pyplot(fig)





st.subheader("Price vs Mileage Scatter Plot")
fig, ax = plt.subplots()
ax.scatter(df['price'], df['mileage'], alpha=0.5)
ax.set_title('Price vs Mileage')
ax.set_xlabel('Mileage (km)')
ax.set_ylabel('Price (€)')
st.pyplot(fig)




st.title("Car Price vs. Engine Power")

st.write("This plot shows how car prices are influenced by engine power (kW).")

# Plot: Price vs Engine Power
fig, ax = plt.subplots()
ax.scatter(df['kw'], df['price'], alpha=0.5)
ax.set_xlabel('Engine Power (kW)')
ax.set_ylabel('Price (€)')
ax.set_title('Car Price vs Engine Power')


st.pyplot(fig)

# Plot : Price vs Body type
st.subheader("Price vs Body Type Scatter Plot")
fig, ax = plt.subplots()
ax.scatter(df['price'], df['body_type'], alpha=0.5)
ax.set_title('Price vs Body Type')
ax.set_xlabel('Price (€)')
ax.set_ylabel('Body Type')
st.pyplot(fig)

df['transmission'] = df['transmission'].str.strip().str.lower()
valid_transmissions = ['mechaninė', 'automatinė']
df = df[df['transmission'].isin(valid_transmissions)]

st.subheader("Price vs Transmission Scatter Plot")
fig, ax = plt.subplots()
ax.scatter(df['price'], df['transmission'], alpha=0.5)
ax.set_title('Price vs Transmission')
ax.set_xlabel('Price (€)')
ax.set_ylabel('Transmission')
st.pyplot(fig)


st.subheader("Price vs Location Scatter Plot")
fig, ax = plt.subplots()
ax.scatter(df['location'], df['price'], alpha=0.5)
plt.xticks(rotation=45)
ax.set_title('Price vs Location')
ax.set_xlabel('Location')
ax.set_ylabel('Price (€)')
st.pyplot(fig)


df['tech_check'] = df['tech_check'].astype(str).str[4:].str.strip()
df = df[df['tech_check'] != '']
df['tech_check'] = df['tech_check'].astype(int)

df['has_tech_check'] = df['tech_check'].notnull()
tech_check_yes = df[df['has_tech_check'] == True].shape[0]
tech_check_no = df[df['has_tech_check'] == False].shape[0]


st.subheader("Price vs TC Scatter Plot")
fig, ax = plt.subplots()
ax.scatter(df['price'], df['tech_check'], alpha=0.5)
ax.set_title('Price vs TC')
ax.set_xlabel('Price (€)')
ax.set_ylabel('TC')
st.pyplot(fig)




df['has_tech_check'] = df['tech_check'].notna().astype(int)


df = df.dropna(subset=['price'])


avg_price_with_ta = df[df['has_tech_check'] == 1]['price'].mean()
avg_price_without_ta = df[df['has_tech_check'] == 0]['price'].mean()


st.subheader("Impact of Technical Check (TA) on Car Prices")
st.write(f"Average price with TA: €{avg_price_with_ta:.2f}")
st.write(f"Average price without TA: €{avg_price_without_ta:.2f}")


fig, ax = plt.subplots()
ax.bar(['With TA', 'Without TA'], [avg_price_with_ta, avg_price_without_ta], color=['green', 'red'])
ax.set_title('Average Price by Technical Check Status')
ax.set_ylabel('Average Price (€)')


st.pyplot(fig)



top_10_brands = df['brand'].value_counts().head(10).index
df_top_brands = df[df['brand'].isin(top_10_brands)]

avg_price_per_mileage = df_top_brands.groupby('brand').apply(lambda x: x['price'].mean() / x['mileage'].mean())

st.write("Average Price per Mileage for Top 10 Brands:")
st.write(avg_price_per_mileage)

fig, ax = plt.subplots(figsize=(10, 6))
avg_price_per_mileage.plot(kind='bar', ax=ax)
ax.set_title('Average Price per Mileage for Top 10 Brands')
ax.set_xlabel('Brand')
ax.set_ylabel('Average Price per Mileage (€ per km)')
st.pyplot(fig)


df_top_10_brands = df[df['brand'].isin(top_10_brands)]


st.subheader("Impact of Age on Price for Top 10 Most Popular Brands")
fig, ax = plt.subplots()
ax.scatter(df_top_10_brands['age'], df_top_10_brands['price'], alpha=0.5)
ax.set_title('Price vs Age for Top 10 Most Popular Brands')
ax.set_xlabel('Age (years)')
ax.set_ylabel('Price (€)')
st.pyplot(fig)


df_top_10_brands = df[df['brand'].isin(top_10_brands)]

# Create a scatter plot for KW vs Price
st.subheader("Impact of KW on Price for Top 10 Most Popular Brands")
fig, ax = plt.subplots()
ax.scatter(df_top_10_brands['kw'], df_top_10_brands['price'], alpha=0.5)
ax.set_title('KW vs Price for Top 10 Most Popular Brands')
ax.set_xlabel('KW')
ax.set_ylabel('Price (€)')
st.pyplot(fig)


correlations = df.groupby('brand').apply(lambda x: x[['price', 'mileage', 'age']].corr().iloc[0, 1:])
price_vs_mileage_corr = correlations['mileage']
price_vs_age_corr = correlations['age']


fastest_depreciation = price_vs_age_corr.idxmin()
best_value_retention = price_vs_age_corr.idxmax()


price_variation = df.groupby('brand')['price'].std()
most_variable_brand = price_variation.idxmax()


st.title("Car Value Retention and Price Variation Analysis")
st.write(f"**Fastest Depreciating Brand:** {fastest_depreciation}")
st.write(f"**Best Value Retention Brand:** {best_value_retention}")
st.write(f"**Most Variable Prices:** {most_variable_brand}")

# Plot: Price Variation by Brand
st.subheader("Price Variation by Brand")
fig, ax = plt.subplots(figsize=(10, 5))
price_variation.plot(kind='bar', ax=ax)
ax.set_title('Price Variation by Brand (Standard Deviation)')
ax.set_ylabel('Price Variation (Standard Deviation)')
plt.xticks(rotation=45)
st.pyplot(fig)




top_10_brands = df['brand'].value_counts().head(10).index


df_top_brands = df[df['brand'].isin(top_10_brands)]


correlations = df_top_brands.groupby('brand').apply(
    lambda x: x[['price', 'mileage', 'age']].corr().iloc[0, 1:]
)
price_vs_mileage_corr = correlations['mileage']
price_vs_age_corr = correlations['age']


fastest_depreciation = price_vs_age_corr.idxmin()
best_value_retention = price_vs_age_corr.idxmax()


price_variation = df_top_brands.groupby('brand')['price'].std()
most_variable_brand = price_variation.idxmax()


st.title("Top 10 Brands: Value Retention and Price Variation")
st.write(f"**Fastest Depreciating Brand:** {fastest_depreciation}")
st.write(f"**Best Value Retention Brand:** {best_value_retention}")
st.write(f"**Most Variable Prices:** {most_variable_brand}")


fig, ax = plt.subplots(figsize=(10, 5))
price_variation.plot(kind='bar', ax=ax)
ax.set_title('Price Variation by Brand (Standard Deviation)')
ax.set_ylabel('Price Variation (Standard Deviation)')
plt.xticks(rotation=45)
st.pyplot(fig)



brand_counts = df['brand'].value_counts()
rare_brands = brand_counts[(brand_counts > 5) & (brand_counts < 15)].index
df_rare_brands = df[df['brand'].isin(rare_brands)]

if not rare_brands.empty:
    st.title("Rare Car Brands (5 < x < 15 Listings)")
    st.write(df_rare_brands['brand'].value_counts())

    st.dataframe(df_rare_brands)


st.subheader("Price Distribution of Rare Car Brands")
fig, ax = plt.subplots()
df_rare_brands.boxplot(column='price', by='brand', ax=ax)
ax.set_title('Price Distribution by Rare Car Brands')
ax.set_xlabel('Brand')
ax.set_ylabel('Price (€)')
st.pyplot(fig)


top_10_brands = df['brand'].value_counts().head(10).index


df_top_brands = df[df['brand'].isin(top_10_brands)]


st.header("Engine Power Distribution for Top 10 Popular Brands")


fig, ax = plt.subplots(figsize=(12, 6))
df_top_brands.boxplot(column='kw', by='brand', ax=ax, showfliers=False)
means = df_top_brands.groupby('brand')['kw'].mean()
means.plot(style='ro', markersize=5, ax=ax, label='Mean (Vidurkis)')
ax.set_title('Distribution of Engine Power (kW) by Brand')
ax.set_xlabel('Brand')
ax.set_ylabel('Engine Power (kW)')
plt.suptitle('')  
plt.xticks(rotation=45)

st.pyplot(fig)


top_10_brands = df['brand'].value_counts().head(10).index

df_top_brands = df[df['brand'].isin(top_10_brands)]
print(top_10_brands)
print(df_top_brands)
st.header("Mileage Distribution for Top 10 Popular Brands")

fig, ax = plt.subplots(figsize=(12, 6))
df_top_brands.boxplot(column='mileage', by='brand', ax=ax, showfliers=False)
means = df_top_brands.groupby('brand')['mileage'].mean().reindex(top_10_brands)
means.plot(style='ro', markersize=5, ax=ax, label='Mean (Vidurkis)')

ax.set_title('Mileage Distribution by Brand (Top 10 Brands)')
ax.set_xlabel('Brand')
ax.set_ylabel('Mileage (km)')
plt.suptitle('')  
plt.xticks(rotation=45)

st.pyplot(fig)


top_10_brands = df['brand'].value_counts().head(10).index


df_top_brands = df[df['brand'].isin(top_10_brands)]

st.title("Age Distribution for Top 10 Popular Car Brands")

 
fig, ax = plt.subplots(figsize=(12, 6))
df_top_brands.boxplot(column='age', by='brand', ax=ax, showfliers=False)


means = df_top_brands.groupby('brand')['age'].mean()
means.plot(style='ro', markersize=5, ax=ax, label='Mean (Vidurkis)')


ax.set_title('Age Distribution by Brand (Top 10 Brands)')
ax.set_xlabel('Brand')
ax.set_ylabel('Age (Years)')
plt.suptitle('')  
plt.xticks(rotation=45)  

st.pyplot(fig)


valid_fuel_types = ['elektra', 'benzinas-elektra', 'dujos-elektra', 'benzinas-dujos-elektra', 'dizelinas-elektra']
pattern = '|'.join(valid_fuel_types)
df_electric = df[df['fuel_type'].str.contains(pattern, case=False, na=False)]


df_electric = df_electric.dropna(subset=['price', 'kw'])


correlation = df_electric['price'].corr(df_electric['kw'])


st.title("Price vs Electric Motor Power (kW)")
st.write(f"Correlation between Price and kW: {correlation:.2f}")

# Plot: Price vs kW
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df_electric['kw'], df_electric['price'], alpha=0.6)
ax.set_title('Price vs Electric Motor Power (kW)')
ax.set_xlabel('Motor Power (kW)')
ax.set_ylabel('Price (€)')
st.pyplot(fig)



valid_fuel_types = ['elektra', 'benzinas-elektra', 'dujos-elektra', 'benzinas-dujos-elektra', 'dizelinas-elektra']
pattern = '|'.join(valid_fuel_types)
df_electric = df[df['fuel_type'].str.contains(pattern, case=False, na=False)]


df_electric = df_electric.dropna(subset=['price', 'age'])


st.header("Electric Vehicle Depreciation Rate")

# Scatter plot: Price vs Age (Depreciation trend)
fig, ax = plt.subplots(figsize=(10, 5))
ax.scatter(df_electric['age'], df_electric['price'], alpha=0.6)
ax.set_title('Depreciation of Electric Vehicles: Price vs Age')
ax.set_xlabel('Age (Years)')
ax.set_ylabel('Price (€)')

st.pyplot(fig)

correlation = df_electric['price'].corr(df_electric['age'])
st.write(f"Correlation between Age and Price: {correlation:.2f}")


grouped_data = df_electric.groupby(['brand', 'age'])['price'].median().reset_index()


st.header("Electric Vehicle Depreciation by Brand (Boxplot)")


fig, ax = plt.subplots(figsize=(12, 6))
grouped_data.boxplot(column='price', by='brand', ax=ax, showfliers=False)


ax.set_title('Depreciation of Electric Vehicles by Brand (Boxplot)')
ax.set_xlabel('Brand')
ax.set_ylabel('Price (€)')
plt.suptitle('')  
plt.xticks(rotation=45)

st.pyplot(fig)

