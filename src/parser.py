def p_program(p):
	'program : program ID ;'
	pass

def p_uses(p):
	'uses : USES ID id_list SEMICOLON' 
	pass

def p_id_list(p):
	'''id_list : COMMA ID 
	             | '''
	pass

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
						| ID EQUAL ARRAY SEMICOLON
						| SEMICOLON'''
	pass

def p_record_list(p):
	'''record_list : record_list record_declaration | record_declaration'''
	
def p_record_declaration(p):
	'ID COLON data_type_list'


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

def data_type_list(p):
	'''var_declaration : INTEGER
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
