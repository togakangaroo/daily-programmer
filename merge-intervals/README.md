This is a [leetcode](https://leetcode.com/problems/merge-intervals/description/) [posted to](https://rands-leadership.slack.com/archives/CEX9Y74DB/p1724196987741039?thread_ts=1724195920.502929&cid=CEX9Y74DB) the Rands Leadership Slack


# Problem Statement

Given an array of intervals where `intervals[i] = [start[i], end[i]]`, merge all overlapping intervals, and return the shortest array possible representing the, non-overlapping intervals that cover all the intervals in the input.


## Example 1

[1,3]\*Input\*:

`intervls`

<table id="org1e6baac" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">3</td>
</tr>

<tr>
<td class="org-right">8</td>
<td class="org-right">10</td>
</tr>

<tr>
<td class="org-right">2</td>
<td class="org-right">6</td>
</tr>

<tr>
<td class="org-right">15</td>
<td class="org-right">18</td>
</tr>
</tbody>
</table>

**Output**:

<table id="org8750a0c" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">6</td>
</tr>

<tr>
<td class="org-right">8</td>
<td class="org-right">10</td>
</tr>

<tr>
<td class="org-right">15</td>
<td class="org-right">18</td>
</tr>
</tbody>
</table>

**Explanation**: Since intervals `[1,3]` and `[2,6]` overlap, merge them into `[1,6]`.


## Example 2:

**Input**:

<table id="org0364737" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">4</td>
</tr>

<tr>
<td class="org-right">4</td>
<td class="org-right">5</td>
</tr>
</tbody>
</table>

**Output**:

<table id="orgc1a576b" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">5</td>
</tr>
</tbody>
</table>

**Explanation**: Intervals `[1,4]` and `[4,5]` are considered overlapping.


## Constraints

-   `1 <= intervals.length <= 10^4`
-   `intervals[i].length == 2`
-   `0 <= start[i] <= end[i] <= 10^4`


# Brainstorming

Well first of all, the second half of the question is a red herring. If you've merged all overlapping intervals, then what remains is the smallest set of non-overlapping intervals that covers all

So really this is just about merging intervals which is easy enough. First sort by start, then move through the list one at a time merging intervals until your each a gap between the current end and next next start


# Implementation


## In Python

    def merge_intervals(intervals):
        sorted_by_start = iter(sorted(intervals, key=lambda t: t[0]))
        current_start, current_end = next(sorted_by_start)
    
        for next_start, next_end in sorted_by_start:
            if current_end < next_start:
                yield (current_start, current_end)
                current_start, current_end = next_start, next_end
            else:
                current_end = next_end
    
        yield (current_start, current_end)
    
    return list(merge_intervals(intervals))

Run it on example-1

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">6</td>
</tr>

<tr>
<td class="org-right">8</td>
<td class="org-right">10</td>
</tr>

<tr>
<td class="org-right">15</td>
<td class="org-right">18</td>
</tr>
</tbody>
</table>

Run it on example-2

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">1</td>
<td class="org-right">5</td>
</tr>
</tbody>
</table>

It works!

