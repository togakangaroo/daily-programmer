# [[file:../README.org::*Basic structures][Basic structures:1]]
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Iterator, Tuple

type Position = Tuple[int, int]
type CellValue = int
type MagicSquareCells = dict[Position, CellValue]

@dataclass(frozen=True)
class MagicSquareBuilder:
    """A magic square that is in process of being constructed."""
    cells: MagicSquareCells
    side_size: int
    max_span_sum: int = field(init=False)

    def __post_init__(self) -> None:
        # Using Godel's(?) equation for summing up sequential sequences / square_size
        object.__setattr__(self, 'max_span_sum', self.side_size*(1+self.side_size**2)/2)
# Basic structures:1 ends here

# [[file:../README.org::*Constraints][Constraints:1]]
type Possibility = int

@dataclass(frozen=True)
class Constraint(ABC):
    """Abstract base class for constraints on a magic square."""
    square: MagicSquareBuilder
    position: Position

    @abstractmethod
    def filter(self, possibilities: Iterator[Possibility]) -> Iterator[Possibility]:
        """
        Filter down the given possibilities based on this constraint.
        """
        pass
# Constraints:1 ends here

# [[file:../README.org::*Constraints][Constraints:2]]
class UniquenessConstraint(Constraint):
    def filter(self, possibilities: Iterator[Possibility]) -> Iterator[Possibility]:
        square_values = set(self.square.cells.values())
        return (p for p in possibilities if p not in square_values)
# Constraints:2 ends here
