import pandas as pd
import numpy as np
from typing import Iterable
from dataclasses import dataclass, field

MagicSquareCells = pd.DataFrame

@dataclass(frozen=True)
class Position:
    row: int
    column: int

@dataclass(frozen=True)
class MagicSquareBuilder:
    cells: MagicSquareCells
    side_size: int = field(init=False)
    max_span_sum: int = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, 'side_size', self.cells.shape[0])
        # Using Godel's(?) equation for summing up sequential sequences / square_size
        object.__setattr__(self, 'max_span_sum', self.side_size*(1+self.side_size**2)/2)

def get_spans(square: MagicSquareBuilder, position: Position) -> Iterable[np.ndarray]:
    row, column = position
    # This row
    yield square.cells.iloc[row, :].values

    # This column
    yield square.cells.iloc[:, column].values

    # \ Diagonal (main diagonal)
    if row == column:
        yield np.diag(square.cells.values)

    # / Diagonal (anti-diagonal)
    if row == square.side_size - column - 1:
        yield np.diag(np.fliplr(square.cells.values))

def try_set(square: MagicSquareBuilder, position: Position, value: int) -> None | MagicSquareBuilder:
    """Return a new square with position set to the passed in value. This will
    do some basic checking to ensure that the returned square could potentially
    still be a magic square. If not it will return None.

    """
    spans = get_spans(square, position)
    if any((square.max_span_sum < (span.sum() + value)) for span in spans):
        return None

    new_cells = square.cells.copy()
    new_cells.iloc[*position] = value
    return MagicSquareBuilder(cells=new_cells)

def remaining_values_to_try(square: MagicSquareBuilder) -> set[int]:
    already_used_values = set(square.cells.values.flatten())
    possible_values = set(range(1, square.side_size**2+1))
    return possible_values - already_used_values

def is_magic_square(square: MagicSquareBuilder) -> bool:
    if remaining_values_to_try(square):
        return False
    row_sums = square.cells.sum(axis=1)
    first_row_sum = row_sums.iloc[0]
    all_rows_equal = (row_sums == first_row_sum).all()
    if not all_rows_equal:
        return False
    col_sums = square.cells.sum(axis=0)
    all_cols_sum_same_as_rows = (col_sums == first_row_sum).all()
    if not all_cols_sum_same_as_rows:
        return False
    return first_row_sum == np.diag(square.cells.values).sum() == np.diag(np.fliplr(square.cells.values)).sum()

remaining_recursions = 100
def fill_magic_square(square: None | MagicSquareBuilder, remaining_positions: list[Position]) -> None | MagicSquareBuilder:
    """Move through the list of positions that need to be filled. At each
    position we try all the remaining possibilities and recurse to the next
    position as needed.
    """
    print("fill_magic_square\n", square and square.cells.to_string(index=False, header=False), "\n", remaining_positions)
    global remaining_recursions
    remaining_recursions -= 1
    if remaining_recursions < 0:
        raise Exception("recursion limit exceeded")
    if not square:
        return None
    if not remaining_positions:
        # If we are out of positions to test and there's a square, then that's going to be the answer
        return square if is_magic_square(square) else None

    next_position, *other_positions = remaining_positions
    for value in remaining_values_to_try(square):
        print("trying", value, "at", next_position, "from", remaining_values_to_try(square))
        square_with_value = try_set(square, next_position, value)
        res = fill_magic_square(square_with_value, other_positions)
        if res:
            return res

    return None

def find_magic_square(size: int) -> None | MagicSquareCells:
    # While prefilling with zeros is not technically correct and would in many situations be better
    # to use nan, when working specifically with magic squares it kind of doesn't matter and
    # prefilling with zeros is just more efficient
    square = MagicSquareBuilder(cells=pd.DataFrame(np.zeros((size, size), dtype=int)))
    positions = list((r, c) for r in range(size) for c in range(size))
    square = fill_magic_square(square, positions)
    return square and square.cells
