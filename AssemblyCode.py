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
        self.main_program_variables = []
        self.global_space_counter = 0
    
    def generate_number(self, number, register):
        assembly_code = []
        binary_representation = bin(number)[2:]

        for i, bit in enumerate(binary_representation):
            if bit == '1':
                assembly_code.append(Instructions.INC.value + " " + register)
            if i < len(binary_representation) - 1:
                assembly_code.append(Instructions.SHL.value + " " + register)

        return assembly_code

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
        for i in range(len(self.declarations_in_main)):
            variable = {}
            if isinstance(self.declarations_in_main[i]['identifier'], str):
                variable['variable_'+str(i+1)] = self.declarations_in_main[i]['identifier']
                variable['initialized'] = False
                variable['place_in_memory'] = None
            elif isinstance(self.declarations_in_main[i]['identifier'], dict):
                variable['variable_'+str(i+1)] = (self.declarations_in_main[i]['identifier']['identifier'], self.declarations_in_main[i]['identifier']['range'])
                variable['initialized'] = False
                variable['place_in_memory'] = self.declarations_in_main[i]['identifier']['range']
                self.global_space_counter = variable['place_in_memory']              
            self.main_program_variables.append(variable)
        for block in self.program_basic_blocks[0]:
            assembly_code_for_one_block = self.identifyTypeOfInstructions(block)
            block['instructions'] = assembly_code_for_one_block
        for instruction in block['instructions']:
            for code in instruction:
                print(code)

    def identifyTypeOfInstructions(self, block):
        block_instructions = block['instructions']
        assembly_code_for_one_block = []
        for instruction in block_instructions:
            if ':=' in instruction:
                if instruction[1] == ':=':
                    assembly_code = self.assignToIntegerVariable(instruction)
                elif instruction[2] == ':=':
                    assembly_code = self.assignToArrayVariable(instruction)
            elif 'Write' in instruction:
                if len(instruction) == 1:
                    assembly_code = self.writeIntegerVariable(instruction)
                elif len(instruction) == 2:
                    assembly_code = self.writeArrayVariable(instruction)
            elif 'Read' in instruction:
                if len(instruction) == 1:
                    assembly_code = self.readToIntegerVariable(instruction)
                elif len(instruction) == 2:
                    assembly_code = self.readToArrayVariable(instruction)
            else:
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
        assembly_code = []
        if isinstance(instruction[2], int):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                    break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
                variable1['place_in_memory'] = self.global_space_counter
                self.global_space_counter += 1
            place_in_memory = variable1['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.extend(self.generate_number(instruction[2], "a"))
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[2], str):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                    break
            for var in self.main_program_variables:
                if instruction[2] in var.values():
                    variable2 = var
                    break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
                variable1['place_in_memory'] = self.global_space_counter
                self.global_space_counter += 1
            place_in_memory_of_variable1 = variable1['place_in_memory']
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_of_variable2, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toIntegerVariableAssignArrayVariable(self, instruction):
        assembly_code = []
        if isinstance(instruction[3], int):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                    break
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable2 = var
                        break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
                variable1['place_in_memory'] = self.global_space_counter
                self.global_space_counter += 1
            place_in_memory = variable1['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.extend(self.generate_number(instruction[3], "a"))
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[3], str):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                    break
            for var in self.main_program_variables:
                if instruction[3] in var.values():
                    variable2 = var
                    break
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable3 = var
                        break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
                variable1['place_in_memory'] = self.global_space_counter
                self.global_space_counter += 1
            place_in_memory_of_variable1 = variable1['place_in_memory']
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(place_in_memory_of_variable2, "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "c")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.LOAD.value + " " + "c")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toIntegerVariableAssignBinaryOperationOfTwoIntegerVariables(self, instruction):
        assembly_code = []
        if instruction[3] == '+':
            if isinstance(instruction[2], int) and isinstance(instruction[4], int):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                        break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                    variable1['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                place_in_memory = variable1['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[4], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], int) and isinstance(instruction[4], str):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                        break
                for var in self.main_program_variables:
                    if instruction[4] in var.values():
                        variable2 = var
                        break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                    variable1['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[2], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.ADD.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], str) and isinstance(instruction[4], int):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                        break
                for var in self.main_program_variables:
                    if instruction[2] in var.values():
                        variable2 = var
                        break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                    variable1['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[4], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.ADD.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], str) and isinstance(instruction[4], str):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                        break
                for var in self.main_program_variables:
                    if instruction[2] in var.values():
                        variable2 = var
                        break
                for var in self.main_program_variables:
                    if instruction[4] in var.values():
                        variable3 = var
                        break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                    variable1['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable3, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.ADD.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

        elif instruction[3] == '-':
            if isinstance(instruction[2], int) and isinstance(instruction[4], int):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                        break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                    variable1['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                place_in_memory = variable1['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[4], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.SUB.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], int) and isinstance(instruction[4], str):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                        break
                for var in self.main_program_variables:
                    if instruction[4] in var.values():
                        variable2 = var
                        break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                    variable1['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[2], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], str) and isinstance(instruction[4], int):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                        break
                for var in self.main_program_variables:
                    if instruction[2] in var.values():
                        variable2 = var
                        break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                    variable1['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[4], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], str) and isinstance(instruction[4], str):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                        break
                for var in self.main_program_variables:
                    if instruction[2] in var.values():
                        variable2 = var
                        break
                for var in self.main_program_variables:
                    if instruction[4] in var.values():
                        variable3 = var
                        break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                    variable1['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable3, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")
                
        elif instruction[3] == '*':
            pass
        elif instruction[3] == '/':
            pass        
        elif instruction[3] == '%':
            pass
        return assembly_code

    def toIntegerVariableAssignBinaryOperationOfIntegerAndArrayVariables(self, instruction):
        if instruction[3] in ['+', '-', '*', '/', '%']:
            if instruction[3] == '+':
                if isinstance(instruction[2], int) and isinstance(instruction[5], int):
                    pass
                elif isinstance(instruction[2], int) and isinstance(instruction[5], str):
                    pass
                elif isinstance(instruction[2], str) and isinstance(instruction[5], int):
                    pass
                elif isinstance(instruction[2], str) and isinstance(instruction[5], str):
                    pass
            elif instruction[3] == '-':
                if isinstance(instruction[2], int) and isinstance(instruction[5], int):
                    pass
                elif isinstance(instruction[2], int) and isinstance(instruction[5], str):
                    pass
                elif isinstance(instruction[2], str) and isinstance(instruction[5], int):
                    pass
                elif isinstance(instruction[2], str) and isinstance(instruction[5], str):
                    pass
            elif instruction[3] == '*':
                pass
            elif instruction[3] == '/':
                pass        
            elif instruction[3] == '%':
                pass
        elif instruction[4] in ['+', '-', '*', '/', '%']:
            if instruction[4] == '+':
                if isinstance(instruction[3], int) and isinstance(instruction[5], int):
                    pass
                elif isinstance(instruction[3], int) and isinstance(instruction[5], str):
                    pass
                elif isinstance(instruction[3], str) and isinstance(instruction[5], int):
                    pass
                elif isinstance(instruction[3], str) and isinstance(instruction[5], str):
                    pass
            elif instruction[4] == '-':
                if isinstance(instruction[3], int) and isinstance(instruction[5], int):
                    pass
                elif isinstance(instruction[3], int) and isinstance(instruction[5], str):
                    pass
                elif isinstance(instruction[3], str) and isinstance(instruction[5], int):
                    pass
                elif isinstance(instruction[3], str) and isinstance(instruction[5], str):
                    pass
            elif instruction[4] == '*':
                pass
            elif instruction[4] == '/':
                pass        
            elif instruction[4] == '%':
                pass

    def toIntegerVariableAssignBinaryOperationOfTwoArraysVariables(self, instruction):
        if instruction[4] == '+':
            if isinstance(instruction[3], int) and isinstance(instruction[6], int):
                pass
            elif isinstance(instruction[3], int) and isinstance(instruction[6], str):
                pass
            elif isinstance(instruction[3], str) and isinstance(instruction[6], int):
                pass
            elif isinstance(instruction[3], str) and isinstance(instruction[6], str):
                pass
        elif instruction[4] == '-':
            if isinstance(instruction[3], int) and isinstance(instruction[6], int):
                pass
            elif isinstance(instruction[3], int) and isinstance(instruction[6], str):
                pass
            elif isinstance(instruction[3], str) and isinstance(instruction[6], int):
                pass
            elif isinstance(instruction[3], str) and isinstance(instruction[6], str):
                pass
        elif instruction[4] == '*':
            pass
        elif instruction[4] == '/':
            pass        
        elif instruction[4] == '%':
            pass

    def toArrayVariableAssignIntegerVariable(self, instruction):
        assembly_code = []
        if isinstance(instruction[1], int) and isinstance(instruction[3], int):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable1 = var
                        break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[1], "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(instruction[3], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")
                        
        elif isinstance(instruction[1], int) and isinstance(instruction[3], str):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable1 = var
                        break
            for var in self.main_program_variables:
                if instruction[3] in var.values():
                    variable2 = var
                    break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[1], "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(place_in_memory_of_variable2, "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[1], str) and isinstance(instruction[3], int):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable1 = var
                        break
            for var in self.main_program_variables:
                if instruction[1] in var.values():
                    variable2 = var
                    break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(instruction[3], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(place_in_memory_of_variable2, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.GET.value + " " + "c")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[1], str) and isinstance(instruction[3], str):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable1 = var
                        break
            for var in self.main_program_variables:
                if instruction[1] in var.values():
                    variable2 = var
                    break
            for var in self.main_program_variables:
                if instruction[3] in var.values():
                    variable3 = var
                    break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable2 = variable2['place_in_memory']
            place_in_memory_of_variable3 = variable3['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(place_in_memory_of_variable2, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(place_in_memory_of_variable3, "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.LOAD.value + " " + "c")
            assembly_code.append(Instructions.STORE.value + " " + "b")  

        return assembly_code

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
