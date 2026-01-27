#!/usr/bin/env python3
# rail_compiler/compiler.py
import sys
import os
from lexer import tokenize
from parser import Parser
from codegen import generate_c

def compile_rail(source_code, input_filename="<stdin>"):
    """Основная функция компиляции"""
    try:
        tokens = tokenize(source_code)
        parser = Parser(tokens)
        ast = parser.parse()
        return generate_c(ast)
    except Exception as e:
        # Добавляем информацию о файле в ошибку
        raise Exception(f"Compilation error in {input_filename}: {e}")

def get_source_code():
    """Определяет, откуда брать исходный код с поддержкой мобильной разработки"""
    
    # Режим 1: Компиляция из файла (если передан аргумент)
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            sys.exit(f"Error: File '{filename}' not found.")
        with open(filename, 'r') as f:
            return f.read(), filename
    
    # Режим 2: Интерактивный ввод (для телефона)
    print("=== Rail Compiler (Interactive Mode) ===")
    print("Enter your Rail code line by line.")
    print("Type 'end' on a separate line to finish.")
    print("-" * 40)
    
    lines = []
    line_number = 1
    
    while True:
        try:
            # Показываем номер строки для удобства
            prompt = f"[{line_number:3d}] > "
            line = input(prompt)
            
            # Проверяем маркер завершения
            if line.strip().lower() == "end":
                break
            
            lines.append(line)
            line_number += 1
            
        except KeyboardInterrupt:
            print("\n\nCompilation cancelled.")
            sys.exit(0)
        except EOFError:
            print("\nUnexpected end of input.")
            break
    
    # Объединяем все строки
    source_code = '\n'.join(lines)
    
    if not source_code.strip():
        print("No code provided. Using example...")
        source_code = """fn main() {
    var x = 10;
    println("Hello Rail!", x);
}"""
    
    return source_code, "<interactive>"

def main():
    # Получаем исходный код
    source_code, input_name = get_source_code()
    
    if not source_code.strip():
        sys.exit("Error: No code to compile.")
    
    try:
        # Компилируем
        c_code = compile_rail(source_code, input_name)
        
        # Сохраняем результат
        output_file = "output.c"
        with open(output_file, "w") as f:
            f.write(c_code)
        
        print("-" * 40)
        print(f"✅ Successfully compiled to: {output_file}")
        print(f"📊 Statistics:")
        print(f"   • Input lines: {len(source_code.splitlines())}")
        print(f"   • C code size: {len(c_code)} characters")
        print(f"   • Output file: {output_file}")
        
        # Показываем превью C-кода
        print("\n📝 Generated C code preview:")
        print("-" * 30)
        c_lines = c_code.splitlines()[:5]  # Первые 5 строк
        for line in c_lines:
            print(f"  {line}")
        if len(c_code.splitlines()) > 5:
            print(f"  ... and {len(c_code.splitlines()) - 5} more lines")
        
        # Инструкция по сборке
        print("\n🔧 To compile and run:")
        print(f"   gcc {output_file} -o program")
        print("   ./program")
        
    except Exception as e:
        print("-" * 40)
        print(f"❌ Compilation failed:")
        print(f"   Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()