#!/usr/bin/env python3
# rail_compiler/compiler.py
import sys
from lexer import tokenize
from parser import Parser
from codegen import generate_c

def compile_rail(source_code):
    """Основная функция компиляции"""
    tokens = tokenize(source_code)
    parser = Parser(tokens)
    ast = parser.parse()
    return generate_c(ast)

def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
    else:
        code = """fn main() {
    var x = 10;
    println("Hello Rail!", x);
}"""
    
    c_code = compile_rail(code)
    print(c_code)
    
    # Можно сохранить в файл
    with open("output.c", "w") as f:
        f.write(c_code)

if __name__ == "__main__":
    main()
