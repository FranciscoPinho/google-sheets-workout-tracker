import requests
from datetime import datetime
NUTRITIONIX_APP_ID = "30ae04b8"
NUTRITIONIX_API_KEY = "43d4a492a559f8640bf53304113f094d"
GOOGLE_SHEETS_API_ENDPOINT = "https://api.sheety.co/259c16015c49cec2d6ebb7679d9eb7fd/myWorkouts/workouts"


class Workout:
    def __init__(self, date, time, exercise, duration, calories):
        self.date = date
        self.time = time
        self.exercise = exercise
        self.duration = duration
        self.calories = calories


def get_exercise_details(query: str) -> dict:
    headers = {
        "x-app-id": NUTRITIONIX_APP_ID,
        "x-app-key": NUTRITIONIX_API_KEY,
        "Content-Type": "application/json"
    }
    body = {
        "query": query
    }
    response = requests.post(url="https://trackapi.nutritionix.com/v2/natural/exercise", json=body, headers=headers)
    return response.json()


def add_row_google_sheets(workout: Workout) -> dict:
    body = {
        "workout": {
            "date": workout.date,
            "time": workout.time,
            "exercise": workout.exercise,
            "duration": workout.duration,
            "calories": workout.calories
        }
    }
    response = requests.post(url=GOOGLE_SHEETS_API_ENDPOINT, json=body)
    return response.json()


workout_query = input("Tell me which exercises you did: ")
workout_details = get_exercise_details(workout_query)
for exercise in workout_details["exercises"]:
    now = datetime.now()
    new_workout = Workout(
        now.strftime("%d/%m/%Y"),
        now.strftime("%X"),
        exercise["name"].title(),
        exercise["duration_min"],
        exercise["nf_calories"]
    )
    print(add_row_google_sheets(new_workout))