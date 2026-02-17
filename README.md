## Setup
From the root directory, install required dependencies:
```bash
pip install -r requirements.txt
```

For the application to work, you must place 'assignment_input.csv' in the root directory.

## Running the Program
From the root directory execute:
```bash
python main.py
```

Output files will be created in the `output/` directory.

## Running Tests
From the root directory execute:
```bash
pytest
```

## Business Rules
The assignment states that data should be "validated against business rules" but does not explicitly enumerate them. Based on the specification, I implemented the following validations:

1. **Minutes Played**: Must be between 0 and 90.
   - Reason: It is specified that "All matches should be 90 minutes in duration"
   
2. **Goals Scored**: Cannot be negative.
   - Reason: Negative goals are impossible

It is stated that it can be assumed that "each player only plays for one team across the entire dataset",
this could be validated as a data quality check but i interpret this as meaning it is always satisfied in this case.

Rows violating any of these rules are excluded from output datasets and written to `output/anomalies.json`.

## Additional Observations
The **is_home** field contained the values *True, False, yes*. But it is specified that **is_home** should be of type boolean.
I decided that *yes* should be interpreted as *True* in order to convert it to the specified type.

## Futurework
Given more time, i could add the following:
  - Error handling: e.g. in build_match verify each match has exactly 1 home team and 1 away team.
  - Complete test suite: make sure code works with respect to each specification, for all contexts.
