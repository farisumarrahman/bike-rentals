import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache  # Cache the dataset to improve performance
def load_data():
    return pd.read_csv('day.csv')

# Mengubah data categorical yang encoded menjadi label
def transform_categorical(df):
    # Mendefinisikan mapping value
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    year_mapping = {0: 2011, 1: 2012}
    month_mapping = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    weather_mapping = {1: 'Clear', 2: 'Mist', 3: 'Light Snow', 4: 'Heavy Rain'}

    # Mengubah encoded value sesuai mapping
    df['season'] = df['season'].map(season_mapping)
    df['yr'] = df['yr'].map(year_mapping)
    df['mnth'] = df['mnth'].map(month_mapping)
    df['weathersit'] = df['weathersit'].map(weather_mapping)

    return df

# Sidebar untuk filtering
def sidebar(df):
    st.sidebar.header('Filter Data')

    # Membuat list kategori untuk filtering
    categorical_cols = [col for col in df.columns if df[col].dtype == 'object']
    categorical_cols.append('yr')

    # Dropdown untuk memilih filter categorical column 
    selected_column = st.sidebar.selectbox('Select Column', categorical_cols)
    selected_values = df[selected_column].unique()
    selected_values = st.sidebar.multiselect('Select Values', selected_values) # Multiselect

    return selected_column, selected_values

# Main function
def main():
    st.title('Bike Rentals Dashboard ✨')

    df = load_data()

    # Copy dataframe untuk menghindari CachedObjectMutationWarning
    df_transformed = transform_categorical(df.copy())  

    # Sidebar untuk filter
    selected_column, selected_values = sidebar(df_transformed)
    if selected_values:
        filtered_df = df_transformed[df_transformed[selected_column].isin(selected_values)]
    else:
        filtered_df = df_transformed

    # Menampilkan tabel data
    st.subheader('Data')
    st.write(filtered_df)

    # Menampilkan total penyewaan sepeda
    st.subheader('Total Penyewaan Sepeda di Washington DC')
    rentals_count = filtered_df['cnt'].sum()
    st.write(f'Sebanyak {rentals_count} sepeda telah disewakan')

    # Visualisasi Data dengan Bar Chart
    st.subheader('Visualisasi Data dengan Bar Chart')
    if selected_column:
        rentals_by_category = filtered_df.groupby(selected_column)['cnt'].sum()
        plt.figure(figsize=(10, 6))
        sns.barplot(x=rentals_by_category.index, y=rentals_by_category.values)
        plt.xticks(rotation=45)
        plt.xlabel(selected_column)
        plt.ylabel('Jumlah sepeda disewakan')
        st.pyplot(plt)

    # Mendapatkan 10 hari dengan penyewaan sepeda terbanyak
    daily_rentals = df_transformed.groupby('dteday')['cnt'].sum().reset_index()
    top_days = daily_rentals.nlargest(10, 'cnt')

    # Menampilkan data
    st.subheader('Top 10 hari dengan penyewaan sepeda terbanyak')
    st.write(top_days)

    # Memvisualisasikan dalam bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x='dteday', y='cnt', data=top_days, palette='viridis')
    plt.xlabel('Date')
    plt.ylabel('Bike Rentals Count')
    plt.xticks(rotation=45)
    st.pyplot(plt)

    st.caption('Made with 🤩 by Faris')

# Run
if __name__ == '__main__':
    main()
