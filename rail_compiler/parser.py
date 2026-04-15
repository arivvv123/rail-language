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
            _, _, line, col = token
            raise SyntaxError(f"Expected {expected_type}, got {token[0]} at line {line}, column {col}")
        
        if expected_value and token[1] != expected_value:
            _, _, line, col = token
            raise SyntaxError(f"Expected '{expected_value}', got '{token[1]}' at line {line}, column {col}")
        
        self.pos += 1
        return token
    
    def parse(self):
        ast = {'type': 'program', 'functions': []}
        
        while self.peek():
            if self.peek()[1] == 'fn':
                ast['functions'].append(self.parse_function())
            else:
                token = self.peek()
                _, _, line, col = token
                raise SyntaxError(f"Unexpected token {token[1]} at line {line}, column {col}")
        
        return ast
    
    def parse_function(self):
        self.consume('KEYWORD', 'fn')
        name_token = self.consume('IDENT')
        name = name_token[1]
        self.consume('LPAR', '(')
        self.consume('RPAR', ')')
        body = self.parse_block()
        return {'type': 'function', 'name': name, 'body': body, 'line': name_token[2]}
    
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
            _, _, line, col = token
            raise SyntaxError(f"Unexpected statement {token[1]} at line {line}, column {col}")
    
    def parse_var_decl(self):
        mutable_token = self.consume('KEYWORD')
        name_token = self.consume('IDENT')
        name = name_token[1]
        line = name_token[2]
        
        explicit_type = None
        if self.peek() and self.peek()[1] == ':':
            self.consume('COLON', ':')
            type_token = self.consume('TYPE')
            explicit_type = type_token[1]
        
        value = None
        if self.peek() and self.peek()[1] == '=':
            self.consume('ASSIGN', '=')
            value = self.parse_logic()
        
        self.consume('SEMI', ';')
        
        return {
            'type': 'var_decl',
            'mutable': mutable_token[1],
            'name': name,
            'explicit_type': explicit_type,
            'value': value,
            'line': line
        }
    
    def parse_print(self):
        println_token = self.consume('KEYWORD', 'println')
        line = println_token[2]
        self.consume('LPAR', '(')
        
        args = []
        if self.peek() and self.peek()[1] != ')':
            args.append(self.parse_logic())
            while self.peek() and self.peek()[1] == ',':
                self.consume('COMMA', ',')
                args.append(self.parse_logic())
        
        self.consume('RPAR', ')')
        self.consume('SEMI', ';')
        return {'type': 'print', 'args': args, 'line': line}
    
    def parse_logic(self):
        node = self.parse_comparison()
        while self.peek() and self.peek()[1] in ('&&', '||'):
            op_token = self.consume()
            op = op_token[1]
            right = self.parse_comparison()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        return node
    
    def parse_comparison(self):
        node = self.parse_expr()
        while self.peek() and self.peek()[1] in ('==', '!=', '<', '>'):
            op_token = self.consume()
            op = op_token[1]
            right = self.parse_expr()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        return node
    
    def parse_expr(self):
        node = self.parse_term()
        while self.peek() and self.peek()[1] in ('+', '-'):
            op_token = self.consume()
            op = op_token[1]
            right = self.parse_term()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        return node
    
    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek()[1] in ('*', '/'):
            op_token = self.consume()
            op = op_token[1]
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
        elif token[0] == 'KEYWORD' and token[1] in ('true', 'false'):
            self.consume('KEYWORD')
            return {'type': 'bool', 'value': token[1]}
        elif token[1] == '(':
            self.consume('LPAR', '(')
            expr = self.parse_logic()
            self.consume('RPAR', ')')
            return expr
        else:
            _, _, line, col = token
            raise SyntaxError(f"Unexpected expression {token[1]} at line {line}, column {col}")

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
        print(f"Функция: {func['name']} (строка {func['line']})")
        for stmt in func['body']['statements']:
            if stmt and stmt['type'] == 'var_decl':
                print(f"  Переменная: {stmt['name']} (строка {stmt['line']}), тип: {stmt['explicit_type']}, значение: {stmt['value']}")
            elif stmt and stmt['type'] == 'print':
                print(f"  println (строка {stmt['line']})")