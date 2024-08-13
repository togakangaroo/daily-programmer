enum class Direction { NORTH, EAST, SOUTH, WEST }
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
fun countSlashDelineatedRegions(input: Array<String>): Int {
    return getNonInterconnectedGraphs(getNodes(input)).toList().size
}
println(countSlashDelineatedRegions(arrayOf("/\\",
                                            "\\/")))
