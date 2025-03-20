#!/usr/bin/env python3
import json, csv, os, time, random
import numpy as np

def load_cube():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv_export-StartPos.csv")
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        rows = list(reader)
    if len(rows) < 2:
        raise ValueError("CSV file must contain at least two rows.")
    cube_list = rows[1]
    if len(cube_list) != 54:
        raise ValueError("Cube must have 54 colors")
    # Convert the list to a NumPy array
    cube = np.array(cube_list)
    return cube

def load_mappings():
    with open("mappings.json", "r", encoding="utf-8") as f:
        return json.load(f)

def precompute_permutations(mappings):
    """
    For each move, compute a permutation vector (as a NumPy array) of length 54,
    so that for each position i: new_cube[i] = cube[perm[i]].
    Position indices in the mappings are 1-indexed; here they are converted to 0-indexed values.
    """
    perms = {}
    for move, mapping_for_move in mappings.items():
        # Default: identity permutation
        perm = np.arange(54)
        for src, tgt in mapping_for_move.items():
            tgt_index = int(tgt) - 1
            src_index = int(src) - 1
            perm[tgt_index] = src_index
        perms[move] = perm
    return perms

def apply_move(cube, move, perms):
    perm = perms.get(move)
    if perm is None:
        return cube  # If the move is not defined, make no change
    return cube[perm]

def apply_moves(cube, moves, perms):
    for move in moves:
        cube = apply_move(cube, move, perms)
    return cube

def cube_to_string(cube_state):
    # This function formats the cube state in a multiline layout.
    def col(pos):
        return cube_state[pos - 1]
    lines = [
        f"        {col(19)} {col(20)} {col(21)}",
        f"        {col(22)} {col(23)} {col(24)}",
        f"        {col(25)} {col(26)} {col(27)}",
        f"{col(10)} {col(11)} {col(12)} | {col(1)} {col(2)} {col(3)} | {col(28)} {col(29)} {col(30)}",
        f"{col(13)} {col(14)} {col(15)} | {col(4)} {col(5)} {col(6)} | {col(31)} {col(32)} {col(33)}",
        f"{col(16)} {col(17)} {col(18)} | {col(7)} {col(8)} {col(9)} | {col(34)} {col(35)} {col(36)}",
        f"        {col(37)} {col(38)} {col(39)}",
        f"        {col(40)} {col(41)} {col(42)}",
        f"        {col(43)} {col(44)} {col(45)}",
        f"        {col(46)} {col(47)} {col(48)}",
        f"        {col(49)} {col(50)} {col(51)}",
        f"        {col(52)} {col(53)} {col(54)}"
    ]
    return "\n".join(lines)

def main():
    # Parameter input
    num_moves_per_sequence = int(input("Enter the number of moves per sequence: "))
    num_iterations = int(input("Enter the number of iterations (sequences) per run: "))
    num_runs = int(input("Enter the number of runs: "))
    
    # Reading the starting position and move mappings
    cube = load_cube()
    mappings = load_mappings()
    # Precompute all permutation vectors
    perms = precompute_permutations(mappings)
    
    # Display the starting cube position
    print("----- Cube Starting Position -----")
    print(cube_to_string(cube))
    
    available_moves = list(perms.keys())
    
    # Applying the move sequences
    for run in range(1, num_runs + 1):
        start_time = time.time()
        for _ in range(num_iterations):
            # Generating a random sequence of moves
            moves = [random.choice(available_moves) for _ in range(num_moves_per_sequence)]
            cube = apply_moves(cube, moves, perms)
        end_time = time.time()
        runtime = end_time - start_time
        formatted_runtime = time.strftime('%H:%M:%S', time.gmtime(runtime))
        print(f"\n----- Run {run}: Runtime {formatted_runtime} -----")
    
    # Display the final cube position
    print("\n----- Final Cube Position -----")
    print(cube_to_string(cube))

if __name__ == '__main__':
    main()