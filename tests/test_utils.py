import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from utils import *

import pandas as pd
import numpy as np

class TestUtils():
    def test_home_to_binary(self):
        df = pd.read_csv("data/team1_stats.csv")
        df["Home"] = df["Home"].apply(home_to_binary)
        assert df["Home"].isin([0, 1]).all(), "Home column should only contain 0s and 1s"

        assert (home_to_binary("@") == 0), "Home column should be 0 if @"
        assert (home_to_binary("-") == 1), "Home column should be 1"
        assert (home_to_binary(np.nan) == 1), "Home column should be 1"

    def test_win_to_binary(self):

        assert (win_to_binary("W") == 1), "Win column should be 1 if W"
        assert (win_to_binary("L") == 0), "Win column should be 0"
        assert (win_to_binary(np.nan) == 0), "Win column should be 0"

    def test_get_day_of_week(self):

        assert (get_day_of_week("Mon, Oct 19, 2020") == "Mon"), "Day column should be Mon"
        assert (get_day_of_week("Tue, Oct 20, 2020") == "Tue"), "Day column should be Tue"
        assert (get_day_of_week("Wed, Oct 21, 2020") == "Wed"), "Day column should be Wed"
        assert (get_day_of_week("Thu, Oct 22, 2020") == "Thu"), "Day column should be Thu"
        assert (get_day_of_week("Fri, Oct 23, 2020") == "Fri"), "Day column should be Fri"
        assert (get_day_of_week("Sat, Oct 24, 2020") == "Sat"), "Day column should be Sat"
        assert (get_day_of_week("Sun, Oct 25, 2020") == "Sun"), "Day column should be Sun"

    def test_get_date(self):
 
        assert (get_date("Mon, Oct 19, 2020") == "2020-10-19"), "Date column should be 2020-10-19"
        assert (get_date("Tue, Oct 20, 2020") == "2020-10-20"), "Date column should be 2020-10-20"
        assert (get_date("Wed, Oct 21, 2020") == "2020-10-21"), "Date column should be 2020-10-21"
        assert (get_date("Thu, Oct 22, 2020") == "2020-10-22"), "Date column should be 2020-10-22"
        assert (get_date("Fri, Oct 23, 2020") == "2020-10-23"), "Date column should be 2020-10-23"
        assert (get_date("Sat, Oct 24, 2020") == "2020-10-24"), "Date column should be 2020-10-24"
        assert (get_date("Sun, Oct 25, 2020") == "2020-10-25"), "Date column should be 2020-10-25"


# run all tests

test = TestUtils()
test.test_home_to_binary()
test.test_win_to_binary()
test.test_get_day_of_week()
test.test_get_date()
print("All tests passed!")