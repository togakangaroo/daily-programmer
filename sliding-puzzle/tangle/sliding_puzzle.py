def _get_value_at_index(coll, idx):
    if not (0 <= idx < len(coll)):
        raise IndexError(f"Invalid index {idx}")
    return coll[idx]

def value_at_location(state, loc, **kwargs):
    try:
        return _get_value_at_index( _get_value_at_index(state, loc[0]), loc[1])
    except IndexError:
        if "default" in kwargs:
            return kwargs["default"]
        raise

from copy import deepcopy
def swap(state, from_, to_):
    t = value_at_location(state, to_)
    s = list(deepcopy(state))
    s[to_[0]] = list(s[to_[0]])
    s[from_[0]] = list(s[from_[0]])
    s[to_[0]][to_[1]] = value_at_location(state, from_)
    s[from_[0]][from_[1]] = t
    s[to_[0]] = tuple(s[to_[0]])
    s[from_[0]] = tuple(s[from_[0]])
    return tuple(s)

def get_navigable_states(state, from_value):
    for (r, row) in enumerate(state):
        for (c, cell) in enumerate(row):
            if cell == from_value:
                for l in ((r,c+1),
                          (r+1,c),
                          (r,c-1),
                          (r-1,c)):
                    if value_at_location(state, l, default=None) is not None:
                        yield swap(state, (r,c), l)
                return


from itertools import chain

_end_state = ((1,2,3), (4,5,0))
def find_min_move(states, desired_state=_end_state, known_states=set()):
    if desired_state in states:
        return 0
    novel_states = set(states) - known_states
    if not novel_states:
        return None
    known_states = known_states | novel_states #https://stackoverflow.com/questions/58583158/why-does-seem-to-mutate-a-set-when-the-long-form-does-not

    next_states = list(chain(*(get_navigable_states(s, from_value=0) for s in novel_states)))
    next_count = find_min_move(next_states, desired_state, known_states)
    return None if next_count is None else next_count + 1
