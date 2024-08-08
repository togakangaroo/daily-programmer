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

PlaceName = Struct.new(:place, :name, :next)
ALL_PLACE_NAMES = PlaceName.new(10, "billion",
                   PlaceName.new(7, "million",
                    PlaceName.new(4, "thousand")))

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

def number_to_english(num)
  if num == 0
    "zero"
  else
    many_digits_to_english(num.to_s.split(""), ALL_PLACE_NAMES).strip
  end
end

[0, 4, 12, 99, 100, 911, 1000, 10001, 100000, 1000001, 1000000000, 2000000011].each { |n| puts "#{n}, #{(number_to_english n)}" }
