import pandas as pd
import streamlit as st
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.polynomial as poly
import seaborn as sns

db_file_path = r'C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\cars1.db'
conn = sqlite3.connect(db_file_path)

df_cars = pd.read_sql_query("select brand, engine, registration_year, mileage, fuel_type, transmission, price from car_listings", conn)

conn.close()

df = pd.DataFrame(df_cars)

df['mileage_clean'] = df['mileage'].str.replace(' km', '').str.replace(' ', '')
df['mileage_clean'] = pd.to_numeric(df['mileage_clean'], errors='coerce').astype(float)
df['price_clean'] = df['price'].str.replace(' €', '').str.replace(' ', '').astype(float)
df[['engine_size_cm3', 'horsepower_kw']] = df['engine'].str.extract(r'(\d+) cm³.*\((\d+)kW\)').astype(float)

current_year = pd.Timestamp.now().year
df['registration_year_clean'] = pd.to_numeric(df['registration_year'].astype(str).str[:4], errors='coerce')
df['age'] = current_year - df['registration_year_clean']

df = df.dropna()

# Prepare the dataset for model training
features = ['mileage_clean', 'age', 'engine_size_cm3', 'brand', 'fuel_type', 'transmission']
df = pd.get_dummies(df, columns=['brand', 'fuel_type', 'transmission'], drop_first=True)

df['brand'] = df_cars['brand']
df['fuel_type'] = df_cars['fuel_type']
df['transmission'] = df_cars['transmission']

def main():
    st.title("Car Price Prediction")
    
    # User input for car details
    brand = st.selectbox('Select Brand', df['brand'].unique())
    engine_size = st.number_input('Enter Engine Size (in cm³)', min_value=500, max_value=10000, step=100)
    mileage = st.number_input('Enter Mileage (in km)', min_value=0, max_value=500000, step=1000)
    age = st.slider('Select Age of the Car', 0, 30, 5)
    fuel_type = st.selectbox('Select Fuel Type', df['fuel_type'].unique())
    transmission = st.selectbox('Select Transmission', df['transmission'].unique())
    
    # the average of all 6 components
    price_mileage = df['price_clean'].mean() * (1 - mileage / df['mileage_clean'].max())
    price_age = df['price_clean'].mean() * (1 - age / df['age'].max())
    price_engine_size = df['price_clean'].mean() * (engine_size / df['engine_size_cm3'].max())
    price_brand = df[df['brand'] == brand]['price_clean'].mean() if brand in df['brand'].unique() else df['price_clean'].mean()
    price_fuel_type = df[df['fuel_type'] == fuel_type]['price_clean'].mean() if fuel_type in df['fuel_type'].unique() else df['price_clean'].mean()
    price_transmission = df[df['transmission'] == transmission]['price_clean'].mean() if transmission in df['transmission'].unique() else df['price_clean'].mean()
    
    predicted_price = (price_mileage + price_age + price_engine_size + price_brand + price_fuel_type + price_transmission) / 6
    
    if st.button('Predict Price'):
        st.success(f"Predicted Price: {predicted_price:.2f} €")


    
    demo = df[['mileage_clean', 'price_clean']]
    demo.dropna(inplace=True)
    demo['mileage_clean'] = np.ceil(demo['mileage_clean'].values/5000.0)*5000.0
    demogr = demo.groupby('mileage_clean').mean(numeric_only=True).reset_index()
    DM2 = demogr.query(expr='mileage_clean < 500000')
    
    st.header("Polynomial Fit Plots for Features vs Price")
    features_to_plot = ['age', 'engine_size_cm3']
    feature_names = [ 'Age', 'Engine Size']
    coef = np.polyfit(x=DM2['mileage_clean'], y=DM2['price_clean'], deg=3)

    fn_fit = poly.Polynomial(coef[::-1])
    kainos_fitted = fn_fit(DM2['mileage_clean'])
    DM2['K_fit'] = kainos_fitted
    plt.figure(figsize=(10, 6))
    ax = sns.regplot(data=DM2, x='mileage_clean', y='price_clean', order=3)
    ax.scatter(x=DM2['mileage_clean'][::10], y=DM2['K_fit'][::10], c='red')
    
    st.pyplot(plt)
    for feature, feature_name in zip(features_to_plot, feature_names):
        coef = np.polyfit(x=df[feature], y=df['price_clean'], deg=3)
        fn_fit = poly.Polynomial(coef[::-1])
        kainos_fitted = fn_fit(df[feature])
        df['K_fit'] = kainos_fitted

        plt.figure(figsize=(10, 6))
        ax = sns.regplot(data=df, x=feature, y='price_clean', order=3, scatter_kws={'color': 'blue'}, line_kws={'color': 'green'})
        ax.scatter(x=df[feature][::10], y=df['K_fit'][::10], c='red', label='Polynomial Fit Points')
        plt.xlabel(feature_name)
        plt.ylabel('Price (€)')
        plt.title(f'Polynomial Fit: {feature_name} vs Price')
        plt.legend()
        st.pyplot(plt)
        plt.close()

        
    st.header("Histograms for Brand, Fuel Type, and Transmission vs Price")
    categorical_features = ['brand', 'fuel_type', 'transmission']
    for feature in categorical_features:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=feature, y='price_clean', bins=30, kde=True)
        plt.xlabel(feature.capitalize())
        plt.ylabel('Price (€)')
        plt.title(f'Histogram: {feature.capitalize()} vs Price')
        plt.xticks(rotation=45)
        st.pyplot(plt)
        plt.close()


if __name__ == "__main__":
    main()
