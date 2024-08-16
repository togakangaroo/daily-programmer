
# Table of Contents

1.  [Problem Statement](#orged2bee2)
    1.  [Example 1:](#org3154d70)
    2.  [Example 2:](#orgfc9f328)
    3.  [Constraints:](#org8833c88)
2.  [Brainstorming](#orgc162afa)
3.  [Implementation](#orge53d3b7)

This is a [leetcode problem](https://leetcode.com/problems/lemonade-change/description/) that was done in the [UnderdogDevs slack](https://underdog-devs.slack.com/archives/C02FFHZT200/p1723684246585919)


<a id="orged2bee2"></a>

# Problem Statement

At a lemonade stand, each lemonade costs $5. Customers are standing in a queue to buy from you and order one at a time (in the order specified by bills). Each customer will only buy one lemonade and pay with either a $5, $10, or $20 bill. You must provide the correct change to each customer so that the net transaction is that the customer pays $5.

Note that you do not have any change in hand at first.

Given an integer array bills where bills[i] is the bill the ith customer pays, return true if you can provide every customer with the correct change, or false otherwise.


<a id="org3154d70"></a>

## Example 1:

-   **Input:** `bills = [5,5,5,10,20]`
-   **Output:** `true`
-   **Explanation:** -   From the first 3 customers, we collect three $5 bills in order.
    -   From the fourth customer, we collect a $10 bill and give back a $5.
    -   From the fifth customer, we give a $10 bill and a $5 bill.
    -   Since all customers got correct change, we output true.


<a id="orgfc9f328"></a>

## Example 2:

-   **Input:** `bills = [5,5,10,10,20]`
-   **Output:** `false`
-   **Explanation:** -   From the first two customers in order, we collect two $5 bills.
    -   For the next two customers in order, we collect a $10 bill and give back a $5 bill.
    -   For the last customer, we can not give the change of $15 back because we only have two $10 bills.
    -   Since not every customer received the correct change, the answer is false.


<a id="org8833c88"></a>

## Constraints:

-   `1 <= bills.length <= 10000`
-   `bills[i]` is either `5, 10, or 20`.


<a id="orgc162afa"></a>

# Brainstorming

I actually don't think there's any way to do it other than just iterating once thorugh. It's just a reduce. The one thing that makes it not **quite** a reduce is that you can return early if say the 4th person out of 50 cannot get proper change then we should stop iterating.

Another thought is do the bills you actually have in your bank matter or do they not at the current denominations? Some observations:

-   The first bill **has** to be a 5 or this doesn't work, you won't be able to give change
-   Once you have a 5, the second one can be a 5 or a 10, it cannot be a 20
-   You cannot have a 20 until you have 3 5s or a 5 and a 10. If you have both, always give the latter.

So really the only decision point you have is in the latter, and there is always a right answer (the most flexible one)

This also points the way to a - probably unnecessary - optimization. If you ever end up in a situtaion where you don't have a 5 and there are still people in line, you're boned, nothing you can do.

So does that mean that the actual bills you have can practically speaking matter? I think so

-   `5 5 5 20 10` doesn't work, before the last person you are holding $20 but no way to give change to a 10
-   `5 5 5 5 10` is perfectly fine however even though you still have $20 before

I'm not convinced that the number of 10s or 20s matters, but the total number of 5s definitely does, and so does the size of the bank of course. If we simply track each of the 3 denominations separately that certainly works as well. Actually there is no way to give a 20 as change, so tracking them doesn't matter either


<a id="orge53d3b7"></a>

# Implementation

I like lisp, I'm in emacs. Let's just do Emacs Lisp. I need to practice the loop facility macro

    (cl-loop
     with bank5 = 0
     with bank10 = 0
     for bill in bills
     do (pcase bill
          (5 (setq bank5 (1+ bank5)))
          (10 (setq bank5 (1- bank5))
              (setq bank10 (1+ bank10)))
          (20 (cond ((< 0 bank10) (setq bank10 (1- bank10))
                                  (setq bank5 (1- bank5)))
                    (t (setq bank5 (0 bank5 3))))))
      always (and (<= 0 bank5)
                  (<= 0 bank10))) ; I don't even think this one is necessary but not sure.

Lets try it with example 1

    t

Now example 2

    nil

Yay. I like the looping facility macro a lot!

