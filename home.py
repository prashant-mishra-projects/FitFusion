import streamlit as st
import pandas as pd
import plotly.express as px
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_config import firebase_admin

# Initialize Firebase connection (uncomment if not initialized in another file)
# cred = credentials.Certificate('gym-app-minor-project-da12df6a9c60.json')
# firebase_admin.initialize_app(cred)


db = firestore.client()

def get_total_workouts(user_id):
    workout_counts = {}
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    for day in days:
        workouts_ref = db.collection("users").document(user_id).collection("days").document(day).collection("workouts")
        workouts = workouts_ref.stream()
        
        # Count workouts for each day
        workout_counts[day] = sum(1 for _ in workouts)
    
    return workout_counts

def app():
    st.title("🏋️ Dashboard")
    
    if "username" not in st.session_state:
        st.session_state["username"] = ""

    if st.session_state.username == '':
        st.warning("Login to view your workout dashboard.")
    else:
        user_id = st.session_state.username
        st.header(f"Welcome, {user_id}!")

        # Retrieve workout counts
        workout_counts = get_total_workouts(user_id)
        total_workouts = sum(workout_counts.values())
        
        # Display total workouts
        st.metric(label="Total Workouts Completed", value=total_workouts)

        # Let the user select the chart type
        chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart", "Line Chart"])

        days = list(workout_counts.keys())
        counts = list(workout_counts.values())
        
        # Display the selected chart type
        if chart_type == "Bar Chart":
            st.subheader("Workouts Per Day - Bar Chart")
            fig = px.bar(
                x=days,
                y=counts,
                labels={'x': 'Day of the Week', 'y': 'Number of Workouts'},
                title="Workouts Distribution Over the Week"
            )
            st.plotly_chart(fig)
        
        elif chart_type == "Pie Chart":
            st.subheader("Workout Distribution - Pie Chart")
            fig_pie = px.pie(
                names=days,
                values=counts,
                title="Percentage of Workouts by Day",
                hole=0.3
            )
            st.plotly_chart(fig_pie)
        
        elif chart_type == "Line Chart":
            st.subheader("Workout Trend Over the Week - Line Chart")
            fig_line = px.line(
                x=days,
                y=counts,
                labels={'x': 'Day of the Week', 'y': 'Number of Workouts'},
                title="Weekly Workout Trend"
            )
            st.plotly_chart(fig_line)