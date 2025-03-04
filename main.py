import streamlit as st
import pandas as pd
import numpy as np
from data_generator import generate_mock_data
from utils import create_status_chart, create_region_chart, create_progress_gauge, filter_dataframe

# Page config
st.set_page_config(
    page_title="Telecom Project Dashboard",
    page_icon="📡",
    layout="wide"
)

# Custom CSS - updated to include table styling
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
    .tracker-table {
        margin-top: 1rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
    }
    .build-status-table {
        margin-top: 1rem;
        font-size: 14px;
    }
    .build-status-table th {
        background-color: #f8f9fa;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = generate_mock_data()

# Create tabs
tab1, tab2, tab3 = st.tabs(["📊 Projects Dashboard", "🔍 Fuze Trackers", "🏗️ Build Status"])

with tab1:
    # Original dashboard content
    st.title("📡 Telecom Project Dashboard")

    # Overall Summary Section
    st.subheader("Overall Summary")

    # Create summary data
    summary_data = pd.DataFrame({
        'PROGRAM': ['CBand', 'Macro New', 'Relo', 'HBR', '5G mmW', 'Crown', 'SC New', 
                   'Carrier Add', 'Top10', 'Root', '1F Conversion', 'eNSB (Hub)'],
        'Actuals_LTD': [134, 134, 19, 9, 8, 218, 96, 95, 222, 254, 0, 96],
        'Total_Projects': [596, 131, 19, 12, 8, 185, 97, 526, 42, 69, 85, 69],
        'YTD_Goal': [0, 22, 0, 2, 1, 45, 6, 0, 0, 0, 0, 9],
        'Yearly_Goal': [0, 119, 0, 15, 6, 267, 28, 0, 0, 0, 0, 44],
        'Actuals_YTD': [1, 5, 0, 0, 0, 33, 0, 1, 22, 9, 0, 14],
        'YTD_%_of_Goal': ['0%', '23%', '0%', '0%', '100%', '73%', '0%', '0%', '0%', '0%', '0%', '156%'],
        'Monthly_Goal': [0, 8, 0, 1, 0, 15, 1, 0, 0, 0, 0, 4],
        'Actuals_MTD': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'MTD_%_of_Goal': ['0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%'],
        'Monthly_Avg': [46, 10, 1, 2, 2, 17, 16, 6, 4, 7, 8, 5],
        'Activated_Today': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    })

    # Display summary table
    st.dataframe(
        summary_data,
        column_config={
            'PROGRAM': st.column_config.TextColumn('PROGRAM'),
            'Actuals_LTD': st.column_config.NumberColumn('Actuals LTD'),
            'Total_Projects': st.column_config.NumberColumn('Total Projects'),
            'YTD_Goal': st.column_config.NumberColumn('YTD Goal'),
            'Yearly_Goal': st.column_config.NumberColumn('Yearly Goal'),
            'Actuals_YTD': st.column_config.NumberColumn('Actuals YTD'),
            'YTD_%_of_Goal': st.column_config.TextColumn('YTD % of Goal'),
            'Monthly_Goal': st.column_config.NumberColumn('Monthly Goal'),
            'Actuals_MTD': st.column_config.NumberColumn('Actuals MTD'),
            'MTD_%_of_Goal': st.column_config.TextColumn('MTD % of Goal'),
            'Monthly_Avg': st.column_config.NumberColumn('Monthly Avg.'),
            'Activated_Today': st.column_config.NumberColumn('Activated Today')
        },
        hide_index=True,
        use_container_width=True
    )

    # Sidebar filters
    st.sidebar.header("Filters")
    search_term = st.sidebar.text_input("Search Projects", "")
    regions = ["All"] + list(st.session_state.data["Region"].unique())
    selected_region = st.sidebar.selectbox("Select Region", regions)
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

with tab2:
    st.title("🔍 Fuze Trackers")

    # Search and filters for Fuze trackers
    search_tracker = st.text_input("Search Trackers", "")

    # Mock Fuze tracker data
    fuze_data = pd.DataFrame({
        'Owner': ['PM Team', 'Anastasia Aubrey', 'Jennifer Behn', 'Julia Weigel', 'Leonard Strickland'],
        'Program': ['All', '1F Conversions', '4G SCL', 'Macro', 'Mobile Asset'],
        'Tracker_Name': ['MIK 2024', 'MI 2024 1F Conversions', '4G MIK Self Perform', 'MIK_New Build', 'MIK Mobile Asset and Events'],
        'Tracker_ID': ['2870866', '2693211', '2413432', '2458399', '2981551']
    })

    # Filter based on search
    if search_tracker:
        mask = (
            fuze_data['Owner'].str.contains(search_tracker, case=False) |
            fuze_data['Program'].str.contains(search_tracker, case=False) |
            fuze_data['Tracker_Name'].str.contains(search_tracker, case=False)
        )
        fuze_data = fuze_data[mask]

    # Display Fuze trackers in a modern table
    st.dataframe(
        fuze_data,
        column_config={
            'Owner': st.column_config.TextColumn('Owner'),
            'Program': st.column_config.TextColumn('Program'),
            'Tracker_Name': st.column_config.TextColumn('Tracker Name'),
            'Tracker_ID': st.column_config.TextColumn(
                'Tracker Link',
                help="Click to view tracker details"
            )
        },
        hide_index=True,
        use_container_width=True
    )

    # Add links below the table
    for _, row in fuze_data.iterrows():
        st.markdown(f"[{row['Tracker_Name']}](https://example.com/tracker/{row['Tracker_ID']})")

    # Add some helpful information
    st.info("Click on the tracker names above to open the detailed tracker view in a new tab.")

with tab3:
    st.title("🏗️ Build Status Dashboard")

    # Initialize build status data
    initial_build_data = pd.DataFrame({
        'Project_Type': ['5G mmW', 'CBand', 'Crown', 'HBR', 'Macro New', 'Relo', 'Root', 'SC New', 'Top10'],
        'Total_Active': [7, 2, 185, 10, 129, 17, 51, 45, 40],
        'Initial_Site_Walk': [7, 1, 137, 2, 8, 0, 5, 24, 10],
        'Candidates_Accepted': [7, 2, 183, 10, 139, 15, 63, 46, 40],
        'Candidates_Appd': [7, 2, 185, 11, 131, 15, 63, 46, 40],
        'Preliminary_RFDS': [7, 2, 68, 9, 114, 15, 52, 40, 34],
        'Construction_RFDS_Completed': [0, 0, 0, 4, 29, 0, 11, 6, 0],
        'NEPA_Submit': [0, 0, 0, 0, 0, 0, 0, 0, 0],
        'RFDS_Complete': [7, 2, 185, 10, 139, 17, 51, 46, 40]
    })

    modification_data = pd.DataFrame({
        'Project_Type': ['1F Conversion', '5G mmW', 'CBand', 'eNSB (Hub)', 'Relo', 'Root', 'SC New', 'Top10'],
        'Total_Active': [85, 1, 596, 69, 2, 6, 51, 2],
        'Initial_Site_Walk': [0, 0, 0, 0, 0, 0, 0, 0],
        'Candidates_Accepted': [64, 1, 596, 49, 2, 6, 51, 2],
        'Candidates_Appd': [64, 1, 596, 49, 2, 6, 51, 2],
        'Preliminary_RFDS': [0, 0, 579, 0, 1, 5, 45, 2],
        'Construction_RFDS_Completed': [0, 0, 268, 0, 0, 3, 0, 2],
        'NEPA_Submit': [0, 0, 0, 0, 0, 0, 0, 0],
        'RFDS_Complete': [85, 1, 596, 69, 2, 6, 51, 2]
    })

    # Display Initial Build section
    st.subheader("Initial Build")
    st.dataframe(
        initial_build_data,
        column_config={
            'Project_Type': st.column_config.TextColumn('Project Type'),
            'Total_Active': st.column_config.NumberColumn('Total Active Projects'),
            'Initial_Site_Walk': st.column_config.NumberColumn('Initial Site Walk (A)'),
            'Candidates_Accepted': st.column_config.NumberColumn('Candidates Accepted (A)'),
            'Candidates_Appd': st.column_config.NumberColumn('Candidates Appd By RF (A)'),
            'Preliminary_RFDS': st.column_config.NumberColumn('Preliminary RFDS'),
            'Construction_RFDS_Completed': st.column_config.NumberColumn('Construction RFDS Completed(A)'),
            'NEPA_Submit': st.column_config.NumberColumn('NEPA Submit (A)'),
            'RFDS_Complete': st.column_config.NumberColumn('RFDS Complete (A)')
        },
        hide_index=True,
        use_container_width=True
    )

    # Display Modification section
    st.subheader("Modification")
    st.dataframe(
        modification_data,
        column_config={
            'Project_Type': st.column_config.TextColumn('Project Type'),
            'Total_Active': st.column_config.NumberColumn('Total Active Projects'),
            'Initial_Site_Walk': st.column_config.NumberColumn('Initial Site Walk (A)'),
            'Candidates_Accepted': st.column_config.NumberColumn('Candidates Accepted (A)'),
            'Candidates_Appd': st.column_config.NumberColumn('Candidates Appd By RF (A)'),
            'Preliminary_RFDS': st.column_config.NumberColumn('Preliminary RFDS'),
            'Construction_RFDS_Completed': st.column_config.NumberColumn('Construction RFDS Completed(A)'),
            'NEPA_Submit': st.column_config.NumberColumn('NEPA Submit (A)'),
            'RFDS_Complete': st.column_config.NumberColumn('RFDS Complete (A)')
        },
        hide_index=True,
        use_container_width=True
    )

    # Add some helpful information
    st.info("This dashboard shows the current status of all build and modification projects across different stages.")

# Footer
st.markdown("---")
st.markdown("*Dashboard created for telecom project tracking and monitoring*")