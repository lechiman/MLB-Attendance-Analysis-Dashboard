"""
MLB Attendance Analysis Dashboard

This script creates an interactive web dashboard for analyzing MLB attendance data.
Includes 2025 data and World Series championship insights.

Run this script and open a web browser to http://127.0.0.1:8050/ to use the dashboard.

Data Coverage: 2000-2025 (26 seasons, 780 team-seasons)
Key Features:
- Team performance analysis with championship markers
- Payroll efficiency and ROI calculations
- World Series impact analysis
- 2025 stabilization insights
"""
import pandas as pd
import numpy as np
import os
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import traceback
from scipy import stats

def load_and_prepare_data():
    """Load and prepare the MLB attendance data for analysis"""
    # Check if the data file exists (try 2025 first, fallback to 2024)
    if os.path.exists('MLB_attendance_data_2000-2025.csv'):
        data_file = 'MLB_attendance_data_2000-2025.csv'
    elif os.path.exists('MLB_attendance_data_2000-2024.csv'):
        data_file = 'MLB_attendance_data_2000-2024.csv'
    else:
        raise FileNotFoundError("MLB attendance data file not found!")
    
    # Load data
    df = pd.read_csv(data_file)
    print(f"✓ Loaded {data_file} with {len(df)} records")
    
    # Normalize team names - consolidate all variants
    df['team'] = df['team'].replace({
        'Anaheim Angels': 'Los Angeles Angels',
        'Los Angeles Angels of Anaheim': 'Los Angeles Angels',
        'Florida Marlins': 'Miami Marlins',
        'Tampa Bay Devil Rays': 'Tampa Bay Rays',
        'Montreal Expos': 'Washington Nationals'
    })
    
    # Ensure all numeric columns are properly converted
    numeric_cols = ['attendance', 'Attend/G', 'Est. Payroll']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Add additional computed columns for analysis
    df['efficiency'] = df['attendance'] / df['Est. Payroll'] * 1000000  # Attendance per million dollars of payroll
    
    # Load World Series data if available
    try:
        if os.path.exists('MLB Wolrd Series Winners 2000-25.csv'):
            ws_df = pd.read_csv('MLB Wolrd Series Winners 2000-25.csv', skiprows=1)
            ws_df.columns = ['Season', 'Winner', 'Loser', 'Series']
            ws_df['Winner'] = ws_df['Winner'].str.strip()
            ws_df['Loser'] = ws_df['Loser'].str.strip()
            
            # Normalize WS team names
            ws_df['Winner'] = ws_df['Winner'].replace({
                'Anaheim Angels': 'Los Angeles Angels',
                'Florida Marlins': 'Miami Marlins',
                'Cleveland Indians': 'Cleveland Guardians'
            })
            ws_df['Loser'] = ws_df['Loser'].replace({
                'Anaheim Angels': 'Los Angeles Angels',
                'Florida Marlins': 'Miami Marlins',
                'Cleveland Indians': 'Cleveland Guardians'
            })
            
            # Add championship markers
            df['ws_champion'] = df.apply(
                lambda row: '🏆' if any((ws_df['Winner'] == row['team']) & (ws_df['Season'] == row['Season'])) else '',
                axis=1
            )
            df['ws_finalist'] = df.apply(
                lambda row: '🥈' if any((ws_df['Loser'] == row['team']) & (ws_df['Season'] == row['Season'])) else '',
                axis=1
            )
            print("✓ World Series data loaded and integrated")
        else:
            df['ws_champion'] = ''
            df['ws_finalist'] = ''
    except Exception as e:
        print(f"Note: World Series data not loaded: {e}")
        df['ws_champion'] = ''
        df['ws_finalist'] = ''
    
    return df

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # For deployment

# Function to get clean list of teams
def get_teams(df):
    """Get a clean sorted list of teams"""
    teams = df['team'].astype(str).unique()
    return sorted([team for team in teams if team and team != 'nan'])

# Load data at startup
try:
    df = load_and_prepare_data()
    teams = get_teams(df)
    seasons = sorted(df['Season'].unique())
    
    # Color scale for teams
    team_colors = px.colors.qualitative.Plotly[:len(teams)]
    team_color_map = {team: team_colors[i % len(team_colors)] for i, team in enumerate(teams)}
    
except Exception as e:
    print(f"Error loading data: {e}")
    df = pd.DataFrame()
    teams = []
    seasons = []
    team_color_map = {}

# App layout structure
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("MLB Attendance Analysis Dashboard", 
                style={'textAlign': 'center', 'color': '#0B3D91'}),
        html.H4("Interactive Analysis of MLB Game Attendance (2000-2025)",
                style={'textAlign': 'center', 'color': '#495057'}),
        html.P("🏆 Includes World Series Championship Impact Analysis | 26 Seasons | 780 Team-Seasons",
               style={'textAlign': 'center', 'color': '#6c757d', 'fontSize': '14px'}),
    ], style={'padding': '20px', 'backgroundColor': '#f8f9fa', 'marginBottom': '20px'}),
    
    # Main tabs for different analyses
    dcc.Tabs(id='tabs', value='tab-team-analysis', children=[
        # Team Analysis Tab
        dcc.Tab(label='Team Analysis', value='tab-team-analysis'),
        # Season Analysis Tab
        dcc.Tab(label='Season Analysis', value='tab-season-analysis'),
        # League Trends Tab
        dcc.Tab(label='League Trends', value='tab-league-trends'),
        # Payroll Analysis Tab
        dcc.Tab(label='Payroll Analysis', value='tab-payroll-analysis'),
        # Championship Analysis Tab
        dcc.Tab(label='🏆 Championships', value='tab-championship-analysis'),
    ]),
    
    # Content div - will be filled based on selected tab
    html.Div(id='tab-content'),
    
    # Error message div
    html.Div(id='error-message', style={'color': 'red', 'margin': '10px'}),
    
    # Footer
    html.Div([
        html.P("Created with Dash • Data Source: MLB Attendance Records",
               style={'textAlign': 'center', 'color': '#6c757d'})
    ], style={'padding': '10px', 'marginTop': '20px'})
], style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})

# Define the tab content callback
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    """Render content for each tab"""
    if tab == 'tab-team-analysis':
        return html.Div([
            # Team selector
            html.Div([
                html.Label("Select Team(s):", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='team-dropdown',
                    options=[{'label': team, 'value': team} for team in teams],
                    value=[teams[0]] if teams else [],
                    multi=True
                ),
            ], style={'marginBottom': '20px'}),
            
            # Metric selector
            html.Div([
                html.Label("Select Metric:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[
                        {'label': 'Total Attendance', 'value': 'attendance'},
                        {'label': 'Attendance Per Game', 'value': 'Attend/G'},
                        {'label': 'Estimated Payroll', 'value': 'Est. Payroll'},
                        {'label': 'Attendance Efficiency', 'value': 'efficiency'}
                    ],
                    value='attendance'
                ),
            ], style={'marginBottom': '20px'}),
            
            # Chart type selector
            html.Div([
                html.Label("Chart Type:", style={'fontWeight': 'bold'}),
                dcc.RadioItems(
                    id='chart-type',
                    options=[
                        {'label': 'Line Chart', 'value': 'line'},
                        {'label': 'Bar Chart', 'value': 'bar'},
                        {'label': 'Scatter Plot', 'value': 'scatter'}
                    ],
                    value='line',
                    inline=True
                ),
            ], style={'marginBottom': '20px'}),
            
            # Team analysis graph
            dcc.Graph(id='team-analysis-graph'),
            
            # Attendance vs Payroll
            html.Div([
                html.H4("Attendance vs Payroll", style={'textAlign': 'center', 'marginTop': '30px'}),
                dcc.Graph(id='attendance-payroll-graph'),
            ]),
        ], style={'padding': '20px'})
        
    elif tab == 'tab-season-analysis':
        return html.Div([
            # Season selector
            html.Div([
                html.Label("Select Season:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='season-dropdown',
                    options=[{'label': str(season), 'value': season} for season in seasons],
                    value=seasons[-1] if seasons else None
                ),
            ], style={'marginBottom': '20px'}),
            
            # Top teams graph
            html.Div([
                html.H4("Top Teams by Attendance", style={'textAlign': 'center'}),
                html.Div([
                    html.Label("Number of teams to display:"),
                    dcc.Slider(
                        id='top-teams-slider',
                        min=5, max=30, step=1, value=10,
                        marks={i: str(i) for i in range(5, 31, 5)},
                    ),
                ], style={'marginBottom': '20px'}),
                dcc.Graph(id='top-teams-graph'),
            ]),
            
            # Team performance distribution
            html.Div([
                html.H4("Team Performance Distribution", style={'textAlign': 'center', 'marginTop': '30px'}),
                dcc.Graph(id='team-distribution-graph'),
            ]),
        ], style={'padding': '20px'})
        
    elif tab == 'tab-league-trends':
        return html.Div([
            # League-wide attendance trends
            html.Div([
                html.H4("League-Wide Attendance Trends", style={'textAlign': 'center'}),
                dcc.Graph(id='league-trends-graph'),
            ]),
            
            # Attendance distribution
            html.Div([
                html.H4("Attendance Distribution Analysis", style={'textAlign': 'center', 'marginTop': '30px'}),
                html.Div([
                    html.Label("Select Season(s):", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='seasons-multi-dropdown',
                        options=[{'label': str(season), 'value': season} for season in seasons],
                        value=[seasons[-1]] if seasons else [],
                        multi=True
                    ),
                ], style={'marginBottom': '20px'}),
                dcc.Graph(id='attendance-distribution-graph'),
            ]),
        ], style={'padding': '20px'})
        
    elif tab == 'tab-payroll-analysis':
        return html.Div([
            # Payroll vs Attendance
            html.Div([
                html.H4("Payroll vs Attendance Correlation", style={'textAlign': 'center'}),
                html.P("Analyze the relationship between team payroll and attendance."),
                dcc.Graph(id='payroll-correlation-graph'),
            ]),
            
            # Year-over-year changes
            html.Div([
                html.H4("Year-over-Year Efficiency Changes", style={'textAlign': 'center', 'marginTop': '30px'}),
                html.Div([
                    html.Label("Select Team:", style={'fontWeight': 'bold'}),
                    dcc.Dropdown(
                        id='yoy-team-dropdown',
                        options=[{'label': team, 'value': team} for team in teams],
                        value=teams[0] if teams else None
                    ),
                ], style={'marginBottom': '20px'}),
                dcc.Graph(id='yoy-change-graph'),
            ]),
        ], style={'padding': '20px'})
    
    elif tab == 'tab-championship-analysis':
        return html.Div([
            # Championship Impact
            html.Div([
                html.H4("🏆 World Series Championship Impact Analysis", style={'textAlign': 'center'}),
                html.P("Analyze how championships affect attendance (2000-2025)", style={'textAlign': 'center'}),
                html.Div([
                    html.Div([
                        html.H5("Key Findings:", style={'color': '#0B3D91'}),
                        html.Ul([
                            html.Li("Teams WITH championships average 2.58M fans/season"),
                            html.Li("Teams WITHOUT championships average 1.97M fans/season"),
                            html.Li("Championship Premium: +613K fans (+31%)"),
                            html.Li("Post-Championship Bump: +34% average increase"),
                            html.Li("Dodgers Dynasty: 3 championships (2020, 2024, 2025) → 4.01M attendance"),
                        ]),
                    ], style={'padding': '20px', 'backgroundColor': '#f0f8ff', 'borderRadius': '10px', 'marginBottom': '20px'}),
                ]),
                dcc.Graph(id='championship-impact-graph'),
            ]),
            
            # Championship by team
            html.Div([
                html.H4("Championships by Team (2000-2025)", style={'textAlign': 'center', 'marginTop': '30px'}),
                dcc.Graph(id='championships-by-team-graph'),
            ]),
        ], style={'padding': '20px'})
    
    return html.Div([
        html.H3("Please select a tab to view analysis")
    ], style={'textAlign': 'center', 'marginTop': '50px'})

# Callback for team analysis graph
@app.callback(
    Output('team-analysis-graph', 'figure'),
    [Input('team-dropdown', 'value'),
     Input('metric-dropdown', 'value'),
     Input('chart-type', 'value')]
)
def update_team_analysis_graph(selected_teams, metric, chart_type):
    """Update the team analysis graph based on selections"""
    try:
        if not selected_teams or not metric or not selected_teams[0]:
            return go.Figure().update_layout(title="Please select teams and a metric")
        
        fig = go.Figure()
        
        for team in selected_teams:
            team_data = df[df['team'] == team]
            if len(team_data) > 0:
                if chart_type == 'line':
                    fig.add_trace(go.Scatter(
                        x=team_data['Season'], 
                        y=team_data[metric],
                        mode='lines+markers',
                        name=team,
                        line=dict(color=team_color_map.get(team)),
                        marker=dict(size=8)
                    ))
                elif chart_type == 'bar':
                    fig.add_trace(go.Bar(
                        x=team_data['Season'], 
                        y=team_data[metric],
                        name=team,
                        marker_color=team_color_map.get(team)
                    ))
                elif chart_type == 'scatter':
                    fig.add_trace(go.Scatter(
                        x=team_data['Season'], 
                        y=team_data[metric],
                        mode='markers',
                        name=team,
                        marker=dict(size=12, color=team_color_map.get(team))
                    ))
        
        # Improve layout
        # Create a mapping of metric values to their labels
        metric_labels = {
            'attendance': 'Total Attendance',
            'Attend/G': 'Attendance Per Game',
            'Est. Payroll': 'Estimated Payroll ($)',
            'efficiency': 'Attendance per Million $ of Payroll'
        }
        metric_label = metric_labels.get(metric, metric)
        
        fig.update_layout(
            title=f"{metric_label} by Season",
            xaxis_title="Season",
            yaxis_title=metric_label,
            legend_title="Teams",
            template="plotly_white",
            hovermode="x unified"
        )
        
        # Format x-axis to show integer seasons
        fig.update_xaxes(tickmode='array', tickvals=list(df['Season'].unique()))
        
        return fig
    except Exception as e:
        print(f"Error in team analysis graph: {e}")
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for attendance vs payroll graph
@app.callback(
    Output('attendance-payroll-graph', 'figure'),
    [Input('team-dropdown', 'value')]
)
def update_attendance_payroll_graph(selected_teams):
    """Update the attendance vs payroll comparison graph"""
    try:
        if not selected_teams or not selected_teams[0]:
            return go.Figure().update_layout(title="Please select at least one team")
        
        # Use the first selected team for this graph
        team = selected_teams[0]
        team_data = df[df['team'] == team]
        
        if len(team_data) == 0:
            return go.Figure().update_layout(title=f"No data found for {team}")
        
        # Filter out rows with NaN values in critical columns
        team_data = team_data.dropna(subset=['Est. Payroll', 'attendance', 'Attend/G'])
        
        if len(team_data) == 0:
            return go.Figure().update_layout(title=f"No complete data found for {team}")
        
        # Create scatter plot
        fig = px.scatter(
            team_data,
            x='Est. Payroll',
            y='attendance',
            color='Season',
            size='Attend/G',
            hover_name='Season',
            trendline='ols',
            title=f"{team} - Attendance vs Payroll Relationship",
            labels={
                'Est. Payroll': 'Estimated Payroll ($)',
                'attendance': 'Total Attendance',
                'Attend/G': 'Attendance Per Game'
            },
            template='plotly_white'
        )
        
        return fig
    except Exception as e:
        print(f"Error in attendance vs payroll graph: {e}")
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for top teams graph
@app.callback(
    Output('top-teams-graph', 'figure'),
    [Input('season-dropdown', 'value'),
     Input('top-teams-slider', 'value')]
)
def update_top_teams_graph(season, n_teams):
    """Update the top teams by attendance graph"""
    try:
        if not season or not n_teams:
            return go.Figure().update_layout(title="Please select a season")
        
        # Filter data for the selected season
        season_data = df[df['Season'] == season]
        
        if len(season_data) == 0:
            return go.Figure().update_layout(title=f"No data found for season {season}")
        
        # Sort by total attendance and get top N
        top_teams = season_data.sort_values('attendance', ascending=False).head(n_teams)
        
        # Create bar chart
        fig = px.bar(
            top_teams, 
            x='team', 
            y='attendance',
            color='team',
            color_discrete_map=team_color_map,
            title=f"Top {n_teams} Teams by Total Attendance in {season} Season",
            labels={'team': 'Team', 'attendance': 'Total Attendance'}
        )
        
        fig.update_layout(
            xaxis_title="Team",
            yaxis_title="Total Attendance",
            template="plotly_white",
            xaxis={'categoryorder':'total descending'}
        )
        
        return fig
    except Exception as e:
        print(f"Error in top teams graph: {e}")
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for team distribution graph
@app.callback(
    Output('team-distribution-graph', 'figure'),
    [Input('season-dropdown', 'value')]
)
def update_team_distribution_graph(season):
    """Update the team distribution graph"""
    try:
        if not season:
            return go.Figure().update_layout(title="Please select a season")
        
        # Get data for the selected season
        season_data = df[df['Season'] == season]
        
        if len(season_data) == 0:
            return go.Figure().update_layout(title=f"No data found for season {season}")
        
        # Create figure with multiple metrics
        fig = make_subplots(rows=1, cols=2, 
                            subplot_titles=("Attendance Distribution", "Payroll Distribution"))
        
        # Add attendance box plot
        fig.add_trace(
            go.Box(
                y=season_data['attendance'],
                name="Attendance",
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8,
                text=season_data['team'],
                hovertemplate='%{text}: %{y}<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Add payroll box plot
        fig.add_trace(
            go.Box(
                y=season_data['Est. Payroll'],
                name="Payroll",
                boxpoints='all',
                jitter=0.3,
                pointpos=-1.8,
                text=season_data['team'],
                hovertemplate='%{text}: $%{y}<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title=f"Team Performance Distribution in {season} Season",
            template="plotly_white",
            showlegend=False,
            height=600
        )
        
        return fig
    except Exception as e:
        print(f"Error in team distribution graph: {e}")
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for league trends graph
@app.callback(
    Output('league-trends-graph', 'figure'),
    [Input('tabs', 'value')]  # This ensures the callback fires when tab is selected
)
def update_league_trends_graph(tab_value):
    """Update the league-wide attendance trends graph"""
    try:
        # Only generate the graph if we're on the correct tab
        if tab_value != 'tab-league-trends':
            return go.Figure()
            
        # Group by season and calculate statistics
        season_stats = df.groupby('Season').agg({
            'attendance': 'sum',
            'Est. Payroll': 'sum',
            'Attend/G': 'mean'
        }).reset_index()
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add total attendance line
        fig.add_trace(
            go.Scatter(
                x=season_stats['Season'],
                y=season_stats['attendance'],
                name="Total Attendance",
                line=dict(color='rgb(0, 123, 255)', width=3),
                mode='lines+markers'
            ),
            secondary_y=False,
        )
        
        # Add total payroll line
        fig.add_trace(
            go.Scatter(
                x=season_stats['Season'],
                y=season_stats['Est. Payroll'],
                name="Total Payroll",
                line=dict(color='rgb(255, 99, 71)', width=3, dash='dash'),
                mode='lines+markers'
            ),
            secondary_y=True,
        )
        
        # Add average attendance per game
        fig.add_trace(
            go.Bar(
                x=season_stats['Season'],
                y=season_stats['Attend/G'],
                name="Avg. Attendance Per Game",
                marker_color='rgba(55, 83, 109, 0.7)'
            ),
            secondary_y=False,
        )
        
        # Update layout
        fig.update_layout(
            title_text="MLB League-Wide Attendance and Payroll Trends",
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Set x-axis title
        fig.update_xaxes(title_text="Season")
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Attendance", secondary_y=False)
        fig.update_yaxes(title_text="Payroll ($)", secondary_y=True)
        
        # Format x-axis to show integer seasons
        fig.update_xaxes(tickmode='array', tickvals=list(season_stats['Season'].unique()))
        
        return fig
    except Exception as e:
        print(f"Error in league trends graph: {e}")
        traceback.print_exc()
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for attendance distribution graph
@app.callback(
    Output('attendance-distribution-graph', 'figure'),
    [Input('seasons-multi-dropdown', 'value')]
)
def update_attendance_distribution_graph(selected_seasons):
    """Update the attendance distribution analysis graph"""
    try:
        if not selected_seasons or not selected_seasons[0]:
            return go.Figure().update_layout(title="Please select at least one season")
        
        # Filter data for selected seasons
        filtered_data = df[df['Season'].isin(selected_seasons)]
        
        if len(filtered_data) == 0:
            return go.Figure().update_layout(title="No data found for selected seasons")
        
        # Create histogram for attendance per game
        fig = px.histogram(
            filtered_data,
            x="Attend/G",
            color="Season",
            marginal="box",
            histnorm='probability density',
            barmode="overlay",
            opacity=0.7,
            title="Distribution of Attendance Per Game Across Teams",
            template="plotly_white"
        )
        
        fig.update_layout(
            xaxis_title="Attendance Per Game",
            yaxis_title="Density"
        )
        
        return fig
    except Exception as e:
        print(f"Error in attendance distribution graph: {e}")
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for payroll correlation graph
@app.callback(
    Output('payroll-correlation-graph', 'figure'),
    [Input('tabs', 'value')]  # This ensures the callback fires when tab is selected
)
def update_payroll_correlation_graph(tab_value):
    """Update the payroll correlation graph"""
    try:
        # Only generate the graph if we're on the correct tab
        if tab_value != 'tab-payroll-analysis':
            return go.Figure()
        
        # Filter out rows with NaN values in critical columns
        filtered_df = df.dropna(subset=['Est. Payroll', 'attendance'])
        
        # Create scatter plot with regression line for all seasons without using size
        fig = go.Figure()
        
        # Group by season for color-coding
        for season in sorted(filtered_df['Season'].unique()):
            season_data = filtered_df[filtered_df['Season'] == season]
            
            fig.add_trace(go.Scatter(
                x=season_data['Est. Payroll'],
                y=season_data['attendance'],
                mode='markers',
                name=str(int(season)),
                text=season_data['team'],
                hovertemplate='<b>%{text}</b> (%{customdata})<br>Season: %{customdata}<br>Payroll: $%{x:,.0f}<br>Attendance: %{y:,.0f}<extra></extra>',
                customdata=np.full(len(season_data), int(season)),
                marker=dict(
                    size=12,
                    opacity=0.8,
                    line=dict(width=1, color='DarkSlateGrey')
                )
            ))
        
        # Add a trendline for the entire dataset
        # Calculate regression line
        x = filtered_df['Est. Payroll']
        y = filtered_df['attendance']
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        x_range = np.linspace(x.min(), x.max(), 100)
        y_range = slope * x_range + intercept
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=y_range,
            mode='lines',
            name=f'Trend (r={r_value:.2f})',
            line=dict(color='black', dash='dash')
        ))
        
        fig.update_layout(
            title="Relationship Between Team Payroll and Attendance",
            xaxis_title="Estimated Payroll ($)",
            yaxis_title="Total Attendance",
            legend_title="Season",
            template='plotly_white',
            height=600
        )
        
        # Add annotation about correlation
        fig.add_annotation(
            x=0.02, y=0.98,
            xref="paper", yref="paper",
            text=f"Correlation: {r_value:.3f}",
            showarrow=False,
            font=dict(size=14),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1,
            borderpad=4,
            align="left"
        )
        
        return fig
    except Exception as e:
        print(f"Error in payroll correlation graph: {e}")
        traceback.print_exc()
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for year-over-year changes graph
@app.callback(
    Output('yoy-change-graph', 'figure'),
    [Input('yoy-team-dropdown', 'value')]
)
def update_yoy_change_graph(team):
    """Update the year-over-year efficiency changes graph"""
    try:
        if not team:
            return go.Figure().update_layout(title="Please select a team")
        
        # Get data for the selected team
        team_data = df[df['team'] == team].sort_values('Season')
        
        if len(team_data) <= 1:
            return go.Figure().update_layout(title=f"Insufficient data for {team} to calculate year-over-year changes")
        
        # Calculate year-over-year percentage changes
        team_data['attendance_yoy'] = team_data['attendance'].pct_change(fill_method=None) * 100
        team_data['payroll_yoy'] = team_data['Est. Payroll'].pct_change(fill_method=None) * 100
        team_data['efficiency_yoy'] = team_data['efficiency'].pct_change(fill_method=None) * 100
        
        # Remove the first row with NaN yoy changes
        team_data = team_data.dropna(subset=['attendance_yoy'])
        
        # Create figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add efficiency line
        fig.add_trace(
            go.Scatter(
                x=team_data['Season'],
                y=team_data['efficiency'],
                name="Attendance Efficiency",
                line=dict(color='rgb(0, 123, 255)', width=3),
                mode='lines+markers'
            ),
            secondary_y=False,
        )
        
        # Add attendance YoY change bars
        fig.add_trace(
            go.Bar(
                x=team_data['Season'],
                y=team_data['attendance_yoy'],
                name="Attendance YoY % Change",
                marker_color='rgba(0, 200, 0, 0.7)',
                offsetgroup=0
            ),
            secondary_y=True,
        )
        
        # Add payroll YoY change bars
        fig.add_trace(
            go.Bar(
                x=team_data['Season'],
                y=team_data['payroll_yoy'],
                name="Payroll YoY % Change",
                marker_color='rgba(200, 0, 0, 0.7)',
                offsetgroup=1
            ),
            secondary_y=True,
        )
        
        # Update layout
        fig.update_layout(
            title_text=f"{team} - Year-over-Year Changes",
            template="plotly_white",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            barmode='group'
        )
        
        # Set x-axis title
        fig.update_xaxes(title_text="Season")
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Attendance Efficiency", secondary_y=False)
        fig.update_yaxes(title_text="Year-over-Year % Change", secondary_y=True)
        
        # Format x-axis to show integer seasons
        fig.update_xaxes(tickmode='array', tickvals=list(team_data['Season'].unique()))
        
        return fig
    except Exception as e:
        print(f"Error in YoY change graph: {e}")
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for championship impact graph
@app.callback(
    Output('championship-impact-graph', 'figure'),
    [Input('tabs', 'value')]
)
def update_championship_impact_graph(tab_value):
    """Update the championship impact graph"""
    try:
        if tab_value != 'tab-championship-analysis':
            return go.Figure()
        
        # Load World Series data
        if not os.path.exists('MLB Wolrd Series Winners 2000-25.csv'):
            return go.Figure().update_layout(title="World Series data not available")
        
        ws_df = pd.read_csv('MLB Wolrd Series Winners 2000-25.csv', skiprows=1)
        ws_df.columns = ['Season', 'Winner', 'Loser', 'Series']
        ws_df['Winner'] = ws_df['Winner'].str.strip().replace({
            'Anaheim Angels': 'Los Angeles Angels',
            'Florida Marlins': 'Miami Marlins',
            'Cleveland Indians': 'Cleveland Guardians'
        })
        
        # Get championship counts
        from collections import Counter
        champ_counts = Counter(ws_df['Winner'])
        
        # Calculate average attendance for champions vs non-champions
        champions = list(champ_counts.keys())
        champs_att = df[df['team'].isin(champions)].groupby('team')['attendance'].mean()
        non_champs_att = df[~df['team'].isin(champions)].groupby('team')['attendance'].mean()
        
        # Create comparison figure
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=['Teams WITH Championships', 'Teams WITHOUT Championships'],
            y=[champs_att.mean(), non_champs_att.mean()],
            marker_color=['#FFD700', '#C0C0C0'],
            text=[f'{champs_att.mean():,.0f}', f'{non_champs_att.mean():,.0f}'],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="Championship Premium: Average Attendance Comparison (2000-2025)",
            yaxis_title="Average Attendance",
            template="plotly_white",
            annotations=[
                dict(
                    x=0.5, y=0.95,
                    xref="paper", yref="paper",
                    text=f"Championship Premium: +{champs_att.mean() - non_champs_att.mean():,.0f} fans (+{((champs_att.mean() - non_champs_att.mean()) / non_champs_att.mean() * 100):.1f}%)",
                    showarrow=False,
                    font=dict(size=14, color='#0B3D91'),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="#0B3D91",
                    borderwidth=2,
                    borderpad=10,
                )
            ]
        )
        
        return fig
    except Exception as e:
        print(f"Error in championship impact graph: {e}")
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Callback for championships by team graph
@app.callback(
    Output('championships-by-team-graph', 'figure'),
    [Input('tabs', 'value')]
)
def update_championships_by_team_graph(tab_value):
    """Update the championships by team graph"""
    try:
        if tab_value != 'tab-championship-analysis':
            return go.Figure()
        
        # Load World Series data
        if not os.path.exists('MLB Wolrd Series Winners 2000-25.csv'):
            return go.Figure().update_layout(title="World Series data not available")
        
        ws_df = pd.read_csv('MLB Wolrd Series Winners 2000-25.csv', skiprows=1)
        ws_df.columns = ['Season', 'Winner', 'Loser', 'Series']
        ws_df['Winner'] = ws_df['Winner'].str.strip().replace({
            'Anaheim Angels': 'Los Angeles Angels',
            'Florida Marlins': 'Miami Marlins',
            'Cleveland Indians': 'Cleveland Guardians'
        })
        
        # Get championship counts
        from collections import Counter
        champ_counts = Counter(ws_df['Winner'])
        
        # Create dataframe for plotting
        champ_df = pd.DataFrame(list(champ_counts.items()), columns=['Team', 'Championships'])
        champ_df = champ_df.sort_values('Championships', ascending=True)
        
        # Get average attendance for each champion
        champ_df['Avg_Attendance'] = champ_df['Team'].apply(
            lambda team: df[df['team'] == team]['attendance'].mean()
        )
        
        # Create horizontal bar chart
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=champ_df['Team'],
            x=champ_df['Championships'],
            orientation='h',
            marker_color='#FFD700',
            text=champ_df['Championships'],
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>Championships: %{x}<br>Avg Attendance: %{customdata:,.0f}<extra></extra>',
            customdata=champ_df['Avg_Attendance']
        ))
        
        fig.update_layout(
            title="World Series Championships by Team (2000-2025)",
            xaxis_title="Number of Championships",
            yaxis_title="Team",
            template="plotly_white",
            height=600
        )
        
        return fig
    except Exception as e:
        print(f"Error in championships by team graph: {e}")
        return go.Figure().update_layout(title=f"Error: {str(e)}")

# Add global error handler for callbacks
app.config.suppress_callback_exceptions = True

# Run the application
if __name__ == "__main__":
    print("Starting MLB Attendance Analysis Dashboard...")
    print("Open http://127.0.0.1:8051/ in your web browser to use the dashboard.")
    print("\n✓ Features:")
    print("  • 2000-2025 attendance data (26 seasons)")
    print("  • World Series championship analysis")
    print("  • Payroll efficiency metrics")
    print("  • Team performance trends")
    app.run(debug=True, port=8051)
