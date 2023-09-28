import string


def lzw_encode(text):
    chars_set = list(set(list(text)))
    dictionary_size = len(chars_set)
    dictionary = {chars_set[i]: i for i in range(dictionary_size)}
    cur_str = ""
    compressed_data = []

    for symbol in text:
        string_plus_symbol = cur_str + symbol
        if string_plus_symbol in dictionary:
            cur_str = string_plus_symbol
        else:
            compressed_data.append(dictionary[cur_str])
            if len(dictionary) <= maximum_table_size:
                dictionary[string_plus_symbol] = dictionary_size
                dictionary_size += 1
            cur_str = symbol

    if cur_str in dictionary:
        compressed_data.append(dictionary[cur_str])

    return compressed_data, dictionary


with open("text.txt", 'r') as f_in:
    input_data = f_in.read().strip().lower().translate(str.maketrans('', '', string.punctuation))
    maximum_table_size = 2 ** len(input_data)
    c_data, dict_ = lzw_encode(input_data)

    c_data = list(map(lambda x: bin(x)[2:], c_data))

    print(c_data)

    print(''.join(c_data))
    print(len(input_data) * 8, 'Длина исходного текста, если 1 символ = 8 бит')
    print(len(''.join(c_data)), 'Длина в битах закодированного текста')
