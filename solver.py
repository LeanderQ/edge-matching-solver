"""
Edge Matching Puzzle Solver

This script finds all valid solutions for arranging 9 unicorn cards in a 3x3 grid
where adjacent edges must match (same color and opposite unicorn parts: H-T or T-H).
"""

from typing import List, Tuple, Optional
from itertools import permutations

# The set of 9 unicorn cards
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
    - Parts must be opposite (H-T or T-H)
    
    Args:
        edge1: First edge [color, part]
        edge2: Second edge [color, part]
    
    Returns:
        True if edges match, False otherwise
    """
    if edge1[0] != edge2[0]:  # Colors don't match
        return False
    
    if edge1[1] == edge2[1]:  # Parts are the same (both H or both T)
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
                       row: int, col: int, card: List[List[str]]) -> bool:
    """
    Check if placing a card at position (row, col) is valid.
    
    A placement is valid if:
    - The card's top edge matches the card above (if exists)
    - The card's right edge matches the card to the right (if exists)
    - The card's bottom edge matches the card below (if exists)
    - The card's left edge matches the card to the left (if exists)
    
    Args:
        grid: 3x3 grid of cards (None for empty positions)
        row: Row index (0-2)
        col: Column index (0-2)
        card: The card to place
    
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
    if col < 2 and grid[row][col+1] is not None:
        right_edge = get_edge(card, 'right')
        left_edge_right = get_edge(grid[row][col+1], 'left')
        if not edges_match(right_edge, left_edge_right):
            return False
    
    # Check bottom edge (must match card below)
    if row < 2 and grid[row+1][col] is not None:
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


def solve_puzzle() -> List[List[List[List[List[str]]]]]:
    """
    Find all valid solutions for the 3x3 edge matching puzzle.
    
    Uses backtracking to try all permutations of cards and rotations.
    
    Returns:
        List of all valid solutions, where each solution is a 3x3 grid of cards
    """
    solutions = []
    grid = [[None for _ in range(3)] for _ in range(3)]
    
    def backtrack(card_index: int, used_cards: set):
        """
        Backtracking function to find valid placements.
        
        Args:
            card_index: Current position in the grid (0-8, row-major order)
            used_cards: Set of card indices already used
        """
        if card_index == 9:
            # All positions filled - found a solution
            # Deep copy the solution
            solution = [[card.copy() for card in row] for row in grid]
            solutions.append(solution)
            return
        
        row = card_index // 3
        col = card_index % 3
        
        # Try each unused card
        for card_idx in range(9):
            if card_idx in used_cards:
                continue
            
            # Try each rotation of the card
            for rotation in range(4):
                rotated_card = rotate_card(unicorn_cardset[card_idx], rotation)
                
                # Check if this placement is valid
                if is_valid_placement(grid, row, col, rotated_card):
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
        solution: A 3x3 grid of cards
    """
    # Calculate separator line length (3 cards * 8 chars per card + 4 separators)
    separator = "-" * 28
    
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


def main():
    """
    Main function to solve the puzzle and display results.
    """
    print("Solving edge matching puzzle...")
    print(f"Total cards: {len(unicorn_cardset)}")
    print("Grid size: 3x3")
    print("\nSearching for all valid solutions...")
    
    solutions = solve_puzzle()
    
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
    main()
