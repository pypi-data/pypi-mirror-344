# Snipper
A lightweight framework for removing code from student solutions.
## Installation
```console
pip install codesnipper
```
## What it does
This project address the following three challenges for administering a python-based course

 - Maintain a (working) version for debugging as well as a version handed out to students (with code missing)
 - Use LaTeX references in source code to link to course material (i.e. `\ref{mylabel}` -> *"(see equation 2.1 in exercise 5)"*)
 - Including code snippets and console output in lectures notes/exercises/beamer slides
 - Automatically create student solutions

This framework address these problems and allow you to maintain a **single**, working project repository. Below is an example of the snippets produced and included using simple `\inputminted{python}{...}` commands (see the `examples/` directory):

![LaTeX sample](https://gitlab.compute.dtu.dk/tuhe/snipper/-/raw/main/docs/latex_nup.png)

The project is currently used in **02465** at DTU. An example of student code can be found at:
 - https://gitlab.gbar.dtu.dk/02465material/02465students/blob/master/irlc/ex02/dp.py

A set of lectures notes where all code examples/output are automatically generated from the working repository can be found a
- https://lab.compute.dtu.dk/tuhe/books (see **Sequential decision making**)
 
# Usage
All examples can be found in the `/examples` directory. The idea is all our (complete) files are found in the instructor directory and snipper keeps everything up-to-date:
```text
examples/cs101_instructor  # This directory contains the (hidden) instructor files. You edit these
examples/cs101_students    # This directory contains the (processed) student files. Don't edit these
examples/cs101_output      # This contains automatically generated contents (snippets, etc.).
```
The basic functionality is you insert special comment tags in your source, such as `#!b` or `#!s` and the script then process
the sources based on the tags.  The following will show most common usages:

## The #!f-tag
Let's start with the simplest example, blocking out a function (see `examples/cs101_instructor/f_tag.py`; actually it will work for any scope)
You insert a comment like: `#!f <exception message>` like so:
```python
def myfun(a,b): #!f return the sum of a and b
    """ The doc-string is not removed. """
    sm = a+b
    return sm
```
To compile this (and all other examples) use the script `examples/process_cs101.py`
```python
if __name__ == "__main__":
    from snipper.snip_dir import snip_dir
    snip_dir("./cs101_instructor", "./cs101_students", output_dir="./cs101_output")
```
The output can be found in `examples/students/f_tag.py`. It will cut out the body of the function but leave any return statement and docstrings. It will also raise an exception (and print how many lines are missing) to help students.
```python
def myfun(a,b): 
    """ The doc-string is not removed. """
    # TODO: 1 lines missing.
    raise NotImplementedError("return the sum of a and b")
    return sm
```

## The #!b-tag
The #!b-tag allows you more control over what is cut out. The instructor file:
```python
def primes_sieve(limit):
    limitn = limit+1 #!b
    primes = range(2, limitn)
    for i in primes:
        factors = list(range(i, limitn, i))
        for f in factors[1:]:
            if f in primes:
                primes.remove(f) #!b Compute the list `primes` here of all primes up to `limit`
    return primes
width, height = 2, 4
print("Area of square of width", width, "and height", height, "is:")
print(width*height) #!b #!b Compute and print area here
print("and that is a fact!")
```
Is compiled into:
```python 
def primes_sieve(limit):
    # TODO: 8 lines missing.
    raise NotImplementedError("Compute the list `primes` here of all primes up to `limit`")
    return primes
width, height = 2, 4
print("Area of square of width", width, "and height", height, "is:")
# TODO: 1 lines missing.
raise NotImplementedError("Compute and print area here")
print("and that is a fact!")
```
This allows you to cut out text across scopes, but still allows you to insert exceptions. 



## The #!s-tag
The #!s-tag is useful for making examples to include in exercises and lecture notes. The #!s (snip) tag cuts out the text between 
tags and places it in files found in the output-directory. As an example, here is the instructor file:
```python
width, height = 2, 4
print("Area of square of width", width, "and height", height, "is:") #!s
print(width*height)  #!s  # This is an example of a simple cutout
print("and that is a fact!")
print("An extra cutout") #!s #!s  # This will be added to the above cutout
def primes_sieve(limit): #!s=a # A named cutout
    limitn = limit+1
    primes = range(2, limitn)
    for i in primes: #!s=b A nested/named cutout.
        factors = list(range(i, limitn, i))
        for f in factors[1:]:
            if f in primes:
                primes.remove(f)  #!s=b
    return primes #!s=a
```
Note it allows 
 - naming using the #!s=<name> command 
 - automatically join snippets with the same name (useful to cut out details)
 - The named tags will be matched, and do not have to strictly contained in each other

This example will produce three files
`cs101_output/s_tag.py`, `cs101_output/s_tag_a.py`, and `cs101_output/s_tag_b.py` containing the output:
```python 
# s_tag.py
print("Area of square of width", width, "and height", height, "is:") 
print(width*height)  
print("An extra cutout")
```
and 
```python 
# s_tag.py
def primes_sieve(limit): 
    limitn = limit+1
    primes = range(2, limitn)
    for i in primes: #!s=b A nested/named cutout.
        factors = list(range(i, limitn, i))
        for f in factors[1:]:
            if f in primes:
                primes.remove(f)  #!s=b
    return primes
```
and finally:
```python 
# s_tag.py
    for i in primes: 
        factors = list(range(i, limitn, i))
        for f in factors[1:]:
            if f in primes:
                primes.remove(f)
```
I recommend using `\inputminted{filename}` to insert the cutouts in LaTeX. 


## The #!o-tag
The #!o-tag allows you to capture output from the code, which can be useful when showing students the expected 
behavior of their scripts. Like the #!s-tag, the #!o-tags can be named. 

As an example, Consider the instructor file
```python
if __name__ == "__main__":
    print("Here are the first 4 square numbers") #!o=a
    for k in range(1,5):
        print(k*k, "is a square")
    #!o=a
    print("This line will not be part of a cutout.")
    width, height = 2, 4 #!o=b
    print("Area of square of width", width, "and height", height, "is:")
    print(width*height)
    print("and that is a fact!") #!o=b
```
This example will produce two files `cs101_output/o_tag_a.txt`, `cs101_output/o_tag_b.txt`:
```terminal 
Here are the first 4 square numbers
1 is a square
4 is a square
9 is a square
16 is a square
```
and 
```terminal 
Area of square of width 2 and height 4 is:
8
and that is a fact!
```

## The #!i-tag
The #!i-tag allows you to create interactive python shell-snippets that can be imported using 
 the minted `pycon` environment (`\inputminted{python}{input.shell}`).
 As an example, consider the instructor file
```python
for animal in ["Dog", "cat", "wolf"]: #!i=a
    print("An example of a four legged animal is", animal) #!i=a
#!i=b
def myfun(a,b):
    return a+b
myfun(3,4) #!i=b
# Snipper will automatically insert an 'enter' after the function definition.
```
This example will produce two files `cs101_output/i_tag_a.shell`, `cs101_output/i_tag_b.shell`:
```pycon
>>> for animal in ["Dog", "cat", "wolf"]:
...     print("An example of a four legged animal is", animal)
... 
An example of a four legged animal is Dog
An example of a four legged animal is cat
An example of a four legged animal is wolf
```
and 
```pycon 
>>> def myfun(a,b):
...     return a+b
...
>>> myfun(3,4)
7
```
Note that apparently there 
 is no library for converting python code to shell sessions so I had to write it myself, which means it can properly get confused with multi-line statements (lists, etc.). On the plus-side, it will automatically insert newlines after the end of scopes. 
 My parse is also known to be a bit confused if your code outputs `...` since it has to manually parse the interactive python session and this normally indicates a new line. 

# References and citations (`\ref` and `\cite`)
One of the most annoying parts of maintaining student code is to constantly write *"see equation on slide 41 bottom"* only to have the reference go stale because slide 23 got removed. Well not anymore, now you can direcly refence anything with a bibtex or aux file!
Let's consider the following example of a simple document with a couple of references: (see `examples/latex/index.pdf`):

![LaTeX sample](https://gitlab.compute.dtu.dk/tuhe/snipper/-/raw/main/docs/index.png)

The code for this document is:
```latex
\documentclass{article}
\usepackage{url,graphics,rotating,hyperref}
\usepackage{cleveref}
\usepackage{showlabels}
\begin{document}
\section{First section}\label{sec1}
Math is hard \cite{bertsekasII,rosolia2018data,herlau}, see also \cref{eq1} and \cref{fig1}.
\begin{equation}
	2+2 = 4 \label{eq1}
\end{equation}
\begin{figure}\centering
\includegraphics[width=.8\linewidth]{br}\caption{A figure}\label{fig1}
\end{figure}
\bibliographystyle{alpha}
\bibliography{library}						
\end{document}
``` 

To use the references in code we first have to load the `references.bib` file and the `index.aux`-file and then:
 - Snipper allows you to directly insert this information using `\cite` and `\ref`
 - You can also define custom citation command which allows you to reference common sources like 
   - Lecture notes
    - Exercise sheets
    - Slides for a particular week

Let's look at all of these in turn. The file we will consider in the instructor-version looks like this: (`examples/cs101_instructor/references.py`):
```python
def myfun():
    """
    Simple aux references \ref{eq1} in \ref{sec1}.
    Simple bibtex citations: \cite{bertsekasII} and \cite[Somewhere around the middle]{herlau}
    Example of custom command (reference notes)
    > \nref{fig1}
    Other example of custom command (reference assignment)
    > \aref2{sec1}
    """
    print("See \ref{sec1}")  # Also works.
    return 42
```
Note the last parts of the file contains the special commands `\nref` (references to lecture notes) and `\aref2` (assignment 2) which I want to define. 
This can be done by changing the call to snipper as follows (`examples/process_cs101_references.py`)
```python
from snipper.snip_dir import snip_dir
from snipper.load_citations import get_aux, get_bibtex
def main():
    bibfile = get_bibtex('latex/library.bib')
    auxfile = get_aux('latex/index.aux')
    references = dict(bibtex=bibfile,
                      aux=auxfile,
                      commands=[dict(command='\\aref2', output="(Assignment 2, %s)", aux=auxfile),
                                dict(command='\\nref', output="\cite[%s]{herlau}", aux=auxfile),
                               ])
    snip_dir("./cs101_instructor", "./cs101_students", output_dir="./cs101_output", references=references)
if __name__ == "__main__":
    main()
```
And this then produce the output:
```python
"""
References:
  [Ber07] Dimitri P. Bertsekas. Dynamic Programming and Optimal Control, Vol. II. Athena Scientific, 3rd edition, 2007. ISBN 1886529302.
  [Her21] Tue Herlau. Sequential decision making. (See 02465_Notes.pdf), 2021.
"""
def myfun():
    """
    Simple aux references eq. (1) in Section 1.
    Simple bibtex citations: (Ber07) and (Her21, Somewhere around the middle)
    Example of custom command (reference notes)
    > (Her21, Figure 1)
    Other example of custom command (reference assignment)
    > (Assignment 2, Section 1)
    """
    print("See Section 1")  # Also works.
    return 42
```
Since the aux/bibtex databases are just dictionaries it is easy to join them together from different sources. 
 I have written reference tags to lecture and exercise material as well as my notes and it makes reference management very easy. 


# Partial solutions
The default behavior for code removal (#!b and #!f-tags) is to simply remove the code and insert the number of missing lines.
We can easily create more interesting behavior. The code for the following example can be found in `examples/b_example.py` and will deal with the following problem:
```python
import numpy as np  
# Implement a sieve here.
def primes_sieve(limit):
    limitn = limit+1 #!b
    primes = range(2, limitn)
    for i in primes:
        factors = list(range(i, limitn, i))
        for f in factors[1:]:
            if f in primes:
                primes.remove(f)
    return primes #!b
# Example use: print(primes_sieve(42))
```
The examples below shows how we can easily define custom functions for processing the code which is to be removed; I have not included the functions here for brevity, 
but they are all just a few lines long and all they do is take a list of lines (to be obfuscated) and return a new list of lines (the obfuscated code). 

### Example 1: Permute lines
This example simple randomly permutes the line and prefix them with a comment tag to ensure the code still compiles
```python
import numpy as np  
# Implement a sieve here.
def primes_sieve(limit):
    #             primes.remove(f)
    #         if f in primes:
    #     factors = list(range(i, limitn, i))
    # for i in primes:
    # 
    # limitn = limit+1 
    # return primes 
    # primes = range(2, limitn)
    #     for f in factors[1:]:
# Example use: print(primes_sieve(42)) 
raise NotImplementedError('Complete the above program')
```
### Example 2: Partial replacement
This example replaces non-keyword, non-special-symbol parts of the lines:
```python
import numpy as np  
# Implement a sieve here.
def primes_sieve(limit):
    # ?????? = ?????+1 
    # ?????? = ?????(2, ??????)
    # 
    # for ? in ??????:
    #     ??????? = ????(?????(?, ??????, ?))
    #     for ? in ???????[1:]:
    #         if ? in ??????:
    #             ??????.??????(?)
    # return ?????? 
# Example use: print(primes_sieve(42)) 
raise NotImplementedError('Complete the above program')
```

### Example 3: Half of the solution
The final example displays half of the proposed solution:
```python
import numpy as np  
# Implement a sieve here.
def primes_sieve(limit):
    # limitn =????????
    # primes = ran?????????????
    # 
    # for i in????????
    #     factors = list(ra??????????????????
    #     for f in f???????????
    #         if f in????????
    #             primes.r????????
    # return???????
# Example use: print(primes_sieve(42)) 
raise NotImplementedError('Complete the above program')
```


# Citing
```bibtex
@online{codesnipper,
	title={Codesnipper (0.1.0): \texttt{pip install codesnipper}},
	url={https://lab.compute.dtu.dk/tuhe/snipper},
	urldate = {2021-09-07}, 
	month={9},
	publisher={Technical University of Denmark (DTU)},
	author={Tue Herlau},
	year={2021},
}
```