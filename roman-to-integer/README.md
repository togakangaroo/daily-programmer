
# Table of Contents

1.  [Roman Numeral to Integer](#org172b201)
    1.  [Problem Statement](#org1279241)
    2.  [Glossary](#org10c2e7f)
    3.  [Ideation](#org9b0e930)
    4.  [Ruby Playground](#orgfbd84d1)
    5.  [Solution](#org4c338ea)
        1.  [Create Roman Numeral Symbol hash](#org9dd7459)
        2.  [Define `calculate_numeral_value`](#org3c6e0ba)
        3.  [Test it out](#org7eba142)


<a id="org172b201"></a>

# Roman Numeral to Integer


<a id="org1279241"></a>

## Problem Statement

[From the Operation Code #daily-programmer channel](https://operation-code.slack.com/archives/C7JMZ5LAV/p1572432071067600)

Roman numerals are represented by seven different symbols:

<table id="org7abdb19" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Symbol</th>
<th scope="col" class="org-right">Value</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">I</td>
<td class="org-right">1</td>
</tr>


<tr>
<td class="org-left">V</td>
<td class="org-right">5</td>
</tr>


<tr>
<td class="org-left">X</td>
<td class="org-right">10</td>
</tr>


<tr>
<td class="org-left">L</td>
<td class="org-right">50</td>
</tr>


<tr>
<td class="org-left">C</td>
<td class="org-right">100</td>
</tr>


<tr>
<td class="org-left">D</td>
<td class="org-right">500</td>
</tr>


<tr>
<td class="org-left">M</td>
<td class="org-right">1000</td>
</tr>
</tbody>
</table>

For example, two is written as `II` in Roman numeral, just two one's added together. Twelve is written as, `XII`, which is simply `X + II`. The number twenty seven is written as `XXVII`, which is `XX + V + II`.

Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not `IIII`. Instead, the number four is written as `IV`. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as `IX`. There are six instances where subtraction is used:

> I can be placed before V (5) and X (10) to make 4 and 9. 
> X can be placed before L (50) and C (100) to make 40 and 90. 
> C can be placed before D (500) and M (1000) to make 400 and 900.
> Given a roman numeral, convert it to an integer. Input is guaranteed to be within the range from 1 to 3999.

We should be able to get the following values (where blank means that roman numeral is invalid)

<table id="orgf48b5b6" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-left">Numeral</th>
<th scope="col" class="org-right">Value</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-left">III</td>
<td class="org-right">3</td>
</tr>


<tr>
<td class="org-left">IV</td>
<td class="org-right">4</td>
</tr>


<tr>
<td class="org-left">IX</td>
<td class="org-right">9</td>
</tr>


<tr>
<td class="org-left">MCMXCIV</td>
<td class="org-right">1994</td>
</tr>


<tr>
<td class="org-left">IIII</td>
<td class="org-right">&#xa0;</td>
</tr>


<tr>
<td class="org-left">IL</td>
<td class="org-right">&#xa0;</td>
</tr>
</tbody>
</table>


<a id="org10c2e7f"></a>

## Glossary

These are the terms as used in this document

-   **Symbol** - A single letter symbol `I`, `V`, etc
-   **Numeral Increment** - A valid combination of symbols to make a single instance that represents a "digit". Eg I, III, IV, V, but not VI


<a id="org9b0e930"></a>

## Ideation

Basic ass way of doing this. Start from left to right one symbol at a time. As you process the next symbol several things are possible

-   It is the same symbol as prev and there are < 3 in a row - add in that symbol to buffer
-   It is the next symbol of higher value from prev and there is only one symbol buffered - Add in value from buffer
-   It is a lower value symbol - Add in value from buffer and add symbol to buffer
-   It is end - add in value from buffer
-   Else - **Error**

Also, since I have a Ruby interview coming up, lets do this in Ruby


<a id="orgfbd84d1"></a>

## Ruby Playground

I'm not good with ruby so lets play with ruby

How exactly would string destructuring work?

ok, I'm seeing something really odd happen where variables inside of functions are not always always visible in an inner scope. Lets check that out.

[`define_method`](https://apidock.com/ruby/Module/define_method) [Ruby local variable is undefined - Stack Overflow](https://stackoverflow.com/a/9671368/5056) 


<a id="org4c338ea"></a>

## Solution


<a id="org9dd7459"></a>

### Create Roman Numeral Symbol hash

According to the logic in <a id="org6dc34b7"></a> we will need the ability to look up a symbol's value, the next highest symbol, and to look a symbol up by its string char

    RomanNumeralSymbol = Struct.new("RomanNumeralSymbol", :symbol, :value, :next)

We can now create instances of this and put them into a `roman_numeral_symbols` hash like we need

    rns = symbol_values.map { |(symbol, value)| RomanNumeralSymbol.new(symbol, value)}
    rns.zip(rns.drop(1)).each do |(s, n)| 
      s.next = n
    end
    roman_numeral_symbols = rns.map { |x| [x.symbol, x] }.to_h


<a id="org3c6e0ba"></a>

### Define `calculate_numeral_value`

    class CannotCreateNumeralError < Error
    end
    
    def calculate_numeral_values(numeral, roman_numeral_symbols)
      Enumerator.new do |enum|
        prev_symbol, *other_symbols = numeral.chars
        prev = roman_numeral_symbols[prev_symbol]
        buffer = [prev]
    
        define_method(:finish_buffer) do
          sum = buffer.map { |s| s.value}.reduce(0, :+)
          buffer.clear
          sum
        end
    
        other_symbols.each do |symbol_char|
          s = roman_numeral_symbols[symbol_char]
          if prev == s and buffer.length < 3 
            #eg III
            buffer.push s
          elsif prev.value < s.value and buffer.length == 1
            #eg IV
            enum.yield (s.value - prev.value)
            finish_buffer()
          elsif prev.value > s.value
            enum.yield finish_buffer()
            buffer.push s
          else
            p "prev", prev.symbol, "s", s.symbol, "buffer", buffer.map {|x| x.symbol}
            raise CannotCreateNumeralError, "This numeral cannot be processed"
          end
          prev = s
        end
        enum.yield finish_buffer()
      end
    end
    
    define_method(:calculate_numeral_value) do |numeral|
      calculate_numeral_values(numeral, roman_numeral_symbols).reduce(0, :+)
    end


<a id="org7eba142"></a>

### Test it out

    test-numeral-values.map do |(numeral, value)| 
      begin
        calculate_numeral_value(numeral)
      rescue CannotCreateNumeralError
        nil
      end
    end

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-left">III</td>
<td class="org-right">3</td>
</tr>


<tr>
<td class="org-left">IV</td>
<td class="org-right">4</td>
</tr>


<tr>
<td class="org-left">IX</td>
<td class="org-right">9</td>
</tr>


<tr>
<td class="org-left">MCMXCIV</td>
<td class="org-right">1994</td>
</tr>


<tr>
<td class="org-left">IIII</td>
<td class="org-right">&#xa0;</td>
</tr>


<tr>
<td class="org-left">IL</td>
<td class="org-right">&#xa0;</td>
</tr>
</tbody>
</table>

