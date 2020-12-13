from zipfile import ZipFile
from pathlib import Path
from itertools import product
import string

CHARSET = "0123456789"
#abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()[]{+-}"

file_name = input("Enter the name of the zip file (with .zip): ")
zip_file = Path(file_name)
while not zip_file.exists():
    print()
    file_name = input("Couldn't find that file. Please try again: (with .zip): ")
    zip_file = Path(file_name)

pw_max_length = 0
while pw_max_length <= 0:
    try:
        pw_max_length = int(input("Enter the maximum length of the password: "))
    except:
        print("Please type in a number [0..9]")

password = 'password' 
with ZipFile(zip_file) as zf:  
    
    
    for wordchars in product(CHARSET, repeat=pw_max_length):
        pw = ''.join(wordchars)
        try:
            zf.extractall(pwd=bytes(pw,'utf-8'))
            print ("The password is " + pw)
            break
        except:
            pass





# Fácil Gere todas as combinações de números até 4 dígitos [0, 9999];

# Médio Gere todas as combinações de números e letras, maiúsculas e minúsculas, até tamanho 8;

# Avançado O programa recebe uma lista de caracteres ASCII e um parâmetro k indicando o tamanho máximo da senha, gerando todas as possíveis combinações;

# Expert Resolva o avançado gerando as combinações de senha com t threads em paralelo!


# hard -> Números, letras (Maiúsculas e Minúsculas), especiais (!, @, #, $, %, ^, &, *, (, ), [, {, +, -), com menos de 30 caracteres.