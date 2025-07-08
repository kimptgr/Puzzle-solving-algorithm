"""Script to solve the helpful server puzzles in the game "Layton's Mystery Journey".
    """
import copy
import math

FERN = "🎍"
DISH = "🍝"
GIRL_UP = "🔽"
GIRL_RIGHT = "◀️"
BOY_LEFT = "▶️"
BOY_DOWN = "🔼"
EMPTY = "🔳"

elements = [GIRL_UP, GIRL_RIGHT, BOY_DOWN, BOY_LEFT, DISH]


def solve(puzzle_to_solve: list[list[str]] | None = None) -> None:
    """Solve a given puzzle or call choose_puzzle to build it.

    Args:
        puzzle (list[list[str]], optional): Puzzle who must be resolved. Defaults to None.
    """
    if not puzzle_to_solve:
        puzzle_to_solve = create_puzzle()
    results = []
    next_item(puzzle_to_solve, [], results)
    for result in results:
        if tables_have_guests(result):
            print("Solution :")
            print_puzzle(result)
            print()
    if not results:
        print("Pas de solution trouvée.")


def next_item(initial_puzzle: list[list[str]], current_puzzle: list[list[str]],
              res: list[list[list[str]]]):
    """Build the differant way to sole a puzzle and save the potential result.

    Args:
        initial_puzzle (list[list[str]]): The starting puzzle
        current_puzzle (list[list[str]]): the puzzle being solved
        res (list[list[list[str]]]): Possible solutions to the puzzle
    """
    if not current_puzzle:
        current_puzzle = copy.deepcopy(initial_puzzle)

    if all(current_puzzle[line].count(EMPTY) == 0 for line in range(len(
            current_puzzle))):
        res.append(copy.deepcopy(current_puzzle))

    best_choice = find_best_item(current_puzzle)
    if best_choice is None:
        return
    (x, y) = best_choice

    for choice in elements:
        current_puzzle[y][x] = choice

        if is_correct(current_puzzle, (x, y)):
            next_item(initial_puzzle, current_puzzle, res)
            current_puzzle[y][x] = EMPTY


def find_best_item(puzzle: list[list[str]]) -> tuple[int, int] | None:
    """Find a case in puzzle with the fewer possibilities to fill.

    Args:
        puzzle list[list[str]]: the puzzle

    Returns:
        tuple[int, int]: the coordinates of the case with the fewer possibilities
    """
    best_choice = None
    best_count = math.inf
    for y, line in enumerate(puzzle):
        for x, case in enumerate(line):
            if case == EMPTY:
                count = count_choices(puzzle, (x, y))
                if count == 1:
                    return (x, y)
                if 0 < count < best_count or not best_choice:
                    best_count = count
                    best_choice = (x, y)

    return best_choice


def is_correct(puzzle: list[list[str]], case: tuple[int, int]) -> bool:
    """Said if a case in a puzzle follow the rules

    Args:
        puzzle list[list[str]]: the puzzle where the case is
        case : tuple[int, int]: the coordinates of the case x in line, y column

    Returns:
        bool: Return true if case is a valid choice
    """
    (x, y) = case
    neighbors = get_neighbors(puzzle, case)

    choice = puzzle[y][x]

    if choice == DISH and sum([
        neighbors["left"] in (BOY_LEFT, DISH, EMPTY),
        neighbors["right"] in (GIRL_RIGHT, DISH, EMPTY),
        neighbors["up"] in (GIRL_UP, DISH, EMPTY),
        neighbors["down"] in (BOY_DOWN, DISH, EMPTY),
    ]) > 1:
        return True
    if neighbors["up"] == GIRL_UP or neighbors["right"] == GIRL_RIGHT or neighbors["down"] == BOY_DOWN or neighbors["left"] == BOY_LEFT:
        return False
    if choice == GIRL_UP and neighbors["down"] in (DISH, EMPTY):
        return True
    if choice == GIRL_RIGHT and neighbors["left"] in (DISH, EMPTY):
        return True
    if choice == BOY_DOWN and neighbors["up"] in (DISH, EMPTY):
        return True
    if choice == BOY_LEFT and neighbors["right"] in (DISH, EMPTY):
        return True
    return False


def get_neighbors(puzzle: list[list[str]], case: tuple[int, int]) -> dict[str, str]:
    """Give the cases around a case

    Args:
        puzzle (list[list[str]]): puzzle where case is
        case (tuple[int, int]): case who we need neighbor

    Returns:
        dict[str, str]: a list of neighbor
    """
    (x, y) = case
    neighbors = {"up": "", "down": "", "right": "", "left": ""}
    if x > 0:
        neighbors["left"] = puzzle[y][x-1]
    if x < len(puzzle[0])-1:
        neighbors["right"] = puzzle[y][x+1]
    if y > 0:
        neighbors["up"] = puzzle[y-1][x]
    if y < len(puzzle) - 1:
        neighbors["down"] = puzzle[y+1][x]

    return neighbors


def count_choices(puzzle: list[list[str]], case: tuple[int, int]) -> int:
    """Count the valid choices for a case in a puzzle

    Args:
        puzzle list[list[str]]: the puzzle where the case is
        case : tuple[int, int]: the coordinates of the case x in line, y column

    Returns:
        int: the count of valid choices
    """
    count = 0
    (x, y) = case
    if puzzle[y][x] != EMPTY:
        return count
    for choice in elements:
        puzzle[y][x] = choice
        if is_correct(puzzle, case):
            count += 1
        puzzle[y][x] = EMPTY
    return count


def tables_have_guests(result: list[list[str]]) -> bool:
    """Determine if each table is surrounded by 2 guests facing each other.

    Args:
        result (list[list[str]]): The puzzle with tables and guests.

    Returns:
        bool: Return False if each table is not surrounded by 2 guests facing each other.
    """
    for y, line in enumerate(result):
        for x, case in enumerate(line):
            if case == DISH:
                neighbors = get_neighbors(result, (x, y))
                if (neighbors["left"] == BOY_LEFT and neighbors["right"] == GIRL_RIGHT) or (neighbors["up"] == GIRL_UP and neighbors["down"] == BOY_DOWN):
                    continue
                if neighbors["left"] == BOY_LEFT:
                    i = 1
                    while neighbors["right"] == DISH:
                        if x + i < len(line):
                            neighbors["right"] = result[y][x+i]
                            i += 1
                        else:
                            return False
                    if neighbors["right"] == GIRL_RIGHT:
                        x += i
                        continue
                    return False
                if neighbors["left"] in [BOY_LEFT, DISH] and neighbors["right"] in [GIRL_RIGHT, DISH]:
                    continue
                if neighbors["up"] == GIRL_UP:
                    i = 1
                    while neighbors["down"] == DISH:
                        if y+i < len(result):
                            neighbors["down"] = result[y+i][x]
                            i += 1
                        else:
                            return False
                    if neighbors["down"] == BOY_DOWN:
                        y += i
                        continue
                    return False
                if neighbors["up"] in [GIRL_UP, DISH] and neighbors["down"] in [BOY_DOWN, DISH]:
                    continue
                return False
            if y == len(result)-1 and case == BOY_DOWN:
                neighbors = get_neighbors(result, (x, y))
                i = 1
                while neighbors["up"] == DISH:
                    if y-i >= 0:
                        neighbors["up"] = result[y-i][x]
                        i += 1
                    else:
                        return False
                if neighbors["up"] == GIRL_UP:
                    continue
                return False

    return True


def create_puzzle() -> list[list[str]]:
    """Build a puzzle with the user.

    Returns:
        list[list[str]]: _description_
    """
    SYMBOLS = {
        1: FERN,
        2: DISH,
        3: GIRL_UP,
        4: GIRL_RIGHT,
        5: BOY_LEFT,
        6: BOY_DOWN,
        7: EMPTY
    }

    try:
        rows = int(input("Nombre de lignes du puzzle : "))
        cols = int(input("Nombre de colonnes du puzzle : "))
    except ValueError:
        print("Entrée invalide. Veuillez entrer des nombres entiers.")
        return create_puzzle()

    print("\nUtilisez les numéros suivants pour chaque case :")
    for num, symbol in SYMBOLS.items():
        print(f"{num}. {symbol}")
    print("Entrez chaque ligne avec les numéros sans espace(ex: 17237)\n")

    puzzle = []
    for y in range(rows):
        while True:
            line_input = input(f"Ligne {y+1} : ")
            if len(line_input) != cols or not all(c.isdigit() and int(c) in SYMBOLS for c in line_input):
                print(
                    f"⚠️  Ligne invalide. Entrez exactement {cols} chiffre{"" if cols == 1 else "s"} entre 1 et 7.")
                continue
            puzzle.append([SYMBOLS[int(c)] for c in line_input])
            break

    print("\nGrille finale :")
    print_puzzle(puzzle)
    return puzzle


def print_puzzle(puzzle: list[list[str]]):
    """Print the puzzle in the console

    Args:
        puzzle (list[list[str]]): Puzzle who should be print in the console
    """
    for line in puzzle:
        print("   ".join(line))


if __name__ == "__main__":
    PUZZLE = [
        [GIRL_RIGHT, DISH, BOY_DOWN],
        [BOY_LEFT, DISH, GIRL_RIGHT],
        [BOY_LEFT, BOY_DOWN, BOY_LEFT],
    ]
    PUZZLE_04 = [
        [FERN, EMPTY, EMPTY, EMPTY, EMPTY],  # 17777
        [EMPTY, EMPTY, GIRL_RIGHT, GIRL_UP, EMPTY],  # 77437
        [BOY_LEFT, EMPTY, EMPTY, EMPTY, EMPTY],  # 57777
        [EMPTY, EMPTY, EMPTY, EMPTY, BOY_DOWN],  # 77776
        [FERN, BOY_DOWN, EMPTY, EMPTY,  EMPTY]  # 16777
    ]
    solve()
