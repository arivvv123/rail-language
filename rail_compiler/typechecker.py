# rail_compiler/typechecker.py
class TypeChecker:
    def __init__(self):
        self.symbol_table = {}  # Имя переменной -> её тип
        
    def check(self, ast):
        """Основной метод проверки всей программы"""
        for func in ast['functions']:
            self.check_function(func)
        return True  # Если дошли сюда без ошибок
    
    def check_function(self, func):
        """Проверяет одну функцию"""
        # Временно очищаем таблицу символов для каждой функции
        local_table = {}
        self.symbol_table = local_table
        
        # Проверяем тело функции
        self.check_block(func['body'])
        
        # Восстанавливаем (пока нет глобальных переменных)
        self.symbol_table = {}
    
    def check_block(self, block):
        """Проверяет блок statements"""
        for stmt in block['statements']:
            if stmt:
                self.check_statement(stmt)
    
    def check_statement(self, stmt):
        """Проверяет statement и возвращает его тип (если есть)"""
        if stmt['type'] == 'var_decl':
            return self.check_var_decl(stmt)
        elif stmt['type'] == 'print':
            return self.check_print(stmt)
        return None
    
    def check_var_decl(self, decl):
        """Проверяет объявление переменной"""
        var_name = decl['name']
        var_type = self.infer_expr_type(decl['value'])
        
        # Сохраняем тип переменной в таблице символов
        self.symbol_table[var_name] = var_type
        return var_type
    
    def check_print(self, stmt):
        """Проверяет аргументы println"""
        for arg in stmt['args']:
            self.infer_expr_type(arg)
        return None
    
    def infer_expr_type(self, expr):
        """Выводит тип выражения. Выбрасывает ошибку при несовместимости."""
        if expr['type'] == 'number':
            return 'int'
        elif expr['type'] == 'string':
            return 'string'
        elif expr['type'] == 'bool':
            return 'bool'
        elif expr['type'] == 'ident':
            # Ищем переменную в таблице символов
            if expr['value'] in self.symbol_table:
                return self.symbol_table[expr['value']]
            raise TypeError(f"Undefined variable: {expr['value']}")
        elif expr['type'] == 'binop':
            return self.check_binop(expr)
        else:
            raise TypeError(f"Unknown expression type: {expr['type']}")
    
    def check_binop(self, expr):
        """Проверяет бинарную операцию"""
        left_type = self.infer_expr_type(expr['left'])
        right_type = self.infer_expr_type(expr['right'])
        op = expr['op']
        
        # Таблица допустимых операций
        valid_ops = {
            ('int', 'int'): ['+', '-', '*', '/', '==', '!=', '<', '>'],
            ('bool', 'bool'): ['&&', '||', '==', '!='],
            ('string', 'string'): ['==', '!='],
        }
        
        # Проверяем совместимость типов
        type_pair = (left_type, right_type)
        
        if type_pair not in valid_ops:
            raise TypeError(f"Invalid operation between {left_type} and {right_type}")
        
        if op not in valid_ops[type_pair]:
            raise TypeError(f"Operator '{op}' not supported for {left_type}")
        
        # Определяем тип результата
        if op in ['&&', '||']:
            return 'bool'
        elif op in ['==', '!=', '<', '>']:
            return 'bool'
        else:
            # Для арифметики сохраняем тип операндов
            return left_type  # int или string (если в будущем конкатенация)