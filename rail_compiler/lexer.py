# rail_compiler/lexer.py
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
    ('COLON',   r':'),  # НОВОЕ: для явных типов

    # Скобки и пунктуация
    ('LPAR',    r'\('),
    ('RPAR',    r'\)'),
    ('LBRACE',  r'\{'),
    ('RBRACE',  r'\}'),
    ('COMMA',   r','),
    ('SEMI',    r';'),

    # Пропускаем комментарии и пробелы
    ('SKIP',    r'#.*|\s+'),
]

def tokenize(code):
    tokens = []
    pos = 0
    regexes = [(name, re.compile(pattern)) for name, pattern in TOKEN_SPEC]
    
    while pos < len(code):
        match = None
        for name, regex in regexes:
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if name != 'SKIP':
                    tokens.append((name, text))
                pos = match.end()
                break
        
        if not match:
            raise SyntaxError(f"Invalid char: {code[pos]}")
    
    return tokens

if __name__ == "__main__":
    test_code = 'var x: int = 10;'
    print("Тестируем:", test_code)
    for tok in tokenize(test_code):
        print(f"  {tok}")