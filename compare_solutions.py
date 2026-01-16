"""
Script to compare solver output with known solutions.
"""

def extract_solutions(file_path):
    """Extract solution grids from a file."""
    solutions = []
    current_solution = []
    current_row_cards = []  # Will hold 3 lines (top, middle, bottom) for one grid row
    line_count = 0
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("Solution"):
                if current_solution:
                    solutions.append(current_solution)
                    current_solution = []
                current_row_cards = []
                line_count = 0
            elif line.startswith("----------------------------"):
                if current_row_cards and len(current_row_cards) == 3:
                    # We've collected a complete grid row (3 lines)
                    current_solution.append(current_row_cards)
                    current_row_cards = []
                    line_count = 0
            elif line.startswith("|") and "|" in line:
                # Extract card data from line like: |   PT   |   PT   |   YH   |
                parts = [p.strip() for p in line.split("|") if p.strip()]
                current_row_cards.append(parts)
                line_count += 1
    
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

def compare_solutions(known_file, output_file):
    """Compare known solutions with solver output."""
    print("Reading known solutions...")
    known_solutions = extract_solutions(known_file)
    print(f"Found {len(known_solutions)} known solutions")
    
    print("\nReading solver output...")
    output_solutions = extract_solutions(output_file)
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
    known_file = "/Users/leanderquiring/Documents/GitHub/edge_matching_puzzle/unicorn solutions.txt"
    output_file = "/Users/leanderquiring/Documents/GitHub/edge-matching-solver/output.txt"
    
    compare_solutions(known_file, output_file)
