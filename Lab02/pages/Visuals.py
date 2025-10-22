import streamlit as st
import pandas as pd

st.set_page_config(page_title="Study Analytics", page_icon="📊")
st.title("Study Efficiency Analytics Dashboard")

def load_csv_data():
    try:
        return pd.read_csv('data.csv')
    except:
        return pd.DataFrame()

# 初始化 Session State
def init_session_state():
    if 'chart_data' not in st.session_state:
        st.session_state.chart_data = {
            "Computer Science": 88,
            "Mathematics": 85, 
            "Physics": 78,
            "English": 92,
            "Chemistry": 82
        }
    if 'selected_subject' not in st.session_state:
        st.session_state.selected_subject = "All"
    if 'hour_range' not in st.session_state:
        st.session_state.hour_range = (1.0, 4.0)
    if 'chart_updates' not in st.session_state:
        st.session_state.chart_updates = 0

def create_subject_scores_chart():
    st.header("1. Course Performance Comparison")
    
    # 使用 Session State 中的数据
    df = pd.DataFrame({
        'subject': list(st.session_state.chart_data.keys()),
        'score': list(st.session_state.chart_data.values())
    })
    
    st.bar_chart(df.set_index('subject')['score'])
    st.write("Bar chart showing performance scores across different subjects.")
    
    # Session State 交互：允许用户重置数据
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Reset Scores", key="reset_scores"):
            st.session_state.chart_data = {
                "Computer Science": 88,
                "Mathematics": 85, 
                "Physics": 78,
                "English": 92,
                "Chemistry": 82
            }
            st.session_state.chart_updates += 1
            st.rerun()
    
    with col2:
        st.metric("Chart Updates", st.session_state.chart_updates)

def create_study_trends_chart(csv_data):
    st.header("2. Study Hours Trends")
    
    # 使用 Session State 存储科目选择
    subjects = ['All'] + (sorted(csv_data['subject'].unique().tolist()) if not csv_data.empty else [])
    
    # 科目选择器 - 值存储在 Session State 中
    selected_subject = st.selectbox(
        "Select Subject", 
        subjects, 
        key="subject_selector",
        index=subjects.index(st.session_state.selected_subject) if st.session_state.selected_subject in subjects else 0
    )
    
    # 更新 Session State
    if selected_subject != st.session_state.selected_subject:
        st.session_state.selected_subject = selected_subject
        st.session_state.chart_updates += 1
        st.rerun()
    
    if csv_data.empty:
        st.info("No CSV data available. Showing example data.")
        example_data = pd.DataFrame({
            'date': ['2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04'],
            'study_hours': [3.5, 2.0, 4.0, 3.0]
        })
        st.line_chart(example_data.set_index('date')['study_hours'])
    else:
        filtered_data = csv_data
        if selected_subject != 'All':
            filtered_data = csv_data[csv_data['subject'] == selected_subject]
        
        st.line_chart(filtered_data[['study_hours']])
    
    st.write(f"Line chart showing study hours trends for {selected_subject}.")

def create_focus_understanding_chart(csv_data):
    st.header("3. Focus vs Understanding Analysis")
    
    # 使用 Session State 存储滑块值
    hour_range = st.slider(
        "Study Hours Range", 
        0.5, 8.0, 
        value=st.session_state.hour_range,
        step=0.5, 
        key="hour_slider"
    )
    
    # 更新 Session State 当滑块值改变时
    if hour_range != st.session_state.hour_range:
        st.session_state.hour_range = hour_range
        st.session_state.chart_updates += 1
        st.rerun()
    
    if csv_data.empty:
        st.info("No CSV data available. Showing example relationship.")
        example_data = pd.DataFrame({
            'focus_level': [7, 8, 5, 9, 6, 8, 7],
            'understanding': [8, 7, 6, 9, 7, 8, 8]
        })
        st.scatter_chart(example_data)
    else:
        filtered_data = csv_data[
            (csv_data['study_hours'] >= hour_range[0]) & 
            (csv_data['study_hours'] <= hour_range[1])
        ]
        
        if not filtered_data.empty:
            st.scatter_chart(filtered_data[['focus_level', 'understanding']])
        else:
            st.info("No data in selected range.")
    
    st.write(f"Scatter plot for study hours between {hour_range[0]} and {hour_range[1]} hours.")
    
    # 显示 Session State 信息
    with st.expander("Session State Info"):
        st.write(f"Current subject: {st.session_state.selected_subject}")
        st.write(f"Current hour range: {st.session_state.hour_range}")
        st.write(f"Total chart updates: {st.session_state.chart_updates}")

def main():
    # 初始化 Session State
    init_session_state()
    
    csv_data = load_csv_data()
    
    # 显示 Session State 计数器
    st.sidebar.metric("Session Updates", st.session_state.chart_updates)
    
    create_subject_scores_chart()
    st.divider()
    create_study_trends_chart(csv_data)
    st.divider()
    create_focus_understanding_chart(csv_data)

if __name__ == "__main__":
    main()
