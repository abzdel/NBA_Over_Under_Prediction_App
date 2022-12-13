import pandas as pd
import numpy as np
from utils import *


matchup = pd.read_csv("matchup.txt", header=None)
matchup = str(matchup[0].values[0])
print(f"matchup is: {matchup}")


# split matchup into team1 and team2
team1 = matchup.split(" ")[0]
team2 = matchup.split(" ")[-1]


# scrape from basketball reference for both teams
team1_stats = pd.read_html(f"https://www.basketball-reference.com/teams/{team1}/2023_games.html")
team2_stats = pd.read_html(f"https://www.basketball-reference.com/teams/{team2}/2023_games.html")

# cleaning step to get correct form
team1_stats = team1_stats[0]
team2_stats = team2_stats[0]


# more data cleaning steps
team1_stats.dropna(subset={"Tm"}, inplace=True) # null scores haven't happened yet
team1_stats.drop(columns={"Unnamed: 3", "Unnamed: 4", "Unnamed: 8", "Notes"}, inplace=True) # drop columns we don't need
team1_stats = team1_stats[team1_stats["Date"] != "Date"] # remove header row showing up as a game
team1_stats.rename(columns={"Unnamed: 5": "Home", "Unnamed: 7": "Win"}, inplace=True)

# do above steps for team2
team2_stats.dropna(subset={"Tm"}, inplace=True)
team2_stats.drop(columns={"Unnamed: 3", "Unnamed: 4", "Unnamed: 8", "Notes"}, inplace=True)
team2_stats = team2_stats[team2_stats["Date"] != "Date"]
team2_stats.rename(columns={"Unnamed: 5": "Home", "Unnamed: 7": "Win"}, inplace=True)


team1_stats["Home"] = team1_stats.apply(lambda x: home_to_binary(x["Home"]), axis=1)
team1_stats["Win"] = team1_stats.apply(lambda x: win_to_binary(x["Win"]), axis=1)
team1_stats["Day"] = team1_stats.apply(lambda x: get_day_of_week(x["Date"]), axis=1)

# set data types
team1_stats["Tm"] = team1_stats["Tm"].astype(int)
team1_stats["Opp"] = team1_stats["Opp"].astype(int)
team1_stats["W"] = team1_stats["W"].astype(int)
team1_stats["L"] = team1_stats["L"].astype(int)

# do same for team2
team2_stats["Home"] = team2_stats.apply(lambda x: home_to_binary(x["Home"]), axis=1)
team2_stats["Win"] = team2_stats.apply(lambda x: win_to_binary(x["Win"]), axis=1)
team2_stats["Day"] = team2_stats.apply(lambda x: get_day_of_week(x["Date"]), axis=1)

team2_stats["Tm"] = team2_stats["Tm"].astype(int)
team2_stats["Opp"] = team2_stats["Opp"].astype(int)
team2_stats["W"] = team2_stats["W"].astype(int)
team2_stats["L"] = team2_stats["L"].astype(int)

# load in ranks, join
ranks = pd.read_html("https://www.cbssports.com/nba/powerrankings/")
ranks = ranks[0]

# clean ranks, rename note col
ranks["Chg"] = ranks["Chg"].apply(lambda x: 0 if x == "--" else x)
ranks.rename(columns={"Unnamed: 2": "Note"}, inplace=True) # may incorporate sentiment analysis into model

team1_stats["teamname"] = team1_stats["Opponent"].apply(lambda x: x.split(" ")[-1])
team2_stats["teamname"] = team2_stats["Opponent"].apply(lambda x: x.split(" ")[-1])

team1_stats = team1_stats.merge(ranks, how="left", left_on="teamname", right_on="Teams")
team2_stats = team2_stats.merge(ranks, how="left", left_on="teamname", right_on="Teams")


team1_stats = team1_stats[["Rk", "Chg", "Home", "Tm"]]
team2_stats = team2_stats[["Rk", "Chg", "Home", "Tm"]]

team1_stats.dropna(inplace=True)
team2_stats.dropna(inplace=True)

# export both to csv
team1_stats.to_csv("data/team1_stats.csv", index=False)
team2_stats.to_csv("data/team2_stats.csv", index=False)

# export ranks
ranks.to_csv("data/ranks.csv", index=False)