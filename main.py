import streamlit as st
import pandas as pd
from data_generator import generate_mock_data
from utils import create_status_chart, create_region_chart, create_progress_gauge, filter_dataframe

# Page config
st.set_page_config(
    page_title="Telecom Project Dashboard",
    page_icon="📡",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
    }
    .row-widget.stButton button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = generate_mock_data()

# Header
st.title("📡 Telecom Project Dashboard")

# Sidebar filters
st.sidebar.header("Filters")

# Search box
search_term = st.sidebar.text_input("Search Projects", "")

# Region filter
regions = ["All"] + list(st.session_state.data["Region"].unique())
selected_region = st.sidebar.selectbox("Select Region", regions)

# Status filter
statuses = ["All"] + list(st.session_state.data["Status"].unique())
selected_status = st.sidebar.selectbox("Select Status", statuses)

# Apply filters
filtered_df = filter_dataframe(
    st.session_state.data,
    region=selected_region,
    status=selected_status,
    search_term=search_term
)

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Projects", len(filtered_df))
with col2:
    st.metric("Completed Projects", len(filtered_df[filtered_df['Status'] == 'Completed']))
with col3:
    st.metric("In Progress", len(filtered_df[filtered_df['Status'] == 'In Progress']))
with col4:
    avg_progress = round(filtered_df['Progress'].mean(), 1)
    st.metric("Average Progress", f"{avg_progress}%")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(create_status_chart(filtered_df), use_container_width=True)

with col2:
    st.plotly_chart(create_region_chart(filtered_df), use_container_width=True)

# Project List
st.subheader("Project List")

# Display projects in a table
st.dataframe(
    filtered_df[[
        'Project_ID', 'Project_Name', 'Region', 'Status',
        'Progress', 'Start_Date', 'Priority'
    ]],
    hide_index=True
)

# Project Details Section
st.subheader("Project Details")
selected_project = st.selectbox(
    "Select Project to View Details",
    filtered_df['Project_ID'].tolist(),
    format_func=lambda x: f"{x} - {filtered_df[filtered_df['Project_ID'] == x]['Project_Name'].iloc[0]}"
)

if selected_project:
    project_data = filtered_df[filtered_df['Project_ID'] == selected_project].iloc[0]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Project Information**")
        st.write(f"Project ID: {project_data['Project_ID']}")
        st.write(f"Project Name: {project_data['Project_Name']}")
        st.write(f"Region: {project_data['Region']}")
        st.write(f"Site Type: {project_data['Site_Type']}")
        st.write(f"Priority: {project_data['Priority']}")
    
    with col2:
        st.write("**Progress Tracker**")
        st.plotly_chart(create_progress_gauge(project_data['Progress']), use_container_width=True)
    
    st.write("**Additional Details**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write(f"Status: {project_data['Status']}")
    with col2:
        st.write(f"Start Date: {project_data['Start_Date']}")
    with col3:
        st.write(f"Budget: ${project_data['Budget']:,}")

# Footer
st.markdown("---")
st.markdown("*Dashboard created for telecom project tracking and monitoring*")
