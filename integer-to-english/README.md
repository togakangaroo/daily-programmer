[This is a leetcode problem](https://leetcode.com/problems/integer-to-english-words/description/) posted to the underdog devs slack. I recently got laid off and I should practice

This is the actual process of me solving the problem. The final ruby-file can be viewed [here](./number_to_english.rb).


# Problem Statement

> Convert a non-negative integer num to its English words representation.

    0 <= num <= 2**31 - 1


## Example 1

Input: num = 123
Output: "One Hundred Twenty Three"


## Example 2

Input: num = 12345
Output: "Twelve Thousand Three Hundred Forty Five"


## Example 3

Input: num = 1234567
Output: "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"


# Brainstorming

What's the max here? That detemrmines how many decimal place value names I have to hard code `2147483648`. Ok, so that's just "billions", easy.

Let's see if we can just say the rules in english and I'll try to avoid saying that the right answer is just to throw it at ChatGPT.

I'm thinking about examining the number form the back forward

-   If literally 0 then say zero
-   For the ones
    -   if 1-9 then say the digit
    -   if 0 then say nothing
-   For the tens
    -   if 4, 6-9 then its the digit+ty
    -   if 5, then fifty
    -   if 3, then thirty
    -   if 2, then twenty
    -   if 0, then nothing
    -   if 1, then
        -   do not run the ones
        -   if ones place is
            -   0 then ten
            -   1 then eleven
            -   2 then twelve
            -   3 then thirteen
            -   5 then fifteen
            -   4, 6-9 then digit+teen
-   For hundres
    -   digit+hundred
-   For thousands
    -   digit+thousand
-   Tens thousands
    -   same rules as tens+thousand
-   Hundred thousands
    -   same rules as hundreds+thousand
-   Millions
    -   same as ones+million

I'm not the most clear on the more advanced numbers but I feel like if I get 0-9999 right then the rest will fall into place

I do think that maybe we need to handle the case of a two digit number together, all the exceptions are in the interactions there


# Playground

You know, I've seen ruby pop up several times in JDs I've looked at and&#x2026;I'm not a ruby guy, so like, lets do it in ruby to demenstrate that I can still sling it

Clearly I'm going to need to do pattern matching, lets see how it looks in ruby

I'm on a mac which already has ruby installed, but pattern matching in ruby got more powerful in 2.7 and the installed version is `ruby 2.6.10p210 (2022-04-12 revision 67958) [universal.arm64e-darwin23]`. I can `brew install ruby` to get latest but it doesn't symlink automatically. I'll have to explicitly call `/opt/homebrew/opt/ruby/bin/ruby` (or `irb`)

    case num
    in 0
      "zero"
    in x if 1 <= x && x <= 5
      "low"
    in x if 5 < x && x < 10
      "high"
    end

    zero

    zero

    low

    high

    low


# Implementation

Well, we'll need a way to convert just flat out digits to english, right? But for our needs we never say "zero" (except literally for 0), you just ignore it

    def digit_to_english(digit)
      case digit
      in "0"
        ""
      in "1"
        "one"
      in "2"
        "two"
      in "3"
        "three"
      in "4"
        "four"
      in "5"
        "five"
      in "6"
        "six"
      in "7"
        "seven"
      in "8"
        "eight"
      in "9"
        "nine"
      end
    end

    
    
    digit_to_english "4"

    four

Now lets try to do two digits

    def two_digits_to_english(digits)
      case digits
      in [d]
        digit_to_english d
      in ["0", "0"]
        ""
      in ["0", d]
        digit_to_english d
      in ["1", "0"]
        "ten"
      in ["1", "1"]
        "eleven"
      in ["1", "2"]
        "twelve"
      in ["1", "3"]
        "thirteen"
      in ["1", "5"]
        "fifteen"
      in ["1", d]
        "#{digit_to_english d}teen"
      in ["2", d]
        "twenty #{digit_to_english d}"
      in ["3", d]
        "thirty #{digit_to_english d}"
      in ["5", d]
        "fifty #{digit_to_english d}"
      in ["8", d]
        "eighty #{digit_to_english d}"
      in [d1, d2]
        "#{digit_to_english d1}ty #{digit_to_english d2}"
      end
    end

    
    
    
    [0, 4, 12, 16, 25, 36, 50, 99].map { |n| (two_digits_to_english (n.to_s.split "")) }

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">four</td>
<td class="org-left">twelve</td>
<td class="org-left">sixteen</td>
<td class="org-left">twenty five</td>
<td class="org-left">thirty six</td>
<td class="org-left">fifty</td>
<td class="org-left">ninety nine</td>
</tr>
</tbody>
</table>

woah look at that, it worked!

Ok, so now we're getting to understand the rest of the pattern. First of all, I'll observe that we can use `two_digits_to_english` with single digit numbers too, so lets alias it to `dte` and use that as much as possible

-   for a 3 digit number its `(dte d1) hundred (dte d23)` we'll alias this `3dte`
-   for a 4 digit number its `(dte d1) thousand (3dte d234)`
-   for a 5 digit number its `(dte d12) thousand (3dte d345)`
-   for a 6 digit number its `(3dte d123) thousand (3dte d456)` we'll alias this to 6dte
-   for a 7 digit number its `(dte d1) million (6dte d234567)`
-   for a 8 digit number its `(dte d12) million (6dte d345678)`
-   for a 9 digit number its `(3dte d123) million (6dte d456789)` - we'll alias this to 9dte
-   for a 10 digit number its `(dte d1) billion (9dte d234567890)`

Ok, so its becoming clear that it might be useful for `dte` to be able to handle 3 digits, that would simplify things

    def three_digits_to_english(digits)
      case digits
      in x if x.length <= 2
        two_digits_to_english x
      in ["0", *d23]
        two_digits_to_english d23
      in [d1, *d23]
        "#{two_digits_to_english [d1]} hundred #{two_digits_to_english d23}".strip
      end
    end

    
    
    
    
    [0, 4, 12, 99, 100, 145, 232, 911].map { |n| (three_digits_to_english (n.to_s.split "")) }

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />

<col  class="org-left" />
</colgroup>
<tbody>
<tr>
<td class="org-left">&#xa0;</td>
<td class="org-left">four</td>
<td class="org-left">twelve</td>
<td class="org-left">ninety nine</td>
<td class="org-left">one hundred</td>
<td class="org-left">one hundred fourty five</td>
<td class="org-left">two hundred thirty two</td>
<td class="org-left">nine hundred eleven</td>
</tr>
</tbody>
</table>

now this can be simplified to the following. Here we alias our new `three_digits_to_english` as `dte`

-   for a 4 digit number its `(dte d1) thousand (dte d234)`
-   for a 5 digit number its `(dte d12) thousand (dte d345)`
-   for a 6 digit number its `(dte d123) thousand (dte d456)` we'll alias this to 6dte
-   for a 7 digit number its `(dte d1) million (6dte d234567)`
-   for a 8 digit number its `(dte d12) million (6dte d345678)`
-   for a 9 digit number its `(dte d123) million (6dte d456789)` - we'll alias this to 9dte
-   for a 10 digit number its `(dte d1) billion (9dte d234567890)`

So now, we just know the breaks and the word associated to each of the breaks and then we do something like `(dte head..break) word rest`

Ok so lets do that. There's the question of what the structure for those breaks/word associations should look like. While we could do an array or a hash, because we're always processing it from highest break to lowest I think the best approach is more like a linked list as it can be unrolled more easily. Quick google tells me Ruby has one-line structs that can be used for this. Note that we have special handling for "hundreds and below" already so no need to go lower

    PlaceName = Struct.new(:place, :name, :next)
    ALL_PLACE_NAMES = PlaceName.new(10, "billion",
                       PlaceName.new(7, "million",
                        PlaceName.new(4, "thousand")))

Note the capitalization here is interesting. I got stuck on it for a bit. In ruby - unlike other languages - all caps matters for making your variable visible down the scope chain

We're almost there, we can now unroll this across all our digits

There's one gocha here, in that if the next set of digits are all 0, then we don't want to say anything. This will allow us to handle situations like `10000` recursively without saying the "hundred" that you **would** say if you've got a number like `100` or `10100`

    def many_digits_to_english(digits, place_name)
      if digits.all? { |d| d == "0" } # the hundreds in 1000
        ""
      elsif not place_name # terminal condition and when 3 digit or lower
        three_digits_to_english digits
      elsif digits.length < place_name.place # when not in the billions and need to get down to the place name that matters
        many_digits_to_english(digits, place_name.next)
      else
        split_at = digits.length - place_name.place
        place_digits = digits[0..split_at]
        rest_digits = digits[(split_at + 1)..-1]
        if place_digits.all? { |d| d == "0" } # situations like 1000001
          many_digits_to_english(rest_digits, place_name.next)
        else # normal case
          "#{three_digits_to_english place_digits} #{place_name.name} #{many_digits_to_english(rest_digits, place_name.next)}"
        end
      end
    end

Now we just have to do the splitting of digits. Oh, and handle zero

    def number_to_english(num)
      if num == 0
        "zero"
      else
        many_digits_to_english(num.to_s.split(""), ALL_PLACE_NAMES).strip
      end
    end

And put it all together

lets test it out. 

    
    
    [0, 4, 12, 99, 100, 911, 1000, 10001, 100000, 1000001, 1000000000, 2000000011].each { |n| puts "#{n}, #{(number_to_english n)}" }

    0, zero
    4, four
    12, twelve
    99, ninety nine
    100, one hundred
    911, nine hundred eleven
    1000, one thousand
    10001, ten thousand one
    100000, one hundred thousand
    1000001, one million one
    1000000000, one billion
    2000000011, two billion eleven

I've also tangled the file so the full ruby-only can be viewed [here](./number_to_english.rb).

