import roman

def select(options:list[str], firstLetterSelections = True) -> str:
    while True:
        print("Please choose a option:")
        for option in options:
            if firstLetterSelections:
                print(f"[{option[0]}]{option[1:]}")
            else:
                print(option)
        response = input(">>> ").lower()
        if firstLetterSelections:
            for option in options:
                if response == option[1].lower():
                    return option.lower()
        else:
            for option in options:
                if response == option.lower():
                    return option.lower()
        print("Invalid option, please try again.")

def numbered_select(options:list[str], use_parens = False, roman_numerals = False) -> str:
    while True:
        print("Please choose a option:")
        for index, option in enumerate(options):
            if roman_numerals:
                if use_parens:
                    print(f"{roman.toRoman(index+1)}) {option}")
                else:
                    print(f"{roman.toRoman(index+1)}. {option}")
            else:
                if use_parens:
                    print(f"{index+1}) {option}")
                else:
                    print(f"{index+1}. {option}")
        response = input(">>> ").lower()
        if roman_numerals:
            for index, option in enumerate(options):
                if response == roman.toRoman(index+1).lower():
                    return option
        else:
            for index, option in enumerate(options):
                if response == str(index+1):
                    return option
        print("Invalid option, please try again.")
