# ---------------------------------------------------------------------------- #
#                          Diogo Rodrigues 55740 FCUL                          #
# ---------------------------------------------------------------------------- #

import struct

# ---------------------------------------------------------------------------- #
#                                    emitter                                   #
# ---------------------------------------------------------------------------- #

class Emitter(object):
    def __init__(self):
        self.count = 0
        self.lines = []
        self.id_stack = [{}]
        self.stack = [{}]
        self.labels = []
        self.tipoArray = []
        self.not_ = False
        self.not__count = 0
        self.OR = False
        self.AND = False
        self.lambda_fun = []
        self.newF = []
        self.isLambda = False
        self.isLambdaExp = False
        self.lmbd= []
        self.lambda_args = []
        self.ext_var = []
        self.lambda_fun_is = []

# ----------------------------------- TYPES ---------------------------------- #

    def get_type(self, name):
        if name == 'lambda':
            pass
        else:
            for scope in self.stack:
                if name in scope:
                    return scope[name]
                    
    def set_type(self, name, value):
        scope = self.stack[0]
        scope[name] = value

    def get_etypes(self, tipo):
        if tipo == 'Int':
            tipo = 'i32'
        elif tipo == 'Float':
            tipo = 'float'
        elif tipo == 'Boolean':
            tipo = 'zeroext i1'
        elif tipo == 'String':
            tipo = 'i8*'
        elif tipo == 'Void':
            tipo = 'void'
        return tipo

# --------------------------------- ID NAMES --------------------------------- #

    def set_id_name(self, nome, valor):
        scope = self.id_stack[0]
        scope[nome] = valor
    
    def get_id_name(self, nome):
        for scope in self.id_stack:
            if nome in scope:
                return scope[nome]

# ---------------------------------- labels ---------------------------------- #

    def store_label(self, label):
        self.labels.append(label)
        
    def get_label(self):
        var = self.labels
        return var

    def labls_updt(self):
        self.labels = []

# ----------------------------------- align ---------------------------------- #

    def get_align(self, tipo):
        align = ""        
        if tipo == "Float":
            align = "4"
        elif tipo == "String":
            align = "8"
        elif tipo == "Int":
            align =  "4"
        elif tipo == "Boolean":
            align ="1"
        elif tipo == "Void":
            align = ""
        
        return align

# -------------------------------- print types ------------------------------- #

    def get_print_types(self, tipo):
        if tipo == "Float":
            return "%f"
        elif tipo == "String":
            return "%s"
        elif tipo == "Int":
            return "%d"
        else:
            return None

# ------------------------------------ -- ------------------------------------ #

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



RETURN_CODE = "$ret"  
 
# ---------------------------------------------------------------------------- #
#                                  COMPILADOR                                  #
# ---------------------------------------------------------------------------- #

def compilador( node, emitter=None):
# ---------------------------------- program --------------------------------- #

    if node['nt'] == 'Program':
        emitter = Emitter()

        emitter << "declare i32 @printf(i8*, ...) #1"
        emitter << "declare i32 @array_get(i8*) #1"
        emitter << "declare i32 @array_create(i32) #1"

        for Def_declr in node["Def_Decl"]:
            compilador(Def_declr, emitter)

        return emitter.get_code()
 
# --------------------------------- DECL DEF --------------------------------- #

    elif node['nt'] == "Declaration":
        fType = node['Type']
        fName = node['F_Name']
        typee = emitter.get_etypes(fType)
        name = fName + '_function'
        emitter.set_type(name, typee)
        return

    elif node['nt'] == "Definition":
        fType = node['Type']
        fName = node['F_Name']
        
        
        typee = emitter.get_etypes(fType)
        name = fName + '_function'
        argument_e = ""
        
        emitter.set_type(name, typee)

        for argument in node["Argument"]:
            
            temp = emitter.get_etypes(argument["type"])
            if "i1" in temp:
                temp = "i1 zeroext"

            argument_e += temp
            pname = emitter.get_pointer_name(argument["variable_name"])
            argument_e += f" {pname}, "
            
            if argument["variable_name"] == "Void":
                argument_e = ""
            else:
                arg_name = argument["variable_name"] + "_VArg"
                typee_arg = argument["type"]          
                emitter.set_type(arg_name, typee_arg)

        argument_e = argument_e[:-2]
        if emitter.isLambda == True:       
            emitter.lambda_fun.append(f"define {typee} @{fName}({argument_e}) #0 {'{'}")
        else:
            emitter << f"define {typee} @{fName}({argument_e}) #0 {'{'}"   

        for argument in node["Argument"]:
            
            if argument['variable_name']!= "Void":
                if argument['type'] == "i32":
                    argument['type'] == 'Int'
                elif argument['type'] == "float":
                    argument['type'] == 'Float'
                elif argument['type'] == "i8":
                    argument['type'] == 'String'
            
                type_arg = emitter.get_etypes(argument["type"])
                pname = emitter.get_pointer_name(argument["variable_name"])
                reg = "%" + emitter.get_id()
                align = emitter.get_align(argument["type"])
                emitter.set_id_name(pname, reg)
                if emitter.isLambda == True:
                    if "i1" in type_arg:
                        type_arg = "i8"
                        temp_reg = "%" + emitter.get_id()
                        emitter.lambda_fun.append(f"   {reg} = alloca {type_arg}, align {align}")
                        emitter.lambda_fun.append(f"   {temp_reg} = zext i1 {pname} to i8")
                        emitter.lambda_fun.append(f"   store {type_arg} {temp_reg}, {type_arg}* {reg}, align {align}")
                    else:
                        emitter.lambda_fun.append(f"   {reg} = alloca {type_arg}, align {align}")
                        emitter.lambda_fun.append(f"   store {type_arg} {pname}, {type_arg}* {reg}, align {align}")

                else:
                    if "i1" in type_arg:
                        type_arg = "i8"
                        temp_reg = "%" + emitter.get_id()
                        emitter << f"   {reg} = alloca {type_arg}, align {align}"
                        emitter << f"   {temp_reg} = zext i1 {pname} to i8"
                        emitter << f"   store {type_arg} {temp_reg}, {type_arg}* {reg}, align {align}"

                    else:                     
                        emitter << f"   {reg} = alloca {type_arg}, align {align}"
                        emitter << f"   store {type_arg} {pname}, {type_arg}* {reg}, align {align}"

        for b in node["Block"]:
            if b !=None:
                
                compilador(b, emitter)
        
        if emitter.isLambda == True:
            emitter.lambda_fun.append("}")
        elif emitter.isLambdaExp == True:
            pass
        else:        
            emitter << "}"

# ------------------------------- if else while ------------------------------ #
    
    elif node['nt'] == "If" or node['nt'] == "While" or node['nt'] == "If_Else":
        cond = node["Condition"]
        block = node["Block"]
        if_else = False
        while_ = False
        if node["nt"] == "If_Else":
            else_block = node["Else_block"]  
            if_else = True 
            
        if node['nt'] == "If" or node['nt'] == "If_Else":
            lb_s_e = "if_"  
        else:
            lb_s_e = "while_"
            while_ = True
            
        emitter.labls_updt()
        
        lf_while_id = emitter.get_id()
        
        label_start = lb_s_e + "start_" + lf_while_id
        label_while = "while_block_" + lf_while_id
        label_else = "if_else_" + lf_while_id
        label_end = lb_s_e + "end_" + lf_while_id
        
        if node['nt'] == "While":
            emitter<< f"   br label %{label_start}"
            emitter<< f"{label_start}:"                       
            emitter.store_label(label_while)
            emitter.store_label(label_end)


        if(node['nt'] == "If_Else"):
            emitter.store_label(label_start)
            emitter.store_label(label_else)
        else:
            emitter.store_label(label_start)
            emitter.store_label(label_end)
        emitter.store_label(-1)
            
        
        condicao = compilador(cond, emitter)   
        if "AND" in condicao:
            if "1" or "not" in condicao:
                if if_else == True:
                    emitter << f"   br label %{label_else}"
                else:
                    emitter << f"   br label %{label_end}"
            else:
                if while_ == True:
                    emitter << f"   br label %{label_while}"
                else:
                    emitter << f"   br label %{label_start}"
            
            if while_ == True:
                emitter << f"{label_while}:"
            else: 
                emitter << f"{label_start}:"
            
            for statement in block:
                if statement != None:
                    compilador(statement, emitter)           
            

            if while_ == True:
                emitter << f"   br label %{label_start}:"
            else:
                emitter << f"   br label %{label_end}"
            
            if if_else == True:              
                emitter << f"{label_else}:"
                for statement in else_block:
                    if statement != None:
                        compilador(statement, emitter)
                emitter << f"   br label %{label_end}"
       
            emitter << f"{label_end}:"

        elif "OR" in condicao:
            if "1" or "not" in condicao: 
                if while_ == True:
                    emitter << f"   br label %{label_while}"
                else:
                    emitter << f"   br label %{label_start}"
            else:
                if if_else == True:
                    emitter << f"   br label %{label_else}"
                else:
                    emitter << f"   br label %{label_end}"
                
            if while_ == True:              
                emitter << f"{label_while}"
            else:
                emitter << f"{label_start}:"
            
            for statement in block:
                if statement != None:
                    compilador(statement, emitter)

            if while_ == True:  
                emitter << f"   br label %{label_start}"
            else:
                emitter << f"   br label %{label_end}"
            

            if if_else == True:               
                emitter << f"{label_else}:"
                for statement in else_block:
                    if statement != None:
                        compilador(statement, emitter)
                emitter << f"   br label %{label_end}"
                
            emitter << f"{label_end}:"           
        else:
            if "not" in condicao:
                condicao = condicao.split("-")
                if while_ == True:
                    emitter << f"   br {condicao[1]}, label %{label_end}, label %{label_while}"
                else:
                    emitter << f"   br {condicao[1]}, label %{label_end}, label %{label_start}"
            else:
                if while_ == True:                   
                    emitter << f"   br {condicao}, label %{label_while}, label %{label_end}"
                elif if_else == True:
                    emitter << f"   br {condicao}, label %{label_start}, label %{label_else}"
                else:
                    emitter << f"   br {condicao}, label %{label_start}, label %{label_end}"
                    
            if while_ == True:              
                emitter << f"{label_while}:"
            else:                   
                emitter << f"{label_start}:"
            
            for statement in block:
                if statement != None:
                    compilador(statement, emitter)

            if while_ == True:
                emitter <<f"    br label %{label_start}"
            else:
                emitter <<f"    br label %{label_end}"
                     
            
            if if_else == True:                
                emitter << f"{label_else}:"
                for statement in else_block:
                    if statement != None:
                        compilador(statement, emitter)
                emitter << f"   br label %{label_end}"

            emitter << f"{label_end}:"                           
        return 
        
# ----------------------------------- array ---------------------------------- #

    elif node['nt'] == 'Array':
        nome = node["name"]
        tipo_index = node["index_type"]

        name = "Array_" + nome
        registo = "%" + emitter.get_id()
        pname = emitter.get_pointer_name(nome)
        typee = emitter.get_type(name)
        tipo = emitter.get_etypes(typee)
        align = emitter.get_align(typee)

        array_type = ""

        for array in emitter.tipoArray:
            if array["name"]== name:
                array_type = array["type"]
        if "i1" in tipo:
            tipo = "i8"

        variavel = compilador(tipo_index, emitter)
        i = variavel.split(" ")
        reg = "%" + emitter.get_id()
        j = "%" + emitter.get_id()
        if"%" in i[1]:
            emitter <<f"    {reg} = sext {variavel} to i64"
            emitter <<f"    {j} = getelementptr inbounds {array_type}, {array_type}* {pname}, i64 0, i64 {reg}"
        else:
            emitter <<f"    {j} = getelementptr inbounds {array_type}, {array_type}* {pname}, i64 0, i64 {i[1]}" 
        emitter <<f"   {registo} = load {tipo}, {tipo}* {j}, align {align}"  
        return f"{tipo} {registo}"    

    elif node['nt'] == "Array Declaration":
        nome = node['name']
        pnome = emitter.get_pointer_name(nome)
        typee = node['type']
        tipo = emitter.get_etypes(typee)
        align = emitter.get_align(typee)
        size_array = node["size"]

        name = "Array_" + nome 
        emitter.set_type(name, typee)

        if "i1" in tipo:
            tipo = "i8"
        
        size = compilador(size_array, emitter)
        size = size.split(" ")

        emitter << f"   {pnome} = alloca [{size[1]} x {tipo}], align {align}"
        emitter.tipoArray.append({"name": name, "type": f"[{size[1]} x {tipo}]"})

        return

    elif node['nt'] == 'Array Assignment':
        nome = node["name"]
        expr = node["expression"]
        tipo_index = node["index type"]

        name = "Array_" + nome

        pname = emitter.get_pointer_name(nome)
        typee = emitter.get_type(name)
        tipo = emitter.get_etypes(typee)
        align = emitter.get_align(typee)

        array_type = ""

        for array in emitter.tipoArray:
            if array["name"]== name:
                array_type = array["type"]
        
    
        registo = compilador(expr, emitter)
        v = compilador(tipo_index, emitter)
        v2 = v.split(" ")
        reg = "%" + emitter.get_id()
        i = "%" + emitter.get_id()
        if"%" in v2[1]:
            emitter <<f"    {reg} = sext {v} to i64"
            emitter <<f"    {i} = getelementptr inbounds {array_type}, {array_type}* {pname}, i64 0, i64 {reg}"
        else:
            emitter <<f"    {i} = getelementptr inbounds {array_type}, {array_type}* {pname}, i64 0, i64 {i[1]}" 
        emitter <<f"   store {registo}, {tipo}* {i}, align {align}" 

    elif node['nt'] == 'Create_Array':
        a = compilador(node["Array_Size"], emitter)
        return 
# --------------------------------- VARIABLES -------------------------------- #

    elif node['nt'] == "Variable Declaration":
        nome = node['Variable Name']
        typee = node['type']
        expr = node['Expression']
        pnome = emitter.get_pointer_name(nome)
        tipo = emitter.get_etypes(typee)
        align = emitter.get_align(typee)
        name = nome + "_var"

        if expr['nt'] == 'lambda':
            emitter.lmbd = ( nome,typee )
            rr = compilador(expr, emitter)
            return

        else:
            emitter.set_type(name, typee)           

            registo = compilador(expr, emitter)
        
            if "i1" in tipo:
                tipo = "i8"
    
            emitter << f"   {pnome} = alloca {tipo}, align {align}"

            if "i1" in registo:
                if "true" in registo:
                    registo = "i8 1"
                elif "false" in registo:
                    registo = "i8 0"
        
            emitter << f"   store {registo}, {tipo}* {pnome}, align {align}"
            return

   

    elif node['nt'] == "Variable Assignment":        
        expr = node['Expression']
        vnome = node['Variable']
        name = vnome + "_var"     
        if expr['nt'] == 'lambda':          
            tipo = emitter.get_type(name)            
            rr = compilador(expr, emitter)
            return

        else: 
            tipo = emitter.get_type(name) 

        registo = compilador(expr, emitter)
        pnome = emitter.get_pointer_name(vnome)        
        tipo_e = emitter.get_etypes(tipo) 
        align = emitter.get_align(tipo)
        
        if tipo_e == None:
            name = vnome + "_VArg"
            tipo_e = emitter.get_etypes(tipo)
            align = emitter.get_align(tipo)
            pnome = emitter.get_id_name(pnome)
                
        emitter << f"   store {registo}, {tipo_e}* {pnome}, align {align}"
        return
        
    elif node['nt'] == 'Variable':
        vname = node["Value"]    
        name = vname + "_var"
        reg = "%" + emitter.get_id()
        pname = emitter.get_pointer_name(vname)
        
        if emitter.isLambda == True:
            if emitter.isLambdaExp == True:
                tipo = emitter.get_type(name)
                if tipo != None:
                    arg = {'nt': 'Variable Name', 'variable_name': vname, 'type':tipo}
                    emitter.ext_var += vname 
                    if arg not in emitter.lambda_args:
                        emitter.lambda_args.append(arg)
                        emitter.set_type(name, tipo)                        
            else:
                tipo = emitter.get_type(name)

                if tipo == None:
                    name = vname + "_VArg"
                    tipo = emitter.get_type(name)
                    pname = emitter.get_id_name(pname)

                tipo_e = emitter.get_etypes(tipo)
                align = emitter.get_align(tipo)
                if vname in emitter.ext_var:
                    pname = emitter.get_id_name(pname)                  
                
                
                emitter.lambda_fun.append(f"   {reg} = load {tipo_e}, {tipo_e}* {pname}, align {align}")
                return f"{tipo_e} {reg}"
        
        else:
            tipo = emitter.get_type(name)
            tipo_e = emitter.get_etypes(tipo)
            align = emitter.get_align(tipo)

            if tipo_e == None:
                nome = vname + "_VArg"
                tipo = emitter.get_type(nome)
                tipo_e = emitter.get_etypes(tipo) 
                align = emitter.get_align(tipo)           
                pname = emitter.get_id_name(pname)

            if "i1" in tipo_e:
                tipo_e = "i8"

            emitter << f"   {reg} = load {tipo_e}, {tipo_e}* {pname}, align {align}"
            return f"{tipo_e} {reg}"

# ----------------------------- BIANRY OPERATIONS ---------------------------- #
     
    elif node['nt'] == "Binary Operation":
        Operador = node['Operator']      
          
        if Operador == "<":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")                       
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f"    {rr} = fcmp olt {ler}, {rer[1]}"
            else:
                emitter <<f"    {rr} = icmp slt {ler}, {rer[1]}"           
            return f"i1 {rr}"
        
        elif Operador == ">":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")                       
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f"    {rr} = fcmp ogt {ler}, {rer[1]}"
            else:
                emitter <<f"    {rr} = icmp sgt {ler}, {rer[1]}"           
            return f"i1 {rr}"
        
        elif Operador == ">=":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")                       
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f"    {rr} = fcmp oge {ler}, {rer[1]}"
            else:
                emitter <<f"    {rr} = icmp sge {ler}, {rer[1]}"           
            return f"i1 {rr}"
        
        elif Operador == "<=":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")                       
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f"    {rr} = fcmp ole {ler}, {rer[1]}"
            else:
                emitter <<f"    {rr} = icmp sle {ler}, {rer[1]}"           
            return f"i1 {rr}"
        
        elif Operador == "+":            
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            if emitter.isLambdaExp == False:                
                rr = "%" + emitter.get_id()
                rer = temp.split(" ")
                if emitter.isLambda == True:
                    if rer[0] == "float":
                        emitter.lambda_fun.append(f"   {rr} = fadd {ler}, {rer[1]}")
                    else: 
                        emitter.lambda_fun.append(f"   {rr} = add nsw {ler}, {rer[1]}" )
                else:
                    if rer[0] == "float":
                        emitter << f"   {rr} = fadd {ler}, {rer[1]}"	
                    else:
                        emitter << f"   {rr} = add nsw {ler}, {rer[1]}"
                                
                return f"{rer[0]} {rr}"
        
        elif Operador == "-":           
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            
            if emitter.isLambdaExp == False:
                rr = "%" + emitter.get_id()
                rer = temp.split(" ")
                if emitter.isLambda == True:
                    if rer[0] == "float":
                        emitter.lambda_fun.append(f"   {rr} = fsub {ler}, {rer[1]}")
                    else: 
                        emitter.lambda_fun.append(f"    {rr} = sub nsw {ler}, {rer[1]}")
                else:
                    if rer[0] == "float":
                        emitter << f"   {rr} = fsub {ler}, {rer[1]}"	
                    else:
                        emitter << f"    {rr} = sub nsw {ler}, {rer[1]}" 

                return f"{rer[0]} {rr}"
            
        elif Operador == "*":           
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rr = "%" + emitter.get_id()
            rer = temp.split(" ")
            if emitter.isLambda == True:
                if rer[0] == "float":
                    emitter.lambda_fun.append(f"    {rr} = fmul {ler}, {rer[1]}")
                else: 
                    emitter.lambda_fun.append(f"    {rr} = mul nsw {ler}, {rer[1]}")
                    
            elif emitter.isLambdaExp == True:
                pass
            else:
                if rer[0] == "float":
                    emitter << f"   {rr} = fmul {ler}, {rer[1]}"	
                else:
                    emitter << f"   {rr} = mul nsw {ler}, {rer[1]}" 
        
            return f"{rer[0]} {rr}"

        elif Operador == "/":           
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rr = "%" + emitter.get_id()
            rer = temp.split(" ")
            if emitter.isLambda == True:
                if rer[0] == "float":
                    emitter.lambda_fun.append(f"   {rr} = fdiv {ler}, {rer[1]}")
                else: 
                    emitter.lambda_fun.append(f"    {rr} = sdiv {ler}, {rer[1]}")
            
            elif emitter.isLambdaExp == True:
                pass
            else:
                if rer[0] == "float":
                    emitter << f"   {rr} = fdiv {ler}, {rer[1]}"	
                else:
                    emitter << f"   {rr} = sdiv {ler}, {rer[1]}" 

            return f"{rer[0]} {rr}"
        
        elif Operador == "%":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")
            rr = "%" + emitter.get_id()

            if emitter.isLambda == True:
                emitter.lambda_fun.append(f"    {rr} = srem {ler}, {rer[1]}")
                
            elif emitter.isLambdaExp == True:
                pass
            else:
                emitter <<f"    {rr} = srem {ler}, {rer[1]}"   

            return f"{rer[0]} {rr}"
        
        elif Operador == "&&":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter']  
            
            labels = emitter.get_labels()
            label_and = "start_and_" + labels[0][9:]
            label_or = labels[1]
            var = emitter.get_count()
            var2 = emitter.get_count()
            i = ""
            j = "" 

            if emitter.not_ == True:
                ler = compilador(l_express,emitter)
                if "OR" and "AND" not in ler:
                    if "not" in ler:
                        ler = ler.split("-")
                        emitter << f"   br{ler[1]}, label % {labels[0]}, label %{label_and}_{var}"
                    else:
                        emitter << f"   br{ler},  label %{label_and}_{var}, label %{labels[0]}"
                    emitter << f"{label_and}_{var}:"

                rer = compilador(r_express, emitter)
                if "OR" and "AND" not in rer:
                    if "not" in rer:
                        rer = rer.split("-")
                        emitter << f"   br{rer[1]}, label % {labels[0]}, label %{label_and}_{var2}"
                    else:
                        emitter << f"   br{ler},  label %{label_and}_{var2}, label %{labels[0]}"
                    emitter << f"{label_and}_{var2}:"
                j = "not"
                emitter.not_ = False
            else:
                if emitter.OR == True:
                    label_or = f"{label_and}_{var2}"

                emitter.AND = True
                ler = compilador(l_express, emitter)
                if "OR" and "AND" not in ler:
                    if "not" in ler:
                        ler = ler.split("-")
                        emitter << f"   br{ler[1]}, label % {label_or}, label %{label_and}_{var}"
                    else:
                        emitter << f"   br{ler},  label %{label_and}_{var}, label %{label_or}"
                    emitter << f"{label_and}_{var}:" 

                emitter.AND = False                  
                rer = compilador(r_express, emitter)
                if "OR" and "AND" not in rer:
                    if "not" in rer:
                        rer = rer.split("-")
                        emitter << f"   br{rer[1]}, label % {label_or}, label %{label_and}_{var2}"
                    else:
                        emitter << f"   br{ler},  label %{label_and}_{var2}, label %{label_or}"
                    emitter << f"{label_and}_{var2}:"
                
                if "OR" in rer:
                    i = "1"
                return f"AND {i} {j}"

        elif Operador == "||":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter']  
            
            labels = emitter.get_labels()
            label_or = "start_or_" + labels[0][9:]
            label_and = labels[0]
            var = emitter.get_count()
            var2 = emitter.get_count()
            i = ""
            j = "" 

            if emitter.not_ == True:
                ler = compilador(l_express,emitter)
                if "OR" and "AND" not in ler:
                    if "not" in ler:
                        ler = ler.split("-")
                        emitter << f"   br{ler[1]}, label % {label_or}_{var}, label %{labels[1]}"
                    else:
                        emitter << f"   br{ler}, label %{labels[1]}, label %{label_or}_{var} "
                    emitter << f"{label_or}_{var}:"

                rer = compilador(r_express, emitter)
                if "OR" and "AND" not in rer:
                    if "not" in rer:
                        rer = rer.split("-")
                        emitter << f"   br{rer[1]}, label %{label_or}_{var2}, label % {labels[1]}"
                    else:
                        emitter << f"   br{ler}, label %{labels[1]}, label %{label_or}_{var2}"
                    emitter << f"{label_or}_{var2}:"
                j = "not"
                emitter.not_ = False
            else:
                if emitter.AND == True:
                    label_or = f"{label_or}_{var2}"

                emitter.OR = True
                ler = compilador(l_express, emitter)
                if "OR" and "AND" not in ler:
                    if "not" in ler:
                        ler = ler.split("-")
                        emitter << f"   br{ler[1]}, label %{label_or}_{var}, label % {label_and}"
                    else:
                        emitter << f"   br{ler}, label %{label_and}, label %{label_or}_{var}"
                    emitter << f"{label_or}_{var}:" 

                emitter.OR = False                  
                rer = compilador(r_express, emitter)
                if "OR" and "AND" not in rer:
                    if "not" in rer:
                        rer = rer.split("-")
                        emitter << f"   br{rer[1]}, label %{label_or}_{var2} , label % {label_and}"
                    else:
                        emitter << f"   br{ler}, label %{label_and}, label %{label_or}_{var2}"
                    emitter << f"{label_or}_{var2}:"
                
                if "AND" in rer:
                    i = "1"
                return f"OR {i} {j}"
             
        elif Operador == "!=":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer = temp.split(" ")
            
            if "i8" in ler:
                reg1 = "%" + emitter.get_id()
                reg2 = "%" + emitter.get_id()
                
                emitter << f"   {reg1} = trunc {ler} to i1"
                emitter << f"   {reg2} = zext i1 {reg1} to i32"
                
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
                
                emitter << f"   {reg1} = trunc {rer[0]} {rer[1]} to i1"
                
                emitter << f"   {reg2} = zext i1 {reg1} to i32"
                
                registo_r[1] = f"{reg2}"
                
            rr = "%" + emitter.get_id()
            if rer[0] == "float":
                emitter <<f"   {rr} = fcmp une {ler}, {rer[1]}"
            else:
                emitter <<f"   {rr} = icmp ne {ler}, {rer[1]}"  
                
            return f"i1 {rr}"
        
        elif Operador == "==":
            l_express = node['Left Parameter']
            r_express = node['Right Parameter'] 
            ler = compilador(l_express,emitter)
            temp = compilador(r_express, emitter)
            rer= temp.split(" ")
            
            
            if "i8" in ler:
                reg1 = "%" + emitter.get_id()
                reg2 = "%" + emitter.get_id()
                
                emitter << f"   {reg1} = trunc {ler} to i1"
                emitter << f"   {reg2} = zext i1 {reg1} to i32"
                
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
                emitter << f"   {reg1} = trunc {rer[0]} {rer[1]} to i1"
                emitter << f"   {reg2} = zext i1 {reg1} to i32"
                registo_r[1] = f"{reg2}"

            rr = "%" + emitter.get_id()
   
            if rer[0] == "float":
                emitter <<f"   {rr} = fcmp oeq {ler}, {rer[1]}"

            else:
                emitter <<f"   {rr} = icmp eq {ler}, {rer[1]}"
            
            return f"i1 {rr}"

# ----------------------------------- TYPES ---------------------------------- #

    elif node['nt'] == 'String':
        typee = emitter.get_etypes(node["nt"])
        value = node["Value"]
        valor = value.replace('"', '')
        counter = valor.count("\\n")
        value = valor.replace("\\n", "")
        valor = valor.replace("\\n", "\\0A")
        size = 1        
        size += counter
        size += len(value)
        id = emitter.get_id()

        string_n = f"@.casual_str_{id}"
        decl = f"""{string_n} = private unnamed_addr constant [{size} x i8] c"{valor}\\00", align 1"""
        emitter.lines.insert(0, decl)
        
        return f"i8* getelementptr inbounds ([{size} x i8], [{size} x i8]* {string_n}, i64 0, i64 0)"
    
    elif node['nt'] =='Int':
        typee = emitter.get_etypes(node["nt"])
        value = str(node["Value"])
        return f"{typee} {value}"

    elif node['nt'] =='Float':
        typee = emitter.get_etypes(node["nt"])
        value = node["Value"]
        float_single = struct.unpack('f', struct.pack('f', value))[0]
        valor = hex(struct.unpack('<Q', struct.pack('<d', float_single))[0])
        return f"{typee} {valor}"
        
    elif node['nt'] == 'Boolean':
        typee = "i1"
        value = node["Value"]
        return f"{typee} {value}"

    elif node['nt'] == 'Void':
        return "void"


# -------------------------- GROUP NOT UMINUS S_EXP -------------------------- #

    elif node['nt'] == 'Group':
        valor = node["Valor"]      
        g_exp = compilador(valor, emitter)
        
        return g_exp

    elif node['nt'] == 'Not':

        emitter.not__count += 1
        expr = node["value"]

        if expr["nt"] != "Not_Unary":
            if emitter.not__count % 2 == 0:
                emitter.not__count = 0
                reg = compilador(expr["value"], emitter)
                return reg
            else:
                if expr["nt"] == "Group_expr":		
                    var = expr["value"]
                    if var["operator"] == "&&" or var["operator"] == "||":
                        emitter.not_ = True

                emitter.not__count = 0
                reg = compilador(expr, emitter)
                return f"not-{reg}"
        else:
            reg = compilador(expr, emitter)
            return reg

    elif node['nt'] == 'Uminus':
        express = compilador(node['Valor'], emitter)
        express = express.split(" ") 
        
        return f"{express[0]} -{express[1]}"
    
    elif node['nt'] == 'Statement Expression':
        St  = node['Expression']
        se = compilador(St, emitter)
        
        return 
# ---------------------------------- LAMBDA ---------------------------------- #

    elif node['nt'] == 'lambda':
        index = 0
        for line in emitter.lines:
            if "define" in line:
                index = emitter.lines.index(line)

        emitter.lambda_args = []

        for arg in node['Arguments']:
            if arg != "Void":
                emitter.lambda_args.append({'nt': 'Variable Name', 'variable_name': arg['variable_name'], 'type':arg['type']})
       
        emitter.isLambda = True
        emitter.isLambdaExp = True

        compilador(node['Expression'], emitter)
        
        emitter.isLambdaExp = False 

        newF={'nt': 'Definition', 'F_Name' : emitter.lmbd[0], 'Argument': emitter.lambda_args, 'Type': emitter.lmbd[1], 'Block': [{ 'nt': 'Return', 'Expression': node['Expression']}]}
        
        emitter.lambda_fun_is.append(emitter.lmbd[0])
        compilador(newF, emitter) 
               
        for line in emitter.lambda_fun:                         
            emitter.lines.insert(index, line)
            index += 1
        
        
        emitter.isLambda = False

        return 

# ---------------------------- FUNCTION INVOCATION --------------------------- #

    elif node['nt'] == "Function Invocation":
        fname = node['Function Name'] 
        name = fname + "_function"
        reg_arg = ""
        
        typee = emitter.get_etypes(emitter.get_type(name))
        t_name = emitter.get_pointer_name(fname)
        
        pname = t_name + "_" + str(emitter.get_count())
        
        if emitter.isLambda == False:
            for i in emitter.lambda_fun_is:
                if i == fname:
                    for j in emitter.ext_var:
                        j_dic = {'nt': 'Variable', 'Value': j} 
                        node["Function Arguments"].append(j_dic)

        for argument in node["Function Arguments"]:
            if argument['nt'] == "Void":
                reg_arg = ""
            else:
                t = compilador(argument, emitter) + ", "
                if "i1" in t:
                    t = t.replace("i1", "i1 zeroext")
                elif "i8" in t and "*" not in t:
                    variable = t.split(" ")
                    variable[1] = variable[1].replace(",", "")
                    treg = "%" + emitter.get_id()
                    
                    emitter << f"   {treg} = trunc i8 {variable[1]} to i1"
                reg_arg += t     
        reg_arg = reg_arg[:-2]
        if typee == "void":
            emitter << f"   call {typee} @{fname} ({reg_arg})"
        else:
            emitter << f"   {pname} = call {typee} @{fname}({reg_arg})"
        
        if "i1" in typee:
            treg = "%" + emitter.get_id()
            emitter << f"   {treg} = zext i1 {pname} to i8"
            tipo = "i8"
            pname = treg
   
        return f"{typee} {pname}"


# ----------------------------------- PRINT ---------------------------------- #

    elif node['nt'] == "Print":
        prt_string = node["print_string"]
        node_ = {'nt': 'String', 'Value': prt_string}
        registo_string = compilador(node_,emitter)
        arguments = ""
        for argument in node["print_arguments"]:
            if argument["nt"] == "Void":
                print (argument['nt'])
                arguments = ""
            else:
                i = compilador(argument, emitter)
                if "float" in i:
                    registo = "%" + emitter.get_id()
                    emitter << f"   {registo} = fpext {i} to double"
                    i = f"double {registo}"
                arguments += ","
                arguments += i
                
        print_registo = "%" + emitter.get_id()
        emitter << f"   call i32 (i8*, ...) @printf({registo_string}{arguments})"

# ---------------------------------- RETURN ---------------------------------- #

    elif node['nt'] == "Return":
        ret_cond = node["Expression"]
        if ret_cond != None:
            reg = compilador(ret_cond, emitter)
        else:
            reg = "void"
        
        if "i8" in reg and "*" not in reg:
            t_reg = "%" + emitter.get_id()
            i = emitter.get_count()
            if emitter.isLambda == True:
                emitter.lambda_fun.append(f"   {t_reg} = trunc i8 %cas_{i} to i1")
            elif emitter.isLambdaExp == True:
                pass
            else: 
                emitter << f"   {t_reg} = trunc i8 %cas_{i} to i1"
            reg = f"i1 {t_reg}"
        
        if emitter.isLambda == True:
            emitter.lambda_fun.append(f"   ret {reg}")
        elif emitter.isLambdaExp == True:
            pass
        else:     
            emitter << f"   ret {reg}"  
        
