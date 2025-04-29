from functools import wraps
from typing import Any, Callable, Literal, Union


def weight(value: Union[int, float]) -> Callable[[Any], Any]:
    """
    Decorator for setting the weight of a test.
    :param value: The weight of the test.
    :return: A decorator that adds the weight attribute to the test function.

    Usage: @weight(10)
    """
    if not isinstance(value, (int, float)):
        raise TypeError("Weight must be an integer or a float")
    if value < 0:
        raise ValueError("Weight must be a non-negative integer")

    def wrapper(f):
        f.weight = value
        return f

    return wrapper


def number(value: str) -> Callable[[Any], Any]:
    """
    Optional decorator for setting the number of a test.
    :param value: The number of the test.
    :return: A decorator that adds the number attribute to the test function.

    Usage: @number("1.5")
    """

    def wrapper(f):
        f.number = str(value)
        return f

    return wrapper


type Visibility = Union[
    Literal["hidden"],
    Literal["after_due_date"],
    Literal["after_published"],
    Literal["visible"],
]


def visibility(visibility: Visibility) -> Callable[[Any], Any]:
    """
    Optional decorator for setting the visibility of a test.
    :param visibility: The visibility of the test.
    Can be one of "hidden", "after_due_date", "after_published", or "visible" (default)
    :return: A decorator that adds the visibility attribute to the test function.
    Usage: @visibility("hidden")
    """
    if visibility not in ["hidden", "after_due_date", "after_published", "visible"]:
        raise ValueError(
            "Visibility must be one of 'hidden', 'after_due_date', 'after_published', or 'visible'"
        )

    def wrapper(f):
        f.visibility = visibility
        return f

    return wrapper


def hide_errors(msg: str = "Test failed") -> Callable[[Any], Any]:
    """
    Optional decorator for hiding errors in a test.
    :return: A decorator that adds the hide_errors attribute to the test function.

    Usage: @hide_errors()
    """

    def wrapper(f):
        f.hide_errors = msg
        return f

    return wrapper


def tags(tags: Union[str, list[str]]) -> Callable[[Any], Any]:
    """
    Optional decorator for setting tags for a test.
    :param tags: A single tag or a list of tags for the test.
    :return: A decorator that adds the tags attribute to the test function.
    Usage: @tags("example") or @tags(["example", "test"])
    """
    if isinstance(tags, str):
        tags = [tags]
    if not isinstance(tags, list):
        raise TypeError("Tags must be a string or a list of strings")

    def wrapper(f):
        f.tags = [str(tag) for tag in tags]
        return f

    return wrapper


type LeaderboardSortOrder = Union[Literal["asc"], Literal["desc"]]


def leaderboard(
    column_name: str, sort_order: LeaderboardSortOrder = "desc"
) -> Callable[[Any], Any]:
    """
    Optional decorator for setting leaderboard attributes for a test.
    :param column_name: The name of the column to be used in the leaderboard.
    :param sort_order: The sort order of the leaderboard, either "asc" or "desc". Default is "desc".
    :return: A decorator that adds the leaderboard attributes to the test function.
    Usage:
    @leaderboard("score", "asc")
    def test_function(set_leaderboard_value=None):
        set_leaderboard_value(100)
    """

    if sort_order not in ["asc", "desc"]:
        raise ValueError("Sort order must be either 'asc' or 'desc'")

    def wrapper(f):
        f.leaderboard_column = str(column_name)
        f.leaderboard_sort_order = sort_order

        def set_leaderboard_value(value: Any) -> None:
            f.leaderboard_value = value

        @wraps(f)
        def internal_wrapper(*args, **kwargs):
            kwargs["set_leaderboard_value"] = set_leaderboard_value
            return f(*args, **kwargs)

        return internal_wrapper

    return wrapper


def partial_credit(value: Union[int, float]) -> Callable[[Any], Any]:
    """
    Optional decorator for setting partial credit for a test.
    :param value: The partial credit value for the test.
    :return: A decorator that adds the partial_credit attribute to the test function.

    Usage:
    @partial_credit(5)
    def test_function(set_score=None):
        set_score(3)
    """
    if not isinstance(value, (int, float)):
        raise TypeError("Weight must be an integer or a float")
    if value < 0:
        raise ValueError("Weight must be a non-negative integer")

    def wrapper(f):
        f.weight = value

        def set_score(score: Union[int, float]) -> None:
            if not isinstance(score, (int, float)):
                raise TypeError("Score must be an integer or a float")
            if score < 0:
                raise ValueError("Score must be a non-negative integer")
            f.score = score

        @wraps(f)
        def internal_wrapper(*args, **kwargs):
            kwargs["set_score"] = set_score
            return f(*args, **kwargs)

        return internal_wrapper

    return wrapper
