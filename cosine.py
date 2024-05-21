import streamlit as st
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

player_metrics = pickle.load(open('player_metric.pkl', 'rb'))
player_metric = pd.DataFrame(player_metrics)

def find_similar_player(input_player_name, team_players, num_similar_players=3):
    input_player_features = player_metric[player_metric['players'] == input_player_name][['runs_scored', 'batting_strike_rate', 'economy_rate']].values
    team_player_features = player_metric[player_metric['players'].isin(team_players)][['runs_scored', 'batting_strike_rate', 'economy_rate']].values

    if len(input_player_features) == 0 or len(team_player_features) == 0:
        return "Player not found or no team players selected."

    similarities = cosine_similarity(input_player_features, team_player_features)
    most_similar_indices = similarities.argsort()[0][-num_similar_players:][::-1]
    most_similar_players = [team_players[idx] for idx in most_similar_indices]
    return most_similar_players


def validate_selections(selections, min_count, max_count):
    if len(selections) < min_count:
        st.warning(f"Please select at least {min_count} players.")
    elif len(selections) > max_count:
        st.warning(f"More than {max_count} players selected.",icon="⚠️")
        return selections[:max_count]
    return selections

def calculate_average_rating(selected_players):
    selected_players_ratings = player_metric[player_metric['players'].isin(selected_players)]
    average_rating = selected_players_ratings['player_rating'].mean()
    return average_rating

def predict_winning_team(team1_average_rating, team2_average_rating):
    if team1_average_rating > team2_average_rating:
        return "Team 1"
    elif team1_average_rating < team2_average_rating:
        return "Team 2"
    else:
        return "Draw"

def calculate_winning_percentage(team_rating, total_performance):
    return (team_rating / total_performance) * 100


def main():
    st.title("Team Selection and Match Simulation")

    num_teams = st.number_input("Enter the number of teams:", min_value=2, max_value=10, step=1)
    teams = []
    for i in range(1, num_teams + 1):
        team_name = st.text_input(f"Enter the name of team {i}:")
        teams.append(team_name)

    st.header("Team Formation")
    team1 = st.selectbox("Select Team 1:", teams)
    team2 = st.selectbox("Select Team 2:", [team for team in teams if team != team1])

    st.write(f"Team 1: {team1}")
    st.write(f"Team 2: {team2}")

    st.header("Player Selection")

    col1, col2 = st.columns(2)

    with col1:
        team1_players = st.multiselect(f"Select 11 players for {team1}:", player_metric['players'].values, key=f"{team1}team1_players")
        team1_players = validate_selections(team1_players, min_count=11, max_count=11)
        st.write(f"Selected players for {team1}: {team1_players}")

    with col2:
        team2_players = st.multiselect(f"Select 11 players for {team2}:", player_metric['players'].values, key=f"{team2}team2_players")
        team2_players = validate_selections(team2_players, min_count=11, max_count=11)
        st.write(f"Selected players for {team2}: {team2_players}")

    st.header("Player Performances")

    if len(team1_players) == 11 and len(team2_players) == 11:
        if st.button("Calculate Average Ratings"):
            team1_average_rating = calculate_average_rating(team1_players)
            team2_average_rating = calculate_average_rating(team2_players)

            st.write("Average Rating for Team 1:", team1_average_rating)
            st.write("Average Rating for Team 2:", team2_average_rating)

            total_performance = team1_average_rating + team2_average_rating
            winning_percentage_team1 = calculate_winning_percentage(team1_average_rating, total_performance)
            winning_percentage_team2 = calculate_winning_percentage(team2_average_rating, total_performance)

            st.write(f"Winning Percentage for {team1}: {winning_percentage_team1:.2f}%")
            st.write(f"Winning Percentage for {team2}: {winning_percentage_team2:.2f}%")

            st.title("Winning team is:")

            winning_team = predict_winning_team(team1_average_rating, team2_average_rating)
            st.write(
                f"<div style='text-align: center;background-color:#228B22; padding: 5px ; font-size: larger;color:black;font-weight: bold'>{winning_team}</div>",
                unsafe_allow_html=True)


    st.header("Player Recommendation")

    selected_player_name = st.text_input("Enter the name of a selected player:", "")
    if st.button("Get Similar Player Recommendations"):

        if selected_player_name:
            if selected_player_name in team1_players:
                similar_player = find_similar_player(selected_player_name, team1_players)
                st.write(f"Similar player for {selected_player_name} in {team1}: {similar_player}")
            elif selected_player_name in team2_players:
                similar_player = find_similar_player(selected_player_name, team2_players)
                st.write(f"Similar player for {selected_player_name} in {team2}: {similar_player}")
            else:
                st.warning(f"{selected_player_name} is not in any of the selected teams.")
        else:
            st.warning("Please enter the name of a selected player.")

if __name__ == "__main__":
    main()
