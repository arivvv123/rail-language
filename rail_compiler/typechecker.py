class TypeChecker:
    def __init__(self):
        self.symbol_table = {}
    
    def check(self, ast):
        for func in ast['functions']:
            self.check_function(func)
        return True
    
    def check_function(self, func):
        local_table = {}
        self.symbol_table = local_table
        try:
            self.check_block(func['body'])
        except TypeError as e:
            # Добавляем позицию функции, если её нет в ошибке
            if 'line' in func:
                raise TypeError(f"{e} (in function '{func['name']}' at line {func['line']})")
            raise
        self.symbol_table = {}
    
    def check_block(self, block):
        for stmt in block['statements']:
            if stmt:
                self.check_statement(stmt)
    
    def check_statement(self, stmt):
        if stmt['type'] == 'var_decl':
            return self.check_var_decl(stmt)
        elif stmt['type'] == 'print':
            return self.check_print(stmt)
        return None
    
    def check_var_decl(self, decl):
        var_name = decl['name']
        line = decl.get('line', 'unknown')
        
        # Если есть значение, выводим тип
        inferred_type = None
        if decl['value']:
            try:
                inferred_type = self.infer_expr_type(decl['value'])
            except TypeError as e:
                raise TypeError(f"{e} (in variable '{var_name}' at line {line})")
        
        explicit_type = decl.get('explicit_type')
        
        # Проверка на соответствие типов
        if explicit_type and inferred_type:
            if explicit_type != inferred_type:
                raise TypeError(
                    f"Type mismatch in variable '{var_name}' at line {line}: "
                    f"declared as {explicit_type} but got {inferred_type}"
                )
        
        # Если нет значения, но есть явный тип — ок
        # Если нет значения и нет явного типа — ошибка
        if not explicit_type and not inferred_type:
            raise TypeError(
                f"Cannot infer type for variable '{var_name}' at line {line}. "
                f"Please specify type explicitly."
            )
        
        # Сохраняем тип
        final_type = explicit_type or inferred_type
        self.symbol_table[var_name] = final_type
        return final_type
    
    def check_print(self, stmt):
        line = stmt.get('line', 'unknown')
        for arg in stmt['args']:
            try:
                self.infer_expr_type(arg)
            except TypeError as e:
                raise TypeError(f"{e} (in println at line {line})")
        return None
    
    def infer_expr_type(self, expr):
        if expr['type'] == 'number':
            return 'int'
        elif expr['type'] == 'string':
            return 'string'
        elif expr['type'] == 'bool':
            return 'bool'
        elif expr['type'] == 'ident':
            var_name = expr['value']
            if var_name in self.symbol_table:
                return self.symbol_table[var_name]
            raise TypeError(f"Undefined variable: '{var_name}'")
        elif expr['type'] == 'binop':
            return self.check_binop(expr)
        else:
            raise TypeError(f"Unknown expression type: {expr['type']}")
    
    def check_binop(self, expr):
        try:
            left_type = self.infer_expr_type(expr['left'])
            right_type = self.infer_expr_type(expr['right'])
        except TypeError as e:
            raise TypeError(f"In binary operation: {e}")
        
        op = expr['op']
        
        valid_ops = {
            ('int', 'int'): ['+', '-', '*', '/', '==', '!=', '<', '>'],
            ('bool', 'bool'): ['&&', '||', '==', '!='],
            ('string', 'string'): ['==', '!='],
        }
        
        type_pair = (left_type, right_type)
        
        if type_pair not in valid_ops:
            raise TypeError(
                f"Invalid operation between {left_type} and {right_type} "
                f"(operator '{op}')"
            )
        
        if op not in valid_ops[type_pair]:
            raise TypeError(
                f"Operator '{op}' not supported for {left_type}"
            )
        
        if op in ['&&', '||', '==', '!=', '<', '>']:
            return 'bool'
        else:
            return left_type

if __name__ == "__main__":
    from lexer import tokenize
    from parser import Parser
    
    print("=== Тест проверки типов с позициями ===")
    
    # Корректный код
    code_ok = """
    fn main() {
        var x: int = 10;
        val name: string = "Rail";
        var flag: bool = true;
        println(x, name, flag);
    }
    """
    tokens = tokenize(code_ok)
    parser = Parser(tokens)
    ast = parser.parse()
    typechecker = TypeChecker()
    try:
        typechecker.check(ast)
        print("✅ OK: типы совпадают")
    except TypeError as e:
        print(f"❌ Ошибка: {e}")
    
    # Некорректный код с ошибкой типа
    code_bad = """
    fn main() {
        var x: int = true;
    }
    """
    tokens = tokenize(code_bad)
    parser = Parser(tokens)
    ast = parser.parse()
    typechecker = TypeChecker()
    try:
        typechecker.check(ast)
        print("❌ Ошибка не поймана (плохо)")
    except TypeError as e:
        print(f"✅ Ошибка поймана: {e}")
    
    # Некорректный код с необъявленной переменной
    code_undef = """
    fn main() {
        var x: int = y;
    }
    """
    tokens = tokenize(code_undef)
    parser = Parser(tokens)
    ast = parser.parse()
    typechecker = TypeChecker()
    try:
        typechecker.check(ast)
        print("❌ Ошибка не поймана (плохо)")
    except TypeError as e:
        print(f"✅ Ошибка поймана: {e}")