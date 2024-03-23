class MiniJavaParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def parse(self):
        return self.program()

    def program(self):
        class_declarations = []
        while self.current_token_index < len(self.tokens):
            class_declarations.append(self.class_declaration())
        return class_declarations

    def consume(self, token_type):
        token = self.tokens[self.current_token_index]
        if token.type == token_type:
            self.current_token_index += 1
            return token
        else:
            raise SyntaxError(f"Expected token type '{token_type}', found '{token.type} {token.value}'")

    def match(self, token_type):
        token = self.tokens[self.current_token_index]
        return token.type == token_type

    def class_declaration(self):
        self.consume('KEYWORD')  # class
        class_name = self.consume('IDENTIFIER').value
        start_class_block = self.consume('SYMBOL').value  # {
        if(start_class_block != '{'):
            raise SyntaxError("Expected '{' at the beginning of class definition")
        
        # Parse class body
        methods = []
        fields = []
        while not self.match('SYMBOL'):
            if self.match('KEYWORD'):  # MethodDeclaration
                if self.tokens[self.current_token_index].value == 'public' and \
                self.tokens[self.current_token_index + 1].value == 'static' and \
                self.tokens[self.current_token_index + 2].value == 'void' and \
                self.tokens[self.current_token_index + 3].value == 'main':
                    methods.append(self.main_method())
                else:
                    methods.append(self.method_declaration())
            else:  # FieldDeclaration
                fields.append(self.variable_declaration())
        self.consume('SYMBOL')  # }
        return {'class_name': class_name, 'methods': methods, 'fields': fields}

    def main_method(self):
        self.consume('KEYWORD').value  # public
        self.consume('KEYWORD')  # static
        self.consume('KEYWORD')  # void
        method_name = self.consume('IDENTIFIER').value  # main
        self.consume('SYMBOL')  # (
        self.consume('KEYWORD')  # String
        self.consume('SYMBOL')  # [
        self.consume('SYMBOL')  # ]
        parameter = self.consume('IDENTIFIER').value  # args
        self.consume('SYMBOL')  # )
        self.consume('SYMBOL')  # {
        # Parse method body
        statements = []
        while self.tokens[self.current_token_index].value != '}':
            statements.append(self.statement())
        self.consume('SYMBOL')  # }
        return {'name': method_name, 'return_type': 'void', 'parameters': [parameter], 'statements': statements}

    def method_declaration(self):
        self.consume('KEYWORD').value  # public
        return_type = self.consume('KEYWORD').value  # Type
        method_name = self.consume('IDENTIFIER').value
        start_param = self.consume('SYMBOL').value  # (
        
        if(start_param != '('):
            raise SyntaxError("Expected '('")

        # Parse parameters
        parameters = []
        while not self.match('SYMBOL'):
            parameter_type = self.consume('KEYWORD').value  # Type
            parameter_name = self.consume('IDENTIFIER').value
            parameters.append({'type': parameter_type, 'name': parameter_name})
            if self.match('SYMBOL'):
                break
            self.consume('SYMBOL')  # ,
        self.consume('SYMBOL')  # )
        start_method_block = self.consume('SYMBOL').value  # {
       
       # Parse method body
        statements = []

        if(start_method_block != '{'):
            raise SyntaxError("Expected '{'")
        
        while not self.match('SYMBOL'):
            statements.append(self.statement())
        self.consume('SYMBOL')  # }
        return {'name': method_name, 'return_type': return_type, 'parameters': parameters, 'statements': statements}

    def statement(self):
        if self.match('KEYWORD'):  # VariableDeclaration or Assignment or PrintStatement or IfStatement or WhileStatement or ReturnStatement
            keyword = self.tokens[self.current_token_index].value
            if keyword == 'int' or keyword == 'boolean':
                return self.variable_declaration()
            elif keyword == 'System.out.println':
                return self.print_statement()
            elif keyword == 'if':
                return self.if_statement()
            elif keyword == 'while':
                return self.while_statement()
            elif keyword == 'return':
                return self.return_statement()
        elif self.match('IDENTIFIER'):
            return self.assignment()
        elif self.match('SYMBOL'):
            return self.block()

    def variable_declaration(self):
        var_type = self.consume('KEYWORD').value  # Type
        var_name = self.consume('IDENTIFIER').value
        expression = None
        if self.tokens[self.current_token_index].value == '=':  # Check for initialization
            self.consume('SYMBOL')  # =
            # Parse initialization expression
            expression = self.expression()
        self.consume('SYMBOL')  # ;
        return {'type': 'VariableDeclaration', 'var_type': var_type, 'name': var_name, 'expression': expression}

    def assignment(self):
        var_name = self.consume('IDENTIFIER').value
        self.consume('SYMBOL')  # =
        # Parse assignment expression
        expression = self.expression()
        self.consume('SYMBOL')  # ;
        return {'type': 'Assignment', 'var_name': var_name, 'expression': expression}

    def print_statement(self):
        self.consume('KEYWORD')  # System.out.println
        self.consume('SYMBOL')  # (
        # Parse expression to print
        expression = self.expression()
        self.consume('SYMBOL')  # )
        self.consume('SYMBOL')  # ;
        return {'type': 'PrintStatement', 'expression': expression}

    def if_statement(self):
        self.consume('KEYWORD')  # if
        self.consume('SYMBOL')  # (
        # Parse condition expression
        condition = self.expression()
        self.consume('SYMBOL')  # )

        # Parse if statement body
        if_body = self.statement()
        else_body = None
        if self.match('KEYWORD') and self.tokens[self.current_token_index].value == 'else':
            self.consume('KEYWORD')  # else
            # Parse else statement body
            else_body = self.statement()
        return {'type': 'IfStatement','condition': condition, 'if_body': if_body, 'else_body': else_body}

    def while_statement(self):
        self.consume('KEYWORD')  # while
        self.consume('SYMBOL')  # (
        # Parse condition expression
        condition = self.expression()
        self.consume('SYMBOL')  # )
        # Parse while loop body
        body = self.statement()
        return {'type': 'WhileStatement','while-condition': condition, 'body': body}

    def return_statement(self):
        self.consume('KEYWORD')  # return
        # Parse return expression
        expression = self.expression()
        self.consume('SYMBOL')  # ;
        return {'type': 'ReturnStatement', 'expression': expression}

    def block(self):
        self.consume('SYMBOL')  # {
        # Parse block statements
        statements = []
        while not self.match('SYMBOL'):
            statements.append(self.statement())
        self.consume('SYMBOL')  # }
        return {'statements': statements}

    def expression(self):
        return self.relational_expression()
    
    def relational_expression(self):
        expr = self.additive_expression()
        while self.match('RELATIONAL_OPERATOR'):
            operator = self.consume('RELATIONAL_OPERATOR').value
            right_expr = self.additive_expression()
            expr = {'left': expr, 'operator': operator, 'right': right_expr}
        return expr

    def additive_expression(self):
        expr = self.multiplicative_expression()
        while self.match('SYMBOL') and (self.tokens[self.current_token_index].value == '+' or self.tokens[self.current_token_index].value == '-'):
            operator = self.consume('SYMBOL').value
            right_expr = self.multiplicative_expression()
            expr = {'left': expr, 'operator': operator, 'right': right_expr}
        return expr

    def multiplicative_expression(self):
        expr = self.primary_expression()
        while self.match('SYMBOL') and (self.tokens[self.current_token_index].value == '*' or self.tokens[self.current_token_index].value == '/'):
            operator = self.consume('SYMBOL').value
            right_expr = self.primary_expression()
            expr = {'left': expr, 'operator': operator, 'right': right_expr}
        return expr

    def primary_expression(self):
        if self.match('SYMBOL') and self.tokens[self.current_token_index].value == '(':
            self.consume('SYMBOL')  # (
            # Parse expression within parentheses
            expression = self.expression()
            self.consume('SYMBOL')  # )
            return expression
        elif self.match('IDENTIFIER'):
            identifier = self.consume('IDENTIFIER').value
            return identifier
        elif self.match('INTEGER_LITERAL'):
            return int(self.consume('INTEGER_LITERAL').value)