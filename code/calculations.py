import pandas as pd
import os
from pathlib import Path

def calculate_weighted_coverage(df, project_root):
    """
    Calculate weighted coverage with robust error handling.
    Args:
        df: DataFrame from load_and_clean_data()
        project_root: Path to project directory
    """
    try:
        # Validate input
        required_cols = {'Status', 'Births_2022'}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"Missing columns: {required_cols - set(df.columns)}")
        
        # Clean data
        df = df.dropna(subset=['Births_2022']).query('Births_2022 > 0')
        indicators = [col for col in df.columns if col.startswith('MNCH_')]
        
        # Calculate metrics
        results = []
        for status in ['on-track', 'off-track']:
            subset = df[df['Status'] == status]
            if subset.empty:
                continue
                
            total_births = subset['Births_2022'].sum()
            for indicator in indicators:
                try:
                    coverage = (subset[indicator] * subset['Births_2022']).sum() / total_births
                    results.append({
                        'Status': status,
                        'Indicator': indicator.replace('MNCH_', ''),
                        'Coverage (%)': round(coverage * 100, 1),
                        'Countries': len(subset),
                        'Total Births': f"{total_births:,}"
                    })
                except Exception as e:
                    print(f"Skipped {indicator} ({status}): {str(e)}")
        
        # Save results
        results_df = pd.DataFrame(results)
        output_path = project_root / "processed_data" / "analysis_results.csv"
        results_df.to_csv(output_path, index=False)
        print(f"✅ Results saved to {output_path}")
        return results_df
        
    except Exception as e:
        print(f"CALCULATION ERROR:\n{str(e)}")
        raise

if __name__ == "__main__":
    # Test with sample data
    test_data = pd.DataFrame({
        'Status': ['on-track', 'off-track'],
        'MNCH_ANC4': [0.8, 0.5],
        'Births_2022': [1000, 2000]
    })
    calculate_weighted_coverage(test_data, Path.cwd())