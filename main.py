# from curses.ascii import isdigit
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
            self.next_token = self.token_source.build_token()
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
                return 0
            if self.current_token in self.ofu_is_ofu:
                if self.next_token in self.ozk_l_ps_ls_lz:
                    self.next_token = self._get_next_token()[1]
                    if not self.next_token == self.EOT:
                        print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                        return 1
                return 0

            
        def parse(self):
            if not self.current_token.isdigit():
                print(f'{self.token_source._get_name()} ERROR: numer obrębu powinien być liczbą')
                return 1
            self.current_token = self._get_next_token()[0]
            if not self.current_token == '-':
                print(f'{self.token_source._get_name()} ERROR: błąd składniowy, oczekiwany znak - ')
                return 1
            self.current_token = self._get_next_token()[0]
            if not self.current_token.isdigit():
                print(f'{self.token_source._get_name()} ERROR: numer klasyfikacyjny powinien być liczbą')
                return 1
            self.current_token = self._get_next_token()[0]
            if not self.current_token == '/':
                print(f'{self.token_source._get_name()} ERROR: błąd składniowy, oczekiwany znak / ')
                return 1
            self.current_token, self.next_token = self._get_next_token()
                            # przypadek z ofu simple
            dupa = self._build_ofu_alone_or_isofu()
            if dupa != None:
                return dupa
           
    
            if self.current_token in self.ofu_l_ and self.next_token == '-':
                self.current_token, self.next_token = self._get_next_token()
                self.current_token, self.next_token = self._get_next_token()
                if self.current_token in ['Ł', 'Ps'] and self.next_token in self.ozk_l_ps_ls_lz:
                    self.current_token, self.next_token = self._get_next_token()
                    if self.current_token in self.ozk_l_ps_ls_lz and self.next_token == self.EOT:
                        return 0
                if self.current_token == 'R' and self.next_token in self.ozk_l_ps_ls_lz:
                    self.current_token, self.next_token = self._get_next_token()
                    if self.current_token in ['III', 'IV'] and self.next_token in ['a', 'b']:
                        self.next_token = self._get_next_token()[1]
                        if not self.next_token == self.EOT:
                            print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                            return 1
                        return 0
                    if self.current_token == 'VI' and self.next_token == 'z':
                        self.next_token = self._get_next_token()[1]
                        if not self.next_token == self.EOT:
                            print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                            return 1
                        return 0
                    self.current_token, self.next_token = self._get_next_token()
                    if not self.next_token == self.EOT:
                        print(f'{self.token_source._get_name()} ERROR: błąd')
                        return 1
                    return 0
            if self.current_token in ['W'] and self.next_token == '-':
                self.current_token, self.next_token = self._get_next_token()
                self.current_token, self.next_token = self._get_next_token()
                if self.current_token in ['Ł', 'Ps', 'Lz', 'Ls'] and self.next_token in self.ozk_l_ps_ls_lz:
                    self.next_token = self._get_next_token()[1]
                    if not self.next_token == self.EOT:
                            print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                            return 1

                if self.current_token == 'R' and self.next_token in self.ozk_l_ps_ls_lz:
                    self.current_token, self.next_token = self._get_next_token()
                    if self.current_token in ['III', 'IV'] and self.next_token in ['a', 'b']:
                        self.next_token = self._get_next_token()[1]
                        if not self.next_token == self.EOT:
                            print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                            return 1
                        return 0
                    if self.current_token == 'VI' and self.next_token == 'z':
                        self.next_token = self._get_next_token()[1]
                        if not self.next_token == self.EOT:
                            print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                            return 1
                        return 0
                    self.current_token, self.next_token = self._get_next_token()
                    if not self.next_token == self.EOT:
                        print(f'{self.token_source._get_name()} ERROR: błąd')
                        return 1
                self.current_token, self.next_token = self._get_next_token()    
                if not self.current_token in self.ozk_l_ps_ls_lz or not self.next_token == self.EOT:
                    print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                    return 1
                return 0
            if self.current_token == 'R' and self.next_token in self.ozk_l_ps_ls_lz:
                    self.current_token, self.next_token = self._get_next_token()
                    if self.current_token in ['III', 'IV']: 
                        if not self.next_token in ['a', 'b']:
                            print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                            return 1
                        self.next_token = self._get_next_token()[1]
                        if not self.next_token == self.EOT:
                            print(f'{self.token_source._get_name()} ERROR: błąd')
                            return 1
                        return 0
                    if self.current_token == 'VI': 
                        self.next_token = self._get_next_token()[1]
                        if self.next_token == self.EOT:
                            return 0
                        if self.next_token == 'z':
                            self.next_token = self._get_next_token()[1]
                            if not self.next_token == self.EOT:
                                print(f'{self.token_source._get_name()} ERROR: błąd OZK')
                                return 1
                        return 0
                    self.current_token, self.next_token = self._get_next_token()
                    if not self.next_token == self.EOT:
                        print(f'{self.token_source._get_name()} ERROR: błąd')
                        return 1
                    return 0
            print(f'{self.token_source._get_name()} ERROR: błąd klasyfikacji')
            return 1           

if __name__ == "__main__":
    data = np.array([])
    filepath = 'kontrolny_plik.txt'
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

    count = 0
    for i in data1:
        inp = get_input(i)
        lex = lexer(inp)
        pars = parser(lex)
        count += pars.parse()

    print('liczba błędów: ' + str(count))        

    
        

            