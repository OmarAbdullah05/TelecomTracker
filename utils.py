import plotly.express as px
import plotly.graph_objects as go

def create_status_chart(df):
    status_counts = df['Status'].value_counts()
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title='Project Status Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    return fig

def create_region_chart(df):
    region_counts = df['Region'].value_counts()
    fig = px.bar(
        x=region_counts.index,
        y=region_counts.values,
        title='Projects by Region',
        labels={'x': 'Region', 'y': 'Number of Projects'},
        color_discrete_sequence=['#007bff']
    )
    return fig

def create_progress_gauge(progress):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=progress,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': "#007bff"},
               'steps': [
                   {'range': [0, 33], 'color': "#f8d7da"},
                   {'range': [33, 66], 'color': "#fff3cd"},
                   {'range': [66, 100], 'color': "#d4edda"}
               ]}
    ))
    fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
    return fig

def filter_dataframe(df, region=None, status=None, search_term=None):
    filtered_df = df.copy()
    
    if region and region != "All":
        filtered_df = filtered_df[filtered_df['Region'] == region]
        
    if status and status != "All":
        filtered_df = filtered_df[filtered_df['Status'] == status]
        
    if search_term:
        search_mask = (
            filtered_df['Project_ID'].str.contains(search_term, case=False) |
            filtered_df['Project_Name'].str.contains(search_term, case=False)
        )
        filtered_df = filtered_df[search_mask]
        
    return filtered_df
