from des_resources import (
    D_BOX,
    FP,
    IP,
    KP_1,
    KP_2,
    S_BOX,
    SHIFTS,
    STRAIGHT_PERMUTATION,
)


def split_bites(bites: list, nth: int) -> list:
    return [bites[nth * i : nth * (i + 1)] for i in range(len(bites) // nth)]


def convert_bits_to_string(bites: list) -> str:
    return "".join(
        [
            chr(int(string, 2))
            for string in [
                "".join(list(map(str, byte))) for byte in split_bites(bites, 8)
            ]
        ]
    )


def remove_two_bites(character: str) -> list:
    return (
        list(bin(character)[2:])
        if isinstance(character, int)
        else list(bin(ord(character))[2:])
    )


def pull_bite_number(bites: list, nth: int) -> None:
    [bites.insert(0, "0") for i in range(nth - len(bites))]


def convert_string_to_bits(string: str) -> list:
    bites = []
    for character in string:
        byte = remove_two_bites(character)
        pull_bite_number(byte, 8)

        bites.extend(byte)

    return list(map(int, bites))


def permute(key: list or str, table: list) -> list:
    return [key[i - 1] for i in table]


def xor(a: list, b: list) -> list:
    return [x ^ y for x, y in zip(a, b)]


def generate_keys(password: str) -> list:
    keys = []
    key = convert_string_to_bits(password)
    key = permute(key, KP_1)
    left, right = split_bites(key, 28)
    for i in range(16):
        left, right = left_shift(left, SHIFTS[i]), left_shift(right, SHIFTS[i])
        compose = left + right
        keys.append(permute(compose, KP_2))

    return keys


def left_shift(key: list, nth_shifts: int) -> list:
    return key[nth_shifts:] + key[:nth_shifts]


def right_shift(key: list, nth_shifts: int) -> list:
    return key[len(key) - nth_shifts :] + key[: len(key) - nth_shifts]


def add_padding(text: list or str) -> list:
    pad_len = 8 - (len(text) % 8)
    text += pad_len * chr(pad_len)

    return text


def remove_padding(data: list or str) -> list:
    pad_len = ord(data[-1])

    return data[:-pad_len]


def substitute(expanded_value: list) -> list:
    blocks = split_bites(expanded_value, 6)
    result = list()

    for i in range(len(blocks)):
        block = blocks[i]
        row = int(str(block[0]) + str(block[5]), 2)
        column = int("".join([str(x) for x in block[1:][:-1]]), 2)
        table_value = S_BOX[i][row][column]

        bites = remove_two_bites(table_value)
        pull_bite_number(bites, 4)

        result += [int(x) for x in bites]

    return result


def des(key: str, text: str, *, encrypt: bool = True, padding: bool = False):
    if len(key) < 8:
        raise Exception("Length of key is lower than 8 symbols!")
    elif len(key) > 8:
        key = key[:8]

    if padding and encrypt:
        text = add_padding(text)
    elif len(text) % 8 != 0:
        raise Exception("Data size should be multiple of 8!")

    keys = generate_keys(key)
    text_blocks = split_bites(text, 8)
    result = []

    for block in text_blocks:
        block = convert_string_to_bits(block)
        block = permute(block, IP)
        left, right = split_bites(block, 32)

        for i in range(16):
            right_expanded = permute(right, D_BOX)
            if encrypt:
                temp_result = xor(keys[i], right_expanded)
            else:
                temp_result = xor(keys[15 - i], right_expanded)

            temp_result = substitute(temp_result)
            temp_result = permute(temp_result, STRAIGHT_PERMUTATION)
            temp_result = xor(left, temp_result)
            left, right = right, temp_result
        result += permute(right + left, FP)

    return (
        remove_padding(convert_bits_to_string(result))
        if padding and not encrypt
        else convert_bits_to_string(result)
    )


class DES:
    @staticmethod
    def encrypt(data: list or tuple, key: int) -> str:
        print("\nBEFORE encrypt:", data)
        cipher = des(str(key), str(data), encrypt=True, padding=True)
        print("AFTER encrypt:", cipher, end="\n\n")

        return cipher

    @staticmethod
    def decrypt(data: str, key: int) -> tuple:
        print("\nBEFORE decrypt:", data)
        plain_text = eval(des(str(key), data, encrypt=False, padding=True))
        print("AFTER decrypt:", plain_text, end="\n\n")

        return plain_text


if __name__ == "__main__":
    key = "maryzyryanova"
    text = "hello world"
    res = des(key, text, encrypt=True, padding=True)
    print("Ciphered:", repr(res))
    sd = des(key, res, encrypt=False, padding=True)
    print("Deciphered:", sd)
