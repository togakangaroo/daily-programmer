var rows = 5
var columns = 6
var rStart = 1
var cStart = 4
data class Coordinates(val row: Int, val column: Int)


fun spiral(): Sequence<Coordinates> = sequence {
    var row = 0
    var col = 0

    yield(Coordinates(row, col))

    val ordinals = generateSequence(1) { it + 1}
    val sideSizes = ordinals.iterator()

    while (true) {
        var sideSize = sideSizes.next()
        // →
        for (n in 0 until sideSize)
            yield(Coordinates(row, ++col))
        // ↓
        for (n in 0 until sideSize)
            yield(Coordinates(++row, col))

        var nextSideSize = sideSizes.next()
        // ←
        for (n in 0 until nextSideSize)
            yield(Coordinates(row, --col))
        // ↑
        for (n in 0 until nextSideSize)
            yield(Coordinates(--row, col))
    }
}
var spiralCoordinates = spiral().map{ Coordinates(it.row+rStart, it.column+cStart)}
var onGridSpiral = spiralCoordinates.filter { it.row in 0..(rows-1) && it.column in 0..(columns-1) }
var gridInSpiralOrder = onGridSpiral.take(rows*columns)
"\n"+gridInSpiralOrder.map{ "[${it.row}, ${it.column}]"}.joinToString("\n")
