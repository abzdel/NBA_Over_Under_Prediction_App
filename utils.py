import pandas as pd
import numpy as np
import os
from datetime import datetime, timezone
import pytz
import joblib
import streamlit as st

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


def train():
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
        f"https://www.basketball-reference.com/teams/{team1}/2023_games.html"
    )[0]
    team2_stats = pd.read_html(
        f"https://www.basketball-reference.com/teams/{team2}/2023_games.html"
    )[0]

    # use get date
    team1_stats["Date"] = team1_stats.apply(lambda x: get_date(x["Date"]), axis=1)
    team2_stats["Date"] = team2_stats.apply(lambda x: get_date(x["Date"]), axis=1)

    team1_stats["Date"] = pd.to_datetime(team1_stats["Date"])
    team2_stats["Date"] = pd.to_datetime(team2_stats["Date"])

    # drop null subset date
    team1_stats.dropna(subset=["Date"], inplace=True)
    team2_stats.dropna(subset=["Date"], inplace=True)

    # apply utc to both
    team1_stats["Date"] = team1_stats.apply(lambda x: utc_to_local(x["Date"]), axis=1)
    team2_stats["Date"] = team2_stats.apply(lambda x: utc_to_local(x["Date"]), axis=1)

    est = pytz.timezone("US/Eastern")

    # localize each date to est
    team1_stats["Date"] = team1_stats.apply(lambda x: est.localize(x["Date"]), axis=1)
    team2_stats["Date"] = team2_stats.apply(lambda x: est.localize(x["Date"]), axis=1)

    timezone = pytz.timezone("US/Eastern")
    now = datetime.now(tz=timezone)
    now = now.strftime("%Y %m %d")
    team1_stats = team1_stats[team1_stats["Date"] == now]
    team2_stats = team2_stats[team2_stats["Date"] == now]

    # shorten opponent teamname for ranks join
    team1_stats["opp_teamname"] = team1_stats["Opponent"].apply(
        lambda x: x.split(" ")[-1]
    )
    team2_stats["opp_teamname"] = team2_stats["Opponent"].apply(
        lambda x: x.split(" ")[-1]
    )

    ranks = pd.read_csv("data/ranks.csv")

    # merge ranks
    team1_stats = team1_stats.merge(
        ranks, how="left", left_on="opp_teamname", right_on="Teams"
    )
    team2_stats = team2_stats.merge(
        ranks, how="left", left_on="opp_teamname", right_on="Teams"
    )

    # home to binary
    team1_stats["Home"] = team1_stats["Unnamed: 5"].apply(lambda x: home_to_binary(x))
    team2_stats["Home"] = team2_stats["Unnamed: 5"].apply(lambda x: home_to_binary(x))

    # choose final columns
    team1_stats = team1_stats[["Rk", "Chg", "Home"]]
    team2_stats = team2_stats[["Rk", "Chg", "Home"]]

    return team1_stats, team2_stats


def predict(team1_stats, team2_stats):
    # load model
    model1 = joblib.load("models/team1_model.pkl")
    model2 = joblib.load("models/team2_model.pkl")

    # get predictions
    predictions1 = model1.predict(team1_stats)
    predictions2 = model2.predict(team2_stats)

    # sum both predictions for over/under
    total = int(predictions1 + predictions2)

    if total:
        st.success(f"predicted score: {total}:checkered_flag:")

    return total


def main(matchup):

    pd.Series(matchup).to_csv("matchup.txt", index=False)

    matchup = pd.read_csv("matchup.txt", header=None)
    # split matchup into team1 and team2
    team1 = matchup.loc[1][0].split(" ")[0]
    team2 = matchup.loc[1][0].split(" ")[-1]

    # call pull matchup data file
    os.system("python pull_matchup_data.py")

    # train model
    train()

    # get matchup to predict
    print(team1, team2)
    team1_stats, team2_stats = get_matchup_to_predict(team1, team2)

    # get predictions
    total = predict(team1_stats, team2_stats)
    total = int(total)
    # print results
    print(f"Predicted score: {total}")


if __name__ == "__main__":
    main()
