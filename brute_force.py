from zipfile import ZipFile
from pathlib import Path
from itertools import chain, product
import string
import time
import multiprocessing as mp
from functools import partial

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
        

def get_charset_combinations(charset, maxlength):
    return (''.join(candidate)
        for candidate in chain.from_iterable(product(charset, repeat=i)
        for i in range(1, maxlength + 1)))

def check_password(pw):
    try:
        zf.extractall(pwd=bytes(pw,'utf-8'))
        print ("The password is " + pw)
        return pw
    except:
        pass

# generator is ran by the individual processes
def generator(first_char, wordtail_length, length):

    # Generate all strings of length `length` starting with `first_char`.
    # Once length > wordtail_length, only the wordtail_length characters
    # need to be generated.
    if length <= wordtail_length:
        assert first_char == ""
        # creating all combinations of length charset here (short strings)
        for t in product(charset, repeat=length):
            result = "".join(t)
            print(result)
            # To compare to hash or keyword, do something with result here
            check_password(result)
    else:
        assert len(first_char) + wordtail_length == length
        # creating all combinations of length charset here (longer strings)
        for t in product(charset, repeat=wordtail_length):
            result = first_char + "".join(t)
            print(result)
            # To compare to hash or keyword, do something with result here
            check_password(result)
    
# Bruteforce algorithm. Tests combination possibilities
# of characters in charset
def bruteforce(pool, chunk_size=1000000):
    charset_length = len(charset)

    # This chunk sets max largest wordtail_length to be
    # computed without separating jobs by first_char
    wordtail_length = 1
    while charset_length**wordtail_length <= chunk_size:
        wordtail_length += 1
    wordtail_length -= 1

    # short strings: generate words from size 1 to short words max
    max_short_len = min(wordtail_length, pw_max_length)
    for length in range(1, max_short_len + 1):
        pool.apply_async(generator, args=("", wordtail_length, length))

    # longer strings: generate words from short words max to maxlength
    for length in range(max_short_len + 1, pw_max_length + 1):
        # Get the cartesian product chars in the charset
        for t in product(charset, repeat=length-wordtail_length):
            first_char = "".join(t) # Remove punctuation

            # Run generator function for on each process with args
            pool.apply_async(generator, args=(first_char, wordtail_length, length))


if __name__ == '__main__':
    zip_file = get_file()
    zf = ZipFile(zip_file)
    pw_max_length = get_max_pw_size()
    charset = get_charset()
    cores_used = None # defaults to all available cores
    result_pw = ""

    print("\nCharacter set chosen: ", charset)

    print("\nCores on machine to be used: ", mp.cpu_count())

    print("\n...Starting the Process....\n")

    start_time = time.time()

    # Multiprocessing setup here
    #pool = mp.Pool(cores_used)
    #bruteforce(pool)
    #pool.close()
    #pool.join()

    """
    for attempt in product(charset, repeat=pw_max_length):
        pw = "".join(attempt)
        if check_password(pw) != None:
            break
    """

    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(elapsed_time), "\n")



# Fácil Gere todas as combinações de números até 4 dígitos [0, 9999];

# Médio Gere todas as combinações de números e letras, maiúsculas e minúsculas, até tamanho 8;

# Avançado O programa recebe uma lista de caracteres ASCII e um parâmetro k indicando o tamanho máximo da senha, gerando todas as possíveis combinações;

# Expert Resolva o avançado gerando as combinações de senha com t threads em paralelo!


# hard -> Números, letras (Maiúsculas e Minúsculas), especiais (!, @, #, $, %, ^, &, *, (, ), [, {, +, -), com menos de 30 caracteres.