This is a [neetcode problem](https://neetcode.io/problems/count-number-of-islands) that I told Job him and I can do together.


# Problem Statement

Given a 2D grid grid where `'1'` represents land and `'0'` represents water, count and return the number of islands.

An island is formed by connecting adjacent lands horizontally or vertically and is surrounded by water. You may assume water is surrounding the grid (i.e., all the edges are water).


## Example 1:

Input:

    return [
        ["0","1","1","1","0"],
        ["0","1","0","1","0"],
        ["1","1","0","0","0"],
        ["0","0","0","0","0"]
    ]

Output: `1`


## Example 2:

Input:

    return [
        ["1","1","0","0","1"],
        ["1","1","0","0","1"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"]
    ]

Output: `4`


## Constraints:

-   `1 <= grid.length, grid[i].length <= 100`
-   `grid[i][j]` is `'0'` or `'1'`.


# Brainstorming

As always, we start by looking at hte constraints. Worst case scenario here is `10,000` grid cells. That's not very much

Lets say we just sweep accross all the cells, for each one that's a `1`, we are going to look around and visit all other connected `1` to basically investigate the island. Each time we ru into a previously unvisited `1` that's a new island!

Worst case scenario for that is a checkerboard pattern which would result in visiting something like `10000 + 4*(10000/2) = 30000` cells. That's nothing, optimization beyond that is worthless. Let's just do that.

Since I want to share this with Job, let's do it in python since he knows python.


# Implementation in Python

So first, we're going to need the ability to follow the 1s around and accumulate individual islands

    def accumulate(grid, visited_islands, visited_other, coordinate):
        if coordinate in visited_islands or coordinate in visited_other:
            return
        r, c = coordinate
        if not (0 <= r < len(grid)) or not (0 <= c < len(grid[r])):
            return
        if grid[r][c] == "0":
            return visited_other.add(coordinate)
    
        visited_islands.add(coordinate)
        accumulate(grid, visited_islands, visited_other, (r-1, c))
        accumulate(grid, visited_islands, visited_other, (r, c+1))
        accumulate(grid, visited_islands, visited_other, (r+1, c))
        accumulate(grid, visited_islands, visited_other, (r, c-1))

Lets see if we can use that to get an island

    
    island = set()
    accumulate(example1, island, set(), (1, 1))
    return island

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">0</td>
<td class="org-right">1</td>
</tr>


<tr>
<td class="org-right">2</td>
<td class="org-right">1</td>
</tr>


<tr>
<td class="org-right">1</td>
<td class="org-right">1</td>
</tr>


<tr>
<td class="org-right">0</td>
<td class="org-right">3</td>
</tr>


<tr>
<td class="org-right">2</td>
<td class="org-right">0</td>
</tr>


<tr>
<td class="org-right">0</td>
<td class="org-right">2</td>
</tr>


<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
</tr>
</tbody>
</table>

Yes! We can.

Ok, so then lets figure out the islands

    
    def get_islands(grid):
        "Yield back one node on each island in the grid of characters. Water is a '0'."
    
        visited = set()
    
        for r, row in enumerate(grid):
            for c, cell in enumerate(row):
                coordinate = (r,c)
                if cell != "0" and (coordinate not in visited):
                    yield coordinate
                accumulate(grid, visited, visited, coordinate)

So that will yield back once for each island. Will it give us the right answers?

    
    return sum((1 for _ in get_islands(example1)))

    1

    
    return sum((1 for _ in get_islands(example2)))

    4

Why yes! Yes it will.

