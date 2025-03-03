import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(num_projects=50):
    np.random.seed(42)
    
    regions = ['North', 'South', 'East', 'West', 'Central']
    statuses = ['Planning', 'In Progress', 'On Hold', 'Completed']
    site_types = ['Macro Site', 'Small Cell', 'DAS', 'Rooftop']
    
    data = {
        'Project_ID': [f'PRJ-{i:04d}' for i in range(1, num_projects + 1)],
        'Project_Name': [f'Telecom Site {i:04d}' for i in range(1, num_projects + 1)],
        'Region': np.random.choice(regions, num_projects),
        'Status': np.random.choice(statuses, num_projects),
        'Site_Type': np.random.choice(site_types, num_projects),
        'Progress': np.random.randint(0, 101, num_projects),
        'Start_Date': [
            (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')
            for _ in range(num_projects)
        ],
        'Budget': np.random.randint(100000, 1000000, num_projects),
        'Priority': np.random.choice(['High', 'Medium', 'Low'], num_projects),
    }
    
    return pd.DataFrame(data)
