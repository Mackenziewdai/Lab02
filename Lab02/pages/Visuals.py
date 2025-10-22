import streamlit as st
import pandas as pd
import json
import matplotlib.pyplot as plt

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

        fig, ax = plt.subplots()
        ax.bar(df['label'], df['value'], color='lightblue')
        ax.set_xlabel('Subject')
        ax.set_ylabel('Score')
        ax.set_title('Course Performance')
        plt.xticks(rotation=45)
        st.pyplot(fig)
        st.write("Bar chart showing performance scores across different subjects.")
    else:
        st.warning("JSON data not available for this chart.")


def create_study_trends_chart(csv_data):
    st.header("2. Study Hours Trends")

    if csv_data.empty:
        st.warning("No CSV data available.")
        return

    subjects = ['All'] + sorted(csv_data['subject'].unique().tolist())
    selected_subject = st.selectbox("Select Subject", subjects)

    filtered_data = csv_data
    if selected_subject != 'All':
        filtered_data = csv_data[csv_data['subject'] == selected_subject]

    if not filtered_data.empty:
        st.line_chart(filtered_data[['study_hours']])
        st.write(f"Study hours trends for {selected_subject}")


def create_focus_understanding_chart(csv_data):
    st.header("3. Focus vs Understanding Analysis")

    if csv_data.empty:
        st.warning("No CSV data available.")
        return

    hour_range = st.slider("Study Hours Range", 0.5, 8.0, (1.0, 4.0))

    filtered_data = csv_data[
        (csv_data['study_hours'] >= hour_range[0]) &
        (csv_data['study_hours'] <= hour_range[1])
        ]

    if not filtered_data.empty:
        fig, ax = plt.subplots()
        scatter = ax.scatter(filtered_data['focus_level'],
                             filtered_data['understanding'],
                             s=50, alpha=0.6)
        ax.set_xlabel('Focus Level')
        ax.set_ylabel('Understanding Level')
        ax.set_title('Focus vs Understanding')
        st.pyplot(fig)
        st.write("Scatter plot showing relationship between focus and understanding")


def main():
    csv_data = load_csv_data()
    json_data = load_json_data()

    create_subject_scores_chart(json_data)
    st.divider()
    create_study_trends_chart(csv_data)
    st.divider()
    create_focus_understanding_chart(csv_data)


if __name__ == "__main__":
    main()