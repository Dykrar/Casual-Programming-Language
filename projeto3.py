
from collections.abc import Iterable

import struct 
import re
import subprocess

tokens = (
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS', 'COMP',
    'LPAREN','RPAREN','AND','OR','NOT_EQUALS',
    'GREATER_OR_EQUAL','LESS_OR_EQUALS','GREATER','LESS',
    'MODULO','TRUE','FALSE','INT','FLOAT','STRING',
    'VARIABLE','DECL','DEF', 'RETURN','IF','ELSE', 'WHILE',
    'COLON', 'SEMICOLONS', 'LRPAREN', 'RRPAREN', 'LBRACKET', 'RBRACKET',
    'INT_TYPE','FLOAT_TYPE', 'STRING_TYPE', 'BOOL_TYPE', 'GET_ARRAY', 'NOT', 'VOID_TYPE','COMMA','PRINT'
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
t_LRPAREN           = r'\['
t_RRPAREN           = r']'
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

def p_empty(t):
    'empty : '

def p_declaration(t):
    '''declaration : DECL VARIABLE LPAREN varg RPAREN COLON type
                   | DECL VARIABLE LPAREN arg RPAREN COLON type'''

    t[0] = {'nt': 'Declaration', 'F_Name': t[2], 'Argument': list(l_helper([t[4]])), 'Type':t[7]}

def p_definition(t):
    '''definition : DEF VARIABLE LPAREN arg RPAREN COLON type block
                  | DEF VARIABLE LPAREN varg RPAREN COLON type block '''

    t[0] = {'nt': 'Definition', 'F_Name': t[2],'Argument': list(l_helper([t[4]])), 'Type':t[7], 'Block':t[8]}

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
                     | print'''
                     
    t[0] = t[1]

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
		t[0] = {'nt': 'Print', 'print_string': t[3], 'print_argsuments': [{'nt': 'Void', 'value': 'Void'}]}
    
def p_return(t):
    '''return : RETURN SEMICOLONS
              | RETURN expression SEMICOLONS'''

    if len(t) == 4:
        t[0] = {'nt': 'Return', 'Expression': t[2]}
    else:
        t[0] = {'nt': 'Return', 'Expression': None}

def p_stat_expression(t):
    'stat_expression : expression SEMICOLONS '

    t[0] = {'nt': 'Statement Expression', 'Expression': t[1]}

def p_if(t):
    'if : IF expression block'

    t[0] = {'nt':'If', 'Condition': t[2],'Block': t[3]}


def p_if_else(t):
    '''if_else : IF expression block ELSE block'''

    t[0] = {'nt': 'If_Else', 'Condition': t[2], 'Block': t[3], 'Else_block': t[5]}

def p_while(t):
    'while : WHILE expression block'

    t[0] = {'nt':'While', 'Condition' : t[2],'Block' : t[3]}
                
def p_variable_declar(t):
    'var_decl : VARIABLE COLON type EQUALS expression SEMICOLONS'

    t[0] = {'nt':'Variable Declaration', 'Variable Name': t[1], 'type' :t[3], 'Expression' : t[5]}

def p_array_declaration(t):
    'array_decl : VARIABLE COLON LRPAREN type RRPAREN SEMICOLONS'
    t[0] = {'nt': 'Array Declaration', 'name': t[1], 'type':t[4]}

def p_array_assign(t):
    'array_ass : VARIABLE LRPAREN expression RRPAREN EQUALS expression SEMICOLONS'
    t[0] = {'nt': 'Array Assignment', 'name': t[1], 'index type':t[3], 'expression':t[6]} 

def p_variable_type(t):
    '''type : INT_TYPE
            | FLOAT_TYPE
            | STRING_TYPE
            | BOOL_TYPE  
            | VOID_TYPE'''

    t[0] = t[1] 
def p_variable_assign(t):
    'var_ass : VARIABLE EQUALS expression SEMICOLONS'

    t[0] = {'nt': 'Variable Assignment', 'Variable': t[1],'Expression': t[3]}

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

def p_expression_index(t):
    '''expression : VARIABLE LRPAREN expression RRPAREN  
                  | GET_ARRAY LRPAREN expression RRPAREN '''

    t[0] = {'nt': 'Array', 'Array' :t[1], 'Index' : t[3]}

def p_expression_fun_invocation(t):
    '''expression : VARIABLE LPAREN argument_f RPAREN'''

    t[0] = {'nt': "Function Invocation", 'Function Name': t[1], 'Function Arguments' :t[3]}

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


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

def p_error(t):
    if t is not None:
        columnno = find_column(f_code, t)
        print("Syntax error at '%s (line %s, column %s)" % (t.value, t.lineno, columnno))
    else:
        print("No Input detected - File empty")


def l_helper(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, dict):
            for i in l_helper(item):
                yield i
        else:
            yield item


class TypeError(Exception):
    pass

class Context(object):
    def __init__(self):
        self.stack = [{}]
    
    def get_type(self, name):
        for scope in self.stack:
            if name in scope:
                return scope[name]
        if "Array_" in name:
            varivavel = name.replace("Array_", "")
            raise TypeError(f"Array {varivavel} not in context")
        else:   
            raise TypeError(f"Variable {name} not in context")
    
    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value

    def has_var(self, name):
        for scope in self.stack:
            if name in scope:
                return True
        return False

    def has_var_in_current_scope(self, name):
        return name in self.stack[0]

    def enter_scope(self):
        self.stack.insert(0, {})

    def exit_scope(self):
        self.stack.pop(0)
        
    def print_types(self, types):
        if types == "Int":
            return "%d"
        elif types == "Flaot":
            return "%f"
        elif types == "String":
            return "%s"
        elif types == "%d":
            return "Int"
        elif types == "%f":
            return "Float"
        elif types == "%s":
            return "String"
        else:
            return None

RETURN_CODE = "$ret"

def verify_semantic(ctx:Context, node):
    if node['nt'] == 'Program':

        for Def_declr in node["Def_Decl"]:
            name = Def_declr["F_Name"]
            if ctx.has_var(name):
                raise TypeError(f"Function {name} is already defined in the context.")
            assinatura = (Def_declr["Type"], [par["type"] for par in Def_declr["Argument"]])
            ctx.set_type(name, assinatura)

        for Def_declr in node["Def_Decl"]:
            verify_semantic(ctx, Def_declr)

    elif node['nt'] == "Variable Name":
        name = node["variable_name"]    
        if ctx.has_var_in_current_scope(name):
            raise TypeError(f"Variable {name} is already defined in the context.")    
        ctx.set_type(name, node['Type'])

    elif node['nt'] == "Definition":
        ctx.enter_scope()
        ctx.set_type(RETURN_CODE, node["Type"])

        for argument in node["Argument"]:
            ctx.set_type(argument["variable_name"], argument["type"])

        ctx.enter_scope()
        for Sts in node["Block"]:
            verify_semantic(ctx, Sts)

        ctx.exit_scope()
        ctx.exit_scope()

    elif node['nt'] == "If" or node['nt'] == "While" :
        cond = node["Condition"]
        if verify_semantic(ctx, cond) != "Boolean":
            raise TypeError(f" Condition not boolean")

        ctx.enter_scope()
        for st in node["Block"]:
            verify_semantic(ctx, st)
        ctx.exit_scope()

    elif node['nt'] == "Return":
        if(node["Expression"] == None):
            t = "Void"
        else:
            t = verify_semantic(ctx, node["Expression"])        
        expected_t = ctx.get_type(RETURN_CODE)
        if t != expected_t:
            if t == "Void":
                raise TypeError(f"Return requires {expected_t} expression")
            elif expected_t == "Void":
                raise TypeError(f"Return shouldn't have an expression")
            else:
                raise TypeError(f"Return expected {expected_t} but received {t}")
    elif node["nt"] == "If_Else":
        stat = node["nt"]
        condicao = node["condition"]
        
        if verify_semantic(ctx, condicao) != "Boolean":
            raise TypeError(f"{stat} condition expected Boolean type but got {verify_semantic(ctx, condicao)}")
        
        ctx.enter_scope()
        if node["Block"] != None:
            for statment in node["If_block"]:
                verify_semantic(ctx, statment)
        ctx.exit_scope()
        
        ctx.enter_scope()
        if node["Else_block"] != None:
            for statment in node["Else_block"]:
                verify_semantic(ctx,statment)
            ctx.exit_scope()
  
    

    elif node['nt'] == "Variable Declaration":

        nome = node['Variable Name']
        name = "Array_"+ nome 
        typee = node['type']        
        expr = node['Expression']
        typeeE = verify_semantic(ctx, expr)
        if ctx.has_var_in_current_scope(nome) or ctx.has_var_in_current_scope(name) :
            raise TypeError(f"Variable {nome} is already defined in the context.")  

        if typee != typeeE:
            raise TypeError(f"Variable {nome} is of type {typee} but received type {typeeE}")
        ctx.set_type(nome, node['type'])

    elif node['nt'] == 'Array':
        name = node['Array']
        nome = 'Array_' + name
        array_type = ctx.get_type(nome)
        index = node['Index']
        index_type = verify_semantic(ctx,index)

        if not ctx.has_var(nome):
            raise TypeError(f"Array {name} isn't defined in the context")

        if index_type != 'Int':
            raise TypeError(f"Index of array {name} must be a Int but got {index_type}")
        
        return ctx.get_type(nome)

    elif node['nt'] == "Array Declaration":

        name = node['name'] 
        nome = 'Array_' + name      
        index_type = node['type']

        if ctx.has_var_in_current_scope(name) or ctx.has_var_in_current_scope(name):
            raise TypeError(f"Variable {name} already defined in the context")
        
        ctx.set_type(nome, node['type'])

    elif node['nt'] == 'Array Assignment':
        name = node['name']
        nome = 'Array_' + name
        array_type = ctx.get_type(nome)
        index = node['index type']
        index_type = verify_semantic(ctx,index)
        expression = node['expression']
        expression_type = verify_semantic(ctx,expression)

        if not ctx.has_var(nome):
            raise TypeError(f"Array {name} not defined in the context")

        if index_type != "Int":
            raise TypeError(f"Array {name} Index must be of type Int and not '{index_type}")

        if array_type != expression_type:
            raise TypeError(f"Array {name} type {array_type} don't match the expression type {expression_type}")
        
        return ctx.get_type(nome)

    elif node['nt'] == "Variable Assignment":        
        nome = node['Variable']        
        typee = ctx.get_type(nome)
        expr = node['Expression']
        typeeE = verify_semantic(ctx, expr)
        if not ctx.has_var(nome):
            raise TypeError(f"Variable not defined")
        if typee != typeeE:
            raise TypeError(f"Variable {nome} is of type {typee} but received type{typeeE}")
        return typee
   
    elif node['nt'] == 'Variable':
        name = node["Value"]
        if not ctx.has_var(name):
            raise TypeError(f"Variable {name} isn't defined in the contexto")
        return ctx.get_type(name)

    elif node['nt'] == 'Group':
        return verify_semantic(ctx, node["Valor"])
        
    elif node['nt'] == "Binary Operation":
        
        Operador = node['Operator']
        l_express = node['Left Parameter']
        r_express = node['Right Parameter']

        if Operador == "<" or Operador == ">" or Operador == ">=" or Operador == "<=":
            LType = 'a'
            RType = 'b'

            if(l_express['nt']) == 'Int' or (l_express['nt']) == 'Float' :
                LType =  l_express['nt']

            elif (l_express['nt']) == 'String' or (l_express['nt']) == 'Boolean':

                LType =  l_express['nt']
                raise TypeError(f"The left argument does not support {LType}")

            elif l_express['nt'] == 'Variable':
                name = l_express['Value']
                LType = ctx.get_type(name)

            elif l_express['nt'] == 'Group':                
                LType = verify_semantic(ctx, l_express)
            
            elif l_express['nt'] == 'Function Invocation' or l_express['nt'] == 'Not' or l_express['nt'] == 'Uminus' or l_express['nt'] =='Binary Operation':
                LType = verify_semantic(ctx, l_express)

            if(r_express['nt']) == 'Int' or (r_express['nt']) == 'Float' :
                RType = r_express['nt']

            elif r_express['nt'] == 'String' or (r_express['nt']) == 'Boolean':
                RType = r_express['nt']
                raise TypeError(f"The right argument does not support {RType}")

            elif r_express['nt'] == 'Variable':
                name = r_express['Value']
                RType = ctx.get_type(name)

            elif r_express['nt'] == 'Group':                
                RType = verify_semantic(ctx, r_express)
                
            elif r_express['nt'] == 'Function Invocation' or r_express['nt'] == 'Not' or r_express['nt'] == 'Uminus' or r_express['nt'] =='Binary Operation':
                RType = verify_semantic(ctx, r_express)

            
            if LType == RType:
                return 'Boolean'
            elif LType != RType:
                raise TypeError(f"The operator arguments aren't Boolean")  

        elif Operador == "+" or Operador == "-" or Operador == "*" or Operador == "/":
            LType = 'a'
            RType = 'b'
            if(l_express['nt']) == 'Int' or (l_express['nt']) == 'Float' :
                LType =  l_express['nt']

            elif l_express['nt'] == 'String' or (l_express['nt']) == 'Boolean':

                LType =  l_express['nt']
                raise TypeError(f"The left operator does not support {LType}")

            elif l_express['nt'] == 'Variable':
                name = l_express['Value']
                LType = ctx.get_type(name)

            elif l_express['nt'] == 'Group':                
                LType = verify_semantic(ctx, l_express)
            
            elif l_express['nt'] == 'Function Invocation' or l_express['nt'] == 'Not' or l_express['nt'] == 'Uminus' or l_express['nt'] =='Binary Operation':
                LType = verify_semantic(ctx, l_express)

            if(r_express['nt']) == 'Int' or (r_express['nt']) == 'Float' :
                RType = r_express['nt']

            elif r_express['nt'] == 'String' or (r_express['nt']) == 'Boolean':
                RType = r_express['nt']
                raise TypeError(f"The right argument does not support {RType}")

            elif r_express['nt'] == 'Variable':
                name = r_express['Value']
                RType = ctx.get_type(name)
                
            elif r_express['nt'] == 'Group':                
                RType = verify_semantic(ctx, r_express)

            elif r_express['nt'] == 'Function Invocation' or r_express['nt'] == 'Not' or r_express['nt'] == 'Uminus' or r_express['nt'] =='Binary Operation':
                RType = verify_semantic(ctx, r_express)

            
            if (LType == RType):
                return LType
            elif LType != RType:
                raise TypeError(f"The operator is not Int / Float")

        elif Operador == "%":
            LType = 'a'
            RType = 'b'
            if(l_express['nt']) == 'Int' :
                LType = l_express['nt']               

            elif(l_express['nt']) == 'Float' or (l_express['nt']) == 'String' or (l_express['nt']) == 'Boolean':
                LType = l_express['nt']
                raise TypeError(f"The left argument isn't Int")

            elif l_express['nt'] == 'Group':                
                LType = verify_semantic(ctx, l_express)   

            elif l_express['nt'] == 'Variable':
                name = l_express['Value']
                LType = ctx.get_type(name)
            
            elif l_express['nt'] == 'Function Invocation' or l_express['nt'] == 'Not' or l_express['nt'] == 'Uminus' or l_express['nt'] =='Binary Operation':
                LType = verify_semantic(ctx, l_express)

            if(r_express['nt']) == 'Int' :
                RType = r_express['nt']   
                          
            elif r_express['nt'] == 'Group':                
                RType = verify_semantic(ctx, r_express)

            elif(r_express['nt']) == 'Float' or (r_express['nt']) == 'String' or (r_express['nt']) == 'Boolean':
                RType = r_express['nt']
                raise TypeError(f"The right argument isn't Int")

            elif r_express['nt'] == 'Variable':
                name = r_express['Value']
                RType = ctx.get_type(name)
            
            elif r_express['nt'] == 'Function Invocation' or r_express['nt'] == 'Not' or r_express['nt'] == 'Uminus' or r_express['nt'] =='Binary Operation':
                RType = verify_semantic(ctx, r_express)

            if (LType == RType):
                return LType
            elif LType != RType:
                raise TypeError(f"The operator is not Boolean")  


        elif Operador == "&&" or Operador == "||":
            LType = 'a'
            RType = 'b'
            if(l_express['nt']) == 'Boolean' :
                LType = l_express['nt']                

            elif(l_express['nt']) == 'Float' or (l_express['nt']) == 'String' or (l_express['nt']) == 'Int':
                LType = l_express['nt']
                raise TypeError(f"The left argument isnt Boolean")

            elif l_express['nt'] == 'Variable':
                name = l_express['Value']
                LType = ctx.get_type(name)

            elif l_express['nt'] == 'Group':                
                LType = verify_semantic(ctx, l_express)   

            elif l_express['nt'] == 'Function Invocation' or l_express['nt'] == 'Not' or l_express['nt'] == 'Uminus' or l_express['nt'] =='Binary Operation':
                LType = verify_semantic(ctx, l_express)

            if(r_express['nt']) == 'Boolean' :
                RType = r_express['nt']                

            elif(r_express['nt']) == 'Float' or (r_express['nt']) == 'String' or (r_express['nt']) == 'Int':
                RType = r_express['nt']
                raise TypeError(f"The right argument isn't Boolean")

            elif r_express['nt'] == 'Variable':
                name = r_express['Value']
                RType = ctx.get_type(name)

            elif r_express['nt'] == 'Group':                
                RType = verify_semantic(ctx, r_express)

            elif r_express['nt'] == 'Function Invocation' or r_express['nt'] == 'Not' or r_express['nt'] == 'Uminus' or r_express['nt'] =='Binary Operation':
                RType = verify_semantic(ctx, r_express)

            if (LType == RType):
                return LType
            elif LType != RType:
                raise TypeError(f"The operator is not Boolean")  
        
        elif Operador == "!=" or Operador == "==":
            LType = 'a'
            RType = 'b'
            if(l_express['nt']) == 'Boolean' or (l_express['nt']) == 'Float' or (l_express['nt']) == 'Int':
                LType = l_express['nt']                

            elif(l_express['nt']) == 'String':
                LType = l_express['nt']
                raise TypeError(f"The Rigt argument can't be a String")

            elif l_express['nt'] == 'Variable':
                name = l_express['Value']
                LType = ctx.get_type(name)
            
            elif l_express['nt'] == 'Function Invocation' or l_express['nt'] == 'Not' or l_express['nt'] == 'Uminus' or l_express['nt'] =='Binary Operation':
                LType = verify_semantic(ctx, l_express)

            if(r_express['nt']) == 'Boolean' or (r_express['nt']) == 'Float' or (r_express['nt']) == 'Int':
                RType = r_express['nt']                

            elif(r_express['nt']) == 'String':
                RType = r_express['nt']
                raise TypeError(f"The Right argument can't be a String")


            elif r_express['nt'] == 'Variable':
                name = r_express['Value']
                RType = ctx.get_type(name)
            
            elif r_express['nt'] == 'Function Invocation' or r_express['nt'] == 'Not' or r_express['nt'] == 'Uminus' or r_express['nt'] =='Binary Operation':
                RType = verify_semantic(ctx, r_express)


            if (LType) == (RType):
                return 'Boolean'
            elif LType != RType:
                raise TypeError(f"Both arguments need to be Int or Float ")  

    elif node['nt'] == 'String' or node['nt'] =='Int' or node['nt'] =='Float' or node['nt'] == 'Boolean' or node['nt'] == 'Void':
        return node['nt']

    elif node['nt'] == 'Not':
        r =  ctx.get_type(node["Value"])
        if not (r == "Boolean"):
            raise TypeError(f"Operator '!' expects Boolean Type but received {r}")
        return "Boolean"
    
    elif node['nt'] == 'Uminus':
        r =  ctx.get_type(node["Value"])
        if r == 'Int' or 'Float':
            return r
        else:
            raise TypeError(f"Uminus expression expected Int / Float but received but received {r}") 

    elif node['nt'] == 'Statement Expression':
        St  = node['Expression']
        verify_semantic(ctx,St)

    elif node['nt'] == 'Print':
        string = node["print_string"]
        arguments = node["print_argument"]
        
        arg_flt = "%f"
        arg_int = "%d"
        arg_string = "%s"
        
        n_float = string.count(arg_flt)
        n_int = string.count(arg_int)
        n_str = string.count(arg_string)
        
        
        r1 = re.compile('|'.join([arg_flt,arg_int,arg_string]))
        str_types = r1.findall(string)
        args_types = []
        n_args_needed = n_float + n_int + n_str
        n_args = 0
  
        for arg in arguments:
            n_args += 1
            if arg["nt"] == "Void":
                n_args = 0
            types = verify_semantic(ctx,arg)
            args_types.append(ctx.print_types(types))
            
        if n_args != n_args_needed:
            raise TypeError(f"Print needed {n_args_needed} arguments but received {n_args}")
        if n_args != 0:
            for str_type, arg_type in zip(str_types, args_types):
                if str_type != arg_type:
                    var1 = ctx.print_types(str_type)
                    var2 = ctx.print_types(str_type)
                    raise TypeError(f"Print identifier '{str_type} needs {var1} but received {var2}")
                
    elif node['nt'] == "Function Invocation":
        fname = node['Function Name']
        contadorFD = 0
        contadorFI = 0
        
        for k in node['Function Arguments']:
            contadorFD += 1
            if k['nt'] == 'Void':
                contadorFD = 0

        (expected_return, parameter_types) = ctx.get_type(node["Function Name"])

        for k in parameter_types:
            contadorFI += 1
            if k == 'Void':
                contadorFI = 0
            
        for (i, (arg, par_t)) in enumerate(zip(node["Function Arguments"], parameter_types)):            
            arg_t = verify_semantic(ctx, arg)
            if(contadorFI != contadorFD):
                raise TypeError(f"Function {fname} expected {contadorFI} arguments but received {contadorFD}")

            if arg_t != par_t:
                index = i+1
                raise TypeError(f"Argument #{index} expected {par_t} but received {arg_t}") 
          
        return expected_return
    
class Emitter(object):
    def __init__(self):
        self.count = 0
        self.lines = []
        self.stack = [{}]
        self.labels = []
        self.unary = False
        self.unary_count = 0   
    
    def get_type(self, name):
        for scope in self.stack:
            if name in scope:
                return scope[name]
        if "Array_" in name:
            varivavel = name.replace("Array_", "")
    
    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value
    
    def store_label(self, label):
        self.labels.append(label)
        
    def get_label(self):
        var = self.labels
        return var

    def get_count(self):
        self.count += 1
        return self.count

    def get_id(self): 
        id = self.get_count()
        return f"cas_{id}"

    def __lshift__(self, v):    
        self.lines.append(v)

    def get_code(self):
        return "\n".join(self.lines)

    def get_pointer_name(self, n):
        return f"%pont_{n}"
    
    def nome_type(self, nome):
        
        return
    
    def get_etypes(self, typee):


        if typee == "Int":
            typee = "i32"
        elif typee == "Float":
            typee = "float"
        elif typee == "Boolean":
            typee = "zeroext i1"
        elif typee == "String":
            typee = "i8*"
        elif typee == "Void":
            typee = "void"

        return 
        
    def get_align(self, typee):
        
        if typee == "Float":
            align = "4"
        elif typee == "String":
            align = "8"
        elif typee == "Int":
            align =  "4"
        elif typee == "Boolean":
            align ="1"
        elif typee == "Void":
            align = " "
        
        return align
    
    def get_print_types(self, type):
        if type == "Float":
            return "%f"
        elif type == "String":
            return "%s"
        elif type == "Int":
            return "%d"
        else:
            return None

RETURN_CODE = "$ret"  
 
def compilador( node, emitter=None):
    if node['nt'] == 'Program':
        emitter = Emitter()

        emitter << "declare i32 @printf(i8*, ...) #1"

        for Def_declr in node["Def_Decl"]:
            compilador(Def_declr, emitter)

        return emitter.get_code()
 
    elif node['nt'] == "Declaration":
        fType = node['Type']
        fName = node['F_name']
        typee = emitter.get_etypes(fType)
        name = fName + '_function'
        emitter.set_type(name, typee)
        return
    elif node['nt'] == "Definition":
        fType = node['Type']
        fName = node['F_name']
        
        
        typee = emitter.get_etypes(fType)
        name = fName + '_function'
        argument_e = ""
        
        emitter.set_type(name, typee)

        for argument in node["Argument"]:
            temp = emitter.get_etypes(argument["Type"])
            if "i1" in temp:
                temp = "i1 zeroext"
            argument_e += temp
            pname = emitter.get_pointer_name(argument["Type"])
            argument_e += f"{pname}"
            
            if argument["variable_name"] == "Void":
                argument_e = ""
            else:
                arg_name = argument["variable_name"] + "_VArg"
                typee = argument["Type"]                
                emitter.set_type(arg_name, typee)
                
        argument_e = argument_e[:-2] 
        emitter << f"define {typee} @{fName}({argument_e}) #0 {'{'}"   
        
        for argument in node["Arguments"]:
            if argument["variable_name"] != "Void":

                type_arg = emitter.get_emitter_type(argument["type"])
                pname = emitter.get_pointer_name(argument["name"])

                reg = "%" + emitter.get_id()
                align = emitter.get_emitter_align(argument["type"])
                emitter.set_id_name(pname, reg)

            if "i1" in type_arg:

                type_arg = "i8"
                temp_reg = "%" + emitter.get_id()
                emitter << f"  {reg} = alloca {type_arg}, {align}"
                emitter << f"  {temp_reg} = zext i1 {pname} to i8"
                emitter << f"  store {type_arg} {temp_reg}, {type_arg}* {reg}, align {align}"

            else:

                emitter << f"  {reg} = alloca {type_arg}, {align}"
                emitter << f"  store {type_arg} {pname}, {type_arg}* {reg}, align {align}"

        for b in node["Block"]:
            if b !=None:
                compilador(b, emitter)
                
        emitter << "}"
        
    elif node['nt'] == "Variable Name":
        vname = node["variable_name"]
        emitter.set_type(name, node['Type'])
        return
    
    elif node['nt'] == "If" or node['nt'] == "While" or node['nt'] == "if_else":
        cond = node["Condition"]
        block = node["Block"]
        if_else = False
        while_ = False
        if node["nt"] == "if_else":
            else_block = node["Else_block"]  
            if_else = True
        
        if node['nt'] == "if_else":
            compilador(node["If", emitter])    
            
        if node['nt'] == "IF" or node['nt'] == "if_else":
            lb_s_e = "if_" 
        else:
            lb_s_e = "while_"
            while_ = True
        emitter.update_labels()
        
        lf_while_id = emitter.get_id()
        
        label_start = lb_s_e + "start_" + lf_while_id
        label_while = "while_block_" + lf_while_id
        label_else = "if_else" + lf_while_id
        label_end = lb_s_e + "end_" + lf_while_id
        
                   
        emitter.store_label(label_start)
        emitter.store_label(label_end)
        emitter.store_label(label_while)
        emitter.store_label(label_else)
        emitter.store_label(-1)
            
        
        condicao = compilador(cond, emitter)
        
        if "AND" in condicao:
            if "1" or "not" in condicao:
                emitter << f" br label %{label_end}"
            else:
                if while_ == True:
                    emitter << f" br label %{label_while}"
                else:
                    emitter << f" br label %{label_start}"
            
            if while_ == True:
                emitter << f"{label_while}"
            else:
                emitter << f"{label_start}"
            
            for statement in block:
                if statement != None:
                    compilador(statement, emitter)
            emitter << f" br label %{label_end}"
            
            if if_else == True:
                emitter << f"{label_else}:"
                for statement in else_block:
                    if statement != None:
                        compilador(statement, emitter)
                emitter << f" br label %{label_end}"
       
            emitter << f"{label_end}"

        elif "OR" in condicao:
            if "1" or "not" in condicao: 
                if while_ == True:
                    emitter << f" br label %{label_while}"
                else:
                    emitter << f" br label %{label_start}"
            else:
                emitter << f" br label %{label_end}"
                
            if while_ == True:
                emitter << f" br label %{label_while}"
            else:
                emitter << f"{label_start}"
            
            for statement in block:
                if statement != None:
                    compilador(statement, emitter)
            emitter << f" br label %{label_end}"
            
            if if_else == True:
                emitter << f"{label_else}:"
                for statement in else_block:
                    if statement != None:
                        compilador(statement, emitter)
                emitter << f" br label %{label_end}"
                
            emitter << f"{label_end}"           
        else:
            if "not" in condicao:
                condicao = condicao.split("-")
                if while_ == True:
                    emitter << f" br{condicao[1]}, label %{label_end}, label %{label_while}"
                else:
                    emitter << f" br{condicao[1]}, label %{label_end}, label %{label_start}"
            else:
                if while_ == True:
                    emitter << f" br{condicao[1]}, label %{label_while}, label %{label_end}"
                else:
                    emitter << f" br{condicao}, label %{label_start}, label %{label_end}"
                    
            if while_ == True:
                emitter << f"{label_while}"
            else:    
                emitter << f"{label_start}"
            
            for statement in block:
                if statement != None:
                    compilador(statement, emitter)
            emitter << f" br label %{label_end}"
            
            if if_else == True:
                emitter << f"{label_else}:"
                for statement in else_block:
                    if statement != None:
                        compilador(statement, emitter)
                emitter << f" br label %{label_end}"

            emitter << f"{label_end}"                 
        return
    
   

    elif node['nt'] == "Return":
        ret_cond = node["Expression"]
        reg = compilador(ret_cond, emitter)
        
        if "i8" in reg and "*" not in reg:
            t_reg = "%" + emitter.get_id()
            i = emitter.get_count() 
            emitter << f" {t_reg} = trunc i8 %cas_{i} to i1"
            reg = f"i1 {t_reg}"
        
        emitter << f" ret {reg}"
   

    elif node['nt'] == "Variable Declaration":
        nome = node['Variable Name']
        typee = node['type']        
        expr = node['Expression']
        pnome = emitter.get_pointer_name(nome)
        tipo = emitter.get_etypes(typee)
        align = emitter.get_align(typee)
        name = nome + "_var"
        
        if "i1" in tipo:
            tipo = "i8"
   
        emitter << f" {pnome} = alooca {tipo}, {align}"
      
        registo = compilador(expr, emitter)
        
        if "i1" in registo:
            if "true" in registo:
                registo = "i8 1"
            elif "false" in registo:
                registo = "i8 0"
    
        emitter << f" store {registo}, {tipo}* {pnome}, {align}"
        return
        
  
    elif node['nt'] == 'Array':
        pass
    elif node['nt'] == "Array Declaration":
        pass
    elif node['nt'] == 'Array Assignment':
        pass

    elif node['nt'] == "Variable Assignment":        
        expr = node['Expression']
        vnome = node['Variable']
        name = vnome + "_var"
        
        registo = compilador(expr, emitter)
        pnome = emitter.get_pointer_name(vnome)
        tipo = emitter.get_type(vnome) 
        
        tipo_e = emitter.get_etypes(tipo) 
        align = emitter.get_align(tipo)
        
        emitter << f"  store {registo}, {tipo_e}* {pnome}, align {align}"
        return
        
    elif node['nt'] == 'Variable':
        vname = node["Value"]        
        name = vname + "_var"
        reg = "%" + emitter.get_id()
        pname = emitter.get_pointer_name(vname)
        tipo = emitter.nome_type(name)
        tipo_e = emitter.get_etypes(tipo) 
        align = emitter.get_align(tipo)
        
        if "i1" in tipo_e:
            tipo_e = "i8"
            
        emitter << f"   {reg} = load {tipo_e}, {tipo_e}* {pname}, align {align}"
        return reg

    elif node['nt'] == 'Group':
        valor = node["valor"]      
        g_exp = compilador(valor, emitter)
        
        return
     
    elif node['nt'] == "Binary Operation":
        Operador = node['Operator']      
          
        if Operador == "<":
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")                       
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f" {rr} = fcmp olt {ler}, {rer[1]}"
            else:
                emitter <<f" {rr} = icmp stl {ler}, {rer[1]}"           
            return f"i1 {rr}"
        
        elif Operador == ">":
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")                       
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f" {rr} = fcmp ogt {ler}, {rer[1]}"
            else:
                emitter <<f" {rr} = icmp sgt {ler}, {rer[1]}"           
            return f"i1 {rr}"
        
        elif Operador == ">=":
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")                       
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f" {rr} = fcmp oge {ler}, {rer[1]}"
            else:
                emitter <<f" {rr} = icmp sge {ler}, {rer[1]}"           
            return f"i1 {rr}"
        
        elif Operador == "<=":
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")                       
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f" {rr} = fcmp ole {ler}, {rer[1]}"
            else:
                emitter <<f" {rr} = icmp sle {ler}, {rer[1]}"           
            return f"i1 {rr}"
        
        elif Operador == "+":            
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rr = "%" + emitter.get_id()
            rer = temp.slit(" ")
            if rer[0] == "float":
                emitter << f"   {rr} = fadd {ler}, {rer[1]}"	
            else:
                emitter <<f"    {rr} = add nsw {typee} {ler}, {rer}"           
            return f"{ler[0]} {rr}"
        
        elif Operador == "-":           
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            rer = compilador(r_express, emitter)
            rr = "%" + emitter.get_id()
            rer = temp.slit(" ")
            if rer[0] == "float":
                emitter << f"   {rr} = fsub {ler}, {rer[1]}"	
            else:            
                emitter <<f"    {rr} = sub nsw {typee} {ler}, {rer}"           
            return f"{ler[0]} {rr}"
            
        elif Operador == "*":           
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rr = "%" + emitter.get_id()
            rer = temp.slit(" ")
            if rer[0] == "float":
                emitter << f"   {rr} = fmul {ler}, {rer[1]}"	
            else:            
                emitter <<f"    {rr} = mul nsw {typee} {ler}, {rer[1]}"           
            return f"{rer[0]} {rr}"

        elif Operador == "/":           
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rr = "%" + emitter.get_id()
            rer = temp.slit(" ")
            if rer[0] == "float":
                emitter << f"   {rr} = fdiv {ler}, {rer[1]}"	
            else: 
                emitter <<f" {rr} = sdiv nsw {typee} {ler}, {rer[1]}"           
            return f"{rer[0]} {rr}"
        
        elif Operador == "%":
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")
            rr = "%" + emitter.get_id()
            emitter <<f" {rr} = srem {ler}, {rer[1]}"           
            return f"{ler[0]} {rr}"
        
        elif Operador == "&&":
            pass
        
        elif Operador == "||":
            '''l_express = node['Left Parameter']
            r_express = node['Right  Parameter']  
            
            labels = emitter.get_labels()
            label_or = "start_or_" + labels[0][9:]
            var = emitter.get_count()
            var2 = emitter.get_count()'''
            pass
            
             
        elif Operador == "!=":
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")
            
            if "i8" in ler:
                reg1 = "%" + emitter.get_id()
                reg2 = "%" + emitter.get_id()
                
                emitter << f"  {reg1} = trunc {ler} to i1"
                emitter << f"  {reg2} = zext i1 {reg1} to i32"
                
                registo_l = f"i32 {reg2}"
            
            
            elif "i1" in ler:
                if"true" in ler:
                    value = 1
                else:
                    value = 0
                ler = f"i32 {value}"
            
            if rer[0] == "i1":
                reg1 = "%" + emitter.get_id()
                reg2 = "%" + emitter.get_id()
                
                emitter << f"  {reg1} = trunc {rer[0]} {rer[1]} to i1"
                
                emitter << f"  {reg2} = zext i1 {reg1} to i32"
                
                registo_r[1] = f"{reg2}"
                
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter << f"  {rr} = fcmp une {ler}, {rer[1]}"
            else:
                emitter << f"  {rr} = icmp ne {ler}, {rer[1]}"  
                
            return f"i1 {rr}"
        
        elif Operador == "==":
            l_express = node['Left Parameter']
            r_express = node['Right  Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer= temp.slip(" ")
            
            
            if "i8" in ler:
                reg1 = "%" + emitter.get_id()
                reg2 = "%" + emitter.get_id()
                
                emitter << f"  {reg1} = trunc {ler} to i1"
                emitter << f"  {reg2} = zext i1 {reg1} to i32"
                
                ler = f"i32 {reg2}"

            elif "i1" in ler:
                if "true" in ler:
                    value = 1
                else:
                    value = 0
                ler = f"i32 {value}"

            if rer[0] == "i1":
                if rer[1] == "true":
                    rer[1] = 1
                else:
                    rer[1] = 0
     
            elif rer[0] == "i8":
                reg1 = "%" + emitter.get_id()
                reg2 = "%" + emitter.get_id()
                emitter << f"  {reg1} = trunc {rer[0]} {rer[1]} to i1"
                emitter << f"  {reg2} = zext i1 {reg1} to i32"
                registo_r[1] = f"{reg2}"

            rr = "%" + emitter.get_id()
   
            if rer[0] == "float":
                emitter << f"  {rr} = fcmp oeq {ler}, {rer[1]}"

            else:
                emitter << f"  {rr} = icmp eq {ler}, {rer[1]}"
            
            return f"i1 {rr}"

    elif node['nt'] == 'String':
        typee = emitter.get_etypes(node["nt"])
        value = node["value"]
        size = len(value)
        id = emitter.get_id()
        string_n = f"@.casual_str_{id}"
        
        return f"i8* getelementptr inbounds ([{size} x i8], [{size} x i8]* {string_n}, i64 0, i64 0)"
    
    elif node['nt'] =='Int':
        typee = emitter.get_etypes(node["nt"])
        value = str(node["value"])
        return f"{typee} {value}"

    elif node['nt'] =='Float':
        typee = emitter.get_etypes(node["nt"])
        value = node["value"]
        float_single = struct.unpack('f', struct.pack('f', value))[0]
        valor = hex(struct.unpack('<Q', struct.pack('<d', float_single))[0])
        return f"{tipo} {valor}"
        
    elif node['nt'] == 'Boolean':
        typee = "i1"
        value = node["value"]
        return f"{typee} {value}"

    elif node['nt'] == 'Void':
        return "void"

    elif node['nt'] == 'Not':
        emitter.unary_count += 1
        expr = node["value"]

        if expr["nt"] != "Not_Unary":
            if emitter.unary_count % 2 == 0:
                emitter.unary_count = 0
                reg = compilador(expr["value"], emitter)
                return reg
            else:
                if expr["nt"] == "Group_expr":		
                    var = expr["value"]
                    if var["operator"] == "&&" or var["operator"] == "||":
                        emitter.unary = True

                emitter.unary_count = 0
                reg = compilador(expr, emitter)
                return f"not-{reg}"
        else:
            reg = compilador(expr, emitter)
            return reg


    elif node['nt'] == 'Uminus':
        express = compilador(node['expression'], emitter)
        express = express.split(" ") 
        
        return f"{express[0]} -{express[1]}"
    
    elif node['nt'] == 'Statement Expression':
        St  = node['Expression']
        se = compilador(St, emitter)
        
        return 

    elif node['nt'] == "Function Invocation":
        fname = node['Function Name'] 
        name = fname + "_function"
        reg_arg = ""
        
        typee = emitter.get_etypes(emitter.get_type(name))
        t_name = emitter.get_pointer_name(fname)
        
        pname = t_name + "_" + str(emitter.get_count())
        
        for argument in node["Argument"]:
            if argument['nt'] == "Void":
                reg_arg = ""
            else:
                t = compilador(argument, emitter) + ", "
                if "i1" in t:
                    t = t.replace("i1", "i1 zeroext")
                elif "i8" in t and "*" not in t:
                    variable = t.slip(" ")
                    variable[1] = variable[1].replace(",", "")
                    treg = "%" + emitter.get_id()
                    
                    emitter << f" {treg} = trunc i8 {variable[1]} to i1"
                reg_arg += t
                
        reg_arg = reg_arg[:-2]
        if typee == "void":
            emitter << f" call {typee} @{fname} ({reg_arg})"
        else:
            emitter << f" {pname} = call {typee} @{fname}({reg_arg})"
        
        if "i1" in typee:
            treg = "%" + emitter.get_id()
            emitter << f"  {treg} = zext i1 {pname} to i8"
            tipo = "i8"
            pname = treg
   
        return f"{typee} {pname}"

    elif node['nt'] == "Print":
        pass
    
    print("WARNING", node['nt'])

import ply.yacc as yacc
parser = yacc.yacc()

try:
    if len(sys.argv) < 2:
        print("There isn't a file to read")

    else:
        file = open(sys.argv[1])
        code = file.read()
        f_code = parser.parse(code)
        if f_code != None:

            verify_semantic(Context(), f_code)
            name = sys.argv[1].split(".cas")

            llvm_code = compilador(f_code)
            print(llvm_code)


except EOFError:
    print("File could not be opened")

