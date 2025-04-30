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

def is_magic_square(square: MagicSquareBuilder) -> bool:
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

def _potential_span_sums(square: MagicSquareBuilder, position: Position) -> Iterable[int]:
    row, column = position
    yield square.cells.iloc[row, :].values.sum()
    yield square.cells.iloc[:, column].values.sum()

    # \ Diagonal (main diagonal)
    if row == column:
        yield np.diag(square.cells.values).sum()

    # / Diagonal (anti-diagonal)
    if row == square.side_size - column - 1:
        yield np.diag(np.fliplr(square.cells.values)).sum()

def try_set(square: MagicSquareBuilder, position: Position, value: int) -> None | MagicSquareBuilder:
    """Return a new square with position set to the passed in value. This will
    do some basic checking to ensure that the returned square could potentially
    still be a magic square. If not it will return None.
    """

    span_sums = _potential_span_sums(square, position)
    if any((square.max_span_sum < (x + value)) for x in span_sums):
        return None

    new_cells = square.cells.copy()
    new_cells.iloc[*position] = value
    return MagicSquareBuilder(cells=new_cells)

remaining_recursions = 100000
def fill_magic_square(square: None | MagicSquareBuilder, remaining_positions: list[Position], remaining_values_to_try: list[int]) -> None | MagicSquareBuilder:
    assert len(remaining_positions) == len(remaining_values_to_try)
    global remaining_recursions

    assert 0 < remaining_recursions
    remaining_recursions -= 1

    if not remaining_positions:
        return square if is_magic_square(square) else None

    position_to_set, *other_positions = remaining_positions

    for value in remaining_values_to_try:
        square_with_value = try_set(square, position_to_set, value)
        if not square_with_value:
            continue
        all_other_values_to_try = [v for v in remaining_values_to_try if v != value]
        filled_square_with_value = fill_magic_square(square_with_value, other_positions, all_other_values_to_try)
        if filled_square_with_value:
            return filled_square_with_value

    return None

def find_magic_square(size: int) -> None | MagicSquareCells:
    # While prefilling with zeros is not technically correct and would in many situations be better
    # to use nan, when working specifically with magic squares it kind of doesn't matter and
    # prefilling with zeros is just more efficient
    square = MagicSquareBuilder(cells=pd.DataFrame(np.zeros((size, size), dtype=int)))
    positions = list((r, c) for r in range(size) for c in range(size))
    all_values = list(range(1, size**2+1))
    square = fill_magic_square(square, positions, all_values)
    return square and square.cells

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        find_magic_square(int(sys.argv[1]))
