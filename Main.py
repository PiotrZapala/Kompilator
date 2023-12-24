from Parser import Parser
from AbstractSyntaxTree import AbstractSyntaxTree
from Debugger import Debugger

def main():
    with open("tests/error1.imp", "r") as file:
        data = file.read()

    parser = Parser()
    parser.build()
    result = parser.parse(data)
    AST = AbstractSyntaxTree(result)
    DEB = Debugger()
    decl_in_main = AST.getVariableDeclarationsInMain()
    procedures_head = AST.getArgumentsDeclarationsInProceduresHead()
    decl_in_procedures = AST.getVariableDeclarationsInProcedures()
    main_commands_array, procedure_commands_array = AST.traverseTreeForCommands()
    #AST.printMainProgram(decl_in_main, main_commands_array)
    #AST.printProcedures(procedures_head, decl_in_procedures, procedure_commands_array)
    DEB.programDebugger(main_commands_array, decl_in_main, procedure_commands_array, decl_in_procedures, procedures_head)

if __name__ == "__main__":
    main()
