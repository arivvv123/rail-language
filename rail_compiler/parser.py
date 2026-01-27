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
            value = self.parse_logic()  # ИЗМЕНЕНО: было parse_expr()
        
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
            args.append(self.parse_logic())  # ИЗМЕНЕНО: было parse_expr()
            
            while self.peek() and self.peek()[1] == ',':
                self.consume('COMMA', ',')
                args.append(self.parse_logic())  # ИЗМЕНЕНО: было parse_expr()
        
        self.consume('RPAR', ')')
        self.consume('SEMI', ';')
        return {'type': 'print', 'args': args}
    
    # ===== НОВАЯ ИЕРАРХИЯ ПАРСИНГА ВЫРАЖЕНИЙ =====
    def parse_logic(self):
        """Парсит логические операторы && и || (самый низкий приоритет)"""
        node = self.parse_comparison()
        
        while self.peek() and self.peek()[1] in ('&&', '||'):
            op = self.consume()[1]
            right = self.parse_comparison()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        
        return node
    
    def parse_comparison(self):
        """Парсит операторы сравнения ==, !=, <, >"""
        node = self.parse_expr()
        
        while self.peek() and self.peek()[1] in ('==', '!=', '<', '>'):
            op = self.consume()[1]
            right = self.parse_expr()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        
        return node
    
    def parse_expr(self):
        """Парсит сложение и вычитание (+, -)"""
        node = self.parse_term()
        
        while self.peek() and self.peek()[1] in ('+', '-'):
            op = self.consume()[1]
            right = self.parse_term()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        
        return node
    
    def parse_term(self):
        """Парсит умножение и деление (*, /) — высший приоритет"""
        node = self.parse_factor()
        
        while self.peek() and self.peek()[1] in ('*', '/'):
            op = self.consume()[1]
            right = self.parse_factor()
            node = {'type': 'binop', 'op': op, 'left': node, 'right': right}
        
        return node
    
    def parse_factor(self):
        """Парсит атомарные значения и выражения в скобках"""
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
            expr = self.parse_logic()  # Рекурсивно парсим выражение в скобках
            self.consume('RPAR', ')')
            return expr
        else:
            raise SyntaxError(f"Unexpected expression: {token}")

# Тест
if __name__ == "__main__":
    from lexer import tokenize
    
    # Тест 1: Старый пример (должен работать)
    print("=== Тест 1: Старая программа ===")
    code = """
    fn main() {
        var x = 10;
        println("Hello", x);
    }
    """
    tokens = tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse()
    print("✅ AST создан успешно")
    
    # Тест 2: Новые операторы
    print("\n=== Тест 2: Новые операторы ===")
    test_expr = "a == b && c > 5"
    tokens = tokenize(test_expr)
    parser = Parser(tokens)
    try:
        ast = parser.parse_logic()
        print("✅ Выражение распарсено")
        print("   AST:", ast)
    except SyntaxError as e:
        print("❌ Ошибка:", e)
    
    # Тест 3: Приоритет операторов
    print("\n=== Тест 3: Приоритет операторов ===")
    test_expr = "2 + 3 * 4 == 14 && 5 < 10"
    tokens = tokenize(test_expr)
    parser = Parser(tokens)
    try:
        ast = parser.parse_logic()
        print("✅ Приоритеты соблюдены")
        print("   AST:", ast)
    except SyntaxError as e:
        print("❌ Ошибка:", e)