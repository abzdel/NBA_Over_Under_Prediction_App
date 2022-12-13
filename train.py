# imports
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

print("Training models...")
# read data
team1_stats = pd.read_csv("data/team1_stats.csv")
team2_stats = pd.read_csv("data/team2_stats.csv")

features = ["Rk", "Chg", "Home"]

# train and export team 1 model
X = team1_stats[features]
y = team1_stats["Tm"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, "models/team1_model.pkl")
print("Team 1 model trained and saved.")

# train and export team 2 model
X = team2_stats[features]
y = team2_stats["Tm"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X, y)
joblib.dump(model, "models/team2_model.pkl")
print("Team 2 model trained and saved.")
