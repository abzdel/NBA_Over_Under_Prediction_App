import pandas as pd
import numpy as np
import os
from datetime import datetime, timezone
import pytz

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

    temp = pd.to_datetime(date[4:])
    temp = str(temp)[:-9]
    return temp

# load data, predict, and return results


def load_data(team_num):
    df = pd.read_csv(f"data/team{team_num}_stats.csv")
    return df


def train(df):
    # run train.py file
    os.system("python train.py")


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def get_matchup_to_predict(team1, team2):
    # scrape data once again
    # will be merged a little differently than before
    # huge function due to the complexities of merging with datetimes here
    # would rather keep everything consistent in one function than exporting/importing it
    # elsewhere and having to deal with issues later
    team1_stats = pd.read_html(
        f"https://www.basketball-reference.com/teams/{team1}/2023_games.html")[0]
    team2_stats = pd.read_html(
        f"https://www.basketball-reference.com/teams/{team2}/2023_games.html")[0]

    # use get date
    team1_stats["Date"] = team1_stats.apply(
        lambda x: get_date(x["Date"]), axis=1)
    team2_stats["Date"] = team2_stats.apply(
        lambda x: get_date(x["Date"]), axis=1)

    team1_stats["Date"] = pd.to_datetime(team1_stats["Date"])
    team2_stats["Date"] = pd.to_datetime(team2_stats["Date"])

    # drop null subset date
    team1_stats.dropna(subset=["Date"], inplace=True)
    team2_stats.dropna(subset=["Date"], inplace=True)

    # apply utc to both
    team1_stats["Date"] = team1_stats.apply(
        lambda x: utc_to_local(x["Date"]), axis=1)
    team2_stats["Date"] = team2_stats.apply(
        lambda x: utc_to_local(x["Date"]), axis=1)

    est = pytz.timezone('US/Eastern')

    # localize each date to est
    team1_stats["Date"] = team1_stats.apply(
        lambda x: est.localize(x["Date"]), axis=1)
    team2_stats["Date"] = team2_stats.apply(
        lambda x: est.localize(x["Date"]), axis=1)

    timezone = pytz.timezone('US/Eastern')
    now = datetime.now(tz=timezone)
    now = now.strftime("%Y %m %d")
    team1_stats = team1_stats[team1_stats["Date"] == now]
    team2_stats = team2_stats[team2_stats["Date"] == now]

    ranks = pd.read_csv("data/ranks.csv")

    team1_stats = team1_stats.merge(
        ranks, how="left", left_on="Date", right_on="Date")


def predict(team_num, df):
    # load model
    model = joblib.load(f"models/team{team_num}_model.pkl")

    # get predictions
    predictions = model.predict(df)

    # get average prediction
    avg_prediction = np.mean(predictions)

    return avg_prediction
