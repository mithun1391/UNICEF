import os
import sys
from pathlib import Path

def get_project_root():
    """Get the absolute path to the project root with verification"""
    script_path = Path(__file__).absolute()
    project_root = script_path.parent.parent
    
    # Debugging output
    print(f"\nDEBUGGING INFORMATION:")
    print(f"Script location: {script_path}")
    print(f"Project root: {project_root}")
    print(f"Raw data path: {project_root/'raw_data'}")
    
    
    return project_root

PROJECT_ROOT = get_project_root()


def main():
    print("=== UNICEF Maternal Health Coverage Analysis ===")
    
        
    try:
        from data_processing import load_and_clean_data
        from calculations import calculate_weighted_coverage
        from visualization import create_visualization
        from reporting import generate_html_report
        
        # Create output folders
        (PROJECT_ROOT/"processed_data").mkdir(exist_ok=True)
        (PROJECT_ROOT/"results").mkdir(exist_ok=True)
        
        print("\nSTEP 1: Data Processing")
        merged_data = load_and_clean_data(PROJECT_ROOT)
        
        print("\nSTEP 2: Calculations")
        results = calculate_weighted_coverage(merged_data, PROJECT_ROOT)
        
        print("\nSTEP 3: Visualization")
        create_visualization(results, PROJECT_ROOT)
        
        print("\nSTEP 4: Reporting")
        generate_html_report(PROJECT_ROOT)
        
        print("\nSUCCESS! Analysis completed.")
        print(f"Results saved in: {PROJECT_ROOT/'results'}")
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()