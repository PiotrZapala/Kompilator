from Parser import Parser
from AbstractSyntaxTree import AbstractSyntaxTree

def main():
    with open("tests/error1.imp", "r") as file:
        data = file.read()

    parser = Parser()
    parser.build()
    result = parser.parse(data)
    AST = AbstractSyntaxTree(result)
    decl_in_main = AST.getVariableDeclarationsInMain()
    procedures_head = AST.getArgumentsDeclarationsInProceduresHead()
    decl_in_procedures = AST.getVariableDeclarationsInProcedures()
    main_commands_array, procedure_commands_array = AST.traverseTreeForCommands()
    #printMainProgram(decl_in_main, main_commands_array)
    #printProcedures(procedures_head, decl_in_procedures, procedure_commands_array)
    AST.checkIfThereAreUndeclaredVariables(procedure_commands_array[0], decl_in_procedures[0], procedures_head[0])

def printNestedDict(d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            print(" " * indent + f"{key}:")
            printNestedDict(value, indent + 4)
        elif isinstance(value, list):
            print(" " * indent + f"{key}:")
            for item in value:
                printNestedDict(item, indent + 4)
        else:
            print(" " * indent + f"{key}: {value}")

def printMainProgram(decl_in_main, main_commands_array):
    print()
    print("Main Program Declarations")
    for z in range(len(decl_in_main)):
        printNestedDict(decl_in_main[z])
    print()
    print("Main Program Commands")
    for i in range(len(main_commands_array)):
        printNestedDict(main_commands_array[i])

def printProcedures(procedures_head, decl_in_procedures, procedure_commands_array):
    for k in range(len(procedures_head)):
        print()
        print("Procedure Identifier")
        print(procedures_head[k]["procedure identifier"])
        print()
        print("Procedure Head")
        for j in range(len(procedures_head[k]["arguments declarations"])):
            printNestedDict(procedures_head[k]["arguments declarations"][j])
        print()
        print("Procedure Declarations")
        if len(decl_in_procedures) != 0:
            for z in range(len(decl_in_procedures[k])):
                printNestedDict(decl_in_procedures[k][z])
            print()
        print("Procedure Commands")
        for i in range(len(procedure_commands_array[k])):
            printNestedDict(procedure_commands_array[k][i])

if __name__ == "__main__":
    main()