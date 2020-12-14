from zipfile import ZipFile
from pathlib import Path
from itertools import chain, product
import string
import time

# Asks the user the name of the file until it is a valid file
def get_file():
    file_name = input("\nEnter the name of the zip file (with .zip): ")
    zip_file = Path(file_name)
    while not zip_file.exists():
        file_name = input("Couldn't find that file. Please try again: (with .zip): ")
        zip_file = Path(file_name)
    return zip_file

# Asks the user the maximum password length to check until it is a valid number
def get_max_pw_size():
    pw_max_length = 0
    while pw_max_length <= 0:
        try:
            pw_max_length = int(input("\nEnter the maximum length of the password: "))
        except:
            print("Please type in a number [0..9]")
    return pw_max_length

# Asks the user the type of charset to use until it is a valid charset
def get_charset():
    print("\n-------- CHARSETS -------\n" +
        "1 -> digits\n" + 
        "2 -> upper and lower case letters\n" +
        "3 -> digits and lower case leters\n" + 
        "4 -> digits, upper and lowercase letters\n" + 
        "5 -> digits, upper and lowercase letters, and common special characters\n")

    charset_type = 0
    while charset_type <= 0 or charset_type >= 6:
        try:
            charset_type = int(input("Choose the charset: "))
        except:
            print("Please type in a number [0..9]")

    if charset_type == 1:
        return "0123456789"
    elif charset_type == 2:
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    elif charset_type == 3:
        return "0123456789abcdefghijklmnopqrstuvwxyz"
    elif charset_type == 4:
        return "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    elif charset_type == 5:
        return "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()[]{+-}"
        
"""
def get_charset_combinations(charset, minlength, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(minlength, maxlength)))
"""


if __name__ == '__main__':
    zip_file = get_file()
    zf = ZipFile(zip_file)
    pw_max_length = get_max_pw_size()
    charset = get_charset()

    print("\nCharacter set chosen: ", charset)

    print("\n...Starting the Process....\n")

    start_time = time.time()

    with ZipFile(zip_file) as zf:
        for attempt in product(charset, repeat=pw_max_length):
            pw = "".join(attempt)
            try:
                zf.extractall(pwd=bytes(pw,'utf-8'))
                print ("The password is " + pw)
                break
            except:
                pass

    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(elapsed_time), "\n")



# Fácil Gere todas as combinações de números até 4 dígitos [0, 9999];

# Médio Gere todas as combinações de números e letras, maiúsculas e minúsculas, até tamanho 8;

# Avançado O programa recebe uma lista de caracteres ASCII e um parâmetro k indicando o tamanho máximo da senha, gerando todas as possíveis combinações;

# Expert Resolva o avançado gerando as combinações de senha com t threads em paralelo!


# hard -> Números, letras (Maiúsculas e Minúsculas), especiais (!, @, #, $, %, ^, &, *, (, ), [, {, +, -), com menos de 30 caracteres.