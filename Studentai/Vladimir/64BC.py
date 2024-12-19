import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\piguBicyclesI.csv")



tab1, tab2 = st.tabs(["Plots for Bicycles", "Plots for Fridges"])


col1, col2 = st.columns(2)

with tab1:
    with col1:

        st.title('Bicycles Pigu Analysis')

        # df['Ratų skersmuo:'] = df['Ratų skersmuo:'].str.replace('"','')
        # df['price'] = pd.to_numeric(df['price'], errors='coerce')
        # df['Ratų skersmuo:'] = pd.to_numeric(df['Ratų skersmuo:'], errors='coerce')



        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df['Ratų skersmuo:'] = df['Ratų skersmuo:'].str.replace('"', '').str.strip(',')
        df['Ratų skersmuo:'] = pd.to_numeric(df['Ratų skersmuo:'], errors='coerce')
        df['Pavarų skaičius:'] = pd.to_numeric(df['Pavarų skaičius:'], errors='coerce')
        df['Rėmas:'] = df['Rėmas:'].fillna("Nenurodyta")

        
        manufacturer_counts = df['brand'].value_counts()
        filtered_df = df[df['brand'].isin(manufacturer_counts[manufacturer_counts > 2].index)]

        
        top_3_expensive = filtered_df.groupby('brand')['price'].mean().nlargest(3)
        middle_3 = filtered_df.groupby('brand')['price'].mean().sort_values().iloc[len(filtered_df.groupby('brand')['price'].mean()) // 2 - 1:len(filtered_df.groupby('brand')['price'].mean()) // 2 + 2]
        cheapest_3 = filtered_df.groupby('brand')['price'].mean().nsmallest(3)

       
        st.subheader("Price Distribution by Brand")
        fig, ax = plt.subplots(figsize=(10, 6))
        filtered_df.groupby('brand')['price'].mean().sort_values().plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title("Average Price by Brand")
        ax.set_xlabel("Brand")
        ax.set_ylabel("Average Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        
        st.subheader("Top 3 Most Expensive Brands")
        fig, ax = plt.subplots(figsize=(10, 6))
        top_3_expensive.plot(kind='bar', color='purple', ax=ax)
        ax.set_title("Top 3 Most Expensive Brands")
        ax.set_xlabel("Brand")
        ax.set_ylabel("Average Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        
        st.subheader("Middle 3 Brands")
        fig, ax = plt.subplots(figsize=(10, 6))
        middle_3.plot(kind='bar', color='yellow', ax=ax)
        ax.set_title("Middle 3 Brands")
        ax.set_xlabel("Brand")
        ax.set_ylabel("Average Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        
        st.subheader("Top 3 Cheapest Brands")
        fig, ax = plt.subplots(figsize=(10, 6))
        cheapest_3.plot(kind='bar', color='brown', ax=ax)
        ax.set_title("Top 3 Cheapest Brands")
        ax.set_xlabel("Brand")
        ax.set_ylabel("Average Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        
        st.subheader("Price Dependency on Frame Material")
        fig, ax = plt.subplots(figsize=(10, 6))
        filtered_df.groupby('Rėmas:')['price'].mean().plot(kind='bar', color='purple', ax=ax)
        ax.set_title("Price Dependency on Frame Material")
        ax.set_xlabel("Frame Material")
        ax.set_ylabel("Average Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        
        st.subheader("Price Dependency on Wheel Diameter")
        fig, ax = plt.subplots(figsize=(10, 6))
        filtered_df.groupby('Ratų skersmuo:')['price'].mean().plot(kind='line', marker='o', color='green', ax=ax)
        ax.set_title("Price Dependency on Wheel Diameter")
        ax.set_xlabel("Wheel Diameter (inches)")
        ax.set_ylabel("Average Price (€)")
        st.pyplot(fig)

        
        st.subheader("Price Dependency on Number of Gears")
        fig, ax = plt.subplots(figsize=(10, 6))
        filtered_df.groupby('Pavarų skaičius:')['price'].mean().plot(kind='bar', color='blue', ax=ax)
        ax.set_title("Price Dependency on Number of Gears")
        ax.set_xlabel("Number of Gears")
        ax.set_ylabel("Average Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)



        
        st.subheader("Price Dependency on Type")
        fig, ax = plt.subplots(figsize=(10, 6))
        filtered_df.groupby('Rūšis:')['price'].mean().plot(kind='bar', color='pink', ax=ax)
        ax.set_title("Price Dependency on Bicycle Type")
        ax.set_xlabel("Type")
        ax.set_ylabel("Average Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        
        st.subheader("Price Dependency on Purpose")
        fig, ax = plt.subplots(figsize=(10, 6))
        filtered_df.groupby('Skirta:')['price'].mean().plot(kind='bar', color='cyan', ax=ax)
        ax.set_title("Price Dependency on Purpose")
        ax.set_xlabel("Purpose")
        ax.set_ylabel("Average Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)



    with col2:

            st.title('Bicycles Varle Analysis')


            dfI = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\varleBicyclesI.csv")


            dfI['price'] = pd.to_numeric(dfI['price'], errors='coerce')
            dfI['Combined_skersmuo'] = dfI['Combined_skersmuo'].str.split(' ').str[0]
            dfI['Combined_skersmuo'] = pd.to_numeric(dfI['Combined_skersmuo'], errors='coerce')
            dfI['Combined_gearsI'] = dfI['Combined_gearsI'].str.split(' ').str[0]
            dfI['Combined_gearsI'] = pd.to_numeric(dfI['Combined_gearsI'], errors='coerce')




            
            brand_counts = dfI['brand'].value_counts()
            filtered_df = dfI[dfI['brand'].isin(brand_counts[brand_counts > 2].index)]

            
            brand_price_means = filtered_df.groupby('brand')['price'].mean().sort_values()

            top_3_expensive = brand_price_means[-3:]
            middle_3 = brand_price_means[len(brand_price_means) // 2 - 1: len(brand_price_means) // 2 + 2]
            bottom_3_cheap = brand_price_means[:3]

            st.subheader("Price Distribution by Brand")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.boxplot(column='price', by='brand', ax=ax)
            plt.xticks(rotation=45)
            plt.title('Price Distribution by Brand')
            plt.suptitle('')
            plt.xlabel('Brand')
            plt.ylabel('Price (€)')
            st.pyplot(fig)

            
            # st.subheader("Top 3 Most Expensive Brands")
            # st.write(top_3_expensive)

            # st.subheader("Middle 3 Brands")
            # st.write(middle_3)

            # st.subheader("Top 3 Cheapest Brands")
            # st.write(bottom_3_cheap)

            
            st.subheader("Top 3 Most Expensive Brands")
            fig, ax = plt.subplots(figsize=(8, 5))
            top_3_expensive.plot(kind='bar', color='purple', ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Top 3 Most Expensive Brands")
            ax.set_xlabel("Brand")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Middle 3 Brands")
            fig, ax = plt.subplots(figsize=(8, 5))
            middle_3.plot(kind='bar', color='yellow', ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Middle 3 Brands")
            ax.set_xlabel("Brand")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Top 3 Cheapest Brands")
            fig, ax = plt.subplots(figsize=(8, 5))
            bottom_3_cheap.plot(kind='bar', color='brown', ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Top 3 Cheapest Brands")
            ax.set_xlabel("Brand")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)


            st.subheader("Price Dependency on Frame Material")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Combined_remas')['price'].mean().plot(kind='bar', ax=ax, color='orange')
            plt.xticks(rotation=45)
            ax.set_title("Price Dependency on Frame Material")
            ax.set_xlabel("Frame Material")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            

            st.subheader("Price Dependency on Wheel Diameter")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Combined_skersmuo')['price'].mean().plot(kind='line', marker='o', color='purple', ax=ax)
            ax.set_title("Price Dependency on Wheel Diameter")
            ax.set_xlabel("Wheel Diameter (inches)")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            st.subheader("Price Dependency on Number of Gears")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Combined_gearsI')['price'].mean().plot(kind='line', marker='s', color='red', ax=ax)
            ax.set_title("Price Dependency on Number of Gears")
            ax.set_xlabel("Number of Gears")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)


            st.subheader("Price Dependency on Type")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Combined_tipai')['price'].mean().plot(kind='bar', ax=ax, color='blue')
            plt.xticks(rotation=45)
            ax.set_title("Price Dependency on Type")
            ax.set_xlabel("Type")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)
            

            
            st.subheader("Price Dependency on Purpose")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Combined_paskirtis')['price'].mean().plot(kind='bar', ax=ax, color='green')
            plt.xticks(rotation=45)
            ax.set_title("Price Dependency on Purpose")
            ax.set_xlabel("Purpose")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)


with tab2:
     
    col1, col2 = st.columns(2)


with col1:
            st.title('Fridges Pigu Analysis')


            dfII = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\piguFridgesI.csv")

            dfII['price'] = pd.to_numeric(dfII['price'], errors='coerce')
            dfII['Bendra talpa:'] = dfII['Bendra talpa:'].str.replace('l', '').str.strip()
            dfII['Bendra talpa:'] = pd.to_numeric(dfII['Bendra talpa:'], errors='coerce')
            dfII['Energijos sąnaudos per metus:'] = dfII['Energijos sąnaudos per metus:'].str.replace('kWh', '').str.strip()
            dfII['Energijos sąnaudos per metus:'] = pd.to_numeric(dfII['Energijos sąnaudos per metus:'], errors='coerce')
            dfII['Maksimalus triukšmo lygis:'] = dfII['Maksimalus triukšmo lygis:'].str.replace('dB', '').str.strip()
            dfII['Maksimalus triukšmo lygis:'] = pd.to_numeric(dfII['Maksimalus triukšmo lygis:'], errors='coerce')
            dfII['Pakuotės išmatavimai ir svoris (1):'] = dfII['Pakuotės išmatavimai ir svoris (1):'].str.split('m,').str[0]
            # dfII['Pakuotės išmatavimai ir svoris (1):'] = pd.to_numeric(dfII['Pakuotės išmatavimai ir svoris (1):'], errors='coerce')



            manufacturer_counts = dfII['brand'].value_counts()
            filtered_df = dfII[dfII['brand'].isin(manufacturer_counts[manufacturer_counts > 2].index)]


            
            st.subheader("Price Distribution by Mounting Type")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Montavimo tipas:')['price'].mean().plot(kind='bar', ax=ax, color='green')
            ax.set_title("Average Price by Mounting Type")
            ax.set_xlabel("Mounting Type")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Price Distribution by Fridge Type")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Šaldytuvo tipas:')['price'].mean().plot(kind='bar', ax=ax, color='blue')
            ax.set_title("Average Price by Fridge Type")
            ax.set_xlabel("Fridge Type")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Price Dependency on Fridge Volume")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Bendra talpa:')['price'].mean().plot(kind='line', marker='o', color='orange', ax=ax)
            ax.set_title("Price Dependency on Fridge Volume")
            ax.set_xlabel("Fridge Volume (liters)")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Price Dependency on Package Dimensions")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Pakuotės išmatavimai ir svoris (1):')['price'].mean().plot(kind='line', marker='s', color='purple', ax=ax)
            plt.xticks(rotation=45)
            ax.set_title("Price Dependency on Package Dimensions")
            ax.set_xlabel("Package Dimensions (meters)")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Price Distribution by Energy Class")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Energijos klasė:')['price'].mean().plot(kind='bar', ax=ax, color='red')
            ax.set_title("Average Price by Energy Class")
            ax.set_xlabel("Energy Class")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Price Dependency on Noise Level")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Maksimalus triukšmo lygis:')['price'].mean().plot(kind='line', marker='x', color='cyan', ax=ax)
            ax.set_title("Price Dependency on Noise Level")
            ax.set_xlabel("Noise Level (dB)")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Price Vs Energy Consumption")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Energijos sąnaudos per metus:')['price'].mean().plot(kind='line', marker='d', color='magenta', ax=ax)
            ax.set_title("Price Vs Energy Consumption")
            ax.set_xlabel("Energy Consumption (kWh/year)")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Price Distribution by Control Type")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Valdymas:')['price'].mean().plot(kind='bar', ax=ax, color='yellow')
            ax.set_title("Average Price by Control Type")
            ax.set_xlabel("Control Type")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

            
            st.subheader("Price Distribution by Brand")
            fig, ax = plt.subplots(figsize=(12, 6))
            filtered_df.boxplot(column='price', by='brand', ax=ax)
            plt.xticks(rotation=45)
            plt.title('Price Distribution by Brand')
            plt.suptitle('')
            plt.xlabel('Brand')
            plt.ylabel('Price (€)')
            st.pyplot(fig)

            
            st.subheader("Price Distribution by Color")
            fig, ax = plt.subplots(figsize=(10, 6))
            filtered_df.groupby('Spalva:')['price'].mean().plot(kind='bar', ax=ax, color='pink')
            ax.set_title("Average Price by Color")
            ax.set_xlabel("Color")
            ax.set_ylabel("Average Price (€)")
            st.pyplot(fig)

with col2:
      

            st.title('Fridges Varle Analysis')

            dfIX = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\varleFridgesI.csv")

            dfIX['price'] = pd.to_numeric(dfIX['price'], errors='coerce')
            dfIX['Metinės energijos sąnaudos'] = dfIX['Metinės energijos sąnaudos'].str.replace('kWh','').str.split(' ').str[0]
            dfIX['Metinės energijos sąnaudos'] = pd.to_numeric(dfIX['Metinės energijos sąnaudos'], errors='coerce')
            dfIX['Talpa (L)'] = pd.to_numeric(dfIX['Talpa (L)'], errors='coerce')
            dfIX['Aukštis (cm)'] = pd.to_numeric(dfIX['Aukštis (cm)'], errors='coerce')


            montavimo_tipas = {
                'Laisvai statomi': 'Statomas',
                'Pastatytas': 'Statomas',
                'Laisvai pastatoma': 'Statomas',
                'Laisvai pastatomos': 'Statomas',
                'laisvai pastatoma': 'Statomas',
                'Įmontuojami': 'Montuojamas',
                'Integruota': 'Montuojamas',
                'Montuojami': 'Montuojamas',
                'įmontuojama': 'Montuojamas',
                'Pilnai įmontuojama': 'Montuojamas'
            }

            
            dfIX['Montavimo tipas'] = dfIX['Montavimo tipas'].map(montavimo_tipas)

            
            dfIX['Montavimo tipas'] = dfIX['Montavimo tipas'].fillna('Kita')



            tipas = {'Mini\n\nSu kamera viduje': 'Mini', 'Mini\n\nBe kameros': 'Mini', 'Mini\nBe kameros': 'Mini', 'Mini\nSu kamer viduje': 'Mini', 'Mini': 'Mini',
                    'Su kamera viršuje': 'Šaldytuvas su šaldikliu viršuje', 'Fridge with top freezer': 'Šaldytuvas su šaldikliu viršuje', 'Šaldytuvai su šaldikliu viršuje': 'Šaldytuvas su šaldikliu viršuje',
                    'Su kamera apačioje': 'Šaldytuvas su šaldikliu apačioje', 'Fridge with bottom freezer': 'Šaldytuvas su šaldikliu apačioje', 'Šaldytuvai su šaldikliu apačioje': 'Šaldytuvas su šaldikliu apačioje', 'Šaldytuvas su apatiniu šaldikliu': 'Šaldytuvas su šaldikliu apačioje',
                    'Be kameros': 'Šaldytuvas be šaldiklio', 'Fridge without freezer': 'Šaldytuvas be šaldiklio', 'Šaldytuvai be šaldiklio': 'Šaldytuvas be šaldiklio', 'Šaldytuvas be šaldiklio': 'Šaldytuvas be šaldiklio',
                    'Su kamera viduje': 'Šaldytuvas su šaldikliu viduje', 'Fridge with freezer inside': 'Šaldytuvas su šaldikliu viduje', 'Šaldytuvai su šaldymo kamera': 'Šaldytuvas su šaldikliu viduje', 'Su kamera': 'Šaldytuvas su šaldikliu viduje', 'Šaldikliai': 'Šaldytuvas su šaldikliu viduje',
                    'Dviduriai': 'Dviejų durų',
                    'Vitrina': 'Vitrina',
                    'Laisvai pastatomas' : 'Kiti', 'Pastatas': 'Kiti', 'Vienaduriai': 'Kiti', 'Mažo prietaiso priedas': 'Kiti', 'Lentynėlė': 'Kiti', 'Saugykla': 'Kiti', 'Side by side': 'Kiti', 'Stačiai': 'Kiti'}

            dfIX['Tipas'] = dfIX['Tipas'].map(tipas)

            dfIX['Tipas'] = dfIX['Tipas'].fillna('Kiti')
            print(dfIX['Tipas'].unique())


            max_value = dfIX['Talpa (L)'].max()

            dfIX = dfIX[dfIX['Talpa (L)'] != max_value]

            dfIX['Aukštis (cm)'] = pd.to_numeric(dfIX['Aukštis (cm)'], errors='coerce')


            top_four_max_values = dfIX['Aukštis (cm)'].nlargest(4)

            dfIX = dfIX[~dfIX['Aukštis (cm)'].isin(top_four_max_values)]


            valdymas = { 'Internal touch control LCD': 'Electroninis Sensorinis', 'Electronical with LCD': 'Electroninis Sensorinis', 'Touch control with LCD': 'Electroninis Sensorinis', 'External touch control LCD': 'Electroninis Sensorinis', 'Elektroninė su LCD': 'Electroninis Sensorinis', 'jutiklinis ekranas „Touch“': 'Electroninis Sensorinis', 'Jutiklinė elektronika': 'Electroninis Sensorinis', 'Jutiklinis valdymas': 'Electroninis Sensorinis',
             'Elektroninė': 'Elektroninis',  'Vidinis elektroninis valdymas': 'Elektroninis', 'Elektroninis': 'Elektroninis', 'External electronic control': 'Elektroninis',
              'Mechaninis': 'Mechaninis', 'išplėstinė vartotojo sąsaja': 'Mechaninis'}

            dfIX['Valdymas'] = dfIX['Valdymas'].map(valdymas)

            dfIX['Valdymas'] = dfIX['Valdymas'].fillna('Kita')


            manufacturer_counts = dfIX['Gamintojas'].value_counts()
            df_filtered = dfIX[dfIX['Gamintojas'].isin(manufacturer_counts[manufacturer_counts > 2].index)]

            
            st.subheader("Price Distribution by Mounting Type")
            fig1, ax1 = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_filtered, x='Montavimo tipas', y='price', ax=ax1)
            plt.xticks(rotation=45)
            ax1.set_title("Price Distribution by Mounting Type")
            ax1.set_xlabel("Mounting Type")
            ax1.set_ylabel("Price (€)")
            st.pyplot(fig1)

            
            st.subheader("Price Distribution by Fridge Type")
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_filtered, x='Tipas', y='price', ax=ax2)
            plt.xticks(rotation=45)
            ax2.set_title("Price Distribution by Fridge Type")
            ax2.set_xlabel("Fridge Type")
            ax2.set_ylabel("Price (€)")
            st.pyplot(fig2)

            
            st.subheader("Price vs Volume")
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            sns.scatterplot(data=df_filtered, x='Talpa (L)', y='price', hue='Energijos klasė', ax=ax3)
            ax3.set_title("Price vs Volume with Energy Class")
            ax3.set_xlabel("Volume (L)")
            ax3.set_ylabel("Price (€)")
            st.pyplot(fig3)

            
            st.subheader("Price vs Height")
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            sns.scatterplot(data=df_filtered, x='Aukštis (cm)', y='price', hue='Energijos klasė', ax=ax4)
            ax4.set_title("Price vs Height with Energy Class")
            ax4.set_xlabel("Height (cm)")
            ax4.set_ylabel("Price (€)")
            st.pyplot(fig4)

            
            st.subheader("Price Distribution by Energy Class")
            fig5, ax5 = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_filtered, x='Energijos klasė', y='price', ax=ax5)
            ax5.set_title("Price Distribution by Energy Class")
            ax5.set_xlabel("Energy Class")
            ax5.set_ylabel("Price (€)")
            st.pyplot(fig5)

            st.subheader("Price Dependency on Noise Level")
            fig9, ax9 = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_filtered, x='Garso lygio klasė', y='price', ax=ax9)
            ax9.set_title("Price Dependency on Noise Level")
            ax9.set_xlabel("Noise Level Class")
            ax9.set_ylabel("Price (€)")
            st.pyplot(fig9)

            
            st.subheader("Price Vs Energy Consumption")
            fig10, ax10 = plt.subplots(figsize=(10, 6))
            sns.scatterplot(data=df_filtered, x='Metinės energijos sąnaudos', y='price', hue='Energijos klasė', ax=ax10)
            ax10.set_title("Price Vs Energy Consumption")
            ax10.set_xlabel("Annual Energy Consumption (kWh)")
            ax10.set_ylabel("Price (€)")
            st.pyplot(fig10)

            
            st.subheader("Price Distribution by Control Type")
            fig6, ax6 = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_filtered, x='Valdymas', y='price', ax=ax6)
            plt.xticks(rotation=45)
            ax6.set_title("Price Distribution by Control Type")
            ax6.set_xlabel("Control Type")
            ax6.set_ylabel("Price (€)")
            st.pyplot(fig6)

            
            st.subheader("Price Distribution by Brand")
            fig7, ax7 = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_filtered, x='Gamintojas', y='price', ax=ax7)
            ax7.set_title("Price Distribution by Brand")
            ax7.set_xlabel("Brand")
            ax7.set_ylabel("Price (€)")
            plt.xticks(rotation=45)
            st.pyplot(fig7)

            
            st.subheader("Price Vs Color")
            fig8, ax8 = plt.subplots(figsize=(10, 6))
            sns.boxplot(data=df_filtered, x='Spalva', y='price', ax=ax8)
            ax8.set_title("Price by Color")
            ax8.set_xlabel("Color")
            ax8.set_ylabel("Price (€)")
            plt.xticks(rotation=45)
            st.pyplot(fig8)
      

            

            

