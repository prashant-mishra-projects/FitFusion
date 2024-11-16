import streamlit as st
import requests

# Replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube API key
YOUTUBE_API_KEY = "AIzaSyApv86cQPqXLf1aw34Lh9Zsu3_oOX46Qfc"

def get_youtube_video_url(exercise_name):
    # YouTube Data API endpoint for searching videos
    search_url = "https://www.googleapis.com/youtube/v3/search"
    
    # Define parameters for the API request
    params = {
        "part": "snippet",
        "q": f"{exercise_name} exercise tutorial",
        "type": "video",
        "key": YOUTUBE_API_KEY,
        "maxResults": 1
    }
    
    # Make a request to the YouTube API
    response = requests.get(search_url, params=params)
    results = response.json()
    
    # Extract video URL if there are results
    if "items" in results and len(results["items"]) > 0:
        video_id = results["items"][0]["id"]["videoId"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return video_url
    else:
        return None

# Streamlit App
def app():
    if "username" not in st.session_state or st.session_state.username == "":
        st.warning("Please log in to view and search for workout tutorials.")
    else:
        st.title("Exercise Tutorials")
        
        # Input field for the exercise name
        exercise_name = st.text_input("Enter the name of the exercise:")
        
        # Search button
        if st.button("Search"):
            if exercise_name:
                # Fetch the YouTube video URL
                video_url = get_youtube_video_url(exercise_name)
                
                # Display the video or a message if no video is found
                if video_url:
                    st.write(f"Showing top result for **{exercise_name}**:")
                    st.video(video_url)
                else:
                    st.warning("No video found for the given exercise.")
            else:
                st.warning("Please enter an exercise name to search.")