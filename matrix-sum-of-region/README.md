
# Table of Contents

1.  [Matrix Sum of Region](#org4156e58)
    1.  [Problem Statement](#orgdf71e84)
    2.  [Playground](#org87dcaf0)
        1.  [String formats](#org45e2d7d)
        2.  [Hashes](#orgfcd61ed)
        3.  [Structs](#org4d7bfcc)
        4.  [Array](#orgf5888ec)
        5.  [Array Slicing](#orgbb540e7)
    3.  [Implementation](#orgaaed595)



<a id="org4156e58"></a>

# Matrix Sum of Region


<a id="orgdf71e84"></a>

## Problem Statement

[From the Operation Code #daily-programmer chat](https://operation-code.slack.com/archives/C7JMZ5LAV/p1574682267172200)

Given a matrix of integers and the top left and bottom right coordinates of a rectangular region within the matrix, find the sum of numbers falling inside the rectangle.

Example:

    #[#[1 2 3 4]
      #[5 6 7 8]
      #[9 0 1 2]]

    (struct location (column row))
    (struct region-test (start end expected-sum))
    
    (region-test (location 1 1) (location 3 2) 24)


<a id="org87dcaf0"></a>

## Playground

This section is because I am only just learning Racket. If you want to skip past me figuring this stuff out then jump to [1.3](#orgaaed595).


<a id="org45e2d7d"></a>

### String formats

[Docs](https://docs.racket-lang.org/reference/strings.html#%28part._format%29)


<a id="orgfcd61ed"></a>

### Hashes

I don't like to have just random tuples in lists - I think I should learn about hashes.

    (define h (make-hash '((a . "apple") (b . "banana"))))
    (printf "h is: ~a\n" h)
    (printf "has a: ~a, the value is: ~a\n" (dict-has-key? h 'a) (dict-ref h 'b))
    (printf "has c: ~a\n" (dict-has-key? h 'c))


<a id="org4d7bfcc"></a>

### Structs

[Docs](https://download.racket-lang.org/docs/5.1/html/guide/define-struct.html)
But I think structs are actually more natural for this

    (struct posn (x y))
    (define p (posn 139 73))
    (printf "p: ~a, prop x is: ~a\n" p (posn-x p))


<a id="orgf5888ec"></a>

### Array

[Docs](https://docs.racket-lang.org/math/array.html)
Arrays are different from lists, they seem to be&#x2026;multidimensional? Which is after all waht I want here

    (require math/array)
    (array #[#['first 'row 'data] #['second 'row 'data]])

    (require math/array)
    (build-array #(4 5) (λ (js)
                          (match-define (vector j0 j1) js)
                          (+ j0 j1)))


<a id="orgbb540e7"></a>

### Array Slicing

[Docs](https://docs.racket-lang.org/math/array_slicing.html)
So this takes an array with a [Slice Spec](https://docs.racket-lang.org/math/array_indexing.html#(form._((lib._math/array..rkt)._.Slice-.Spec))). This is multidimensional. Lets figure out the slide spec for copying out `#[#[6 7 8] #[0 1 2]]`

    (require math/array)
    (define matrix (array #[#[1 2 3 4]
                            #[5 6 7 8]
                            #[9 0 1 2]]))
    (define sliced (array-slice-ref matrix (list (:: 1 3) (:: 1 4))))
    (printf "~a\n" sliced)
    (printf "sum: ~a" (array-all-sum sliced))


<a id="orgaaed595"></a>

## Implementation

Uhh&#x2026;ok&#x2026;so with the array functions above this becomes stupid simple

    (require math/array)
    
    (struct location (column row))
    
    (define (sum-matrix matrix start end)
      (define slice-spec (list (:: (location-row start)
                                   (add1 (location-row end)))
                               (:: (location-column start)
                                   (add1 (location-column end)))))
      (define sliced (array-slice-ref matrix slice-spec))
      (array-all-sum sliced))
    
    (sum-matrix (array #[#[1 2 3 4]
                         #[5 6 7 8]
                         #[9 0 1 2]])
                (location 1 1)
                (location 3 2))

Hacha!

