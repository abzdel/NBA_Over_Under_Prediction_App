[![Makefile CI](https://github.com/abzdel/NBA_Over_Under_Prediction_App/actions/workflows/makefile.yml/badge.svg)](https://github.com/abzdel/NBA_Over_Under_Prediction_App/actions/workflows/makefile.yml)

# Description
This repository contains an NBA over/under prediction app built with Python and Streamlit. It uses a linear regression model to make predictions on the over/under bets for NBA games. The user simply chooses which game they'd like predictions on, and the app automatically scrapes new data about the team, makes predictions, and returns the predicted total score for the user.

# Project Architecture
![final_architecture drawio](https://user-images.githubusercontent.com/55398496/207462993-51db9219-bf31-4d77-922f-ae36cd092ced.png)


# How Does the Code Work?
Here's a secondary diagram, showing what's happening when a team is selected from the dropdown in our app:
![final_code_diagram drawio](https://user-images.githubusercontent.com/55398496/207474113-96efe05e-0a53-47d5-9e3a-22df7743bfba.png)


As can be seen above, our main() function calls various other python files and functions to perform a variety of tasks. These include:
1) Automatically scraping the most recent data for teams in our matchup
2) Re-training the model to ensure we have up to date features<br>
  For example, our teams' **weekly power ranking** is a feature in the model.<br>
  This won't be much use if it's not completely up to date
3) Returning predictions to the app
<br>
You may also notice that there are two places this can be pushed - to our EC2 instance, or to our local app. I don't plan to leave this running on a deployment service like App Runner, so the following tutorial will deal with running this for yourself locally!

# How to Run the App

1) Clone the repo
```python
git clone https://github.com/abzdel/NBA_Over_Under_Prediction_App.git
```
2) Setup - Install the required packages
```python
make all
```
3) Run the application (automatically scrapes data + trains model)
```python
streamlit run app.py --server.enableCORS=false
```
<br>
After this, we simply select the matchup we want and get our predicted total score (score from both teams combined)

## Disclaimer
Please don't actually use the linear regression to place bets on games - the emphasis of this project is the deployment of the application and the ability to build a basic MLOps system. I spent very little time feature engineering and working with the performance metrics of the models. However, if anyone has an interest in changing the model and making it more feasible to use - I'd be happy to help in the process however I can, so don't hesitate to reach out!
