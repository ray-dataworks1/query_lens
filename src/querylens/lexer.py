import ply.lex as lex

# 1. Define Token types (must be defined first to avoid errors)
tokens = (
    'SELECT', 'FROM', 'WHERE',  # Keywords
    'ID', 'INT', 'STRING',      # Identifiers and literals
    'EQ', 'GT', 'LT',           # Operators (equality, greater than, less than)
    'COMMA', 'STAR'             # Punctuation (comma, asterisk)
)

# 2. Define matching rules for keywords (higher priority than identifiers, as keywords also consist of letters)
reserved = {
    'select': 'SELECT',
    'from': 'FROM',
    'where': 'WHERE'
}

# 3. Define regular expressions for Tokens (ordered by priority from highest to lowest)
# String literals: enclosed in single quotes, e.g., 'Alice'
def t_STRING(t):
    r"'[^']*'"  # Regex: match any character (excluding single quotes) inside single quotes
    t.value = t.value[1:-1]  # Remove the single quotes to retain the actual content
    return t

# Integer literals: sequences of digits
def t_INT(t):
    r'\d+'
    t.value = int(t.value)  # Convert to integer type
    return t

# Identifiers (table names, column names): start with a letter, followed by letters/digits/underscores
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Check if the identifier is a keyword (e.g., 'select' should be recognized as SELECT, not ID)
    t.type = reserved.get(t.value.lower(), 'ID')
    return t

# Operators
t_EQ = r'='    # Equality
t_GT = r'>'    # Greater than
t_LT = r'<'    # Less than

# Punctuation
t_COMMA = r',' # Comma
t_STAR = r'\*' # Asterisk (needs escaping because * has a special meaning in regex)

# 4. Ignore irrelevant characters (spaces, tabs, newlines)
t_ignore = ' \t\n'

# 5. Error handling (triggered when unrecognizable characters are encountered)
def t_error(t):
    print(f"Unsupported character: '{t.value[0]}'")
    t.lexer.skip(1)  # Skip the invalid character and continue parsing subsequent content

# 6. Create a Lexer instance
lexer = lex.lex()

# Function to tokenise a SQL string
def tokenise(sql):
    """Tokenise a SQL string and return a list of tokens."""
    lexer.input(sql)
    return list(iter(lexer.token, None))

