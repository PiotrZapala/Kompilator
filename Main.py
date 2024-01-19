from Parser import Parser
from AbstractSyntaxTree import AbstractSyntaxTree
from Debugger import Debugger
from BasicBlocks import BasicBlocks
from AssemblyCode import AssemblyCode

def main():
    with open("testy/test2.imp", "r") as file:
        data = file.read()
    parser = Parser()
    parser.build()
    result = parser.parse(data)
    AST = AbstractSyntaxTree(result)
    DEB = Debugger()
    declarations_in_main = AST.getVariableDeclarationsInMain()
    procedures_head = AST.getArgumentsDeclarationsInProceduresHead()
    declarations_in_procedures = AST.getVariableDeclarationsInProcedures()
    main_commands_array, procedure_commands_array = AST.traverseTreeForCommands()
    #AST.printMainProgram(declarations_in_main, main_commands_array)
    #AST.printProcedures(procedures_head, declarations_in_procedures, procedure_commands_array)
    #DEB.programDebugger(main_commands_array, declarations_in_main, procedure_commands_array, declarations_in_procedures, procedures_head)
    BLOCKS = BasicBlocks(procedure_commands_array, main_commands_array)
    main_program_blocks, procedures_blocks = BLOCKS.createBasicBlocks()
    #for block in procedures_blocks[0]:
        #print(block)

    ASM = AssemblyCode(main_program_blocks, declarations_in_main, procedures_blocks, declarations_in_procedures, procedures_head)
    ASM.createAssemblyCode()
    
if __name__ == "__main__":
    main()
