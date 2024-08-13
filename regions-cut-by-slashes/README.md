This is a [Leetecode problem](https://leetcode.com/problems/regions-cut-by-slashes/description/) posted on [UnderdogDevs Slack](https://underdog-devs.slack.com/archives/C02FFHZT200/p1723305799756219)

To view the solution directly as a Kotlin file [see here](./regions-cut-by-slashes.kts).


# Problem Statement

An `n x n` grid is composed of `1 x 1` squares where each `1 x 1` square consists of a `'/'`, `'\'`, or blank space `' '`. These characters divide the square into contiguous regions.

Given the grid grid represented as a string array, return the number of regions.

Note that backslash characters are escaped, so a `'\'` is represented as `'\\'`.


## Example 1:

-   **Input:** 

    [ " /" ,
      "/ " ]

-   **Output:** 2. One region for top left and another bottom right


## Example 1:

-   **Input:** 

    [ " /" ,
      "  " ]

-   **Output:** 1. One region wraps around the slash


## Example 3:

-   **Input:** 

    [ "/\" ,
      "\/" ]

-   **Output:** 5. One region inmiddle and another at each corner


## Constraints:

-   `n == grid.length == grid[i].length`
-   `1 <= n <= 30`
-   `grid[i][j] is either '/', '\', or ' '.`


# Brainstorming

So&#x2026;this is a problem about connectivity. Basically a "how many graphs do we have here" problem. A given cell (1x1 square) is actually one or two two nodes in our graph.

-   If `" "`
    -   A single Node connected in every direction
-   If `"/"`
    -   NodeNW (the top) will be connected left and upward
    -   NodeSE will be connected right and downward
-   If `"\"`
    -   NodeNE (the top) will be connected right and upward
    -   NodeSW will be connected left and downward

Where exactly it will be connected in each direction is interesting since "left" could be either the single Node, NodeA, or NodeB depending on what is going on in that cell. it could also be no connection at all if near a boundary. I think it might be smart to do this in two asses, one to set the nodes in each cell and another to actually connect the nodes.

From there, once you have the graphs built out, its a much simpler problem of just visiting each node and counting.

One thing to note is that the contraints are really pretty good to us here. At worst we have `30x30=900` cells, which is at worst `1800` nodes. Even if we do something dumb and scan the graph once for each node `O(n^2)` that's really only 3.24 million. Easily done on even a low power computer.


# Implementation

While, I'm pretty sure this is unnecessary, where my mind goes to with the plan I laid out above is to doing some basic OO here. You have cells and those contain nodes. Nodes are interconnected to each other. Each cell can contain 1 or 2 nodes (although extensibility would be possible) and these nodes will interconnect

Kotlin works well for this.

Note that for the purposes of our graph-separation, the cells don't actually matter, they are a tool for constructing and connecting nodes, they are not integral to our structure beyond that

    val input = arrayOf(" /",
                        "/ ")
    
    abstract class Node {
        val children: MutableSet<Node> = mutableSetOf()
    }
    class FullNode : Node() {}
    class NodeNW : Node() {}
    class NodeNE : Node() {}
    class NodeSW : Node() {}
    class NodeSE : Node() {}
    
    class Cell(val type: Char) {
        val nodes: Array<Node> = when (type) {
            ' ' -> arrayOf(FullNode())
            '/' -> arrayOf(NodeNW(), NodeSE())
            '\\' -> arrayOf(NodeNE(), NodeSW())
            else -> throw IllegalArgumentException("Invalid cell type: $type")
        }
        override fun toString(): String {
            return "Cell($type, n=${nodes.size})"
        }
    }
    
    val cellGrid = input.map { row -> row.map { char ->
                                          Cell(char)
                                      }.toTypedArray()}.toTypedArray()
    "\n"+cellGrid.map {r -> r.map {c -> c.toString() }.joinToString("")}.joinToString("\n")

    res53: kotlin.String =
    Cell( , n=1)Cell(/, n=2)
    Cell(/, n=2)Cell( , n=1)
    res54: kotlin.String = >>>

This works, now we need to interconnect our nodes. We'll use cardinal directions for communicating ho

    enum class Direction { NORTH, EAST, SOUTH, WEST }

By knowing the direction, each node can know whether it should connect and how

-   FullNode
    -   **→ FullNode:** yes
    -   **→ NWNode:** yes
    -   **→ NENode:** no
    -   **→ SENode:** no
    -   **→ SWNode:** yes
    -   &#x2026;
-   NWNode
    -   → no to all
    -   **← FullNode:** yes
    -   **← NWNode:** no
    -   **← NENode:** yes
    -   **← SENode:** yes
    -   **← SWNode:** no
    -   &#x2026;
-   &#x2026;

So basically each node can "reject" to make a connection. This implies a double-dispatch sort of thing might be a good idea

    abstract class Node {
        val children: MutableSet<Node> = mutableSetOf()
        abstract fun connectTo(node: Node, direction: Direction)
        abstract fun connectFrom(node: Node, direction: Direction) //from node we were connecting in direction
        override fun toString(): String {
            return "${this::class.simpleName}(#c=${children.size})"
        }
    }
    
    
    class FullNode : Node() {
        override fun connectTo(node: Node, direction: Direction) {
            node.connectFrom(this, direction)
        }
        override fun connectFrom(node: Node, direction: Direction) {
            node.children.add(this)
        }
    
    }
    
    class NodeNW : Node() {
        override fun connectTo(node: Node, direction: Direction) {
            if (direction == Direction.NORTH || direction == Direction.WEST)
              node.connectFrom(this, direction)
        }
        override fun connectFrom(node: Node, direction: Direction) {
            if (direction == Direction.SOUTH || direction == Direction.EAST)
              node.children.add(this)
        }
    }
    
    class NodeNE : Node() {
        override fun connectTo(node: Node, direction: Direction) {
            if (direction == Direction.NORTH || direction == Direction.EAST)
              node.connectFrom(this, direction)
        }
        override fun connectFrom(node: Node, direction: Direction) {
            if (direction == Direction.SOUTH || direction == Direction.WEST)
              node.children.add(this)
        }
    }
    
    class NodeSW : Node() {
        override fun connectTo(node: Node, direction: Direction) {
            if (direction == Direction.SOUTH || direction == Direction.WEST)
              node.connectFrom(this, direction)
        }
        override fun connectFrom(node: Node, direction: Direction) {
            if (direction == Direction.NORTH || direction == Direction.EAST)
              node.children.add(this)
        }
    }
    
    class NodeSE : Node() {
        override fun connectTo(node: Node, direction: Direction) {
            if (direction == Direction.SOUTH || direction == Direction.EAST)
              node.connectFrom(this, direction)
        }
        override fun connectFrom(node: Node, direction: Direction) {
            if (direction == Direction.NORTH || direction == Direction.WEST)
              node.children.add(this)
        }
    }

A Cell can also \`connectTo\` other cells, it does this by fully trying to interconnect is nodes with the other's

    class Cell(val type: Char) {
        val nodes: Array<Node> = when (type) {
            ' ' -> arrayOf(FullNode())
            '/' -> arrayOf(NodeNW(), NodeSE())
            '\\' -> arrayOf(NodeNE(), NodeSW())
            else -> throw IllegalArgumentException("Invalid cell type: $type")
        }
    
        fun connectTo(otherCell: Cell?, direction: Direction) {
            if (otherCell == null) return
            for (thisNode in nodes)
                for (otherNode in otherCell.nodes)
                    thisNode.connectTo(otherNode, direction)
        }
    
        override fun toString(): String {
            return "Cell($type, n=${nodes.size})"
        }
    }

We then simply need to use cells to interconnect our nodes. Again, since Cells aren't actually integral to the graph structure, we use the cell structure, but really only care about the nodes this generates.

    fun getNodes(input: Array<String>): Set<Node> {
      val cellGrid = input.map { row -> row.map { char ->
                                            Cell(char)
                                        }.toTypedArray()}.toTypedArray()
    
      for (r in cellGrid.indices) {
          for (c in cellGrid[r].indices) {
              val thisCell = cellGrid[r][c]
              cellGrid.getOrNull(r - 1)?.getOrNull(c)?.let { thisCell.connectTo(it, Direction.NORTH) } // Up
              cellGrid.getOrNull(r)?.getOrNull(c + 1)?.let { thisCell.connectTo(it, Direction.EAST) } // Right
              cellGrid.getOrNull(r + 1)?.getOrNull(c)?.let { thisCell.connectTo(it, Direction.SOUTH) } // Down
              cellGrid.getOrNull(r)?.getOrNull(c - 1)?.let { thisCell.connectTo(it, Direction.WEST) } // Left
          }
      }
    
      return cellGrid.flatMap { it.asIterable() }.flatMap { it.nodes.asIterable() }.toSet()
    }

So now lets run that and see our nodes

    
    
    
    
    println(getNodes(arrayOf(" /",
                             "/ ")))

    [FullNode(#c=2), NodeNW(#c=1), NodeSE(#c=1), NodeNW(#c=1), NodeSE(#c=1), FullNode(#c=2)]
    res66: kotlin.String = >>>

    
    
    
    
    println(getNodes(arrayOf("\\ ",
                             "  ")))

    [NodeNE(#c=1), NodeSW(#c=1), FullNode(#c=2), FullNode(#c=2), FullNode(#c=2)]
    res68: kotlin.String = >>>

Ok, this looks right. Now we have only to count the number of fully interconnected nodes. We do that by navigating from each node to finding all navigable ones from there. The amount of times we **start** on a node that has not been visited is the amount of non-interconnected graphs we have. I like using a generator as a sort of "multipurpose" version of this operation. It will yield back a node for each graph as in a bidirectionally-connected structure like this, any node in a graph can be considered the "root".

    fun getNonInterconnectedGraphs(nodes: Iterable<Node>) : Sequence<Node> = sequence {
        var visited: MutableSet<Node> = mutableSetOf()
    
        fun visit(node: Node) {
            if(visited.contains(node))
                return
            visited.add(node)
            for(n in node.children.asIterable())
                visit(n)
        }
        for(n in nodes) {
            if(!visited.contains(n))
                yield(n)
            visit(n)
        }
    }

Putting it all together

    
    
    
    
    
    fun countSlashDelineatedRegions(input: Array<String>): Int {
        return getNonInterconnectedGraphs(getNodes(input)).toList().size
    }

    
    println(countSlashDelineatedRegions(arrayOf(" /",
                                                "/ ")))

    2
    res88: kotlin.String = >>>

    
    println(countSlashDelineatedRegions(arrayOf(" /",
                                                "  ")))

    1
    res90: kotlin.String = >>>

    
    println(countSlashDelineatedRegions(arrayOf("/\\",
                                                "\\/")))

    5
    res92: kotlin.String = >>>

    
    println(countSlashDelineatedRegions(arrayOf("\\/",
                                                "/\\")))

    4
    res94: kotlin.String = >>>

That's right!

A future possible evolution would be to simplify `Node` futher. The subclasses are doupled to the concept of cells and children do not need to be mutable beyond the invocation of `getNodes`. I would potentially consider creating a simplified \`GraphNode\` type and mapping each of the returned nodes to that.

