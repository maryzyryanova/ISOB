from caesar_cipher import encode, decode

language = input('Language (RU/ENG): ')
message = input('Your meassage: ').upper()
step = int(input('Your step: '))

if language == 'RU':
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
else:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'

enc = encode(alphabet, message, step)
dec = decode(alphabet, enc, step)
print("To Caesar cipher: " + enc)
print("From Caesar cipher: " + dec)