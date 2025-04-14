import re
import pyperclip

def convert_to_htm(notation):
    """Ersetzt 'b' durch ', z. B. Lb → L'"""
    return notation.replace('b', "'")

def simplify_moves(moves):
    simplified = []
    i = 0
    changes_log = []
    
    while i < len(moves):
        current = moves[i]
        count = 1
        while i + count < len(moves) and moves[i + count] == current:
            count += 1

        original_group = " ".join([current] * count)

        if count >= 4:
            remainder = count % 4
            group = [current] * remainder
            reduced = ""
            if remainder == 1:
                reduced = current
                simplified.append(current)
            elif remainder == 2:
                reduced = current[0] + '2'
                simplified.append(reduced)
            elif remainder == 3:
                if "'" in current:
                    reduced = current[0]
                else:
                    reduced = current[0] + "'"
                simplified.append(reduced)
            if remainder:
                changes_log.append(f"{original_group} → {reduced} (nach 4er-Reduktion)")
            else:
                changes_log.append(f"{original_group} → gelöscht")
        elif count == 3:
            if "'" in current:
                reduced = current[0]
            else:
                reduced = current[0] + "'"
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
    print("🔄 Lese Zugfolge aus Zwischenablage …")
    raw_input = pyperclip.paste().strip()
    raw_moves = raw_input.split()
    converted_moves = [convert_to_htm(move) for move in raw_moves]

    simplified_moves, logs = simplify_moves(converted_moves)

    print("\n📥 Ursprüngliche Zugfolge (HTM konvertiert):")
    print(" ".join(converted_moves))

    print("\n📋 Ersetzungen:")
    for log in logs:
        print(" -", log)

    print(f"\n🔢 Anzahl Züge vorher: {len(converted_moves)}")
    print(f"🔢 Anzahl Züge nachher: {len(simplified_moves)}")

    print("\n✅ Ergebnis-Zugfolge:")
    print(" ".join(simplified_moves))

if __name__ == "__main__":
    main()