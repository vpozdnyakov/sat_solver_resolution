tokens = (
    'VAR', 
    'CONJUCTION', 'DISJUNCTION', 'IMPLICATION', 'NEGATION',
    'LPAREN','RPAREN',
)

# Tokens
t_VAR = r'[a-z]'
t_CONJUCTION = r'/\\'
t_DISJUNCTION = r'\\/'
t_IMPLICATION = r'->'
t_NEGATION = r'~'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# Ignored characters
t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

class Unit:
    def __init__(self, value):
        self.value = value

class Clause:
    def __init__(self, unit1, operation, unit2):
        self.units = [unit1, unit2]
        self.operation = operation

class Expression:
    def __init__(self, clauses):
        self.clauses = clauses
    def print(self):
        out_clauses = []
        for clause in self.clauses:
            out_clauses.append('({}{}{})'.format(
                clause.units[0].value, 
                clause.operation, 
                clause.units[1].value))
        print('/\\'.join(out_clauses))


def p_expression_conjuction(p):
    'expression : expression CONJUCTION expression'
    p[0] = Expression(p[1].clauses + p[3].clauses)

def p_expression_paren(p):
    'expression : LPAREN clause RPAREN'
    p[0] = Expression([p[2]])

def p_clause_implication(p):
    'clause : unit IMPLICATION unit'
    p[0] = Clause(p[1], '->', p[3])

def p_clause_disjunction(p):
    'clause : unit DISJUNCTION unit'
    p[0] = Clause(p[1], r'\/', p[3])

def p_unit_negation(t):
    'unit : NEGATION unit'
    t[0] = Unit('~' + t[2].value)

def p_unit_var(t):
    'unit : VAR'
    t[0] = Unit(t[1])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()

# sample = r'(p -> q) /\(~r \/ s) /\ (~q -> p)'
while True:
    try:
        s = input('input > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    result.print()
