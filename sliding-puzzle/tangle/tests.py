from sliding_puzzle import value_at_location, swap, find_min_move
import pytest

state = ((1,2,3),
         (4,5,0))

@pytest.mark.parametrize("loc,val", 
  [
    ((0,1), 2), 
    ((0,3), None), 
    ((-1,1), None),
  ] 
)
def test_value_at_location(loc, val):
  assert value_at_location(state, loc, default=None) == val

@pytest.mark.parametrize("from_,to_,expected",
  [
    ((1,2), (0,2), ((1,2,0),(4,5,3)) ), 
    ((1,2), (1,1), ((1,2,3),(4,0,5)) ), 
  ]
)
def test_swap(from_,to_,expected):
  assert swap(state, from_, to_) == expected

@pytest.mark.parametrize("state, min_move", (
  [(((1, 2, 3), (4, 0, 5)), 1), (((1, 2, 3), (5, 4, 0)), None), (((4, 1, 2), (5, 0, 3)), 5), (((3, 2, 4), (1, 5, 0)), 14)]
  
))
def test_find_min_move(state, min_move):
  assert find_min_move([state]) == min_move
