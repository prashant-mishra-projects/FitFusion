import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    Parameters:
    - a, b, c: Coordinates of the three points [x, y]
    Returns:
    - angle: Angle in degrees
    """
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360 - angle
    return angle

# Exercise-specific analysis functions
def analyze_bicep_curl(landmarks, frame, width, height):
    """Analyze and provide feedback for bicep curls."""
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * width,
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * height]
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * width,
             landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * height]

    # Calculate angle
    angle = calculate_angle(shoulder, elbow, wrist)

    # Display feedback
    if angle < 40:
        feedback = "Full Curl"
        color = (0, 255, 0)
    elif angle > 150:
        feedback = "Arm Extended"
        color = (255, 255, 0)
    else:
        feedback = "Curling"
        color = (0, 0, 255)

    cv2.putText(frame, f'Bicep Angle: {int(angle)}°', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.putText(frame, feedback, (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

def analyze_squat(landmarks, frame, width, height):
    """Analyze and provide feedback for squats."""
    hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x * width,
           landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y * height]
    knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x * width,
            landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y * height]
    ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x * width,
             landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y * height]

    # Calculate angle
    angle = calculate_angle(hip, knee, ankle)

    # Display feedback
    if angle > 160:
        feedback = "Standing"
        color = (0, 255, 0)
    elif angle < 90:
        feedback = "Too Low"
        color = (0, 0, 255)
    else:
        feedback = "Squatting"
        color = (255, 255, 0)

    cv2.putText(frame, f'Squat Angle: {int(angle)}°', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.putText(frame, feedback, (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

def analyze_tricep_extension(landmarks, frame, width, height):
    """Analyze and provide feedback for tricep extensions."""
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * width,
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * height]
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * width,
             landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * height]

    # Calculate angle
    angle = calculate_angle(shoulder, elbow, wrist)

    # Display feedback
    if angle > 160:
        feedback = "Arm Extended"
        color = (0, 255, 0)
    elif 90 < angle <= 160:
        feedback = "Lowering"
        color = (0, 255, 255)
    elif 30 < angle <= 90:
        feedback = "Extending"
        color = (0, 165, 255)
    else:
        feedback = "Check Form"
        color = (0, 0, 255)

    cv2.putText(frame, f'Tricep Angle: {int(angle)}°', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.putText(frame, feedback, (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

def analyze_shoulder_press(landmarks, frame, width, height, counter, stage):
    """Analyze shoulder press with rep counting."""
    shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * width,
                landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * height]
    elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * width,
             landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * height]
    wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * width,
             landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * height]

    # Calculate angle
    angle = calculate_angle(shoulder, elbow, wrist)

    if angle > 160:
        stage = "up"
    if angle < 90 and stage == "up":
        stage = "down"
        counter += 1

    # Display rep count and feedback
    feedback = "Up" if stage == "up" else "Down"
    color = (0, 255, 0) if stage == "up" else (255, 255, 0)

    cv2.putText(frame, f'Reps: {counter}', (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
    cv2.putText(frame, f'Shoulder Press: {feedback}', (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

    return counter, stage

def app():
    st.title("Exercise Posture & Rep Counter")
    st.write("Track your posture and reps for exercises like Bicep Curls, Squats, Tricep Extensions, and Shoulder Press.")

    exercise = st.selectbox("Choose an exercise", ["Bicep Curls", "Squats", "Tricep Extensions", "Shoulder Press"])

    stframe = st.empty()

    cap = cv2.VideoCapture(1)

    counter = 0
    stage = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.warning("Unable to access the camera.")
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(rgb_frame)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                landmarks = results.pose_landmarks.landmark

                if exercise == "Bicep Curls":
                    analyze_bicep_curl(landmarks, frame, width, height)
                elif exercise == "Squats":
                    analyze_squat(landmarks, frame, width, height)
                elif exercise == "Tricep Extensions":
                    analyze_tricep_extension(landmarks, frame, width, height)
                elif exercise == "Shoulder Press":
                    counter, stage = analyze_shoulder_press(landmarks, frame, width, height, counter, stage)

            stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

