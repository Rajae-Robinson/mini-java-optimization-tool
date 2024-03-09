import re

# Define token types
TOKEN_TYPES = {
    'KEYWORD': r'(class|public|static|void|String|int|boolean|true|false|if|else|while|return|new|this|System\.out\.println)',
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z0-9_]*',
    'INTEGER_LITERAL': r'\d+',
    'SYMBOL': r'[{}()\[\];=+\-*/,.]',
    'COMMENT': r'\/\/.*|\/\*(.|\n)*?\*\/',
    'WHITESPACE': r'\s+'
}

# Combine token types into a single regex pattern
TOKEN_REGEX = '|'.join(f'(?P<{token_type}>{pattern})' for token_type, pattern in TOKEN_TYPES.items())
TOKEN_REGEX = re.compile(TOKEN_REGEX)

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f'Token({self.type}, {self.value})'

# Lexer class
class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = self.tokenize()

    def tokenize(self):
        tokens = []
        for match in TOKEN_REGEX.finditer(self.code):
            for name, value in match.groupdict().items():
                if value and name != 'WHITESPACE':
                    tokens.append(Token(name, value))
                    break
        return tokens
