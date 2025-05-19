import ply.yacc as yacc
from src.tokens import tokens


symbol_table_stack = [{}]
current_scope_level = 0
semantic_errors = []


def check_writeln_args(arg_types, lineno):
    for i, arg_type in enumerate(arg_types):
        if not (
            is_numeric_type(arg_type)
            or is_string_type(arg_type)
            or is_char_type(arg_type)
            or is_boolean_type(arg_type)
        ):
            print_semantic_error(
                f"Argument {i+1} for 'writeln' has unprintable type {arg_type}.", lineno
            )
            return False
    return True


PREDEFINED_TYPES = {
    "integer": {"kind": "type", "type_def": ("PRIMITIVE", "INTEGER")},
    "real": {"kind": "type", "type_def": ("PRIMITIVE", "REAL")},
    "char": {"kind": "type", "type_def": ("PRIMITIVE", "CHAR")},
    "boolean": {"kind": "type", "type_def": ("PRIMITIVE", "BOOLEAN")},
    "string": {"kind": "type", "type_def": ("STRING_DEFAULT", 255)},
    "byte": {"kind": "type", "type_def": ("PRIMITIVE", "BYTE")},
    "shortint": {"kind": "type", "type_def": ("PRIMITIVE", "SHORTINT")},
    "word": {"kind": "type", "type_def": ("PRIMITIVE", "WORD")},
    "longint": {"kind": "type", "type_def": ("PRIMITIVE", "LONGINT")},
    "single": {"kind": "type", "type_def": ("PRIMITIVE", "SINGLE")},
    "double": {"kind": "type", "type_def": ("PRIMITIVE", "DOUBLE")},
    "extended": {"kind": "type", "type_def": ("PRIMITIVE", "EXTENDED")},
    "text": {"kind": "type", "type_def": ("file_type", ("PRIMITIVE", "CHAR"))},
}

PREDEFINED_CALLABLES = {
    "writeln": {
        "kind": "predefined_procedure",
        "params_check_func": lambda args, ln: True,
    },
    "readln": {
        "kind": "predefined_procedure",
        "params_check_func": lambda args, ln: True,
    },
    "ord": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "INTEGER"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_ordinal_type(args[0]),
    },
    "chr": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "CHAR"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_integer_type(args[0]),
    },
    "succ": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "INTEGER"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_integer_type(args[0]),
    },
    "pred": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "INTEGER"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_integer_type(args[0]),
    },
    "abs": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "INTEGER"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "sin": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "REAL"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "cos": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "REAL"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "tan": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "REAL"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "sqrt": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "REAL"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "ln": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "REAL"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "exp": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "REAL"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "trunc": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "INTEGER"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "round": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "INTEGER"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "random": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "REAL"),
        "params_check_func": lambda args, ln: len(args) == 0,
    },
    "randomize": {
        "kind": "predefined_procedure",
        "params_check_func": lambda args, ln: len(args) == 0,
    },
    "inttostr": {
        "kind": "predefined_function",
        "return_type": ("STRING_DEFAULT", 255),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_integer_type(args[0]),
    },
    "strtoint": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "INTEGER"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_string_type(args[0]),
    },
    "floattostr": {
        "kind": "predefined_function",
        "return_type": ("STRING_DEFAULT", 255),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_numeric_type(args[0]),
    },
    "strtofloat": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "REAL"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_string_type(args[0]),
    },
    "booltostr": {
        "kind": "predefined_function",
        "return_type": ("STRING_DEFAULT", 255),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_boolean_type(args[0]),
    },
    "strtobool": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "BOOLEAN"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_string_type(args[0]),
    },
    "chartostr": {
        "kind": "predefined_function",
        "return_type": ("STRING_DEFAULT", 255),
        "params_check_func": lambda args, ln: len(args) == 1 and is_char_type(args[0]),
    },
    "strtochar": {
        "kind": "predefined_function",
        "return_type": ("PRIMITIVE", "CHAR"),
        "params_check_func": lambda args, ln: len(args) == 1
        and is_string_type(args[0]),
    },
}


def print_semantic_error(message, lineno):
    error_msg = f"Semantic Error line {lineno}: {message}"
    print(error_msg)
    semantic_errors.append(error_msg)


def enter_scope(scope_name="<anonymous_scope>"):
    global current_scope_level
    current_scope_level += 1
    symbol_table_stack.append(
        {"__scope_name__": scope_name, "__level__": current_scope_level}
    )


def exit_scope():
    global current_scope_level
    if len(symbol_table_stack) > 1:

        symbol_table_stack.pop()
        current_scope_level -= 1
    else:
        print_semantic_error("Attempted to exit global scope.", 0)


def add_symbol(
    name,
    kind,
    type_desc,
    lineno,
    value=None,
    params=None,
    defined=True,
    is_forward_declaration_itself=False,
    target_scope_dict=None,
):
    """
    Añade o actualiza un símbolo en la tabla de símbolos.
    - name: Nombre del identificador.
    - kind: 'variable', 'constant', 'type', 'procedure', 'function', 'parameter', 'return_variable', etc.
    - type_desc: Descriptor del tipo del símbolo.
    - lineno: Número de línea de la declaración.
    - value: Valor (para constantes, o info adicional como modo de parámetro).
    - params: Lista de descriptores de parámetros (para procs/funcs).
    - defined: True si es una definición completa, False si solo es una declaración (como FORWARD incompleta).
    - is_forward_declaration_itself: True si ESTA llamada a add_symbol es para una declaración FORWARD.
    - target_scope_dict: El diccionario de scope específico donde añadir/actualizar. Si es None, usa el scope actual.

    Retorna True si la operación fue exitosa, False si hubo un error semántico (ej. redefinición).
    """
    name_lower = name.lower()

    scope_to_interact_with = (
        target_scope_dict if target_scope_dict is not None else symbol_table_stack[-1]
    )

    scope_level_of_target = current_scope_level
    if target_scope_dict:
        try:

            found_level = None
            for i in range(len(symbol_table_stack) - 1, -1, -1):
                if symbol_table_stack[i] is target_scope_dict:
                    found_level = symbol_table_stack[i].get(
                        "__level__",
                        current_scope_level - ((len(symbol_table_stack) - 1) - i),
                    )
                    break
            if found_level is not None:
                scope_level_of_target = found_level

        except Exception:
            pass

    if name_lower in scope_to_interact_with:
        existing_entry = scope_to_interact_with[name_lower]

        if existing_entry.get("is_forward"):

            if is_forward_declaration_itself:
                print_semantic_error(
                    f"'{name}' re-declared as FORWARD at line {lineno} (previous FORWARD at line {existing_entry['lineno']}).",
                    lineno,
                )
                return False

            else:

                if existing_entry["kind"] != kind:
                    print_semantic_error(
                        f"Cannot change kind of '{name}' from '{existing_entry['kind']}' (FORWARD) to '{kind}' at line {lineno}.",
                        lineno,
                    )
                    return False

                if existing_entry["kind"] in ["procedure", "function"]:
                    if len(existing_entry.get("params", [])) != len(
                        params if params else []
                    ):
                        print_semantic_error(
                            f"Parameter count mismatch for '{name}' at line {lineno}. Expected {len(existing_entry.get('params', []))}, got {len(params if params else [])}.",
                            lineno,
                        )
                        return False

                    if existing_entry["kind"] == "function":

                        expected_return_type = (
                            existing_entry["type"][2]
                            if len(existing_entry["type"]) > 2
                            else None
                        )
                        current_return_type = (
                            type_desc[2] if len(type_desc) > 2 else None
                        )
                        if not are_types_compatible(
                            expected_return_type, current_return_type
                        ):
                            print_semantic_error(
                                f"Return type mismatch for function '{name}' at line {lineno}. Expected '{expected_return_type}', got '{current_return_type}'.",
                                lineno,
                            )
                            return False

                existing_entry["defined"] = True
                existing_entry["is_forward"] = False
                existing_entry["type"] = type_desc
                existing_entry["params"] = (
                    params if params else existing_entry.get("params", [])
                )
                existing_entry["lineno_defined"] = lineno

                return True

        else:

            if (
                existing_entry["kind"] == "return_variable"
                and kind == "return_variable"
            ):

                pass
            else:
                print_semantic_error(
                    f"Identifier '{name}' redefined at line {lineno} (originally declared at line {existing_entry['lineno']}).",
                    lineno,
                )
                return False

    else:
        scope_to_interact_with[name_lower] = {
            "id": name,
            "kind": kind,
            "type": type_desc,
            "value": value,
            "params": params if params else [],
            "defined": defined,
            "is_forward": is_forward_declaration_itself,
            "lineno": lineno,
            "scope_level": scope_level_of_target,
            "lineno_defined": (
                lineno if defined and not is_forward_declaration_itself else None
            ),
        }

        return True

    return False


def update_forward_declaration(name, params, return_type, lineno):
    name_lower = name.lower()

    for scope in reversed(symbol_table_stack):
        if name_lower in scope and scope[name_lower].get("is_forward"):
            entry = scope[name_lower]

            entry["defined"] = True
            entry["is_forward"] = False
            entry["lineno_defined"] = lineno

            return True
    print_semantic_error(f"No matching forward declaration found for '{name}'.", lineno)
    return False


def lookup_symbol(name, lineno, current_scope_only=False):
    name_lower = name.lower()

    if current_scope_only:
        if name_lower in symbol_table_stack[-1]:
            return symbol_table_stack[-1][name_lower]
    else:
        for i in range(len(symbol_table_stack) - 1, -1, -1):
            scope = symbol_table_stack[i]
            if name_lower in scope:

                return scope[name_lower]

    if name_lower in PREDEFINED_TYPES:

        return {
            "id": name_lower,
            "kind": "type",
            "type": PREDEFINED_TYPES[name_lower]["type_def"],
            "defined": True,
            "lineno": 0,
            "scope_level": -1,
        }

    if name_lower in PREDEFINED_CALLABLES:
        return {
            "id": name_lower,
            "kind": PREDEFINED_CALLABLES[name_lower]["kind"],
            "type": PREDEFINED_CALLABLES[name_lower].get("return_type"),
            "params_check_func": PREDEFINED_CALLABLES[name_lower].get(
                "params_check_func"
            ),
            "params": PREDEFINED_CALLABLES[name_lower].get("params"),
            "defined": True,
            "lineno": 0,
            "scope_level": -1,
        }

    print_semantic_error(f"Identifier '{name}' not declared.", lineno)
    return None


def get_type_descriptor(type_name_or_def, lineno):
    """
    Obtiene el descriptor de tipo.
    Si type_name_or_def es un string, lo busca como un nombre de tipo.
    Si es una tupla/lista, se asume que ya es un descriptor de tipo.
    """
    if isinstance(type_name_or_def, str):
        type_symbol = lookup_symbol(type_name_or_def, lineno)
        if type_symbol and (
            type_symbol["kind"] == "type" or type_symbol.get("is_type_alias")
        ):
            return type_symbol["type"]
        elif type_name_or_def.lower() in PREDEFINED_TYPES:
            return PREDEFINED_TYPES[type_name_or_def.lower()]["type_def"]
        else:
            print_semantic_error(f"Type '{type_name_or_def}' not defined.", lineno)
            return ("ERROR_TYPE", f"Undefined type: {type_name_or_def}")
    elif isinstance(type_name_or_def, (tuple, list)):
        return type_name_or_def
    else:
        print_semantic_error(f"Invalid type specification: {type_name_or_def}.", lineno)
        return ("ERROR_TYPE", f"Invalid type spec: {type_name_or_def}")


def is_ordinal_type(type_desc):
    if not isinstance(type_desc, tuple):
        return False

    return (
        type_desc[0] == "PRIMITIVE"
        and type_desc[1] in ["INTEGER", "CHAR", "BOOLEAN", "BYTE", "SHORTINT", "WORD"]
        or type_desc[0] in ["ENUMERATED_TYPE", "SUBRANGE_TYPE"]
    )


def are_types_compatible(type1_desc, type2_desc, context="assignment"):
    if (
        type1_desc is None
        or type2_desc is None
        or type1_desc[0] == "ERROR_TYPE"
        or type2_desc[0] == "ERROR_TYPE"
    ):
        return False

    if type1_desc == type2_desc:
        return True

    if context == "assignment":

        if is_real_type(type1_desc) and is_integer_type(type2_desc):
            return True

        if (type1_desc[0] in ["STRING_DEFAULT", "STRING_FIXED"]) and is_char_type(
            type2_desc
        ):

            if type1_desc[0] == "STRING_FIXED" and type1_desc[1] < 1:
                return False
            return True

        if is_char_type(type1_desc) and is_string_type(type2_desc):
            if type2_desc[0] == "STRING_LITERAL" and type2_desc[1] == 1:
                return True

            return False

        if is_string_type(type1_desc) and is_string_type(type2_desc):

            if type1_desc[0] == "STRING_DEFAULT":

                return True

            elif type1_desc[0] == "STRING_FIXED":
                dest_len = type1_desc[1]

                if type2_desc[0] == "STRING_DEFAULT":

                    return True

                elif (
                    type2_desc[0] == "STRING_FIXED" or type2_desc[0] == "STRING_LITERAL"
                ):
                    src_len = type2_desc[1]

                    if type2_desc[0] == "STRING_LITERAL" and src_len > dest_len:
                        return False

                    return True

        if type1_desc[0] == "SUBRANGE_TYPE" and type1_desc[1] == type2_desc:
            return True
        if type2_desc[0] == "SUBRANGE_TYPE" and type2_desc[1] == type1_desc:
            return True

        if (
            type1_desc[0] == "SUBRANGE_TYPE"
            and type2_desc[0] == "SUBRANGE_TYPE"
            and type1_desc[1] == type2_desc[1]
        ):
            return True

        if is_pointer_type(type1_desc) and is_pointer_type(type2_desc):
            if type2_desc == ("POINTER", "NIL"):
                return True
            if type1_desc[1] == type2_desc[1]:
                return True

        if is_set_type(type1_desc) and is_set_type(type2_desc):

            if are_ordinal_types_compatible_for_set(type1_desc[1], type2_desc[1]):
                return True

        return False

    elif context == "comparison":

        if (is_string_type(type1_desc) or is_char_type(type1_desc)) and (
            is_string_type(type2_desc) or is_char_type(type2_desc)
        ):
            return True

        if is_numeric_type(type1_desc) and is_numeric_type(type2_desc):
            return True

        if is_boolean_type(type1_desc) and is_boolean_type(type2_desc):
            return True

        if is_pointer_type(type1_desc) and is_pointer_type(type2_desc):
            if type2_desc == ("POINTER", "NIL") or type1_desc == ("POINTER", "NIL"):
                return True
            if type1_desc[1] == type2_desc[1]:
                return True

        if is_set_type(type1_desc) and is_set_type(type2_desc):
            if are_ordinal_types_compatible_for_set(type1_desc[1], type2_desc[1]):
                return True

        return False

    return False


def is_array_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 2:
        return False
    return (
        type_desc[0] == "array_type"
        and len(type_desc) >= 2
        and (type_desc[1] == "array" or type_desc[1] == "array_of")
    )


def is_record_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 1:
        return False
    return (
        type_desc[0] == "record_type"
        and len(type_desc) >= 2
        and (type_desc[1] == "record" or type_desc[1] == "record_of")
    )


def is_file_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 1:
        return False
    return (
        type_desc[0] == "file_type"
        and len(type_desc) >= 2
        and (type_desc[1] == "file" or type_desc[1] == "file_of")
    )


def is_date_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 1:
        return False
    return type_desc[0] == "PRIMITIVE" and type_desc[1] == "DATE"


def is_time_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 1:
        return False
    return type_desc[0] == "PRIMITIVE" and type_desc[1] == "TIME"


def is_numeric_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 2:
        return False

    if type_desc[0] == "PRIMITIVE" and type_desc[1] in [
        "INTEGER",
        "REAL",
        "BYTE",
        "SHORTINT",
        "WORD",
        "LONGINT",
        "SINGLE",
        "DOUBLE",
        "EXTENDED",
    ]:
        return True
    if type_desc[0] == "SUBRANGE_TYPE" and is_numeric_type(type_desc[1]):
        return True
    return False


def is_datetime_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 1:
        return False
    return type_desc[0] == "PRIMITIVE" and type_desc[1] == "DATETIME"


def is_integer_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 2:
        return False
    if type_desc[0] == "PRIMITIVE" and type_desc[1] in [
        "INTEGER",
        "BYTE",
        "SHORTINT",
        "WORD",
        "LONGINT",
    ]:
        return True
    if type_desc[0] == "SUBRANGE_TYPE" and is_integer_type(type_desc[1]):
        return True
    if type_desc[0] == "ENUMERATED_TYPE":
        return True
    if type_desc[0] == "SUBRANGE_TYPE" and type_desc[1] == ("PRIMITIVE", "INTEGER"):
        return True
    if type_desc[0] == "SUBRANGE_TYPE" and type_desc[1] == ("PRIMITIVE", "BYTE"):
        return True
    return False


def is_real_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 2:
        return False
    if type_desc[0] == "PRIMITIVE" and type_desc[1] in [
        "REAL",
        "SINGLE",
        "DOUBLE",
        "EXTENDED",
    ]:
        return True
    return False


def is_string_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 1:
        return False
    return type_desc[0] in [
        "STRING_DEFAULT",
        "STRING_FIXED",
        "STRING_LITERAL",
        ("PRIMITIVE", "CHAR"),
    ]


def is_char_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 2:
        return False
    return type_desc == ("PRIMITIVE", "CHAR") or (
        type_desc[0] == "SUBRANGE_TYPE" and type_desc[1] == ("PRIMITIVE", "CHAR")
    )


def is_boolean_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 2:
        return False
    return type_desc == ("PRIMITIVE", "BOOLEAN") or (
        type_desc[0] == "SUBRANGE_TYPE" and type_desc[1] == ("PRIMITIVE", "BOOLEAN")
    )


def is_pointer_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 1:
        return False
    return type_desc[0] == "POINTER"


def is_set_type(type_desc):
    if not isinstance(type_desc, tuple) or len(type_desc) < 1:
        return False
    return type_desc[0] == "set_type"


def are_ordinal_types_compatible_for_set(base1_desc, base2_desc):

    def get_ultimate_base_ordinal(desc):
        if desc[0] == "SUBRANGE_TYPE":
            return get_ultimate_base_ordinal(desc[1])
        if desc[0] == "PRIMITIVE" and desc[1] in [
            "INTEGER",
            "CHAR",
            "BOOLEAN",
            "BYTE",
            "SHORTINT",
            "WORD",
        ]:
            return desc
        if desc[0] == "ENUMERATED_TYPE":
            return desc
        return None

    ub1 = get_ultimate_base_ordinal(base1_desc)
    ub2 = get_ultimate_base_ordinal(base2_desc)

    return ub1 is not None and ub1 == ub2


def get_result_type(operator, type1_desc, type2_desc=None, lineno=0):
    """
    Determina el tipo resultante de una operación.
    Para operadores unarios, type2_desc es None.
    """
    op = operator.upper()

    if (
        type1_desc is None
        or type1_desc[0] == "ERROR_TYPE"
        or (type2_desc is not None and type2_desc[0] == "ERROR_TYPE")
    ):
        return ("ERROR_TYPE", f"Operand type error for operator {op}")

    if type2_desc is None:
        if op == "NOT":
            if is_boolean_type(type1_desc):
                return ("PRIMITIVE", "BOOLEAN")
            else:
                print_semantic_error(
                    f"Operator 'NOT' requires a BOOLEAN operand, got {type1_desc}.",
                    lineno,
                )
        elif op == "-":
            if is_numeric_type(type1_desc):
                return type1_desc
            else:
                print_semantic_error(
                    f"Unary '-' requires a numeric operand, got {type1_desc}.", lineno
                )
        elif op == "+":
            if is_numeric_type(type1_desc):
                return type1_desc
            else:
                print_semantic_error(
                    f"Unary '+' requires a numeric operand, got {type1_desc}.", lineno
                )
        elif op == "@":

            return ("POINTER", type1_desc)
        else:
            print_semantic_error(f"Unknown unary operator '{op}'.", lineno)
        return ("ERROR_TYPE", f"Unary op error {op}")

    if op in ["+", "-", "*"]:
        if is_real_type(type1_desc) or is_real_type(type2_desc):
            if is_numeric_type(type1_desc) and is_numeric_type(type2_desc):
                return ("PRIMITIVE", "REAL")
        elif is_integer_type(type1_desc) and is_integer_type(type2_desc):

            return ("PRIMITIVE", "INTEGER")

        elif (
            op == "+"
            and (is_string_type(type1_desc) or is_char_type(type1_desc))
            and (is_string_type(type2_desc) or is_char_type(type2_desc))
        ):

            return ("STRING_DEFAULT", 255)

        elif (
            op == "+"
            and is_set_type(type1_desc)
            and is_set_type(type2_desc)
            and are_ordinal_types_compatible_for_set(type1_desc[1], type2_desc[1])
        ):
            return type1_desc
        else:
            print_semantic_error(
                f"Operator '{op}' requires numeric, string, or compatible set operands. Got {type1_desc} and {type2_desc}.",
                lineno,
            )

    elif op == "/":
        if is_numeric_type(type1_desc) and is_numeric_type(type2_desc):
            return ("PRIMITIVE", "REAL")
        else:
            print_semantic_error(
                f"Operator '/' requires numeric operands. Got {type1_desc} and {type2_desc}.",
                lineno,
            )
    elif op in ["DIV", "MOD"]:
        if is_integer_type(type1_desc) and is_integer_type(type2_desc):
            return ("PRIMITIVE", "INTEGER")
        else:
            print_semantic_error(
                f"Operators 'DIV', 'MOD' require INTEGER operands. Got {type1_desc} and {type2_desc}.",
                lineno,
            )

    elif op in ["AND", "OR", "XOR"]:
        if is_boolean_type(type1_desc) and is_boolean_type(type2_desc):
            return ("PRIMITIVE", "BOOLEAN")

        else:
            print_semantic_error(
                f"Operator '{op}' requires BOOLEAN operands. Got {type1_desc} and {type2_desc}.",
                lineno,
            )

    elif op in ["=", "<>", "<", "<=", ">", ">="]:
        if are_types_compatible(type1_desc, type2_desc, context="comparison"):
            return ("PRIMITIVE", "BOOLEAN")
        else:
            print_semantic_error(
                f"Cannot compare {type1_desc} and {type2_desc} with operator '{op}'.",
                lineno,
            )

    elif op == "IN":

        if is_set_type(type2_desc):
            base_type_of_set = type2_desc[1]

            if is_ordinal_type(type1_desc) and are_ordinal_types_compatible_for_set(
                type1_desc, base_type_of_set
            ):
                return ("PRIMITIVE", "BOOLEAN")
            else:
                print_semantic_error(
                    f"Element type {type1_desc} is not compatible with set base type {base_type_of_set} for 'IN' operator.",
                    lineno,
                )
        else:
            print_semantic_error(
                f"Operator 'IN' requires a SET as its right operand, got {type2_desc}.",
                lineno,
            )

    elif op in ["*", "-"] and is_set_type(type1_desc) and is_set_type(type2_desc):
        if are_ordinal_types_compatible_for_set(type1_desc[1], type2_desc[1]):
            return type1_desc
        else:
            print_semantic_error(
                f"Set operands for '{op}' must have compatible base types. Got {type1_desc[1]} and {type2_desc[1]}.",
                lineno,
            )

    elif op in ["SHL", "SHR"]:
        if is_integer_type(type1_desc) and is_integer_type(type2_desc):
            return type1_desc
        else:
            print_semantic_error(
                f"Operators 'SHL', 'SHR' require INTEGER operands. Got {type1_desc} and {type2_desc}.",
                lineno,
            )

    else:
        print_semantic_error(
            f"Unknown or unsupported binary operator '{op}' for types {type1_desc} and {type2_desc}.",
            lineno,
        )

    return (
        "ERROR_TYPE",
        f"Op ({op}) type resolution failed for {type1_desc}, {type2_desc}",
    )
