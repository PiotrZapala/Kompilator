import sys
from Parser import Parser
from Debugger import Debugger
from BasicBlocks import BasicBlocks
from AssemblyCode import AssemblyCode
from AbstractSyntaxTree import AbstractSyntaxTree

def main():
    if len(sys.argv) < 2:
        print("Użycie: python3 Kompilator.py nazwa_pliku.imp")
        return
    filename = sys.argv[1]
    try:
        with open(filename, "r") as file:
            data = file.read()
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {filename}")
        return
    parser = Parser()
    parser.build()
    result = parser.parse(data)
    AST = AbstractSyntaxTree(result)
    DEB = Debugger()
    declarations_in_main = AST.getVariableDeclarationsInMain()
    procedures_head = AST.getArgumentsDeclarationsInProceduresHead()
    declarations_in_procedures = AST.getVariableDeclarationsInProcedures()
    main_commands_array, procedure_commands_array = AST.traverseTreeForCommands()
    DEB.programDebugger(main_commands_array, declarations_in_main, procedure_commands_array, declarations_in_procedures, procedures_head)
    BLOCKS = BasicBlocks(procedure_commands_array, main_commands_array)
    main_program_blocks, procedures_blocks = BLOCKS.createBasicBlocks()
    ASM = AssemblyCode(main_program_blocks, declarations_in_main, procedures_blocks, declarations_in_procedures, procedures_head)
    ASM.createAssemblyCode()
    
if __name__ == "__main__":
    main()   
