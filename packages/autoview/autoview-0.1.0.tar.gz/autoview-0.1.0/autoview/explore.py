import pandas as pd
import numpy as np
from tabulate import tabulate
from .visualize import plot_summary, plot_missing
from .report import generate_html_report


def explore(df: pd.DataFrame, plots=False, target=None, show_missing=True, generate_report = None):
    print("\n" + "="*60)
    print(" AutoView - Quick Exploratory Data Summary")
    print("="*60)

    print(f"\nDataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")

    print("\nColumn Data Types:")
    print(tabulate(
        df.dtypes.reset_index().rename(columns={0: 'DataType', 'index': 'Column'}),
        headers="keys", tablefmt="psql"
    ))

    print("\nMissing Values per Column:")
    missing = df.isnull().sum()
    print(tabulate(
        missing.reset_index().rename(columns={0: 'MissingCount', 'index': 'Column'}),
        headers="keys", tablefmt="psql"
    ))

    print("\nUnique Values per Column:")
    print(tabulate(
        df.nunique().reset_index().rename(columns={0: 'UniqueValues', 'index': 'Column'}),
        headers="keys", tablefmt="psql"
    ))

    print("\nDescriptive Statistics (Numeric Columns):")
    print(tabulate(
        df.describe().T,
        headers="keys", tablefmt="fancy_grid"
    ))

    if target:
        print(f"\nTarget Column: '{target}' Value Counts")
        print(tabulate(
            df[target].value_counts().reset_index().rename(columns={"index": target, target: "Count"}),
            headers="keys", tablefmt="psql"
        ))
        class_counts = df[target].value_counts(normalize=True)
        if class_counts.min() < 0.1:
            print(f"\n⚠️ Class imbalance detected in target '{target}'. Consider techniques like SMOTE or stratified sampling.")

    # Skewness Detection
    print("\nSkewness Report:")
    skewed_features = df.select_dtypes(include='number').skew()
    for col, skew_val in skewed_features.items():
        if abs(skew_val) > 2:
            print(f"- Feature '{col}' is highly skewed (skewness = {skew_val:.2f}). Consider log or power transform.")

    # Correlation Warnings
    corr = df.select_dtypes(include='number').corr()
    printed_pairs = set()
    print("\nTop Correlated Features (Pearson > 0.35):")
    for col1 in corr.columns:
        for col2 in corr.columns:
            if col1 != col2 and (col2, col1) not in printed_pairs:
                val = corr.loc[col1, col2]
                if abs(val) >= 0.35:
                    print(f"- '{col1}' and '{col2}' show strong correlation ({val:.2f}).")
                    printed_pairs.add((col1, col2))

    duplicate_count = df.duplicated().sum()
    print("\nDuplicate Rows:", duplicate_count)

    text_cols = df.select_dtypes(include='object').columns
    for col in text_cols:
        print(f"\nText Analysis for '{col}':")
        print(f"  - Unique values: {df[col].nunique()}")
        print(f"  - Most frequent: {df[col].mode().iloc[0]}")
        print(f"  - Avg Length: {df[col].dropna().apply(len).mean():.2f}")

    # Alerts / Suggestions
    print("\n" + "-"*60)
    print("💡 Suggested Actions:")
    if missing.sum() > 0:
        print("- Handle missing values: Consider imputing or dropping columns with high null counts.")
    if duplicate_count > 0:
        print("- Remove duplicate rows: Use df.drop_duplicates().")
    if len(text_cols) > 0:
        print("- Encode text features: Use label encoding or one-hot encoding for ML readiness.")
    if target and target not in df.select_dtypes(include='number').columns:
        print(f"- Target '{target}' is not numeric: You may need to encode it for correlation.")
    if any(abs(skewed_features) > 2):
        print("- Some features are highly skewed. Consider transformations for normalization.")
    if len(corr.columns) > 1 and (abs(corr.where(~np.eye(corr.shape[0], dtype=bool))).gt(0.75).any().any()):
        print("- Highly correlated features detected. Consider removing multicollinearity.")
    print("-"*60)

    if plots:
        print("\nGenerating Visual Summaries...")
        plot_summary(df, target)

    if show_missing:
        print("\nGenerating Missing Data Visualizations...")
        plot_missing(df)

    print("\nSummary completed.")
    print("="*60 + "\n")

    if generate_report is None:
        try:
            choice = input("🛠️ Do you want to generate an HTML report? (yes/no): ").strip().lower()
            generate_report = choice in ['yes', 'y']
        except EOFError:
            generate_report = False

    if generate_report:
        print("\n⚙️ Generating HTML report...")
        generate_html_report(df, target, plots=plots, show_missing=show_missing)
        print("☑ Report saved successfully as 'autoview_report.html'")
    else:
        print("\n🔜 Skipping HTML report generation.")