import streamlit as st
import numpy as np
import pandas as pd
import sklearn
from utils import *
import os

# get todays matchups from python file
os.system("python get_todays_matchups.py")



matchups = pd.read_csv("matchups.csv")
matchups = matchups["0"].tolist()

st.title("Predicting over/under of a game :basketball:")
st.write("This is a machine learning model that predicts the over/under of a game based on the teams' statistics.")
cur_matchup = st.selectbox(label="Choose a team from the dropdown", options=matchups)
st.write(f"Loading results for {cur_matchup}...")


# invoke main command
main(cur_matchup)
#st.button("Predict total points", on_click=main(cur_matchup))

# line to run
# streamlit run app.py --server.enableCORS=false
# from https://docs.streamlit.io/knowledge-base/deploy/remote-start