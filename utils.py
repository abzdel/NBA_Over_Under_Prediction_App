import pandas as pd
import numpy as np
import os

# data cleaning functions
def home_to_binary(home):
    """function to convert Home column to 0 or 1"""

    if home == "@":
        return 0
    else:
        return 1

def win_to_binary(win):
    """function to convert Win column to 0 or 1"""

    if win == "W":
        return 1
    else:
        return 0

def get_day_of_week(date):
    """function to return day of week (first 3 letters) from date"""
    return date[:3]

# load data, predict, and return results
def load_data(team_num):
    df = pd.read_csv(f"data/team{team_num}_stats.csv")
    return df

def train(df):
    # run train.py file
    os.system("python train.py")

def get_matchup_to_predict():
    # get matchup to predict
    matchup = pd.read_csv("matchup.txt", header=None)
    matchup = str(matchup[0].values[0])

    # split matchup into team1 and team2
    team1 = matchup.split(" ")[0]
    team2 = matchup.split(" ")[-1]

    return team1, team2

def predict(team_num, df):
    # load model
    model = joblib.load(f"models/team{team_num}_model.pkl")

    # get predictions
    predictions = model.predict(df)

    # get average prediction
    avg_prediction = np.mean(predictions)

    return avg_prediction