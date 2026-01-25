# rail_compiler/lexer.py
import re

TOKEN_SPEC = [
    ('KEYWORD', r'\b(fn|var|val|println|if|else|for|while|return)\b'),
    ('NUMBER',  r'\b\d+\b'),
    ('STRING',  r'"[^"]*"'),
    ('IDENT',   r'[a-zA-Z_]\w*'),
    ('LPAR',    r'\('),
    ('RPAR',    r'\)'),
    ('LBRACE',  r'\{'),
    ('RBRACE',  r'\}'),
    ('COMMA',   r','),
    ('SEMI',    r';'),
    ('PLUS',    r'\+'),
    ('MINUS',   r'-'),
    ('MUL',     r'\*'),
    ('DIV',     r'/'),
    ('ASSIGN',  r'='),
    ('GT',      r'>'),
    ('LT',      r'<'),
    ('EQ',      r'=='),
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
    test = 'var x = a + 5 * 2;'
    print(tokenize(test))
