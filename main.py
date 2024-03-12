import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load the dataset and exclude "WORLD"
def load_data():
    data = pd.read_csv("Forest_Area.csv")
    # Exclude the row where 'Country and Area' is 'WORLD'
    return data[data['Country and Area'] != 'WORLD']

df = load_data()

# Setup of the Streamlit app
st.title('Forest Area Analysis Over Time')

# Display data overview
st.header('Data Overview')
st.write(df.head())

# Allow users to select countries for comparison
countries = df['Country and Area'].unique()
selected_countries = st.multiselect('Select countries to visualize', countries, default=[countries[0]])

# Filter the dataset based on selected countries
filtered_df = df[df['Country and Area'].isin(selected_countries)]

# Visualization
st.header('Forest Area Comparison Over Time')

if not filtered_df.empty:
    # Melt the dataframe to long format for easier plotting
    years_of_interest = ['Forest Area, 1990', 'Forest Area, 2000', 'Forest Area, 2010', 'Forest Area, 2015', 'Forest Area, 2020']
    long_df = pd.melt(filtered_df, id_vars=['Country and Area'], value_vars=years_of_interest,
                      var_name='Year', value_name='Forest Area')
    # Adjust the 'Year' for plotting
    long_df['Year'] = long_df['Year'].str.replace('Forest Area, ', '').astype(int)
    
    # Plotting
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=long_df, x='Year', y='Forest Area', hue='Country and Area', marker='o')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Forest Area (sq km)', fontsize=12)
    plt.title('Forest Area Comparison from 1990 to 2020')
    plt.xticks(rotation=45)
    plt.legend(title='Country and Area', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.gca().invert_yaxis()

    st.pyplot(plt)
else:
    st.write("Please select at least one country to visualize.")
