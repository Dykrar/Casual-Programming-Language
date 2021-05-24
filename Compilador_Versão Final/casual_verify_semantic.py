# ---------------------------------------------------------------------------- #
#                          Diogo Rodrigues 55740 FCUL                          #
# ---------------------------------------------------------------------------- #

import re

class TypeError(Exception):
    pass

# ---------------------------------------------------------------------------- #
#                                    CONTEXT                                   #
# ---------------------------------------------------------------------------- #

class Context(object):
    def __init__(self):
        self.stack = [{}]
        self.lambdas = []
    
    def get_type(self, name):
        for scope in self.stack:
            if name in scope:
                i = scope[name]
                if i[0] == "Declarataion" and "Function_" in name:
                    variavel = name.replace('Function_','')
                    raise TypeError(f"Function {variavel} not in context")
                else:
                    return scope[name]

        if "Array_" in name:
            variavel = name.replace("Array_", "")
            raise TypeError(f"Array {variavel} not in context")

        elif "Function_" in name:
            variavel = name.replace('Function_','')
            raise TypeError(f"Function {variavel} not in context")

        else:   
            raise TypeError(f"Variable {name} not in context")
    
    def set_type(self, name, value):
        scope = self.stack[0]

        i =  scope.keys()
        for j in i:
            if j == name:
                if scope[name][0] == "Definition":
                    if value[0] == "Declaration":
                        return

        scope[name] = value

    def has_var(self, name):
        for scope in self.stack:
            if name in scope:
                return True
        return False
    
    def has_function(self, name, assinatura):
        for scope in self.stack:
            if name in scope:
                tipo1 = scope[name][2]
                tipo1.sort()
                nome1 = scope[name][3]
                nome1.sort()
                tipo2 = assinatura[2]
                tipo2.sort()
                nome2 = assinatura[3]
                nome2.sort()
                dec_def1 = scope[name][0]
                dec_def2 = assinatura[0]
                dec_def_type1 = scope[name][1]
                dec_def_type2 = assinatura[1]

                if dec_def1 == dec_def2:
                    return True,1
                
                elif (dec_def1 != dec_def2) and ((dec_def_type1 != dec_def_type2) or (len(tipo1)!= len(tipo2))):
                    return True, 2
                
                elif (tipo1 != tipo2 ) or (nome1 != nome2):
                    return True, 3
                    
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
        elif types == "Float":
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


# ---------------------------------------------------------------------------- #
#                                VERIFY SEMANTIC                               #
# ---------------------------------------------------------------------------- #

def verify_semantic(ctx:Context, node):
    if node['nt'] == 'Program':        

        for Def_declr in node["Def_Decl"]:
            name = Def_declr["F_Name"]
            name = "Function_" + name

            assinatura = (Def_declr['nt'], Def_declr["Type"], [argument['type'] for argument in Def_declr["Argument"]], [argument['variable_name'] for argument in Def_declr["Argument"]])

            for a in assinatura[2]:
                if a == "Void":
                    assinatura[2].remove(a)

            if ctx.has_function(name, assinatura):
                fname = name.replace("Function_", "")
                if ctx.has_function(name, assinatura)[1] == 2 or ctx.has_function(name, assinatura)[1] == 3:
                    raise TypeError(f"Function '{fname}' definition doen't match with '{fname}' declaration")
                else:
                    if assinatura[0] == "Definition":
                        raise TypeError(f"Function {name} is already defined in the context.")
                    else:
                        raise TypeError(f"Function {name} is already declared in the context.")

            ctx.set_type(name, assinatura)

        for Def_declr in node["Def_Decl"]:
            verify_semantic(ctx, Def_declr)

# -------------------------------- DEFINITION -------------------------------- #

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

# ------------------------------- IF ELSE WHILE ------------------------------ #

    elif node['nt'] == "If" or node['nt'] == "While" :
        cond = node["Condition"]
        if verify_semantic(ctx, cond) != "Boolean":
            raise TypeError(f" Condition not boolean")

        ctx.enter_scope()
        for st in node["Block"]:
            verify_semantic(ctx, st)
        ctx.exit_scope()

    elif node["nt"] == "If_Else":
        stat = node["nt"]
        condicao = node["Condition"]
        
        if verify_semantic(ctx, condicao) != "Boolean":
            raise TypeError(f"{stat} condition expected Boolean type but got {verify_semantic(ctx, condicao)}")
        
        ctx.enter_scope()
        if node["Block"] != None:
            for statment in node["Block"]:
                verify_semantic(ctx, statment)
        ctx.exit_scope()
        
        ctx.enter_scope()
        if node["Else_block"] != None:
            for statment in node["Else_block"]:
                verify_semantic(ctx,statment)
            ctx.exit_scope()
    
# ---------------------------------- ARRAYS ---------------------------------- #

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
        size = node['size']

        if ctx.has_var_in_current_scope(name) or ctx.has_var_in_current_scope(name):
            raise TypeError(f"Array {name} already defined in the context")

        tipo_size = verify_semantic(ctx, size)
        if tipo_size != "Int":
            raise TypeError(f"Array {name} size must be Int")
        
        ctx.set_type(nome, index_type)

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
    
    elif node['nt'] == "Get_Array":
        name = node['name']
        return name

    elif node["nt"] == 'Create_Array':
        size = node["size"]
        return verify_semantic(ctx, size)

# --------------------------------- VARIABLE --------------------------------- #

    elif node['nt'] == "Variable Assignment":        
        nome = node['Variable']        
        typee = ctx.get_type(nome)
        expr = node['Expression']
        

        if expr['nt'] == "lambda":
            assinatura = (expr['nt'], typee, [arg["type"] for arg in expr['Arguments']], [arg['variable_name'] for arg in expr["Arguments"]])
            name = "Function_" + name
            ctx.set_type(name, assinatura)
            typeeE = verify_semantic(ctx, expr)
        else:
            typeeE = verify_semantic(ctx, expr)
            if not ctx.has_var(nome):
                raise TypeError(f"Variable not defined")
            if typee != typeeE:
                raise TypeError(f"Variable {nome} is of type {typee} but received type{typeeE}")
            return typee
   
    elif node['nt'] == 'Variable':
        name = node["Value"]  
        if not ctx.has_var(name):
            for a in ctx.lambdas:
                if a != "Void":
                    if name == a["variable_name"]:
                        return a ["type"] 
                           
            if "Array_" in name:
                name.replace("Array_","")
                raise TypeError(f"Array {name} isn't defined in the contexto")
            else:
                raise TypeError(f"Variable {name} isn't defined in the contexto")
        return ctx.get_type(name)

    elif node['nt'] == "Variable Name":
        name = node["variable_name"]   
        if ctx.has_var_in_current_scope(name):
            if "Array_" in name:
                name.replace("Array_","")
                raise TypeError(f"Variable {name} is already defined in the context.") 
            else:
                raise TypeError(f"Variable {name} is already defined in the context.")    
        ctx.set_type(name, node['Type'])  

    elif node['nt'] == "Variable Declaration":
        nome = node['Variable Name']
        name = "Array_"+ nome 
        typee = node['type']        
        expr = node['Expression']
        if expr['nt'] == "lambda":
            assinatura = (expr['nt'], typee, [arg["type"] for arg in expr['Arguments']], [arg['variable_name'] for arg in expr["Arguments"]])
            name = "Function_" + nome 
            ctx.set_type(name, assinatura) 
            typeeE = verify_semantic(ctx, expr)
        else:
            typeeE = verify_semantic(ctx, expr)
            if ctx.has_var_in_current_scope(nome) or ctx.has_var_in_current_scope(name) :
                raise TypeError(f"Variable {nome} is already defined in the context.")  

            if typee != typeeE:
                raise TypeError(f"Variable {nome} is of type {typee} but received type {typeeE}")
            ctx.set_type(nome, node['type'])
    
# ---------------------------------- LAMBDA ---------------------------------- #

    elif node['nt'] == "lambda":

        for argument in node["Arguments"]:
            ctx.lambdas.append(argument)                

        expression = node['Expression']
        expr = verify_semantic(ctx, expression)

        return expr

# ----------------------------- BINARY OPERATION ----------------------------- #

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
                LType = verify_semantic(ctx, l_express)

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
                RType = verify_semantic(ctx, r_express)

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
                LType = verify_semantic(ctx, l_express)

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
                RType = verify_semantic(ctx, r_express)
                
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
                LType = verify_semantic(ctx, l_express) 
            
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
                RType = verify_semantic(ctx, r_express)
            
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
                LType = verify_semantic(ctx, l_express) 

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
                RType = verify_semantic(ctx, r_express)

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
                LType = verify_semantic(ctx, l_express)
            
            elif l_express['nt'] == 'Function Invocation' or l_express['nt'] == 'Not' or l_express['nt'] == 'Uminus' or l_express['nt'] =='Binary Operation':
                LType = verify_semantic(ctx, l_express)

            if(r_express['nt']) == 'Boolean' or (r_express['nt']) == 'Float' or (r_express['nt']) == 'Int':
                RType = r_express['nt']                

            elif(r_express['nt']) == 'String':
                RType = r_express['nt']
                raise TypeError(f"The Right argument can't be a String")


            elif r_express['nt'] == 'Variable':
                RType = verify_semantic(ctx, r_express)
            
            elif r_express['nt'] == 'Function Invocation' or r_express['nt'] == 'Not' or r_express['nt'] == 'Uminus' or r_express['nt'] =='Binary Operation':
                RType = verify_semantic(ctx, r_express)


            if (LType) == (RType):
                return 'Boolean'
            elif LType != RType:
                raise TypeError(f"Both arguments need to be Int or Float ")  

# --------------------- GROUP NOT UMINUS STAT_EXPRESSION --------------------- #

    elif node['nt'] == 'Group':
        return verify_semantic(ctx, node["Valor"])

    elif node['nt'] == 'Not':
        r =  ctx.get_type(node["Value"])
        if not (r == "Boolean"):
            raise TypeError(f"Operator '!' expects Boolean Type but received {r}")
        return "Boolean"
    
    elif node['nt'] == 'Uminus':
        r =  verify_semantic(ctx, node["Valor"])
        if r == 'Int' or 'Float':
            return r
        else:
            raise TypeError(f"Uminus expression expected Int / Float but received {r}") 

    elif node['nt'] == 'Statement Expression':
        St  = node['Expression']
        verify_semantic(ctx,St)

# ----------------------------------- TYPES ---------------------------------- #

    elif node['nt'] == 'String' or node['nt'] =='Int' or node['nt'] =='Float' or node['nt'] == 'Boolean' or node['nt'] == 'Void':
        return node['nt']
# ----------------------------------- PRINT ---------------------------------- #

    elif node['nt'] == 'Print':
        string = node["print_string"]
        arguments = node["print_arguments"]
        
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





# ---------------------------- FUNCTION INVOCATION --------------------------- #

    elif node['nt'] == "Function Invocation":
        fname = node['Function Name']
        name = "Function_" + fname
        contadorFD = 0
        contadorFI = 0
        
        for k in node['Function Arguments']:
            contadorFD += 1
            if k['nt'] == 'Void':
                contadorFD = 0


        (def_decl , tipo, argstype, argsname) = ctx.get_type(name)
        temp = list((def_decl , tipo, argstype, argsname))
        temp.remove((temp[0]))
        temp.remove((temp[2]))
        (expected_return, parameter_types) = tuple(temp)



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

# ---------------------------------- RETURN ---------------------------------- #

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