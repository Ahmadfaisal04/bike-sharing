# Bike Sharing Data Analysis with Python - Dicoding Submission

## Installation
1. Clone this repository to your local machine:
```
git clone https://github.com/Ahmadfaisal04/bike-sharing.git
```
2. Go to the project directory
```
cd bike-sharing
```
3. Install the required Python packages by running:
```
pip install -r requirements.txt
```

## Usage
1. **Data Wrangling**:
- Data is imported using Pandas from two CSV files: one for daily data and one for hourly data.
- Data quality is assessed through methods like .info(), .isna(), .duplicated(), and .describe().
- Data cleaning involves dropping unnecessary columns and renaming columns for better understanding. Additionally, some numerical values are mapped to categorical labels.
- Data types are converted to appropriate types like datetime and categorical.

2. **Exploratory Data Analysis (EDA)**: 
- Grouping and aggregation operations are performed to understand patterns based on different features like month, weather condition, holiday, weekday, working day, and season.
- Correlation heatmap is plotted to visualize relationships between numerical features.

3. **Visualization**: Run the Streamlit dashboard for interactive data exploration:

```
cd bike-sharing/dashboard
streamlit run dashboard.py
```