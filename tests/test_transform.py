import pandas as pd
from transform import build_match, build_statistic, build_standings

def test_buildmatch_AggregatesGoalsCorrectly():
    # Arrange
    df = pd.DataFrame({
        'match_id': [1, 1, 1, 1],
        'match_name': ['Season x'] * 4,
        'team_id': [10, 10, 20, 20],
        'is_home': [True, True, False, False],
        'goals_scored': [1, 2, 0, 1]
    })
    
    # Act
    result = build_match(df)
    
    # Assert
    assert result['home_goals'].iloc[0] == 3
    assert result['away_goals'].iloc[0] == 1


def test_buildmatch_TwoMatches_BothMatchesReturned():
    # Arrange
    df = pd.DataFrame({
        'match_id': [1, 1, 2, 2],
        'match_name': ['Season x', 'Season x', 'Season Y', 'Season Y'],
        'team_id': [10, 20, 30, 40],
        'is_home': [True, False, True, False],
        'goals_scored': [2, 1, 0, 0]
    })
    
    # Act
    result = build_match(df)
    
    # Assert
    assert len(result) == 2
    assert result['match_id'].tolist() == [1, 2]

def test_buildstatistic_CalculatesMinutesFractionCorrectly():
    # Arrange
    df = pd.DataFrame({
        'player_id': [1, 2],
        'match_id': [100, 100],
        'goals_scored': [0, 0],
        'minutes_played': [90, 45]
    })
    
    # Act
    result = build_statistic(df)
    
    # Assert
    assert result['fraction_of_total_minutes_played'].iloc[0] == 1.0
    assert result['fraction_of_total_minutes_played'].iloc[1] == 0.5


def test_buildstatistic_CalculatesGoalsFractionCorrectly():
    # Arrange
    df = pd.DataFrame({
        'player_id': [1, 2],
        'match_id': [100, 100],
        'goals_scored': [2, 1],
        'minutes_played': [90, 90]
    })
    
    # Act
    result = build_statistic(df)
    
    # Assert
    assert abs(result['fraction_of_total_goals_scored'].iloc[0] - 0.67) < 0.01
    assert abs(result['fraction_of_total_goals_scored'].iloc[1] - 0.33) < 0.01


def test_buildstatistics_HandlesZeroGoals():
    # Arrange
    df = pd.DataFrame({
        'player_id': [1, 2],
        'match_id': [100, 100],
        'goals_scored': [0, 0],
        'minutes_played': [90, 90]
    })
    
    # Act
    result = build_statistic(df)
    
    # Assert
    assert result['fraction_of_total_goals_scored'].iloc[0] == 0.0
    assert result['fraction_of_total_goals_scored'].iloc[1] == 0.0

def test_buildstandings_CalculatesPointsCorrectly():
    # Arrange
    match_df = pd.DataFrame({
        'match_id': [1],
        'home_team_id': [10],
        'away_team_id': [20],
        'home_goals': [3],
        'away_goals': [0]
    })
    team_df = pd.DataFrame({
        'team_id': [10, 20],
        'team_name': ['Team A', 'Team B']
    })
    
    # Act
    result = build_standings(match_df, team_df)
    
    # Assert
    winner = result[result['team_id'] == 10].iloc[0]
    assert winner['won'] == 1
    assert winner['points'] == 3
    
    loser = result[result['team_id'] == 20].iloc[0]
    assert loser['lost'] == 1
    assert loser['points'] == 0


def test_buildstandings_ProducesCorrectSortingOrder():
    # Arrange
    match_df = pd.DataFrame({
        'match_id': [1, 2],
        'home_team_id': [10, 20],
        'away_team_id': [20, 10],
        'home_goals': [1, 1],
        'away_goals': [2, 2]
    })
    team_df = pd.DataFrame({
        'team_id': [10, 20],
        'team_name': ['Team A', 'Team B']
    })
    
    # Act
    result = build_standings(match_df, team_df)
    
    # Assert
    # Team A should win based on team_name
    assert result['rank'].iloc[0] == 1
    assert result['team_name'].iloc[0] == 'Team A'
