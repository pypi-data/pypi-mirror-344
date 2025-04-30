import pandas as pd
from autoview.report import generate_html_report
import os

def test_html_report_generation():
    df = pd.DataFrame({
        "age": [20, 30, 40, 25],
        "salary": [50000, 60000, 70000, 80000],
        "gender": ["M", "F", "F", "M"]
    })
    report_path = "test_report.html"
    generate_html_report(df, target="gender", report_name=report_path, plots=False, show_missing=False)

    assert os.path.exists(report_path)
    os.remove(report_path)
