import streamlit as st
import numpy as np
import pandas as pd
import joblib
import sklearn


# open pickle file with joblib
model = joblib.load('rf_model.pkl')


st.title("Predicting over/under of a game :basketball:")
st.write("This is a machine learning model that predicts the over/under of a game based on the teams' statistics.")


# line to run
# streamlit run my_app.py --server.enableCORS=false
# from https://docs.streamlit.io/knowledge-base/deploy/remote-start