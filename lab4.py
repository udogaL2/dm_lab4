import string
from collections import Counter
from pprint import pprint

with open("text.txt", 'r') as f_in:
    input_data = f_in.read().strip().lower().translate(str.maketrans('', '', string.punctuation))

    symbols = {}
    p_symbols = {}
    counter = Counter(input_data)

    for letter in input_data:
        if letter not in symbols:
            symbols[letter] = 1
        else:
            symbols[letter] += 1

    for i in range(len(input_data) - 1):
        p_s = input_data[i] + input_data[i + 1]
        if p_s not in p_symbols:
            p_symbols[p_s] = 1
        else:
            p_symbols[p_s] += 1


