# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Study Efficiency Survey",
    page_icon="📚",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Study Efficiency Tracker 📚")
st.write("Please fill out the form below to track your study sessions and improve learning efficiency.")

# DATA INPUT FORM
with st.form("survey_form"):
    st.subheader("Study Session Details")

    subject_input = st.selectbox(
        "Select Subject:",
        ["Computer Science", "Mathematics", "English", "Physics", "Chemistry", "Biology", "Other"]
    )

    study_hours_input = st.slider(
        "Study Hours:",
        min_value=0.5,
        max_value=8.0,
        value=2.0,
        step=0.5,
        help="Duration of effective study time"
    )

    focus_level_input = st.slider(
        "Focus Level (1-10):",
        min_value=1,
        max_value=10,
        value=7,
        help="1 = Easily distracted, 10 = Fully focused"
    )

    understanding_input = st.slider(
        "Understanding Level (1-10):",
        min_value=1,
        max_value=10,
        value=7,
        help="1 = Completely confused, 10 = Fully understood"
    )

    topics_input = st.text_input(
        "Topics Covered:",
        placeholder="e.g., Python functions, Calculus derivatives..."
    )

    submitted = st.form_submit_button("Submit Study Data")

    if submitted:
        if not topics_input:
            st.error("Please enter the topics covered during your study session.")
        else:
            new_data = {
                'timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                'subject': [subject_input],
                'study_hours': [study_hours_input],
                'focus_level': [focus_level_input],
                'understanding': [understanding_input],
                'topics_covered': [topics_input]
            }

            new_row_df = pd.DataFrame(new_data)

            if os.path.exists('data.csv'):
                new_row_df.to_csv('data.csv', mode='a', header=False, index=False)
            else:
                new_row_df.to_csv('data.csv', index=False)

            st.success("Your study data has been submitted successfully!")
            st.write(
                f"**Session Summary:** {study_hours_input} hours of {subject_input} - Focus: {focus_level_input}/10, Understanding: {understanding_input}/10")

# DATA DISPLAY
st.divider()
st.header("Current Study Data")

if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    current_data_df = pd.read_csv('data.csv')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Sessions", len(current_data_df))
    with col2:
        total_hours = current_data_df['study_hours'].sum()
        st.metric("Total Study Hours", f"{total_hours:.1f}")
    with col3:
        avg_focus = current_data_df['focus_level'].mean()
        st.metric("Average Focus", f"{avg_focus:.1f}/10")

    st.dataframe(current_data_df)
else:
    st.warning("No study data has been recorded yet. Submit your first study session above!")