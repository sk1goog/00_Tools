#!/usr/bin/env python3
import json, csv, os, time, random
import numpy as np

def load_cube():
    """
    Load the initial cube configuration from a CSV file.
    
    The CSV file "csv_export-StartPos.csv" is expected to be in the same directory as this script.
    It must contain at least two rows (e.g., a header and one data row).
    The second row should contain exactly 54 entries (one for each facelet of the cube).
    The loaded list is converted to a NumPy array for further processing.
    """
    # Build the absolute file path to the CSV file
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv_export-StartPos.csv")
    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        rows = list(reader)
    
    # Ensure that the CSV file has at least two rows (header and one data row)
    if len(rows) < 2:
        raise ValueError("CSV file must contain at least two rows.")
    
    # The second row represents the cube configuration
    cube_list = rows[1]
    
    # Validate that the cube configuration has exactly 54 elements (one per facelet)
    if len(cube_list) != 54:
        raise ValueError("Cube must have 54 colors")
    
    # Convert the cube list into a NumPy array for efficient manipulation
    cube = np.array(cube_list)
    return cube

def load_mappings():
    """
    Load the move mappings from a JSON file.
    
    The JSON file "mappings.json" should define how each move permutes the cube's facelets.
    """
    with open("mappings.json", "r", encoding="utf-8") as f:
        return json.load(f)

def precompute_permutations(mappings):
    """
    Precompute permutation vectors for each move defined in the mappings.
    
    For each move, a permutation vector (as a NumPy array) of length 54 is computed.
    This vector defines the new cube state such that for each position i:
      new_cube[i] = cube[perm[i]]
    Note: The positions in the JSON mappings are 1-indexed. They are converted to 0-indexed values here.
    """
    perms = {}
    for move, mapping_for_move in mappings.items():
        # Start with an identity permutation (i.e., no change)
        perm = np.arange(54)
        # Update the permutation vector based on the mapping provided for this move
        for src, tgt in mapping_for_move.items():
            tgt_index = int(tgt) - 1  # Convert to 0-indexed
            src_index = int(src) - 1  # Convert to 0-indexed
            perm[tgt_index] = src_index
        perms[move] = perm
    return perms

def apply_move(cube, move, perms):
    """
    Apply a single move to the cube.
    
    If the move is defined in the permutation dictionary (perms),
    the cube's state is rearranged according to the corresponding permutation vector.
    If the move is not defined, the cube remains unchanged.
    """
    perm = perms.get(move)
    if perm is None:
        return cube  # No change if the move is not defined
    return cube[perm]

def apply_moves(cube, moves, perms):
    """
    Apply a sequence of moves to the cube.
    
    Each move in the moves list is applied consecutively, updating the cube's state.
    """
    for move in moves:
        cube = apply_move(cube, move, perms)
    return cube

def cube_to_string(cube_state):
    """
    Convert the cube state into a formatted multiline string for display.
    
    The function arranges the 54 facelets in a layout that reflects the cube's structure.
    """
    def col(pos):
        # Convert the 1-indexed position into the corresponding element in the cube state array
        return cube_state[pos - 1]
    
    # Define the layout lines for the cube's visual representation
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
    """
    Main function to run the cube manipulation program.
    
    The user is prompted to input:
      - The number of moves per sequence.
      - The number of iterations (sequences) per run.
      - The number of runs.
    
    The program then:
      1. Loads the initial cube configuration and move mappings.
      2. Precomputes permutation vectors for each move.
      3. Displays the starting cube state.
      4. Applies random move sequences for each run while measuring the runtime.
      5. Displays the final cube state after all moves have been applied.
    """
    # Prompt the user for configuration parameters
    num_moves_per_sequence = int(input("Enter the number of moves per sequence: "))
    num_iterations = int(input("Enter the number of iterations (sequences) per run: "))
    num_runs = int(input("Enter the number of runs: "))
    
    # Load the starting cube position and move mappings from files
    cube = load_cube()
    mappings = load_mappings()
    # Precompute all permutation vectors for each move for efficiency
    perms = precompute_permutations(mappings)
    
    # Display the initial cube position in a formatted manner
    print("----- Cube Starting Position -----")
    print(cube_to_string(cube))
    
    # Get the list of available moves from the precomputed permutations
    available_moves = list(perms.keys())
    
    # Process the move sequences over the specified number of runs
    for run in range(1, num_runs + 1):
        # Record the start time of this run
        start_time = time.time()
        for _ in range(num_iterations):
            # Generate a random sequence of moves from the available moves
            moves = [random.choice(available_moves) for _ in range(num_moves_per_sequence)]
            # Apply the sequence of moves to update the cube's state
            cube = apply_moves(cube, moves, perms)
        # Calculate the time taken for this run
        end_time = time.time()
        runtime = end_time - start_time
        formatted_runtime = time.strftime('%H:%M:%S', time.gmtime(runtime))
        print(f"\n----- Run {run}: Runtime {formatted_runtime} -----")
    
    # Display the final cube position after all move sequences have been applied
    print("\n----- Final Cube Position -----")
    print(cube_to_string(cube))

if __name__ == '__main__':
    main()