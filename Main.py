from Parser import Parser
from AbstractSyntaxTree import AbstractSyntaxTree
from Debugger import Debugger
from BasicBlocks import BasicBlocks

def main():
    with open("testy/test1.imp", "r") as file:
        data = file.read()
    parser = Parser()
    parser.build()
    result = parser.parse(data)
    AST = AbstractSyntaxTree(result)
    DEB = Debugger()
    BLOCKS = BasicBlocks()
    decl_in_main = AST.getVariableDeclarationsInMain()
    procedures_head = AST.getArgumentsDeclarationsInProceduresHead()
    decl_in_procedures = AST.getVariableDeclarationsInProcedures()
    main_commands_array, procedure_commands_array = AST.traverseTreeForCommands()
    #print(procedure_commands_array)
    #AST.printMainProgram(decl_in_main, main_commands_array)
    #AST.printProcedures(procedures_head, decl_in_procedures, procedure_commands_array)
    #DEB.programDebugger(main_commands_array, decl_in_main, procedure_commands_array, decl_in_procedures, procedures_head)
    BLOCKS.createBasicBlocks(procedure_commands_array[0])
    #print(basic_blocks[0][0].first_jump.first_jump.second_jump.first_jump.first_jump)
    #print(basic_blocks[0][0].first_jump.first_jump.second_jump.first_jump.second_jump.first_jump.first_jump.first_jump.first_jump.second_jump)
    #print(basic_blocks[0][0].first_jump.first_jump.first_jump.first_jump.second_jump.first_jump.first_jump.first_jump.first_jump.first_jump.first_jump.first_jump.first_jump.second_jump.first_jump.second_jump.second_jump.second_jump.first_jump.first_jump.second_jump.second_jump)

if __name__ == "__main__":
    main()
