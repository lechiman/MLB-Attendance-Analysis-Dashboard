# MLB Attendance Analysis Dashboard

An interactive web dashboard for analyzing MLB game attendance data across multiple seasons, including World Series championship impact analysis.

## Overview

This project provides a comprehensive analysis tool for MLB attendance data (2000-2025), allowing users to explore attendance patterns, trends, championship impacts, and business insights through an interactive web interface.

**Data Coverage:** 26 seasons (2000-2025), 780 team-seasons, 30 teams  
**Key Features:** Championship analysis, payroll efficiency, attendance forecasting, 2025 stabilization insights

## Features

### Team Analysis
- Compare attendance metrics for multiple teams over time
- Championship markers (🏆) for World Series winners
- View different attendance metrics (total, per game, payroll efficiency)
- Multiple chart types (line, bar, scatter plots)
- Attendance vs payroll correlation analysis

### Season Analysis
- Top teams by attendance for specific seasons
- Season-specific attendance distributions
- Box plots showing performance variance
- Historical comparisons across eras

### League Trends
- League-wide attendance trends over time (2000-2025)
- **2025 Stabilization Analysis** (+0.09% growth, ending decline)
- Total attendance and average per-game metrics
- Payroll trends and efficiency analysis

### Payroll Analysis
- Payroll vs attendance correlation (r=0.54)
- Efficiency metrics (attendance per $1M payroll)
- Year-over-year efficiency changes
- ROI calculations and benchmarking

### 🏆 Championship Analysis (NEW!)
- **Championship Premium:** Teams with titles average +613K fans (+31%)
- **Post-Championship Bump:** +34% average attendance increase
- **Dynasty Analysis:** Dodgers 3 championships (2020, 2024, 2025) → 4.01M attendance
- Championships by team (2000-2025)
- World Series impact on attendance trends

## Project Files

### Interactive Dashboard
- `BossLeveMLBSportsAttendance.py` - Main dashboard application with championship analysis

### Data Files
- `MLB_attendance_data_2000-2025.csv` - Complete MLB attendance data (780 records)
- `MLB Wolrd Series Winners 2000-25.csv` - World Series champions and finalists (26 years)

### Analysis Scripts
- `business_insights_analysis.py` - Comprehensive business analytics (11 modules)
- `world_series_attendance_analysis.py` - Championship impact analysis

### Documentation
- `README.md` - This file
- `EXECUTIVE_SUMMARY.md` - Leadership brief with key findings
- `ANALYSIS_FINDINGS.md` - Comprehensive 32KB analysis report
- `BUSINESS_INSIGHTS.md` - Business intelligence framework
- `WORLD_SERIES_INSIGHTS.md` - Championship analysis (26 pages)

### Results & Updates
- `business_insights_results.json` - Complete analysis results
- `world_series_attendance_results.json` - Championship impact data
- `UPDATE_SUMMARY.md` - 2025 data integration details
- `WORLD_SERIES_UPDATE_COMPLETE.md` - Championship analysis completion

## Installation

1. Install required Python packages:
```bash
pip install dash pandas plotly numpy scipy
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

2. Ensure data files are in the same directory:
   - `MLB_attendance_data_2000-2025.csv` (required)
   - `MLB Wolrd Series Winners 2000-25.csv` (optional, for championship features)

## Usage

### Interactive Dashboard

1. Run the dashboard:
```bash
python BossLeveMLBSportsAttendance.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:8051/
```

3. Explore the five interactive tabs:
   - **Team Analysis** - Compare teams, view trends
   - **Season Analysis** - Top performers, distributions
   - **League Trends** - Industry-wide patterns, 2025 stabilization
   - **Payroll Analysis** - ROI, efficiency metrics
   - **🏆 Championships** - World Series impact analysis

### Business Analytics

Run comprehensive analysis:
```bash
python business_insights_analysis.py
```

Generates `business_insights_results.json` with 11 analytical modules.

### Championship Analysis

Run World Series impact analysis:
```bash
python world_series_attendance_analysis.py
```

Generates `world_series_attendance_results.json` with championship insights.

## Data Structure

### Attendance Data (MLB_attendance_data_2000-2025.csv)
- **Seasons:** 2000-2025 (26 years)
- **Records:** 780 team-seasons
- **Teams:** 30 MLB teams (normalized names)
- **Metrics:**
  - Total attendance
  - Attendance per game
  - Estimated payroll
  - Computed efficiency (attendance per $1M payroll)

### World Series Data (MLB Wolrd Series Winners 2000-25.csv)
- **Championships:** 26 World Series (2000-2025)
- **Winners & Losers:** Complete finalists data
- **Series Results:** Game counts (e.g., 4-3, 4-1)
- **Integration:** Linked with attendance data for impact analysis

## Key Findings

### 2025 Breakthrough
- **Attendance Stabilized:** 71.4M fans (+0.09% vs 2024)
- **Dodgers Milestone:** 4.01M attendance - first 4M+ by ANY team since 2007
- **Potential Turning Point:** Ends years of decline

### Championship Impact
- **Championship Premium:** +613K fans/season (+31%) for teams with titles
- **Post-Championship Bump:** +34% average attendance increase following year
- **Dynasty Effect:** Dodgers' 3 championships (2020, 2024, 2025) = market dominance
- **ROI:** Championships worth $150-300M over 5 years

### Efficiency Leaders
1. **San Diego Padres:** 36,126 fans/$1M payroll
2. **Milwaukee Brewers:** 36,110 fans/$1M payroll
3. **Colorado Rockies:** 32,587 fans/$1M payroll

### All-Time Attendance Leaders (2000-2025)
1. **Los Angeles Dodgers:** 3.57M average (3 championships)
2. **New York Yankees:** 3.46M average (2 championships)
3. **St. Louis Cardinals:** 3.21M average (2 championships)

## Technical Details

### Technologies
- **Dash** - Python web framework for interactive dashboards
- **Plotly** - Interactive visualizations and charts
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computations
- **SciPy** - Statistical analysis and correlations

### Features
- Responsive design for different screen sizes
- Real-time interactive filtering and selection
- Multiple visualization types (line, bar, scatter, box plots)
- Statistical overlays (trend lines, correlations)
- Championship markers and annotations

## Business Applications

This analysis supports:
- **Team Owners:** ROI analysis, franchise valuation, investment decisions
- **General Managers:** Payroll justification, performance accountability
- **Marketing Departments:** Campaign planning, fan engagement strategies
- **CFOs:** Revenue forecasting, budget allocation
- **League Office:** Competitive balance, market health assessment

## Data Sources

- **MLB Attendance Records:** 2000-2025 (26 seasons, 780 team-seasons)
- **World Series Data:** Champions and finalists 2000-2025 (26 championships)
- **Payroll Data:** Estimated team payrolls by season

## Documentation

For detailed analysis and insights, see:
- `EXECUTIVE_SUMMARY.md` - Quick overview for leadership (15-min read)
- `ANALYSIS_FINDINGS.md` - Comprehensive report (60-min read)
- `WORLD_SERIES_INSIGHTS.md` - Championship impact analysis (26 pages)
- `BUSINESS_INSIGHTS.md` - Business intelligence framework

## License & Usage

This project is for educational and analysis purposes. Data sourced from publicly available MLB records.

---

**Last Updated:** February 2026  
**Data Coverage:** 2000-2025 (26 seasons)  
**Key Achievement:** First comprehensive analysis linking World Series performance to attendance patterns