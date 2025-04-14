import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os
import statistics

# Converts lowercase 'b' notation (e.g. Lb) to standard HTM notation (L')
def convert_to_htm(notation):
    return notation.replace('b', "'")

# Simplifies a list of moves according to HTM reduction rules
def simplify_moves(moves):
    simplified = []
    i = 0
    while i < len(moves):
        current = moves[i]
        count = 1
        while i + count < len(moves) and moves[i + count] == current:
            count += 1

        if count >= 4:
            remainder = count % 4
            if remainder == 1:
                simplified.append(current)
            elif remainder == 2:
                simplified.append(current[0] + '2')
            elif remainder == 3:
                simplified.append(current[0] if "'" in current else current[0] + "'")
            # multiples of 4 are discarded
        elif count == 3:
            simplified.append(current[0] if "'" in current else current[0] + "'")
        elif count == 2:
            simplified.append(current[0] + "2")
        else:
            simplified.append(current)
        i += count

    return simplified

# Transforms a single sequence: converts to HTM and simplifies
def transform_sequence(seq):
    original_moves = seq.strip().split()
    converted_moves = [convert_to_htm(m) for m in original_moves]
    simplified = simplify_moves(converted_moves)
    return len(original_moves), " ".join(simplified), len(simplified)

def main():
    # File selection dialog
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select CSV file with move sequences",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        print("❌ No file selected.")
        return

    # Read and filter data
    df = pd.read_csv(file_path, sep=';')
    df_filtered = df[df["Total Correct Pieces"] == 20]

    results = []

    for _, row in df_filtered.iterrows():
        raw_sequence = str(row["Total Move Sequence"])
        len_original, simplified_seq, len_simplified = transform_sequence(raw_sequence)

        results.append({
            "Original Sequence": raw_sequence,
            "Original Length": len_original,
            "Transformed Sequence": simplified_seq,
            "Transformed Length": len_simplified
        })

    result_df = pd.DataFrame(results)

    # Create output file paths
    base_dir = os.path.dirname(file_path)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    transformed_csv = os.path.join(base_dir, f"{base_name}_htm_transformed.csv")
    stats_csv = os.path.join(base_dir, f"{base_name}_htm_stats.csv")

    # Save transformed data
    result_df.to_csv(transformed_csv, sep=';', index=False)

    # Compute statistics for transformed lengths
    trans_lengths = result_df["Transformed Length"]

    stats_data = {
        "Statistic": [
            "Min",
            "Max",
            "Average",
            "Median",
            "Standard Deviation",
            "Variance"
        ],
        "Value": [
            min(trans_lengths),
            max(trans_lengths),
            round(statistics.mean(trans_lengths), 2),
            statistics.median(trans_lengths),
            round(statistics.stdev(trans_lengths), 2),
            round(statistics.variance(trans_lengths), 2)
        ]
    }

    stats_df = pd.DataFrame(stats_data)
    stats_df.to_csv(stats_csv, sep=';', index=False)

    # Console output
    print("\n📊 Statistics for transformed move sequences:")
    for stat, value in zip(stats_data["Statistic"], stats_data["Value"]):
        print(f"{stat}: {value}")

    print(f"\n🔢 Number of transformed rows: {len(result_df)}")
    print(f"✅ Transformed data saved to: {transformed_csv}")
    print(f"✅ Statistics saved to: {stats_csv}")

if __name__ == "__main__":
    main()