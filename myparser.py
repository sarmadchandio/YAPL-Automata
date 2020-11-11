import lexer
import ply.lex as lex
# from lexer import tokens

tokens = lexer.tokens


precedence = (
    ('left', 'ANDAND', 'OROR'),
    ('left', 'EQUALEQUAL', 'NOTEQUAL'),
    ('left', 'GE', 'GT', 'LE', 'LT'),
    ('left', 'NOT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'POWER', 'MODULO'),
    ('left', 'LPAREN', 'RPAREN'),
    ('right', 'UMINUS')
)

start="stmtS"

def p_stmtS(p):
    '''
    stmtS : stmt SEMICOLON stmtS
    '''
    # print("stmtS: ", p[1], p[2], p[3])
    p[0] = [p[1]] + p[3]

def p_empty_stmtS(p):
    'stmtS : '
    p[0] = []

def p_do_while(p):
    '''
    stmt : DO LBRACE stmtS RBRACE WHILE LPAREN exp RPAREN
    '''
    p[0] = ('do-while', (p[3], p[7]))


def p_struct_define(p):
    ' stmt : STRUCT IDENTIFIER LBRACE stmtS RBRACE'
    p[0] = ('struct-define', p[2], p[4])


def p_stmt(p):
    '''stmt : print
            | new_assign
            | re_assign
            | declare
            | struct_cons
            | s_attr
            | exp
    '''
    # print("stmt", p[1])
    p[0] = ('stmt', p[1])

def p_struct_construct(p):
    ' struct_cons : STRUCT IDENTIFIER IDENTIFIER'
    p[0] = ('struct-construct', p[2], p[3])

def p_struct_attribute(p):
    ''' s_attr : IDENTIFIER DOT IDENTIFIER '''
    p[0] = ('struct-attribute', p[1], p[3])

# def p_if_else(p):
#     ''' stmt : IF exp compound_stmt   
#              | IF exp compound_stmt ELSE compound_stmt
#     '''
#     p[0] = ('if-then-else', p[1], p[2])

# def p_paren_compound_stmt(p):
#     '''
#     compound_stmt : LBRACE stmt RBRACE
#     ''' 
#     p[0] = ('compound_stmt', [p[2]])

# Assign a var
def p_new_assign(p):
    'new_assign : dtype IDENTIFIER EQUAL exp'
    p[0] = ('new_assign', p[1],p[2], p[4])

def p_struct_reassign(p):
    ' re_assign : s_attr EQUAL exp'
    p[0] = ('re_assign', p[1][1]+'.'+p[1][2], p[3])
# re-assign a variable
def p_re_assign(p):
    '''
    re_assign  : IDENTIFIER EQUAL exp
    '''
    # print("id = exp")
    p[0] = ('re_assign', p[1],p[3])
# declare a var
def p_declare(p):
    '''
    declare : dtype IDENTIFIER
    '''
    # print("dt id")
    p[0] = ('declare', p[1], p[2])


def p_dtype(p):
    ''' 
    dtype : DTYPE_INT
          | DTYPE_DOUBLE
          | DTYPE_BOOL
          | DTYPE_STRING
          | DTYPE_CHAR
    '''
    # print("Dtype-{}".format(p[1]))
    p[0] = p[1]

# print func
def p_print(p):
    ' print : PRINT LPAREN arg RPAREN '
    p[0] = ('print', p[3])

def p_args(p):
    ' arg : arg COMMA arg'
    # print("arg1: {} arg2: {}".format(p[1], p[3]))
    p[0] = []+p[1]+p[3]
    # print("Appended: {}\n".format(p[0]))

def p_arg_empty(p):
    ' arg : '
    p[0] = []
def p_arg(p):
    ''' arg : exp '''
    p[0] = [p[1]]

def p_binop(p):
    ''' 
    exp : exp PLUS exp
        | exp MINUS exp
        | exp TIMES exp
        | exp DIVIDE exp
        | exp ANDAND exp
        | exp OROR exp
        | exp EQUALEQUAL exp
        | exp GT exp
        | exp GE exp
        | exp LT exp
        | exp LE exp
        | exp NOTEQUAL exp
        | exp POWER exp
        | exp MODULO exp

    '''
    # print('binop', p[1], p[2], p[3])
    p[0] = ('binop', p[1], p[2], p[3])

def p_expr_sattr(p):
    ' exp : s_attr '
    p[0] = p[1]

def p_unary(p):
    ''' 
    exp : exp PLUSPLUS
        | exp MINUSMINUS
    '''
    # print('uniary')
    p[0] = ('unary', p[1], p[2])

def p_name(p):
    ' exp : IDENTIFIER'
    # print("ident_expre")
    p[0] = ('identifier', p[1])

def p_exp_string(p):
    ' exp : STRING '
    # print('expstring')
    p[0] = ('string', p[1])
def p_exp_char(p):
    ' exp : CHAR '
    # print('expchar')
    p[0] = ('char', p[1])
def p_exp_number(p):
    ''' 
    exp  : INT
         | DOUBLE
    '''
    # print('expnumber')
    p[0] = ('number', p[1])

def p_exp_not(p):
    ' exp : NOT exp '
    p[0] = ('unary', p[2], '!')
    # print('not!', p[0])

def p_expr_uminus(p):
     'exp : MINUS exp %prec UMINUS'
     p[0] = ('unary', p[2], '-')
    
def p_exp_boolean(p):
    '''
        exp : TRUE
            | FALSE
    '''
    if p[1]=="True":
        p[1] = True
    else:
        p[1] = False
    
    p[0] = ('bool', p[1])
    # print('exp-bool', p[0])

def p_exp(p):
    'exp : LPAREN exp RPAREN'
    # print("exp: parenthehsis")
    p[0] = p[2]


def p_error(p):
    print("Syntax Error in Input", p)


# import ply.yacc as yacc
# val = """ string a=("hi") + "bo"; """
# myLexer = lex.lex(module=lexer)
# parser = yacc.yacc()
# myLexer.input(val)
# while True:
#     token = myLexer.token()
#     if not token:
#         break
#     print(token)
# parsed = parser.parse(val, lexer=myLexer)
# print("parsed: ", parsed)


