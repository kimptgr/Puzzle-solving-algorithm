"""Test the helpful server script"""
from helpful_server import *


def test_is_correct():
    """Test the fonction is correct
    """

    assert is_correct([[DISH,  GIRL_RIGHT], [BOY_LEFT, DISH]], (0, 0)) is False
    assert is_correct([[DISH,  GIRL_RIGHT], [BOY_DOWN, DISH]], (0, 0)) is True
    assert is_correct([[DISH, DISH,  GIRL_RIGHT], [
                      BOY_DOWN, FERN, FERN]], (0, 0)) is True
    assert is_correct([[EMPTY,  GIRL_UP], [BOY_DOWN, DISH]], (0, 1)) is True
    assert is_correct([[FERN,  GIRL_UP], [BOY_LEFT, GIRL_UP]], (1, 1)) is False
    assert is_correct([[FERN,  GIRL_UP], [BOY_DOWN, GIRL_UP]], (0, 1)) is False
    assert is_correct([[DISH,  GIRL_UP], [BOY_DOWN, GIRL_UP]], (0, 1)) is True
    assert is_correct([[DISH,  GIRL_UP], [BOY_LEFT, DISH]], (0, 1)) is True
    assert is_correct(
        [[DISH,  GIRL_UP], [BOY_LEFT, BOY_LEFT]], (1, 1)) is False


def test_count_choices():
    """test the count choices function
    """
    PUZZLE = [
        [EMPTY, DISH, BOY_LEFT],
        [GIRL_RIGHT, EMPTY, BOY_LEFT],
        [EMPTY, EMPTY, EMPTY],
    ]
    assert count_choices(PUZZLE, (0, 0)) == 1
    assert count_choices(PUZZLE, (0, 1)) == 0
    assert count_choices(PUZZLE, (1, 2)) == 4


def test_find_best_item():
    """test the find_best_item's function
    """
    assert find_best_item([[EMPTY, GIRL_RIGHT], [BOY_DOWN, FERN]]) == (0, 0)
    assert find_best_item([
        [BOY_LEFT, EMPTY, EMPTY],
    ]) == (1, 0)


def test_table_have_guests():
    """test the table_have_guests's function
    """
    assert tables_have_guests([[BOY_LEFT, DISH, GIRL_RIGHT]]) is True
    assert tables_have_guests([[BOY_LEFT, DISH, DISH, GIRL_RIGHT]]) is True
    assert tables_have_guests([[GIRL_UP], [DISH], [BOY_DOWN]]) is True
    assert tables_have_guests([[GIRL_UP], [DISH], [DISH], [BOY_DOWN]]) is True
    assert tables_have_guests([[GIRL_UP], [DISH], [DISH]]) is False


def test_get_neighbors():
    """the the get_neighbors function"""
    assert get_neighbors([
        [GIRL_RIGHT, DISH, BOY_DOWN],
        [BOY_LEFT, DISH, GIRL_RIGHT],
        [BOY_LEFT, BOY_DOWN, BOY_LEFT],
    ], (1, 1)) == {'up': DISH, 'down': BOY_DOWN, 'right': GIRL_RIGHT, 'left': BOY_LEFT}

    assert get_neighbors([
        [GIRL_RIGHT, DISH, BOY_DOWN],
        [BOY_LEFT, DISH, GIRL_RIGHT],
        [BOY_LEFT, BOY_DOWN, BOY_LEFT],
    ], (2, 2)) == {'up': GIRL_RIGHT, 'down': '', 'right': '', 'left': BOY_DOWN}

# execute and coverage with coverage run -m pytest && coverage report
