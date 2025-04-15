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
    'type : TYPE type_list'
    pass

def p_type_list(p):
    '''type_list : type_list type_declaration
                 | type_declaration'''
    pass

def p_type_declaration(p):
    'type_declaration : ID EQUAL type_definition SEMICOLON'
    pass

def p_type_definition(p):
    '''type_definition : data_type_list
                       | LPAREN id_list RPAREN
                       | INTEGERNUMBER DOBLEDOT INTEGERNUMBER
                       | CHAR DOBLEDOT CHAR
                       | RECORD record_list END
                       | ARRAY LBRACKET INTEGERNUMBER DOBLEDOT INTEGERNUMBER RBRACKET OF data_type_list
                       | SET OF set_range
                       | CARET ID'''
    pass

def p_set_range(p):
    '''set_range : data_type_set
                 | INTEGERNUMBER DOBLEDOT INTEGERNUMBER
                 | CHAR DOBLEDOT CHAR'''
    pass

def p_record_list(p):
    '''record_list : record_list record_declaration
                   | record_declaration'''
    pass

def p_record_declaration(p):
    'record_declaration : id_list COLON data_type_list SEMICOLON'
    pass



# Definición de cómo se usa var

def p_var(p):
    'var : VAR var_list'
    pass

def p_var_list(p):
    '''var_list : var_list var_declaration
                | var_declaration'''
    pass

def p_var_declaration(p):
    'var_declaration : id_list COLON data_type_list SEMICOLON'
    pass

def p_id_list(p):
    '''id_list : ID
               | id_list COMMA ID'''
    pass


# definción de cómo se usa begin FALTA ESTO 

def p_begin(p):
	'begin : BEGIN sentences_list END DOT' 
	pass


# definición de cómo se usa for

def p_for(p):
    'for: FOR ID ASIGNATION INTEGERNUMBER TO INTEGERNUMBER DO'

# definición de cómo se usa while

# definición de cómo se usa if 



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
