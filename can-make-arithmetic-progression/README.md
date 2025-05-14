A lot of jobs are talking about Go now, I guess lets try Go.

Pulling a problem from an old #daily-programmer post


# Problem Statement - Can make arithmetic progression from sequence

A sequence of numbers is called an arithemtic progression if the difference between any two consecutive elements is the same. Given an array of numbers `arr`. return `true` if the array can be rearranged to form an arithmetic progression. Otherwise return `false`.


## Example 1

-   **Input:** `3 5 1`
-   **Output:** `true`


## Example 2

-   **Input:** `1 2 4`
-   **Output:** `false`


## Constraints

-   `2 <= input.length <= 1000`
-   `-100 <= input[i] <= 100`


# Brainstorming


## As Streams

I mean&#x2026;you could do this DFS, I suppose. This is really a stream sort of situation

There's a stream for evaluating if a given sequence is an arithmetic progression

-   One stream that produces numbers in a given order
-   A transform that calculates deltas
-   A short circuit where if any delta is not equal to the previous one, then the whole thing returns false
-   if the stream terminates the whole thing return true

And another stream for generating all possible sequences

-   using DFS
-   if any one sequence is an arithmetic progression, then return true
-   if all sequences were checked, then return false

This actually sounds like a go routine and a go channel sort of thing

Ok so lets get a feel for channels


## Learning Go Channels

Let's grab an example from mistral.

    package main
    
    import (
      "fmt"
      "time"
    )
    
    func sendValues(c chan<- int) {
      for i := 0; i < 5; i++ {
        c <- i
        time.Sleep(100 * time.Millisecond)
      }
      close(c)
    }
    
    func receiveValues(c <-chan int) {
      for value := range c {
        fmt.Println("Received:", value)
      }
    }
    
    func arithmetic_progression() {
      ch := make(chan int, bufferSize)
      go sendValues(ch)
      receiveValues(ch)
    }

I see, so it looks like you get bufferred delivery, what happens if you call it with bufferring disabled?

Same deal, so in this case it really didn't matter, they just ran sequentially similar to javascript's `defer` behavior I imagine. I'm sure there's a way to parallelize from there. Beyond that, it is just a matter of learning some syntax.


## Essence of the problem

As I think about it more, that is quite a lot of permutations that you might have to check.

for an input of size `2` there is only up to `1` permutation to try as the answer to **all** permutations that they are, in fact, arithmetic progressions of 1.

What about for an input the size of `3`? Lets consider the possible positions

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Permutation</td>
<td class="org-left">Is AP?</td>
</tr>

<tr>
<td class="org-left">1 2 3</td>
<td class="org-left">X</td>
</tr>

<tr>
<td class="org-left">1 3 2</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">2 1 3</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">2 3 1</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">3 1 2</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-left">3 2 1</td>
<td class="org-left">X</td>
</tr>
</tbody>
</table>

So hold on&#x2026;that is a good point. If you just sort the list can it not be a simple scan to see if each subsequent delta is the same? Are there counter-examples where sorting is not the only answer?

I'm thinking about something that bounces betweens positive and negative. But no, that doesn't make sense. If you think about it, if you were to chart out any algorithmic progression it would have to have a constant, monotonic slope. But anything with negatives and positive mixed would contain not only not the same slope but a slope in the opposite direction. The same argument could be made for why it **has** to be a sorted list since an out-of-sort-order list's derivative chart could would not be monotonic.

To speak to performance, I know that in just about any language that a sort of 999 items is nearly instantaneous so even if there's further improvements possible, this approach should fit within our constraints very nicely.

So maybe the solution isn't all that perfect a fit for go channels&#x2026;we need only to sort with a builtin then walk the sorted list to see if any two are differnt


# Implementation


## Simple Implementation

Ok lets do it based on the deeper insight above. It becomes quite simple

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
    
    func arithmetic_progression() {
      fmt.Println(isArithmeticProgression([]int{3, 5, 1}))
      fmt.Println(isArithmeticProgression([]int{1, 2, 4}))
    }


## Simple implementation tests

Lets write some tests

    package main
    
    import (
      "testing"
    )
    
    func TestIsArithmeticProgression(t *testing.T) {
      testCases := []struct {
        name     string
        input    []int
        expected bool
      }{
        {"Example 1 - Valid progression", []int{3, 5, 1}, true},
        {"Example 2 - Invalid progression", []int{1, 2, 4}, false},
        {"Empty array", []int{}, true},
        {"Single element", []int{5}, true},
        {"Two elements", []int{1, 2}, true},
        {"Negative numbers", []int{-3, -1, 1}, true},
        {"Same numbers", []int{2, 2, 2, 2}, true},
      }
    
      for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
          result := isArithmeticProgression(tc.input)
          if result != tc.expected {
            t.Errorf("isArithmeticProgression(%v) = %v; want %v", tc.input, result, tc.expected)
          }
        })
      }
    }

We can then run this like this

    go test 

    PASS
    ok  	github.com/user/can-make-arithmetic-progression	0.002s


## Using channels

Ok, so hear me out, the above works just fine of course, but in other languages I would be using a generator or a stream to calculate the stream of deltas which I could then just compare one after the other, perhaps even generating another generator. With Go, the equivalent is to use channels. [Because of the semantics around closing them](https://stackoverflow.com/a/34466755/5056) hover it's not so straightforward and has higher overhead. Still, I would like to try and implement it as a learning exercise.

First some standard imports

    package main
    
    import (
      "fmt"
      "slices"
    )
    
    var _ = fmt.Printf // Just for the sake of how we're structuring things here we don't want to get an unused import error

Here there will actually be multiple channels

-   **Channel that has written into it a sorted stream of numbers**

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

We should be able to use that

    
    
    
    
    func arithmetic_progression() {
      for val := range emitSequentialNumbers([]int{3, -2, 5, 1}) {
        fmt.Println(val)
      }
    }

Sweet!

---

-   ****Channel that has written into it deltas between sequential numbers****

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

let's test that one

We should be able to use that

    
    
    
    
    
    
    func arithmetic_progression() {
      for val := range emitDeltasBetweenSequentialNumbers(emitSequentialNumbers([]int{3, -2, 5, 1})) {
        fmt.Println(val)
      }
    }

That is indeed correct

---

-   ****Signal-only channel that has written into it a signal which pops whether two sequential numbers have changed****

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

Lets test this real quick

    
    
    
    
    
    
    func main() {
      for range emitIfValueChanged(emitSequentialNumbers([]int{0, 0, 0})) {
        fmt.Println("got a change in the first loop")
      }
      for range emitIfValueChanged(emitSequentialNumbers([]int{0, 0, 1})) {
        fmt.Println("got a change in the second loop")
      }
    }

    got a change in the second loop

Aha, interesting how the `_` variable was not only not necessary here, but actually didn't work

---

Finally, lets actually create a function to return true/false here

    func IsArithmeticProgressionWithChannels(array []int) bool {
      _, changed := <-emitIfValueChanged(emitDeltasBetweenSequentialNumbers(emitSequentialNumbers(array)))
      return !changed
    }


## Channel implementation tests

Lets write some tests

    package main
    
    
    import (
      "testing"
    )
    
    func TestIsArithmeticProgressionUsingChannels(t *testing.T) {
      testCases := []struct {
        name     string
        input    []int
        expected bool
      }{
        {"Example 1 - Valid progression", []int{3, 5, 1}, true},
        {"Example 2 - Invalid progression", []int{1, 2, 4}, false},
        {"Empty array", []int{}, true},
        {"Single element", []int{5}, true},
        {"Two elements", []int{1, 2}, true},
        {"Negative numbers", []int{-3, -1, 1}, true},
        {"Same numbers", []int{2, 2, 2, 2}, true},
      }
    
      for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
          result := IsArithmeticProgressionWithChannels(tc.input)
          if result != tc.expected {
            t.Errorf("IsArithmeticProgressionWithChannels(%v) = %v; want %v", tc.input, result, tc.expected)
          }
        })
      }
    }

We can then run all our tests to make sure they still work

    go test -v

    === RUN   TestIsArithmeticProgression
    === RUN   TestIsArithmeticProgression/Example_1_-_Valid_progression
    === RUN   TestIsArithmeticProgression/Example_2_-_Invalid_progression
    === RUN   TestIsArithmeticProgression/Empty_array
    === RUN   TestIsArithmeticProgression/Single_element
    === RUN   TestIsArithmeticProgression/Two_elements
    === RUN   TestIsArithmeticProgression/Negative_numbers
    === RUN   TestIsArithmeticProgression/Same_numbers
    --- PASS: TestIsArithmeticProgression (0.00s)
        --- PASS: TestIsArithmeticProgression/Example_1_-_Valid_progression (0.00s)
        --- PASS: TestIsArithmeticProgression/Example_2_-_Invalid_progression (0.00s)
        --- PASS: TestIsArithmeticProgression/Empty_array (0.00s)
        --- PASS: TestIsArithmeticProgression/Single_element (0.00s)
        --- PASS: TestIsArithmeticProgression/Two_elements (0.00s)
        --- PASS: TestIsArithmeticProgression/Negative_numbers (0.00s)
        --- PASS: TestIsArithmeticProgression/Same_numbers (0.00s)
    === RUN   TestIsArithmeticProgressionUsingChannels
    === RUN   TestIsArithmeticProgressionUsingChannels/Example_1_-_Valid_progression
    === RUN   TestIsArithmeticProgressionUsingChannels/Example_2_-_Invalid_progression
    === RUN   TestIsArithmeticProgressionUsingChannels/Empty_array
    === RUN   TestIsArithmeticProgressionUsingChannels/Single_element
    === RUN   TestIsArithmeticProgressionUsingChannels/Two_elements
    === RUN   TestIsArithmeticProgressionUsingChannels/Negative_numbers
    === RUN   TestIsArithmeticProgressionUsingChannels/Same_numbers
    --- PASS: TestIsArithmeticProgressionUsingChannels (0.00s)
        --- PASS: TestIsArithmeticProgressionUsingChannels/Example_1_-_Valid_progression (0.00s)
        --- PASS: TestIsArithmeticProgressionUsingChannels/Example_2_-_Invalid_progression (0.00s)
        --- PASS: TestIsArithmeticProgressionUsingChannels/Empty_array (0.00s)
        --- PASS: TestIsArithmeticProgressionUsingChannels/Single_element (0.00s)
        --- PASS: TestIsArithmeticProgressionUsingChannels/Two_elements (0.00s)
        --- PASS: TestIsArithmeticProgressionUsingChannels/Negative_numbers (0.00s)
        --- PASS: TestIsArithmeticProgressionUsingChannels/Same_numbers (0.00s)
    PASS
    ok  	github.com/user/can-make-arithmetic-progression	0.002s

