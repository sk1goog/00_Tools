import re
import pyperclip

# Converts lowercase 'b' notation (e.g. Lb) to HTM standard (e.g. L')
def convert_to_htm(notation):
    return notation.replace('b', "'")

# Simplifies sequences by combining repeated moves into HTM-style notation
def simplify_moves(moves):
    simplified = []
    i = 0
    changes_log = []

    while i < len(moves):
        current = moves[i]
        count = 1
        # Count how many times the same move appears consecutively
        while i + count < len(moves) and moves[i + count] == current:
            count += 1

        original_group = " ".join([current] * count)

        # Reduction rules
        if count >= 4:
            remainder = count % 4
            reduced = ""
            if remainder == 1:
                reduced = current
                simplified.append(current)
            elif remainder == 2:
                reduced = current[0] + '2'
                simplified.append(reduced)
            elif remainder == 3:
                reduced = current[0] if "'" in current else current[0] + "'"
                simplified.append(reduced)
            if remainder:
                changes_log.append(f"{original_group} → {reduced} (after 4-move reduction)")
            else:
                changes_log.append(f"{original_group} → deleted")
        elif count == 3:
            reduced = current[0] if "'" in current else current[0] + "'"
            simplified.append(reduced)
            changes_log.append(f"{original_group} → {reduced}")
        elif count == 2:
            reduced = current[0] + "2"
            simplified.append(reduced)
            changes_log.append(f"{original_group} → {reduced}")
        else:
            simplified.append(current)
        i += count

    return simplified, changes_log

def main():
    print("🔄 Reading move sequence from clipboard …")
    raw_input = pyperclip.paste().strip()
    raw_moves = raw_input.split()

    # Convert all moves to HTM format
    converted_moves = [convert_to_htm(move) for move in raw_moves]

    # Apply simplification rules
    simplified_moves, logs = simplify_moves(converted_moves)

    # Display original converted sequence
    print("\n📥 Original sequence (HTM converted):")
    print(" ".join(converted_moves))

    # Display all reductions and transformations
    print("\n📋 Applied transformations:")
    for log in logs:
        print(" -", log)

    # Statistics
    print(f"\n🔢 Number of moves before: {len(converted_moves)}")
    print(f"🔢 Number of moves after: {len(simplified_moves)}")

    # Final output
    print("\n✅ Final transformed sequence:")
    print(" ".join(simplified_moves))

if __name__ == "__main__":
    main()