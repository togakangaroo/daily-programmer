
# Table of Contents

1.  [Problem Statement](#orgf607838)
    1.  [Example:](#org86ea130)
2.  [Brainstorming](#org3098584)
3.  [Python Implementation](#orgf45a25f)
4.  [Emacs Lisp Implementation](#orgbe37e9b)
5.  [Go Implementation](#org89db21a)

This one is a little different because it is a problem I myself came up with. Asking AI about it, it seems like what I describe here is similar to problems in leetcode and elsewhere known as "k-sum", though I think this formulation is a bit different. I'm not even sure that this doesn't have a much easier solution, but running through it, it's not obvious


<a id="orgf607838"></a>

# Problem Statement

Given a range of numbers $ [1,N] $ and a sum `S`, what are all sets of `K` numbers from the range (without replacement) that add up to `S`?


<a id="org86ea130"></a>

## Example:

-   Of the range `[1,3]`, $ K=2 $ and $ S=4 $ you have only the single-element set `{(1 3)}`
-   Of the range `[1,4]`, $ K=2 $ and $ S=5 $ you have the set `{(1 4) (2 3)}`
-   Of the range `[1,5]`, $ K=3 $ and $ S=7 $ you have again a single-element set `{(1 2 4)}`. No other combinations of three numbers from this range work.
-   Of the range `[1,7]`, $ K=3 $ and $ S=10 $ you have the set `{(1 2 7) (1 3 6) (1 4 5) (2 3 5)}`


<a id="org3098584"></a>

# Brainstorming

Lets just chart out a bunch of examples and see what patterns we see. How do you pick subsets from a range anyways?

-   Of the range `[1,5]`, $ K=3 $

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">3</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">4</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">5</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-right">4</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-right">5</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">4</td>
<td class="org-right">5</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">4</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">5</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">4</td>
<td class="org-right">5</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">4</td>
<td class="org-right">5</td>
</tr>
</tbody>
</table>

I think that's all the combinations? So the trick was basically to increase the rightmost column starting with one more than the number to the left. Once you hit five, you increment the number to the left and start again

Now do that and layer over the sum thing which determines what the third number should be

-   Of the range `[1,7]`, $ K=3 $ and $ S=10 $

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-left">7</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-left">6</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">4</td>
<td class="org-left">5</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">5</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">6</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">7</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-left">5</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">4</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">5</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">4</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">5</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">6</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-right">4</td>
<td class="org-right">5</td>
<td class="org-left">-</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">6</td>
<td class="org-left">&#xa0;</td>
</tr>

<tr>
<td class="org-right">6</td>
<td class="org-right">7</td>
<td class="org-left">&#xa0;</td>
</tr>
</tbody>
</table>

Lets do one more

-   Of the range `[1,9]`, $ K=3 $ and $ S=15 $

In the table below, a blank in the third column indicates that the options for the current run have been exhausted, whereas a dash that the only way to resolve it is with a duplicate

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">12</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-right">11</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">4</td>
<td class="org-right">10</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">5</td>
<td class="org-right">9</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">6</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">7</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">10</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">4</td>
<td class="org-right">9</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">5</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">6</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">7</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">4</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">5</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">6</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">4</td>
<td class="org-right">5</td>
<td class="org-right">6</td>
</tr>

<tr>
<td class="org-right">4</td>
<td class="org-right">6</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">6</td>
<td class="org-right">-</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">7</td>
<td class="org-right">-</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">8</td>
<td class="org-right">-</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">9</td>
<td class="org-right">-</td>
</tr>

<tr>
<td class="org-right">6</td>
<td class="org-right">7</td>
<td class="org-right">-</td>
</tr>

<tr>
<td class="org-right">6</td>
<td class="org-right">8</td>
<td class="org-right">-</td>
</tr>
</tbody>
</table>

-   If you cannot place a digit because it would equal or exceed with the prevopis (eg `(1 7 7)` or `(2 7 6)`) then no point decrementing further as it would have already been covered higehr up on the list
    
    What if $ S=14 $?

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">11</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-right">10</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">4</td>
<td class="org-right">9</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">5</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">6</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">7</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">9</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">4</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">5</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">6</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">4</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">5</td>
<td class="org-right">6</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">6</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">4</td>
<td class="org-right">5</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">6</td>
<td class="org-right">-</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">7</td>
<td class="org-right">-</td>
</tr>

<tr>
<td class="org-right">5</td>
<td class="org-right">8</td>
<td class="org-right">-</td>
</tr>

<tr>
<td class="org-right">6</td>
<td class="org-right">7</td>
<td class="org-right">-</td>
</tr>
</tbody>
</table>

oh that does look like a sort of pattern, we lost a set from the second and fourth groupings. If $ S=13 $ I can see that first grouping would lose 1 more set

Lets try that again but with $ S=15, K=4 $

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">9</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">4</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">5</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">6</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-right">4</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-right">5</td>
<td class="org-right">6</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-right">6</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">4</td>
<td class="org-right">6</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">5</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">4</td>
<td class="org-right">5</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">5</td>
<td class="org-right">6</td>
<td class="org-right">&#xa0;</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">4</td>
<td class="org-right">5</td>
<td class="org-right">&#xa0;</td>
</tr>
</tbody>
</table>

Ah, so look, once we can no longer have the numbers be increasing, we should go on to the next line

There **is** something recursive here. For example if I have $ S=15, K=4 $

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-left">?</td>
<td class="org-left">?</td>
<td class="org-left">?</td>
</tr>
</tbody>
</table>

The question marks are the same as $ S=14, K=3 $ when `start_at=2`

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-right">2</td>
<td class="org-left">?</td>
<td class="org-left">?</td>
</tr>
</tbody>
</table>

Which is the same as $ S=12,K=2 $ when `start_at=3`

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-right">3</td>
<td class="org-left">?</td>
</tr>
</tbody>
</table>

Which is the same as $ S=9,K=1 $ and `start_at` doesn't matter

Lets see if I can actually implement this


<a id="orgf45a25f"></a>

# Python Implementation

    def get_lowest_incrementing_addends(lowest_first_number: int, k: int, desired_sum: int):
        assert 1<=k
        assert 0<desired_sum
    
        if desired_sum < lowest_first_number:
            return
    
        if k==1:
            yield desired_sum
            return
    
        yield lowest_first_number
    
        yield from get_lowest_incrementing_addends(lowest_first_number+1, k-1, desired_sum-lowest_first_number)

Lets test that

    print(list(get_lowest_incrementing_addends(1, 4, 15)))
    print(list(get_lowest_incrementing_addends(2, 4, 15)))
    print(list(get_lowest_incrementing_addends(2, 3, 15)))

    [1, 2, 3, 9]
    [2, 3, 4, 6]
    [2, 3, 10]

ok so I think that getting "all" should be similar, you just iterate upwards and spread out

    from typing import Iterator
    
    type SetOfAddends = tuple[int]
    
    def get_incrementing_addends(lowest_first_number: int, upper_bound: int, k: int, desired_sum: int) -> Iterator[SetOfAddends]:
        assert 1<=k, "K must be positive"
    
        if desired_sum <= 0:
            return
    
        if  upper_bound <= lowest_first_number:
            return
    
        if desired_sum < lowest_first_number:
            return
    
        if k==1:
            yield (desired_sum, )
            return
    
        for new_lowest_first_number in range(lowest_first_number, upper_bound):
            for addends in get_incrementing_addends(new_lowest_first_number+1, upper_bound, k-1, desired_sum-new_lowest_first_number):
                yield (new_lowest_first_number,)+ addends

    print(list(get_incrementing_addends(1, 9, 3, 15)))
    print(list(get_incrementing_addends(1, 9, 4, 15)))

    [(1, 2, 12), (1, 3, 11), (1, 4, 10), (1, 5, 9), (1, 6, 8), (2, 3, 10), (2, 4, 9), (2, 5, 8), (2, 6, 7), (3, 4, 8), (3, 5, 7), (4, 5, 6)]
    [(1, 2, 3, 9), (1, 2, 4, 8), (1, 2, 5, 7), (1, 3, 4, 7), (1, 3, 5, 6), (2, 3, 4, 6)]

Oh snap, I think that worked!

I do suspect that some further optimization is possible, it certainly is not necessary for that final loop to run all the way up to `upper_bound`, but those branches would teriminate rapidly either way so I'm not concerned


<a id="orgbe37e9b"></a>

# Emacs Lisp Implementation

I know no one cares about my abilities to code in lisp, but I do enjoy it even if the emacs flavor is not my favorite, lets just do one of those really quick. Plus, its good experience using cl-loop which I like a lot

    (require 'generator)
    
    (iter-defun gim/get-incrementing-addends (lowest-first-number upper-bound k desired-sum)
      (cl-assert (when (<= 1 k) 't) nil "k must be positive")
      (when (and (< 0 desired-sum)
                 (< lowest-first-number upper-bound)
                 (<= lowest-first-number desired-sum))
        (if (= k 1)
            (iter-yield (list desired-sum))
          (cl-loop for new-lowest from lowest-first-number to upper-bound
                   do (cl-loop for addends iter-by (gim/get-incrementing-addends (+ 1 new-lowest) upper-bound (- k 1) (- desired-sum new-lowest))
                               do (iter-yield (cons new-lowest addends)))))))
    
    (cl-loop for addends iter-by (gim/get-incrementing-addends 1 9 3 15)
             collect addends)

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">12</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
<td class="org-right">11</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">4</td>
<td class="org-right">10</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">5</td>
<td class="org-right">9</td>
</tr>

<tr>
<td class="org-right">1</td>
<td class="org-right">6</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">10</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">4</td>
<td class="org-right">9</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">5</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">6</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">4</td>
<td class="org-right">8</td>
</tr>

<tr>
<td class="org-right">3</td>
<td class="org-right">5</td>
<td class="org-right">7</td>
</tr>

<tr>
<td class="org-right">4</td>
<td class="org-right">5</td>
<td class="org-right">6</td>
</tr>
</tbody>
</table>

Nice! I really like lisps&#x2026;


<a id="org89db21a"></a>

# Go Implementation

I've been poking at Go lately and while it doesn't have generators it has channels which are a similar use case

    package main
    
    import "fmt"
    
    func getIncrementingAddends(lowestFirstNumber, upperBound, k, desiredSum int) <-chan []int {
      resultChan := make(chan []int)
    
      go func() {
        defer close(resultChan)
    
        if k <= 0 {
          panic("K must be positive")
        }
    
        if desiredSum <= 0 || upperBound <= lowestFirstNumber || desiredSum < lowestFirstNumber {
          return
        }
    
        if k == 1 {
          if desiredSum <= upperBound {
            resultChan <- []int{desiredSum}
          }
          return
        }
    
        for newLowestFirstNumber := lowestFirstNumber; newLowestFirstNumber < upperBound; newLowestFirstNumber++ {
          resultsToTheRightChan := getIncrementingAddends(newLowestFirstNumber+1, upperBound, k-1, desiredSum-newLowestFirstNumber,)
    
          for subResult := range resultsToTheRightChan {
            result := append([]int{newLowestFirstNumber}, subResult...)
            resultChan <- result
          }
        }
      }()
    
      return resultChan
    }
    
    func main() {
      for addends := range getIncrementingAddends(1, 9, 3, 15) {
        fmt.Println(addends)
      }
    }

    [1 5 9]
    [1 6 8]
    [2 4 9]
    [2 5 8]
    [2 6 7]
    [3 4 8]
    [3 5 7]
    [4 5 6]

