import ply.lex as lex

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
lexer = lex.lex()

# Test it out
data = r'(p -> q) /\(~r \/ s) /\ (~q -> p)'

# Give the lexer some input
lexer.input(data)

# Tokenize
for tok in lexer:
    print(tok)