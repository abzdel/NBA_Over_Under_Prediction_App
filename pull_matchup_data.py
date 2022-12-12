import pandas as pd
import numpy as np


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