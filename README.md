# Edge Matching Puzzle Solver

A Python solver for edge matching puzzles that finds all valid solutions for arranging puzzle cards in a grid where adjacent edges must match.

## Supported Puzzles

### Unicorn Puzzle (3×3)
- **Grid Size**: 3×3 (9 cards)
- **Colors**: Pink (P), Green (G), Red (R), Yellow (Y)
- **Matching**: Head (H) must match Tail (T) on adjacent edges
- **Solutions**: 8 unique solutions

### Ultimate Puzzle (4×4)
- **Grid Size**: 4×4 (16 cards)
- **Colors**: Cyan (C), Amber (A), Blue (B), Purple (P)
- **Matching**: In (I) must match Out (O) on adjacent edges
- **Solutions**: 48 unique solutions

## Features

- **Backtracking Algorithm**: Efficiently explores all possible card arrangements and rotations
- **Rotation Support**: Each card can be rotated 0°, 90°, 180°, or 270°
- **Edge Matching**: Validates that adjacent edges have matching colors and opposite parts
- **Solution Verification**: Compare solver output against known solutions
- **Flexible Design**: Supports both 3×3 and 4×4 grids with different cardsets

## Installation

No external dependencies required. Uses only Python standard library.

```bash
# Clone the repository
git clone https://github.com/LeanderQ/edge-matching-solver.git
cd edge-matching-solver
```

## Usage

### Solving Puzzles

Run the solver for either puzzle type:

```bash
# Solve the Unicorn Puzzle (3×3)
python3 solver.py unicorn

# Solve the Ultimate Puzzle (4×4)
python3 solver.py ultimate
```

The solver will display all valid solutions in a formatted grid layout.

### Saving Solutions to File

```bash
# Save Unicorn Puzzle solutions
python3 solver.py unicorn > unicorn_solutions.txt

# Save Ultimate Puzzle solutions
python3 solver.py ultimate > ultimate_solutions.txt
```

### Verifying Solutions

Compare your solver output against known solutions:

```bash
# Verify Unicorn Puzzle solutions
python3 compare_solutions.py unicorn

# Verify Ultimate Puzzle solutions
python3 compare_solutions.py ultimate
```

The comparison script will:
- Check if all known solutions are found
- Identify any missing solutions
- Report any extra solutions not in the known set

## Output Format

Solutions are displayed in a grid format with box borders:

```
----------------------------
|   PT   |   PT   |   YH   |
| YH  GT | GH  RT | RH  PT |
|   RH   |   YH   |   YT   |
----------------------------
|   RT   |   YT   |   YH   |
| GH  GT | GH  PT | PH  RT |
|   PH   |   YH   |   GT   |
----------------------------
|   PT   |   YT   |   GH   |
| RT  RH | RT  PH | PT  YH |
|   GH   |   GH   |   YT   |
----------------------------
```

Each card shows:
- **Top edge** (top row)
- **Left and right edges** (middle row)
- **Bottom edge** (bottom row)

## How It Works

1. **Card Representation**: Each card is represented as `[top, right, bottom, left]` where each edge is `[color, part]`

2. **Edge Matching**: Two edges match if:
   - Colors are identical
   - Parts are opposite (H↔T or I↔O)

3. **Backtracking Algorithm**:
   - Places cards one at a time in row-major order
   - For each position, tries all unused cards in all 4 rotations
   - Validates placement by checking adjacent edges
   - Backtracks when no valid placement is possible
   - Records complete solutions when all positions are filled

4. **Optimization**: The algorithm prunes invalid branches early by checking edge compatibility before placing cards

## File Structure

```
edge-matching-solver/
├── solver.py                 # Main solver implementation
├── compare_solutions.py       # Solution verification script
├── unicorn_solutions.txt      # All 8 Unicorn Puzzle solutions
├── ultimate_solutions.txt     # All 48 Ultimate Puzzle solutions
└── README.md                  # This file
```

## Puzzle Rules

### Edge Matching Rules
- Adjacent edges must have the **same color**
- Adjacent edges must have **opposite parts**:
  - Unicorn Puzzle: Head (H) matches Tail (T)
  - Ultimate Puzzle: In (I) matches Out (O)

### Example
For the Unicorn Puzzle, if a card has a Pink Head (PH) on its right edge, the card to its right must have a Pink Tail (PT) on its left edge.

## Performance

- **Unicorn Puzzle (3×3)**: Solves in < 1 second
- **Ultimate Puzzle (4×4)**: Solves in several minutes (due to larger search space: 16! × 4¹⁶ possible arrangements)

## Verification Results

✅ **Unicorn Puzzle**: All 8 solutions verified against known solutions  
✅ **Ultimate Puzzle**: All 48 solutions verified against known solutions

## License

This project is open source and available for educational and personal use.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
