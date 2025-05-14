// Simple Implementation
// Ok lets do it based on the deeper insight above. It becomes quite simple


// [[file:README.org::*Simple Implementation][Simple Implementation:1]]
package main



import (
  "fmt"
  "slices"
)

func isArithmeticProgression(array []int) bool {
  if len(array) <= 2 {
    return true
  }

  sortedArray := slices.Clone(array)
  slices.Sort(sortedArray)

  prevItem := sortedArray[1]
  prevGap := prevItem - sortedArray[0]

  for _, item := range sortedArray[2:] {
    newGap := item - prevItem
    if newGap != prevGap {
      return false
    }
    prevGap = newGap
    prevItem = item
  }

  return true
}

func main() {
  fmt.Println(isArithmeticProgression([]int{3, 5, 1}))
  fmt.Println(isArithmeticProgression([]int{1, 2, 4}))
}
// Simple Implementation:1 ends here
