import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from tkinter import filedialog
import os

def main():
    # File selection
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select statistics CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    if not file_path:
        print("❌ No file selected.")
        return

    # Read and prepare data
    df = pd.read_csv(file_path, sep=';')
    numeric_cols = ['Min', 'Max', 'Average', 'Median', 'Standard Deviation', 'Variance']
    for col in numeric_cols:
        df[col] = df[col].astype(str).str.replace(',', '.').astype(float)

    df_long = pd.melt(df, id_vars=['Statistic'], value_vars=numeric_cols,
                      var_name='Measure', value_name='Value')
    df_long.rename(columns={'Statistic': 'Script/Date'}, inplace=True)

    # Plot
    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_long, x='Script/Date', y='Value', hue='Measure', marker='o')
    plt.title("Statistical Measures over Time")
    plt.xlabel("Script Version / Date")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Save to file
    plot_path = os.path.join(os.path.dirname(file_path), "statistics_plot.png")
    plt.savefig(plot_path, dpi=300)
    print(f"✅ Plot saved as image: {plot_path}")

if __name__ == "__main__":
    main()