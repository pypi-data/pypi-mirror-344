"""
This module contains the `homo` function, which converts a given number into a symbolic expression.
"""
from .utils import get_min_div, finisher, demolish
import json
import os

def load_nums() -> dict:
    """
    Loads the `nums.json` file, which contains mappings for specific numbers
    to corresponding symbolic expressions.

    Returns:
        dict: A dictionary containing number-symbol mappings from `nums.json`.
    """
    path = os.path.join(os.path.dirname(__file__), 'statics/nums.json')
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Load number-symbol mappings from JSON file
NUMS = load_nums()

def homo(num: int or float or str) -> str:
    """
    Converts a given number (integer, float, or string) into a symbolic expression
    based on predefined mappings in `NUMS`.

    Args:
        num (int, float, or str): The number to be converted into a symbolic expression.

    Returns:
        str: The symbolic expression corresponding to the input number.
    """
    if not isinstance(num, str):
        num = str(num)  # Ensure `num` is always a string for processing

    # Calculate all available divisors from `NUMS`, filtering and sorting them in descending order
    nums_reversed = sorted(
        [
            int(x)
            for x in NUMS.keys()
            if x.isascii() and x.isdigit() and int(x) > 0
        ], reverse=True
    )

    # Generate and format the expression for the input number
    expression = demolish(num, NUMS, nums_reversed)
    return finisher(expression, NUMS)