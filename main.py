import numpy as np
from lexer_file import get_input, lexer
from parser_file import parser


if __name__ == "__main__":
    data = np.array([])
    filepath = 'kontrolny_plik.txt'
    # nr obrebu - nr klasyfikacyjny / ofu ozu ozk
    # wczytanie pliku tekstowego i filtracja do samych kodow
    with open(filepath) as f:
        for line in f:
            data = np.append(data, line.strip())
    data = list(data)
    data1 = np.array([])
    for x in data:
        if len(x) > 4 and len(x) < 20:
            data1 = np.append(data1, x)

    count = 0
    for i in data1:
        inp = get_input(i)
        lex = lexer(inp)
        pars = parser(lex)
        count += pars.parse()

    print('liczba błędów: ' + str(count))        

    
        

            