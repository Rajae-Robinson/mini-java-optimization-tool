from ir import TACGenerator
from lexer import Lexer
from mini_java_parser import MiniJavaParser

def main():
    code = '''
    class WhileIfExample {
        public static void main(String[] args) {
            int x;
            x = 5;
            System.out.println(x);
            if (5) {
                System.out.println(1);
            } else {
                System.out.println(0);
            }
            int i;
            i = 0;
            while (5) {
                System.out.println(i);
                i = i + 1;
            }
            return 0;
        }
    }
    '''
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
        print(f"Syntax error: {e} at line {code.count('\n', 0, parser.current_token_index) + 1}")

    if(parse_tree):
        tac_generator = TACGenerator(parse_tree)
        tac_generator.generate_tac()
        print("INTERMEDIATE CODE GENERATION\n")
        print("TAC Instructions:")
        for instruction in tac_generator.instructions:
            print(instruction)

if __name__ == "__main__":
    main()
