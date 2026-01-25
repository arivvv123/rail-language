# rail_compiler/parser.py
from lexer import tokenize

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def consume(self, expected_type=None, expected_value=None):
        token = self.peek()
        if not token:
            raise SyntaxError("Unexpected EOF")
        
        if expected_type and token[0] != expected_type:
            raise SyntaxError(f"Expected {expected_type}, got {token[0]}")
        
        if expected_value and token[1] != expected_value:
            raise SyntaxError(f"Expected '{expected_value}', got '{token[1]}'")
        
        self.pos += 1
        return token
    
    def parse(self):
        ast = {'type': 'program', 'functions': []}
        
        while self.peek():
            if self.peek()[1] == 'fn':
                ast['functions'].append(self.parse_function())
            else:
                raise SyntaxError(f"Unexpected token: {self.peek()}")
        
        return ast
    
    def parse_function(self):
        self.consume('KEYWORD', 'fn')
        name = self.consume('IDENT')[1]
        self.consume('LPAR', '(')
        self.consume('RPAR', ')')
        body = self.parse_block()
        return {'type': 'function', 'name': name, 'body': body}
    
    def parse_block(self):
        self.consume('LBRACE', '{')
        stmts = []
        
        while self.peek() and self.peek()[1] != '}':
            stmt = self.parse_statement()
            if stmt:
                stmts.append(stmt)
        
        self.consume('RBRACE', '}')
        return {'type': 'block', 'statements': stmts}
    
    def parse_statement(self):
        token = self.peek()
        
        if token[1] in ('var', 'val'):
            return self.parse_var_decl()
        elif token[1] == 'println':
            return self.parse_print()
        elif token[1] == ';':
            self.consume('SEMI', ';')
            return None
        else:
            raise SyntaxError(f"Unexpected statement: {token}")
    
    def parse_var_decl(self):
        mutable = self.consume('KEYWORD')[1]  # var/val
        name = self.consume('IDENT')[1]
        value = None
        
        if self.peek() and self.peek()[1] == '=':
            self.consume('ASSIGN', '=')
            value = self.parse_expr()
        
        self.consume('SEMI', ';')
        return {
            'type': 'var_decl',
            'mutable': mutable,
            'name': name,
            'value': value or {'type': 'number', 'value': '0'}
        }
    
    def parse_print(self):
        self.consume('KEYWORD', 'println')
        self.consume('LPAR', '(')
        
        args = []
        if self.peek() and self.peek()[1] != ')':
            args.append(self.parse_expr())
            
            while self.peek() and self.peek()[1] == ',':
                self.consume('COMMA', ',')
                args.append(self.parse_expr())
        
        self.consume('RPAR', ')')
        self.consume('SEMI', ';')
        return {'type': 'print', 'args': args}
    
    def parse_expr(self):
        # Упрощённо — пока только числа, строки, переменные
        token = self.peek()
        
        if token[0] == 'NUMBER':
            self.consume('NUMBER')
            return {'type': 'number', 'value': token[1]}
        elif token[0] == 'STRING':
            self.consume('STRING')
            return {'type': 'string', 'value': token[1]}
        elif token[0] == 'IDENT':
            self.consume('IDENT')
            return {'type': 'ident', 'value': token[1]}
        else:
            # TODO: Добавить арифметику и скобки
            raise SyntaxError(f"Unexpected expression: {token}")

# Тест
if __name__ == "__main__":
    from lexer import tokenize
    code = """
    fn main() {
        var x = 10;
        println("Hello", x);
    }
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)
