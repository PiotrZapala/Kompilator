import ply.lex as lex

class Lexer:
    
    tokens = (
        'SEMICOLON', 'ASSIGN', 'PLUS', 'MINUS', 'ASTERISK', 'SLASH', 'PERCENT',
        'EQUAL', 'NO_EQUAL', 'LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL', 
        'LEFT_SQUARE_BRACKET', 'RIGHT_SQUARE_BRACKET', 'LEFT_BRACKET', 'RIGHT_BRACKET', 'COMMA',
        'PROCEDURE', 'PROGRAM', 'IS', 'IN', 'THEN', 'WHILE', 'DO', 'ENDWHILE',
        'IF', 'T', 'ENDIF', 'END', 'ELSE', 'READ', 'WRITE', 'REPEAT', 'UNTIL',
        'NUMBER', 'IDENTIFIER',
    )

    def __init__(self):
        self.lexer = None
        self.lineno = 1
    
    def t_LESS_EQUAL(self, t):
        r'<='
        return t

    def t_GREATER_EQUAL(self, t):
        r'>='
        return t

    def t_EQUAL(self, t):
        r'='
        return t

    def t_NO_EQUAL(self, t):
        r'!='
        return t

    def t_LESS(self, t):
        r'<'
        return t

    def t_GREATER(self, t):
        r'>'
        return t

    def t_SEMICOLON(self, t):
        r'\;'
        return t

    def t_ASSIGN(self, t):
        r':='
        return t

    def t_PLUS(self, t):
        r'\+'
        return t

    def t_MINUS(self, t):
        r'-'
        return t

    def t_ASTERISK(self, t):
        r'\*'
        return t

    def t_SLASH(self, t):
        r'/'
        return t

    def t_PERCENT(self, t):
        r'%'
        return t

    def t_LEFT_SQUARE_BRACKET(self, t):
        r'\['
        return t

    def t_RIGHT_SQUARE_BRACKET(self, t):
        r'\]'
        return t

    def t_LEFT_BRACKET(self, t):
        r'\('
        return t

    def t_RIGHT_BRACKET(self, t):
        r'\)'
        return t

    def t_COMMA(self, t):
        r','
        return t

    def t_PROCEDURE(self, t):
        r'PROCEDURE'
        return t

    def t_PROGRAM(self, t):
        r'PROGRAM'
        return t

    def t_IS(self, t):
        r'IS'
        return t

    def t_IN(self, t):
        r'IN'
        return t
    
    def t_THEN(self, t):
        r'THEN'
        return t

    def t_T(self, t):
        r'T'
        return t

    def t_WHILE(self, t):
        r'WHILE'
        return t

    def t_DO(self, t):
        r'DO'
        return t

    def t_ENDWHILE(self, t):
        r'ENDWHILE'
        return t

    def t_IF(self, t):
        r'IF'
        return t

    def t_ENDIF(self, t):
        r'ENDIF'
        return t

    def t_END(self, t):
        r'END'
        return t

    def t_ELSE(self, t):
        r'ELSE'
        return t

    def t_READ(self, t):
        r'READ'
        return t

    def t_WRITE(self, t):
        r'WRITE'
        return t

    def t_REPEAT(self, t):
        r'REPEAT'
        return t

    def t_UNTIL(self, t):
        r'UNTIL'
        return t
    
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)    
        return t
    
    def t_IDENTIFIER(self, t):
        r'[_a-z]+'
        t.value = str(t.value)
        return t

    def t_NEWLINE(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_ignore_WHITESPACE(self, t):
        r'[ \t\r]+'
        pass

    def t_ignore_COMMENT(self, t):
        r'\#.*'
        pass

    def t_error(self, t):
        print(f"Illegal character '{t.value[0]}'")
        t.lexer.skip(1)
    
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)