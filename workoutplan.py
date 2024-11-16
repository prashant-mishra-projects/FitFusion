import streamlit as st
import pandas as pd
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_config import firebase_admin

# cred = credentials.Certificate('gym-app-minor-project-da12df6a9c60.json')
# firebase_admin.initialize_app(cred)


db = firestore.client()

def add_workout(user_id, day, exercise_name, reps, sets, weight):
    workout_data = {
        "exercise_name": exercise_name,
        "reps": reps,
        "sets": sets,
        "weight": weight,
    }
    db.collection("users").document(user_id).collection("days").document(day).collection("workouts").add(workout_data)

def delete_workout(user_id, day, workout_id):
    db.collection("users").document(user_id).collection("days").document(day).collection("workouts").document(workout_id).delete()

def update_workout(user_id, day, workout_id, reps, sets):
    workout_ref = db.collection("users").document(user_id).collection("days").document(day).collection("workouts").document(workout_id)
    workout_ref.update({
        "reps": reps,
        "sets": sets
    })

def get_recommendations(goal):
    recommendations = {
        "Strength": [("Bench Press", 8, 4, 60), ("Deadlift", 5, 4, 80), ("Squats", 10, 3, 70)],
        "Endurance": [("Running", 30, 1, 0), ("Cycling", 45, 1, 0), ("Rowing", 20, 1, 0)],
        "Flexibility": [("Yoga", 60, 1, 0), ("Stretching", 15, 1, 0), ("Pilates", 30, 1, 0)],
    }
    return recommendations.get(goal, [])

def app():
    if st.session_state.username == '':
        st.warning("Login to view your workout plans.")
    else:
        user_id = st.session_state.username
        st.title(f"📝 Workout Planner for :green[{user_id}] ")

        day = st.selectbox("Select Day", ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])

        # Workout recommendation based on user goal
        goal = st.selectbox("Choose Your Goal", ["Strength", "Endurance", "Flexibility"])
        recommendations = get_recommendations(goal)
        
        

        # Form to add a new workout
        with st.form("add_workout_form"):
            exercise_name = st.text_input("Exercise Name")
            reps = st.number_input("Reps", min_value=1)
            sets = st.number_input("Sets", min_value=1)
            weight = st.number_input("Weight (kg)", min_value=0)
            add_button = st.form_submit_button("Add Workout")

            if add_button:
                if not exercise_name.strip():
                    st.warning("Please enter an exercise name.")
                else:
                    add_workout(user_id, day, exercise_name, reps, sets, weight)
                    st.success(f"Added {exercise_name} to {day}!")
        
        if recommendations:
            st.subheader(f"Recommended Workouts for {goal}")
            for exercise, reps, sets, weight in recommendations:
                if st.button(f"Add {exercise} ({reps} reps, {sets} sets, {weight} kg) to {day}", key=f"rec_{exercise}"):
                    add_workout(user_id, day, exercise, reps, sets, weight)
                    st.success(f"Added {exercise} to {day} based on your {goal} goal!")

        # Display existing workouts for the selected day in a table format
        st.subheader(f"Workouts for {day}")
        workouts_ref = db.collection("users").document(user_id).collection("days").document(day).collection("workouts")
        workouts = workouts_ref.stream()

        # Prepare a list to display the workouts in a table
        workout_list = []
        for workout in workouts:
            workout_data = workout.to_dict()
            workout_list.append({
                "Exercise": workout_data['exercise_name'],
                "Reps": workout_data['reps'],
                "Sets": workout_data['sets'],
                "Weight (kg)": workout_data['weight'],
                "Workout ID": workout.id
            })

        # Display the workouts in a table using Pandas DataFrame
        if workout_list:
            workout_df = pd.DataFrame(workout_list)
            st.dataframe(workout_df)

            # Modify reps or sets
            for index, workout in workout_df.iterrows():
                workout_id = workout["Workout ID"]
                st.write(f"Update {workout['Exercise']}")

                new_reps = st.number_input(f"New Reps for {workout['Exercise']}", min_value=1, value=workout['Reps'], key=f"reps_{workout_id}")
                new_sets = st.number_input(f"New Sets for {workout['Exercise']}", min_value=1, value=workout['Sets'], key=f"sets_{workout_id}")

                if st.button(f"Update {workout['Exercise']}", key=f"update_button_{workout_id}"):
                    update_workout(user_id, day, workout_id, new_reps, new_sets)
                    st.success(f"Updated {workout['Exercise']} to {new_reps} reps, {new_sets} sets!")

                if st.button(f"Delete {workout['Exercise']}", key=f"delete_button_{workout_id}"):
                    delete_workout(user_id, day, workout_id)
                    st.success(f"Deleted {workout['Exercise']} from {day}")
        else:
            st.write("No workouts added for this day yet.")
