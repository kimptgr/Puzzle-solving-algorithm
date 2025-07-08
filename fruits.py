"""Script to solve today's salad fruit puzzle in the game "Layton's Mystery Journey".
    """
import time
import threading
import itertools
import copy
import math
EMPTY = 0
APPLE = 1
GRAPS = 2
BANANA = 3
MELON = 4
fruits = [EMPTY, APPLE, GRAPS, BANANA, MELON]
fruits_translate = {
    0: "empty",
    1: "apple",
    2: "grap",
    3: "banan",
    4: "melon"
}

fruits_emoji_translate = {
    0: "🔳",
    1: "🍎",
    2: "🍇",
    3: "🍌",
    4: "🍈"
}

stop_animation = False


def resolve(puzzle: list[list[int]]) -> None:
    """_summary_

    Args:
        puzzle (list[list[int]]): _description_
    """
    row_counts = [[0]*len(fruits) for _ in range(len(puzzle))]
    col_counts = [[0]*len(fruits) for _ in range(len(puzzle[0]))]
    for y, line in enumerate(puzzle):
        for x, case in enumerate(line):
            row_counts[y][case] += 1
            col_counts[x][case] += 1
    if not next_fruit(puzzle, [], row_counts, col_counts):
        print("Pas de solution possible")


def loading_animation() -> None:
    """Print a cycle of points in the console during the solution's research
    """
    for dots in itertools.cycle(['.', '..', '...']):
        if stop_animation:
            break
        print(f'\rRecherche{dots}', end='', flush=True)
        time.sleep(0.5)


def is_touching_the_same(puzzle: list[list[int]], case: tuple[int, int]) -> bool:
    """Determine if 2 values are adjacent

    Args:
        puzzle (list[list[int]]): the puzzle
        case (tuple[int, int]): the case to verify

    Returns:
        bool: Return True if the value of the case is the same of a neightboor
    """
    last_x = len(puzzle[0]) - 1
    last_y = len(puzzle) - 1
    x, y = case
    neighbors = []
    # 2 adjacents
    if x > 0:
        neighbors.append(puzzle[y][x-1])
    if x < last_x:
        neighbors.append(puzzle[y][x+1])
    if y > 0:
        neighbors.append(puzzle[y-1][x])
    if y < last_y:
        neighbors.append(puzzle[y+1][x])

    return puzzle[y][x] in neighbors


def have_double_or_single(line: list[int]) -> bool:
    """Determine if values are unique or in a pair

    Args:
        line (list[int]): A list of values

    Returns:
        bool: Return false if the count of values exceed 2 copy
    """
    counts = [0, 0, 0, 0, 0]

    for fruit in line:
        counts[fruit] += 1
        if fruit > 0 and counts[fruit] > 2:
            return False

    return True


def next_fruit(
        initial_puzzle: list[list[int]],
        current_puzzle: list[list[int]],
        row_counts: list[list[int]],
        col_counts: list[list[int]]) -> bool:
    """Build the different way for the next fruit in the puzzle

    Args:
        initial_puzzle (list[list[int]]): the start puzzle
        current_puzzle list[list[int]]: the puzzle in construct
        row_counts (list[list[int]]): the total of fruits by row
        col_counts (list[list[int]]): the total of fruits by column

    Returns:
        bool: return true if solved
    """

    if not current_puzzle:
        current_puzzle = copy.deepcopy(initial_puzzle)

    if all(row_counts[_][EMPTY] == 0 for _ in range(len(row_counts))) and all(
            col_counts[_][EMPTY] == 0 for _ in range(len(col_counts))):
        print("\nC'est gagné !")
        print_puzzle(current_puzzle)
        return True

    best_choice = find_best_choice(current_puzzle, row_counts, col_counts)
    if best_choice is None:
        return False
    (x, y) = best_choice
    for choice in range(1, 5):
        if row_counts[y][choice] >= 2 or col_counts[x][choice] >= 2:
            continue
        current_puzzle[y][x] = choice
        row_counts[y][EMPTY] -= 1
        col_counts[x][EMPTY] -= 1
        col_counts[x][choice] += 1
        row_counts[y][choice] += 1

        if not is_touching_the_same(current_puzzle, (x, y)) and next_fruit(
                initial_puzzle, current_puzzle, row_counts, col_counts):
            return True

        row_counts[y][EMPTY] += 1
        row_counts[y][choice] -= 1
        col_counts[x][EMPTY] += 1
        col_counts[x][choice] -= 1
        current_puzzle[y][x] = EMPTY
    return False


def find_best_choice(current_puzzle: list[list[int]],
                     row_counts: list[list[int]],
                     col_counts: list[list[int]],) -> tuple[int, int] | None:
    """Find the Minimum Remaining Values in puzzle

    Args:
        current_puzzle (list[list[int]]): the puzzle in construct
        row_counts (list[list[int]]): the total of fruits by row
        col_counts (list[list[int]]): the total of fruits by column

    Returns:
        tuple[int, int] | None: The coordonates where there the fewer choices
    """
    best_choice = None
    path_with_best_choice = math.inf
    for y, line in enumerate(current_puzzle):
        for x, case in enumerate(line):
            if not case:
                possible_choice = 0
                for choice in range(1, 5):
                    current_puzzle[y][x] = choice
                    if not is_touching_the_same(current_puzzle, (x, y)) and row_counts[y][choice] < 2 and col_counts[x][choice] < 2:
                        possible_choice += 1
                if possible_choice == 1:
                    current_puzzle[y][x] = 0
                    return (x, y)
                if path_with_best_choice > possible_choice > 0:
                    best_choice = (x, y)
                current_puzzle[y][x] = 0
    return best_choice


def print_puzzle(puzzle: list[list[int]]) -> None:
    """Print a puzzle in the console with the naming fruits

    Args:
        puzzle (list[list[int]]): puzzle to print
    """
    for line in puzzle:
        print([str(x).replace(str(x), str(fruits_emoji_translate.get(x)))
               for x in line])


if __name__ == "__main__":
    PUZZLE_TEST = [
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        # [MELON, BANANA, MELON, BANANA, GRAPS, APPLE, GRAPS, APPLE],
        [GRAPS, APPLE, GRAPS, APPLE, MELON, BANANA, MELON, BANANA],
        [MELON, BANANA, MELON, BANANA, GRAPS, APPLE, GRAPS, APPLE],
        [GRAPS, APPLE, GRAPS, APPLE, MELON, BANANA, MELON, BANANA],
        [BANANA, MELON, BANANA, MELON, APPLE, GRAPS, APPLE, GRAPS],
        [APPLE, GRAPS, APPLE, GRAPS, BANANA, MELON, BANANA, MELON],
        [BANANA, MELON, BANANA, MELON, APPLE, GRAPS, EMPTY, GRAPS],
        [APPLE, GRAPS, APPLE, GRAPS, BANANA, MELON, BANANA, EMPTY]
    ]

    PUZZLE_21 = [
        [EMPTY, EMPTY, APPLE, EMPTY, EMPTY, BANANA, EMPTY, EMPTY],
        [APPLE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, MELON, EMPTY],
        [EMPTY, BANANA, EMPTY, EMPTY, EMPTY, APPLE, EMPTY, GRAPS],
        [EMPTY, EMPTY, EMPTY, APPLE, MELON, EMPTY, EMPTY, EMPTY],
        [MELON, EMPTY, GRAPS, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY, MELON, EMPTY, BANANA, EMPTY, MELON],
        [EMPTY, APPLE, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, GRAPS, EMPTY, EMPTY, APPLE, EMPTY, APPLE],
    ]

    start = time.time()

    animation_thread = threading.Thread(target=loading_animation)
    animation_thread.start()

    try:
        print("Puzzle de départ : ")
        print_puzzle(PUZZLE_21)
        resolve(PUZZLE_21)
    finally:
        stop_animation = True
        animation_thread.join()
        print(f"Temps d'exécution : {time.time() - start:.2f} secondes")
