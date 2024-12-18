import re

class Interpreter:
    def __init__(self):
        self.variables = {}

    def parse_program(self, program):
        lines = program.strip().split("\n")
        for line in lines:
            line = line.strip()
            if not line.endswith(";"):
                print("Syntax error: Missing semicolon")
                return False

            assignment = line[:-1]  # Remove the semicolon
            if not self.parse_assignment(assignment):
                return False
        return True

    def parse_assignment(self, assignment):
        if "=" not in assignment:
            print("Syntax error: Missing '=' in assignment")
            return False

        identifier, expression = map(str.strip, assignment.split("=", 1))

        if not self.is_valid_identifier(identifier):
            print(f"Syntax error: Invalid identifier '{identifier}'")
            return False

        value = self.evaluate_expression(expression)
        if value is None:
            return False

        self.variables[identifier] = value
        return True

    def evaluate_expression(self, expression):
        if not self.validate_expression(expression):
            print("Syntax error: Invalid expression")
            return None

        try:
            sanitized_expression = self.sanitize_expression(expression)
            if sanitized_expression is None:
                print("Error: Uninitialized variable in expression")
                return None
            return eval(sanitized_expression, {}, self.variables)
        except (NameError, SyntaxError):
            print("Syntax error: Invalid expression")
            return None

    def validate_expression(self, expression):
        # Ensure valid tokens and proper structure (e.g., balanced parentheses)
        tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|[-+*/()]|\d+", expression)
        if not tokens:
            return False

        # Check for balanced parentheses
        balance = 0
        for token in tokens:
            if token == "(":
                balance += 1
            elif token == ")":
                balance -= 1
                if balance < 0:
                    return False

        if balance != 0:
            return False

        # Check for invalid sequences like `+-`, `*/`, etc.
        expression = "".join(tokens)
        if re.search(r"[+\-*/]{2,}", expression):
            return False

        return True

    def sanitize_expression(self, expression):
        # Replace valid identifiers with their values
        tokens = re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*|[-+*/()]|\d+", expression)
        sanitized = []
        for token in tokens:
            if self.is_valid_identifier(token):
                if token not in self.variables:
                    return None  # Uninitialized variable
                sanitized.append(str(self.variables[token]))
            elif token.isdigit() and not token.startswith("0") or token == "0":
                sanitized.append(token)
            elif re.match(r"[-+*/()]", token):
                sanitized.append(token)
            else:
                return None

        return "".join(sanitized)

    def is_valid_identifier(self, identifier):
        return re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", identifier) is not None

    def print_variables(self):
        for var, value in sorted(self.variables.items()):
            print(f"{var} = {value}")

# Input program
programs = [
    "x = 001;",
    "x_2 = 0;",
    "x = 0\ny = x;\nz = ---(x+y);",
    "x = 1;\ny = 2;\nz = ---(x+y)*(x+-y);",
]

for i, program in enumerate(programs, start=1):
    print(f"Input {i}")
    interpreter = Interpreter()
    if interpreter.parse_program(program):
        interpreter.print_variables()
    print("\n")