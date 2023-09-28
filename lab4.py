import string
import heapq
from math import log2

standart_codes = {'c': '00000', 'p': '00001', 'z': '0010', 'j': '0011', 'h': '0100', 'f': '01010', 'y': '01011',
                  't': '01100', 'n': '01101', 'i': '01110', 'g': '01111', 's': '10000', 'w': '10001', 'd': '10010',
                  'a': '10011', 'b': '10100', 'x': '10101', 'u': '10110', 'k': '10111', 'v': '11000', 'm': '11001',
                  ' ': '11010', 'q': '11011', 'o': '11100', 'l': '11101', 'r': '11110', 'e': '11111'}


def shennon(symbols, count):
    return sum([(symbols[i] / count) * log2(symbols[i] / count) for i in symbols])


class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq


def build_huffman_tree(freq_dict):
    heap = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, parent)
    return heap[0]


def build_huffman_codes(node, code='', codes=None):
    if codes is None:
        codes = {}

    if node.char:
        codes[node.char] = code
    else:
        build_huffman_codes(node.left, code + '0', codes)
        build_huffman_codes(node.right, code + '1', codes)
    return codes


def huffman_encode(text, codes):
    return ''.join([codes[char] for char in text])


if __name__ == '__main__':
    with open("text.txt", 'r') as f_in:
        input_data = f_in.read().strip().lower().translate(str.maketrans('', '', string.punctuation))

        symbols = {}
        p_symbols = {}

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


    print(p_symbols)
    tree = build_huffman_tree(symbols)
    codes = build_huffman_codes(tree)
    encoded_text = huffman_encode(input_data, codes)

    print(len(input_data) * 8, 'количество бит в исходном тексте, если один символ - один байт')
    print(len(encoded_text), 'количество бит в закодированном тексте. Динамика')

    with open('codes.txt', 'w') as f_out:
        f_out.write('\n'.join(['"' + i + '":  ' + codes[i] for i in codes]))
        f_out.close()

    with open('popularity.txt', 'w') as f_out:
        f_out.write('\n'.join(['"' + i + '":  ' + str(symbols[i]) for i in symbols]))
        f_out.close()

    with open('output.txt', 'w') as f_out:
        f_out.write(encoded_text)
        f_out.close()

    encoded_text = huffman_encode(input_data, standart_codes)
    print(len(encoded_text), 'количество бит в закодированном тексте. Статика')

    with open('standart_output.txt', 'w') as f_out:
        f_out.write(encoded_text)
        f_out.close()

    print(-shennon(symbols, len(input_data)), 'Энтропия в битах по формуле Шеннона')
    print(len(input_data) * -shennon(symbols, len(input_data)), 'Размер текста по энтропии')
