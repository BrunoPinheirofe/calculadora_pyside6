import re

NUM_OR_DOT_REGEX = re.compile(r"^[0-9.]$")


def isNumOrDot(string: str):
    return bool(NUM_OR_DOT_REGEX.search(string))


def isValidNumber(value: str):
    try:
        float(value)
        return True
    except ValueError:
        return False


def isEmpty(string: str):
    return len(string) == 0


def convertToIntOrFloat(number: str) -> int | float: # type: ignore

    numF = float(number)
    if numF.is_integer():
        return int(numF)
    else:
        return numF