import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Read the CSV files for each season
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load data for each season
file_paths = ["2020_IPL.csv", "2021_IPL.csv", "2022_IPL.csv","orange_cap&purple_cap.csv"]
data_seasons = [load_data(file_path) for file_path in file_paths]

# Read orange_cap_purple_cap.csv
orange_purple_data = pd.read_csv("orange_cap&purple_cap.csv")

# Display the Topic name with custom style
st.markdown("<h1 style='font-size: 42px; font-weight: bold;'>Youth League Data Analysis - Multiple Seasons</h1>", unsafe_allow_html=True)

# Select season
selected_season = st.selectbox(
    'Select Season:',
    ['Season 2020', 'Season 2021', 'Season 2022']
)

# Determine selected season index
season_index = -1
if selected_season:
    season_year = int(selected_season.split()[1])  # Extract year from selected season
    if 2020 <= season_year <= 2022:  # Check if the selected year is within the range
        season_index = season_year - 2020  # Calculate index based on year

# Get data for selected season if the index is valid
data = None
if 0 <= season_index < len(data_seasons):
    data = data_seasons[season_index]

# Choose an option
option = st.selectbox(
    'Choose an option:',
    ('Points Table', 'Qualified Teams', 'Most Wins Team', 'Orange Cap Player', 'Purple Cap Player', 'List of Players', 'Statistical Data')
)

# Display information only if both season and option are chosen
if selected_season and option:
    # Display points table for selected season
    if option == 'Points Table':
        st.write(f"Points Table for {selected_season}:")
        if data is not None and 'Team' in data.columns and 'Matches Won' in data.columns and 'Matches Lost' in data.columns:
            points_table = data[['Team', 'Points', 'Matches Won', 'Matches Lost']]
            st.write(points_table)
        else:
            st.write("Data does not contain necessary information.")
    # Display qualified teams for selected season
    elif option == 'Qualified Teams':
        st.write(f"Top 4 Qualified Teams for {selected_season}:")
        if data is not None and 'Team' in data.columns:
            qualified_teams = data.groupby('Team')['Points'].sum().nlargest(4)
            st.write(qualified_teams)
        else:
            st.write("Data does not contain 'Team' information.")
    # Which team has won the most matches in the selected season?
    elif option == 'Most Wins Team':
        st.write(f"Team with Most Wins in {selected_season}:")
        if data is not None and 'Team' in data.columns:
            most_wins_team = data.groupby('Team')['Points'].sum().idxmax()
            st.write(most_wins_team)
        else:
            st.write("Data does not contain necessary information.")
    # Which player scored the most runs in the selected season (Orange Cap)?
    elif option == 'Orange Cap Player':
       st.write(f"Orange Cap Player (Highest Runs Scorer) in {selected_season}:")
       orange_cap_data = orange_purple_data[orange_purple_data['Season'] == selected_season]['Orange Cap Player']
       if not orange_cap_data.empty:
            orange_cap_player = orange_cap_data.iloc[0]
            st.write(orange_cap_player)
       else:
             st.write("No data available for the selected season.")
    # Which player has taken the highest number of wickets in the selected season (Purple Cap)?
    elif option == 'Purple Cap Player':
        st.write(f"Purple Cap Player (Highest Wickets Taken) in {selected_season}:")
        if 'Purple Cap Player' in orange_purple_data.columns:
            purple_cap_player = orange_purple_data[orange_purple_data['Season'] == selected_season]['Purple Cap Player'].iloc[0]
            st.write(purple_cap_player)
        else:
            st.write("Data does not contain necessary information.")
    # Display the list of players of each team for selected season
    elif option == 'List of Players':
        st.write(f"List of Players of Each Team in {selected_season}:")
        if data is not None and 'Team' in data.columns and 'Players' in data.columns:
            # Ensure 'Players' column is not empty
            if not data['Players'].isnull().all():
                # Split the players string into a list
                data['Players'] = data['Players'].apply(lambda x: x.split(','))
                # Explode the list of players to separate rows
                exploded_data = data.explode('Players')
                # Group by team and aggregate players
                team_players = exploded_data.groupby('Team')['Players'].apply(lambda x: ', '.join(x)).reset_index()
                st.write(team_players)
            else:
                st.write("Players information is empty.")
        else:
            st.write("Data does not contain necessary information.")
    # Display statistical data of the points table using matplotlib
    elif option == 'Statistical Data':
        st.write("Statistical Data of Points Table:")
        if data is not None and 'Points' in data.columns:
            points_table = data.groupby('Team')['Points'].sum().sort_values(ascending=False)
            plt.figure(figsize=(10, 6))
            points_table.plot(kind='bar', color='skyblue')
            plt.title('Points Distribution')
            plt.xlabel('Team')
            plt.ylabel('Points')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(plt)
        else:
            st.write("Data does not contain 'Points' information.")