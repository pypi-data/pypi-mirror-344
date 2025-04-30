from tabulate import tabulate
import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import seaborn as sns
import missingno as msno
from io import BytesIO
import base64
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

def encode_plot_to_base64():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    return f"<img src='data:image/png;base64,{img_base64}'/>"

def infer_column_roles(df):
    roles = {}
    for col in df.columns:
        unique_vals = df[col].nunique()
        dtype = df[col].dtype
        if unique_vals == df.shape[0] or 'id' in col.lower():
            roles[col] = ('ID', 'Drop - Unique identifier')
        elif pd.api.types.is_string_dtype(df[col]) and unique_vals > 0.75 * df.shape[0]:
            roles[col] = ('Free Text', 'Consider NLP or drop')
        elif pd.api.types.is_string_dtype(df[col]) and any(name in col.lower() for name in ['name']):
            roles[col] = ('Name', 'Extract titles or drop')
        elif pd.api.types.is_datetime64_any_dtype(df[col]) or 'date' in col.lower():
            roles[col] = ('Datetime', 'Consider time-based features')
        elif unique_vals > 50:
            roles[col] = ('High Cardinality', 'Use frequency/target encoding')
        elif df[col].dtype in ['int64', 'float64'] and df[col].std() < 0.01:
            roles[col] = ('Low Variance', 'Drop - low information')
        else:
            roles[col] = ('Useful', 'Likely useful for modeling')
    return roles

def generate_html_report(df, target=None, report_name="autoview_report.html", plots=True, show_missing=True, verbose=True):
    insights = []
    html_charts = []
    roles = infer_column_roles(df)

    nulls = df.isnull().sum()
    if nulls.sum() > 0:
        top_null = nulls.sort_values(ascending=False).head(1)
        insights.append(f"Column '<b>{top_null.index[0]}</b>' has the most missing values: <b>{top_null.iloc[0]}</b> nulls.")

    uniq = df.nunique()
    most_unique = uniq.sort_values(ascending=False).head(1)
    insights.append(f"Column '<b>{most_unique.index[0]}</b>' has the highest number of unique values: <b>{most_unique.iloc[0]}</b>.")

    if target and target in df.columns:
        class_counts = df[target].value_counts()
        if class_counts.min() / class_counts.max() < 0.5:
            insights.append(f"Target '<b>{target}</b>' seems imbalanced — class <b>{class_counts.idxmin()}</b> is underrepresented.")

        plt.figure(figsize=(6, 4))
        df[target].value_counts().plot(kind='bar', color='#337ab7')
        plt.title(f"Distribution of {target}")
        plt.ylabel("Count")
        html_charts.append((f"Target Distribution for '{target}'", encode_plot_to_base64(), "Distribution of target classes in the dataset."))

    # Correlation Heatmap
    if len(df.select_dtypes(include='number').columns) >= 2:
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.select_dtypes(include='number').corr(), annot=True, fmt='.2f', cmap='coolwarm')
        plt.title("Correlation Heatmap")
        html_charts.append(("Correlation Heatmap", encode_plot_to_base64(), "Shows correlations between numeric features."))

    # Missing Value Visualizations
    for name, plot_func, caption in [
        ("Missingno Matrix", msno.matrix, "Visual representation of missing data patterns."),
        ("Missingno Bar Chart", msno.bar, "Bar chart of missing values per column."),
        ("Missingno Heatmap", msno.heatmap, "Correlation between missing values across columns."),
        ("Missingno Dendrogram", msno.dendrogram, "Clustering of missing values by similarity.")
    ]:
        plt.figure()
        plot_func(df)
        plt.title(name)
        html_charts.append((name, encode_plot_to_base64(), caption))

    # Outlier Boxplots and Histograms for Useful Columns Only
    num_cols = df.select_dtypes(include='number').columns
    for col in num_cols:
        role, _ = roles.get(col, (None, None))
        if role in ['ID', 'Low Variance']:  # Skip unnecessary plots
            continue

        # Histogram
        plt.figure(figsize=(6, 3))
        sns.histplot(df[col].dropna(), kde=True, bins=30)
        plt.title(f"Distribution of {col}")
        html_charts.append((f"Histogram - {col}", encode_plot_to_base64(), f"Distribution and density of values in '{col}'."))

        # Boxplot
        plt.figure(figsize=(6, 1.5))
        sns.boxplot(x=df[col])
        plt.title(f"Outliers in {col}")
        html_charts.append((f"Boxplot - {col}", encode_plot_to_base64(), f"Potential outliers detected using IQR method in '{col}'."))

    # Feature Importance
    if target and target in df.columns:
        try:
            df_copy = df.dropna()
            if not df_copy.empty:
                X = df_copy.drop(columns=[target])
                y = df_copy[target]

                for col in X.select_dtypes(include='object').columns:
                    X[col] = LabelEncoder().fit_transform(X[col])

                if y.dtype == 'object':
                    y = LabelEncoder().fit_transform(y)
                    model = RandomForestClassifier(random_state=42)
                else:
                    model = RandomForestRegressor(random_state=42)

                X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)
                model.fit(X_train, y_train)

                feat_imp = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=True).tail(10)

                plt.figure(figsize=(8, 6))
                feat_imp.plot(kind='barh', color='#00a65a')
                plt.title("Top 10 Feature Importances")
                html_charts.append(("Feature Importance", encode_plot_to_base64(), f"Top features influencing the target '{target}'."))
        except Exception:
            pass

    # HTML Output
    with open(report_name, 'w', encoding='utf-8') as f:
        f.write("""
        <html>
        <head>
            <title>AutoView Report</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f9f9f9;
                    color: #333;
                }
                h1, h2 {
                    color: #004080;
                }
                .table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 30px;
                }
                .table th, .table td {
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: left;
                }
                .table th {
                    background-color: #e6f0ff;
                }
                p {
                    font-size: 16px;
                }
                .section {
                    padding: 10px 20px;
                    background-color: #ffffff;
                    margin-bottom: 20px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                }
                img {
                    max-width: 100%;
                    margin-top: 10px;
                }
                .caption {
                    font-style: italic;
                    color: #555;
                    margin-top: 5px;
                }
            </style>
        </head>
        <body>
            <h1>📊 AutoView - Exploratory Data Report</h1>
        """)

        f.write("<div class='section'><h2>Dataset Shape</h2>")
        f.write(f"<p>{df.shape[0]} rows × {df.shape[1]} columns</p></div>")

        f.write("<div class='section'><h2>Column Data Types</h2>")
        f.write(df.dtypes.to_frame('DataType').to_html(classes="table", border=0))
        f.write("</div>")

        f.write("<div class='section'><h2>Column Role Classification</h2>")
        role_df = pd.DataFrame.from_dict(roles, orient='index', columns=['Role', 'Recommendation'])
        f.write(role_df.to_html(classes="table", border=0))
        f.write("</div>")

        f.write("<div class='section'><h2>Missing Values</h2>")
        f.write(nulls.to_frame('MissingValues').to_html(classes="table", border=0))
        f.write("</div>")

        f.write("<div class='section'><h2>Unique Values</h2>")
        f.write(uniq.to_frame('UniqueValues').to_html(classes="table", border=0))
        f.write("</div>")

        f.write("<div class='section'><h2>Descriptive Statistics (Numeric)</h2>")
        f.write(df.describe().to_html(classes="table", border=0))
        f.write("</div>")

        if target:
            f.write("<div class='section'><h2>Target Column</h2>")
            if target in df.columns:
                f.write(df[target].value_counts().to_frame('Count').to_html(classes="table", border=0))
            else:
                f.write(f"<p>Target '{target}' not found in dataset.</p>")
            f.write("</div>")

        f.write("<div class='section'><h2>💡 Suggested Actions</h2><ul>")
        if nulls.sum() > 0:
            f.write("<li>Handle missing values (imputation or deletion)</li>")
        if df.duplicated().sum() > 0:
            f.write("<li>Remove duplicate rows using <code>df.drop_duplicates()</code></li>")
        if df.select_dtypes(include='object').shape[1] > 0:
            f.write("<li>Encode categorical features using label encoding or one-hot encoding</li>")
        f.write("</ul></div>")

        if insights:
            f.write("<div class='section'><h2>🧠 AutoView Insights</h2>")
            for line in insights:
                f.write(f"<p>{line}</p>")
            f.write("</div>")

        for chart in html_charts:
            if len(chart) == 2:
                title, img = chart
                f.write(f"<div class='section'><h2>{title}</h2>{img}</div>")
            elif len(chart) == 3:
                title, img, caption = chart
                f.write(f"<div class='section'><h2>{title}</h2>{img}<p class='caption'>{caption}</p></div>")

        f.write("</body></html>")