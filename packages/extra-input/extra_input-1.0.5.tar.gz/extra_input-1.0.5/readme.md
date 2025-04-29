# Extra Input
A simple helper lib with a few extra ways to get input from the user

## How to use:
``` python
import extra_input

option = extra_input.selector(["Option [1]","Option [2]"])

print(f"you selected {option}")
```

## Functions:
 * `select(options:list[str], firstLetterSelections = True) -> str`
 * `numbered_select(options:list[str], use_parens = False, roman_numerals = False) -> str`
 * `intput(text:str) -> int`
 * `float_input(text:str) -> float`
 * `custom_input(text:str, allowed:str, tellAllowed = True) -> str`

## Changelog:
 * 1.0.5:
    - Fixed a bug where PyPI didn't show this whole readme
 * 1.0.4:
    - Fixed some misc bugs
    - Fixed selector using the wrong index
    - Fixed selector using its own charecter making it more error prone
 * 1.0.0 - 1.0.3:
    - Firguring out how to make this work