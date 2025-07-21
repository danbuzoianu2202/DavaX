from pydantic import BaseModel, Field


class PowRequest(BaseModel):
    """
    Request schema for power operation.
    Contains base and exponent fields.
    """
    base: int
    exponent: int


class FibonacciRequest(BaseModel):
    """
    Request schema for Fibonacci operation.
    Contains a single field n.
    """
    n: int = Field(ge=0)


class FactorialRequest(BaseModel):
    """
    Request schema for Factorial operation.
    Contains a single field n, which must be non-negative.
    """
    n: int = Field(ge=0)
