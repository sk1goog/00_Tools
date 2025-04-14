import re
import pyperclip

def convert_to_htm(notation):
    """
    Converts lowercase 'b' notation (e.g. Lb) to HTM standard (e.g. L')
    """
    return notation.replace('b', "'")

def simplify_moves(moves):
    """
    Simplifies a sequence of moves by combining repeated consecutive moves
    using modulo-4 reduction, assuming the moves are already in HTM notation.
    
    Rules:
      - 1 move remains unchanged.
      - 2 moves become a 180° turn (e.g. F F → F2).
      - 3 moves become the inverse (e.g. F F F → F', and F' F' F' → F).
      - 4 moves cancel (deleted).
    """
    simplified = []
    i = 0
    changes_log = []
    
    while i < len(moves):
        current = moves[i]
        # Extract the base letter and check whether the move is inverse.
        base = current[0]
        is_prime = ("'" in current)
        
        count = 1
        # Count how many times the same move appears consecutively
        while i + count < len(moves) and moves[i + count] == current:
            count += 1
        
        original_group = " ".join([current] * count)
        
        # Use modulo-4 reduction on the count
        if count >= 4:
            remainder = count % 4
            if remainder == 0:
                reduced = None  # moves cancel out
                changes_log.append(f"{original_group} → deleted")
            elif remainder == 1:
                reduced = base + ("'" if is_prime else "")
                simplified.append(reduced)
                changes_log.append(f"{original_group} → {reduced} (after 4-move reduction)")
            elif remainder == 2:
                # Two moves always yield a 180° turn regardless of prime
                reduced = base + "2"
                simplified.append(reduced)
                changes_log.append(f"{original_group} → {reduced} (after 4-move reduction)")
            elif remainder == 3:
                # Three moves: if the move was forward, result is inverse; if it was inverse, result is forward.
                reduced = base + ("" if is_prime else "'")
                simplified.append(reduced)
                changes_log.append(f"{original_group} → {reduced} (after 4-move reduction)")
        elif count == 3:
            # For 3 moves (not part of a 4-move block)
            reduced = base + ("" if is_prime else "'")
            simplified.append(reduced)
            changes_log.append(f"{original_group} → {reduced}")
        elif count == 2:
            reduced = base + "2"
            simplified.append(reduced)
            changes_log.append(f"{original_group} → {reduced}")
        else:
            simplified.append(current)
        i += count

    return simplified, changes_log

def main():
    print("🔄 Reading move sequence from clipboard …")
    # Read the original input (old notation) from the clipboard
    raw_input_text = pyperclip.paste().strip()
    raw_moves = raw_input_text.split()

    # Output original sequence (old notation) and count
    print("\n📥 Original sequence (old notation):")
    print(" ".join(raw_moves))
    print(f"🔢 Number of moves (old notation): {len(raw_moves)}")
    
    # Convert all moves to HTM format using the conversion function.
    # (This step is maintained if your old notation uses 'b' instead of "'" )
    converted_moves = [convert_to_htm(move) for move in raw_moves]
    
    # Output converted sequence (HTM converted) and count
    print("\n📥 Converted sequence (HTM converted):")
    print(" ".join(converted_moves))
    print(f"🔢 Number of moves (HTM converted): {len(converted_moves)}")
    
    # Apply simplification rules to get the final transformed sequence
    simplified_moves, logs = simplify_moves(converted_moves)
    
    # Display all applied transformations (reductions)
    print("\n📋 Applied transformations:")
    for log in logs:
        print(" -", log)
    
    # Output final transformed sequence and count
    print("\n✅ Final transformed sequence (HTM notation):")
    print(" ".join(simplified_moves))
    print(f"🔢 Number of moves (final HTM notation): {len(simplified_moves)}")

if __name__ == "__main__":
    main()