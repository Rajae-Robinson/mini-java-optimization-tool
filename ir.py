# Three Address Code Generator
import re

class TACGenerator:
    def __init__(self, parse_tree):
        self.parse_tree = parse_tree
        self.current_temp_var = 0
        self.instructions = []

    def generate_tac(self):
        for class_declaration in self.parse_tree:
            for method in class_declaration['methods']:
                self.generate_tac_for_block(method['statements'])

    def generate_tac_for_block(self, block):
        for statement in block:
            if 'type' in statement:
                if statement['type'] == 'VariableDeclaration':
                    self.generate_tac_for_variable_declaration(statement)
                elif statement['type'] == 'Assignment':
                    self.generate_tac_for_assignment(statement)
                elif statement['type'] == 'PrintStatement':
                    self.generate_tac_for_print_statement(statement)
                elif statement['type'] == 'IfStatement':
                    self.generate_tac_for_if_statement(statement)
                elif statement['type'] == 'WhileStatement':
                    self.generate_tac_for_while_statement(statement)
                elif statement['type'] == 'ReturnStatement':
                    self.generate_tac_for_return_statement(statement)

    def generate_temp_var(self):
        temp_var = f't{self.current_temp_var}'
        self.current_temp_var += 1
        return temp_var

    def generate_tac_for_variable_declaration(self, statement):
        if 'expression' in statement:
            temp_var = self.generate_temp_var()
            self.instructions.append(f'{statement["name"]} = {self.generate_tac_for_expression(statement["expression"])}')

    def generate_tac_for_assignment(self, statement):
        self.instructions.append(f'{statement["var_name"]} = {self.generate_tac_for_expression(statement["expression"])}')

    def generate_tac_for_print_statement(self, statement):
        self.instructions.append(f'print {self.generate_tac_for_expression(statement["expression"])}')

    def generate_tac_for_if_statement(self, statement):
        else_start_label = f'L{len(self.instructions) + 1}'
        condition = self.generate_tac_for_expression(statement['condition'])
        self.instructions.append(f'if not {condition} goto {else_start_label}')
        self.generate_tac_for_block(statement['if_body']['statements'])
        self.instructions.append(f'{else_start_label}:')
        if statement['else_body']:
            self.generate_tac_for_block(statement['else_body']['statements'])

    def generate_tac_for_while_statement(self, statement):
        loop_start_label = f'L{len(self.instructions) + 1}'
        loop_end_label = f'L{len(self.instructions) + 2}'
        self.instructions.append(loop_start_label + ':')
        condition = self.generate_tac_for_expression(statement['while-condition'])
        self.instructions.append(f'if not {condition} goto {loop_end_label}')
        self.generate_tac_for_block(statement['body']['statements'])
        self.instructions.append(f'goto {loop_start_label}')
        self.instructions.append(f'{loop_end_label}:')

    def generate_tac_for_return_statement(self, statement):
        self.instructions.append(f'return {self.generate_tac_for_expression(statement["expression"])}')

    def generate_tac_for_expression(self, expression):
        if expression is None:
            return None
        if isinstance(expression, int):
            return str(expression)
        elif isinstance(expression, str) and expression.isalnum():
            return expression
        else:
            left = self.generate_tac_for_expression(expression['left']) # type: ignore
            right = self.generate_tac_for_expression(expression['right']) # type: ignore
            temp_var = self.generate_temp_var()
            self.instructions.append(f'{temp_var} = {left} {expression["operator"]} {right}') # type: ignore
            return temp_var
        
    def optimize_tac(self):
        self.constant_folding()
        self.dead_code_elimination()
        self.common_subexpression_elimination()
        self.loop_unrolling()

    def constant_folding(self):
        def has_no_letters(text):
            return not re.search('[a-zA-Z]', text)
        
        for i, instruction in enumerate(self.instructions):
            parts = instruction.split(' = ')
            if len(parts) == 2 and has_no_letters(parts[1]):
                self.instructions[i] = f"{parts[0]} = {eval(parts[1])}"

    def dead_code_elimination(self):
        used_variables = set()
    
        # First pass: identify variables that are used
        for instruction in self.instructions:
            parts = instruction.split(' = ')
            if len(parts) == 2:
                expr = parts[1].strip()
                assigned_variable = parts[0].strip()
                if expr != "None":
                    used_variables.add(assigned_variable)
        
        # Second pass: remove instructions for unused variables
        new_instructions = []
        for instruction in self.instructions:
            parts = instruction.split(' = ')
            if len(parts) == 2:
                assigned_variable = parts[0].strip()
                if assigned_variable in used_variables:
                    new_instructions.append(instruction)
            else:
                new_instructions.append(instruction)
        
        self.instructions = new_instructions

    def common_subexpression_elimination(self):
        expressions = {}
        for i, instruction in enumerate(self.instructions):
            parts = instruction.split(' = ')
            if len(parts) == 2:
                expr = parts[1]
                if expr in expressions:
                    self.instructions[i] = f"{parts[0]} = {expressions[expr]}"
                else:
                    expressions[expr] = parts[0]
    
    def loop_unrolling(self, max_unroll=2):
        for i in range(len(self.instructions)):
            instruction = self.instructions[i]
            if instruction.startswith('goto L') and i > 0:
                label = instruction.split()[1]
                loop_start_index = None
                for j in range(i - 1, -1, -1):
                    if self.instructions[j].startswith(label + ':'):
                        loop_start_index = j
                        break
                if loop_start_index is not None:
                    loop_body = self.instructions[loop_start_index + 1:i]
                    for k in range(max_unroll - 1):
                        self.instructions[loop_start_index + 1:loop_start_index + 1] = loop_body