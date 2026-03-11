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
    
    # ===== ОБНОВЛЁННЫЙ МЕТОД =====
    def parse_var_decl(self):
        mutable = self.consume('KEYWORD')[1]  # var/val
        name = self.consume('IDENT')[1]
        
        # Явный тип (необязательный)
        explicit_type = None
        if self.peek() and self.peek()[1] == ':':
            self.consume('COLON', ':')
            type_token = self.consume('TYPE')  # int/bool/string
            explicit_type = type_token[1]
        
        # Значение (необязательное)
        value = None
        if self.peek() and self.peek()[1] == '=':
            self.consume('ASSIGN', '=')
            value = self.parse_logic()
        
        self.consume('SEMI', ';')
        
        return {
            'type': 'var_decl',
            'mutable': mutable,
            'name': name,
            'explicit_type': explicit_type,  # Сохраняем
            'value': value
        }
    
    def parse_print(self):
        self.consume('KEYWORD', 'println')
        self.consume('LPAR', '(')
        
        args = []
        if self.peek() and self.peek()[1] != ')':
            args.append(self.parse_logic())
            
            while self.peek() and self.peek()[1] == ',':
                self.consume('COMMA', ',')
                args.append(self.parse_logic())
        
        self.consume('RPAR', ')')
        self.consume('SEMI', ';')
        return {'type': 'print', 'args': args}
    
    # Иерархия парсинга выражений
    def parse_logic(self):
        node = self.parse_comparison()
        
        while self.peek() and self.peek()[1] in ('&&', '||'):
            op = self.consume()[1]
            right = self.parse_comparison()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        
        return node
    
    def parse_comparison(self):
        node = self.parse_expr()
        
        while self.peek() and self.peek()[1] in ('==', '!=', '<', '>'):
            op = self.consume()[1]
            right = self.parse_expr()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        
        return node
    
    def parse_expr(self):
        node = self.parse_term()
        
        while self.peek() and self.peek()[1] in ('+', '-'):
            op = self.consume()[1]
            right = self.parse_term()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        
        return node
    
    def parse_term(self):
        node = self.parse_factor()
        
        while self.peek() and self.peek()[1] in ('*', '/'):
            op = self.consume()[1]
            right = self.parse_factor()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        
        return node
    
    def parse_factor(self):
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
        elif token[1] == '(':
            self.consume('LPAR', '(')
            expr = self.parse_logic()
            self.consume('RPAR', ')')
            return expr
        else:
            raise SyntaxError(f"Unexpected expression: {token}")

if __name__ == "__main__":
    from lexer import tokenize
    
    print("=== Тест явных типов ===")
    code = """
    fn main() {
        var x: int = 10;
        val name: string = "Rail";
        var flag: bool = true;
        println(x, name, flag);
    }
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print("✅ AST создан успешно")
    for func in ast['functions']:
        print(f"Функция: {func['name']}")
        for stmt in func['body']['statements']:
            if stmt and stmt['type'] == 'var_decl':
                print(f"  Переменная: {stmt['name']}, тип: {stmt['explicit_type']}, значение: {stmt['value']}")