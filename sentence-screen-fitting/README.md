
# Table of Contents

1.  [Sentence Screen Fitting](#org34aa856)
    1.  [Problem Statement](#orgb69f05b)
    2.  [Examples](#orga03529f)
    3.  [Helpful Utilities](#orge72ab12)
    4.  [Putting it all together](#org0ad1503)


<a id="org34aa856"></a>

# Sentence Screen Fitting


<a id="orgb69f05b"></a>

## Problem Statement

-   [On the OpCode Slack](https://operation-code.slack.com/archives/C7JMZ5LAV/p1587638845186400)

> Given a rows x cols screen and a sentence represented by a list of non-empty words, find how many times the given sentence can be fitted on the screen.
> Note:
> A word cannot be split into two lines.
> The order of words in the sentence must remain unchanged.
> Two consecutive words in a line must be separated by a single space.
> Total words in the sentence won’t exceed 100.
> Length of each word is greater than 0 and won’t exceed 10.
> 1 ≤ rows, cols ≤ 20,000.
> 
> Example 2:
> Input:
> rows = 3, cols = 6, sentence = ["a", "bcd", "e"]
> Output:
> 2
> Explanation:
> a-bcd-
> e-a&#x2014;
> bcd-e-
> The character '-' signifies an empty space on the screen.


<a id="orga03529f"></a>

## Examples

<table id="org5229d1b" border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-left" />

<col  class="org-right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="org-right">rows</th>
<th scope="col" class="org-right">columns</th>
<th scope="col" class="org-left">sentence</th>
<th scope="col" class="org-right">output</th>
</tr>
</thead>

<tbody>
<tr>
<td class="org-right">2</td>
<td class="org-right">8</td>
<td class="org-left">hello world</td>
<td class="org-right">1</td>
</tr>


<tr>
<td class="org-right">3</td>
<td class="org-right">6</td>
<td class="org-left">a bcd e</td>
<td class="org-right">2</td>
</tr>


<tr>
<td class="org-right">4</td>
<td class="org-right">5</td>
<td class="org-left">I had apple pi</td>
<td class="org-right">1</td>
</tr>
</tbody>
</table>


<a id="orge72ab12"></a>

## Helpful Utilities

I havent done of these in javascript in a while. Also, I'm doing a talk [on javascript generators soon](https://twitter.com/WWCodeFrontEnd/status/1252996198484582402?s=20) and you **know** I'm going to want to use them here, so lets do it.

Since we're going to be using cycles of our sentences here, a method that can cycle forever would be useful

        const cycle = function * (collection) {
            while(true) {
                for(const x of collection)
                    yield x
            }
        }
        const letters = `abcdefg`
    
    const it = cycle(letters)[Symbol.iterator]()
    for(let i=0; i < 25; i+=1, it.next()) {}
    return it.next().value

    e

This is cool, but we to actually know what cycle we're in too

        const cycleCount = function * (collection) {
            let cycles = 0
            while(true) {
                for(const x of collection)
                    yield cycles
                cycles += 1
            }
        }
        const letters = `abcdefg`
    
    const it = cycleCount(letters)[Symbol.iterator]()
    for(let i=0; i < 25; i+=1, it.next()) {}
    return it.next().value

    3

And we can combine these by zipping, which is handy

        const cycle = function * (collection) {
            while(true) {
                for(const x of collection)
                    yield x
            }
        }
    
        const cycleCount = function * (collection) {
            let cycles = 0
            while(true) {
                for(const x of collection)
                    yield cycles
                cycles += 1
            }
        }
    
        const zip = function * (...collections) {
            if(!collections.length)
                return
            const iterators = collections.map(x => x[Symbol.iterator]())
            while(true) {
                const nexts = iterators.map(i => i.next())
                if(nexts.some(x => x.done))
                    return
                yield nexts.map(x => x.value)
            }
        }
    
    const letters = `abcdefg`
    
    const it = zip(cycle(letters), cycleCount(letters))[Symbol.iterator]()
    for(let i=0; i < 25; i+=1, it.next()) {}
    return it.next().value

[ 'e', 3 ]

Cool!


<a id="org0ad1503"></a>

## Putting it all together

So now the plan can become to create an iterator for our words, and then move through it one word at a time, eating up the space remaining on each column and then outputting the final cycle.

        const cycle = function * (collection) {
            while(true) {
                for(const x of collection)
                    yield x
            }
        }
    
        const cycleCount = function * (collection) {
            let cycles = 0
            while(true) {
                for(const x of collection)
                    yield cycles
                cycles += 1
            }
        }
    
        const zip = function * (...collections) {
            if(!collections.length)
                return
            const iterators = collections.map(x => x[Symbol.iterator]())
            while(true) {
                const nexts = iterators.map(i => i.next())
                if(nexts.some(x => x.done))
                    return
                yield nexts.map(x => x.value)
            }
        }
    
    const countCyclesForFitting = (rows, columns, words) => {
        const it = zip(cycle(words), cycleCount(words))[Symbol.iterator]()
        let {value: [currentWord, cycleNum]} = it.next()
        for(let r=0; r<rows; r++) {
            let spaceLeftInRow = columns
            while(spaceLeftInRow >= currentWord.length) {
                spaceLeftInRow -= (currentWord.length + 1) //+1 for the space that follows
                {[currentWord, cycleNum] = it.next().value} //putting this in a block since otherwise omitting the semi-colon above breaks things
            }
        }
        return cycleNum
    }
    
    return examples.map((example) => {
        const [rows, columns, phrase, expected] = example
        return [...example, countCyclesForFitting(rows, columns, phrase.split(` `))]
    })

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="org-right" />

<col  class="org-right" />

<col  class="org-left" />

<col  class="org-right" />

<col  class="org-right" />
</colgroup>
<tbody>
<tr>
<td class="org-right">2</td>
<td class="org-right">8</td>
<td class="org-left">hello world</td>
<td class="org-right">1</td>
<td class="org-right">1</td>
</tr>


<tr>
<td class="org-right">3</td>
<td class="org-right">6</td>
<td class="org-left">a bcd e</td>
<td class="org-right">2</td>
<td class="org-right">2</td>
</tr>


<tr>
<td class="org-right">4</td>
<td class="org-right">5</td>
<td class="org-left">I had apple pi</td>
<td class="org-right">1</td>
<td class="org-right">1</td>
</tr>
</tbody>
</table>

In the above table the second to last column is the expected amount of cycles, the last is the one we got.

Looks like we got it! Woo.

