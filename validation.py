import pandas as pd

def _check_invalid_minutes(df):
    return (df['minutes_played'] < 0) | (df['minutes_played'] > 90)

def _check_invalid_goals(df):
    return df['goals_scored'] < 0

def validate_business_rules(df):
    """
    Validate dataframe against all of the business rules.
    Returns: (original dataframe with no anomalies, anomalies dataframe)
    """
    invalid_min = _check_invalid_minutes(df)
    invalid_goals = _check_invalid_goals(df)
 
    anomalies_mask = invalid_min | invalid_goals

    anomalies_df = df[anomalies_mask].copy()
    
    violation_messages = []
    for idx in anomalies_df.index:
        violations = []
        if invalid_min[idx]:
            violations.append("Minutes played must be between 0 and 90")
        if invalid_goals[idx]:
            violations.append("Goals scored cannot be negative")
        
        violation_messages.append("; ".join(violations))
        
    anomalies_df['violation'] = violation_messages

    return df[~anomalies_mask], anomalies_df
