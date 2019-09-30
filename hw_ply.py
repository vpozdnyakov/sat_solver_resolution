tokens = (
    'VAR', 
    'CONJUNCTION', 'DISJUNCTION', 'IMPLICATION', 'NEGATION',
    'LPAREN','RPAREN',
)

# Tokens
t_VAR = r'[a-z]'
t_CONJUNCTION = r'/\\'
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
        self.negation = False
    
    def printable(self):
        return "~" + self.value if self.negation else self.value

class Clause:
    def __init__(self, unit1, unit2):
        self.units = [unit1, unit2]
        self.tautology = False
        self.satisfiable = True
        if unit1.value == unit2.value:
            if unit1.negation != unit2.negation:
                self.tautology = True
            elif unit1.value is None:
                self.satisfiable = False
            else:
                self.units[0] = Unit(None)
    
    def printable(self):
        return r'({}\/{})'.format(self.units[0].printable(), 
                                  self.units[1].printable())

class Expression:
    def __init__(self, clauses):
        self.clauses = clauses
        self.satisfiable = None
    
    def print(self):
        print('Resolution:', self.printable())
        print('Satisfiable:', self.satisfiable)
    
    def printable(self):
        printable_clauses = []
        for clause in self.clauses:
            printable_clauses.append(clause.printable())
        return '/\\'.join(printable_clauses)

    def reduce_tautology(self):
        n = len(self.clauses)
        for i in range(n):
            clause = self.clauses[n-i-1]
            if clause.tautology: self.clauses.remove(clause)
    
    def is_dublicate(self, new_clause):
        for clause in self.clauses:
            indicator = 0
            for i in range(2):
                for j in range(2):
                    if (new_clause.units[i].value == clause.units[j].value
                            and new_clause.units[i].negation == clause.units[j].negation):
                        indicator += 1
            if indicator == 2:
                return True
        return False
    
    def apply_resolution(self):
        self.satisfiable = True
        while True:
            len_clauses = len(self.clauses)
            clauses = list(self.clauses)
            for clause_i in clauses:
                for clause_j in clauses:
                    if clause_i == clause_j: continue
                    for i in range(2):
                        for j in range(2):
                            i_value = clause_i.units[i].value
                            j_value = clause_j.units[j].value
                            i_neg = clause_i.units[i].negation
                            j_neg = clause_j.units[j].negation
                            if (i_value == j_value and i_neg != j_neg):
                                new_clause = Clause(clause_i.units[i^1], 
                                                    clause_j.units[j^1])
                                if not new_clause.satisfiable:
                                    self.clauses.append(new_clause)
                                    self.satisfiable = False
                                    return
                                if (not new_clause.tautology 
                                        and not self.is_dublicate(new_clause)):
                                    self.clauses.append(new_clause)
            if len_clauses == len(self.clauses): 
                return

# Grammar
def p_expression_conjunction(p):
    'expression : expression CONJUNCTION expression'
    p[0] = Expression(p[1].clauses + p[3].clauses)

def p_expression_paren(p):
    'expression : LPAREN clause RPAREN'
    p[0] = Expression([p[2]])

def p_clause_implication(p):
    'clause : unit IMPLICATION unit'
    p[1].negation = not p[1].negation
    p[0] = Clause(p[1], p[3])

def p_clause_disjunction(p):
    'clause : unit DISJUNCTION unit'
    p[0] = Clause(p[1], p[3])

def p_unit_negation(p):
    'unit : NEGATION unit'
    p[0] = p[2]
    p[0].negation = True

def p_unit_var(p):
    'unit : VAR'
    p[0] = Unit(p[1])

def p_error(p):
    print("Syntax error at '%s'" % p.value)

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()

# example: (p -> q) /\ (~r \/ s) /\ (~q -> p)
# example: (a\/~b)/\(b\/c)/\(~a\/c)/\(e\/~d)/\(d\/~c)/\(~e\/~c)

while True:
    try:
        input_str = input('input > ')
    except EOFError:
        break
    if not input_str: continue
    result = parser.parse(input_str)
    if result is not None:
        result.reduce_tautology()
        result.apply_resolution()
        result.print()
