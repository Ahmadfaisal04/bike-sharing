import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Bike Sharing Analysis", layout="wide")

# Load data
@st.cache_data
def fetch_data():
    url = 'day.csv'
    df = pd.read_csv(url)
    return df

# Data preprocessing
def preprocess_data(df):
    # Select relevant columns
    df = df[['dteday', 'season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit', 'temp', 'atemp', 'hum', 'cnt']]
    
    # Rename columns for clarity
    df.columns = ['date', 'season', 'year', 'month', 'holiday', 'weekday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'rentals']
    
    # Convert date
    df['date'] = pd.to_datetime(df['date'])
    
    # Map categorical variables
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {1: 'Clear', 2: 'Misty', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
    month_map = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 
                 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    weekday_map = {0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'}
    
    df['season'] = df['season'].map(season_map)
    df['weather'] = df['weather'].map(weather_map)
    df['month'] = df['month'].map(month_map)
    df['weekday'] = df['weekday'].map(weekday_map)
    
    return df

# Main dashboard
def main():
    st.title("🚲 Bike Sharing Data Insights")
    st.markdown("Explore bike rental patterns based on weather, season, and time.")

    # Load and preprocess data
    df = fetch_data()
    df = preprocess_data(df)
    
    # Sidebar for filters
    st.sidebar.header("Filters")
    selected_year = st.sidebar.selectbox("Select Year", options=[2011, 2012], index=0)
    selected_season = st.sidebar.multiselect("Select Season", options=['Spring', 'Summer', 'Fall', 'Winter'], default=['Spring', 'Summer', 'Fall', 'Winter'])
    
    # Filter data
    filtered_df = df[(df['date'].dt.year == selected_year) & (df['season'].isin(selected_season))]
    
    # Dashboard layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Monthly Rental Trends")
        monthly_data = filtered_df.groupby('month')['rentals'].mean().reindex(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        fig = px.bar(x=monthly_data.index, y=monthly_data.values, labels={'x': 'Month', 'y': 'Average Rentals'}, color=monthly_data.values)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Rentals by Weather")
        weather_data = filtered_df.groupby('weather')['rentals'].mean()
        fig = px.pie(values=weather_data.values, names=weather_data.index, title="Rentals Distribution by Weather")
        st.plotly_chart(fig, use_container_width=True)
    
    # Interactive time series
    st.subheader("Daily Rentals Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['rentals'], mode='lines', name='Rentals'))
    fig.update_layout(xaxis_title="Date", yaxis_title="Bike Rentals", hovermode="x")
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary metrics
    st.subheader("Key Metrics")
    avg_rentals = filtered_df['rentals'].mean()
    max_rentals = filtered_df['rentals'].max()
    min_rentals = filtered_df['rentals'].min()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Average Daily Rentals", f"{avg_rentals:.0f}")
    col2.metric("Max Daily Rentals", f"{max_rentals}")
    col3.metric("Min Daily Rentals", f"{min_rentals}")
    
    # Data table
    st.subheader("Raw Data")
    st.dataframe(filtered_df, use_container_width=True)

if __name__ == "__main__":
    main()