import streamlit as st

def app():

    # Team member information
    st.subheader(":violet[Meet the Team]")

    team_members = [
        {"name": "Riya Goyal", "enroll_number": "11518002721", "course": "B.Tech Computer Science Engineering", "academic_year": "4th Year"},
        {"name": "Prashant Mishra", "enroll_number": "11218002721", "course": "B.Tech Computer Science Engineering", "academic_year": "4th Year"},
        {"name": "Vayam Dalal", "enroll_number": "10318002721", "course": "B.Tech Computer Science Engineering", "academic_year": "4th Year"},
        {"name": "Saiyam Jain", "enroll_number": "10218002721", "course": "B.Tech Computer Science Engineering", "academic_year": "4th Year"},
    ]

    # Display team members
    for member in team_members:
        st.write(f"**Name:** {member['name']}")
        st.write(f"**Enrollment Number:** {member['enroll_number']}")
        st.write(f"**Course:** {member['course']}")
        st.write(f"**Academic Year:** {member['academic_year']}")
        st.write("---") 