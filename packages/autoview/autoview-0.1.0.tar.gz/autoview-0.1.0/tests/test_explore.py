from autoview import explore
import pandas as pd

def test_explore_runs():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [5, 6, None, 8],
        "C": ["cat", "dog", "dog", "mouse"]
    })
    # Ensure this disables the input() prompt
    explore(df, plots=False, show_missing=False, generate_report=False)
