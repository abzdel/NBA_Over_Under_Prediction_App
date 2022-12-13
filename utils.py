import pandas as pd
import numpy as np
import os
import datetime

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

def get_date(date):
    """truncates day of week out of column, returns datetime object"""
    return datetime.datetime.strptime(date[4:], "%b %d, %Y")

# load data, predict, and return results
def load_data(team_num):
    df = pd.read_csv(f"data/team{team_num}_stats.csv")
    return df

def train(df):
    # run train.py file
    os.system("python train.py")

def get_matchup_to_predict(team1, team2):
    # scrape data once again
    # will be merged a little differently than before
    team1_stats = pd.read_html(f"https://www.basketball-reference.com/teams/{team1}/2023_games.html")[0]
    team2_stats = pd.read_html(f"https://www.basketball-reference.com/teams/{team2}/2023_games.html")[0]

    # get date function
    team1_stats["Date"] = team1_stats["Date"].apply(get_date)
    team2_stats["Date"] = team2_stats["Date"].apply(get_date)

    # ensure games are from today
    today = datetime.today().strftime("%b %d, %Y")
    team1_stats = team1_stats[team1_stats["Date"] == today]
    team2_stats = team2_stats[team2_stats["Date"] == today]

    if not today:
        print("No games today.")
        exit(0)

    ranks = pd.read_csv("data/ranks.csv")

    team1_stats = team1_stats.merge(ranks, how="left", left_on="Date", right_on="Date")



def predict(team_num, df):
    # load model
    model = joblib.load(f"models/team{team_num}_model.pkl")

    # get predictions
    predictions = model.predict(df)

    # get average prediction
    avg_prediction = np.mean(predictions)

    return avg_prediction