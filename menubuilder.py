try:
    import readline # Allows for going back through the text in the input prompt
except ImportError: # It's probably not here
    pass

from enum import Enum, auto

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


class Options(Enum):
    Forward = auto() # ">"
    Back = auto()    # "<"
    Cancel = auto()  # "X"


def menu(name: str, values: list, options: bool=False) -> int:
    """
    Builds a menu and prompts the user with it. Returns their response as an int

    Also will re-ask the user if their input was invalid (too high, too low, or not an integer)

    Args:
        name (str): The name of the menu, shown at the top.
        options (list): A list of options to choose from.

    Returns:
        int: The option number the user picked
    """

    prompt = f"{HEADER}{name}{ENDC}\n\n"
    for option_number, option in enumerate(values):
        prompt += f"{OKBLUE}({option_number}){ENDC} {OKCYAN}{option}{ENDC}\n"

    if options:
        prompt += f"{OKBLUE}(>){ENDC} {OKCYAN}Next Page{ENDC}\n"
        prompt += f"{OKBLUE}(<){ENDC} {OKCYAN}Previous Page{ENDC}\n"

    # Add this anyway, it's important imo
    prompt += f"{OKBLUE}(X){ENDC} {OKCYAN}Close Menu{ENDC}\n"


    prompt += f"\n{OKGREEN}> "
    while True:
        response = input(prompt)
        try:
            response = int(response)
        except ValueError:
            prompt = f"{WARNING}\"{response}\" is not an integer! Please try again.{ENDC}\n{OKGREEN}> "
            continue
        if 0 <= response < len(values):
            print(end=ENDC) # Reset terminal colour
            return response
        else:
            prompt = f"{WARNING}{response} is not a valid option! Please pick an integer between 0 and {len(values) - 1}.{ENDC}\n{OKGREEN}> "

    print(end=ENDC) # Reset terminal colour
