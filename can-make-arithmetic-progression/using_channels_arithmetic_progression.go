// Using channels
// :PROPERTIES:
// :header-args:go+: :eval no
// :header-args:go+: :tangle using_channels_arithmetic_progression.go
// :header-args:go+: :package 'discard
// :END:

// Ok, so hear me out, the above works just fine of course, but in other languages I would be using a generator or a stream to calculate the stream of deltas which I could then just compare one after the other, perhaps even generating another generator. With Go, the equivalent is to use channels. [[https://stackoverflow.com/a/34466755/5056][Because of the semantics around closing them]] hover it's not so straightforward and has higher overhead. Still, I would like to try and implement it as a learning exercise.

// First some standard imports

// #+name: implementation/set-up

// [[file:README.org::implementation/set-up][implementation/set-up]]
package main


import (
  "fmt"
  "slices"
)

var _ = fmt.Printf // Just for the sake of how we're structuring things here we don't want to get an unused import error
// implementation/set-up ends here



// Here there will actually be multiple channels

// - *Channel that has written into it a sorted stream of numbers*

// #+name: implementation/emitSequentialNumbers

// [[file:README.org::implementation/emitSequentialNumbers][implementation/emitSequentialNumbers]]
func emitSequentialNumbers(array []int) <-chan int {
	c := make(chan int)

	go func() {
		defer close(c)
		sortedArray := slices.Clone(array)
		slices.Sort(sortedArray)

		for _, num := range sortedArray {
			c <- num
		}
	}()

	return c
}
// implementation/emitSequentialNumbers ends here



// #+RESULTS:
// : -2
// : 1
// : 3
// : 5

// Sweet!

// --------

// - **Channel that has written into it deltas between sequential numbers**

//   #+name: implementation/emitDeltasBetweenSequentialNumbers

// [[file:README.org::*Using channels][Using channels:4]]
func emitDeltasBetweenSequentialNumbers(sequentialNumbers <-chan int) <-chan int {
	c:= make(chan int)
	go func() {
		defer close(c)
		if prevItem, ok := <- sequentialNumbers; ok {
			for newItem := range sequentialNumbers {
				c <- (newItem - prevItem)
				prevItem = newItem

			}
		}
	}()
	return c
}
// Using channels:4 ends here



// #+RESULTS:
// : 3
// : 2
// : 2

// That is indeed correct

// --------

// - **Signal-only channel that has written into it a signal which pops whether two sequential numbers have changed**

// #+name: implementation/emitIfValueChanged

// [[file:README.org::implementation/emitIfValueChanged][implementation/emitIfValueChanged]]
func emitIfValueChanged[T comparable](values <-chan T) <-chan struct{} {
	c:= make(chan struct{})
	go func() {
		defer close(c)
		if firstItem, ok := <- values; ok {
			for newItem := range values {
				if(newItem != firstItem) {
					c <- struct{}{}
				}
			}
		}
	}()
	return c
}
// implementation/emitIfValueChanged ends here



// #+RESULTS:
// : got a change in the second loop

// Aha, interesting how the ~_~ variable was not only not necessary here, but actually didn't work

// ------
// Finally, lets actually create a function to return true/false here

// [[file:README.org::*Using channels][Using channels:8]]
func IsArithmeticProgressionWithChannels(array []int) bool {
	_, changed := <-emitIfValueChanged(emitDeltasBetweenSequentialNumbers(emitSequentialNumbers(array)))
	return !changed
}
// Using channels:8 ends here
