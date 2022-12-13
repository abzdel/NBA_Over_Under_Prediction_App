import pandas as pd
import re

# get today's over/under for each team from draftkings
df = pd.read_html("https://sportsbook.draftkings.com/leagues/basketball/nba")

# potential problem could occur if draft kings changes format of their html
df = df[0]

# rename column to today instead of tomorrow
# happens due to weird time zone issue when loading in data
df.rename(columns={"Tomorrow": "Today"}, inplace=True)


# function to separate date from team name
def split_team_name(team_and_date_long_string):
    """Splits up the messy "tomorrow" column from our scraped Draft Kings Data.
    Returns time, team abbreviation, and team name."""

    # find date - should be any characters ending with AM or PM
    # NOTE: game times appear to be 5 hours ahead of EST
    # not an issue unless we choose to implement this as a feature
    time = re.search(r"(.+)(AM|PM)", team_and_date_long_string)
    if not time:
        # if game is in progress, ignore
        return None, None, None

    time = time[0]
    # find team name - all characters after the date
    team = re.search(r"(.+)(AM|PM)(.+)", team_and_date_long_string)[3]

    # split abbreviation and team name
    team_abbrev = team.split(" ")[0]
    team_full = team.split(" ")[1]

    return time, team_abbrev, team_full


df[["time", "team_abbrev", "team_full"]] = df.apply(
    lambda x: split_team_name(x["Today"]), axis=1, result_type="expand"
)
df.dropna(inplace=True)


# convert team abbrev to 3 letters if its not


def expand_abbrev(abbrev, name):
    if name == "Lakers":
        return "LAL"
    if name == "Knicks":
        return "NYK"
    if name == "Clippers":
        return "LAC"
    if name == "Spurs":
        return "SAS"
    if name == "Nets":
        return "BRK"
    if name == "Hawks":
        return "ATL"
    if name == "Hornets":
        return "CHO"
    if name == "Pelicans":
        return "NOP"
    if name == "Suns":
        return "PHO"
    if name == "Warriors":
        return "GSW"
    else:
        return abbrev


df["team_abbrev"] = df.apply(
    lambda x: expand_abbrev(x["team_abbrev"], x["team_full"]), axis=1
)


# for example, the first matchup is team abbrev at index 0 and 1
# then 2 and 3, etc.
# we want a function that returns pairs of team names
def find_matchups(df):
    """Finds the matchups in the dataframe.
    Returns a list of tuples with the team abbreviations for each matchup."""
    matchups = []
    for i in range(0, len(df), 2):
        matchups.append((df.iloc[i]["team_abbrev"], df.iloc[i + 1]["team_abbrev"]))
    return matchups


matchups = find_matchups(df)

# convert inner tuples to lists for mutability
matchups = [list(x) for x in matchups]

# insert "vs." in each list
for i in range(len(matchups)):
    matchups[i].insert(1, "vs.")

# turn each list into a string
matchups = [" ".join(x) for x in matchups]

# export matchups
pd.Series(matchups).to_csv("matchups.csv")
