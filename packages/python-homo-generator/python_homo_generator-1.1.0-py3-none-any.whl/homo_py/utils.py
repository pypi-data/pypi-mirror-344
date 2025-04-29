"""
This module contains utility functions for the homo-py package.
"""
from decimal import Decimal, getcontext
import re

# Set precision for Decimal calculations
getcontext().prec = 50

def get_min_div(num: int, nums_reversed: list) -> int:
    """
    Finds the largest divisor that is less than or equal to the given number.

    Args:
        num (int): The number to decompose.
        nums_reversed (list): A list of available divisors in descending order.

    Returns:
        int: The largest divisor less than or equal to `num`.
    """
    for i in nums_reversed:
        if num >= int(i):
            return int(i)
    return None

def demolish(num: str, Nums: dict, nums_reversed: list) -> str:
    """
    Decomposes a number into a symbolic expression using definitions from `Nums`.

    Args:
        num (str): The number to be decomposed, provided as a string.
        Nums (dict): A dictionary containing number-symbol mappings.
        nums_reversed (list): A list of available divisors in descending order.

    Returns:
        str: The symbolic decomposition of the number.
    """
    # Regular expressions to check for digits only and to handle decimals
    is_dot_regex = re.compile(r'\.(\d+?)0{0,}$')

    try:
        # Use Decimal to ensure high-precision calculations
        num = Decimal(num)
        if num == num.to_integral_value():
            # If the integer is directly in Nums, return its representation
            if str(num) in Nums:
                return str(num)
            num = int(num)
        else:
            # If the number is a float, scale it up and recursively call demolish
            n = len(is_dot_regex.search(f"{num:.16f}").group(1))
            numm = f"({demolish(str(int(num * (10 ** n))), Nums, nums_reversed)})/(10)^({n})"
            return numm
    except:
        return f"這麼惡臭的{num}有必要論證嗎（惱"

    # Handle negative numbers by recursively decomposing the positive counterpart
    if num < 0:
        return f"(⑨)*({demolish(str(-num), Nums, nums_reversed)})".replace("*(1)", "")

    # Get the largest divisor of num and decompose recursively
    div = get_min_div(num, nums_reversed)

    if div is None or div == 0 or div > num or (num // div) == 0 or (num % div) == num:
        return str(num)

    return (
        f"{div}*({demolish(str(num // div), Nums, nums_reversed)})+({demolish(str(num % div), Nums, nums_reversed)})"
        .replace("*(1)", "")
        .replace("+(0)", "")
    )

def finisher(expr: str, Nums: dict) -> str:
    """
    Replaces numbers and special symbols in the expression using `Nums` dictionary,
    then formats the expression to make it more readable.

    Args:
        expr (str): The symbolic expression to be formatted.
        Nums (dict): A dictionary containing number-symbol mappings.

    Returns:
        str: The formatted symbolic expression.
    """
    # Replace numbers and specific symbols from Nums, replacing "^" with "**"
    expr = re.sub(r'\d+|⑨', lambda m: str(Nums.get(m.group(), m.group())), expr).replace("^", "**")

    # Match and replace expressions where parentheses follow multiplication or division
    while re.search(r'[\*/]\([^\+\-\(\)]+\)', expr):
        expr = re.sub(r'([\*/])\(([^\+\-\(\)]+)\)', r'\1\2', expr)

    # Match and replace expressions where parentheses follow addition or subtraction
    while re.search(r'[\+\-]\([^\(\)]+\)[\+\-\)]', expr):
        expr = re.sub(r'([\+\-])\(([^\(\)]+)\)([\+\-\)])', r'\1\2\3', expr)

    # Match and replace expressions ending with parentheses following addition or subtraction
    while re.search(r'[\+\-]\([^\(\)]+\)$', expr):
        expr = re.sub(r'([\+\-])\(([^\(\)]+)\)$', r'\1\2', expr)

    # Remove outermost parentheses if the entire expression is enclosed
    if re.match(r'^\([^\(\)]+?\)$', expr):
        expr = re.sub(r'^\(([^\(\)]+)\)$', r'\1', expr)

    # Replace "+-" with "-"
    expr = expr.replace("+-", "-")
    return expr