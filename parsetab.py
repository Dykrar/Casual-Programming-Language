
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'programleftANDORnonassocLESS_OR_EQUALSGREATER_OR_EQUALGREATERLESSCOMPNOT_EQUALSNOTleftPLUSMINUSleftTIMESDIVIDEMODULOrightUMINUSAND BOOL_TYPE COLON COMMA COMP DECL DEF DIVIDE ELSE EQUALS FALSE FLOAT FLOAT_TYPE GET_ARRAY GREATER GREATER_OR_EQUAL IF INT INT_TYPE LBRACKET LESS LESS_OR_EQUALS LPAREN LRPAREN MINUS MODULO NOT NOT_EQUALS OR PLUS PRINT RBRACKET RETURN RPAREN RRPAREN SEMICOLONS STRING STRING_TYPE TIMES TRUE VARIABLE VOID_TYPE WHILEdef_declr : declaration def_declr\n                 | definition def_declr\n                 | declaration\n                 | definition program : def_declr empty : declaration : DECL VARIABLE LPAREN varg RPAREN COLON type\n                   | DECL VARIABLE LPAREN arg RPAREN COLON typedefinition : DEF VARIABLE LPAREN arg RPAREN COLON type block\n                  | DEF VARIABLE LPAREN varg RPAREN COLON type block varg : arg : VARIABLE COLON type\n           | VARIABLE COLON type COMMA argblock : LBRACKET block_content RBRACKET\n             | LBRACKET empty RBRACKET block_content : statement block_content\n                      | statementstatement     : return  \n                     | stat_expression \n                     | if \n                     | if_else \n                     | while \n                     | var_decl \n                     | var_ass\n                     | array_decl\n                     | array_ass\n                     | printprint_helper : COMMA expression\n\t                | COMMA expression print_helperprint : PRINT LPAREN STRING print_helper RPAREN SEMICOLONS\n\t         | PRINT LPAREN STRING empty RPAREN SEMICOLONSreturn : RETURN SEMICOLONS\n              | RETURN expression SEMICOLONSstat_expression : expression SEMICOLONS if : IF expression blockif_else : IF expression block ELSE blockwhile : WHILE expression blockvar_decl : VARIABLE COLON type EQUALS expression SEMICOLONSarray_decl : VARIABLE COLON LRPAREN type RRPAREN SEMICOLONSarray_ass : VARIABLE LRPAREN expression RRPAREN EQUALS expression SEMICOLONStype : INT_TYPE\n            | FLOAT_TYPE\n            | STRING_TYPE\n            | BOOL_TYPE  \n            | VOID_TYPEvar_ass : VARIABLE EQUALS expression SEMICOLONSexpression : expression PLUS expression\n                  | expression MINUS expression\n                  | expression TIMES expression\n                  | expression DIVIDE expression\n                  | expression COMP expression\n                  | expression AND expression\n                  | expression OR expression\n                  | expression NOT_EQUALS expression\n                  | expression GREATER_OR_EQUAL expression\n                  | expression LESS_OR_EQUALS expression\n                  | expression GREATER expression\n                  | expression LESS expression\n                  | expression MODULO expressionexpression : MINUS expression %prec UMINUSexpression : LPAREN expression RPARENexpression : INTexpression : FLOATexpression : STRINGexpression : TRUE\n                  | FALSEexpression : VARIABLEexpression : NOT expressionexpression : VARIABLE LRPAREN expression RRPAREN  \n                  | GET_ARRAY LRPAREN expression RRPAREN expression : VARIABLE LPAREN argument_f RPARENargf :arg_f : expression \n             | expression COMMA arg_fargument_f : arg_f\n                  | argf '
    
_lr_action_items = {'DECL':([0,3,4,24,25,26,27,28,34,35,39,41,70,71,],[5,5,5,-41,-42,-43,-44,-45,-7,-8,-9,-10,-14,-15,]),'DEF':([0,3,4,24,25,26,27,28,34,35,39,41,70,71,],[6,6,6,-41,-42,-43,-44,-45,-7,-8,-9,-10,-14,-15,]),'$end':([1,2,3,4,7,8,24,25,26,27,28,34,35,39,41,70,71,],[0,-5,-3,-4,-1,-2,-41,-42,-43,-44,-45,-7,-8,-9,-10,-14,-15,]),'VARIABLE':([5,6,11,12,33,40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,61,63,68,70,71,73,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[9,10,13,13,13,59,59,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,75,75,75,75,75,75,-14,-15,-32,-34,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,-33,75,-35,-37,75,-46,75,75,-36,75,-38,-39,-30,-31,-40,]),'LPAREN':([9,10,40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,59,60,61,63,68,70,71,73,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[11,12,61,61,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,61,61,61,95,96,61,61,61,-14,-15,-32,95,-34,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,-33,61,-35,-37,61,-46,61,61,-36,61,-38,-39,-30,-31,-40,]),'RPAREN':([11,12,14,15,16,17,23,24,25,26,27,28,38,62,64,65,66,67,75,95,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,122,123,124,125,126,127,135,137,138,140,141,146,149,155,],[-11,-11,19,20,21,22,-12,-41,-42,-43,-44,-45,-13,-64,-62,-63,-65,-66,-67,-72,127,-60,-68,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,135,-75,-76,-73,-6,-61,-71,147,148,-70,-69,-74,-28,-29,]),'COLON':([13,19,20,21,22,59,],[18,29,30,31,32,92,]),'INT_TYPE':([18,29,30,31,32,92,119,],[24,24,24,24,24,24,24,]),'FLOAT_TYPE':([18,29,30,31,32,92,119,],[25,25,25,25,25,25,25,]),'STRING_TYPE':([18,29,30,31,32,92,119,],[26,26,26,26,26,26,26,]),'BOOL_TYPE':([18,29,30,31,32,92,119,],[27,27,27,27,27,27,27,]),'VOID_TYPE':([18,29,30,31,32,92,119,],[28,28,28,28,28,28,28,]),'COMMA':([23,24,25,26,27,28,62,64,65,66,67,75,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,125,126,127,135,140,141,149,],[33,-41,-42,-43,-44,-45,-64,-62,-63,-65,-66,-67,-60,-68,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,136,139,-61,-71,-70,-69,139,]),'LBRACKET':([24,25,26,27,28,36,37,62,64,65,66,67,75,90,91,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,127,130,135,140,141,],[-41,-42,-43,-44,-45,40,40,-64,-62,-63,-65,-66,-67,40,40,-60,-68,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-61,40,-71,-70,-69,]),'EQUALS':([24,25,26,27,28,59,118,134,],[-41,-42,-43,-44,-45,93,131,145,]),'RRPAREN':([24,25,26,27,28,62,64,65,66,67,75,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,121,127,128,129,132,135,140,141,],[-41,-42,-43,-44,-45,-64,-62,-63,-65,-66,-67,-60,-68,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,134,-61,140,141,144,-71,-70,-69,]),'RBRACKET':([40,42,43,44,45,46,47,48,49,50,51,52,53,54,70,71,72,73,76,101,116,117,133,142,150,151,153,154,156,],[-6,70,71,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-14,-15,-16,-32,-34,-33,-35,-37,-46,-36,-38,-39,-30,-31,-40,]),'RETURN':([40,44,45,46,47,48,49,50,51,52,53,54,70,71,73,76,101,116,117,133,142,150,151,153,154,156,],[55,55,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-14,-15,-32,-34,-33,-35,-37,-46,-36,-38,-39,-30,-31,-40,]),'IF':([40,44,45,46,47,48,49,50,51,52,53,54,70,71,73,76,101,116,117,133,142,150,151,153,154,156,],[57,57,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-14,-15,-32,-34,-33,-35,-37,-46,-36,-38,-39,-30,-31,-40,]),'WHILE':([40,44,45,46,47,48,49,50,51,52,53,54,70,71,73,76,101,116,117,133,142,150,151,153,154,156,],[58,58,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-14,-15,-32,-34,-33,-35,-37,-46,-36,-38,-39,-30,-31,-40,]),'PRINT':([40,44,45,46,47,48,49,50,51,52,53,54,70,71,73,76,101,116,117,133,142,150,151,153,154,156,],[60,60,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-14,-15,-32,-34,-33,-35,-37,-46,-36,-38,-39,-30,-31,-40,]),'MINUS':([40,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,61,62,63,64,65,66,67,68,70,71,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,93,94,95,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,120,121,125,127,128,129,131,133,134,135,136,139,140,141,142,143,145,149,150,151,152,153,154,156,],[63,63,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,63,78,63,63,-67,63,-64,63,-62,-63,-65,-66,63,-14,-15,-32,78,-67,-34,63,63,63,63,63,63,63,63,63,63,63,63,63,78,78,63,63,63,78,-60,78,63,-33,63,-47,-48,-49,-50,78,78,78,78,78,78,78,78,-59,-35,-37,78,78,78,-61,78,78,63,-46,-69,-71,63,63,-70,-69,-36,78,63,78,-38,-39,78,-30,-31,-40,]),'INT':([40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,61,63,68,70,71,73,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[64,64,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,64,64,64,64,64,64,-14,-15,-32,-34,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,64,-33,64,-35,-37,64,-46,64,64,-36,64,-38,-39,-30,-31,-40,]),'FLOAT':([40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,61,63,68,70,71,73,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[65,65,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,65,65,65,65,65,65,-14,-15,-32,-34,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,65,-33,65,-35,-37,65,-46,65,65,-36,65,-38,-39,-30,-31,-40,]),'STRING':([40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,61,63,68,70,71,73,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,96,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[62,62,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,62,62,62,62,62,62,-14,-15,-32,-34,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,126,62,-33,62,-35,-37,62,-46,62,62,-36,62,-38,-39,-30,-31,-40,]),'TRUE':([40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,61,63,68,70,71,73,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[66,66,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,66,66,66,66,66,66,-14,-15,-32,-34,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,66,-33,66,-35,-37,66,-46,66,66,-36,66,-38,-39,-30,-31,-40,]),'FALSE':([40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,61,63,68,70,71,73,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[67,67,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,67,67,67,67,67,67,-14,-15,-32,-34,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,-33,67,-35,-37,67,-46,67,67,-36,67,-38,-39,-30,-31,-40,]),'NOT':([40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,61,63,68,70,71,73,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[68,68,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,68,68,68,68,68,68,-14,-15,-32,-34,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,-33,68,-35,-37,68,-46,68,68,-36,68,-38,-39,-30,-31,-40,]),'GET_ARRAY':([40,44,45,46,47,48,49,50,51,52,53,54,55,57,58,61,63,68,70,71,73,76,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,101,102,116,117,131,133,136,139,142,145,150,151,153,154,156,],[69,69,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,69,69,69,69,69,69,-14,-15,-32,-34,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,69,-33,69,-35,-37,69,-46,69,69,-36,69,-38,-39,-30,-31,-40,]),'SEMICOLONS':([55,56,59,62,64,65,66,67,74,75,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,127,134,135,140,141,143,144,147,148,152,],[73,76,-67,-64,-62,-63,-65,-66,101,-67,-60,-68,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,133,-61,-69,-71,-70,-69,150,151,153,154,156,]),'PLUS':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[77,-67,-64,-62,-63,-65,-66,77,-67,77,77,77,-60,77,-47,-48,-49,-50,77,77,77,77,77,77,77,77,-59,77,77,77,-61,77,77,-69,-71,-70,-69,77,77,77,]),'TIMES':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[79,-67,-64,-62,-63,-65,-66,79,-67,79,79,79,-60,79,79,79,-49,-50,79,79,79,79,79,79,79,79,-59,79,79,79,-61,79,79,-69,-71,-70,-69,79,79,79,]),'DIVIDE':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[80,-67,-64,-62,-63,-65,-66,80,-67,80,80,80,-60,80,80,80,-49,-50,80,80,80,80,80,80,80,80,-59,80,80,80,-61,80,80,-69,-71,-70,-69,80,80,80,]),'COMP':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[81,-67,-64,-62,-63,-65,-66,81,-67,81,81,81,-60,None,-47,-48,-49,-50,None,81,81,None,None,None,None,None,-59,81,81,81,-61,81,81,-69,-71,-70,-69,81,81,81,]),'AND':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[82,-67,-64,-62,-63,-65,-66,82,-67,82,82,82,-60,-68,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,82,82,82,-61,82,82,-69,-71,-70,-69,82,82,82,]),'OR':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[83,-67,-64,-62,-63,-65,-66,83,-67,83,83,83,-60,-68,-47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,83,83,83,-61,83,83,-69,-71,-70,-69,83,83,83,]),'NOT_EQUALS':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[84,-67,-64,-62,-63,-65,-66,84,-67,84,84,84,-60,None,-47,-48,-49,-50,None,84,84,None,None,None,None,None,-59,84,84,84,-61,84,84,-69,-71,-70,-69,84,84,84,]),'GREATER_OR_EQUAL':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[85,-67,-64,-62,-63,-65,-66,85,-67,85,85,85,-60,None,-47,-48,-49,-50,None,85,85,None,None,None,None,None,-59,85,85,85,-61,85,85,-69,-71,-70,-69,85,85,85,]),'LESS_OR_EQUALS':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[86,-67,-64,-62,-63,-65,-66,86,-67,86,86,86,-60,None,-47,-48,-49,-50,None,86,86,None,None,None,None,None,-59,86,86,86,-61,86,86,-69,-71,-70,-69,86,86,86,]),'GREATER':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[87,-67,-64,-62,-63,-65,-66,87,-67,87,87,87,-60,None,-47,-48,-49,-50,None,87,87,None,None,None,None,None,-59,87,87,87,-61,87,87,-69,-71,-70,-69,87,87,87,]),'LESS':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[88,-67,-64,-62,-63,-65,-66,88,-67,88,88,88,-60,None,-47,-48,-49,-50,None,88,88,None,None,None,None,None,-59,88,88,88,-61,88,88,-69,-71,-70,-69,88,88,88,]),'MODULO':([56,59,62,64,65,66,67,74,75,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,127,128,129,134,135,140,141,143,149,152,],[89,-67,-64,-62,-63,-65,-66,89,-67,89,89,89,-60,89,89,89,-49,-50,89,89,89,89,89,89,89,89,-59,89,89,89,-61,89,89,-69,-71,-70,-69,89,89,89,]),'LRPAREN':([59,69,75,92,],[94,100,102,119,]),'ELSE':([70,71,116,],[-14,-15,130,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'def_declr':([0,3,4,],[2,7,8,]),'declaration':([0,3,4,],[3,3,3,]),'definition':([0,3,4,],[4,4,4,]),'varg':([11,12,],[14,17,]),'arg':([11,12,33,],[15,16,38,]),'type':([18,29,30,31,32,92,119,],[23,34,35,36,37,118,132,]),'block':([36,37,90,91,130,],[39,41,116,117,142,]),'block_content':([40,44,],[42,72,]),'empty':([40,126,],[43,138,]),'statement':([40,44,],[44,44,]),'return':([40,44,],[45,45,]),'stat_expression':([40,44,],[46,46,]),'if':([40,44,],[47,47,]),'if_else':([40,44,],[48,48,]),'while':([40,44,],[49,49,]),'var_decl':([40,44,],[50,50,]),'var_ass':([40,44,],[51,51,]),'array_decl':([40,44,],[52,52,]),'array_ass':([40,44,],[53,53,]),'print':([40,44,],[54,54,]),'expression':([40,44,55,57,58,61,63,68,77,78,79,80,81,82,83,84,85,86,87,88,89,93,94,95,100,102,131,136,139,145,],[56,56,74,90,91,97,98,99,103,104,105,106,107,108,109,110,111,112,113,114,115,120,121,125,128,129,143,125,149,152,]),'argument_f':([95,],[122,]),'arg_f':([95,136,],[123,146,]),'argf':([95,],[124,]),'print_helper':([126,149,],[137,155,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('def_declr -> declaration def_declr','def_declr',2,'p_def_declr','projeto3.py',153),
  ('def_declr -> definition def_declr','def_declr',2,'p_def_declr','projeto3.py',154),
  ('def_declr -> declaration','def_declr',1,'p_def_declr','projeto3.py',155),
  ('def_declr -> definition','def_declr',1,'p_def_declr','projeto3.py',156),
  ('program -> def_declr','program',1,'p_program','projeto3.py',164),
  ('empty -> <empty>','empty',0,'p_empty','projeto3.py',169),
  ('declaration -> DECL VARIABLE LPAREN varg RPAREN COLON type','declaration',7,'p_declaration','projeto3.py',172),
  ('declaration -> DECL VARIABLE LPAREN arg RPAREN COLON type','declaration',7,'p_declaration','projeto3.py',173),
  ('definition -> DEF VARIABLE LPAREN arg RPAREN COLON type block','definition',8,'p_definition','projeto3.py',178),
  ('definition -> DEF VARIABLE LPAREN varg RPAREN COLON type block','definition',8,'p_definition','projeto3.py',179),
  ('varg -> <empty>','varg',0,'p_varg','projeto3.py',184),
  ('arg -> VARIABLE COLON type','arg',3,'p_arg','projeto3.py',189),
  ('arg -> VARIABLE COLON type COMMA arg','arg',5,'p_arg','projeto3.py',190),
  ('block -> LBRACKET block_content RBRACKET','block',3,'p_block','projeto3.py',197),
  ('block -> LBRACKET empty RBRACKET','block',3,'p_block','projeto3.py',198),
  ('block_content -> statement block_content','block_content',2,'p_block_content','projeto3.py',204),
  ('block_content -> statement','block_content',1,'p_block_content','projeto3.py',205),
  ('statement -> return','statement',1,'p_statement','projeto3.py',216),
  ('statement -> stat_expression','statement',1,'p_statement','projeto3.py',217),
  ('statement -> if','statement',1,'p_statement','projeto3.py',218),
  ('statement -> if_else','statement',1,'p_statement','projeto3.py',219),
  ('statement -> while','statement',1,'p_statement','projeto3.py',220),
  ('statement -> var_decl','statement',1,'p_statement','projeto3.py',221),
  ('statement -> var_ass','statement',1,'p_statement','projeto3.py',222),
  ('statement -> array_decl','statement',1,'p_statement','projeto3.py',223),
  ('statement -> array_ass','statement',1,'p_statement','projeto3.py',224),
  ('statement -> print','statement',1,'p_statement','projeto3.py',225),
  ('print_helper -> COMMA expression','print_helper',2,'p_print_helper','projeto3.py',230),
  ('print_helper -> COMMA expression print_helper','print_helper',3,'p_print_helper','projeto3.py',231),
  ('print -> PRINT LPAREN STRING print_helper RPAREN SEMICOLONS','print',6,'p_statment_print','projeto3.py',238),
  ('print -> PRINT LPAREN STRING empty RPAREN SEMICOLONS','print',6,'p_statment_print','projeto3.py',239),
  ('return -> RETURN SEMICOLONS','return',2,'p_return','projeto3.py',246),
  ('return -> RETURN expression SEMICOLONS','return',3,'p_return','projeto3.py',247),
  ('stat_expression -> expression SEMICOLONS','stat_expression',2,'p_stat_expression','projeto3.py',255),
  ('if -> IF expression block','if',3,'p_if','projeto3.py',260),
  ('if_else -> IF expression block ELSE block','if_else',5,'p_if_else','projeto3.py',266),
  ('while -> WHILE expression block','while',3,'p_while','projeto3.py',271),
  ('var_decl -> VARIABLE COLON type EQUALS expression SEMICOLONS','var_decl',6,'p_variable_declar','projeto3.py',276),
  ('array_decl -> VARIABLE COLON LRPAREN type RRPAREN SEMICOLONS','array_decl',6,'p_array_declaration','projeto3.py',281),
  ('array_ass -> VARIABLE LRPAREN expression RRPAREN EQUALS expression SEMICOLONS','array_ass',7,'p_array_assign','projeto3.py',285),
  ('type -> INT_TYPE','type',1,'p_variable_type','projeto3.py',289),
  ('type -> FLOAT_TYPE','type',1,'p_variable_type','projeto3.py',290),
  ('type -> STRING_TYPE','type',1,'p_variable_type','projeto3.py',291),
  ('type -> BOOL_TYPE','type',1,'p_variable_type','projeto3.py',292),
  ('type -> VOID_TYPE','type',1,'p_variable_type','projeto3.py',293),
  ('var_ass -> VARIABLE EQUALS expression SEMICOLONS','var_ass',4,'p_variable_assign','projeto3.py',297),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','projeto3.py',302),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','projeto3.py',303),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','projeto3.py',304),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','projeto3.py',305),
  ('expression -> expression COMP expression','expression',3,'p_expression_binop','projeto3.py',306),
  ('expression -> expression AND expression','expression',3,'p_expression_binop','projeto3.py',307),
  ('expression -> expression OR expression','expression',3,'p_expression_binop','projeto3.py',308),
  ('expression -> expression NOT_EQUALS expression','expression',3,'p_expression_binop','projeto3.py',309),
  ('expression -> expression GREATER_OR_EQUAL expression','expression',3,'p_expression_binop','projeto3.py',310),
  ('expression -> expression LESS_OR_EQUALS expression','expression',3,'p_expression_binop','projeto3.py',311),
  ('expression -> expression GREATER expression','expression',3,'p_expression_binop','projeto3.py',312),
  ('expression -> expression LESS expression','expression',3,'p_expression_binop','projeto3.py',313),
  ('expression -> expression MODULO expression','expression',3,'p_expression_binop','projeto3.py',314),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','projeto3.py',319),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','projeto3.py',324),
  ('expression -> INT','expression',1,'p_expression_number_int','projeto3.py',329),
  ('expression -> FLOAT','expression',1,'p_expression_number_float','projeto3.py',334),
  ('expression -> STRING','expression',1,'p_expression_string','projeto3.py',339),
  ('expression -> TRUE','expression',1,'p_expression_boolean','projeto3.py',344),
  ('expression -> FALSE','expression',1,'p_expression_boolean','projeto3.py',345),
  ('expression -> VARIABLE','expression',1,'p_expression_variable','projeto3.py',350),
  ('expression -> NOT expression','expression',2,'p_expression_not_unary_op','projeto3.py',355),
  ('expression -> VARIABLE LRPAREN expression RRPAREN','expression',4,'p_expression_index','projeto3.py',360),
  ('expression -> GET_ARRAY LRPAREN expression RRPAREN','expression',4,'p_expression_index','projeto3.py',361),
  ('expression -> VARIABLE LPAREN argument_f RPAREN','expression',4,'p_expression_fun_invocation','projeto3.py',366),
  ('argf -> <empty>','argf',0,'p_argf','projeto3.py',371),
  ('arg_f -> expression','arg_f',1,'p_pre_arg_f','projeto3.py',375),
  ('arg_f -> expression COMMA arg_f','arg_f',3,'p_pre_arg_f','projeto3.py',376),
  ('argument_f -> arg_f','argument_f',1,'p_arg_f','projeto3.py',385),
  ('argument_f -> argf','argument_f',1,'p_arg_f','projeto3.py',386),
]