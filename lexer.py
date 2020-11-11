import ply.lex as lex



reserved = {
    'print' : 'PRINT',
    # 'else'  : 'ELSE',
    # 'if'    : 'IF'  ,
    # 'then'  : 'THEN' ,
    # 'for'   : 'FOR' ,
    'do'    : 'DO',
    'while' : 'WHILE' ,
    'struct': 'STRUCT',
    # 'var'   : 'VAR' ,
    'True'  : 'TRUE' ,
    'False' : 'FALSE' ,
    # 'return' : 'RETURN' ,
    # 'function' : 'FUNCTION',
    'bool'  : 'DTYPE_BOOL',
    'int'   : 'DTYPE_INT',
    'double' : 'DTYPE_DOUBLE',
    'string' : 'DTYPE_STRING',
    'char'  : 'DTYPE_CHAR',
}

# Some tokens taken from the jstokens.py provided by sir Hammad
tokens = [

        'INT',          # int
        'DOUBLE',       # double
        'STRING',       # string
        'CHAR',         # char
        # 'NUMBER'        # number (can be int or float)
        'ANDAND',       # &&
        'NOT',          # !
        'OROR',         # ||
        'COMMA',        # ,
        'LBRACE',       # {
        'LPAREN',       # (
        'EQUAL',        # =
        'EQUALEQUAL',   # ==
        'NOTEQUAL',     # !=
        'GE',           # >=
        'GT',           # >
        'LT',           # <
        'LE',           # <=
        'RPAREN',       # )
        'RBRACE',       # }
        'IDENTIFIER',   # Name of variables
        'SEMICOLON',    # ;
        'PLUS',         # +
        'MINUS',        # -
        'DIVIDE',       # /
        'TIMES',        # *
        'POWER',        # ^
        'MODULO',       # %
        'PLUSPLUS',     # ++
        'MINUSMINUS',   # --
        'NEWLINE',      # \n
        'DOT',          # . operator for structs
] + list(reserved.values())

t_NEWLINE = r'\n'
t_DOT = r'\.'
t_ANDAND =  r'&&'
t_NOTEQUAL = r'!='
t_COMMA =  r','
t_DIVIDE =  r'/'
t_EQUALEQUAL = r'=='
t_EQUAL = r'='
t_GE =  r'>='
t_GT =   r'>'
t_LBRACE = r'\{'
t_LE =  r'<='
t_LPAREN =   r'\('
t_LT = r'<'
t_MINUS = r'-'
t_NOT = r'!'
t_OROR = r'\|\|'
t_PLUSPLUS = r'\+\+'
t_PLUS = r'\+'
t_RBRACE =  r'\}'
t_RPAREN =  r'\)'
t_SEMICOLON =   r';'
t_TIMES = r'\*'
t_POWER = r'\^'

# states = ( 
#     ( 'singlelinecomment', 'exclusive'),  
#     ('multilinecomment', 'exclusive'), )

# def t_singlelinecomment(t):
#     r'--'
#     t.lexer.begin('singlelinecomment')

# def t_singlelinecomment_end(t):
#     r'\n'
#     t.lexer.begin('INITIAL')

# def t_multilinecomment(t):
#   r'/\*'
#   t.lexer.begin('multilinecomment')

# def t_multilinecomment_end(t):
#   r'\*/'
#   t.lexer.begin('INITIAL')

# t_multilinecomment_ignore = r'.'
# t_singlelinecomment_ignore  = r'.'
# t_multilinecomment_error = r'.'
# t_singlelinecomment_error  = r'.'


t_ignore = ' \t\v\r' # whitespace



def t_newline(t):
        r'\n'
        t.lexer.lineno += 1

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_DOUBLE(token):
        r'-?[0-9]+(?:\.[0-9]*)'
        token.value = float(token.value)
        return token

def t_INT(token):
        r'-?[0-9]+'
        token.value = int(token.value)
        return token

# Returns the type from the list of reseved words and tokens
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'IDENTIFIER')    # Check for reserved words
    return t

def t_STRING(token):
        r'"(?:[^"]|(?:\\.))*"' # r'"(?:[^?\\]|(?:\\.))*"'
        token.value = token.value[1:-1]
        return token

def t_CHAR(token):
    r'\'(?:[^\']|(?:\\.))?\''
    token.value = token.value[1:-1]
    return token
lexer = lex.lex()

# while True:
#     val = input('>>')
#     lexer.input(val)
#     while True:
#         token = lexer.token()
#         if not token:
#             break
#         print(token)
