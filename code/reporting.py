import pandas as pd

def generate_html_report(project_root):
    """Create final HTML report"""
    results_df = pd.read_csv(project_root/"processed_data"/"analysis_results.csv")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>UNICEF Maternal Health Coverage Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #3498db; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .results-table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                box-shadow: 0 2px 3px rgba(0,0,0,0.1);
            }}
            .results-table th, .results-table td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            .results-table th {{
                background-color: #3498db;
                color: white;
            }}
            .figure-container {{ text-align: center; margin: 30px 0; }}
            .figure-container img {{ max-width: 800px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <h1>UNICEF Maternal Health Coverage Analysis</h1>
        
        <div class="figure-container">
            <img src="coverage_comparison.png" alt="Coverage Comparison">
        </div>
        
        <h2>Analysis Results</h2>
        {results_df.to_html(classes='results-table', index=False)}
    </body>
    </html>
    """
    
    output_path = project_root/"results"/"unicef_report.html"
    with open(output_path, "w") as f:
        f.write(html_content)