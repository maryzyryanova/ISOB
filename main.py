from lab_1 import caesar_cipher


language = input('Language (RU/ENG): ')
message = input('Your meassage: ').upper()
step = int(input('Your step: '))

if language == 'RU':
    alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
else:
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'

print("Caesar cipher: " + caesar_cipher(alphabet, message, step))