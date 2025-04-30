<p align="center">
  <img src="https://raw.githubusercontent.com/avinash-betha/autoview/main/assets/logo.png" alt="AutoView Logo" width="200"/>
</p>

<h1 align="center">AutoView</h1>

<p align="center">
  <strong>⚡ Fast, Visual, and Insightful Exploratory Data Analysis in Python</strong><br/>
  <em>Automatically generate EDA reports with smart suggestions, visualizations, and actionable insights</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/autoview/"><img alt="PyPI" src="https://img.shields.io/pypi/v/autoview?color=blue"></a>
  <a href="https://github.com/avinash-betha/autoview/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/yourusername/autoview.svg?color=green"></a>
  <a href="https://github.com/avinash-betha/autoview/actions"><img alt="CI" src="https://github.com/avinash-betha/autoview/workflows/Test/badge.svg"></a>
</p>

# AutoView - Exploratory Data Analysis Assistant

AutoView is a powerful Python package designed to accelerate your Exploratory Data Analysis (EDA) workflow. It automatically generates insightful visualizations, statistical summaries, feature suggestions, and a full HTML report to help you understand your dataset deeply before modeling.

---

## 🚀 Features

### 📊 Dataset Summary

- Dataset shape (rows × columns)
- Column data types
- Unique value count per column
- Descriptive statistics for numeric columns
- Detection of duplicate rows

### 🧠 Smart Insights

- Skewed features with transformation suggestions
- Top highly correlated feature pairs (Pearson > 0.35)
- Feature importance using Random Forest
- Target imbalance detection
- Text column profiling (length, mode, uniqueness)
- Column role classification (ID, datetime, name, high cardinality, etc.)

### 📈 Visualizations

- **Histograms** for all numeric features
- **Boxplots** (outlier detection using IQR)
- **Correlation heatmap** for numeric features
- **Missing data visualization** using `missingno`:
  - Matrix plot
  - Bar plot
  - Heatmap
  - Dendrogram
- **Target distribution** bar chart (if specified)
- **Feature importance** horizontal bar chart

### 📋 Suggested Actions

- Encode categorical features
- Handle skewed or correlated features
- Remove ID or low variance columns
- Drop or impute missing values

### 📄 Auto-Generated HTML Report

- Clean, professional UI with embedded plots
- Sectioned layout: Data types, stats, roles, visuals, insights
- No external image files needed (all plots are embedded using base64)

---

## 📦 Installation

```bash
pip install autoview  # (Coming Soon to PyPI)
```

Or clone locally:

```bash
git clone https://github.com/avinash-betha/autoview.git
cd autoview
pip install -r requirements.txt
```

---

## 🧪 Example Usage

```python
from autoview import explore
import pandas as pd

# Load any dataset
df = pd.read_csv("your_dataset.csv")

# Explore the dataset
df_summary = explore(df, target="target_column", plots=True, show_missing=True)
```

---

## ⚙️ Function Parameters

```python
explore(df: pd.DataFrame, plots=False, target=None, show_missing=True)
```

### Parameters:

| Parameter      | Type       | Description                                                               |
| -------------- | ---------- | ------------------------------------------------------------------------- |
| `df`           | DataFrame  | The dataset to analyze.                                                   |
| `plots`        | bool       | If `True`, shows visualizations like histograms, boxplots, heatmaps, etc. |
| `target`       | str / None | Optional target column name for classification/regression analysis.       |
| `show_missing` | bool       | If `True`, shows missing data visualizations using `missingno`.           |

---

## 📁 Project Structure

```
autoview/
├── explore.py          # Main entry point for the EDA pipeline
├── visualize.py        # Plotting logic for histograms, boxplots, etc.
├── report.py           # HTML report generation with embedded charts
├── examples/
│   └── titanic_demo.py
└── README.md
```

---

## 📋 Dependencies

- pandas
- numpy
- seaborn
- matplotlib
- scikit-learn
- missingno
- tabulate

---

## 📜 License

MIT License

Copyright (c) 2024 Avinash Betha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🙌 Contributing

We welcome contributions! Please feel free to open issues or submit PRs for:

- Adding more visualizations (e.g., violin plots, KDE plots)
- Improving column role inference
- Integrating data preprocessing suggestions

---

## 💡 Inspiration

AutoView aims to eliminate the tedious setup of basic EDA steps, freeing analysts and data scientists to focus on deeper insights and modeling.

If you're looking to plug EDA into your workflow with minimal effort and maximum insights, **AutoView is your go-to!**
