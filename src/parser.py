#Definición de cómo se usa program

def p_program(p):
	'program : program ID ;'
	pass



#definición de cómo se usa uses

def p_uses(p):
	'uses : USES ID id_list SEMICOLON' 
	pass

def p_id_list(p):
	'''id_list : COMMA ID 
	             | '''
	pass


#Definición de cómo se usa const

def p_const(p):
	'const : CONST  const_list' 
	pass

def p_const_list(p):
	'''const_list : const_list const_declaration 
	              | const_declaration'''
	pass

def p_const_declaration(p): 
	'''const_declaration : ID EQUAL NUMBER SEMICOLON 
	                     | ID EQUAL STRING SEMICOLON'''
	pass



#Definición de cómo se usa type

def p_type(p):
	'type : TYPE  type_list' 
	pass

def p_type_list(p):
	'''type_list : type_list type_declaration | type_declaration'''
	pass

def p_type_declaration(p):
	'''type_declaration : ID EQUAL data_type_list SEMICOLON 
	                    | ID EQUAL LPAREN ID id_list RPAREN SEMICOLON 
						| ID EQUAL INTEGERNUMBER DOBLEDOT INTEGERNUMBER SEMICOLON
						| ID EQUAL CHAR DOBLEDOT CHAR SEMICOLON
						| ID EQUAL RECORD record_list SEMICOLON END SEMICOLON
						| ID EQUAL ARRAY LBRACKET INTEGERNUMBER DOBLEDOT INTEGERNUMER RBRACKET OF data_type_list SEMICOLON
						| ID EQUAL SET OF (data_type_list2 | INTEGERNUMBER DOBLEDOT INTEGERNUMBER | CHAR DOBLEDOT CHAR) SEMICOLON
						| ID EQUAL CARET ID SEMICOLON
	                    | ID COLON file_type SEMICOLON;
						| ID '''
	pass

def p_record_list(p):
	'''record_list : record_list record_declaration | record_declaration'''
	
def p_record_declaration(p):
	'ID COLON data_type_list'



# Definición de cómo se usa var

def p_var(p):
	'var : VAR var_list ' 
	pass

def p_var_list(p):
	'''var_list : var_list var_declaration | var_declaration''' 
	pass

def p_var_declaration(p):
	'''var_declaration : ID COLON data_type_list SEMICOLON
                       | SEMICOLON
					   | SEMICOLON
					   | SEMICOLON 
					   | SEMICOLON
					   | SEMICOLON
	                   | SEMICOLON''' 
	pass



#TODOS LOS TIPOS DE DATOS QUE SE USAN 



def p_data_type_file(p):
	'''data_type_file  : INTEGER
                       | BYTE
					   | LONGINT
					   | SHORTINT
					   | WORD
					   | BOOLEAN
					   | CHAR
					   | REAL 
					   | SINGLE
					   | DOUBLE
					   | EXTENDED
	                   | ''' 
	pass

def p_data_type_list(p):
	'''data_type_list  : INTEGER
                       | BYTE
					   | LONGINT
					   | SHORTINT
					   | WORD
                       | REAL
					   | SINGLE
					   | DOUBLE
					   | EXTENDED
					   | SHORT
					   | BOOLEAN
					   | CHAR
					   | STRING LPAREN NATURALNUMBER RPAREN''' 
	pass

def data_type_set(p):
	'''data_type_set   : BYTE
					   | SHORTINT
					   | WORD
					   | BOOLEAN
					   | CHAR''' 
	pass
