"""
Edge Matching Puzzle Solver

This script finds all valid solutions for arranging cards in a grid
where adjacent edges must match (same color and opposite parts: H-T/T-H or I-O/O-I).
Supports both the Unicorn Puzzle (3x3) and Ultimate Puzzle (4x4).
"""

from typing import List, Tuple, Optional
from itertools import permutations

# The set of 9 unicorn cards (Unicorn Puzzle)
# Each card has 4 sides: [top, right, bottom, left]
# Each side is [color, part] where color is P/G/R/Y and part is H/T
unicorn_cardset = [
    [["P","T"], ["G","T"], ["R","H"],["Y","H"]],
    [["P","H"], ["G","H"], ["R","T"],["Y","T"]],
    [["R","T"], ["Y","H"], ["G","H"],["P","T"]],
    [["R","H"], ["Y","H"], ["P","T"],["Y","T"]],
    [["R","T"], ["G","T"], ["P","H"],["Y","H"]],
    [["R","T"], ["P","T"], ["R","H"],["G","H"]],
    [["P","H"], ["G","H"], ["R","T"],["G","T"]],
    [["Y","T"], ["P","T"], ["Y","H"],["G","H"]],
    [["P","T"], ["G","H"], ["Y","H"],["Y","T"]]
]

# The set of 16 ultimate cards (Ultimate Puzzle)
# Each card has 4 sides: [top, right, bottom, left]
# Each side is [color, part] where color is C/A/B/P and part is I/O
ultimate_cardset = [
    [["C","O"], ["C","O"], ["A","I"],["C","I"]],
    [["C","O"], ["A","O"], ["P","I"],["C","I"]],
    [["C","O"], ["A","O"], ["A","I"],["C","I"]],
    [["A","O"], ["B","O"], ["C","I"],["A","I"]],
    [["A","O"], ["P","O"], ["C","I"],["A","I"]],
    [["A","O"], ["A","O"], ["B","I"],["C","I"]],
    [["A","O"], ["P","O"], ["B","I"],["P","I"]],
    [["B","O"], ["C","O"], ["P","I"],["C","I"]],
    [["B","O"], ["C","O"], ["A","I"],["B","I"]],
    [["B","O"], ["C","O"], ["B","I"],["P","I"]],
    [["B","O"], ["B","O"], ["P","I"],["C","I"]],
    [["B","O"], ["B","O"], ["P","I"],["A","I"]],
    [["P","O"], ["C","O"], ["C","I"],["B","I"]],
    [["P","O"], ["C","O"], ["C","I"],["P","I"]],
    [["P","O"], ["C","O"], ["A","I"],["A","I"]],
    [["P","O"], ["B","O"], ["B","I"],["A","I"]]
]


def rotate_card(card: List[List[str]], rotations: int) -> List[List[str]]:
    """
    Rotate a card clockwise by the specified number of 90-degree rotations.
    
    Args:
        card: A card represented as [top, right, bottom, left]
        rotations: Number of clockwise 90-degree rotations (0-3)
    
    Returns:
        The rotated card
    """
    rotations = rotations % 4
    if rotations == 0:
        return card.copy()
    
    # Rotate clockwise: top->right, right->bottom, bottom->left, left->top
    rotated = card.copy()
    for _ in range(rotations):
        rotated = [rotated[3], rotated[0], rotated[1], rotated[2]]
    
    return rotated


def edges_match(edge1: List[str], edge2: List[str]) -> bool:
    """
    Check if two edges match (same color, opposite parts).
    
    For edges to match:
    - Colors must be the same
    - Parts must be opposite (H-T/T-H for Unicorn, I-O/O-I for Ultimate)
    
    Args:
        edge1: First edge [color, part]
        edge2: Second edge [color, part]
    
    Returns:
        True if edges match, False otherwise
    """
    if edge1[0] != edge2[0]:  # Colors don't match
        return False
    
    if edge1[1] == edge2[1]:  # Parts are the same (both H/T or both I/O)
        return False
    
    return True  # Same color, opposite parts


def get_edge(card: List[List[str]], direction: str) -> List[str]:
    """
    Get the edge of a card in a specific direction.
    
    Args:
        card: A card [top, right, bottom, left]
        direction: 'top', 'right', 'bottom', or 'left'
    
    Returns:
        The edge [color, part]
    """
    direction_map = {'top': 0, 'right': 1, 'bottom': 2, 'left': 3}
    return card[direction_map[direction]]


def is_valid_placement(grid: List[List[Optional[List[List[str]]]]], 
                       row: int, col: int, card: List[List[str]], 
                       grid_size: int) -> bool:
    """
    Check if placing a card at position (row, col) is valid.
    
    A placement is valid if:
    - The card's top edge matches the card above (if exists)
    - The card's right edge matches the card to the right (if exists)
    - The card's bottom edge matches the card below (if exists)
    - The card's left edge matches the card to the left (if exists)
    
    Args:
        grid: Grid of cards (None for empty positions)
        row: Row index
        col: Column index
        card: The card to place
        grid_size: Size of the grid (3 for 3x3, 4 for 4x4)
    
    Returns:
        True if placement is valid, False otherwise
    """
    # Check top edge (must match card above)
    if row > 0 and grid[row-1][col] is not None:
        top_edge = get_edge(card, 'top')
        bottom_edge_above = get_edge(grid[row-1][col], 'bottom')
        if not edges_match(top_edge, bottom_edge_above):
            return False
    
    # Check right edge (must match card to the right)
    if col < grid_size - 1 and grid[row][col+1] is not None:
        right_edge = get_edge(card, 'right')
        left_edge_right = get_edge(grid[row][col+1], 'left')
        if not edges_match(right_edge, left_edge_right):
            return False
    
    # Check bottom edge (must match card below)
    if row < grid_size - 1 and grid[row+1][col] is not None:
        bottom_edge = get_edge(card, 'bottom')
        top_edge_below = get_edge(grid[row+1][col], 'top')
        if not edges_match(bottom_edge, top_edge_below):
            return False
    
    # Check left edge (must match card to the left)
    if col > 0 and grid[row][col-1] is not None:
        left_edge = get_edge(card, 'left')
        right_edge_left = get_edge(grid[row][col-1], 'right')
        if not edges_match(left_edge, right_edge_left):
            return False
    
    return True


def solve_puzzle(cardset: List[List[List[str]]], grid_size: int) -> List[List[List[List[List[str]]]]]:
    """
    Find all valid solutions for the edge matching puzzle.
    
    Uses backtracking to try all permutations of cards and rotations.
    
    Args:
        cardset: List of cards to use
        grid_size: Size of the grid (3 for 3x3, 4 for 4x4)
    
    Returns:
        List of all valid solutions, where each solution is a grid of cards
    """
    solutions = []
    grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
    total_positions = grid_size * grid_size
    
    def backtrack(card_index: int, used_cards: set):
        """
        Backtracking function to find valid placements.
        
        Args:
            card_index: Current position in the grid (row-major order)
            used_cards: Set of card indices already used
        """
        if card_index == total_positions:
            # All positions filled - found a solution
            # Deep copy the solution
            solution = [[card.copy() for card in row] for row in grid]
            solutions.append(solution)
            return
        
        row = card_index // grid_size
        col = card_index % grid_size
        
        # Try each unused card
        for card_idx in range(len(cardset)):
            if card_idx in used_cards:
                continue
            
            # Try each rotation of the card
            for rotation in range(4):
                rotated_card = rotate_card(cardset[card_idx], rotation)
                
                # Check if this placement is valid
                if is_valid_placement(grid, row, col, rotated_card, grid_size):
                    # Place the card
                    grid[row][col] = rotated_card
                    used_cards.add(card_idx)
                    
                    # Recurse to next position
                    backtrack(card_index + 1, used_cards)
                    
                    # Backtrack
                    grid[row][col] = None
                    used_cards.remove(card_idx)
    
    backtrack(0, set())
    return solutions


def print_card(card: List[List[str]], indent: str = ""):
    """
    Print a card in a readable format.
    
    Args:
        card: A card [top, right, bottom, left]
        indent: Indentation string
    """
    print(f"{indent}    {card[0][0]}{card[0][1]}")
    print(f"{indent}{card[3][0]}{card[3][1]}    {card[1][0]}{card[1][1]}")
    print(f"{indent}    {card[2][0]}{card[2][1]}")


def print_solution(solution: List[List[List[List[str]]]]):
    """
    Print a solution grid in a readable format with box borders.
    
    Args:
        solution: A grid of cards (3x3 or 4x4)
    """
    grid_size = len(solution)
    # Calculate separator line length (grid_size cards * 8 chars per card + (grid_size + 1) separators)
    separator = "-" * (grid_size * 8 + grid_size + 1)
    
    for row_idx, row in enumerate(solution):
        # Print separator line
        print(separator)
        
        # Print top edges: |   PT   |   PT   |   YH   |
        top_parts = [f"   {card[0][0]}{card[0][1]}   " for card in row]
        print("|" + "|".join(top_parts) + "|")
        
        # Print left and right edges: | YH  GT | GH  RT | RH  PT |
        middle_parts = [f" {card[3][0]}{card[3][1]}  {card[1][0]}{card[1][1]} " for card in row]
        print("|" + "|".join(middle_parts) + "|")
        
        # Print bottom edges: |   RH   |   YH   |   YT   |
        bottom_parts = [f"   {card[2][0]}{card[2][1]}   " for card in row]
        print("|" + "|".join(bottom_parts) + "|")
    
    # Print final separator line
    print(separator)


def main(puzzle_type: str = "unicorn"):
    """
    Main function to solve the puzzle and display results.
    
    Args:
        puzzle_type: "unicorn" for Unicorn Puzzle (3x3) or "ultimate" for Ultimate Puzzle (4x4)
    """
    if puzzle_type.lower() == "unicorn":
        cardset = unicorn_cardset
        grid_size = 3
        puzzle_name = "Unicorn Puzzle"
    elif puzzle_type.lower() == "ultimate":
        cardset = ultimate_cardset
        grid_size = 4
        puzzle_name = "Ultimate Puzzle"
    else:
        raise ValueError(f"Unknown puzzle type: {puzzle_type}. Use 'unicorn' or 'ultimate'")
    
    print(f"Solving {puzzle_name}...")
    print(f"Total cards: {len(cardset)}")
    print(f"Grid size: {grid_size}x{grid_size}")
    print("\nSearching for all valid solutions...")
    
    solutions = solve_puzzle(cardset, grid_size)
    
    print(f"\n{'='*50}")
    print(f"Found {len(solutions)} solution(s)")
    print(f"{'='*50}")
    
    if solutions:
        for idx, solution in enumerate(solutions, 1):
            print(f"\nSolution {idx}:")
            print_solution(solution)
    else:
        print("\nNo solutions found!")


if __name__ == "__main__":
    import sys
    puzzle_type = sys.argv[1] if len(sys.argv) > 1 else "unicorn"
    main(puzzle_type)
