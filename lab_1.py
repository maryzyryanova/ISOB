def caesar_cipher(alphabet: str, input: str, step: int) -> str:
    output = ''
    for i in input:
        position = alphabet.find(i)
        new_position = step + position
        if i in alphabet:
            output += alphabet[new_position]
        else:
            output += i
    return output


def vizhener_cipher() -> str:
    def symbol_dict():
        d = {}
        iter = 0
        for i in range(0, 127):
            d[iter] = chr(i)
            iter += 1
        return d