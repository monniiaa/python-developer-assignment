import pandas as pd
from validation import validate_business_rules

def test_validatebusinessrules_NoData_NoAnomaliesExtracted():
    # Arrange
    df = pd.DataFrame({
        'minutes_played': [],
        'goals_scored': []
    })
    
    # Act
    clean_df, anomalies_df = validate_business_rules(df)
    
    # Assert
    assert len(clean_df) == 0
    assert len(anomalies_df) == 0


def test_validatebusinessrules_NoViolation_NoAnomaliesExtracted():
    # Arrange
    df = pd.DataFrame({
        'minutes_played': [45, 10],
        'goals_scored': [0, 1]
    })
    
    # Act
    clean_df, anomalies_df = validate_business_rules(df)
    
    # Assert
    assert len(clean_df) == 2
    assert len(anomalies_df) == 0


def test_validatebusinessrules_InvalidMinutes_AnomaliesExtracted():
    # Arrange
    df = pd.DataFrame({
        'minutes_played': [-5],
        'goals_scored': [0]
    })
    
    # Act
    clean_df, anomalies_df = validate_business_rules(df)
    
    # Assert
    assert len(clean_df) == 0
    assert len(anomalies_df) == 1
    assert "Minutes played must be between 0 and 90" in anomalies_df['violation'].values[0]


def test_validatebusinessrules_InvalidGoals_AnomaliesExtracted():
    # Arrange
    df = pd.DataFrame({
        'minutes_played': [45],
        'goals_scored': [-1]  
    })
    
    # Act
    clean_df, anomalies_df = validate_business_rules(df)
    
    # Assert
    assert len(clean_df) == 0
    assert len(anomalies_df) == 1
    assert "Goals scored cannot be negative" in anomalies_df['violation'].values[0]


def test_validatebusinessrules_MultipleViolations_AnomaliesExtracted():
    # Arrange
    df = pd.DataFrame({
        'minutes_played': [-5],  
        'goals_scored': [-2]     
    })
    
    # Act
    clean_df, anomalies_df = validate_business_rules(df)
    
    # Assert
    assert len(clean_df) == 0
    assert len(anomalies_df) == 1
    
    violation_msg = anomalies_df['violation'].values[0]
    assert "Minutes played must be between 0 and 90; Goals scored cannot be negative" in violation_msg
    