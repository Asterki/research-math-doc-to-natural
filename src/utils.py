import sys

def verbose_print(message):
    if "--verbose" in sys.argv:
        print(f"\033[90m{message}\033[0m")
