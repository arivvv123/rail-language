# rail_compiler/lexer.py
import re

TOKEN_SPEC = [
    # Ключевые слова (должны быть до IDENT, чтобы 'if' не распозналось как идентификатор)
    ('KEYWORD', r'\b(fn|var|val|println|if|else|for|while|return|true|false)\b'),

    # Числа и строки
    ('NUMBER',  r'\b\d+\b'),
    ('STRING',  r'"[^"]*"'),

    # Идентификаторы (после ключевых слов)
    ('IDENT',   r'[a-zA-Z_]\w*'),

    # Сравнение и логика: двойные операторы ВЫШЕ одиночных
    ('EQ',      r'=='),  # равно
    ('NEQ',     r'!='),  # не равно
    ('AND',     r'&&'),  # логическое И
    ('OR',      r'\|\|'), # логическое ИЛИ (экранируем '|')

    # Арифметика и скобки
    ('PLUS',    r'\+'),
    ('MINUS',   r'-'),
    ('MUL',     r'\*'),
    ('DIV',     r'/'),
    ('LT',      r'<'),
    ('GT',      r'>'),

    # Одиночные символы (присваивание и унарное НЕ)
    ('ASSIGN',  r'='),   # должно быть ПОСЛЕ '==' и '!='
    ('NOT',     r'!'),   # должно быть ПОСЛЕ '!='

    # Скобки и пунктуация
    ('LPAR',    r'\('),
    ('RPAR',    r'\)'),
    ('LBRACE',  r'\{'),
    ('RBRACE',  r'\}'),
    ('COMMA',   r','),
    ('SEMI',    r';'),

    # Пропускаем комментарии и пробелы (в самом конце)
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

# Для теста
if __name__ == "__main__":
    test_code = 'if (x == 10 && y != 0) { println("ok"); }'
    print("Тестируем:", test_code)
    for tok in tokenize(test_code):
        print(f"  {tok}")