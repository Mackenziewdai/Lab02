import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="Study Analytics", page_icon="📊")
st.title("Study Efficiency Analytics Dashboard")


def load_csv_data():
    try:
        data = pd.read_csv('data.csv')
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

        st.bar_chart(df.set_index('label')['value'])
        st.write("Bar chart showing performance scores across different subjects.")


        st.dataframe(df)
    else:
        st.warning("JSON data not available for this chart.")


def create_study_trends_chart(csv_data):
    st.header("2. Study Hours Trends")

    if csv_data.empty:
        st.warning("No CSV data available for study trends.")
        return


    subjects = ['All Subjects'] + sorted(csv_data['subject'].unique().tolist())
    selected_subject = st.selectbox("Filter by Subject", subjects, key="subject_filter")

    filtered_data = csv_data.copy()
    if selected_subject != 'All Subjects':
        filtered_data = filtered_data[filtered_data['subject'] == selected_subject]

    if not filtered_data.empty:

        if 'timestamp' in filtered_data.columns:
            chart_data = filtered_data.set_index('timestamp')['study_hours']
        else:
            chart_data = filtered_data['study_hours']

        st.line_chart(chart_data)
        st.write(f"Line chart showing study hours trends for {selected_subject}.")


        avg_hours = filtered_data['study_hours'].mean()
        total_sessions = len(filtered_data)
        st.metric("Average Study Hours", f"{avg_hours:.1f}")
        st.metric("Total Sessions", total_sessions)
    else:
        st.info("No data available for the selected filters.")


def create_focus_understanding_chart(csv_data):
    st.header("3. Focus vs Understanding Analysis")

    if csv_data.empty:
        st.warning("No CSV data available for focus analysis.")
        return


    hour_range = st.slider(
        "Study Hours Range",
        min_value=0.5,
        max_value=8.0,
        value=(1.0, 4.0),
        step=0.5,
        key="hour_slider"
    )

    filtered_data = csv_data[
        (csv_data['study_hours'] >= hour_range[0]) &
        (csv_data['study_hours'] <= hour_range[1])
        ]

    if not filtered_data.empty:

        scatter_data = filtered_data[['focus_level', 'understanding']].rename(
            columns={'focus_level': 'Focus Level', 'understanding': 'Understanding Level'}
        )
        st.scatter_chart(scatter_data)

        st.write("Scatter plot analyzing the relationship between focus level and understanding level.")
        st.write(f"Showing data for study hours between {hour_range[0]} and {hour_range[1]} hours.")


        correlation = filtered_data['focus_level'].corr(filtered_data['understanding'])
        st.metric("Focus-Understanding Correlation", f"{correlation:.2f}")
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

    if 'app_initialized' not in st.session_state:
        st.session_state.app_initialized = True


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