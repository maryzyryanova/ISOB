from caesar_cipher import encode, decode
from vizhener_cipher import encode_symb, decode_symb, encode_all, decode_all

language = input('Language (RU/ENG): ')
message = input('Your meassage: ').upper()
step = int(input('Your step: '))
key = input('Key word: ')

if language == 'RU':
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
else:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'
    encode_key = encode_symb(key)
    enc_vizhener = encode_all(encode_key, encode_symb(message))
    dec_vizhener = decode_all(encode_key, enc_vizhener)
    print("To Vizhener cipher: ", ''.join(decode_symb(enc_vizhener)))
    print("From Vizhener cipher: ", ''.join(decode_symb(dec_vizhener)))

enc_caesar = encode(alphabet, message, step)
dec_caesar = decode(alphabet, enc_caesar, step)
print("To Caesar cipher: " + enc_caesar)
print("From Caesar cipher: " + dec_caesar)
