import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import seaborn as sns
import sqlite3
import mysql.connector as cnt
import plotly.express as px


ptI = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\piguTabletsI.csv")


ptI = ptI.dropna(subset=['brand', 'price'])

tab1, tab2 = st.tabs(["Plots for Tablets", "Plots for Drons"])


col1, col2 = st.columns(2)

with tab1:
    with col1:
        st.title('Tablet Pigu Analysis')


        st.subheader('Average Price by Brand')
        avg_price_by_brand = ptI.groupby('brand')['price'].mean().sort_values()


        fig, ax = plt.subplots(figsize=(10, 6))
        avg_price_by_brand.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title('Average Price by Brand')
        ax.set_ylabel('Average Price (€)')
        ax.set_xlabel('Brand')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)

        st.subheader('Price Distribution by Brand')
        brands = ptI['brand'].unique()
        price_data = [ptI[ptI['brand'] == brand]['price'].dropna() for brand in brands]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.boxplot(price_data, labels=brands, vert=False)
        ax.set_title('Price Distribution by Brand')
        ax.set_xlabel('Price (€)')
        ax.set_ylabel('Brand')
        st.pyplot(fig)
        plt.close(fig)















        ptI = ptI.dropna(subset=['brand'], axis=0)


        ptI['price'] = pd.to_numeric(ptI['price'], errors='coerce').replace(-1, np.nan)
        ptI['price'] = ptI['price'].astype(float)


        top_5e = (
        ptI.sort_values('price', ascending=False)
        .drop_duplicates(subset='brand')
        .nlargest(5, 'price'))
        top_5c = ptI[ptI['price'].notna()].sort_values('price', ascending=False).drop_duplicates(subset='brand').nsmallest(5, 'price')
        middle_5 = ptI.iloc[len(ptI)//2 - 2:len(ptI)//2 + 3]


        # ptI = ptI[ptI['brand'].notna() & ptI['price'].notna()]

        # ptI = ptI.dropna(subset=['brand'], inplace=True)
        # subset=[]
        # ptI = ptI.dropna(subset=['brand'], axis=0)

        # st.title("Price Analysis of Tablets")


        st.subheader("Top 5 Most Expensive Tablets")
        fig, ax = plt.subplots()
        top_5e.plot(x='brand', y='price', kind='bar', ax=ax, color='red', legend=False)
        ax.set_ylabel('Price')
        ax.set_title('Top 5 Most Expensive Tablets')
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Top 5 Cheapest Tablets")
        fig, ax = plt.subplots()
        top_5c.plot(x='brand', y='price', kind='bar', ax=ax, color='green', legend=False)
        ax.set_ylabel('Price')
        ax.set_title('Top 5 Cheapest Tablets')
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Middle 5 Tablets")
        fig, ax = plt.subplots()
        middle_5.plot(x='brand', y='price', kind='bar', ax=ax, color='blue', legend=False)
        ax.set_ylabel('Price')
        ax.set_title('Middle 5 Tablets')
        st.pyplot(fig)
        plt.close(fig)

        # ptI['Vidinė atmintis:'] = ptI['Vidinė atmintis:'].astype(str)
        # ptI['Vidinė atmintis:'] = ptI['Vidinė atmintis:'].str.replace('GB','').str.split(' ').str[0]
        # ptI['Svoris:'] = ptI['Svoris:'].str.replace('kg','')
        # ptI['price'] = pd.to_numeric(ptI['price'], errors='coerce')
        # ptI['Ekrano įstrižainė:'] = pd.to_numeric(ptI['Ekrano įstrižainė:'], errors='coerce')
        # ptI['Svoris:'] = pd.to_numeric(ptI['Svoris:'], errors='coerce')
        # ptI['Vidinė atmintis:'] = pd.to_numeric(ptI['Vidinė atmintis:'], errors='coerce')
        # ptI['Maksimali raiška:'] = pd.to_numeric(ptI['Maksimali raiška:'], errors='coerce')
        # ptI['GPS:'] = ptI['GPS:'].map({'Taip': 1, 'Ne': 0})








        

        # Scatter Plot
        st.subheader('Price vs Screen Size')
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=ptI, x='Ekrano įstrižainė:', y='price', hue='Ekrano tipas:', style='GPS:', s=100, ax=ax)
        legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Type of Screen")
        plt.xticks(rotation=45)
        ax.set_title('Price vs Screen Size')
        ax.set_xlabel('Screen Size (inches)')
        ax.set_ylabel('Price (€)')
        st.pyplot(fig)
        plt.close(fig)
        # Grouped Bar Chart
        st.subheader('Average Price by Screen Type')
        avg_price_by_screen_type = ptI.groupby('Ekrano tipas:')['price'].mean().sort_values()
        fig, ax = plt.subplots(figsize=(8, 6))
        avg_price_by_screen_type.plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title('Average Price by Screen Type')
        ax.set_ylabel('Average Price (€)')
        ax.set_xlabel('Screen Type')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
        # Scatter Plot
        st.subheader('Price vs Weight')
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=ptI, x='Svoris:', y='price', hue='5G:', style='4G:', s=100, ax=ax)
        plt.xticks(rotation=45)
        ax.set_title('Price vs Weight')
        ax.set_xlabel('Weight (kg)')
        ax.set_ylabel('Price (€)')
        st.pyplot(fig)
        plt.close(fig)
        # Pair Plot

        ptI['Vidinė atmintis:'] = ptI['Vidinė atmintis:'].str.replace('GB','').str.split(' ').str[0]
        ptI['Svoris:'] = ptI['Svoris:'].str.replace('kg','')
        ptI['price'] = pd.to_numeric(ptI['price'], errors='coerce')
        ptI['Ekrano įstrižainė:'] = pd.to_numeric(ptI['Ekrano įstrižainė:'], errors='coerce')
        ptI['Svoris:'] = pd.to_numeric(ptI['Svoris:'], errors='coerce')
        ptI['Vidinė atmintis:'] = pd.to_numeric(ptI['Vidinė atmintis:'], errors='coerce')
        # ptI['Maksimali raiška:'] = pd.to_numeric(ptI['Maksimali raiška:'], errors='coerce')
        # ptI['GPS:'] = ptI['GPS:'].map({'Taip': 1, 'Ne': 0})
        st.subheader('Pair Plot: Price and Features')
        selected_features = ['price', 'Maksimali raiška:', 'Vidinė atmintis:', 'GPS:']
        sns.pairplot(ptI[selected_features], diag_kind='auto')
        st.pyplot(plt.gcf())


        
        selected_features = ['price', 'Maksimali raiška:', 'Vidinė atmintis:', 'GPS:']
        filtered_data = ptI[selected_features].dropna()

        
        sns.set(style="whitegrid")
        sns.pairplot(filtered_data, diag_kind='kde', corner=True)

        
        plt.suptitle('Pair Plot of Price and Selected Features', y=1.02)
        plt.tight_layout()
        plt.show()


        # ptI['Vidinė atmintis:'] = ptI['Vidinė atmintis:'].str.replace('GB','').str.split(' ').str[0]
        # ptI['Svoris:'] = ptI['Svoris:'].str.replace('kg','')
        # ptI['price'] = pd.to_numeric(ptI['price'], errors='coerce')
        # ptI['Ekrano įstrižainė:'] = pd.to_numeric(ptI['Ekrano įstrižainė:'], errors='coerce')
        # ptI['Svoris:'] = pd.to_numeric(ptI['Svoris:'], errors='coerce')
        # ptI['Vidinė atmintis:'] = pd.to_numeric(ptI['Vidinė atmintis:'], errors='coerce')
        # ptI['Maksimali raiška:'] = pd.to_numeric(ptI['Maksimali raiška:'], errors='coerce')
        # ptI['GPS:'] = ptI['GPS:'].map({'Taip': 1, 'Ne': 0})
            # Filter relevant columns for pairplot
        # features = ['price', 'Maksimali raiška:', 'Vidinė atmintis:', 'GPS:', 'Svoris:']
        # filtered_data = ptI.dropna(subset=features)[features]

        
        # if not filtered_data.empty:
        #     fig = sns.pairplot(filtered_data, diag_kind='kde', height=3, corner=True)
        #     st.pyplot(fig)
        # else:
        #     st.warning("Not enough data to create a pairplot.")




        ptI['price'] = pd.to_numeric(ptI['price'], errors='coerce')
        ptI['Ekrano įstrižainė:'] = pd.to_numeric(ptI['Ekrano įstrižainė:'], errors='coerce')
        ptI['Svoris:'] = pd.to_numeric(ptI['Svoris:'], errors='coerce')
        
        
        
        
        
        ptI['price'] = pd.to_numeric(ptI['price'], errors='coerce')

        
        price_bins = [0, 200, 400, 600, float('inf')]
        price_labels = ['Up to €200', '€201-400', '€401-600', 'Over €600']
        ptI['price_range'] = pd.cut(ptI['price'], bins=price_bins, labels=price_labels)

        
        def find_representative_tablets(ptI, group_col, target_col):
            representatives = []
            for group, group_df in ptI.groupby(group_col):
                mean_price = group_df[target_col].mean()
                group_df['distance'] = abs(group_df[target_col] - mean_price)
                representative = group_df.loc[group_df['distance'].idxmin()]
                representatives.append(representative)
            return pd.DataFrame(representatives)

        
        representative_tablets = find_representative_tablets(ptI, 'price_range', 'price')


        
        st.subheader("Tablet Counts by Price Range")
        price_range_counts = ptI['price_range'].value_counts().sort_index()
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        price_range_counts.plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_title("Tablet Counts by Price Range")
        ax1.set_xlabel("Price Range")
        ax1.set_ylabel("Number of Tablets")
        plt.xticks(rotation=45)
        st.pyplot(fig1)
        plt.close(fig1)

        
        st.subheader("Most Representative Tablets by Price Range")
        st.dataframe(representative_tablets[['price_range', 'brand', 'price', 'Ekrano tipas:', 'Baterijos talpa (mAh):', 'Vidinė atmintis:']])

        
        st.subheader("Representative Tablets")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.barplot(data=representative_tablets, x='price_range', y='price', hue='brand', ax=ax2)
        ax2.set_title("Representative Tablets by Price Range")
        ax2.set_xlabel("Price Range")
        ax2.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
        plt.close(fig2)


    with col2:
        st.title('Tablet Varle Analysis')

        ptII = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\varleTabletsTI.csv")


        ptII = ptII.dropna(subset=['brand', 'price'])



        
        ptII['price'] = pd.to_numeric(ptII['price'], errors='coerce')
        ptII['brand'] = ptII['brand'].fillna('Unknown')

        
        selected_brands = st.sidebar.multiselect("Select Brands", options=ptII['brand'].unique(), default=ptII['brand'].unique())

        
        filtered_data = ptII[ptII['brand'].isin(selected_brands)]

        
        # top_5_expensive = filtered_data.nlargest(5, 'price')
        top_5_expensive = (
        filtered_data.sort_values('price', ascending=False)
        .drop_duplicates(subset='brand')
        .nlargest(5, 'price'))
        top_5_cheap = filtered_data.nsmallest(5, 'price')
        # middle_5 = filtered_data.iloc[len(filtered_data) // 2 - 2:len(filtered_data) // 2 + 3]


        
        brand_median_prices = filtered_data.groupby('brand')['price'].median().reset_index()

        
        sorted_brands = brand_median_prices.sort_values('price')

        
        if len(sorted_brands) >= 5:
            start = len(sorted_brands) // 2 - 2
            end = len(sorted_brands) // 2 + 3
            middle_5_brands = sorted_brands.iloc[start:end]
        else:
            middle_5_brands = sorted_brands

        
        middle_5 = filtered_data[filtered_data['brand'].isin(middle_5_brands['brand'])].drop_duplicates(subset='brand').nlargest(5, 'price')
            
        tablets_by_brand = filtered_data['brand'].value_counts()


        
        st.subheader("Average Price by Brand")
        avg_price_by_brand = filtered_data.groupby('brand')['price'].mean().sort_values()
        fig, ax = plt.subplots(figsize=(6, 4))
        avg_price_by_brand.plot(kind='bar', color='orange', ax=ax)
        ax.set_title("Average Price by Brand")
        ax.set_ylabel("Average Price (€)")
        ax.set_xlabel("Brand")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)

        st.subheader('Price Distribution by Brand')
        brands = ptII['brand'].unique()
        price_data = [ptII[ptII['brand'] == brand]['price'].dropna() for brand in brands]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.boxplot(price_data, labels=brands, vert=False)
        ax.set_title('Price Distribution by Brand')
        ax.set_xlabel('Price (€)')
        ax.set_ylabel('Brand')
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Top 5 Most Expensive Tablets")
        fig, ax = plt.subplots()
        top_5_expensive.plot(x='brand', y='price', kind='bar', ax=ax, color='red', legend=False)
        ax.set_ylabel('Price')
        ax.set_title('Top 5 Most Expensive Tablets')
        st.pyplot(fig)
        plt.close(fig)
        
        # st.subheader("Top 5 Expensive Tablets")
        # fig, ax = plt.subplots(figsize=(6, 4))
        # ax.bar(top_5_expensive['brand'], top_5_expensive['price'], color='orange')
        # ax.set_title("Top 5 Expensive Tablets")
        # ax.set_xlabel("Brand")
        # ax.set_ylabel("Price (€)")
        # plt.xticks(rotation=45)
        # st.pyplot(fig)

        
        st.subheader("Top 5 Cheapest Tablets")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(top_5_cheap['brand'], top_5_cheap['price'], color='green')
        ax.set_title("Top 5 Cheapest Tablets")
        ax.set_xlabel("Brand")
        ax.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)
        
        # st.subheader("Middle 5 Tablets")
        # fig, ax = plt.subplots(figsize=(6, 4))
        # ax.bar(middle_5['brand'], middle_5['price'], color='purple')
        # ax.set_title("Middle 5 Tablets")
        # ax.set_xlabel("Brand")
        # ax.set_ylabel("Price (€)")
        # plt.xticks(rotation=45)
        # st.pyplot(fig)



        st.subheader("Middle 5 Tablets")
        if not middle_5.empty:
            fig, ax = plt.subplots(figsize=(6, 4))
            middle_5.plot(x='brand', y='price', kind='bar', ax=ax, color='purple', legend=False)
            ax.set_ylabel('Price (€)')
            ax.set_title('Middle 5 Tablets')
            plt.xticks(rotation=45)
            st.pyplot(fig)
            plt.close(fig)
        else:
            st.warning("Not enough data to display middle-range tablets.")
        


        
        # st.subheader('Price vs Screen Size')
        # fig, ax = plt.subplots(figsize=(8, 6))
        # sns.scatterplot(data=ptII, x='Combined_ekrano_įs', y='price', hue='Combined_ekrano_t', style='Combined_gps', s=100, ax=ax)
        # ax.set_title('Price vs Screen Size')
        # ax.set_xlabel('Screen Size (inches)')
        # ax.set_ylabel('Price (€)')
        # st.pyplot(fig)











        
        ptII['price'] = pd.to_numeric(ptII['price'], errors='coerce')
        ptII['brand'] = ptII['brand'].fillna('Unknown')
        ptII['Combined_ekrano_dyd'] = pd.to_numeric(ptII['Combined_ekrano_dyd'], errors='coerce')
        ptII['Combined_vidinė'] = pd.to_numeric(ptII['Combined_vidinė'].str.extract('(\d+)')[0], errors='coerce')
        ptII['Combined_svor'] = pd.to_numeric(ptII['Combined_svor'].str.extract('(\d+\.\d+)')[0], errors='coerce')

        
        filtered_data = ptII[ptII['brand'].isin(selected_brands)]

        
        filtered_data = filtered_data.dropna(subset=['price', 'Combined_ekrano_dyd', 'Combined_vidinė', 'Combined_svor'])


        
        st.subheader("Price vs Screen Size")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=filtered_data, x='Combined_ekrano_dyd', y='price', hue='brand', ax=ax)
        legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        ax.set_title("Price vs Screen Size")
        ax.set_xlabel("Screen Size (inches)")
        ax.set_ylabel("Price (€)")
        st.pyplot(fig)
        plt.close(fig)




        
        st.subheader("Price vs Internal Storage")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=filtered_data, x='Combined_vidinė', y='price', hue='brand', ax=ax)
        legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        ax.set_title("Price vs Internal Storage")
        ax.set_xlabel("Internal Storage (GB)")
        ax.set_ylabel("Price (€)")
        st.pyplot(fig)
        plt.close(fig)



        
        st.subheader("Price vs Weight")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=filtered_data, x='Combined_svor', y='price', hue='brand', ax=ax)
        legend = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        ax.set_title("Price vs Weight")
        ax.set_xlabel("Weight (kg)")
        ax.set_ylabel("Price (€)")
        st.pyplot(fig)
        plt.close(fig)


        
        features = ['price', 'Combined_ekrano_dyd', 'Combined_vidinė', 'Combined_svor']
        filtered_data = ptII.dropna(subset=features)[features]

        
        st.subheader("Pairplot for Price and Features")
        if not filtered_data.empty:
            fig = sns.pairplot(filtered_data, diag_kind='kde', height=3, corner=True)
            st.pyplot(fig)
            
        else:
            st.warning("Not enough data to create a pairplot.")




        
        bins = [0, 200, 400, 600, float('inf')]
        labels = ['Up to €200', '€201-400', '€401-600', 'Over €600']
        ptII['price_range'] = pd.cut(ptII['price'], bins=bins, labels=labels)

        
        def find_most_average(df, group_col, avg_cols):
            representatives = []
            for group, group_df in df.groupby(group_col):
                mean_values = group_df[avg_cols].mean()
                group_df['distance'] = group_df[avg_cols].sub(mean_values).pow(2).sum(axis=1)
                most_average = group_df.loc[group_df['distance'].idxmin()]
                representatives.append(most_average)
            return pd.DataFrame(representatives)

        
        avg_cols = ['price', 'Combined_ekrano_dyd', 'Combined_vidinė', 'Combined_svor']

        
        most_average_tablets = find_most_average(ptII.dropna(subset=avg_cols), 'price_range', avg_cols)

        
        st.subheader("Most Average Tablets by Price Range")
        st.dataframe(most_average_tablets)

        
        st.subheader("Price Distribution by Range")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=most_average_tablets, x='price_range', y='price', hue='brand', ax=ax)
        ax.set_title("Price Distribution by Range")
        ax.set_xlabel("Price Range")
        ax.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        



        
        st.subheader("Screen Size Distribution by Range")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=most_average_tablets, x='price_range', y='Combined_ekrano_dyd', hue='brand', ax=ax)
        ax.set_title("Screen Size Distribution by Range")
        ax.set_xlabel("Price Range")
        ax.set_ylabel("Screen Size (inches)")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        

        
        st.subheader("Internal Storage Distribution by Range")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(data=most_average_tablets, x='price_range', y='Combined_vidinė', hue='brand', ax=ax)
        ax.set_title("Internal Storage Distribution by Range")
        ax.set_xlabel("Price Range")
        ax.set_ylabel("Internal Storage (GB)")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        

with tab2:

         st.title('Drone Pigu Price Analysis')

        