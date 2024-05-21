import streamlit as st
import pickle
import pandas as pd

teams = ['Sunrisers Hyderabad',
         'Mumbai Indians',
         'Royal Challengers Bangalore',
         'Kolkata Knight Riders',
         'Kings XI Punjab',
         'Chennai Super Kings',
         'Rajasthan Royals',
         'Delhi Capitals']

cities = ['Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 'Jaipur',
          'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 'East London', 'Johannesburg',
          'Kimberley', 'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam',
          'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru']

pipe = pickle.load(open('pipe.pkl', 'rb'))
st.title('Match Winning Predictor')

initial_state = st.experimental_get_query_params()

col1, col2, col3 = st.columns(3)

with col1:
    batting_team = st.selectbox('Select the batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select the bowling team', sorted(teams))

selected_city = st.selectbox('Select host city', sorted(cities))


target_range = list(range(100, 281))
target = st.selectbox('T20 Target', target_range)



#col1, col2, col3 = st.columns(3)
#with col1:
#    pitch_conditions = st.selectbox('Pitch conditions', ['Batting-friendly', 'Spinning track', 'Pace-friendly'])
#with col2:
#    weather_conditions = st.selectbox('Weather conditions', ['Sunny', 'Partly cloudy', 'Overcast', 'Rainy'])

#with col3:
#    match_context = st.selectbox('Match context', ['League match', 'Knockout match', 'Final', 'Playoff'])

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Score')
with col4:
    overs = st.number_input('Overs completed', min_value=0, max_value=20)
    if overs > 20:
        st.warning('Maximum overs allowed is 20')
with col5:
    wickets = st.number_input('Wickets out', min_value=0, max_value=10)
    if wickets > 10:
        st.warning('Maximum wickets allowed is 10')

if st.button('Predict Probability'):
    runs_left = target - score
    balls_left = 120 - (overs*6)
    wickets = 10 - wickets
    crr = score/overs
    rrr = (runs_left*6)/balls_left

    input_df = pd.DataFrame({'batting_team':[batting_team],'bowling_team':[bowling_team],'city':[selected_city], 'runs_left':[runs_left],'balls_left':[balls_left],'wickets':[wickets],'total_runs_x':[target],'crr':[crr],'rrr':[rrr]})

    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]
    st.header(batting_team + "- " + str(round(win*100)) + "%")
    st.header(bowling_team + "- " + str(round(loss*100)) + "%")

