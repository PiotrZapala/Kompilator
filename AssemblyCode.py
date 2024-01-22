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
        self.program_variables = {}
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
        self.getAssemblyCodeFromProgramBlocks()

    def getAssemblyCodeFromProgramBlocks(self):
        program = []
        main_variables = []
        procedure_variables = []
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
            main_variables.append(variable)
        self.program_variables['main'] = main_variables
        for j in range(len(self.declarations_in_procedures)):
            proc_decl = []
            for i in range(len(self.declarations_in_procedures[j])):
                variable = {}
                if isinstance(self.declarations_in_procedures[j][i]['identifier'], str):
                    variable['variable_'+str(i+1)] = self.declarations_in_procedures[j][i]['identifier']
                    variable['initialized'] = False
                    variable['place_in_memory'] = self.global_space_counter
                    self.global_space_counter += 1
                elif isinstance(self.declarations_in_procedures[j][i]['identifier'], dict):
                    variable['variable_'+str(i+1)] = (self.declarations_in_procedures[j][i]['identifier']['identifier'], self.declarations_in_procedures[j][i]['identifier']['range'])
                    variable['initialized'] = False
                    variable['starts_at'] = self.global_space_counter
                    variable['ends_at'] = self.declarations_in_procedures[j][i]['identifier']['range'] + self.global_space_counter - 1
                    self.global_space_counter = self.global_space_counter + self.declarations_in_procedures[j][i]['identifier']['range']              
                proc_decl.extend([variable])
            proc_head = []
            for i in range(len(self.procedures_head[j]['arguments declarations'])):
                variable = {}
                variable['variable_'+str(i+1)] = self.procedures_head[j]['arguments declarations'][i]['argument']['identifier']
                variable['is_array'] = self.procedures_head[j]['arguments declarations'][i]['argument']['isArray']
                variable['place_in_memory'] = self.global_space_counter
                self.global_space_counter += 1
                proc_head.extend([variable])
            procedure_variables.append(proc_decl)
            procedure_variables.append(proc_head)
            type = self.procedures_head[j]['procedure identifier']
            self.program_variables[type] = procedure_variables
            procedure_variables = []

        for i in range(len(self.procedures_basic_blocks)):
            type = self.procedures_head[i]['procedure identifier']
            for block in self.procedures_basic_blocks[i]:
                assembly_code_for_one_block = self.identifyTypeOfInstructions(block, type)
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
            for block in self.procedures_basic_blocks[i]:
                program.append(block['instructions'][0])
        for block in self.program_basic_blocks[0]:
            assembly_code_for_one_block = self.identifyTypeOfInstructions(block, 'main')
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
    
    def identifyTypeOfInstructions(self, block, type):
        block_instructions = block['instructions']
        assembly_code_for_one_block = []
        for instruction in block_instructions:
            if ':=' in instruction:
                if instruction[1] == ':=':
                    assembly_code = self.assignToIntegerVariable(instruction, type)
                elif instruction[2] == ':=':
                    assembly_code = self.assignToArrayVariable(instruction, type)
            elif 'Write' in instruction:
                if len(instruction) == 2:
                    assembly_code = self.writeIntegerVariable(instruction, type)
                elif len(instruction) == 3:
                    assembly_code = self.writeArrayVariable(instruction, type)
            elif 'Read' in instruction:
                if len(instruction) == 2:
                    assembly_code = self.readToIntegerVariable(instruction, type)
                elif len(instruction) == 3:
                    assembly_code = self.readToArrayVariable(instruction, type)
            elif 'ProcCall' in instruction:
                assembly_code = self.callProcedure(instruction, type)                
            else:
                if len(instruction) == 3:
                    assembly_code = self.checkConditionForTwoIntegerVariables(instruction, type, block)
                elif len(instruction) == 4:
                    assembly_code = self.checkConditionForIntegerAndArrayVariables(instruction, type, block)
                elif len(instruction) == 5:
                    assembly_code = self.checkConditionForTwoArrayVariables(instruction, type, block)
            assembly_code_for_one_block.append(assembly_code)
        return assembly_code_for_one_block
    

    def assignToIntegerVariable(self, instruction, type):
        if len(instruction) == 3:
            assembly_code = self.toIntegerVariableAssignIntegerVariable(instruction, type)
        elif len(instruction) == 4:
            assembly_code = self.toIntegerVariableAssignArrayVariable(instruction, type)  
        elif len(instruction) == 5:
            assembly_code = self.toIntegerVariableAssignBinaryOperationOfTwoIntegerVariables(instruction, type)
        elif len(instruction) == 6:
            assembly_code = self.toIntegerVariableAssignBinaryOperationOfIntegerAndArrayVariables(instruction, type)
        elif len(instruction) == 7:
            assembly_code = self.toIntegerVariableAssignBinaryOperationOfTwoArraysVariables(instruction, type)

        return assembly_code

    def assignToArrayVariable(self, instruction, type):
        if len(instruction) == 4:
            assembly_code = self.toArrayVariableAssignIntegerVariable(instruction, type)
        elif len(instruction) == 5:
            assembly_code = self.toArrayVariableAssignArrayVariable(instruction, type)  
        elif len(instruction) == 6:
            assembly_code = self.toArrayVariableAssignBinaryOperationOfTwoIntegerVariables(instruction, type)
        elif len(instruction) == 7:
            assembly_code = self.toArrayVariableAssignBinaryOperationOfIntegerAndArrayVariables(instruction, type)
        elif len(instruction) == 8:
            assembly_code = self.toArrayVariableAssignBinaryOperationOfTwoArraysVariables(instruction, type)

        return assembly_code
    
    def createAssemblyWhichStoresToIntegerVariable(self, instruction, type, assembly_code, register):
        if type == 'main':
            for var in self.program_variables[type]:
                if instruction in var.values():
                    variable1 = var
                    break
            if variable1['initialized'] == False:
                variable1['initialized'] = True
            place_in_memory = variable1['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + register)
            ins = self.generate_number(place_in_memory, register)
            if len(ins) != 0:   
                assembly_code.extend(ins)
        else:
            for var in self.program_variables[type][0]:
                if instruction in var.values():
                    variable1 = var
                    is_from_head = False
            for var in self.program_variables[type][1]:
                if instruction in var.values():
                    variable1 = var
                    is_from_head = True
            place_in_memory = variable1['place_in_memory']
            if is_from_head == False:
                if variable1['initialized'] == False:
                    variable1['initialized'] = True 
                assembly_code.append(Instructions.RST.value + " " + register)
                ins = self.generate_number(place_in_memory, register)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
            else:
                assembly_code.append(Instructions.RST.value + " " + register)
                ins = self.generate_number(place_in_memory, register)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register)  
                assembly_code.append(Instructions.PUT.value + " " + register)                        
        return assembly_code
    
    def createAssemblyWhichGetsIntegerVariableFromMemory(self, instruction, type, assembly_code, register1, register2):
        if type == 'main':
            for var in self.program_variables[type]:
                if instruction in var.values():
                    variable2 = var
            place_in_memory_of_variable2 = variable2['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + register1)
            assembly_code.append(Instructions.RST.value + " " + register2)
            ins = self.generate_number(place_in_memory_of_variable2, register2)
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.LOAD.value + " " + register2)
        else:
            for var in self.program_variables[type][0]:
                if instruction in var.values():
                    variable2 = var
                    is_from_head = False
            for var in self.program_variables[type][1]:
                if instruction in var.values():
                    variable2 = var
                    is_from_head = True
            place_in_memory_of_variable2 = variable2['place_in_memory']
            if is_from_head == False:
                assembly_code.append(Instructions.RST.value + " " + register1)
                assembly_code.append(Instructions.RST.value + " " + register2)
                ins = self.generate_number(place_in_memory_of_variable2, register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register2)
                assembly_code.append(Instructions.PUT.value + " " + register2)
            else:
                assembly_code.append(Instructions.RST.value + " " + register1)
                assembly_code.append(Instructions.RST.value + " " + register2)
                ins = self.generate_number(place_in_memory_of_variable2, register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register2)
                assembly_code.append(Instructions.LOAD.value + " " + register1)
        return assembly_code

    def createAssemblyWhichStoresToArrayVariable(self, instruction, index, type, assembly_code, register1, register2):
        if type == 'main':
            if isinstance(index, int):
                for var in self.program_variables[type]:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction:
                            variable1 = var
                            break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                assembly_code.append(Instructions.RST.value + " " + register2)
                ins = self.generate_number(index + variable1['starts_at'], register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
            elif isinstance(index, str):
                for var in self.program_variables[type]:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction:
                            variable1 = var
                    if index in var.values():
                        variable2 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                assembly_code.append(Instructions.RST.value + " " + register1)
                assembly_code.append(Instructions.RST.value + " " + register2)
                ins = self.generate_number(variable2['place_in_memory'], register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register2)
                assembly_code.append(Instructions.PUT.value + " " + register2)
                assembly_code.append(Instructions.RST.value + " " + register1)
                ins = self.generate_number(variable1['starts_at'], register1)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + register2) 
                assembly_code.append(Instructions.PUT.value + " " + register2)

        else:
            if isinstance(index, int):
                for var in self.program_variables[type][0]:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction:
                            variable1 = var
                            is_from_head = False
                for var in self.program_variables[type][1]:
                    if instruction in var.values() and var['is_array'] == True:
                        variable1 = var
                        is_from_head = True
                if is_from_head == False:
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(index + variable1['starts_at'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                else:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generate_number(index, register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.PUT.value + " " + register2)
            elif isinstance(index, str):
                for var in self.program_variables[type][0]:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction:
                            variable1 = var
                            is_identifier_from_head = False
                    if index in var.values():
                        variable2 = var
                        is_index_from_head = False
                for var in self.program_variables[type][1]:
                    if instruction in var.values() and var['is_array'] == True:
                        variable1 = var
                        is_identifier_from_head = True
                    if index in var.values():
                        variable2 = var
                        is_index_from_head = True

                if is_identifier_from_head == False and is_index_from_head == False:
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable2['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generate_number(variable1['starts_at'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + register2) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == False and is_index_from_head == True:
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable1['starts_at'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generate_number(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.ADD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == True and is_index_from_head == False:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generate_number(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == True and is_index_from_head == True:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generate_number(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.LOAD.value + " " + register1)    
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.PUT.value + " " + register2)                    

        return assembly_code

    def createAssemblyWhichGetsArrayVariableFromMemory(self, instruction, index, type, assembly_code, register1, register2):
        if type == 'main':
            if isinstance(index, int):
                for var in self.program_variables[type]:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction:
                            variable1 = var
                            break
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                assembly_code.append(Instructions.RST.value + " " + register1)    
                assembly_code.append(Instructions.RST.value + " " + register2)
                ins = self.generate_number(index + variable1['starts_at'], register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register2) 
                assembly_code.append(Instructions.PUT.value + " " + register2)    
            elif isinstance(index, str):
                for var in self.program_variables[type]:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction:
                            variable1 = var
                    if index in var.values():
                        variable2 = var
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                assembly_code.append(Instructions.RST.value + " " + register1)
                assembly_code.append(Instructions.RST.value + " " + register2)
                ins = self.generate_number(variable2['place_in_memory'], register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register2)
                assembly_code.append(Instructions.PUT.value + " " + register2)
                assembly_code.append(Instructions.RST.value + " " + register1)
                ins = self.generate_number(variable1['starts_at'], register1)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.ADD.value + " " + register2)
                assembly_code.append(Instructions.LOAD.value + " " + register1) 
                assembly_code.append(Instructions.PUT.value + " " + register2)

        else:
            if isinstance(index, int):
                for var in self.program_variables[type][0]:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction:
                            variable1 = var
                            is_from_head = False
                for var in self.program_variables[type][1]:
                    if instruction in var.values() and var['is_array'] == True:
                        variable1 = var
                        is_from_head = True
                if is_from_head == False:
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(index + variable1['starts_at'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)  
                else:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generate_number(index, register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)
            elif isinstance(index, str):
                for var in self.program_variables[type][0]:
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == instruction:
                            variable1 = var
                            is_identifier_from_head = False
                    if index in var.values():
                        variable2 = var
                        is_index_from_head = False
                for var in self.program_variables[type][1]:
                    if instruction in var.values() and var['is_array'] == True:
                        variable1 = var
                        is_identifier_from_head = True
                    if index in var.values():
                        variable2 = var
                        is_index_from_head = True

                if is_identifier_from_head == False and is_index_from_head == False:
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable2['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generate_number(variable1['starts_at'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + register2) 
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == False and is_index_from_head == True:
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable1['starts_at'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generate_number(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.ADD.value + " " + register2)
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == True and is_index_from_head == False:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generate_number(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == True and is_index_from_head == True:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generate_number(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generate_number(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.LOAD.value + " " + register1)    
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)                    

        return assembly_code

    def toIntegerVariableAssignIntegerVariable(self, instruction, type):
        assembly_code = []
        if isinstance(instruction[2], int):
            assembly_code = self.createAssemblyWhichStoresToIntegerVariable(instruction[0], type, assembly_code, "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.extend(self.generate_number(instruction[2], "a"))
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[2], str):
            assembly_code = self.createAssemblyWhichStoresToIntegerVariable(instruction[0], type, assembly_code, "c")
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.STORE.value + " " + "c")

        return assembly_code

    def toIntegerVariableAssignArrayVariable(self, instruction, type):
        assembly_code = []
        assembly_code = self.createAssemblyWhichStoresToIntegerVariable(instruction[0], type, assembly_code, "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.STORE.value + " " + "c")

        return assembly_code
    
    def toArrayVariableAssignIntegerVariable(self, instruction, type):
        assembly_code = []
        if isinstance(instruction[1], int) and isinstance(instruction[3], int):
            assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[3], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")
                        
        elif isinstance(instruction[1], int) and isinstance(instruction[3], str):
            assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.STORE.value + " " + "c")

        elif isinstance(instruction[1], str) and isinstance(instruction[3], int):
            assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[3], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")

        elif isinstance(instruction[1], str) and isinstance(instruction[3], str):
            assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.STORE.value + " " + "c")            

        return assembly_code

    def toArrayVariableAssignArrayVariable(self, instruction, type):
        assembly_code = []
        assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.STORE.value + " " + "c")

        return assembly_code

    def toIntegerVariableAssignBinaryOperationOfTwoIntegerVariables(self, instruction, type):
        assembly_code = []
        if isinstance(instruction[2], int) and isinstance(instruction[4], int):
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

        elif isinstance(instruction[2], int) and isinstance(instruction[4], str):
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(instruction[2], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.GET.value + " " + "c")
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

        elif isinstance(instruction[2], str) and isinstance(instruction[4], int):
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(instruction[4], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
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

        elif isinstance(instruction[2], str) and isinstance(instruction[4], str):
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
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

        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichStoresToIntegerVariable(instruction[0], type, assembly_code, "b")
        assembly_code.append(Instructions.GET.value + " " + "c")
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toIntegerVariableAssignBinaryOperationOfIntegerAndArrayVariables(self, instruction, type):
        assembly_code = []
        if instruction[3] in ['+', '-', '*', '/', '%']:
            if isinstance(instruction[2], int) and (isinstance(instruction[5], int) or isinstance(instruction[5], str)):
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[2], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[4], instruction[5], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.GET.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")
                assembly_code.append(Instructions.GET.value + " " + "c")
                if instruction[3] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "d")
                elif instruction[3] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                elif instruction[3] == '*':
                    pass
                elif instruction[3] == '/':
                    pass
                elif instruction[3] == '%':
                    pass          

            elif isinstance(instruction[2], str) and (isinstance(instruction[5], int) or isinstance(instruction[5], str)):
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[4], instruction[5], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.GET.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")
                assembly_code.append(Instructions.GET.value + " " + "c")
                if instruction[3] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "d")
                elif instruction[3] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                elif instruction[3] == '*':
                    pass
                elif instruction[3] == '/':
                    pass
                elif instruction[3] == '%':
                    pass          

        elif instruction[4] in ['+', '-', '*', '/', '%']:
            if (isinstance(instruction[3], int) or isinstance(instruction[3], str)) and isinstance(instruction[5], int):
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[5], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.GET.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "d")
                assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.GET.value + " " + "b")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "d")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass          
                    
            elif (isinstance(instruction[3], int) or isinstance(instruction[3], str)) and isinstance(instruction[5], str):
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[5], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")
                assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.GET.value + " " + "b")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "d")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass     

        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichStoresToIntegerVariable(instruction[0], type, assembly_code, "b")
        assembly_code.append(Instructions.GET.value + " " + "c")
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toIntegerVariableAssignBinaryOperationOfTwoArraysVariables(self, instruction, type):
        assembly_code = []
        assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[5], instruction[6], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.PUT.value + " " + "d")
        assembly_code.append(Instructions.GET.value + " " + "c")
        if instruction[4] == '+':
            assembly_code.append(Instructions.ADD.value + " " + "d")
        elif instruction[4] == '-':
            assembly_code.append(Instructions.SUB.value + " " + "d")
        elif instruction[4] == '*':
            pass
        elif instruction[4] == '/':
            pass
        elif instruction[4] == '%':
            pass  
        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichStoresToIntegerVariable(instruction[0], type, assembly_code, "b")
        assembly_code.append(Instructions.GET.value + " " + "c")
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toArrayVariableAssignBinaryOperationOfTwoIntegerVariables(self, instruction, type):
        assembly_code = []
        if isinstance(instruction[3], int) and isinstance(instruction[5], int):
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

        elif isinstance(instruction[3], int) and isinstance(instruction[5], str):
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(instruction[3], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[5], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.GET.value + " " + "c")
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

        elif isinstance(instruction[3], str) and isinstance(instruction[5], int):
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generate_number(instruction[5], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
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

        elif isinstance(instruction[3], str) and isinstance(instruction[5], str):
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[5], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
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
        assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "c")
        assembly_code.append(Instructions.STORE.value + " " + "b")
                  
        return assembly_code

    def toArrayVariableAssignBinaryOperationOfIntegerAndArrayVariables(self, instruction, type):
        assembly_code = []
        if instruction[4] in ['+', '-', '*', '/', '%']:
            if isinstance(instruction[3], int) and (isinstance(instruction[6], int) or isinstance(instruction[6], str)):
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[3], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[5], instruction[6], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.GET.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")
                assembly_code.append(Instructions.GET.value + " " + "c")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "d")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass          

            elif isinstance(instruction[3], str) and (isinstance(instruction[6], int) or isinstance(instruction[6], str)):
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[5], instruction[6], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.GET.value + " " + "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")
                assembly_code.append(Instructions.GET.value + " " + "c")
                if instruction[4] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "d")
                elif instruction[4] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                elif instruction[4] == '*':
                    pass
                elif instruction[4] == '/':
                    pass
                elif instruction[4] == '%':
                    pass

        elif instruction[5] in ['+', '-', '*', '/', '%']:
            if (isinstance(instruction[4], int) or isinstance(instruction[4], str)) and isinstance(instruction[6], int):
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[6], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.GET.value + " " + "c")
                assembly_code.append(Instructions.PUT.value + " " + "d")
                assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.GET.value + " " + "b")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "d")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass          
                    
            elif (isinstance(instruction[4], int) or isinstance(instruction[4], str)) and isinstance(instruction[6], str):
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[6], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")
                assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.GET.value + " " + "b")
                if instruction[5] == '+':
                    assembly_code.append(Instructions.ADD.value + " " + "d")
                elif instruction[5] == '-':
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                elif instruction[5] == '*':
                    pass
                elif instruction[5] == '/':
                    pass
                elif instruction[5] == '%':
                    pass

        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "c")
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def toArrayVariableAssignBinaryOperationOfTwoArraysVariables(self, instruction, type):
        assembly_code = []
        assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[6], instruction[7], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.PUT.value + " " + "d")
        assembly_code.append(Instructions.GET.value + " " + "c")
        if instruction[5] == '+':
            assembly_code.append(Instructions.ADD.value + " " + "d")
        elif instruction[5] == '-':
            assembly_code.append(Instructions.SUB.value + " " + "d")
        elif instruction[5] == '*':
            pass
        elif instruction[5] == '/':
            pass
        elif instruction[5] == '%':
            pass         
        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "c")
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code
    
    def writeIntegerVariable(self, instruction, type):
        assembly_code = []
        if isinstance(instruction[1], int):
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(instruction[1], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.WRITE.value)

        elif isinstance(instruction[1], str):
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.WRITE.value)

        return assembly_code

    def writeArrayVariable(self, instruction, type):
        assembly_code = []
        assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[1], instruction[2], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "b")
        assembly_code.append(Instructions.WRITE.value)

        return assembly_code

    def readToIntegerVariable(self, instruction, type):
        assembly_code = []
        assembly_code = self.createAssemblyWhichStoresToIntegerVariable(instruction[1], type, assembly_code, "b")
        assembly_code.append(Instructions.READ.value)
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def readToArrayVariable(self, instruction, type):
        assembly_code = []
        assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[1], instruction[2], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.READ.value)
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code

    def checkConditionForTwoIntegerVariables(self, instruction, type, block):
        assembly_code = []
        if isinstance(instruction[0], int) and isinstance(instruction[2], int):

            if instruction[1] == '=':
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "b") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '<':
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)   
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "c") 
                assembly_code.append(Instructions.DEC.value + " " + "b")
                assembly_code.append(Instructions.SUB.value + " " + "b")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

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
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append("block " + str(block['first_jump'])) 

            elif instruction[1] == '<=':
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)                
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)  
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>=':
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[0], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)                
                ins = self.generate_number(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)  
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '!=':
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)  
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.PUT.value + " " + "e")
                assembly_code.append(Instructions.GET.value + " " + "b") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.ADD.value + " " + "e")
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

        if isinstance(instruction[0], int) and isinstance(instruction[2], str):
            if instruction[1] == '=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")  
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "b") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '<':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")   
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "c") 
                assembly_code.append(Instructions.DEC.value + " " + "d")
                assembly_code.append(Instructions.SUB.value + " " + "d")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.SUB.value + " " + "b")    
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '<=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")               
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)  
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generate_number(instruction[0], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)                
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '!=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "d")   
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.PUT.value + " " + "e")
                assembly_code.append(Instructions.GET.value + " " + "d") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.ADD.value + " " + "e")
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

        if isinstance(instruction[0], str) and isinstance(instruction[2], int):
            if instruction[1] == '=':
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "d")   
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "d") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))
                
            elif instruction[1] == '<': 
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "d") 
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")  
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "c") 
                assembly_code.append(Instructions.DEC.value + " " + "d")
                assembly_code.append(Instructions.SUB.value + " " + "d")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>':
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.SUB.value + " " + "c")    
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append("block " + str(block['first_jump'])) 

            elif instruction[1] == '<=':
                assembly_code.append(Instructions.RST.value + " " + "a")               
                ins = self.generate_number(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins) 
                assembly_code.append(Instructions.PUT.value + " " + "c") 
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.SUB.value + " " + "c") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>=':
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generate_number(instruction[2], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)       
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "b")  
                assembly_code.append(Instructions.GET.value + " " + "c")          
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '!=':
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generate_number(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "d")  
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")   
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.PUT.value + " " + "e")
                assembly_code.append(Instructions.GET.value + " " + "d") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.ADD.value + " " + "e")
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

        if isinstance(instruction[0], str) and isinstance(instruction[2], str):
            if instruction[1] == '=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")   
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "d") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '<':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")   
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")  
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "c") 
                assembly_code.append(Instructions.DEC.value + " " + "d")
                assembly_code.append(Instructions.SUB.value + " " + "d")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.SUB.value + " " + "c")    
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append("block " + str(block['first_jump'])) 

            elif instruction[1] == '<=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c") 
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.SUB.value + " " + "c") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "d")  
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")          
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '!=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "d")  
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")   
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.PUT.value + " " + "e")
                assembly_code.append(Instructions.GET.value + " " + "d") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.ADD.value + " " + "e")
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
                assembly_code.append("block " + str(block['first_jump']))

        return assembly_code

    def checkConditionForIntegerAndArrayVariables(self, instruction, type, block):
        assembly_code = []
        if instruction[1] in ['=', '<', '>', '<=', '>=', '!=']:
            if instruction[1] == '=':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2],  instruction[3], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2],  instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "d")
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "d") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '<':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "c") 
                    assembly_code.append(Instructions.DEC.value + " " + "b")
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "d")
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "c") 
                    assembly_code.append(Instructions.DEC.value + " " + "d")
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.SUB.value + " " + "b")    
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "d")
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.SUB.value + " " + "d")    
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '<=':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")               
                    ins = self.generate_number(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "d")           
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '>=':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    ins = self.generate_number(instruction[0], "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)                
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "d")
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")  
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.GET.value + " " + "d")           
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[1] == '!=':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "d")   
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.PUT.value + " " + "e")
                    assembly_code.append(Instructions.GET.value + " " + "d") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.ADD.value + " " + "e")
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "d")   
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")  
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.PUT.value + " " + "e")
                    assembly_code.append(Instructions.GET.value + " " + "d") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.ADD.value + " " + "e")
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

        elif instruction[2] in ['=', '<', '>', '<=', '>=', '!=']:
            if instruction[2] == '=':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "d")   
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "c")  
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "d") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "d")   
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "c")  
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "d") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[2] == '<':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "d") 
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "c")  
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "c") 
                    assembly_code.append(Instructions.DEC.value + " " + "d")
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "d")   
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "c")  
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "c") 
                    assembly_code.append(Instructions.DEC.value + " " + "d")
                    assembly_code.append(Instructions.SUB.value + " " + "d")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[2] == '>':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")    
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append("block " + str(block['first_jump'])) 

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")    
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append("block " + str(block['first_jump'])) 

            elif instruction[2] == '<=':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")               
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins) 
                    assembly_code.append(Instructions.PUT.value + " " + "c") 
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "c") 
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[2] == '>=':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generate_number(instruction[3], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)       
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.GET.value + " " + "c")          
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "c")       
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.GET.value + " " + "c")          
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

            elif instruction[2] == '!=':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generate_number(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "d")  
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "c")   
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.PUT.value + " " + "e")
                    assembly_code.append(Instructions.GET.value + " " + "d") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.ADD.value + " " + "e")
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "d")  
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "c")   
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.PUT.value + " " + "e")
                    assembly_code.append(Instructions.GET.value + " " + "d") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.ADD.value + " " + "e")
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
                    assembly_code.append("block " + str(block['first_jump']))

        return assembly_code

    def checkConditionForTwoArrayVariables(self, instruction, type, block):
        if instruction[2] == '=':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "d")   
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b") 
            assembly_code.append(Instructions.PUT.value + " " + "c")  
            assembly_code.append(Instructions.SUB.value + " " + "d") 
            assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
            assembly_code.append(Instructions.GET.value + " " + "d") 
            assembly_code.append(Instructions.SUB.value + " " + "c")
            assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
            assembly_code.append("block " + str(block['first_jump']))

        elif instruction[2] == '<':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "d")   
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b") 
            assembly_code.append(Instructions.PUT.value + " " + "c")  
            assembly_code.append(Instructions.SUB.value + " " + "d") 
            assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
            assembly_code.append(Instructions.GET.value + " " + "c") 
            assembly_code.append(Instructions.DEC.value + " " + "d")
            assembly_code.append(Instructions.SUB.value + " " + "d")
            assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
            assembly_code.append("block " + str(block['first_jump']))
        
        elif instruction[2] == '>':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b") 
            assembly_code.append(Instructions.SUB.value + " " + "c")    
            assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 
            assembly_code.append("block " + str(block['first_jump'])) 

        elif instruction[2] == '<=':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c") 
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b") 
            assembly_code.append(Instructions.SUB.value + " " + "c") 
            assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
            assembly_code.append("block " + str(block['first_jump']))

        elif instruction[2] == '>=':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")       
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b") 
            assembly_code.append(Instructions.GET.value + " " + "c")          
            assembly_code.append(Instructions.SUB.value + " " + "b") 
            assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))
            assembly_code.append("block " + str(block['first_jump']))

        elif instruction[2] == '!=':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "d")  
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")   
            assembly_code.append(Instructions.SUB.value + " " + "d") 
            assembly_code.append(Instructions.PUT.value + " " + "e")
            assembly_code.append(Instructions.GET.value + " " + "d") 
            assembly_code.append(Instructions.SUB.value + " " + "c")
            assembly_code.append(Instructions.ADD.value + " " + "e")
            assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))
            assembly_code.append("block " + str(block['first_jump']))

    def callProcedure(self, instruction, type):
        assembly_code = []
        identifier = instruction[1]
        arguments = instruction[2]
        procedure_head_variables = self.program_variables[identifier][1] 
        for i in range(len(procedure_head_variables)):
            arg_in_proc_call = arguments[i]
            for var in self.program_variables[type]:
                if arg_in_proc_call in var.values():
                    variable1 = var
                    place_in_memory_of_variable1 = variable1['place_in_memory']
                if isinstance(list(var.values())[0], tuple):
                    if list(var.values())[0][0] == arg_in_proc_call:
                        variable1 = var
                        place_in_memory_of_variable1 = variable1['starts_at']
            place_in_memory_arg_in_proc_head = procedure_head_variables[i]['place_in_memory']
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generate_number(place_in_memory_arg_in_proc_head, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generate_number(place_in_memory_of_variable1, "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.STORE.value + " " + "b")
        assembly_code.append(Instructions.JUMP.value + " " + "1")

        return assembly_code