import pandas as pd
from pathlib import Path
from calculations import calculate_weighted_coverage  # Import the calculation function

def load_tracking_data(project_root):
    """Load and process country tracking status data"""
    file_path = project_root / "raw_data" / "On-track and off-track countries.xlsx"
    try:
        df = pd.read_excel(file_path, sheet_name='Sheet1')
        if 'Status.U5MR' not in df.columns or 'ISO3Code' not in df.columns:
            raise ValueError("Missing required columns in tracking data")
        
        df['Status'] = df['Status.U5MR'].apply(
            lambda x: 'on-track' if x in ['Achieved', 'On Track'] else 'off-track'
        )
        return df[['ISO3Code', 'Status']]
    except Exception as e:
        print(f"ERROR LOADING TRACKING DATA:\nFile: {file_path}\nError: {str(e)}")
        raise

def load_indicator_data(project_root):
    """Load and process health indicator data"""
    file_path = project_root / "raw_data" / "fusion_GLOBAL_DATAFLOW_UNICEF_1.0_all.csv"
    try:
        df = pd.read_csv(file_path)
        df = df[
            (df['INDICATOR:Indicator'].str.contains('MNCH_ANC4|MNCH_SBA')) &
            (pd.to_numeric(df['TIME_PERIOD:Time period']).between(2018, 2022))
        ]
        df['ISO3Code'] = df['REF_AREA:Geographic area'].str.extract(r'([A-Z]{3})')
        df = df.sort_values('TIME_PERIOD:Time period', ascending=False)
        df = df.drop_duplicates(['ISO3Code', 'INDICATOR:Indicator'])
        
        pivot_df = df.pivot(
            index='ISO3Code',
            columns='INDICATOR:Indicator',
            values='OBS_VALUE:Observation Value'
        ).reset_index()
        return pivot_df
    except Exception as e:
        print(f"ERROR LOADING INDICATOR DATA:\nFile: {file_path}\nError: {str(e)}")
        raise

def load_population_data(project_root):
    """Load population data with auto sheet/skiprow detection"""
    file_path = project_root / "raw_data" / "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
    try:
        excel_file = pd.ExcelFile(file_path)
        for sheet_name in excel_file.sheet_names:
            for skiprows in range(0, 20):
                df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows, nrows=5)
                if 'Year' in df.columns:
                    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows)
                    break
        
        required_cols = ['Year', 'ISO3 Alpha-code', 'Births (thousands)']
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing columns in population data")
            
        df = df[df['Year'] == 2022]
        df = df[['ISO3 Alpha-code', 'Births (thousands)']]
        df.columns = ['ISO3Code', 'Births_2022']
        df['Births_2022'] = df['Births_2022'] * 1000
        return df.dropna()
    except Exception as e:
        print(f"ERROR LOADING POPULATION DATA:\nFile: {file_path}\nError: {str(e)}")
        raise

def load_and_clean_data(project_root):
    """Main data processing pipeline"""
    try:
        print("\nLoading datasets...")
        track_df = load_tracking_data(project_root)
        ind_df = load_indicator_data(project_root)
        pop_df = load_population_data(project_root)
        
        merged_df = pd.merge(
            pd.merge(ind_df, track_df, on='ISO3Code', how='inner'),
            pop_df, on='ISO3Code', how='left'
        )
        
        if merged_df.empty:
            raise ValueError("Merge resulted in empty dataframe")
        
        # Save raw merged data
        output_dir = project_root / "processed_data"
        output_dir.mkdir(exist_ok=True)
        merged_df.to_csv(output_dir / "merged_data.csv", index=False)
        
        print("✅ Data processing complete")
        return merged_df
    except Exception as e:
        print(f"\nDATA PROCESSING FAILED:\nError: {str(e)}")
        raise

if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    merged_data = load_and_clean_data(project_root)
    results = calculate_weighted_coverage(merged_data, project_root)  # Now properly called
    print(results.head())