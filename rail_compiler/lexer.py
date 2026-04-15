import re

TOKEN_SPEC = [
    # Ключевые слова (должны быть до IDENT)
    ('KEYWORD', r'\b(fn|var|val|println|if|else|for|while|return|true|false)\b'),
    
    # ИМЕНА ТИПОВ (НОВОЕ!)
    ('TYPE', r'\b(int|bool|string)\b'),

    # Числа и строки
    ('NUMBER',  r'\b\d+\b'),
    ('STRING',  r'"[^"]*"'),

    # Идентификаторы (после ключевых слов и типов)
    ('IDENT',   r'[a-zA-Z_]\w*'),

    # Операторы сравнения и логики
    ('EQ',      r'=='),
    ('NEQ',     r'!='),
    ('AND',     r'&&'),
    ('OR',      r'\|\|'),

    # Арифметика
    ('PLUS',    r'\+'),
    ('MINUS',   r'-'),
    ('MUL',     r'\*'),
    ('DIV',     r'/'),
    ('LT',      r'<'),
    ('GT',      r'>'),

    # Одиночные символы
    ('ASSIGN',  r'='),
    ('NOT',     r'!'),
    ('COLON',   r':'),

    # Скобки и пунктуация
    ('LPAR',    r'\('),
    ('RPAR',    r'\)'),
    ('LBRACE',  r'\{'),
    ('RBRACE',  r'\}'),
    ('COMMA',   r','),
    ('SEMI',    r';'),

    # Пропускаем комментарии и пробелы (НО НЕ ПЕРЕВОДЫ СТРОК!)
    ('SKIP',    r'#.*|[ \t]+'),  # пробелы и табы, но не \n
    ('NEWLINE', r'\n'),           # считаем переводы строк отдельно
]

def tokenize(code):
    tokens = []
    pos = 0
    line = 1
    col = 1
    
    # Компилируем регулярки
    regexes = [(name, re.compile(pattern)) for name, pattern in TOKEN_SPEC]
    
    while pos < len(code):
        match = None
        for name, regex in regexes:
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                
                if name == 'NEWLINE':
                    line += 1
                    col = 1
                    pos = match.end()
                    break
                elif name != 'SKIP':
                    # Сохраняем токен с позицией
                    tokens.append((name, text, line, col))
                    col += len(text)
                    pos = match.end()
                    break
                else:
                    # SKIP (пробелы, табы, комментарии) — просто увеличиваем колонку
                    col += len(text)
                    pos = match.end()
                    break
        
        if not match:
            raise SyntaxError(f"Invalid character '{code[pos]}' at line {line}, column {col}")
    
    return tokens

if __name__ == "__main__":
    test_code = 'var x: int = 10;'
    print("Тестируем:", test_code)
    for tok in tokenize(test_code):
        print(f"  {tok}")
    
    print("\nТест с несколькими строками:")
    test_code2 = """fn main() {
    var x: int = 10;
    println(x);
}"""
    for tok in tokenize(test_code2):
        print(f"  {tok}")