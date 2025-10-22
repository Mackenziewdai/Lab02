import streamlit as st
import pandas as pd

st.set_page_config(page_title="Study Analytics", page_icon="📊")
st.title("Study Efficiency Analytics Dashboard")


def load_csv_data():
    try:
        return pd.read_csv('data.csv')
    except:
        return pd.DataFrame()


def create_subject_scores_chart():
    st.header("1. Course Performance Comparison")

    # 硬编码科目成绩数据
    chart_data = {
        "Computer Science": 88,
        "Mathematics": 85,
        "Physics": 78,
        "English": 92,
        "Chemistry": 82
    }

    df = pd.DataFrame({
        'subject': list(chart_data.keys()),
        'score': list(chart_data.values())
    })

    st.bar_chart(df.set_index('subject')['score'])
    st.write("Bar chart showing performance scores across different subjects.")


def create_study_trends_chart(csv_data):
    st.header("2. Study Hours Trends")

    if csv_data.empty:
        # 显示示例数据
        st.info("No CSV data available. Showing example data.")
        example_data = pd.DataFrame({
            'date': ['2024-10-01', '2024-10-02', '2024-10-03'],
            'study_hours': [3.5, 2.0, 4.0]
        })
        st.line_chart(example_data.set_index('date')['study_hours'])
    else:
        subjects = ['All'] + sorted(csv_data['subject'].unique().tolist())
        selected_subject = st.selectbox("Select Subject", subjects, key="subject_select")

        filtered_data = csv_data
        if selected_subject != 'All':
            filtered_data = csv_data[csv_data['subject'] == selected_subject]

        st.line_chart(filtered_data[['study_hours']])

    st.write("Line chart showing study hours trends over time.")


def create_focus_understanding_chart(csv_data):
    st.header("3. Focus vs Understanding Analysis")

    if csv_data.empty:
        st.info("No CSV data available. Showing example relationship.")
        # 显示示例散点图
        example_data = pd.DataFrame({
            'focus': [7, 8, 5, 9, 6],
            'understanding': [8, 7, 6, 9, 7]
        })
        st.scatter_chart(example_data)
    else:
        hour_range = st.slider("Study Hours Range", 0.5, 8.0, (1.0, 4.0), key="hour_slider")

        filtered_data = csv_data[
            (csv_data['study_hours'] >= hour_range[0]) &
            (csv_data['study_hours'] <= hour_range[1])
            ]

        if not filtered_data.empty:
            st.scatter_chart(filtered_data[['focus_level', 'understanding']])
        else:
            st.info("No data in selected range.")

    st.write("Scatter plot showing relationship between focus and understanding.")


def main():
    csv_data = load_csv_data()

    create_subject_scores_chart()
    st.divider()
    create_study_trends_chart(csv_data)
    st.divider()
    create_focus_understanding_chart(csv_data)


if __name__ == "__main__":
    main()
