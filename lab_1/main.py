from caesar_cipher import encode, decode
from vizhener_cipher import generateKey, decryption, encryption

language = input('Language (RU/ENG): ')
message = input('Your meassage: ').upper()
step = int(input('Your step: '))
key = input('Key word: ')
print()

if language == 'RU':
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
else:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'

    key = generateKey(message, key) 
    encrypt_text = encryption(message,key) 
    print("Encrypted message:", encrypt_text) 
    print("Decrypted message:", decryption(encrypt_text, key)) 
    
print()
enc_caesar = encode(alphabet, message, step)
dec_caesar = decode(alphabet, enc_caesar, step)
print("To Caesar cipher: " + enc_caesar)
print("From Caesar cipher: " + dec_caesar)