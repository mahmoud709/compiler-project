import sys
class parser:
    
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.tokens = [self.parse_token(token) for token in file.read().split('\n')]
        self.current_token = 0

    def parse_token(self, token_str):
        # Assuming token_str is in the format "Token<KEYWORD, int>"
        startInd = 6
        endInd = len(token_str)-1
        token_str = token_str[startInd:endInd:1]
        parts = token_str.split(", ")
        return parts

    def syntax_error(self, expected, found, row, column):
        print('\033[1;31;40mSyntax Error: expected ' + expected + ' but found '+ found + ' at row ' + row + ' at column ' + str(int(column)-len(found)) +'\033[0m')
        sys.exit()

    def parse(self):
        token = self.tokens[self.current_token]
        if token[0] == 'KEYWORD' and (token[1] == 'int'):
            self.parse_function_declaration()
            self.parse_assignment_statement()
        elif token[0] == 'KEYWORD' and token[1] == 'if':
            self.parse_if_statement()
        elif token[0] == 'KEYWORD' and token[1] == 'while':
            self.parse_while_statement()
        elif token[0] == 'KEYWORD' and token[1] == 'for':
            self.parse_for_loop()
        elif token[0] == 'KEYWORD' and token[1] == 'return':
            self.parse_return_statement()
        elif token[0] == 'KEYWORD' and (token[1] == 'float' or token[1] == 'double' or token[1] == 'char' ):
            self.parse_assignment_statement()
        elif(token[0] == 'IDENTIFIER' or token[0] == 'NUMBER'):
            self.parse_expression()
            if(not self.match('SPECIAL CHARACTER', ';')):
                self.syntax_error(';',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])
        elif(token[0] == 'SPECIAL CHARACTER' and token[1] == ';'):
            self.match('SPECIAL CHARACTER', ';')
        else:
            print(self.current_token)
            print(len(self.tokens))
            if(self.current_token>=len(self.tokens)-1):
                self.syntax_error('}',' ',self.tokens[self.current_token-1][2],self.tokens[self.current_token-1][3]+1)
            self.syntax_error('KEYWORD or IDENTIFIER or NUMBER',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3]) ########## ??????????????????

    def match(self, expected_type, expected_value=None):
        if self.current_token < len(self.tokens):
            token = self.tokens[self.current_token]
            if token[0] == expected_type and (expected_value is None or token[1] == expected_value):
                self.current_token += 1
                print(token[0] + ', ' + token[1])
                return True
            return False
        else:
            self.syntax_error(expected_value,' nothing',self.tokens[self.current_token][2],self.tokens[self.current_token][3])

    

    def parse_function_declaration(self):
        if self.match('KEYWORD', 'int') and self.match('KEYWORD', 'main') and self.match('SPECIAL CHARACTER', '(') and self.match('SPECIAL CHARACTER', ')') and self.match('SPECIAL CHARACTER', '{'):
            self.current_token -= 1
            return self.parse_code_block()
        else:
            return False

    def parse_if_statement(self):

        if self.match('KEYWORD', 'if') and self.match('SPECIAL CHARACTER', '('):
            self.parse_expression()

            if(not self.match('SPECIAL CHARACTER', ')')):
                self.syntax_error(')',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])

            self.check_block_or_statement()

            if self.match('KEYWORD', 'else'):
                self.check_block_or_statement()
        else:
            self.syntax_error('(',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])

    def parse_while_statement(self):

        if self.match('KEYWORD', 'while') and self.match('SPECIAL CHARACTER', '('):
            self.parse_expression()

            if(not self.match('SPECIAL CHARACTER', ')')):
                self.syntax_error(')',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])

            self.check_block_or_statement()
            
        else:
            self.syntax_error('(',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])

    def parse_expression(self): 
        if(not self.check_increment() and not self.check_decrement()):
            if(self.check_operand()):
                while(self.check_operator()):
                    if(not self.check_operand()):
                        self.syntax_error('IDENTIFIER or NUMBER',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])
            

    def check_operand(self):
        return self.match('IDENTIFIER') or self.match('NUMBER')

    def check_operator(self):
        token = self.tokens[self.current_token]
        first_operator = token[1]
        first_op = self.match('OPERATOR')
        second_operator = token[1]
        if(first_operator == '&' and second_operator == '&'):   # &&
            self.match('OPERATOR', '&')
            return True
        if(first_operator == '|' and second_operator == '|'): 
            self.match('OPERATOR', '|')
            return True
        
        second_op = False
        second_op = self.match('OPERATOR', '=')
        return ((first_op and first_operator != '!') or (first_operator == '!' and second_op)) # make sure of !

    def parse_assignment_statement(self):
        if self.match('KEYWORD'): 
            if (not self.match('IDENTIFIER')):
                self.syntax_error('IDENTIFIER',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])
            if self.match('OPERATOR', '='):
                self.parse_expression()
            self.match('SPECIAL CHARACTER', ';') 


    def parse_for_loop(self):
        if self.match('KEYWORD', 'for') and self.match('SPECIAL CHARACTER', '('):
            self.parse_assignment_statement()
            self.parse_expression()
            if(not self.match('SPECIAL CHARACTER', ';')):
                self.syntax_error(';',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])
            self.parse_expression()
            if(not self.match('SPECIAL CHARACTER', ')')):
                self.syntax_error(')',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])
            self.check_block_or_statement()
        else:
            self.syntax_error('(',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])

    def check_block_or_statement(self):
        if (self.tokens[self.current_token][1]=='{'):
                self.parse_code_block()
        else:
            self.parse()

    def check_increment(self):
        flag = True
        curr = self.current_token
        flag &= self.match('IDENTIFIER')
        flag &= self.match('OPERATOR', '+')
        flag &= self.match('OPERATOR', '+')
        if(not flag):
            self.current_token = curr
        return flag

    def check_decrement(self):
        flag = True
        curr = self.current_token
        flag &= self.match('IDENTIFIER')
        flag &= self.match('OPERATOR', '-')
        flag &= self.match('OPERATOR', '-')
        if(not flag):
            self.current_token = curr
        return flag 

    def parse_return_statement(self):
        if self.match('KEYWORD', 'return'):
            print("Return statement:")
            self.parse_expression()
            if(not self.match('SPECIAL CHARACTER', ';')):
                self.syntax_error(';',self.tokens[self.current_token][1],self.tokens[self.current_token][2],self.tokens[self.current_token][3])
            
    def parse_code_block(self):    
        if self.match('SPECIAL CHARACTER', '{'):
            while not self.match('SPECIAL CHARACTER', '}'):
                self.parse()
            return True
        else:
            return False


# Example usage:
file_path = "tokens.txt"
parser = parser(file_path)
parser.parse()
print("\033[1;32;40mParsing successful!\033[0m")
