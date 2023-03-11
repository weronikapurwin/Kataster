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
