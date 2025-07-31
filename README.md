# MLB Attendance Analysis Dashboard

An interactive web dashboard for analyzing MLB game attendance data across multiple seasons.

Video Example of Dashboard


## Overview

This project provides a comprehensive analysis tool for MLB attendance data, allowing users to explore attendance patterns, trends, and statistics through an interactive web interface.

## Features

### Team Analysis
- Compare attendance metrics for multiple teams over time
- Analyze home vs away attendance patterns
- View different attendance metrics (total, home, away, weekly averages)
- Multiple chart types (line, bar, scatter plots)

### Season Analysis
- Top teams by attendance for specific seasons
- Weekly attendance patterns across all teams
- Season-specific attendance distributions

### League Trends
- League-wide attendance trends over time
- Home vs away attendance comparisons
- Overall attendance statistics

### Advanced Analytics
- Correlation analysis between attendance metrics
- Year-over-year attendance changes
- Statistical distribution analysis

## Files

- `BossLeveMLBSportsAttendance.py` - Main dashboard application
- `MLB_attendance_data_2000-2024.csv` - MLB attendance data
- `BossLevelNFLSportsAttendance.py` - NFL attendance analysis (separate project)
- `weekly_attendance_all_seasons.csv` - NFL attendance data

## Installation

1. Install required Python packages:
```
pip install dash pandas plotly numpy scipy
```

2. Ensure the data file `MLB_attendance_data_2000-2024.csv` is in the same directory as the script.

## Usage

1. Run the dashboard:
```
python BossLeveMLBSportsAttendance.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8050/
```

3. Use the interactive tabs to explore different aspects of the attendance data.

## Data Structure

The attendance data includes:
- Team names and seasons
- Total, home, and away attendance figures
- Seasonal attendance breakdowns
- Computed metrics (averages, ranges, ratios)

## Technical Details

- Built with Dash (Python web framework)
- Uses Plotly for interactive visualizations
- Pandas for data manipulation and analysis
- Responsive design for different screen sizes

## Data Source

MLB attendance records from 2000-2024, including seasonal breakdowns and team-specific statistics.


This project is for educational and analysis purposes. 
