def encode(alphabet: str, input: str, step: int) -> str:
    output = ''
    for i in input:
        position = alphabet.find(i)
        new_position = step + position
        if i in alphabet:
            output += alphabet[new_position]
        else:
            output += i
    return output


def decode(alphabet: str, input: str, step: int) -> str:
    output = ''
    for i in input:
        position = alphabet.find(i)
        new_position = position - step
        if i in alphabet:
            output += alphabet[new_position]
        else:
            output += i
    return output