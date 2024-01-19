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
        program = []
        for i in range(len(self.declarations_in_main)):
            variable = {}
            if isinstance(self.declarations_in_main[i]['identifier'], str):
                variable['variable_'+str(i+1)] = self.declarations_in_main[i]['identifier']
                variable['initialized'] = False
                variable['place_in_memory'] = self.global_space_counter
                self.global_space_counter += 1
            elif isinstance(self.declarations_in_main[i]['identifier'], dict):
                variable['variable_'+str(i+1)] = (self.declarations_in_main[i]['identifier']['identifier'], self.declarations_in_main[i]['identifier']['range'])
                variable['initialized'] = False
                variable['starts_at'] = self.global_space_counter
                variable['ends_at'] = self.declarations_in_main[i]['identifier']['range'] + self.global_space_counter - 1
                self.global_space_counter = self.global_space_counter + self.declarations_in_main[i]['identifier']['range']              
            self.main_program_variables.append(variable)
        for block in self.program_basic_blocks[0]:
            assembly_code_for_one_block = self.identifyTypeOfInstructions(block)
            if len(assembly_code_for_one_block) >= 2:
                block['instructions'] = [[instr for sublist in assembly_code_for_one_block for instr in sublist]]
                block['instructions'][0].append("block " + str(block['first_jump']))
            else:
                if 'second_jump' in block:
                    block['instructions'] = assembly_code_for_one_block
                else:
                    block['instructions'] = assembly_code_for_one_block
                    block['instructions'][0].append("block " + str(block['first_jump']))
            block['instructions'][0].insert(0, "block " + str(block['block']))
        for block in self.program_basic_blocks[0]:
            program.append(block['instructions'][0])

        for block in program:
            for code in block:
                print(code)
        for block in program:
            print(block)
    
    def identifyTypeOfInstructions(self, block):
        block_instructions = block['instructions']
        assembly_code_for_one_block = []
        for instruction in block_instructions:
            print(instruction)
            if ':=' in instruction:
                if instruction[1] == ':=':
                    assembly_code = self.assignToIntegerVariable(instruction)
                elif instruction[2] == ':=':
                    assembly_code = self.assignToArrayVariable(instruction)
            elif 'Write' in instruction:
                if len(instruction) == 2:
                    assembly_code = self.writeIntegerVariable(instruction)
                elif len(instruction) == 3:
                    assembly_code = self.writeArrayVariable(instruction)
            elif 'Read' in instruction:
                if len(instruction) == 2:
                    assembly_code = self.readToIntegerVariable(instruction)
                elif len(instruction) == 3:
                    assembly_code = self.readToArrayVariable(instruction)
            elif 'ProcCall' in instruction:
                print("lala")                   
            else:
                if len(instruction) == 3:
                    assembly_code = self.checkConditionForTwoIntegerVariables(instruction, block)
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
                if instruction[2] in var.values():
                    variable2 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
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
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[2]:
                        variable2 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory = variable1['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.extend(self.generate_number(instruction[3]+variable2['starts_at'], "a"))
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[3], str):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[2]:
                        variable3 = var
                if instruction[3] in var.values():
                    variable2 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
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
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable3['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "c")    
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toIntegerVariableAssignBinaryOperationOfTwoIntegerVariables(self, instruction):
        assembly_code = []
        if isinstance(instruction[2], int) and isinstance(instruction[4], int):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                    break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory = variable1['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[2], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(instruction[4], "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            if instruction[3] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "b")
            elif instruction[3] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "b")
            elif instruction[3] == '*':
                pass
            elif instruction[3] == '/':
                pass
            elif instruction[3] == '%':
                pass
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[2], int) and isinstance(instruction[4], str):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                if instruction[4] in var.values():
                    variable2 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
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
            if instruction[3] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[3] == '-':
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.GET.value + " " + "c")
                assembly_code.append(Instructions.SUB.value + " " + "b")
            elif instruction[3] == '*':
                pass
            elif instruction[3] == '/':
                pass
            elif instruction[3] == '%':
                pass
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[2], str) and isinstance(instruction[4], int):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                if instruction[2] in var.values():
                    variable2 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
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
            if instruction[3] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[3] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "c")
            elif instruction[3] == '*':
                pass
            elif instruction[3] == '/':
                pass
            elif instruction[3] == '%':
                pass
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[2], str) and isinstance(instruction[4], str):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                if instruction[2] in var.values():
                    variable2 = var
                if instruction[4] in var.values():
                    variable3 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
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
            if instruction[3] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[3] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "c")
            elif instruction[3] == '*':
                pass
            elif instruction[3] == '/':
                pass
            elif instruction[3] == '%':
                pass
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toIntegerVariableAssignBinaryOperationOfIntegerAndArrayVariables(self, instruction):
        assembly_code = []
        if instruction[3] in ['+', '-', '*', '/', '%']:
            if isinstance(instruction[2], int) and isinstance(instruction[5], int):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[4]:
                               variable2 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory = variable1['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[2], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[5]+variable2['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                if instruction[3] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[3] == '-':
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.GET.value + " " + "c")
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[3] == '*':
                    pass
                elif instruction[3] == '/':
                    pass
                elif instruction[3] == '%':
                    pass                    
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], int) and isinstance(instruction[5], str):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                    if instruction[5] in var.values():
                        variable2 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[4]:
                            variable3 = var        
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
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
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable3['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[3] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[3] == '-':
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.GET.value + " " + "c")
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[3] == '*':
                    pass
                elif instruction[3] == '/':
                    pass
                elif instruction[3] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], str) and isinstance(instruction[5], int):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                    if instruction[2] in var.values():
                        variable2 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[4]:
                            variable3 = var                   
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable2, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[5] + variable3['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                if instruction[3] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[3] == '-':
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.GET.value + " " + "c")
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[3] == '*':
                    pass
                elif instruction[3] == '/':
                    pass
                elif instruction[3] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[2], str) and isinstance(instruction[5], str):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                    if instruction[2] in var.values():
                        variable2 = var
                    if instruction[5] in var.values():
                        variable3 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[4]:
                            variable4 = var                    
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable2, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable3, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable4['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")                    
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[3] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[3] == '-':
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.GET.value + " " + "c")
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[3] == '*':
                    pass
                elif instruction[3] == '/':
                    pass
                elif instruction[3] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

        elif instruction[4] in ['+', '-', '*', '/', '%']:
            if isinstance(instruction[3], int) and isinstance(instruction[5], int):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[2]:
                            variable2 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory = variable1['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[5], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[3] + variable2['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")
                    
            elif isinstance(instruction[3], int) and isinstance(instruction[5], str):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                    if instruction[5] in var.values():
                        variable2 = var   
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[2]:
                            variable3 = var                      
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable2, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[3] + variable3['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[3], str) and isinstance(instruction[5], int):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                    if instruction[3] in var.values():
                        variable2 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[2]:
                            variable3 = var                      
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[5], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable3['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[3], str) and isinstance(instruction[5], str):
                for var in self.main_program_variables:
                    if instruction[0] in var.values():
                        variable1 = var
                    if instruction[5] in var.values():
                        variable2 = var
                    if instruction[3] in var.values():
                        variable3 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[2]:
                            variable4 = var                     
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable1 = variable1['place_in_memory']
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable2, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable3, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable4['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")                    
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toIntegerVariableAssignBinaryOperationOfTwoArraysVariables(self, instruction):
        assembly_code = []
        if isinstance(instruction[3], int) and isinstance(instruction[6], int):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[2]:
                        variable2 = var  
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[5]:
                        variable3 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory = variable1['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(instruction[3] + variable2['starts_at'], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(instruction[6] + variable3['starts_at'], "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.LOAD.value + " " + "c")
            if instruction[4] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "b")
            elif instruction[4] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "b")
            elif instruction[4] == '*':
                pass
            elif instruction[4] == '/':
                pass
            elif instruction[4] == '%':
                pass 
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[3], int) and isinstance(instruction[6], str):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                if instruction[6] in var.values():
                    variable2 = var
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[2]:
                        variable3 = var  
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[5]:
                        variable4 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable1 = variable1['place_in_memory']
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(instruction[3] + variable3['starts_at'], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(place_in_memory_of_variable2, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "c")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable4['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b")                    
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            if instruction[4] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[4] == '-':
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.GET.value + " " + "c")
                assembly_code.append(Instructions.SUB.value + " " + "b")
            elif instruction[4] == '*':
                pass
            elif instruction[4] == '/':
                pass
            elif instruction[4] == '%':
                pass 
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[3], str) and isinstance(instruction[6], int):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                if instruction[3] in var.values():
                    variable2 = var
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[2]:
                        variable3 = var  
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[5]:
                        variable4 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable1 = variable1['place_in_memory']
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(instruction[6] + variable4['starts_at'], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(place_in_memory_of_variable2, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "c")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable3['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b")
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            if instruction[4] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[4] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "c")
            elif instruction[4] == '*':
                pass
            elif instruction[4] == '/':
                pass
            elif instruction[4] == '%':
                pass 
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[3], str) and isinstance(instruction[6], str):
            for var in self.main_program_variables:
                if instruction[0] in var.values():
                    variable1 = var
                if instruction[3] in var.values():
                    variable2 = var
                if instruction[6] in var.values():
                    variable3 = var
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[2]:
                        variable4 = var  
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[5]:
                        variable5 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable1 = variable1['place_in_memory']
            place_in_memory_of_variable2 = variable2['place_in_memory']
            place_in_memory_of_variable3 = variable3['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(place_in_memory_of_variable3, "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(place_in_memory_of_variable2, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "c")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable5['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "c")                
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.PUT.value + " " + "c")

            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable4['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b")
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            if instruction[4] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[4] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "c")
            elif instruction[4] == '*':
                pass
            elif instruction[4] == '/':
                pass
            elif instruction[4] == '%':
                pass 
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

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
            ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
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
                if instruction[3] in var.values():
                    variable2 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
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
                if instruction[1] in var.values():
                    variable2 = var
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
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable1['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b") 
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.GET.value + " " + "c")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[1], str) and isinstance(instruction[3], str):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable1 = var
                if instruction[1] in var.values():
                    variable2 = var
                if instruction[3] in var.values():
                    variable3 = var
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
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable1['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b") 
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.LOAD.value + " " + "c")
            assembly_code.append(Instructions.STORE.value + " " + "b")  

        return assembly_code

    def toArrayVariableAssignArrayVariable(self, instruction):
        assembly_code = []
        if isinstance(instruction[1], int) and isinstance(instruction[4], int):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable1 = var  
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[3]:
                        variable2 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(instruction[4] + variable2['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.STORE.value + " " + "b")
            
        elif isinstance(instruction[1], int) and isinstance(instruction[4], str):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable1 = var  
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[3]:
                        variable2 = var
                if instruction[4] in var.values():
                    variable3 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable3 = variable3['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_of_variable3, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable2['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b")                    
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[1], str) and isinstance(instruction[4], int):
            for var in self.main_program_variables:
                if instruction[1] in var.values():
                    variable1 = var
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable2 = var  
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[3]:
                        variable3 = var
            if variable2['initialized'] == False:
                variable2['initialized'] = True
            place_in_memory_of_variable1 = variable1['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable2['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[4] + variable3['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[1], str) and isinstance(instruction[4], str):
            for var in self.main_program_variables:
                if instruction[1] in var.values():
                    variable1 = var
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[0]:
                        variable2 = var  
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[3]:
                        variable3 = var
                if instruction[4] in var.values():
                    variable4 = var
            if variable2['initialized'] == False:
                variable2['initialized'] = True
            place_in_memory_of_variable1 = variable1['place_in_memory']
            place_in_memory_of_variable4 = variable4['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable2['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_of_variable4, "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(variable3['starts_at'], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "c")
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toArrayVariableAssignBinaryOperationOfTwoIntegerVariables(self, instruction):
        assembly_code = []
        if isinstance(instruction[3], int) and isinstance(instruction[5], int):
            if isinstance(instruction[1], int):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var  
                            break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[3], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[5], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[1], str):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var  
                    if instruction[1] in var.values():
                        variable2 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[3], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[5], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(place_in_memory_of_variable2, "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable1['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)             
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")  
                assembly_code.append(Instructions.GET.value + " " + "c")       
                assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[3], int) and isinstance(instruction[5], str):
            if isinstance(instruction[1], int):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var  
                    if instruction[5] in var.values():
                        variable2 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[3], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[1], str):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var  
                    if instruction[1] in var.values():
                        variable2 = var
                    if instruction[5] in var.values():
                        variable3 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable3, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b") 
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[3], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)   
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(place_in_memory_of_variable2, "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable1['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)             
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")  
                assembly_code.append(Instructions.GET.value + " " + "c")       
                assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[3], str) and isinstance(instruction[5], int):
            if isinstance(instruction[1], int):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var  
                    if instruction[3] in var.values():
                        variable2 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[5], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[1], str):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var  
                    if instruction[1] in var.values():
                        variable2 = var
                    if instruction[3] in var.values():
                        variable3 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[5], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable3, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")    
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(place_in_memory_of_variable2, "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable1['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)             
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")  
                assembly_code.append(Instructions.GET.value + " " + "c")       
                assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[3], str) and isinstance(instruction[5], str):
            if isinstance(instruction[1], int):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var  
                    if instruction[3] in var.values():
                        variable2 = var
                    if instruction[5] in var.values():
                        variable3 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable3, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[1], str):
                for var in self.main_program_variables:    
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var  
                    if instruction[1] in var.values():
                        variable2 = var
                    if instruction[3] in var.values():
                        variable3 = var
                    if instruction[5] in var.values():
                        variable4 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                place_in_memory_of_variable4 = variable4['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable4, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable3, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass 
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(place_in_memory_of_variable2, "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable1['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)             
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")  
                assembly_code.append(Instructions.GET.value + " " + "c")       
                assembly_code.append(Instructions.STORE.value + " " + "b")
                  
        return assembly_code

    def toArrayVariableAssignBinaryOperationOfIntegerAndArrayVariables(self, instruction):
        assembly_code = []
        if instruction[4] in ['+', '-', '*', '/', '%']:
            if isinstance(instruction[1], int):
                if isinstance(instruction[3], int) and isinstance(instruction[6], int):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[5]:
                                variable2 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[1] + variable1['starts_at'], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generate_number(instruction[6] + variable2['starts_at'], "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)                        
                    if instruction[4] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[4] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[4] == '*':
                        pass
                    elif instruction[4] == '/':
                        pass
                    elif instruction[4] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")                       

                elif isinstance(instruction[3], int) and isinstance(instruction[6], str):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[5]:
                                variable2 = var
                        if instruction[6] in var.values():
                            variable3 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[1] + variable1['starts_at'], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generate_number(place_in_memory_of_variable3, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                    assembly_code.append(Instructions.LOAD.value + " " + "a")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)                        
                    if instruction[4] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[4] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[4] == '*':
                        pass
                    elif instruction[4] == '/':
                        pass
                    elif instruction[4] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")

                elif isinstance(instruction[3], str) and isinstance(instruction[6], int):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[5]:
                                variable2 = var
                        if instruction[3] in var.values():
                            variable3 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[1] + variable1['starts_at'], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generate_number(instruction[6] + variable2['starts_at'], "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(place_in_memory_of_variable3, "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)       
                    assembly_code.append(Instructions.LOAD.value + " " + "a")                 
                    if instruction[4] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[4] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[4] == '*':
                        pass
                    elif instruction[4] == '/':
                        pass
                    elif instruction[4] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")

                elif isinstance(instruction[3], str) and isinstance(instruction[6], str):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[5]:
                                variable2 = var
                        if instruction[3] in var.values():
                            variable3 = var
                        if instruction[6] in var.values():
                            variable4 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    place_in_memory_of_variable4 = variable4['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[1] + variable1['starts_at'], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generate_number(place_in_memory_of_variable4, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                    assembly_code.append(Instructions.LOAD.value + " " + "a")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(place_in_memory_of_variable3, "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)       
                    assembly_code.append(Instructions.LOAD.value + " " + "a")                 
                    if instruction[4] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[4] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[4] == '*':
                        pass
                    elif instruction[4] == '/':
                        pass
                    elif instruction[4] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")   

            elif isinstance(instruction[1], str):
                if isinstance(instruction[3], int) and isinstance(instruction[6], int):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[5]:
                                variable2 = var
                        if instruction[1] in var.values():
                            variable3 = var                                    
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable3, "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable1['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")                        
                    ins = self.generate_number(instruction[6] + variable2['starts_at'], "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)                        
                    if instruction[4] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[4] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[4] == '*':
                        pass
                    elif instruction[4] == '/':
                        pass
                    elif instruction[4] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")   

                elif isinstance(instruction[3], int) and isinstance(instruction[6], str):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[5]:
                                variable2 = var
                        if instruction[6] in var.values():
                            variable3 = var
                        if instruction[1] in var.values():
                            variable4 = var 
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    place_in_memory_of_variable4 = variable4['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable4, "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable1['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c") 
                    ins = self.generate_number(place_in_memory_of_variable3, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                    assembly_code.append(Instructions.LOAD.value + " " + "a")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)                        
                    if instruction[4] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[4] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[4] == '*':
                        pass
                    elif instruction[4] == '/':
                        pass
                    elif instruction[4] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")

                elif isinstance(instruction[3], str) and isinstance(instruction[6], int):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[5]:
                                variable2 = var
                        if instruction[3] in var.values():
                            variable3 = var
                        if instruction[1] in var.values():
                            variable4 = var 
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    place_in_memory_of_variable4 = variable4['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable4, "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable1['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c") 
                    ins = self.generate_number(instruction[6] + variable2['starts_at'], "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(place_in_memory_of_variable3, "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)       
                    assembly_code.append(Instructions.LOAD.value + " " + "a")                 
                    if instruction[4] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[4] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[4] == '*':
                        pass
                    elif instruction[4] == '/':
                        pass
                    elif instruction[4] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")

                elif isinstance(instruction[3], str) and isinstance(instruction[6], str):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[5]:
                                variable2 = var
                        if instruction[3] in var.values():
                            variable3 = var
                        if instruction[6] in var.values():
                            variable4 = var
                        if instruction[1] in var.values():
                            variable5 = var 
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    place_in_memory_of_variable4 = variable4['place_in_memory']
                    place_in_memory_of_variable5 = variable5['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable5, "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable1['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c") 
                    ins = self.generate_number(place_in_memory_of_variable4, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                    assembly_code.append(Instructions.LOAD.value + " " + "a")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(place_in_memory_of_variable3, "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)       
                    assembly_code.append(Instructions.LOAD.value + " " + "a")                 
                    if instruction[4] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[4] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[4] == '*':
                        pass
                    elif instruction[4] == '/':
                        pass
                    elif instruction[4] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")   


        elif instruction[5] in ['+', '-', '*', '/', '%']:
            if isinstance(instruction[1], int):
                if isinstance(instruction[4], int) and isinstance(instruction[6], int):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[3]:
                                variable2 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[1] + variable1['starts_at'], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generate_number(instruction[6], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins) 
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[4] + variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "a")
                    if instruction[5] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[5] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[5] == '*':
                        pass
                    elif instruction[5] == '/':
                        pass
                    elif instruction[5] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")  

                elif isinstance(instruction[4], int) and isinstance(instruction[6], str):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[3]:
                                variable2 = var
                        if instruction[6] in var.values():
                            variable3 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[1] + variable1['starts_at'], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generate_number(place_in_memory_of_variable3, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[4] + variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)     
                    assembly_code.append(Instructions.LOAD.value + " " + "a")                 
                    if instruction[5] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[5] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[5] == '*':
                        pass
                    elif instruction[5] == '/':
                        pass
                    elif instruction[5] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")

                elif isinstance(instruction[4], str) and isinstance(instruction[6], int):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[3]:
                                variable2 = var
                        if instruction[4] in var.values():
                            variable3 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[6], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    ins = self.generate_number(place_in_memory_of_variable3, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                    assembly_code.append(Instructions.LOAD.value + " " + "a")   
                    if instruction[5] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "c")
                    elif instruction[5] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "c")
                    elif instruction[5] == '*':
                        pass
                    elif instruction[5] == '/':
                        pass
                    elif instruction[5] == '%':
                        pass
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[1] + variable1['starts_at'], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.STORE.value + " " + "c")

                elif isinstance(instruction[4], str) and isinstance(instruction[6], str):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[3]:
                                variable2 = var
                        if instruction[6] in var.values():
                            variable3 = var
                        if instruction[4] in var.values():
                            variable4 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    place_in_memory_of_variable4 = variable4['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable3, "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins) 
                    assembly_code.append(Instructions.LOAD.value + " " + "a")
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    ins = self.generate_number(place_in_memory_of_variable4, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                    assembly_code.append(Instructions.LOAD.value + " " + "a")    
                    if instruction[5] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "c")
                    elif instruction[5] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "c")
                    elif instruction[5] == '*':
                        pass
                    elif instruction[5] == '/':
                        pass
                    elif instruction[5] == '%':
                        pass
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[1] + variable1['starts_at'], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.STORE.value + " " + "c")

            elif isinstance(instruction[1], str):
                if isinstance(instruction[4], int) and isinstance(instruction[6], int):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[3]:
                                variable2 = var
                        if instruction[1] in var.values():
                            variable3 = var     
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable3, "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable1['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[6], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins) 
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[4] + variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "a")
                    if instruction[5] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[5] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[5] == '*':
                        pass
                    elif instruction[5] == '/':
                        pass
                    elif instruction[5] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")                

                elif isinstance(instruction[4], int) and isinstance(instruction[6], str):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[3]:
                                variable2 = var
                        if instruction[6] in var.values():
                            variable3 = var
                        if instruction[1] in var.values():
                            variable4 = var
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    place_in_memory_of_variable4 = variable4['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable4, "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable1['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable3, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[4] + variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)     
                    assembly_code.append(Instructions.LOAD.value + " " + "a")                 
                    if instruction[5] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "b")
                    elif instruction[5] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "b")
                    elif instruction[5] == '*':
                        pass
                    elif instruction[5] == '/':
                        pass
                    elif instruction[5] == '%':
                        pass
                    assembly_code.append(Instructions.STORE.value + " " + "c")

                elif isinstance(instruction[4], str) and isinstance(instruction[6], int):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[3]:
                                variable2 = var
                        if instruction[4] in var.values():
                            variable3 = var
                        if instruction[1] in var.values():
                            variable4 = var 
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    place_in_memory_of_variable4 = variable4['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[6], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    ins = self.generate_number(place_in_memory_of_variable3, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                    assembly_code.append(Instructions.LOAD.value + " " + "a")   
                    if instruction[5] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "c")
                    elif instruction[5] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "c")
                    elif instruction[5] == '*':
                        pass
                    elif instruction[5] == '/':
                        pass
                    elif instruction[5] == '%':
                        pass
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable4, "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable1['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.STORE.value + " " + "c")

                elif isinstance(instruction[4], str) and isinstance(instruction[6], str):
                    for var in self.main_program_variables:
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[0]:
                                variable1 = var  
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == instruction[3]:
                                variable2 = var
                        if instruction[6] in var.values():
                            variable3 = var
                        if instruction[4] in var.values():
                            variable4 = var
                        if instruction[1] in var.values():
                            variable5 = var 
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    place_in_memory_of_variable3 = variable3['place_in_memory']
                    place_in_memory_of_variable4 = variable4['place_in_memory']
                    place_in_memory_of_variable5 = variable5['place_in_memory']
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable3, "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins) 
                    assembly_code.append(Instructions.LOAD.value + " " + "a")
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    ins = self.generate_number(place_in_memory_of_variable4, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable2['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                    assembly_code.append(Instructions.LOAD.value + " " + "a")    
                    if instruction[5] == '+':
                        assembly_code.append(Instructions.ADD.value + " " + "c")
                    elif instruction[5] == '-':
                        assembly_code.append(Instructions.SUB.value + " " + "c")
                    elif instruction[5] == '*':
                        pass
                    elif instruction[5] == '/':
                        pass
                    elif instruction[5] == '%':
                        pass
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(place_in_memory_of_variable5, "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(variable1['starts_at'], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.STORE.value + " " + "c")

        return assembly_code

    def toArrayVariableAssignBinaryOperationOfTwoArraysVariables(self, instruction):
        assembly_code = []
        if isinstance(instruction[1], int):
            if isinstance(instruction[4], int) and isinstance(instruction[7], int):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var 
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[3]:
                            variable2 = var  
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[6]:
                            variable3 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[4] + variable2['starts_at'], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[7] + variable3['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[4], int) and isinstance(instruction[7], str):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var 
                    if instruction[7] in var.values():
                        variable2 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[3]:
                            variable3 = var  
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[6]:
                            variable4 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[4] + variable3['starts_at'], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable4['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")                    
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.GET.value + " " + "c")
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[4], str) and isinstance(instruction[7], int):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var 
                    if instruction[4] in var.values():
                        variable2 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[3]:
                            variable3 = var  
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[6]:
                            variable4 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[7] + variable4['starts_at'], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable3['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

            elif isinstance(instruction[4], str) and isinstance(instruction[7], str):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var 
                    if instruction[4] in var.values():
                        variable2 = var
                    if instruction[7] in var.values():
                        variable3 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[3]:
                            variable4 = var  
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[6]:
                            variable5 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable3, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable5['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "c")                
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                assembly_code.append(Instructions.PUT.value + " " + "c")

                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable4['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass 
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[1] + variable1['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[1], str):
            if isinstance(instruction[4], int) and isinstance(instruction[7], int):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var 
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[3]:
                            variable2 = var  
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[6]:
                            variable3 = var
                    if instruction[1] in var.values():
                            variable4 = var  
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable4 = variable4['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[4] + variable2['starts_at'], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[7] + variable3['starts_at'], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "b")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass 
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable4, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable1['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.GET.value + " " + "b")
                assembly_code.append(Instructions.STORE.value + " " + "c")

            elif isinstance(instruction[4], int) and isinstance(instruction[7], str):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var 
                    if instruction[7] in var.values():
                        variable2 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[3]:
                            variable3 = var  
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[6]:
                            variable4 = var
                    if instruction[1] in var.values():
                        variable5 = var 
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable5 = variable5['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[4] + variable3['starts_at'], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable4['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")                    
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.GET.value + " " + "c")
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass 
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable5, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable1['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.GET.value + " " + "b")
                assembly_code.append(Instructions.STORE.value + " " + "c")

            elif isinstance(instruction[4], str) and isinstance(instruction[7], int):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var 
                    if instruction[4] in var.values():
                        variable2 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[3]:
                            variable3 = var  
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[6]:
                            variable4 = var
                    if instruction[1] in var.values():
                        variable5 = var                             
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable5 = variable5['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[7] + variable4['starts_at'], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable3['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass 
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable5, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable1['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.GET.value + " " + "b")
                assembly_code.append(Instructions.STORE.value + " " + "c")

            elif isinstance(instruction[4], str) and isinstance(instruction[7], str):
                for var in self.main_program_variables:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[0]:
                            variable1 = var 
                    if instruction[4] in var.values():
                        variable2 = var
                    if instruction[7] in var.values():
                        variable3 = var
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[3]:
                            variable4 = var  
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction[6]:
                            variable5 = var
                    if instruction[1] in var.values():
                        variable6 = var                            
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                place_in_memory_of_variable2 = variable2['place_in_memory']
                place_in_memory_of_variable3 = variable3['place_in_memory']
                place_in_memory_of_variable6 = variable6['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable3, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(place_in_memory_of_variable2, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable5['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "c")                
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                assembly_code.append(Instructions.PUT.value + " " + "c")

                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable4['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "b")
                assembly_code.append(Instructions.LOAD.value + " " + "a")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "c")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass 
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(place_in_memory_of_variable6, "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(variable1['starts_at'], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code.append(Instructions.GET.value + " " + "b")
                assembly_code.append(Instructions.STORE.value + " " + "c")

        return assembly_code
    
    def writeIntegerVariable(self, instruction):
        assembly_code = []
        if isinstance(instruction[1], int):
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[1], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.WRITE.value)

        elif isinstance(instruction[1], str):
            for var in self.main_program_variables:
                if instruction[1] in var.values():
                    variable1 = var
            place_in_memory_of_variable1 = variable1['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_of_variable1, "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.WRITE.value)

        return assembly_code

    def writeArrayVariable(self, instruction):
        assembly_code = []
        if isinstance(instruction[2], int):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[1]:
                        variable1 = var
            place_in_memory_of_variable1 = variable1['starts_at']
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[2] + place_in_memory_of_variable1, "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.WRITE.value)
            
        elif isinstance(instruction[2], str):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[1]:
                        variable1 = var
                if instruction[2] in var.values():
                    variable2 = var                        
            place_in_memory_of_variable1 = variable1['starts_at']
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generate_number(place_in_memory_of_variable2, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_of_variable1, "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b")
            assembly_code.append(Instructions.LOAD.value + " " + "a")
            assembly_code.append(Instructions.WRITE.value)

        return assembly_code

    def readToIntegerVariable(self, instruction):
        assembly_code = []
        for var in self.main_program_variables:
            if instruction[1] in var.values():
                variable1 = var
        if variable1['initialized'] == False:
            variable1['initialized'] = True
        place_in_memory_of_variable1 = variable1['place_in_memory']
        assembly_code.append(Instructions.RST.value + " " + "b")
        assembly_code.append(Instructions.RST.value + " " + "a")
        ins = self.generate_number(place_in_memory_of_variable1, "b")
        if len(ins) != 0:   
            assembly_code.extend(ins)
        assembly_code.append(Instructions.READ.value)
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def readToArrayVariable(self, instruction):
        assembly_code = []
        if isinstance(instruction[2], int):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[1]:
                        variable1 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable1 = variable1['starts_at']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[2] + place_in_memory_of_variable1, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.READ.value)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[2], str):
            for var in self.main_program_variables:
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == instruction[1]:
                        variable1 = var
                if instruction[2] in var.values():
                    variable2 = var
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory_of_variable1 = variable1['starts_at']
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_of_variable2, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_of_variable1, "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.ADD.value + " " + "b") 
            assembly_code.append(Instructions.PUT.value + " " + "b")   
            assembly_code.append(Instructions.READ.value)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def checkConditionForTwoIntegerVariables(self, instruction, block):
        assembly_code = []
        if isinstance(instruction[0], int) and isinstance(instruction[2], int):

            if instruction[1] == '=':
                pass
            elif instruction[1] == '<':
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.SUB.value + " " + "b")    
                if 'second_jump' in block:
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))  
                    assembly_code.append("block " + str(block['first_jump']))
                else:
                    assembly_code.append("block " + str(block['first_jump']))  
                    assembly_code.append(Instructions.HALT.value)   
            elif instruction[1] == '>':
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.SUB.value + " " + "b")    
                if 'second_jump' in block:
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append("block " + str(block['first_jump'])) 
                else:
                    assembly_code.append("block " + str(block['first_jump']))  
                    assembly_code.append(Instructions.HALT.value) 
            elif instruction[1] == '<=':
                pass
            elif instruction[1] == '>=':
                pass
            elif instruction[1] == '!=':
                pass

        if isinstance(instruction[0], int) and isinstance(instruction[2], str):
            if instruction[1] == '=':
                pass
            elif instruction[1] == '<':
                for var in self.main_program_variables:
                    if instruction[2] in var.values():
                        variable1 = var
                place_in_memory_of_variable1 = variable1['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b") 
                assembly_code.append(Instructions.RST.value + " " + "a")   
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.SUB.value + " " + "b")    
                if 'second_jump' in block:
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))  
                    assembly_code.append("block " + str(block['first_jump']))
                else:
                    assembly_code.append("block " + str(block['first_jump']))  
                    assembly_code.append(Instructions.HALT.value)   
            elif instruction[1] == '>':
                for var in self.main_program_variables:
                    if instruction[2] in var.values():
                        variable1 = var
                place_in_memory_of_variable1 = variable1['place_in_memory']
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(place_in_memory_of_variable1, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "b") 
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.SUB.value + " " + "b")    
                if 'second_jump' in block:
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append("block " + str(block['first_jump'])) 
                else:
                    assembly_code.append("block " + str(block['first_jump']))  
                    assembly_code.append(Instructions.HALT.value)
            elif instruction[1] == '<=':
                pass
            elif instruction[1] == '>=':
                pass
            elif instruction[1] == '!=':
                pass

        if isinstance(instruction[0], str) and isinstance(instruction[2], int):
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

        if isinstance(instruction[0], str) and isinstance(instruction[2], str):
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
        return assembly_code

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
