import pandas as pd
import os
from validation import validate_business_rules
from transform import build_match, build_team, build_player, build_statistic, build_standings

input_file = 'assignment_input.csv'
output_directory = 'output'

def export_output_to_jsonl(df, filename):
    """Saves a DataFrame to the output directory in JSON Lines format."""
    os.makedirs(output_directory, exist_ok=True)
    #orient = records so each row of the file represents one row of the data
    #force_ascii = False to for UTF-8 encoding.
    df.to_json(os.path.join(output_directory, filename), orient="records", lines=True, force_ascii=False)

def main():
    input_df = pd.read_csv(input_file, encoding='ISO-8859-1')
    
    #'is_home' contains the value 'yes'. Making the assumption that yes = True, and converting 'is_home' to boolean
    input_df['is_home'] = input_df['is_home'].astype(str).str.strip().str.lower()
    input_df['is_home'] = input_df['is_home'].map({
        'true': True,
        'false': False,
        'yes': True
    })
    
    clean_df, anomalies_df = validate_business_rules(input_df)
    
    match_df = build_match(clean_df)
    team_df = build_team(clean_df)
    player_df = build_player(clean_df)
    statistic_df = build_statistic(clean_df)
    standings_df = build_standings(match_df, team_df)

    
    export_output_to_jsonl(match_df, "match.jsonl")
    export_output_to_jsonl(team_df, "team.jsonl")
    export_output_to_jsonl(player_df, "player.jsonl")
    export_output_to_jsonl(statistic_df, "statistic.jsonl")
    export_output_to_jsonl(standings_df, "standings.jsonl")
    
    anomalies_df.to_json(os.path.join('output', 'anomalies.json'), orient='records', indent=2, force_ascii=False)

if __name__ == "__main__":
    main()
    