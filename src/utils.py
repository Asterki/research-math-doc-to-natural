import sys 

def verbose_print(message):
    if (sys.argv.count("--verbose") > 0):
        print(message)

