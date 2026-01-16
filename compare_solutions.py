"""
Script to compare solver output with known solutions.
Supports both Unicorn Puzzle (3x3) and Ultimate Puzzle (4x4).
"""

def extract_solutions(file_path, grid_size=None):
    """Extract solution grids from a file.
    
    Args:
        file_path: Path to the solutions file
        grid_size: Size of the grid (3 or 4). If None, will be detected from separator length.
    
    Returns:
        List of solutions, where each solution is a list of grid rows
    """
    solutions = []
    current_solution = []
    current_row_cards = []  # Will hold 3 lines (top, middle, bottom) for one grid row
    prev_was_separator = False
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Solution"):
                # Start of a new solution
                if current_solution:
                    solutions.append(current_solution)
                    current_solution = []
                current_row_cards = []
                prev_was_separator = False
            elif line.startswith("-"):
                # This is a separator line - determine grid size from its length if not provided
                if grid_size is None:
                    # separator length = grid_size * 8 + grid_size + 1
                    # For 3x3: 3*8+3+1 = 28, for 4x4: 4*8+4+1 = 37
                    # Some files use 39 dashes for 4x4
                    sep_len = len(line)
                    if sep_len == 28:
                        grid_size = 3
                    elif sep_len in [37, 39]:
                        grid_size = 4
                    else:
                        # Try to infer from number of cards in a row
                        grid_size = 3  # default
                
                # If we have a complete grid row, add it to the solution
                if current_row_cards and len(current_row_cards) == 3:
                    current_solution.append(current_row_cards)
                    current_row_cards = []
                
                # If we see two separators in a row (or separator after completing a solution), 
                # it might indicate a new solution
                if prev_was_separator and current_solution:
                    # Double separator - save current solution and start new one
                    solutions.append(current_solution)
                    current_solution = []
                    current_row_cards = []
                
                prev_was_separator = True
            elif line.startswith("|") and "|" in line:
                # Extract card data from line like: |   PT   |   PT   |   YH   |
                parts = [p.strip() for p in line.split("|") if p.strip()]
                current_row_cards.append(parts)
                prev_was_separator = False
    
    # Don't forget the last solution
    if current_row_cards and len(current_row_cards) == 3:
        current_solution.append(current_row_cards)
    if current_solution:
        solutions.append(current_solution)
    
    return solutions

def normalize_solution(solution):
    """Normalize a solution for comparison."""
    # solution is a list of 3 grid rows
    # each grid row is a list of 3 lines (top edges, middle edges, bottom edges)
    # each line is a list of 3 edge strings
    normalized_rows = []
    for grid_row in solution:
        # grid_row is [top_edges, middle_edges, bottom_edges]
        # Each is a list like ['PT', 'PT', 'YH']
        row_str = "|".join([f"{top}|{mid}|{bot}" for top, mid, bot in zip(grid_row[0], grid_row[1], grid_row[2])])
        normalized_rows.append(row_str)
    return "\n".join(normalized_rows)

def compare_solutions(known_file, output_file, puzzle_type="unicorn"):
    """Compare known solutions with solver output.
    
    Args:
        known_file: Path to file with known solutions
        output_file: Path to file with solver output
        puzzle_type: "unicorn" for 3x3 or "ultimate" for 4x4
    """
    grid_size = 3 if puzzle_type.lower() == "unicorn" else 4
    puzzle_name = "Unicorn Puzzle" if puzzle_type.lower() == "unicorn" else "Ultimate Puzzle"
    
    print(f"Comparing solutions for {puzzle_name} ({grid_size}x{grid_size})...")
    print("\nReading known solutions...")
    known_solutions = extract_solutions(known_file, grid_size)
    print(f"Found {len(known_solutions)} known solutions")
    
    print("\nReading solver output...")
    output_solutions = extract_solutions(output_file, grid_size)
    print(f"Found {len(output_solutions)} solutions from solver")
    
    # Normalize all solutions for comparison
    known_normalized = [normalize_solution(sol) for sol in known_solutions]
    output_normalized = [normalize_solution(sol) for sol in output_solutions]
    
    print("\n" + "="*60)
    print("COMPARISON RESULTS")
    print("="*60)
    
    if len(known_solutions) != len(output_solutions):
        print(f"⚠️  WARNING: Different number of solutions!")
        print(f"   Known: {len(known_solutions)}, Found: {len(output_solutions)}")
    
    # Check if all known solutions are in output
    print("\nChecking if all known solutions are found...")
    missing = []
    for i, known in enumerate(known_normalized, 1):
        if known in output_normalized:
            print(f"✓ Solution {i}: Found")
        else:
            print(f"✗ Solution {i}: MISSING")
            missing.append(i)
    
    # Check if there are any extra solutions
    print("\nChecking for extra solutions...")
    extra = []
    for i, output in enumerate(output_normalized, 1):
        if output not in known_normalized:
            print(f"⚠ Solution {i}: Extra solution not in known set")
            extra.append(i)
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    if not missing and not extra:
        print("✅ SUCCESS: All solutions match perfectly!")
        print(f"   Found all {len(known_solutions)} known solutions")
        print(f"   No extra solutions")
    else:
        if missing:
            print(f"❌ Missing {len(missing)} known solution(s): {missing}")
        if extra:
            print(f"⚠️  Found {len(extra)} extra solution(s): {extra}")
    
    return len(missing) == 0 and len(extra) == 0

if __name__ == "__main__":
    import sys
    
    puzzle_type = sys.argv[1] if len(sys.argv) > 1 else "unicorn"
    
    if puzzle_type.lower() == "unicorn":
        known_file = "/Users/leanderquiring/Documents/GitHub/edge_matching_puzzle/unicorn solutions.txt"
        output_file = "/Users/leanderquiring/Documents/GitHub/edge-matching-solver/unicorn_solutions.txt"
    elif puzzle_type.lower() == "ultimate":
        known_file = "/Users/leanderquiring/Documents/GitHub/edge_matching_puzzle/ultimate puzzle solutions log.txt"
        output_file = "/Users/leanderquiring/Documents/GitHub/edge-matching-solver/ultimate_solutions.txt"
    else:
        print(f"Unknown puzzle type: {puzzle_type}. Use 'unicorn' or 'ultimate'")
        sys.exit(1)
    
    compare_solutions(known_file, output_file, puzzle_type)
