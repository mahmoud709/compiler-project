class Scanner:
    def __init__(self, src):
        self.tokens = []
        self.src = src
        self.pointer = 0

    def scan(self):
        token_string = ""

        while not self.is_eof():
            c = self.src[self.pointer]
            self.pointer += 1

            if self.except_comment():
                print("Invalid Comment")
                return

            if c.isspace():
                continue
            elif c.isalpha():
                while self.pointer < len(self.src) and (self.src[self.pointer].isnumeric() or self.src[self.pointer].isalpha()):
                    c += self.src[self.pointer]
                    self.pointer += 1
                if self.is_keyword(c):
                    self.tokens.append(("Keyword", c))
                else:
                    self.tokens.append(("ID", c))
            elif self.is_special_character(c):
                self.tokens.append((self.is_special_character(c), c))
            elif self.is_operator(c):
                token_string = c + self.src[self.pointer] if self.pointer < len(self.src) else c
                if self.is_operator(token_string):
                    self.pointer += 1
                    self.tokens.append((self.is_operator(token_string), token_string))
                else:
                    self.tokens.append((self.is_operator(c), c))
            elif c.isnumeric():
                while self.pointer < len(self.src) and self.src[self.pointer].isnumeric():
                    c += self.src[self.pointer]
                    self.pointer += 1
                self.tokens.append(("Number", c))
            else:
                break

        return self.tokens

    def is_keyword(self, token_string):
        keywords = {
            "const": "Const",
            "else": "Else",
            "if": "If",
            "int": "Int",
            "return": "Return",
            "void": "Void",
            "while": "While",
            "true": "True",
            "false": "False",
            "for": "For"
        }
        return keywords.get(token_string)

    def is_special_character(self, token_string):
        special_characters = {
            "(": "LParen",
            ")": "RParen",
            "[": "LBracket",
            "]": "RBracket",
            ";": "Semicolon",
            ",": "Comma",
            "{": "LBrace",
            "}": "RBrace",
            "\"": "DoubleQuotes"
        }
        return special_characters.get(token_string)

    def is_operator(self, token_string):
        operators = {
            "!": "Not",
            "!=": "NotEqu",
            "%": "Mod",
            "%=": "ModAssign",
            "&&": "And",
            "||": "Or",
            "*": "Mul",
            "*=": "MulAssign",
            "+": "Plus",
            "++": "Increase",
            "+=": "AddAssign",
            "-": "Minus",
            "--": "Decrease",
            "-=": "SubAssign",
            "/": "Div",
            "/=": "DivAssign",
            "<": "Less",
            "<=": "Lesser",
            "=": "Assign",
            "==": "Equal",
            ">": "Great",
            ">=": "Greater"
        }
        return operators.get(token_string)

    def except_comment(self):
        while not self.is_eof() and self.src[self.pointer].isspace():
            self.pointer += 1

        if self.is_eof():
            return False

        if self.src[self.pointer] == '/':
            if self.pointer + 1 < len(self.src) and self.src[self.pointer + 1] == '/':
                self.pointer += 2
                while not self.is_eof() and self.src[self.pointer] != '\n':
                    self.pointer += 1
                if not self.is_eof():
                    self.pointer += 1
            elif self.pointer + 1 < len(self.src) and self.src[self.pointer + 1] == '*':
                self.pointer += 2
                while self.src[self.pointer] != '*' and self.src[self.pointer + 1] != '/':
                    if self.is_eof():
                        return True
                    self.pointer += 1
                self.pointer += 2
        return False

    def is_eof(self):
        return self.pointer >= len(self.src)


if __name__ == '__main__':
    src = input("Enter the source code:\n")
    sc = Scanner(src)
    tokens = sc.scan()
    print(tokens)
