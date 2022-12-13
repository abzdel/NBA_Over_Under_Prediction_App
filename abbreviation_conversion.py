import pandas as pd

df = pd.read_html(
    "https://en.wikipedia.org/wiki/Wikipedia:WikiProject_National_Basketball_Association/National_Basketball_Association_team_abbreviations",
    header=0,
)
df = df[0]
df["teamname"] = df["Franchise"].apply(lambda x: x.split(" ")[-1])
df.rename(columns={"Abbreviation/ Acronym": "abbreviation"}, inplace=True)

df.to_csv("data/abbreviations.csv", index=False)
