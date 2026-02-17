import pandas as pd

def build_match(df):
    matches = []
    for match_id, group in df.groupby('match_id'):
        match_name = group['match_name'].iloc[0]
        
        teams = group[['team_id', 'is_home']].drop_duplicates()
        
        home_team = teams[teams['is_home']]
        away_team = teams[~teams['is_home']]
        
        home_team_id = home_team['team_id'].iloc[0]
        away_team_id = away_team['team_id'].iloc[0]
        
        home_goals = group[group['is_home']]['goals_scored'].sum()
        away_goals = group[~group['is_home']]['goals_scored'].sum()
        
        matches.append({
            "match_id": match_id,
            "match_name": match_name,
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,
            "home_goals": home_goals,
            "away_goals": away_goals
        })
        
    return pd.DataFrame(matches)

def build_team(df):
    return (
        df[['team_id', 'team_name']]
        .drop_duplicates()
        .sort_values('team_id')
    )
    
def build_player(df):
    return (
        df[['player_id', 'team_id', 'player_name']]
        .drop_duplicates()
        .sort_values('player_id')
    )


def build_statistics(df):
    df = df.reset_index(drop = True)
    match_goals = df.groupby('match_id')['goals_scored'].transform('sum')
    
    stats_df = pd.DataFrame({
        'stat_id': range(1, len(df) + 1),
        'player_id': df['player_id'],
        'match_id': df['match_id'],
        'goals_scored': df['goals_scored'],
        'minutes_played': df['minutes_played'],
        'fraction_of_total_minutes_played': round(df['minutes_played'] / 90.0, 4),
        'fraction_of_total_goals_scored': ( (df['goals_scored'] / match_goals).fillna(0.0).round(4))
    })
    
    return stats_df

def build_standings(match_df, team_df):
    """Calculates the standings using the match (match_df) and team (team_df) dataframes."""
    standings_list = []
    
    for _, team in team_df.iterrows():
        team_id = team['team_id']
        team_name = team['team_name']
        
        home_games = match_df[match_df['home_team_id'] == team_id]
        away_games = match_df[match_df['away_team_id'] == team_id]
        
        goals_for = home_games['home_goals'].sum() + away_games['away_goals'].sum()
        
        goals_against = home_games['away_goals'].sum() + away_games['home_goals'].sum()

        home_wins = (home_games['home_goals'] > home_games['away_goals']).sum()
        away_wins = (away_games['away_goals'] > away_games['home_goals']).sum()
        wins = home_wins + away_wins

        home_draws = (home_games['home_goals'] == home_games['away_goals']).sum()
        away_draws = (away_games['away_goals'] == away_games['home_goals']).sum()
        draws = home_draws + away_draws
        
        played = len(home_games) + len(away_games)
        losses = played - wins - draws
        points = (wins * 3) + draws
        
        standings_list.append({
            "team_id": team_id,
            "team_name": team_name,
            "played": played,
            "won": wins,
            "drawn": draws,
            "lost": losses,
            "goals_for": goals_for,
            "goals_against": goals_against,
            "goal_difference": goals_for - goals_against,
            "points": points
        })
    
    standings_df = pd.DataFrame(standings_list)
    standings_df = standings_df.sort_values(
        by=['points', 'goal_difference', 'goals_for', 'team_name'],
        ascending=[False, False, False, True]
    )
    
    standings_df.insert(0, 'rank', range(1, len(standings_df) + 1))
    
    return standings_df
