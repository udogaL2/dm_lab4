import string


def lzw_encode(text):
    dictionary_size = 256
    dictionary = {chr(i): i for i in range(dictionary_size)}
    string = ""
    compressed_data = []

    for symbol in text:
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if (len(dictionary) <= maximum_table_size):
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            string = symbol

    if string in dictionary:
        compressed_data.append(dictionary[string])

    return compressed_data


with open("test.txt", 'r') as f_in:
    input_data = f_in.read().strip().lower().translate(str.maketrans('', '', string.punctuation))
    maximum_table_size = 2 ** len(input_data)
    print(lzw_encode(input_data))
