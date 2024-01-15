from enum import Enum

class Instructions(Enum):
    READ = "READ"
    WRITE = "WRITE"
    LOAD = "LOAD"
    STORE = "STORE"
    ADD = "ADD"
    SUB = "SUB"
    GET = "GET"
    PUT = "PUT"
    RST = "RST"
    INC = "INC"
    DEC = "DEC"
    SHL = "SHL"
    SHR = "SHR"
    JUMP = "JUMP"
    JPOS = "JPOS"
    JZERO = "JZERO"
    STRK = "STRK"
    JUMPR = "JUMPR"
    HALT = "HALT"

class AssemblyCode:

    def __init__(self, program_basic_blocks, declarations_in_main, procedures_basic_blocks=None, declarations_in_procedures=None, procedures_head=None):
        self.assembly_code = ""
        self.program_basic_blocks = program_basic_blocks
        self.declarations_in_main = declarations_in_main
        self.procedures_basic_blocks = procedures_basic_blocks
        self.declarations_in_procedures = declarations_in_procedures
        self.procedures_head = procedures_head

    def createAssemblyCode(self):
        #self.getAssemblyCodeFromProcedureBlocks()
        self.getAssemblyCodeFromMainProgramBlocks()

    def getAssemblyCodeFromProcedureBlocks(self):
        for procedure_blocks in self.procedures_basic_blocks:
            for block in procedure_blocks:
                print(block)
                block_instructions = block['instructions']
                #self.identifyTypeOfInstructions(block_instructions)
            print()

    def getAssemblyCodeFromMainProgramBlocks(self):
        for block in self.program_basic_blocks[0]:
            print(block)
            block_instructions = block['instructions']
            #self.identifyTypeOfInstructions(block_instructions)
        print()

    def identifyTypeOfInstructions(self, block_instructions):
        assembly_code_for_one_block = []
        for instruction in block_instructions:
            if instruction.type == 'Assign':
                if instruction[1] == ':=':
                    assembly_code = self.assignToIntegerVariable(instruction)
                elif instruction[2] == ':=':
                    assembly_code = self.assignToArrayVariable(instruction)
            elif instruction.type == 'Write':
                if len(instruction) == 1:
                    assembly_code = self.writeIntegerVariable(instruction)
                elif len(instruction) == 2:
                    assembly_code = self.writeArrayVariable(instruction)
            elif instruction.type == 'Read':
                if len(instruction) == 1:
                    assembly_code = self.readToIntegerVariable(instruction)
                elif len(instruction) == 2:
                    assembly_code = self.readToArrayVariable(instruction)
            elif instruction.type == 'Condition':
                if len(instruction) == 3:
                    assembly_code = self.checkConditionForTwoIntegerVariables(instruction)
                elif len(instruction) == 4:
                    assembly_code = self.checkConditionForIntegerAndArrayVariables(instruction)
                elif len(instruction) == 5:
                    assembly_code = self.checkConditionForTwoArrayVariables(instruction)
            assembly_code_for_one_block.append(assembly_code)
        return assembly_code_for_one_block
    

    def assignToIntegerVariable(self, instruction):
        if len(instruction) == 3:
            assembly_code = self.toIntegerVariableAssignIntegerVariable(instruction)
        elif len(instruction) == 4:
            assembly_code = self.toIntegerVariableAssignArrayVariable(instruction)  
        elif len(instruction) == 5:
            assembly_code = self.toIntegerVariableAssignBinaryOperationOfTwoIntegerVariables(instruction)
        elif len(instruction) == 6:
            assembly_code = self.toIntegerVariableAssignBinaryOperationOfIntegerAndArrayVariables(instruction)
        elif len(instruction) == 7:
            assembly_code = self.toIntegerVariableAssignBinaryOperationOfTwoArraysVariables(instruction)
        return assembly_code

    def assignToArrayVariable(self, instruction):
        if len(instruction) == 4:
            assembly_code = self.toArrayVariableAssignIntegerVariable(instruction)
        elif len(instruction) == 5:
            assembly_code = self.toArrayVariableAssignArrayVariable(instruction)  
        elif len(instruction) == 6:
            assembly_code = self.toArrayVariableAssignBinaryOperationOfTwoIntegerVariables(instruction)
        elif len(instruction) == 7:
            assembly_code = self.toArrayVariableAssignBinaryOperationOfIntegerAndArrayVariables(instruction)
        elif len(instruction) == 8:
            assembly_code = self.toArrayVariableAssignBinaryOperationOfTwoArraysVariables(instruction)
        return assembly_code

    def toIntegerVariableAssignIntegerVariable(self, instruction):
        pass

    def toIntegerVariableAssignArrayVariable(self, instruction):
        pass

    def toIntegerVariableAssignBinaryOperationOfTwoIntegerVariables(self, instruction):
        if instruction[3] == '+':
            pass
        elif instruction[3] == '-':
            pass
        elif instruction[3] == '*':
            pass
        elif instruction[3] == '/':
            pass        
        elif instruction[3] == '%':
            pass

    def toIntegerVariableAssignBinaryOperationOfIntegerAndArrayVariables(self, instruction):
        if instruction[3] in ['+', '-', '*', '/', '%']:
            if instruction[3] == '+':
                pass
            elif instruction[3] == '-':
                pass
            elif instruction[3] == '*':
                pass
            elif instruction[3] == '/':
                pass        
            elif instruction[3] == '%':
                pass
        elif instruction[4] in ['+', '-', '*', '/', '%']:
            if instruction[4] == '+':
                pass
            elif instruction[4] == '-':
                pass
            elif instruction[4] == '*':
                pass
            elif instruction[4] == '/':
                pass        
            elif instruction[4] == '%':
                pass

    def toIntegerVariableAssignBinaryOperationOfTwoArraysVariables(self, instruction):
        if instruction[4] == '+':
            pass
        elif instruction[4] == '-':
            pass
        elif instruction[4] == '*':
            pass
        elif instruction[4] == '/':
            pass        
        elif instruction[4] == '%':
            pass

    def toArrayVariableAssignIntegerVariable(self, instruction):
        pass

    def toArrayVariableAssignArrayVariable(self, instruction):
        pass

    def toArrayVariableAssignBinaryOperationOfTwoIntegerVariables(self, instruction):
        if instruction[4] == '+':
            pass
        elif instruction[4] == '-':
            pass
        elif instruction[4] == '*':
            pass
        elif instruction[4] == '/':
            pass        
        elif instruction[4] == '%':
            pass

    def toArrayVariableAssignBinaryOperationOfIntegerAndArrayVariables(self, instruction):
        if instruction[4] in ['+', '-', '*', '/', '%']:
            if instruction[4] == '+':
                pass
            elif instruction[4] == '-':
                pass
            elif instruction[4] == '*':
                pass
            elif instruction[4] == '/':
                pass        
            elif instruction[4] == '%':
                pass
        elif instruction[5] in ['+', '-', '*', '/', '%']:
            if instruction[5] == '+':
                pass
            elif instruction[5] == '-':
                pass
            elif instruction[5] == '*':
                pass
            elif instruction[5] == '/':
                pass        
            elif instruction[5] == '%':
                pass

    def toArrayVariableAssignBinaryOperationOfTwoArraysVariables(self, instruction):
        if instruction[5] == '+':
            pass
        elif instruction[5] == '-':
            pass
        elif instruction[5] == '*':
            pass
        elif instruction[5] == '/':
            pass        
        elif instruction[5] == '%':
            pass

    def writeIntegerVariable(self, instruction):
        pass

    def writeArrayVariable(self, instruction):
        pass

    def readToIntegerVariable(self, instruction):
        pass

    def readToArrayVariable(self, instruction):
        pass

    def checkConditionForTwoIntegerVariables(self, instruction):
        if instruction[1] == '=':
            pass
        elif instruction[1] == '<':
            pass
        elif instruction[1] == '>':
            pass
        elif instruction[1] == '<=':
            pass
        elif instruction[1] == '>=':
            pass
        elif instruction[1] == '!=':
            pass

    def checkConditionForIntegerAndArrayVariables(self, instruction):
        if instruction[1] in ['=', '<', '>', '<=', '>=', '!=']:
            if instruction[1] == '=':
                pass
            elif instruction[1] == '<':
                pass
            elif instruction[1] == '>':
                pass
            elif instruction[1] == '<=':
                pass
            elif instruction[1] == '>=':
                pass
            elif instruction[1] == '!=':
                pass
        elif instruction[2] in ['=', '<', '>', '<=', '>=', '!=']:
            if instruction[2] == '=':
                pass
            elif instruction[2] == '<':
                pass
            elif instruction[2] == '>':
                pass
            elif instruction[2] == '<=':
                pass
            elif instruction[2] == '>=':
                pass
            elif instruction[2] == '!=':
                pass

    def checkConditionForTwoArrayVariables(self, instruction):
        if instruction[2] == '=':
            pass
        elif instruction[2] == '<':
            pass
        elif instruction[2] == '>':
            pass
        elif instruction[2] == '<=':
            pass
        elif instruction[2] == '>=':
            pass
        elif instruction[2] == '!=':
            pass
