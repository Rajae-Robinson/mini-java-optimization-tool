import sys
from ir import TACGenerator
from lexer import Lexer
from mini_java_parser import MiniJavaParser

def main(file_path):
    try:
        with open(file_path, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return

    lexer = Lexer(code)
    print("LEXICAL ANALYSIS\n")
    print("Tokens\n")
    print(f"{lexer.tokens}\n\n")

    parser = MiniJavaParser(lexer.tokens)
    parse_tree = None
    try:
        parse_tree = parser.parse()
        print("SYNTAX ANALYSIS\n")
        print("Parse tree output")
        print(f"{parse_tree}\n\n")
    except SyntaxError as e:
        print("Syntax error: " + str(e) + " at line " + str(code.count('\n', 0, parser.current_token_index) + 1))

    if parse_tree:
        tac_generator = TACGenerator(parse_tree)
        tac_generator.generate_tac()
        print("INTERMEDIATE CODE GENERATION\n")
        print("TAC Instructions:")
        for instruction in tac_generator.instructions:
            print(instruction)

if __name__ == "__main__":
    file_path = sys.argv[1] if len(sys.argv) > 1 else "input.java"
    main(file_path)
