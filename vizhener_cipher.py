from itertools import cycle

def symbol_dict() -> dict:
    return dict([(i, chr(i)) for i in range(128)])

def encode_symb(word: str) -> list:
    d = symbol_dict()
    return [key for w in word for key, value in d.items() if value == w]

def compare(key: str, value: int) -> dict:
    return dict([(index, [symbol[0], symbol[1]]) for index, symbol in enumerate(zip(value, cycle(key)))])

def encode_all(key: str, value: str) -> list:
    d = compare(key, value)
    length = len(symbol_dict())
    return [(v[0] + v[1]) % length for v in d.values()]

def decode_symb(word: str) -> list:
    # length = len(word)
    d = symbol_dict()
    return [d[symbol] for symbol in word if symbol in d]

def decode_all(key: str, value: str):
    d = compare(key, value)
    length = len(symbol_dict())
    return [(v[0] - v[1])%length for v in d.values()]