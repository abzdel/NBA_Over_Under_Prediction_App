import pandas as pd

class MatchupTests():
    def test_matchup(self):
        matchups = pd.read_csv("matchups.csv")
        matchups = matchups["0"]
        for matchup in matchups:
            assert len(matchup.split(" ")) == 3, "Matchup should be in the format of 'Team1 vs. Team2'"



tests = MatchupTests()
tests.test_matchup()
print("All tests passed!")
