import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Study Analytics", page_icon="📊")
st.title("Study Efficiency Analytics Dashboard")


def load_csv_data():
    try:
        data = pd.read_csv('data.csv')
        if 'timestamp' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        return data
    except:
        return pd.DataFrame()


def load_json_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except:
        return {}


def create_subject_scores_chart(json_data):
    st.header("1. Course Performance Comparison")

    if json_data and 'data_points' in json_data:
        df = pd.DataFrame(json_data['data_points'])
        fig = px.bar(df, x='label', y='value',
                     title=json_data['chart_title'],
                     labels={'label': 'Subject', 'value': 'Score'},
                     color='value')
        st.plotly_chart(fig)
        st.write("Bar chart showing performance scores across different subjects.")
    else:
        st.warning("JSON data not available for this chart.")


def create_study_trends_chart(csv_data):
    st.header("2. Study Hours Trends")

    if csv_data.empty:
        st.warning("No CSV data available for study trends.")
        return

    col1, col2 = st.columns(2)

    with col1:
        subjects = ['All Subjects'] + sorted(csv_data['subject'].unique().tolist())
        selected_subject = st.selectbox("Filter by Subject", subjects)

    with col2:
        if 'timestamp' in csv_data.columns:
            date_range = st.date_input("Date Range",
                                       [csv_data['timestamp'].min(), csv_data['timestamp'].max()])

    filtered_data = csv_data.copy()
    if selected_subject != 'All Subjects':
        filtered_data = filtered_data[filtered_data['subject'] == selected_subject]

    if not filtered_data.empty:
        if 'timestamp' in filtered_data.columns:
            fig = px.line(filtered_data, x='timestamp', y='study_hours',
                          title=f"Study Hours Over Time - {selected_subject}",
                          labels={'timestamp': 'Date', 'study_hours': 'Study Hours'})
        else:
            fig = px.line(filtered_data, y='study_hours',
                          title=f"Study Hours - {selected_subject}",
                          labels={'index': 'Session', 'study_hours': 'Study Hours'})

        st.plotly_chart(fig)
        st.write("Line chart showing study hours trends over time with subject filtering.")
    else:
        st.info("No data available for the selected filters.")


def create_focus_understanding_chart(csv_data):
    st.header("3. Focus vs Understanding Analysis")

    if csv_data.empty:
        st.warning("No CSV data available for focus analysis.")
        return

    col1, col2 = st.columns(2)

    with col1:
        hour_range = st.slider("Study Hours Range",
                               min_value=0.5,
                               max_value=8.0,
                               value=(1.0, 4.0),
                               step=0.5)

    with col2:
        show_trendline = st.checkbox("Show Trendline", value=True)

    filtered_data = csv_data[
        (csv_data['study_hours'] >= hour_range[0]) &
        (csv_data['study_hours'] <= hour_range[1])
        ]

    if not filtered_data.empty:
        fig = px.scatter(filtered_data,
                         x='focus_level',
                         y='understanding',
                         size='study_hours',
                         color='subject',
                         title="Focus Level vs Understanding Score",
                         labels={'focus_level': 'Focus Level (1-10)',
                                 'understanding': 'Understanding Level (1-10)'},
                         trendline="ols" if show_trendline else None)

        st.plotly_chart(fig)
        st.write(
            "Scatter plot analyzing the relationship between focus level and understanding level. Bubble size represents study hours.")

        avg_focus = filtered_data['focus_level'].mean()
        avg_understanding = filtered_data['understanding'].mean()

        st.metric("Average Focus Level", f"{avg_focus:.1f}/10")
        st.metric("Average Understanding", f"{avg_understanding:.1f}/10")
    else:
        st.info("No data available for the selected study hours range.")


def display_study_analytics(json_data):
    st.header("Study Analytics Summary")

    if json_data and 'study_analytics' in json_data:
        analytics = json_data['study_analytics']

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Weekly Study Hours", analytics.get('weekly_study_hours', 'N/A'))
        with col2:
            st.metric("Preferred Study Time", analytics.get('preferred_study_time', 'N/A'))
        with col3:
            st.metric("Average Focus Score", f"{analytics.get('average_focus_score', 'N/A')}/10")
        with col4:
            st.metric("Most Productive Subject", analytics.get('most_productive_subject', 'N/A'))
    else:
        st.info("Study analytics data not available.")


def main():
    if 'data_loaded' not in st.session_state:
        st.session_state.data_loaded = True

    csv_data = load_csv_data()
    json_data = load_json_data()

    st.sidebar.title("Navigation")
    chart_option = st.sidebar.selectbox(
        "Select Chart View",
        ["All Charts", "Course Performance", "Study Trends", "Focus Analysis", "Analytics Summary"]
    )

    if chart_option == "All Charts" or chart_option == "Course Performance":
        create_subject_scores_chart(json_data)
        st.divider()

    if chart_option == "All Charts" or chart_option == "Study Trends":
        create_study_trends_chart(csv_data)
        st.divider()

    if chart_option == "All Charts" or chart_option == "Focus Analysis":
        create_focus_understanding_chart(csv_data)
        st.divider()

    if chart_option == "All Charts" or chart_option == "Analytics Summary":
        display_study_analytics(json_data)


if __name__ == "__main__":
    main()