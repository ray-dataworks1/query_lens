"""
syntaxer.py
------------
This module defines the *syntactic analyser* (parser) for v.0.1 of the SQL parser project.
It takes a list of tokens from the lexer and organizes them into a structured
Abstract Syntax Tree (AST) based on defined grammar rules.
"""

import ply.yacc as yacc
from querylens.lexer import tokens  # ← import your token definitions from the lexer


# 1. AST NODE CREATION HELPER


def create_ast(node_type, **kwargs):
    """
    Helper function that builds a dictionary-style AST node.
    Every rule in the parser will call this to keep structure consistent.
    Example:
        create_ast('FromClause', table='users')
        → {'type': 'FromClause', 'table': 'users'}
    """
    return {'type': node_type, **kwargs}


# 2. GRAMMAR RULES


# Starting rule: defines what a full query looks like.
# A query always has: SELECT clause + FROM clause + optional WHERE clause.
def p_query(p):
    '''query : select_clause from_clause where_clause_opt'''
    # p[0] is the "result" of this rule (the combined AST node)
    # p[1], p[2], p[3] represent the results of the subrules matched
    p[0] = create_ast(
        'Query',
        select=p[1],
        from_clause=p[2],
        where_clause=p[3] if p[3] else None
    )


# Optional WHERE clause — it can either appear or not.
def p_where_clause_opt(p):
    '''where_clause_opt : WHERE condition
                        | empty'''
    # If WHERE clause exists → use its condition AST.
    if len(p) == 3:
        p[0] = p[2]
    else:
        # If not present, return None.
        p[0] = None


# SELECT clause — handles both "SELECT *" and "SELECT col1, col2".
def p_select_clause(p):
    '''select_clause : SELECT STAR
                     | SELECT column_list'''
    # If * was used, columns list = ['*']
    if p[2] == '*':
        p[0] = create_ast('SelectClause', columns=['*'])
    else:
        # Otherwise store parsed list of columns.
        p[0] = create_ast('SelectClause', columns=p[2])


# Column list rule — recursive definition:
#  "column_list → ID" or "column_list → column_list , ID"
def p_column_list(p):
    '''column_list : ID
                   | column_list COMMA ID'''
    # If only one column name
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        # Combine existing list + new column name
        p[0] = p[1] + [p[3]]


# FROM clause — always of the form "FROM table_name"
def p_from_clause(p):
    '''from_clause : FROM ID'''
    p[0] = create_ast('FromClause', table=p[2])


# WHERE condition — defines valid expressions in WHERE.
# e.g., "age > 18" or "name = 'Alice'"
def p_condition(p):
    '''condition : ID EQ INT
                 | ID EQ STRING
                 | ID GT INT
                 | ID LT INT'''
    p[0] = create_ast(
        'Condition',
        column=p[1],
        operator=p[2],
        value=p[3]
    )


# Empty rule (for optional clauses like WHERE).
def p_empty(p):
    '''empty :'''
    p[0] = None



# 3. ERROR HANDLING


def p_error(p):
    """
    Handles unexpected or invalid syntax.
    Called automatically if the parser encounters something
    that doesn't fit any of the grammar rules.
    """
    if p:
        print(f"Syntax error near token: {p.type} (Value: {p.value})")
    else:
        print("Syntax error: Unexpected end of input")



# 4. BUILD PARSER INSTANCE


# This compiles the grammar and returns a parser object.
parser = yacc.yacc()



# 5. PUBLIC FUNCTION (CLEAN ENTRY POINT)


def parse_sql(sql: str):
    """
    Parses an input SQL string and returns its AST.
    Example:
        parse_sql("SELECT id FROM users WHERE age > 18")
    """
    return parser.parse(sql)
