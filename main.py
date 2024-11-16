import streamlit as st
from streamlit_option_menu import option_menu
import home, tutorials, workoutplan,about, account,posturecheck

st.set_page_config(
    page_title="GYM APP",
    page_icon="🏋️",
    layout="wide"
)

# CSS for custom styling
st.markdown("""
    <style>
    /* Sidebar container styling */
    .css-1d391kg {  /* Sidebar styling for Streamlit */
        background-color: #2C2F33 !important;
    }
    /* Overall container padding */
    .css-18e3th9 {
        padding-top: 1rem;
        padding-bottom: 1rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    /* Option menu customization */
    .option-menu-container {
        background-color: #23272A !important;
        border-radius: 8px;
        padding: 10px;
    }
    .option-menu-container .nav-link, .option-menu-container .nav-link:hover {
        color: #FFFFFF !important;
        font-size: 18px;
        border-radius: 8px;
    }
    .option-menu-container .nav-link-selected {
        background-color: #7289DA !important;
        color: #FFFFFF !important;
    }
    /* Header and title styling */
    .css-10trblm {
        font-size: 24px;
        color: #7289DA !important;
    }
    /* Button hover effect */
    button:hover {
        background-color: #5865F2 !important;
    }
    </style>
    """, unsafe_allow_html=True)

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })

    def run(self):
        # Render the sidebar with the navigation menu
        with st.sidebar:
            st.markdown("## Fitness Fusion")  # Sidebar header
            app = option_menu(
                menu_title=None,
                options=["Account", "Home", "Workout Planner", "Tutorials", "Posture Check", "About"],
                icons=["person", "house", "dumbbell", "play-circle", "camera", "info-circle"],
                menu_icon="fitness-center",
                default_index=1,
                orientation="vertical",
                styles={
                    "container": {"padding": "5px", "background-color": "#23272A"},
                    "icon": {"color": "#7289DA", "font-size": "18px"},
                    "nav-link": {
                        "font-size": "18px",
                        "color": "white",
                        "text-align": "center",
                        "margin": "0px",
                        "--hover-color": "#5865F2",
                    },
                    "nav-link-selected": {
                        "background-color": "#7289DA",
                        "color": "white",
                        "border-radius": "5px",
                    },
                }
            )

        # Clear any existing sidebar titles/content to avoid display in sidebar
        st.sidebar.empty()
        
        # Display the selected page in the main area
        if app == "Account":
            account.app()
        elif app == "Home":
            home.app()
        elif app == "Workout Planner":
            workoutplan.app()
        elif app == "Tutorials":
            tutorials.app()
        elif app == "Posture Check":
            posturecheck.app()
        elif app == "About":
            about.app()

# Instantiate and run the app
app = MultiApp()
app.run()
