import math


class Services:
    """
    A collection of mathematical services for various calculations.
    """

    @staticmethod
    def calculate_power(base: int, exponent: int) -> int:
        """
        Calculate the power of a number.

        :param base: The base number.
        :param exponent: The exponent to raise the base to.
        :return: The result of base raised to the exponent.
        """
        return base ** exponent

    @staticmethod
    def calculate_fibonacci(n: int) -> int:
        """
        Calculate the nth Fibonacci number.

        :param n: The position in the Fibonacci sequence (0-indexed).
        :return: The nth Fibonacci number.
        """
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a

    @staticmethod
    def calculate_factorial(n: int) -> int:
        """
        Calculate the factorial of a number.

        :param n: The number to calculate the factorial for.
        :return: The factorial of n."""
        if n < 0:
            raise ValueError("Negative numbers not allowed")
        return math.factorial(n)
