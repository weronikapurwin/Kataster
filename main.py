from curses.ascii import isdigit
from logging import raiseExceptions
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
        self.EOT = -2

    def _get_next_char(self):
            self.current_char = self.next_char
            try:
                self.next_char = self.input.get_char()
            except StopIteration:
                self.next_char = None

    def _build_number(self):
        value = ""
        if self.current_char.isdigit():
            if self.current_char == "0":
                if self.next_char.isdigit():
                    print(f"No digits allowed after 0 in number ")
                    return -1
                return '0'
            else:
                while self.next_char and self.next_char.isdigit():
                    value += self.current_char
                    self._get_next_char()
                value += self.current_char
            return value
            
    def _build_identifier(self):
        value = ""
        if self.current_char.isalpha():
            while self.next_char and (self.next_char.isalpha() and self.next_char not in ['I', 'V']):
                value += self.current_char
                self._get_next_char()
            value += self.current_char
            return value 
    
    def _build_roman(self):
        value = ""
        if self.current_char in ['I', 'V']:
            while self.next_char and (self.next_char in ['I', 'V']):
                value += self.current_char
                self._get_next_char()
            value += self.current_char 
            return value 

    def build_token(self):
        self._get_next_char()
           
        if self.current_char == None:
            return self.EOT

        if self.current_char in ['-', '/', ' ', '\t']:
            return self.current_char
        r = self._build_roman()
        if r:
            return r

        i = self._build_identifier()
        if i:
            return i

        t = self._build_number()
        if t:
            return t
    
    def _get_name(self):
        return self.input.get_string()
    # def build_token(self):
    #     self._get_next_char()

    #     if self.current_char == None:
    #         return self.EOT

    #     if self.current_char in ['-', '/', ' ', '\t']:
    #         return self.current_char

    #     t = self._build_number()
    #     if t:
    #         return t
            
    #     if self.current_char == 'K' or self.current_char == 'N':
    #         if self.next_char == None:
    #             return self.current_char
    #         else:
    #             print(f'{self.input.get_string()} OFU = K co tu robi {self.next_char} hmmm? powinien byc koniec stringa')
    #             return -1

    #     #  przypadki z R i Ł
    #     if self.current_char in ['R', 'Ł'] :
    #         if self.next_char in ['I', 'V']:
    #             return self.current_char
    #         else:
    #             print(f'{self.input.get_string()} OFU = OZU co tu robi {self.next_char} hmmm?')
    #             return -1
    #     # przypadki Z W
    #     if self.current_char == 'W':
    #         if self.next_char == '-':
    #             return self.current_char
    #         if self.next_char == 's':
    #             self._get_next_char()
    #             if self.next_char == 'r':
    #                 self._get_next_char()
    #                 if self.next_char == '-':
    #                     return 'Wsr'
    #                 else:
    #                     print(f'{self.input.get_string()} OFU to tylko Wsr a ty co tworzysz?')
    #                     return -1
    #             if self.next_char == None:
    #                 return 'Ws'
    #             else:
    #                 print(f'{self.input.get_string()} coś nie dziala z Ws')
    #                 return -1
    #         if self.next_char in ['m', 'p']:
    #             return 'W' + self.next_char
    #         else:
    #             print(f'{self.input.get_string()} OFU /= OZU co tu robi {self.next_char} hmmm? powinien być myślnik')
    #             return -1
    #     # przypadek z S
    #     if self.current_char == 'S':
    #         if self.next_char == '-':
    #             return self.current_char
    #         else:
    #             print(f'{self.input.get_string()} OFU /= OZU co tu robi {self.next_char} hmmm? powinien być myślnik')
    #             return -1
    #     # przypadki z B
    #     if self.current_char == 'B':
    #         if self.next_char == None:
    #             return self.current_char
    #         if self.next_char == 'r':
    #             self._get_next_char()
    #             if self.next_char == '-':
    #                 return 'Br'
    #             else:
    #                 print(f'{self.input.get_string()} powinno być Br')
    #                 return -1
    #         # else:
    #         #         print(f'{self.input.get_string()} OFU /= OZU co tu robi {self.next_char} jest tylko OFU = Br')
    #         if self.next_char in ['a', 'i', 'p', 'z']:
    #             self._get_next_char()
    #             if self.next_char == None:
    #                 return 'B' + self.current_char
    #             else:
    #                 print(f'{self.input.get_string()} powinno być Ba bi bp lub bz')
    #                 return -1
    #         else:
    #             print(f'{self.input.get_string()} jakiś blad z B')
    #             return -1
    #     # przypadek z Ps
    #     if self.current_char == 'P':
    #         if self.next_char == 's':
    #             self._get_next_char()
    #             if self.next_char in ['I', 'V']:
    #                 return 'Ps'
    #             else:
    #                 print(f'{self.input.get_string()} cos po Ps nie gra')
    #                 return -1
  
    #         else:
    #             print(f'{self.input.get_string()} OFU /= OZU co tu robi {self.next_char} jest tylko OFU = Ps')
    #             return -1
    #     # przypadki z Ls
    #     if self.current_char == 'L':
    #         if self.next_char == 's':
    #             self._get_next_char()
    #             if self.next_char in [None, 'I', 'V']:
    #                 return 'Ls'
    #             else:
    #                 print(f'{self.input.get_string()} powinno po Ls byc nic lub liczba rzymska')
    #                 return -1

    #         else:
    #             print(f'{self.input.get_string()} OFU = OZU co tu robi {self.next_char} powinno być samo Ls')
    #             return -1
    #     # przypadki z Lz i Lzr
    #     if self.current_char == 'L':
    #         if self.next_char == 'z':
    #             self._get_next_char()
    #             if self.next_char == 'r':
    #                 self._get_next_char()
    #                 if self.next_char == '-':
    #                     return 'Lzr'
    #                 else:
    #                     print(f'{self.input.get_string()} powinno być Lzr')
    #                     return -1
    #             if self.next_char in [None, 'I', 'V']:
    #                 return 'Lz' 
    #             else:
    #                 print(f'{self.input.get_string()} powinno być Lz')
    #                 return -1
    #         else:
    #             print(f'{self.input.get_string()} ERROR expected ofu Lz or Lzr')
    #             return -1
    #     # przypadek z dr
    #     if self.current_char == 'd':
    #         if self.next_char == 'r':
    #             return 'dr'
    #         else:
    #              print(f'{self.input.get_string()} ERROR: expected ofu = dr')
    #              return -1
    #     # przypadek z T
    #     if self.current_char == 'T':
    #         if self.next_char in ['k', 'i', 'p', 'r']:
    #             return 'T' + self.next_char
    #         else:
    #             print(f'{self.input.get_string()} cos pojebane z T')
    #             return -1
    #     else:
    #         print(f'{self.input.get_string()} cos  zle')
    #         return -1
    
    # do testowania
    def get_all_tokens(self):
        t = self.build_token()
        while t != self.EOT:
            yield t
            t = self.build_token()
        yield t


class parser:
        def __init__(self, token_source: lexer):
            self.token_source = token_source
            self.current_token = self.token_source.build_token()
            self.next_token = self.current_token.build_token()
            self.ofu_simple = ['Lz', 'B', 'Ba', 'Bi', 'Bp', 'Bz', 'K', 'dr', 'Tk', 'Ti', 'Tp', 'Wm', 'Wp', 'Ws', 'Tr', 'N']
            self.ofu_l_ = ['S', 'Br', 'Wsr', 'Lzr']
            self.ofu_w = ['W']
            self.ofu_is_ofu = ['Ps', 'Ł', 'Lz', 'Ls']
            self.ofu_r = ['R']

            self.ozk_r = ['I', 'II', 'IIIa', 'IIIb', 'IVa', 'IVb', 'V', 'VI', 'VIz']
            self.ozk_l_ps_ls_lz = ['I', 'II', 'III','IV', 'V', 'VI']
            self.EOT = -2

        # def __get_next_token(self):
        #     self.current_token = self.token_source.build_token()
        #     return self.current_token
        
        def _get_next_token(self):
            self.current_token = self.next_token
            self.next_token = self.token_source.build_token()
            return self.current_token, self.next_token 

        def _build_ofu_alone_or_isofu(self):
            if self.current_token in self.ofu_simple and self.next_token == self.EOT:
                return
            if self.current_token in self.ofu_is_ofu and self.next_token in self.ozk_l_ps_ls_lz:
                return
            else:
                print(f'{self.token_source._get_name()} ERROR: błąd OFU')
            

        def parse(self):
            if not self.current_token.isdigit():
                print(f'{self.token_source._get_name()} ERROR: numer obrębu powinien być liczbą')
            self.current_token[0] = self._get_next_token()
            if not self.current_token == '-':
                print(f'{self.token_source._get_name()} ERROR: błąd składniowy, oczekiwany znak - ')
            self.current_token[0] = self._get_next_token()
            if not self.current_token.isdigit():
                print(f'{self.token_source._get_name()} ERROR: numer klasyfikacyjny powinien być liczbą')
            self.current_token[0] = self._get_next_token()
            if not self.current_token == '/':
                print(f'{self.token_source._get_name()} ERROR: błąd składniowy, oczekiwany znak / ')
            self.current_token, self.next_token = self._get_next_token()
                            # przypadek z ofu simple
            self._build_ofu_alone_or_isofu()
            if self.current_token in self.ofu_l_ and self.next_token == '-':
                self.current_token[0] = self._get_next_token()
                if not self.current_token in ['Ł', 'Ps'] and self.next_token in self.ozk_l_ps_ls_lz:
                    print(f'{self.token_source._get_name()} ERROR: błąd OFU')
                self.current_token[0] = self._get_next_token()
                if not self.current_token in self.ozk_l_ps_ls_lz and self.next_token == self.EOT:
                    print(f'{self.token_source._get_name()} ERROR: błąd OFU')


            # if not self.current_token in self.ofu_simple and self.next_token == self.EOT:
            #     print(f'{self.token_source._get_name()} ERROR: OFU ')
                                

                                
                                
             
            

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

    data2 = ['23-146/RIVa']
    count = 0
    for i in data2:
        inp = get_input(i)
        lex = lexer(inp)
        for token in lex.get_all_tokens():
            if token == -1:
                count+=1
            print(token)
    print('liczba błędów: ' + str(count))        

    
        

            