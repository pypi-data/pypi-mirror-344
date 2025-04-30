import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def plot_summary(df, target=None):
    num_cols = df.select_dtypes(include='number').columns
    cat_cols = df.select_dtypes(exclude='number').columns

    print("\n▶️ Generating Histograms for numeric columns...")
    for col in num_cols:
        if df[col].nunique() > 1 and not col.lower().endswith("id"):
            plt.figure(figsize=(8, 4))
            sns.histplot(df[col].dropna(), kde=True, bins=30)
            plt.title(f"Distribution of {col}")
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    print("\n▶️ Generating Countplots for categorical columns...")
    for col in cat_cols:
        if df[col].nunique() <= 50:
            plt.figure(figsize=(8, 4))
            sns.countplot(x=col, data=df, order=df[col].value_counts().index)
            plt.title(f"Count Plot of {col}")
            plt.xticks(rotation=45)
            plt.xlabel(col)
            plt.ylabel('Count')
            plt.grid(True)
            plt.tight_layout()
            plt.show()

    if not target:
        print("\n▶️ No target provided. Suggesting potential target candidates:")
        candidate_targets = []
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64'] and df[col].nunique() < 10:
                candidate_targets.append((col, 'categorical'))
            elif df[col].dtype == 'object' and df[col].nunique() < 10:
                candidate_targets.append((col, 'categorical'))
            elif df[col].dtype in ['int64', 'float64'] and df[col].nunique() > 10:
                candidate_targets.append((col, 'regression'))

        if candidate_targets:
            for col, kind in candidate_targets[:3]:
                print(f" - {col} ({kind} target)")
        else:
            print(" ⚠️ No obvious target candidates found.")

    if target:
        print(f"\n▶️ Correlation with Target '{target}':")
        numeric_df = df.select_dtypes(include='number')
        if target in numeric_df.columns:
            correlations = numeric_df.corr()[target].sort_values(ascending=False)
            print(correlations)

            if df[target].nunique() <= 10:
                class_dist = df[target].value_counts(normalize=True)
                if class_dist.min() < 0.1:
                    print("⚠️ Class imbalance detected in target. Consider SMOTE or stratified sampling.")
        else:
            print(f"⚠️ Warning: Target '{target}' is not numeric or not found in numeric columns.")

    print("\n▶️ Correlation Heatmap (All numeric features)...")
    plt.figure(figsize=(10, 8))
    corr = df.select_dtypes(include='number').corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Correlation Heatmap")
    plt.tight_layout()
    plt.show()

    print("\n▶️ Outlier Detection (Boxplots & IQR Method)...")
    for col in num_cols:
        if df[col].nunique() > 1 and not col.lower().endswith("id"):
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
            outlier_count = outliers.shape[0]
            print(f"{col}: {outlier_count} potential outliers detected using IQR")
            plt.figure(figsize=(6, 1.5))
            sns.boxplot(x=df[col])
            plt.title(f"Boxplot for {col}")
            plt.tight_layout()
            plt.show()

    print("\n▶️ Categorical Feature Insights...")
    for col in cat_cols:
        unique_vals = df[col].nunique()
        print(f"'{col}' → {unique_vals} unique categories")
        if unique_vals > 10:
            print(f"  ⚠️ Consider encoding '{col}' using frequency or target encoding (too many unique values)")
        else:
            print(f"  ✅ Suitable for one-hot encoding")
        print("  Most frequent category:", df[col].mode().iloc[0])

    print("\n▶️ Time-based Feature Detection...")
    datetime_cols = df.select_dtypes(include='datetime').columns
    if len(datetime_cols) > 0:
        for col in datetime_cols:
            print(f"'{col}' appears to be a time-based feature. Consider time series analysis (trend/seasonality).")
    else:
        print("No datetime columns detected.")

    if target and target in df.columns:
        print("\n▶️ Feature Importance (Random Forest)...")
        try:
            df_copy = df.copy().dropna()
            if df_copy.empty:
                print("⚠️ Skipping feature importance: No rows without missing values.")
                return

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

            importances = model.feature_importances_
            feature_names = X.columns
            feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)

            print(feat_imp.head(10))
            feat_imp.head(10).plot(kind='barh')
            plt.gca().invert_yaxis()
            plt.title("Top 10 Feature Importances")
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"⚠️ Could not compute feature importances: {e}")
            if target in num_cols:
                print("\nFalling back to correlation-based importance:")
                print(df[num_cols].corr()[target].sort_values(ascending=False).head(10))


def plot_missing(df):
    print("\n▶️ Visualizing Missing Data - Matrix...")
    msno.matrix(df)
    plt.title("Missing Value Matrix")
    plt.tight_layout()
    plt.show()

    print("\n▶️ Visualizing Missing Data - Bar Chart...")
    msno.bar(df)
    plt.title("Missing Values per Column")
    plt.tight_layout()
    plt.show()

    print("\n▶️ Visualizing Missing Data - Heatmap...")
    msno.heatmap(df)
    plt.title("Missing Value Correlation Heatmap")
    plt.tight_layout()
    plt.show()

    print("\n▶️ Visualizing Missing Data - Dendrogram...")
    msno.dendrogram(df)
    plt.title("Missing Value Clustering Dendrogram")
    plt.tight_layout()
    plt.show()
