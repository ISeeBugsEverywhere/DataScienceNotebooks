import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt





df = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\piguDronsI.csv")



tab1, tab2 = st.tabs(["Plots for Drons", "Plots for TVs"])


col1, col2 = st.columns(2)

with tab1:
    with col1:
        df['Skraidymo laikas:'] = df['Skraidymo laikas:'].str.replace('min.','')
        df['Pakuotės išmatavimai ir svoris (1):'] = df['Pakuotės išmatavimai ir svoris (1):'].astype(str).str.replace('kg','').str.split('m,').str[1]
        df['Pakuotės išmatavimai ir svoris (1):'].str.replace(',','.')
        df['Talpa:'] = df['Talpa:'].str.replace('mAh','')
        df['Veikimo atstumas:'] = df['Veikimo atstumas:'].str.replace('m','')
                
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        numeric_columns = ['Skraidymo laikas:', 'Veikimo atstumas:', 'Pakuotės išmatavimai ir svoris (1):', 'Talpa:']

        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        
        df['brand'] = df['brand'].fillna('Unknown')

        
        st.sidebar.header("Filters")
        selected_brands = st.sidebar.multiselect("Select Brands", options=df['brand'].unique(), default=df['brand'].unique())
        filtered_data = df[df['brand'].isin(selected_brands)]

        
        st.title("Drone Pigu Analysis")
        
        st.subheader("Price Analysis by Brand")
        avg_price = filtered_data.groupby('brand')['price'].mean().sort_values()
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        avg_price.plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_title("Average Price by Brand")
        ax1.set_ylabel("Average Price (€)")
        ax1.set_xlabel("Brand")
        plt.xticks(rotation=45)
        st.pyplot(fig1)
        plt.close(fig1)

        
        st.subheader("Correlation Heatmap")
        numeric_features = ['price'] + numeric_columns
        corr_matrix = filtered_data[numeric_features].corr()

        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax2)
        ax2.set_title("Feature Correlation Heatmap")
        st.pyplot(fig2)
        plt.close(fig2)

        
        st.subheader("Price vs Flight Time")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=filtered_data, x='Skraidymo laikas:', y='price', hue='brand', ax=ax3)
        legend = ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        ax3.set_title("Price vs Flight Time")
        ax3.set_xlabel("Flight Time (minutes)")
        ax3.set_ylabel("Price (€)")
        st.pyplot(fig3)
        plt.close(fig3)

        
        st.subheader("Flight Time Distribution")
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        sns.histplot(filtered_data['Skraidymo laikas:'], bins=10, kde=True, ax=ax4)
        ax4.set_title("Flight Time Distribution")
        ax4.set_xlabel("Flight Time (minutes)")
        st.pyplot(fig4)
        plt.close(fig4)

        
        st.subheader("Battery Capacity vs Price")
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=filtered_data, x='Talpa:', y='price', ax=ax5)
        ax5.set_title("Battery Capacity vs Price")
        ax5.set_xlabel("Battery Capacity (mAh)")
        ax5.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig5)
        plt.close(fig5)





        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        categorical_columns = ['Kamera:', 'GPS:', 'Skrydžio stabilizacija:']

        
        for col in categorical_columns:
            df[col] = df[col].fillna('Unknown')

        

        
        st.subheader("Price Dependency on Camera:")
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x='Kamera:', y='price', ax=ax1)
        ax1.set_title("Price vs Kamera Presence")
        ax1.set_xlabel("Kamera Presence")
        ax1.set_ylabel("Price (€)")
        st.pyplot(fig1)
        plt.close(fig1)

        
        st.subheader("Price Dependency on GPS:")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x='GPS:', y='price', ax=ax2)
        ax2.set_title("Price vs GPS Presence")
        ax2.set_xlabel("GPS Presence")
        ax2.set_ylabel("Price (€)")
        st.pyplot(fig2)
        plt.close(fig2)

        
        st.subheader("Price Dependency on Stabilization")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df, x='Skrydžio stabilizacija:', y='price', ax=ax3)
        ax3.set_title("Price vs Skrydžio Stabilizacija Presence")
        ax3.set_xlabel("Stabilization Presence")
        ax3.set_ylabel("Price (€)")
        st.pyplot(fig3)
        plt.close(fig3)







        
        price_bins = [0, 100, 200, 400, 600, float('inf')]
        price_labels = ['Up to €100', '€101-200', '€201-400', '€401-600', 'Over €600']
        df['price_range'] = pd.cut(df['price'], bins=price_bins, labels=price_labels)

        
        def find_most_representative(df, group_col, target_col):
            representatives = []
            for group, group_df in df.groupby(group_col):
                avg_price = group_df[target_col].mean()
                group_df['distance'] = abs(group_df[target_col] - avg_price)
                most_representative = group_df.loc[group_df['distance'].idxmin()]
                representatives.append(most_representative)
            return pd.DataFrame(representatives)

        
        most_representative_drones = find_most_representative(df, 'price_range', 'price')

        
        st.subheader("Drone Counts by Price Range")
        price_range_counts = df['price_range'].value_counts().sort_index()
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        price_range_counts.plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_title("Drone Counts by Price Range")
        ax1.set_xlabel("Price Range")
        ax1.set_ylabel("Number of Drones")
        plt.xticks(rotation=45)
        st.pyplot(fig1)
        plt.close(fig1)

        
        st.subheader("Most Representative Drones by Price Range")
        st.dataframe(most_representative_drones[['price_range', 'brand', 'price', 'Kamera:', 'GPS:', 'Skrydžio stabilizacija:']])

        
        st.subheader("Most Representative Drones")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.barplot(data=most_representative_drones, x='price_range', y='price', hue='brand', ax=ax2)
        ax2.set_title("Representative Drones by Price Range")
        ax2.set_xlabel("Price Range")
        ax2.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
        plt.close(fig2)


    with col2:

        dfI = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\varleDronsIII.csv")
                
        dfI['price_x'] = dfI['price_x'].str.replace('€', '').str.strip().astype(float)

        
        def extract_numeric(series, unit=None):
            
            if unit:
                return series.str.replace(unit, '').str.extract(r'(\d+(?:\.\d+)?)')[0].astype(float)
            return series.str.extract(r'(\d+(?:\.\d+)?)')[0].astype(float)
        dfI['Combined_Laikas'] = dfI['Combined_Laikas'].str.split('m').str[0]
        dfI['Vaizdo raiška'] = dfI['Vaizdo raiška'].str.replace('p','').str.extract(r'\](.*)')
        # dfI['Combined_Atstumas'] = dfI['Combined_Atstumas'].astype(str)
        # dfI['Combined_Atstumas'] = dfI['Combined_Atstumas'].str.split(': ').str[1].str.replace('m','')
        # dfI['Combined_Atstumas'] = dfI['Combined_Atstumas'].str.replace(' ','').str.split(',').str[0]
        dfI['Combined_Laikas'] = extract_numeric(dfI['Combined_Laikas'], 'minutė')
        dfI['Combined_Atstumas'] = extract_numeric(dfI['Combined_Atstumas'].astype(str), 'm')
        dfI['Combined_Talpa'] = extract_numeric(dfI['Combined_Talpa'], 'mAh')
        dfI['Combined_svoris'] = extract_numeric(dfI['Combined_svoris'], 'g')
        # dfI['Combined_Atstumas'] = dfI['Combined_Atstumas'].astype(str)
        # dfI['Combined_Atstumas'] = dfI['Combined_Atstumas'].str.split(': ').str[1].str.replace('m','')
        # dfI['Combined_Atstumas'] = dfI['Combined_Atstumas'].str.replace(' ','').str.split(',').str[0]


        # Fill missing values with 0
        dfI['Combined_Laikas'].fillna(0, inplace=True)
        dfI['Combined_Atstumas'].fillna(0, inplace=True)
        dfI['Combined_Talpa'].fillna(0, inplace=True)
        dfI['Combined_svoris'].fillna(0, inplace=True)

        
        st.title("Drone Varle Analysis")
        

        
        st.subheader("Price Distribution by Brand")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=dfI, x='brand_x', y='price_x', ax=ax1)
        ax1.set_title("Price Distribution by Brand")
        ax1.set_xlabel("Brand")
        ax1.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig1)
        plt.close(fig1)



        
        st.subheader("Correlation Heatmap")
        numeric_features = ['price_x', 'Combined_Laikas', 'Combined_Atstumas', 'Combined_Talpa', 'Combined_svoris']
        correlation_matrix = dfI[numeric_features].corr()

        fig_corr, ax_corr = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
        ax_corr.set_title("Correlation Between Features")
        st.pyplot(fig_corr)
        plt.close(fig_corr)



        
        st.subheader("Price vs Flight Time")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=dfI, x='Combined_Laikas', y='price_x', hue='brand_x', ax=ax2)
        legend = ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        ax2.set_title("Price vs Flight Time")
        ax2.set_xlabel("Flight Time (minutes)")
        ax2.set_ylabel("Price (€)")
        st.pyplot(fig2)
        plt.close(fig2)

        
        st.subheader("Price vs Flight Distance")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=dfI, x='Combined_Atstumas', y='price_x', hue='brand_x', ax=ax3)
        legend = ax3.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        ax3.set_title("Price vs Flight Distance")
        ax3.set_xlabel("Distance (m)")
        ax3.set_ylabel("Price (€)")
        st.pyplot(fig3)
        plt.close(fig3)

        
        st.subheader("Price vs Battery Capacity")
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=dfI, x='Combined_Talpa', y='price_x', hue='brand_x', ax=ax4)
        legend = ax4.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        ax4.set_title("Price vs Battery Capacity")
        ax4.set_xlabel("Battery Capacity (mAh)")
        ax4.set_ylabel("Price (€)")
        st.pyplot(fig4)
        plt.close(fig4)

        
        st.subheader("Price vs Drone Weight")
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=dfI, x='Combined_svoris', y='price_x', hue='brand_x', ax=ax5)
        legend = ax5.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        ax5.set_title("Price vs Drone Weight")
        ax5.set_xlabel("Weight (g)")
        ax5.set_ylabel("Price (€)")
        st.pyplot(fig5)
        plt.close(fig5)






        
        categorical_columns = [ 'Vaizdo raiška', 'Combined_gps', 'Combined_Stabilization']
        for col in categorical_columns:
            dfI[col] = dfI[col].astype(str).fillna('Unknown')

        

        
        st.subheader("Price Dependency on Video Resolution")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=dfI, x='Vaizdo raiška', y='price_x', ax=ax1)
        ax1.set_title("Price vs Video Resolution")
        ax1.set_xlabel("Video Resolution")
        ax1.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig1)
        plt.close(fig1)

        
        st.subheader("Price Dependency on GPS")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=dfI, x='Combined_gps', y='price_x', ax=ax2)
        ax2.set_title("Price vs GPS")
        ax2.set_xlabel("GPS Presence")
        ax2.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
        plt.close(fig2)

        
        st.subheader("Price Dependency on Stabilization")
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=dfI, x='Combined_Stabilization', y='price_x', ax=ax3)
        ax3.set_title("Price vs Stabilization")
        ax3.set_xlabel("Stabilization Type")
        ax3.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig3)
        plt.close(fig3)






        
        price_bins = [0, 100, 200, 400, 600, float('inf')]
        price_labels = ['Up to €100', '€101-200', '€201-400', '€401-600', 'Over €600']
        dfI['price_range'] = pd.cut(dfI['price_x'], bins=price_bins, labels=price_labels)

        
        def find_representative_drones(dfI, group_col, target_col):
            representatives = []
            for group, group_df in dfI.groupby(group_col):
                mean_price = group_df[target_col].mean()
                group_df['distance'] = abs(group_df[target_col] - mean_price)
                representative = group_df.loc[group_df['distance'].idxmin()]
                representatives.append(representative)
            return pd.DataFrame(representatives)

        
        representative_drones = find_representative_drones(dfI, 'price_range', 'price_x')


        
        st.subheader("Drone Counts by Price Range")
        price_range_counts = df['price_range'].value_counts().sort_index()
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        price_range_counts.plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_title("Drone Counts by Price Range")
        ax1.set_xlabel("Price Range")
        ax1.set_ylabel("Number of Drones")
        plt.xticks(rotation=45)
        st.pyplot(fig1)
        plt.close(fig1)

        
        st.subheader("Most Representative Drones by Price Range")
        st.dataframe(representative_drones[['price_range', 'brand_x', 'price_x', 'Vaizdo raiška', 'Combined_gps', 'Combined_Stabilization']])

        
        st.subheader("Representative Drones")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        sns.barplot(data=representative_drones, x='price_range', y='price_x', hue='brand_x', ax=ax2)
        ax2.set_title("Representative Drones by Price Range")
        ax2.set_xlabel("Price Range")
        ax2.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
        plt.close(fig2)




with tab2:
    col1, col2 = st.columns(2)

    with col1:
        dfII = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\piguTVsI.csv")
        
        dfII['price'] = pd.to_numeric(dfII['price'], errors='coerce')
        
        
        st.title("TV Pigu Analysis")


        
        dfII['price'] = pd.to_numeric(dfII['price'], errors='coerce')
        dfII['Ekrano įstrižainė:'] = dfII['Ekrano įstrižainė:'].str.replace('~', '').str.extract(r'(\d+)').astype(float)
        dfII['Maksimali raiška:'] = dfII['Maksimali raiška:'].str.replace(' ', '').str.extract(r'(\d+)').astype(float)
        
        
        dfII = dfII.dropna(subset=['price', 'Ekrano įstrižainė:', 'Maksimali raiška:'])

        
        
        st.subheader("Price Dependence on Resolution and Screen Size")
        fig1, ax1 = plt.subplots(figsize=(8, 6))
        sns.scatterplot(data=dfII, x='Ekrano įstrižainė:', y='price', hue='Maksimali raiška:', palette='viridis', ax=ax1)
        ax1.set_title("Price Dependence on Resolution and Screen Size")
        ax1.set_xlabel("Screen Size (inches)")
        ax1.set_ylabel("Price (€)")
        st.pyplot(fig1)
        
        
        st.subheader("Price Distribution Among Top 5 Brands")
        top_brands = dfII['brand'].value_counts().head(5).index
        top_brands_data = dfII[dfII['brand'].isin(top_brands)]
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.boxplot(data=top_brands_data, x='brand', y='price', ax=ax2, palette='Set2')
        ax2.set_title("Price Distribution Among Top 5 Brands")
        ax2.set_xlabel("Brand")
        ax2.set_ylabel("Price (€)")
        st.pyplot(fig2)
        
        
        st.subheader("OS vs Price")
        dfII['Operacinė sistema:'] = dfII['Operacinė sistema:'].fillna('No OS')
        fig3, ax3 = plt.subplots(figsize=(8, 6))
        sns.boxplot(data=dfII, x='Operacinė sistema:', y='price', ax=ax3, palette='coolwarm')
        ax3.set_title("Impact of OS on Price Levels")
        ax3.set_xlabel("Operating System")
        ax3.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig3)
        




        price_bins = [0, 100, 200, 500, float('inf')]
        price_labels = ['Up to €100', '€101-200', '€201-500', 'Over €500']
        dfII['price_range'] = pd.cut(dfII['price'], bins=price_bins, labels=price_labels)

        
        def find_representative_products(data, group_col, target_col):
            representatives = []
            for group, group_df in data.groupby(group_col):
                mean_price = group_df[target_col].mean()
                group_df['distance'] = abs(group_df[target_col] - mean_price)
                representative = group_df.loc[group_df['distance'].idxmin()]
                representatives.append(representative)
            return pd.DataFrame(representatives)

        
        representative_tvs = find_representative_products(dfII, 'price_range', 'price')

        

        
        st.subheader("Most Representative TVs by Price Range")
        st.dataframe(representative_tvs[['price_range', 'brand', 'price', 'Ekrano įstrižainė:', 'Maksimali raiška:']])

        
        st.subheader("Distribution of TVs by Price Range")
        price_range_counts = dfII['price_range'].value_counts().sort_index()
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        price_range_counts.plot(kind='bar', color='skyblue', ax=ax1)
        ax1.set_title("Number of TVs by Price ")
        ax1.set_xlabel("Price Range")
        ax1.set_ylabel("Number of TVs")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

        
        st.subheader("Representative TVs")
        fig2, ax2 = plt.subplots(figsize=(8, 6))
        sns.barplot(data=representative_tvs, x='price_range', y='price', hue='brand', ax=ax2, palette='Set2')
        ax2.set_title("Representative TVs by Price ")
        ax2.set_xlabel("Price Range")
        ax2.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig2)


    with col2:
        dfIII = pd.read_csv(r"C:\Users\Batia\Desktop\DataScienceNotebooks\Studentai\Vladimir\varleTVsI.csv")
        



        
        dfIII['price'] = pd.to_numeric(dfIII['price'], errors='coerce')
        dfIII['Combined_raiska'] = dfIII['Combined_raiska'].str.extract(r'(\d+x\d+)')
        # dfIII['Combined_istrizaine'] = dfIII['Combined_istrizaine'].astype(str)
        # dfIII['Combined_istrizaine'] = dfIII['Combined_istrizaine'].str.extract(r'(\d+)')
        # dfIII['Combined_istrizaine'] = pd.to_numeric(dfIII['Combined_istrizaine'], errors='coerce')
        dfIII['Combined_istrizaine'] = dfIII['Combined_istrizaine'].astype(str)
        dfIII['Combined_istrizaine'] = (
            dfIII['Combined_istrizaine']
            .str.replace(r'[^0-9"\s]', '', regex=True)  # Remove unwanted characters except digits, spaces, and quotes
            .str.extract(r'(\d+)"|(\d+)')  # Extract values like 55" or plain numbers like 55
            .bfill(axis=1)  # Backfill to handle either group (quoted or plain) correctly
            .iloc[:, 0]  # Take the first non-null extracted value
        )
        # dfIII['Combined_istrizaine'] = dfIII['Combined_istrizaine'].astype(str)
        dfIII = dfIII[~dfIII['Combined_istrizaine'].astype(str).str.match(r'^\d{4}\.')]
        
        # dfIII['Combined_istrizaine'] = pd.to_numeric(dfIII['Combined_istrizaine'], errors='coerce')


        
        top_5_brands = dfIII['brand'].value_counts().head(5).index
        top_5_data = dfIII[dfIII['brand'].isin(top_5_brands)]

        
        st.title("TV Varle Analysis")
        

        # Resolution vs Price
        fig1, ax1 = plt.subplots()
        sns.boxplot(data=dfIII, x='Combined_raiska', y='price', ax=ax1)
        ax1.set_title("Price vs Resolution")
        ax1.set_xlabel("Resolution")
        ax1.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig1)

        # Screen Size vs Price
        fig2, ax2 = plt.subplots()
        sns.scatterplot(data=dfIII, x='Combined_istrizaine', y='price', hue='brand', ax=ax2, palette="tab10")
        legend = ax2.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Brands")
        plt.xticks(rotation=45)
        ax2.set_title("Price vs Screen Size")
        ax2.set_xlabel("Screen Size (inches)")
        ax2.set_ylabel("Price (€)")
        st.pyplot(fig2)

        
        st.markdown("### Price Distribution Among Top 5 Brands")
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=top_5_data, x='brand', y='price', ax=ax3, palette="Set2")
        ax3.set_title("Price Distribution Among Top 5 Brands")
        ax3.set_xlabel("Brand")
        ax3.set_ylabel("Price (€)")
        st.pyplot(fig3)

        
        st.markdown("### Influence of Operating System on Prices")
        fig4, ax4 = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=dfIII, x='Combined_operacine', y='price', ax=ax4, palette="coolwarm")
        ax4.set_title("Price by Operating System")
        ax4.set_xlabel("Operating System")
        ax4.set_ylabel("Price (€)")
        plt.xticks(rotation=45)
        st.pyplot(fig4)




        import numpy as np
        bins = [0, 100, 200, 500, np.inf]
        labels = ['< 100 €', '101-200 €', '201-500 €', '> 500 €']
        dfIII['price_range'] = pd.cut(dfIII['price'], bins=bins, labels=labels)

        
        def find_representative(df, group_col, value_col):
            representatives = []
            for group, group_data in df.groupby(group_col):
                avg_price = group_data[value_col].mean()
                representative = group_data.iloc[(group_data[value_col] - avg_price).abs().argsort()[:1]]
                representatives.append(representative)
            return pd.concat(representatives)

        
        representative_tvs = find_representative(dfIII, 'price_range', 'price')

        

        
        st.subheader("Most Representative TVs by Price Range")
        st.dataframe(representative_tvs[['title', 'price', 'price_range', 'brand']])

        
        st.subheader("Price Distribution by Range")
        fig, ax = plt.subplots(figsize=(10, 6))
        dfIII['price_range'].value_counts().sort_index().plot(kind='bar', color='skyblue', ax=ax)
        ax.set_title("Number of TVs in Each Price Range")
        ax.set_xlabel("Price Range (€)")
        ax.set_ylabel("Number of TVs")
        st.pyplot(fig)

        
        st.subheader("Average Price by Range")
        avg_prices = dfIII.groupby('price_range')['price'].mean()
        fig, ax = plt.subplots(figsize=(10, 6))
        avg_prices.plot(kind='bar', color='orange', ax=ax,)
        ax.set_title("Average Price by Range")
        ax.set_xlabel("Price Range (€)")
        ax.set_ylabel("Average Price (€)")
        st.pyplot(fig)
        