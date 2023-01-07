-   [From the Operation Code Slack](https://operation-code.slack.com/archives/C7JMZ5LAV/p1673011098106419)


# Problem Statement

It is a sweltering summer day, and a boy wants to buy some ice cream bars.

At the store, there are `n` ice cream bars. You are given an array `costs` of length `n`, where `costs[i]` is the price of the `ith` ice cream bar in coins. The boy initially has `coins` coins to spend, and he wants to buy as many ice cream bars as possible.

Return the maximum number of ice cream bars the boy can buy with `coins` coins.

*Note:* The boy can buy the ice cream bars in any order.


## Example 1

<table id="org7c7d319" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Costs</td>
<td class="org-right">1 3 2 4 1</td>
</tr>


<tr>
<td class="org-left">Coins</td>
<td class="org-right">7</td>
</tr>


<tr>
<td class="org-left">Result</td>
<td class="org-right">4</td>
</tr>
</tbody>
</table>

**Explanation:** The boy can buy ice cream bars at indices `0,1,2,4` for a total price of `1 + 3 + 2 + 1 = 7`.


## Example 2

<table id="org3ff3a39" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Costs</td>
<td class="org-right">10 6 8 7 7 8</td>
</tr>


<tr>
<td class="org-left">Coins</td>
<td class="org-right">5</td>
</tr>


<tr>
<td class="org-left">Result</td>
<td class="org-right">0</td>
</tr>
</tbody>
</table>

**Explanation:** The boy cannot afford any of the ice cream bars.


## Example 3

<table id="orga38d3ff" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Costs</td>
<td class="org-right">1 6 3 1 2 5</td>
</tr>


<tr>
<td class="org-left">Coins</td>
<td class="org-right">20</td>
</tr>


<tr>
<td class="org-left">Result</td>
<td class="org-right">6</td>
</tr>
</tbody>
</table>

**Explanation:** The boy can buy all the ice cream bars for a total price of `1 + 6 + 3 + 1 + 2 + 5 = 18`.


## Constraints

-   `costs.length == n`
-   `1 <= n <= 105`
-   `1 <= costs[i] <= 105`
-   `1 <= coins <= 108`


# Analysis

This seems like it would just be a matter of sorting all costs and adding up from the bottom until we exhaust the list or exceed the sum `coins` value.

With `n` being so low (max of `105`) there's no harm of sorting the full `costs` list though it shoudl be observed that we will never need the **whole** list sorted, merely the lowest `n` values which has a different Big-O performance profile. But again, the Big-O does not matter when you have a max of `105` numbers.

I am trying to think if it is possible to not simply pick the lowest valued ice cream in order, but I believe it almost must be. After all, if we currently have an ice cream bar of value `x` selected and another `y < x` is available, we can always substitute `y` for `x` to no detriment, it can only help.


# Implementation

I've been largely doing emacs lisp lately, and I'm wrting this within Emacs, so lets do that

What I'm thinking is that once we have a `sorted-costs` (again, no need to optimize given the constraints), we just walk through that list one step after the other, totalling up the amount spent until we exceed the allotted amount of `coins`

So imagine moving down this list from left to right with `coins = 5` until the total of values in the second row exceeded this.

➡️ ➡️ ➡️ ➡️ ➡️

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-left">Sorted cost</td>
<td class="org-right">1</td>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">3</td>
<td class="org-right">4</td>
</tr>


<tr>
<td class="org-left">Running cost</td>
<td class="org-right">1</td>
<td class="org-right">2</td>
<td class="org-right">4</td>
<td class="org-right">7</td>
<td class="org-right">11</td>
</tr>


<tr>
<td class="org-left">Continue?</td>
<td class="org-right">y</td>
<td class="org-right">y</td>
<td class="org-right">y</td>
<td class="org-right">n</td>
<td class="org-right">&#xa0;</td>
</tr>
</tbody>
</table>

If you were to count the number of steps you took moving left toright you would get 3 as you should.

This seems to just be a simple loop in an iterator

    (iter-make
     (cl-loop for c in sorted-costs
              with running-total-cost = 0
              do (setq running-total-cost (+ running-total-cost c))
              if (< coins running-total-cost)
              return nil
              do (iter-yield c)
              finally return nil))

And we can test that by passing in the example tables above and evaluating things.

    (require 'generator)
    (let* ((expected (car (cdaddr data)))
           (coins (cadadr data))
           (costs (read (format "(%s)" (cadar data))))
           (sorted-costs (-sort '< costs))
           (ice-cream-bar-prices-you-can-afford
            <<iterate-sorted-costs-you-could-afford>>)
           (actual (cl-loop for x iter-by ice-cream-bar-prices-you-can-afford
                            do (princ (format "%s\n" x))
                            count 1)))
      (princ (if (equalp actual expected) "PASS" "FAIL")))

    1
    1
    2
    3
    PASS

Oh wow that seemeds to work. What about some others?

    PASS

    1
    1
    2
    3
    5
    6
    PASS

And with that, I think I've passed all the test cases. This is correct, time to just wrap it up as requested in the problem

    (require 'generator)
    (let* ((sorted-costs (-sort '< costs))
           (ice-cream-bar-prices-you-can-afford
            <<iterate-sorted-costs-you-could-afford>>))
      (cl-loop for x iter-by ice-cream-bar-prices-you-can-afford
               count 1))

    4

Yup! That works

