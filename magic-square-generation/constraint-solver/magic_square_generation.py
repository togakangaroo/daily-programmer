# [[file:../../README.org::*Basic structures][Basic structures:1]]
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Iterable, Tuple

type Position = Tuple[int, int]
type CellValue = int
type MagicSquareCells = dict[Position, CellValue]

@dataclass(frozen=True)
class MagicSquareBuilder:
    """A magic square that is in process of being constructed."""
    cells: MagicSquareCells
    side_size: int
    span_sum: int = field(init=False)

    def __post_init__(self) -> None:
        # Using Godel's(?) equation for summing up sequential sequences / square_size
        object.__setattr__(self, 'span_sum', self.side_size*(1+self.side_size**2)/2)

    def set(self, position: Position, value: CellValue) -> "MagicSquareBuilder":
        new_cells = {**self.cells, position: value}
        return MagicSquareBuilder(cells=new_cells, side_size=self.side_size)
# Basic structures:1 ends here

# [[file:../../README.org::*Constraints][Constraints:1]]
type Possibility = int

@dataclass(frozen=True)
class Constraint(ABC):
    """Abstract base class for constraints on a magic square."""
    square: MagicSquareBuilder
    position: Position

    @abstractmethod
    def filter(self, possibilities: Iterable[Possibility]) -> Iterable[Possibility]:
        """
        Filter down the given possibilities based on this constraint.
        """
        pass
# Constraints:1 ends here

# [[file:../../README.org::*Constraints][Constraints:2]]
@dataclass(frozen=True)
class UniquenessConstraint(Constraint):
    def filter(self, possibilities: Iterable[Possibility]) -> Iterable[Possibility]:
        square_values = set(self.square.cells.values())
        return (p for p in possibilities if p not in square_values)
# Constraints:2 ends here

# [[file:../../README.org::*Constraints][Constraints:3]]
@dataclass(frozen=True)
class RowSumConstraint(Constraint):
    def filter(self, possibilities: Iterable[Possibility]) -> Iterable[Possibility]:
        r,c = self.position
        sum_before_position = sum((self.square.cells[(rb,c)] for rb in range(0,r)))
        lowest_possible_sum_after_position = int((self.square.side_size-r-1)*(self.square.side_size-r)/2) # this cannot ever be odd

        maximum = self.square.span_sum - sum_before_position - lowest_possible_sum_after_position
        minimum = 1 if r+1<self.square.side_size else maximum

        return (p for p in possibilities if minimum <= p <= maximum)

@dataclass(frozen=True)
class ColumnSumConstraint(Constraint):
    def filter(self, possibilities: Iterable[Possibility]) -> Iterable[Possibility]:
        r,c = self.position
        sum_before_position = sum((self.square.cells[(r,cb)] for cb in range(0,c)))
        lowest_possible_sum_after_position = int((self.square.side_size-c-1)*(self.square.side_size-c)/2) # this cannot ever be odd

        maximum = self.square.span_sum - sum_before_position - lowest_possible_sum_after_position
        minimum = 1 if c+1<self.square.side_size else maximum

        return (p for p in possibilities if minimum <= p <= maximum)

@dataclass(frozen=True)
class DiagonalSumConstraint(Constraint):
    def filter(self, possibilities: Iterable[Possibility]) -> Iterable[Possibility]:
        r,c = self.position
        if r != c:
            return possibilities
        sum_before_position = sum((self.square.cells[(rb,rb)] for rb in range(0,r)))

        lowest_possible_sum_after_position = int((self.square.side_size-r-1)*(self.square.side_size-r)/2) # this cannot ever be odd

        minimum = 1
        maximum = self.square.span_sum - sum_before_position - lowest_possible_sum_after_position
        minimum = 1 if r+1<self.square.side_size else maximum

        return (p for p in possibilities if minimum <= p <= maximum)

@dataclass(frozen=True)
class AntiDiagonalSumConstraint(Constraint):
    def filter(self, possibilities: Iterable[Possibility]) -> Iterable[Possibility]:
        r,c = self.position
        if r + 1 != self.square.side_size - c:
            return possibilities
        sum_before_position = sum((self.square.cells[(rb,(self.square.side_size-rb-1))] for rb in range(0,r)))

        lowest_possible_sum_after_position = int((self.square.side_size-r-1)*(self.square.side_size-r)/2) # this cannot ever be odd

        minimum = 1
        maximum = self.square.span_sum - sum_before_position - lowest_possible_sum_after_position
        minimum = 1 if r+1<self.square.side_size else maximum

        return (p for p in possibilities if minimum <= p <= maximum)
# Constraints:3 ends here

# [[file:../../README.org::*Constraints][Constraints:4]]
def get_possibilities(square: MagicSquareBuilder) -> Iterable[Possibility]:
    return range(1, square.side_size**2+1)
# Constraints:4 ends here

# [[file:../../README.org::*Implementing our search][Implementing our search:1]]
def possibilities_to_values(possibilities: Iterable[Possibility]) -> Iterable[CellValue]:
    return possibilities # For now that is all this is, at some point later we might be handling ranges here

def fill_magic_square(square: MagicSquareBuilder, remaining_positions: list[Position]) -> None | MagicSquareBuilder:
    if not square or not remaining_positions:
        return square

    position, *other_positions = remaining_positions

    filters = (
        UniquenessConstraint(square, position),
        RowSumConstraint(square, position),
        ColumnSumConstraint(square, position),
        DiagonalSumConstraint(square, position),
        AntiDiagonalSumConstraint(square, position),
    )

    possibilities = get_possibilities(square)
    for f in filters:
        possibilities = f.filter(possibilities)

    for value in possibilities_to_values(possibilities):
        resulting_filled_square = fill_magic_square(square.set(position, value), other_positions)
        if resulting_filled_square:
            return resulting_filled_square

    return None
# Implementing our search:1 ends here

# [[file:../../README.org::*Implementing our search][Implementing our search:4]]
def find_magic_square(size: int) -> None | MagicSquareBuilder:
    square = MagicSquareBuilder(cells={}, side_size=size)
    positions = list((r, c) for r in range(size) for c in range(size))
    final_square = fill_magic_square(square, positions)
    return final_square

def print_magic_square(square: MagicSquareBuilder | None) -> None:
    if not square:
        print("No such square")
        return

    for r in range(square.side_size):
        print('\t'.join([str(square.cells[r,c]) for c in range(square.side_size)]))

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        find_magic_square(int(sys.argv[1]))
# Implementing our search:4 ends here
