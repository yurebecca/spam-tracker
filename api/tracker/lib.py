import math

# Simple way to count number of words in a string
def word_count(str):
    words = str.split()

    return len(words)

# This is due to python's rounding issue
def round_half_up(n, decimals = 0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier