# ---------------------------------------------------------------------------- #
#                          Diogo Rodrigues 55740 FCUL                          #
# ---------------------------------------------------------------------------- #

from collections.abc import Iterable
import casual_verify_semantic as cvs
import casual_compiler as cc
import ply.yacc as yacc
import ply.lex as lex
import sys
import struct 
import re
import subprocess


# ---------------------------------------------------------------------------- #
#                                    TOKENS                                    #
# ---------------------------------------------------------------------------- #

tokens = (
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS', 'COMP',
    'LPAREN','RPAREN','AND','OR','NOT_EQUALS',
    'GREATER_OR_EQUAL','LESS_OR_EQUALS','GREATER','LESS',
    'MODULO','TRUE','FALSE','INT','FLOAT','STRING',
    'VARIABLE','DECL','DEF', 'RETURN','IF','ELSE', 'WHILE',
    'COLON', 'SEMICOLONS', 'LRPAREN', 'RRPAREN', 'LBRACKET', 'RBRACKET',
    'INT_TYPE','FLOAT_TYPE', 'STRING_TYPE', 'BOOL_TYPE', 'GET_ARRAY', 'NOT', 'VOID_TYPE','COMMA','PRINT', 'CREATE_ARRAY', 'LAMBDA'
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
t_STRING            = r'"(([a-zA-Z% \\]*)|[a-zA-Z% \\]+([\\][a-zA-Z% \\]+)+)"'
t_VARIABLE          = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_COMMA             = r',' 
t_COLON             = r':'
t_SEMICOLONS        = r';'
t_LRPAREN           = r'\['
t_RRPAREN           = r']'
t_LBRACKET          = r'\{'
t_RBRACKET          = r'\}'
t_NOT               = r'!'

def t_INT_TYPE(t):
    r'Int'
    return t

def t_LAMBDA(t):
    r'lambda'
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
    r'get_array'
    return t

def t_CREATE_ARRAY(t):
    r'create_array'

def t_PRINT(t):
    r'Print'
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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# ---------------------------------------------------------------------------- #
#                                  PRECEDENCES                                 #
# ---------------------------------------------------------------------------- #

precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc','LESS_OR_EQUALS','GREATER_OR_EQUAL','GREATER','LESS','COMP','NOT_EQUALS','NOT'),
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE', 'MODULO'),    
    ('right','UMINUS'),
    )



# ---------------------------------------------------------------------------- #
#                                    PROGRAM                                   #
# ---------------------------------------------------------------------------- #

start = 'program'

def p_def_declr(t):
    '''def_declr : declaration def_declr
                 | definition def_declr
                 | declaration
                 | definition '''
                 
    if len(t) == 2:
       t[0] = t[1]
    else:
        t[0] = [t[1],t[2]]

def p_program(t):
    '''program : def_declr '''
      
    t[0] = {'nt': 'Program', 'Def_Decl': list(l_helper([t[1]]))}     


# ------------------------ DECLARATION AND DEFINITION ------------------------ #

def p_declaration(t):
    '''declaration : DECL VARIABLE LPAREN varg RPAREN COLON type
                   | DECL VARIABLE LPAREN arg RPAREN COLON type'''

    t[0] = {'nt': 'Declaration', 'F_Name': t[2], 'Argument': list(l_helper([t[4]])), 'Type':t[7]}

def p_definition(t):
    '''definition : DEF VARIABLE LPAREN arg RPAREN COLON type block
                  | DEF VARIABLE LPAREN varg RPAREN COLON type block '''

    t[0] = {'nt': 'Definition', 'F_Name': t[2],'Argument': list(l_helper([t[4]])), 'Type':t[7], 'Block':t[8]}


# --------------------------------- ARGUMENTS -------------------------------- #

def p_varg(t):
    'varg : '
    t[0] = {'nt': 'Void', 'variable_name': 'Void', 'type': 'Void'}


def p_arg(t):
    '''arg : VARIABLE COLON type
           | VARIABLE COLON type COMMA arg'''
    if len(t) == 6:
        t[0] = [{'nt': 'Variable Name', 'variable_name':t[1], 'type': t[3]}, t[5]]
    else:
        t[0] = {'nt': 'Variable Name','variable_name': t[1], 'type':t[3]}

def p_argf(t):
    'argf :'
    t[0] = {'nt': 'Void', 'value': 'Void'}

def p_pre_arg_f(t):
    '''arg_f : expression 
             | expression COMMA arg_f'''

    if len(t) == 4:
        t[0] = [t[1], t[3]]

    else:
        t[0] = t[1]

def p_arg_f(t):
    '''argument_f : arg_f
                  | argf '''

    f_temp = [t[1]]
    t[0] = list(l_helper(f_temp))


# ----------------------------------- BLOCK ---------------------------------- #

def p_block(t):
    '''block : LBRACKET block_content RBRACKET
             | LBRACKET empty RBRACKET'''

    t[0] = list(l_helper([t[2]]))
    

def p_block_content(t):
    ''' block_content : statement block_content
                      | statement'''

    if len(t) == 3 :

        t[0] = [t[1], t[2]]

    else:

       t[0] = [t[1]]



# --------------------------------- STATMENT --------------------------------- #


def p_statement(t):
    '''statement     : return  
                     | stat_expression 
                     | if 
                     | if_else 
                     | while 
                     | var_decl 
                     | var_ass
                     | array_decl
                     | array_ass
                     | print
                     | lambda_expression'''
                     
    t[0] = t[1]


def p_stat_expression(t):
    'stat_expression : expression SEMICOLONS '

    t[0] = {'nt': 'Statement Expression', 'Expression': t[1]}

# ---------------------------------- LAMBDA ---------------------------------- #

def p_lambda(t):
    '''lambda_expression : LAMBDA arg COLON expression 
                         | LAMBDA varg COLON expression'''

    t[0] = {'nt': 'lambda', 'Arguments': list(l_helper([t[2]])), 'Expression': t[4]}



# ----------------------------------- PRINT ---------------------------------- #

def p_print_helper(t):
	'''print_helper : COMMA expression
	                | COMMA expression print_helper'''
	if len(t) == 3:
		t[0] = [t[2]]
	else:
		t[0] = [t[2], t[3]]

def p_statment_print(t):
	'''print : PRINT LPAREN STRING print_helper RPAREN SEMICOLONS
	         | PRINT LPAREN STRING empty RPAREN SEMICOLONS'''
	if t[4] != None:
		t[0] = {'nt': 'Print', 'print_string': t[3], 'print_arguments': list(l_helper(t[4]))}
	else:
		t[0] = {'nt': 'Print', 'print_string': t[3], 'print_arguments': [{'nt': 'Void', 'value': 'Void'}]}

# ---------------------------------- RETURN ---------------------------------- #
    
def p_return(t):
    '''return : RETURN SEMICOLONS
              | RETURN expression SEMICOLONS
              | RETURN lambda_expression SEMICOLONS'''

    if len(t) == 4:
        t[0] = {'nt': 'Return', 'Expression': t[2]}
    else:
        t[0] = {'nt': 'Return', 'Expression': None}

# ------------------------------- IF ELSE WHILE ------------------------------ #

def p_if(t):
    'if : IF expression block'

    t[0] = {'nt':'If', 'Condition': t[2],'Block': t[3]}


def p_if_else(t):
    '''if_else : IF expression block ELSE block'''

    t[0] = {'nt': 'If_Else', 'Condition': t[2], 'Block': t[3], 'Else_block': t[5]}

def p_while(t):
    'while : WHILE expression block'

    t[0] = {'nt':'While', 'Condition' : t[2],'Block' : t[3]}


# ---------------------------------- ARRAYS ---------------------------------- #
                


def p_create_array(t):
    'create_array : CREATE_ARRAY LPAREN expression RPAREN'
    t[0] = {'nt': "Create_Array", 'Array_Size':t[3]}

def p_array_declaration(t):
    '''array_decl : VARIABLE COLON  type LRPAREN expression RRPAREN SEMICOLONS
                  | VARIABLE COLON  type EQUALS create_array SEMICOLONS'''
    t[0] = {'nt': 'Array Declaration', 'name': t[1], 'type':t[3], 'size':t[5]}

def p_array_assign(t):
    'array_ass : VARIABLE LRPAREN expression RRPAREN EQUALS expression SEMICOLONS'
    t[0] = {'nt': 'Array Assignment', 'name': t[1], 'index type':t[3], 'expression':t[6]} 

def p_get_array(t):
    'get_array : GET_ARRAY LRPAREN VARIABLE RRPAREN'
    t[0] = {'nt': 'Get_Array', 'name' :t[3]}


def p_expression_index(t):
    '''expression : VARIABLE LRPAREN expression RRPAREN  
                  | get_array LRPAREN expression RRPAREN'''

    t[0] = {'nt': 'Array', 'name' :t[1], 'Index_Type' : t[3]}



# --------------------------------- VARIABLES -------------------------------- #

def p_variable_declar(t):
    '''var_decl : VARIABLE COLON type EQUALS expression SEMICOLONS
                | VARIABLE COLON type EQUALS lambda_expression SEMICOLONS'''

    t[0] = {'nt':'Variable Declaration', 'Variable Name': t[1], 'type' :t[3], 'Expression' : t[5]}

def p_variable_assign(t):
    '''var_ass : VARIABLE EQUALS expression SEMICOLONS
                | VARIABLE EQUALS lambda_expression SEMICOLONS'''

    t[0] = {'nt': 'Variable Assignment', 'Variable': t[1],'Expression': t[3]}

def p_variable_type(t):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE  
            | VOID_TYPE'''

    t[0] = t[1] 


# -------------------------------- EXPRESSIONS -------------------------------- #

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

    t[0] = {'nt':'Binary Operation','Operator' : t[2], 'Left Parameter': t[1], 'Right Parameter': t[3]}


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'

    t[0] = {'nt' : 'Uminus', 'Valor' :t[2]}

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'

    t[0] = {'nt' : 'Group', 'Valor' : t[2]}

def p_expression_number_int(t):
    'expression : INT'

    t[0] = {'nt': 'Int', 'Value' :t[1]}

def p_expression_number_float(t):
    'expression : FLOAT'

    t[0] = {'nt': 'Float', 'Value' : t[1]}

def p_expression_string(t):
    'expression : STRING'

    t[0] = {'nt': 'String', 'Value': t[1]}

def p_expression_boolean(t):
    '''expression : TRUE
                  | FALSE'''

    t[0] = {'nt': 'Boolean', 'Value': t[1]}

def p_expression_variable(t):
    'expression : VARIABLE'

    t[0] = {'nt':'Variable', 'Value':t[1]}

def p_expression_not_unary_op(t):
    'expression : NOT expression'

    t[0] = {'nt' : 'Not','Value': t[2]}

def p_expression_fun_invocation(t):
    '''expression : VARIABLE LPAREN argument_f RPAREN'''

    t[0] = {'nt': "Function Invocation", 'Function Name': t[1], 'Function Arguments' :t[3]}


def p_empty(t):
    'empty : '

def p_error(t):
    if t is not None:
        columnno = find_column(code, t)
        print("Syntax error at '%s (line %s, column %s)" % (t.value, t.lineno, columnno))
    else:
        print("No Input detected - File empty")


# ---------------------------------------------------------------------------- #
#                                EXTRA FUNCTIONS                               #
# ---------------------------------------------------------------------------- #
 

# ------------------ funcao para descobrir a coluna do erro ------------------ #

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


# ------- funcao Para transformar elementos de uma lista em Dicionarios ------ #

def l_helper(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, dict):
            for i in l_helper(item):
                yield i
        else:
            yield item


# ------------------------------------- - ------------------------------------ #

parser = yacc.yacc()
lexer = lex.lex()

# ---------------------------------------------------------------------------- #
#                                      RUN                                     #
# ---------------------------------------------------------------------------- #

try:
    if len(sys.argv) < 2:
        print("There isn't a file to read")

    else:
        file = open(sys.argv[1])
        code = file.read()
        f_code = parser.parse(code)
        if f_code != None:

            cvs.verify_semantic(cvs.Context(), f_code)

            name = sys.argv[1].split(".cas")

            llvm_code = cc.compilador(f_code)
            print(llvm_code)
            with open(f"{name[0]}.ll", "w") as f:
                f.write(llvm_code)
            
            r = subprocess.call(f"/lib/llvm-10/bin/llc {name[0]}.ll && clang {name[0]}.s -o {name[0]} && ./{name[0]}",shell=True,)

            #print(r)

except EOFError:
    print("File could not be opened")

