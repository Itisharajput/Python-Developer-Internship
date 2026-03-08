# ============================================================
#   N-QUEENS PROBLEM — Task 3 (Level 3 Advanced)
#   Description: Place N queens on NxN chessboard
#                so no two queens threaten each other
#   Method     : Backtracking Algorithm
# ============================================================

# Colors
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def print_success(msg): print(f"{GREEN}✅ {msg}{RESET}")
def print_error(msg):   print(f"{RED}❌ {msg}{RESET}")
def print_info(msg):    print(f"{YELLOW}ℹ️  {msg}{RESET}")
def print_section(msg): print(f"\n{BLUE}{BOLD}{'═'*52}\n   {msg}\n{'═'*52}{RESET}")


# ============================================================
#   STEP 1 — REPRESENT CHESSBOARD AS 2D ARRAY
# ============================================================

def create_board(n):
    """Create empty NxN chessboard filled with 0s"""
    return [[0] * n for _ in range(n)]


def print_board(board, solution_number=None):
    """Display the chessboard beautifully"""
    n = len(board)

    if solution_number:
        print(f"\n  {CYAN}{BOLD}Solution {solution_number}:{RESET}")

    # Top border
    print("  ┌" + "───┬" * (n - 1) + "───┐")

    for row in range(n):
        line = "  │"
        for col in range(n):
            if board[row][col] == 1:
                line += f" {GREEN}Q{RESET} │"   # Queen
            else:
                # Checkerboard pattern for empty cells
                if (row + col) % 2 == 0:
                    line += f" {YELLOW}·{RESET} │"
                else:
                    line += "   │"
        print(line)

        # Row separator
        if row < n - 1:
            print("  ├" + "───┼" * (n - 1) + "───┤")

    # Bottom border
    print("  └" + "───┴" * (n - 1) + "───┘")

    # Show queen positions
    positions = []
    for row in range(n):
        for col in range(n):
            if board[row][col] == 1:
                positions.append(f"Row {row+1} Col {col+1}")
    print(f"  {YELLOW}Queens at: {', '.join(positions)}{RESET}")


# ============================================================
#   STEP 2 — CHECK IF POSITION IS SAFE
#   A queen threatens: same row, same column, same diagonal
# ============================================================

def is_safe(board, row, col):
    """
    Check if placing a queen at (row, col) is safe.
    We only check previous rows since we place row by row.
    """
    n = len(board)

    # Check same COLUMN (all rows above current row)
    for i in range(row):
        if board[i][col] == 1:
            return False

    # Check upper-LEFT diagonal
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    # Check upper-RIGHT diagonal
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1

    return True   # Position is safe!


# ============================================================
#   STEP 3 — BACKTRACKING ALGORITHM
#   Place queens one row at a time
#   If stuck, go back and try next column
# ============================================================

def solve_n_queens(board, row, solutions, max_solutions=10):
    """
    Recursively solve N-Queens using backtracking.

    Logic:
    - Try placing queen in each column of current row
    - If safe → place queen → move to next row
    - If not safe → try next column
    - If no column works → backtrack to previous row
    - If all rows filled → solution found!
    """
    n = len(board)

    # BASE CASE: all rows filled = solution found!
    if row == n:
        # Save a copy of the solution
        solution = [r[:] for r in board]
        solutions.append(solution)
        return

    # Try placing queen in each column of this row
    for col in range(n):

        # Check if this position is safe
        if is_safe(board, row, col):

            # PLACE the queen
            board[row][col] = 1

            # RECURSE — move to next row
            solve_n_queens(board, row + 1, solutions, max_solutions)

            # Stop if we found enough solutions
            if len(solutions) >= max_solutions:
                return

            # BACKTRACK — remove queen and try next column
            board[row][col] = 0


# ============================================================
#   COUNT TOTAL SOLUTIONS (without storing all)
# ============================================================

def count_solutions(n):
    """Count total number of solutions for N-Queens"""
    board = create_board(n)
    count = [0]

    def backtrack(row):
        if row == n:
            count[0] += 1
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row][col] = 1
                backtrack(row + 1)
                board[row][col] = 0

    backtrack(0)
    return count[0]


# ============================================================
#   SHOW HOW BACKTRACKING WORKS (Step by step)
# ============================================================

def show_backtracking_explanation():
    print_section("HOW BACKTRACKING WORKS")
    print(f"""
  {BOLD}N-Queens Problem Explained:{RESET}

  Goal: Place N queens on NxN board so that
        NO two queens can attack each other.

  A queen can attack in:
    ↕  Same column
    ↔  Same row
    ↗↙ Same diagonal

  {BOLD}Backtracking Steps:{RESET}

  Row 1: Try Column 1 → Place Queen ✅
  Row 2: Try Column 1 → UNSAFE (same column) ❌
         Try Column 2 → UNSAFE (same diagonal) ❌
         Try Column 3 → Place Queen ✅
  Row 3: Try all columns → ALL UNSAFE ❌
         BACKTRACK to Row 2 → Remove queen
         Try Column 4 → Place Queen ✅
  Row 3: Try Column 2 → Place Queen ✅
  ... continue until all rows filled!

  {CYAN}It's like solving a maze — if you hit a dead end,
  go back and try a different path!{RESET}
    """)


# ============================================================
#   KNOWN SOLUTIONS TABLE
# ============================================================

KNOWN_SOLUTIONS = {
    1: 1, 2: 0, 3: 0, 4: 2, 5: 10,
    6: 4, 7: 40, 8: 92, 9: 352, 10: 724
}


# ============================================================
#   MAIN PROGRAM
# ============================================================

def main():
    print(f"""
{BLUE}{BOLD}
╔══════════════════════════════════════════════════╗
║           N-QUEENS PROBLEM SOLVER               ║
║        Level 3 Task 3 — Advanced Python         ║
║                                                 ║
║  Algorithm : Backtracking                       ║
║  Board     : 2D Array                           ║
║  Features  : Solve + Visualize + Count          ║
╚══════════════════════════════════════════════════╝
{RESET}""")

    while True:
        print(f"{BOLD}  MAIN MENU:{RESET}")
        print("    1. Solve N-Queens (see solutions)")
        print("    2. Count total solutions for N")
        print("    3. How backtracking works (explanation)")
        print("    4. Known solutions table")
        print("    5. Exit")

        choice = input(f"\n  Enter choice (1-5): ").strip()

        # ── SOLVE ──
        if choice == "1":
            print_section("SOLVE N-QUEENS")
            try:
                n = int(input("  Enter N (board size, e.g. 4, 5, 6, 8): ").strip())
                if n < 1:
                    print_error("N must be at least 1!")
                    continue
                if n > 12:
                    print_info("N > 12 may take a long time. Showing first 3 solutions only.")

            except ValueError:
                print_error("Please enter a valid number!")
                continue

            print_info(f"Solving {n}-Queens problem using backtracking...")

            board     = create_board(n)
            solutions = []
            max_show  = 3 if n > 8 else 5

            solve_n_queens(board, 0, solutions, max_solutions=max_show)

            if not solutions:
                print_error(f"No solution exists for {n}-Queens!")
                print_info("N=2 and N=3 have no solutions.")

            else:
                print_success(f"Found {len(solutions)} solution(s) (showing up to {max_show})!\n")

                for i, sol in enumerate(solutions, 1):
                    print_board(sol, solution_number=i)
                    print()

                # Total count
                if n <= 10:
                    total = KNOWN_SOLUTIONS.get(n, "?")
                    print_info(f"Total solutions for {n}-Queens: {total}")

        # ── COUNT ──
        elif choice == "2":
            print_section("COUNT TOTAL SOLUTIONS")
            try:
                n = int(input("  Enter N (1-12 recommended): ").strip())
                if n < 1:
                    print_error("N must be at least 1!")
                    continue
                if n > 13:
                    print_info("Warning: N > 13 may take very long!")

            except ValueError:
                print_error("Please enter a valid number!")
                continue

            print_info(f"Counting all solutions for {n}-Queens...")

            import time
            start = time.time()
            total = count_solutions(n)
            elapsed = time.time() - start

            print(f"""
  {CYAN}{BOLD}Results for {n}-Queens:{RESET}
  Board Size    : {n} x {n}
  Total Queens  : {n}
  Total Solutions: {GREEN}{BOLD}{total}{RESET}
  Time Taken    : {elapsed:.4f} seconds
            """)

            if total == 0:
                print_info(f"No solution exists for {n}-Queens problem!")
            else:
                print_success(f"{total} valid arrangement(s) found!")

        # ── EXPLANATION ──
        elif choice == "3":
            show_backtracking_explanation()

        # ── TABLE ──
        elif choice == "4":
            print_section("KNOWN SOLUTIONS TABLE")
            print(f"\n  {BOLD}{'N':>4}  {'Board':>8}  {'Solutions':>12}  {'Note'}{RESET}")
            print(f"  {'─'*50}")

            notes = {
                1: "Trivial",
                2: "No solution",
                3: "No solution",
                4: "First real solution",
                8: "Classic problem",
            }

            for n, sol in KNOWN_SOLUTIONS.items():
                note  = notes.get(n, "")
                color = GREEN if sol > 0 else RED
                print(f"  {n:>4}  {f'{n}x{n}':>8}  "
                      f"{color}{sol:>12}{RESET}  {YELLOW}{note}{RESET}")

        # ── EXIT ──
        elif choice == "5":
            print(f"\n{GREEN}{BOLD}  Goodbye! All 3 Level tasks complete! 🎉{RESET}\n")
            break

        else:
            print_error("Invalid choice! Enter 1-5.")

        print()


if __name__ == "__main__":
    main()
