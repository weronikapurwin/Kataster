import numpy as np
import re

# przeszukuje mi kazdy znak w stringu
class get_input:
    def __init__(self, string):
        self.string = string
        self.gen = self._char_generator()

    def _char_generator(self) -> str:
        for char in self.string:
                yield char

    def get_char(self) -> str:
        return next(self.gen)

    def get_string(self):
        return self.string

class lexer:
    def __init__(self, source: get_input):
        self.current_char = None
        self.input = source
        self.next_char = self.input.get_char()
        # self.ofu_r = ['R', 'S', 'Br', 'Wsr', 'W', 'Lzr']   # 23-13/W-RIIIb 23 -> nr obrębu - nr klasy / 
        # self.ofu_l_ = ['Ł', 'S' 'Br', 'Wsr', 'W', 'Lzr']
        # self.ofu_ps = ['Ps', 'S' 'Br', 'Wsr', 'W', 'Lzr']
        # self.ofu_ls = ['Ls', 'W']
        # self.ofu_lz = ['Lz', 'W']

        # self.ozk_r = ['I', 'II', 'IIIa', 'IIIb', 'IVa', 'IVb', 'V', 'VI', 'VIz']
        # self.ozk_l_ps_ls_lz = ['I', 'II', 'III','IV', 'V', 'VI']

        self.EOT = -1

    def _get_next_char(self):
            self.current_char = self.next_char
            try:
                self.next_char = self.input.get_char()
            except StopIteration:
                self.next_char = None

    def _build_number(self):
        pass
 
    def build_token(self):

        self._get_next_char()
        if self.current_char == '-':
            return self.current_char

        if self.current_char == 'K' or self.current_char == 'N':
            if self.next_char == None:
                return self.current_char
            else:
                print(f'{self.input.get_string()} OFU = K co tu robi {self.next_char} hmmm? powinien byc koniec stringa')
                return

        #  przypadki z R i Ł
        if self.current_char in ['R', 'Ł'] :
            if self.next_char in ['I', 'V']:
                return self.current_char
            else:
                print(f'{self.input.get_string()} OFU = OZU co tu robi {self.next_char} hmmm?')
                return
        # przypadki Z W
        if self.current_char == 'W':
            if self.next_char == '-':
                return self.current_char
            if self.next_char == 's':
                self._get_next_char()
                if self.next_char == 'r':
                    self._get_next_char()
                    if self.next_char == '-':
                        return 'Wsr'
                    else:
                        print(f'{self.input.get_string()} OFU to tylko Wsr a ty co tworzysz?')
                        return
                if self.next_char == None:
                    return 'Ws'
                else:
                    print(f'{self.input.get_string()} coś nie dziala z Ws')
                    return
            if self.next_char in ['m', 'p']:
                return 'W' + self.next_char
            else:
                print(f'{self.input.get_string()} OFU /= OZU co tu robi {self.next_char} hmmm? powinien być myślnik')
                return
        # przypadek z S
        if self.current_char == 'S':
            if self.next_char == '-':
                return self.current_char
            else:
                print(f'{self.input.get_string()} OFU /= OZU co tu robi {self.next_char} hmmm? powinien być myślnik')
                return
        # przypadki z B
        if self.current_char == 'B':
            if self.next_char == None:
                return self.current_char
            if self.next_char == 'r':
                self._get_next_char()
                if self.next_char == '-':
                    return 'Br'
                else:
                    print(f'{self.input.get_string()} powinno być Br')
                    return
            # else:
            #         print(f'{self.input.get_string()} OFU /= OZU co tu robi {self.next_char} jest tylko OFU = Br')
            if self.next_char in ['a', 'i', 'p', 'z']:
                self._get_next_char()
                if self.next_char == None:
                    return 'B' + self.current_char
                else:
                    print(f'{self.input.get_string()} powinno być Ba bi bp lub bz')
                    return
            else:
                print(f'{self.input.get_string()} jakiś blad z B')
                return
        # przypadek z Ps
        if self.current_char == 'P':
            if self.next_char == 's':
                self._get_next_char()
                if self.next_char in ['I', 'V']:
                    return 'Ps'
                else:
                    print(f'{self.input.get_string()} cos po Ps nie gra')
                    return
  
            else:
                print(f'{self.input.get_string()} OFU /= OZU co tu robi {self.next_char} jest tylko OFU = Ps')
                return
        # przypadki z Ls
        if self.current_char == 'L':
            if self.next_char == 's':
                self._get_next_char()
                if self.next_char in [None, 'I', 'V']:
                    return 'Ls'
                else:
                    print(f'{self.input.get_string()} powinno po Ls byc nic lub liczba rzymska')
                    return

            else:
                print(f'{self.input.get_string()} OFU = OZU co tu robi {self.next_char} powinno być samo Ls')
                return
        # przypadki z Lz i Lzr
        if self.current_char == 'L':
            if self.next_char == 'z':
                self._get_next_char()
                if self.next_char == 'r':
                    self._get_next_char()
                    if self.next_char == '-':
                        return 'Lzr'
                    else:
                        print(f'{self.input.get_string()} powinno być Lzr')
                        return
                if self.next_char in [None, 'I', 'V']:
                    return 'Lz' 
                else:
                    print(f'{self.input.get_string()} powinno być Lz')
                    return
            else:
                print(f'{self.input.get_string()} cos pojebane z ofu Lz lub Lzr ma byc')
                return
        # przypadek z dr
        if self.current_char == 'd':
            if self.next_char == 'r':
                return 'dr'
            else:
                 print(f'{self.input.get_string()} cos pojebane z dr')
                 return
        # przypadek z T
        if self.current_char == 'T':
            if self.next_char in ['k', 'i', 'p', 'r']:
                return 'T' + self.next_char
            else:
                print(f'{self.input.get_string()} cos pojebane z T')
                return 

if __name__ == "__main__":
    data = np.array([])
    filepath = 'Kontury_eksport_dz.txt'
    # nr obrebu - nr klasyfikacyjny / ofu ozu ozk
    with open(filepath) as f:
        for line in f:
            data = np.append(data, line.strip())
    data = list(data)
    data.sort(key = lambda x: len(x))
    data1 = np.array([])
    for x in data:
        if len(x) > 4 and len(x) < 20:
            data1 = np.append(data1, x)

    data2 = ['R', 'RV', 'N', 'N', 'LsIII' ,'PsIII']
    for i in data2:
        inp = get_input(i)
        lex = lexer(inp)
        print(lex.build_token())

    
        

            