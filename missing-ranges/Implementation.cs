IEnumerable<string> MissingRanges(int lower, int upper, IEnumerable<int> nums) {
    var current = lower;
    foreach(var num in nums){
        if(current < num) {
            if(current + 1 == num)
                yield return $"{current}";
            else
                yield return $"{current}->{num-1}";
            current = num;
        } else
            current += 1;
    }
    if(current == upper)
        yield return $"{current}";
    else if (current < upper)
        yield return $"{current}->{upper}";
}

IEnumerable<int> nums = Args[0].Split("\n").Select(n => Int32.Parse(n));
var (lower, upper) = (Int32.Parse(Args[1]), Int32.Parse(Args[2]));
Console.WriteLine(String.Join(", ", MissingRanges(lower, upper, nums)));
