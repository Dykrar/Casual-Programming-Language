

tokens = (
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS', 'COMP',
    'LPAREN','RPAREN','AND','OR','NOT_EQUALS',
    'GREATER_OR_EQUAL','LESS_OR_EQUALS','GREATER','LESS',
    'MODULO','TRUE','FALSE','INT','FLOAT','STRING',
    'VARIABLE','DECL','DEF', 'RETURN','IF','ELSE', 'WHILE',
    'COLON', 'SEMICOLONS', 'LRPARN', 'RRPAREN', 'LBRACKET', 'RBRACKET',
    'INT_TYPE','FLOAT_TYPE', 'STRING_TYPE', 'BOOL_TYPE', 'GET_ARRAY', 'NOT', 'VOID_TYPE','COMMA'
)


t_PLUS              = r'\+'
t_MINUS             = r'-'
t_TIMES             = r'\*'
t_DIVIDE            = r'/'
t_EQUALS            = r'='
t_COMP              = r'=='
t_LPAREN            = r'\('
t_RPAREN            = r'\)'
t_AND               = r'&&'
t_OR                = r'\|\|'
t_NOT_EQUALS        = r'!='
t_GREATER_OR_EQUAL  = r'\>='
t_LESS_OR_EQUALS    = r'\<='
t_GREATER           = r'\>'
t_LESS              = r'\<'
t_MODULO            = r'%' 
t_VARIABLE          = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_STRING            = r'\"(([a-zA-Z]+[\\]?[a-zA-Z]+)|([a-zA-Z]*))\"'
t_COMMA             = r',' 
t_COLON             = r':'
t_SEMICOLONS        = r';'
t_LRPARN            = r'\['
t_RRPAREN           = r'\]'
t_LBRACKET          = r'\{'
t_RBRACKET          = r'\}'
t_NOT               = r'!'

def t_INT_TYPE(t):
    r'Int'
    return t

def t_FLOAT_TYPE(t):
    r'Float'
    return t

def t_STRING_TYPE(t):
    r'String'
    return t
    
def t_BOOL_TYPE(t):
    r'Boolean'
    return t
    
def t_VOID_TYPE(t):
    r'Void'
    return t

def t_GET_ARRAY(t):
    r'get_array()'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_IF(t):
    r'if'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_RETURN(t):
    r'return'
    return t

def t_DECL(t):
    r'decl'
    return t

def t_DEF(t):
    r'def'
    return t

def t_FLOAT(t):
    r'([0-9]*[.])[0-9]+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        t.value = 0
    return t

def t_INT(t):
    r'[0-9][0-9_]*[0-9]|[0-9]+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'

precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc','LESS_OR_EQUALS','GREATER_OR_EQUAL','GREATER','LESS','COMP','NOT_EQUALS','NOT'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MODULO'),    
    ('right','UMINUS'),
    )

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


import ply.lex as lex
import sys

lexer = lex.lex()

def p_program(t):
    '''program : declaration program
               | definition program
               | declaration
               | definition '''

def p_empty(t):
    'empty : '

def p_declaration(t):
    '''declaration : DECL VARIABLE LPAREN RPAREN COLON type
                   | DECL VARIABLE LPAREN arg RPAREN COLON type'''

def p_definition(t):
    '''definition : DEF VARIABLE LPAREN arg RPAREN COLON type block return
                  | DEF VARIABLE LPAREN RPAREN COLON type block return'''

def p_arg(t):
    '''arg : VARIABLE COLON type
           | VARIABLE COLON type COMMA arg'''

def p_block(t):
    'block : LBRACKET block_content_check RBRACKET'

def p_block_content_check(t):
    ''' block_content_check : block_content block_content_check
                            | empty'''
def p_block_content(t):
    '''block_content : return  
                     | stat_expression 
                     | if 
                     | if_else 
                     | while 
                     | var_decl 
                     | var_ass'''

def p_return(t):
    '''return : RETURN SEMICOLONS
              | RETURN expression SEMICOLONS'''

def p_stat_expression(t):
    'stat_expression : expression SEMICOLONS '

def p_if(t):
    'if : IF expression block'

def p_if_else(t):
    'if_else : if ELSE block'

def p_while(t):
    'while : WHILE expression block'
                
def p_variable_declar(t):
    'var_decl : VARIABLE COLON type EQUALS expression SEMICOLONS'
                                  
def p_variable_type(t):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE
            | VOID_TYPE'''

def p_variable_assign(t):
    'var_ass : VARIABLE EQUALS expression SEMICOLONS'

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression COMP expression
                  | expression AND expression
                  | expression OR expression
                  | expression NOT_EQUALS expression
                  | expression GREATER_OR_EQUAL expression
                  | expression LESS_OR_EQUALS expression
                  | expression GREATER expression
                  | expression LESS expression
                  | expression MODULO expression'''

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'

def p_expression_number_int(t):
    'expression : INT'
                  
def p_expression_number_float(t):
    'expression : FLOAT'

def p_expression_string(t):
    'expression : STRING'

def p_expression_boolean(t):
    '''expression : TRUE
                  | FALSE'''

def p_expression_variable(t):
    'expression : VARIABLE'

def p_expression_not_unary_op(t):
    'expression : NOT expression'

def p_expression_index(t):
    '''expression : VARIABLE LRPARN expression RRPAREN  
                  | GET_ARRAY LRPARN expression RRPAREN '''

def p_expression_fun_invocation(t):
    'expression : VARIABLE LPAREN arg_f RPAREN'

def p_arg_f(t):
    '''arg_f : VARIABLE 
             | VARIABLE COMMA arg_f'''



def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def p_error(t):
    if t is not None:
        columnno = find_column(f_code, t)
        print("Syntax error at '%s (line %s, column %s)" % (t.value, t.lineno, columnno))
    else:
        print("No Input detected - File empty")

import ply.yacc as yacc
parser = yacc.yacc()

try:
    if len(sys.argv) < 2:
        print("There isn't a file to read")
    else:
        file = open(sys.argv[1])
        f_code = file.read()
        p = parser.parse(f_code)
except EOFError:
    print("File could not be opened")

