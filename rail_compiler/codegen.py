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
                formats.append("%s")
                args.append(arg_c)
            else:
                formats.append("%d")
                args.append(arg_c)
        
        format_str = '"' + " ".join(formats) + '\\n"'
        return f'printf({format_str}, {", ".join(args)});'
    
    return ""

def generate_expr(expr):
    if expr['type'] == 'string':
        return expr['value']  # Уже в кавычках
    return expr['value']
