This is a sports analytics project in the field of cricket. Most existing sports analytics done in the field of cricket is based on match-to-match data (macro level), however, this project aims at micro level analysis that is player by player analysis, to uncover strengths/weakness for a given player

In this project, we have considered 2 international batsmen:
1.	Rohit Sharma (India)
2.	David Warner (Australia)

A novel attempt to devise a model that would predict various attributes of a player’s game based on data collected from each ball (play by play) across multiple games and opponents for 3 years.

Following is a high-level end to end approach:
Data Collection:
	•	Wrangled data from cricbuzz.com service to fetch running commentary in JSON format for all One-day international matches played by each 		player from the year 2016.
	•	Approximate was able to fetch data for 50 matches.
	•	Picked different measures to create the dataset.
	•	Feature engineered new measures.

Exploratory Data Analysis
	•	Used Matplotlib and Seaborn libraries.
	•	Discovered strengths and weaknesses of a player, few were obvious insights, and few weren’t.

Machine Learning Models
	•	Employed Decision tree and Random Forest using Scikit learn.
	•	Tuned hyper parameters and evaluated the performance

Following things are attached in the folder:
	•	The final dataset with all the attributes and new calculated attributes for both the players
	•	Exploratory data analysis uncovering few obvious and few not so obvious insights for each player
	•	Models for each dependent variable, for each player
