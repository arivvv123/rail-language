
# rail_compiler/codegen.py

def generate_c(ast):
    """Генерирует C-код из AST"""
    parts = ["#include <stdio.h>", "#include <stdbool.h>", ""]
    
    for func in ast['functions']:
        parts.append(generate_function(func))
    
    return "\n".join(parts)

def generate_function(func):
    body = generate_block(func['body'])
    return f"int {func['name']}() {{\n{body}\n}}"

def generate_block(block):
    lines = []
    for stmt in block['statements']:
        if stmt:
            lines.append(f"  {generate_statement(stmt)}")
    return "\n".join(lines) if lines else "  // empty"

def generate_statement(stmt):
    if stmt['type'] == 'var_decl':
        c_type = "const int" if stmt['mutable'] == 'val' else "int"
        value = generate_expr(stmt['value'])
        return f"{c_type} {stmt['name']} = {value};"
    
    elif stmt['type'] == 'print':
        if not stmt['args']:
            return 'printf("\\n");'
        
        formats, args = [], []
        for arg in stmt['args']:
            arg_c = generate_expr(arg)
            if arg['type'] == 'string':
                # Убираем кавычки для формата %s
                str_content = arg['value'][1:-1]
                formats.append("%s")
                args.append(f'{str_content}')
            elif arg['type'] == 'bool':
                formats.append("%s")
                args.append(f'({arg_c} ? "true" : "false")')
            else:  # number, ident, binop
                formats.append("%d")
                args.append(arg_c)
        
        format_str = '"' + " ".join(formats) + '\\n"'
        return f'printf({format_str}, {", ".join(args)});'
    
    return ""

def generate_expr(expr):
    """Генерирует C-код для выражения"""
    
    if expr['type'] == 'number':
        return expr['value']
    
    elif expr['type'] == 'string':
        # Возвращаем строку как есть (в кавычках)
        return expr['value']
    
    elif expr['type'] == 'ident':
        return expr['value']
    
    elif expr['type'] == 'bool':
        return "true" if expr['value'] == 'true' else "false"
    
    elif expr['type'] == 'binop':
        left = generate_expr(expr['left'])
        right = generate_expr(expr['right'])
        op = expr['op']
        
        # Маппинг операторов Rail -> C
        c_op = {
            '+': '+', '-': '-', '*': '*', '/': '/',
            '==': '==', '!=': '!=', '<': '<', '>': '>',
            '&&': '&&', '||': '||'
        }.get(op, op)  # Если оператор не найден, используем как есть
        
        return f"({left} {c_op} {right})"
    
    else:
        # На случай, если встретится неизвестный тип
        raise ValueError(f"Unsupported expression type in codegen: {expr['type']}")

# Простой тест
if __name__ == "__main__":
    # Тестовое AST для выражения: (2 + 3) == 5
    test_ast = {
        'type': 'binop',
        'op': '==',
        'left': {
            'type': 'binop',
            'op': '+',
            'left': {'type': 'number', 'value': '2'},
            'right': {'type': 'number', 'value': '3'}
        },
        'right': {'type': 'number', 'value': '5'}
    }
    
    print("Тест генерации выражения:")
    print(generate_expr(test_ast))
    # Ожидаемый вывод: ((2 + 3) == 5)