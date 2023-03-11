from lexer_file import lexer

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
            temp = self._build_ofu_alone_or_isofu()
            if temp != None:
                return temp
           
    
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
