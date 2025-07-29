# UNICEF Maternal Health Coverage Analysis

Modular analysis of maternal health indicators comparing on-track vs off-track countries.

## Project Structure
# UNICEF Maternal Health Coverage Analysis

Modular analysis of maternal health indicators comparing on-track vs off-track countries.

## Project Structure
UNICEF/
├── code/ # All analysis scripts
│ ├── main.py # Workflow orchestrator
│ ├── data_processing.py # Data loading/cleaning
│ ├── calculations.py # Statistical calculations
│ ├── visualization.py # Plot generation
│ └── reporting.py # Report creation
├── raw_data/ # Input data files
├── processed_data/ # Cleaned data (auto-created)
└── results/ # Outputs (auto-created)


## Setup

1. Place these files in `UNICEF/raw_data/`:
   - `fusion_GLOBAL_DATAFLOW_UNICEF_1.0_all.csv`
   - `On-track and off-track countries.xlsx`
   - `WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx`

2. Install dependencies:

   pip install -r requirements.txt

Run the analysis:

python code/main.py

Outputs
Processed data in processed_data/

Visualizations and report in results/

Positions Applied For:
1. Learning and Skills Data Analyst Consultant
2. Household Survey Data Analyst Consultant
3. Microdata Harmonization Consultant
4. Administrative Data Analyst

This structure provides:
1. Clear separation of concerns
2. Modular, maintainable code
3. Easy debugging and testing
4. Self-documenting workflow
5. Automatic folder creation
6. Professional outputs

The `main.py` script orchestrates the entire workflow by calling each module in sequence. Each script handles one specific aspect of the analysis, making the code easier to maintain and modify.