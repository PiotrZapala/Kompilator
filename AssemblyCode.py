from enum import Enum

MUL = ["JUMP main", "GET c",  "PUT e",
      "SHL c", "GET b", "SHR b",
      "JZERO 15", "SHL b", "SUB b",
      "SHR b", "JZERO 1", "GET d",
      "ADD e", "PUT d", "JUMP 1", "JUMPR h"]

DIV = ["RST d", "RST e", "RST f", "RST g", "GET c", "JZERO 58", "GET c", 
       "SUB b", "JPOS 60", "GET c", "PUT g", "SHL c", "GET c", "SUB b",
       "JPOS 33", "INC d", "JUMP 27", "SHR c", "GET d", "JZERO 55", "INC e",
       "DEC a", "SHL e","JPOS 37", "GET e", "ADD f", "PUT f", "RST d", "RST e",
       "GET b", "SUB c", "JZERO 59", "PUT b", "GET g", "SUB b", "JPOS 59", "GET g",
       "PUT c", "JUMP 25", "INC e", "ADD e", "ADD f", "PUT f", "JUMPR h", "RST a", "PUT f", "JUMPR h"]

MOD = ["GET c", "JZERO 104", "RST d", "RST e", "RST f", "RST g", "GET c", "PUT g",
       "SHL c", "GET c", "SUB b", "JPOS 77", "INC d", "JUMP 71", "SHR c", "GET d",
       "JZERO 96", "INC e", "DEC a", "SHL e", "JPOS 81", "GET e", "ADD f",
       "PUT f", "RST d", "RST e", "GET b", "SUB c", "JZERO 100", "PUT b",
       "GET g", "PUT c", "JUMP 69", "GET g", "SUB b", "JPOS 103", "GET b",
       "SUB g", "PUT f", "JUMP 105", "GET b", "PUT f", "JUMPR h"]

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

    def __init__(self, program_basic_blocks, declarations_in_main, output_file, procedures_basic_blocks=None, declarations_in_procedures=None, procedures_head=None):
        self.assembly_code = ""
        self.program_basic_blocks = program_basic_blocks
        self.declarations_in_main = declarations_in_main
        self.procedures_basic_blocks = procedures_basic_blocks
        self.declarations_in_procedures = declarations_in_procedures
        self.procedures_head = procedures_head
        self.program_variables = {}
        self.jumps = {}
        self.global_space_counter = 0
        self.output_file = output_file
    
    def generateNumber(self, number, register):
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
        for j in range(len(self.procedures_head)):
            proc_decl = []
            procedure_identifier = self.procedures_head[j]['procedure identifier']
            declarations_for_procedure = None
            for k in range(len(self.declarations_in_procedures)):
                if self.declarations_in_procedures[k]['procedure identifier'] == procedure_identifier:
                    declarations_for_procedure =  self.declarations_in_procedures[k]
                    break
            if declarations_for_procedure != None:
                for i in range(len(declarations_for_procedure['declarations'])):
                    variable = {}
                    if isinstance(declarations_for_procedure['declarations'][i]['identifier'], str):
                        variable['variable_'+str(i+1)] = declarations_for_procedure['declarations'][i]['identifier']
                        variable['initialized'] = False
                        variable['place_in_memory'] = self.global_space_counter
                        self.global_space_counter += 1
                    elif isinstance(declarations_for_procedure['declarations'][i]['identifier'], dict):
                        variable['variable_'+str(i+1)] = (declarations_for_procedure['declarations'][i]['identifier']['identifier'], declarations_for_procedure['declarations'][i]['identifier']['range'])
                        variable['initialized'] = False
                        variable['starts_at'] = self.global_space_counter
                        variable['ends_at'] = declarations_for_procedure['declarations'][i]['identifier']['range'] + self.global_space_counter - 1
                        self.global_space_counter = self.global_space_counter + declarations_for_procedure['declarations'][i]['identifier']['range']              
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
            procedure_variables.append([{'return address':self.global_space_counter}])
            self.global_space_counter += 1
            type = self.procedures_head[j]['procedure identifier']
            self.program_variables[type] = procedure_variables
            procedure_variables = []
        self.writeMulDivModToFile(self.output_file)
        for i in range(len(self.procedures_basic_blocks)):
            type = self.procedures_head[i]['procedure identifier']
            for block in self.procedures_basic_blocks[i]:
                assembly_code_for_one_block = self.identifyTypeOfInstructions(block, type)
                if len(assembly_code_for_one_block) >= 2:
                    block['instructions'] = [[instr for sublist in assembly_code_for_one_block for instr in sublist]]
                else:
                    if 'second_jump' in block:
                        block['instructions'] = assembly_code_for_one_block
                    else:
                        block['instructions'] = assembly_code_for_one_block
            return_block = self.createReturnFromProcedure(type)
            self.procedures_basic_blocks[i].append({'block': 'return', 'instructions': [return_block]})
            self.writeProcedureBlocksToFile(self.procedures_basic_blocks[i], 1, self.output_file, type)
            self.modifyJumpInstructions(self.output_file, self.output_file, type)
            self.updateJumpsInstructions(self.output_file, type)

        for block in self.program_basic_blocks[0]:
            assembly_code_for_one_block = self.identifyTypeOfInstructions(block, 'main')
            if len(assembly_code_for_one_block) >= 2:
                block['instructions'] = [[instr for sublist in assembly_code_for_one_block for instr in sublist]]
            else:
                if 'second_jump' in block:
                    block['instructions'] = assembly_code_for_one_block
                else:
                    block['instructions'] = assembly_code_for_one_block
        self.program_basic_blocks[0].append({'block': 'end', 'instructions': [[Instructions.HALT.value]]})
        self.writeProgramBlocksToFile(self.program_basic_blocks[0], 1, self.output_file, 'main')
        self.modifyJumpInstructions(self.output_file, self.output_file, 'main')
        self.updateJumpsInstructions(self.output_file, 'main')
        self.updateJumpsToProceduresOrMain(self.output_file)

    def modifyJumpInstructions(self, input_file_path, output_file_path, identifier_of_procedure):
        with open(input_file_path, 'r') as file:
            lines = file.readlines()
            jumps = {}
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                line_parts = line.split()
                if line == identifier_of_procedure:
                    jumps[identifier_of_procedure] = i
                    lines.pop(i)
                    lines.pop(i)
                if line_parts[0] == "block":
                    jumps[line] = i
                    lines.pop(i)
                i += 1
        self.jumps[identifier_of_procedure] = jumps
        with open(output_file_path, 'w') as file:
            for line in lines:
                file.write(line)
    
    def updateJumpsInstructions(self, output_file_path, identifier):
        jumps = self.jumps[identifier]

        with open(output_file_path, 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i].strip()
            parts = line.split()

            if len(parts) == 3 and parts[0] in ["JUMP", "JPOS", "JZERO"]:
                block_label = parts[1] + " " + parts[2] + ":"
                if block_label in jumps:
                    jump_line_number = jumps[block_label]
                    parts[1] = str(jump_line_number)
                    lines[i] = parts[0] + " " + parts[1] + '\n'
                elif parts[2] == "None":
                    if identifier == 'main':
                        jump_line_number = jumps.get('block end:', 'end')
                    else:
                        jump_line_number = jumps.get('block return:', 'return')
                    lines[i] = parts[0] + " " + str(jump_line_number) + '\n'

        with open(output_file_path, 'w') as file:
            file.writelines(lines)

    def updateJumpsToProceduresOrMain(self, output_file_path):
        with open(output_file_path, 'r') as file:
            lines = file.readlines()

        for i in range(len(lines)):
            line = lines[i].strip()
            parts = line.split()

            if len(parts) == 2 and parts[0] == "JUMP":
                jump_identifier = parts[1]
                if jump_identifier in self.jumps:
                    line_number = self.jumps[jump_identifier][jump_identifier]
                    parts[1] = str(line_number)
                    lines[i] = ' '.join(parts) + '\n'

        with open(output_file_path, 'w') as file:
            file.writelines(lines)
                                            
    def writeMulDivModToFile(self, filename):
        with open(filename, 'w') as file:
            for instruction in MUL:
                file.write(f"{instruction}\n")

            for instruction in DIV:
                file.write(f"{instruction}\n")

            for instruction in MOD:
                file.write(f"{instruction}\n")
        
    def writeProcedureBlocksToFile(self, blocks, start_block, filename, name):
        with open(filename, 'a') as file:
            processed_blocks = self.processBlocksInProcedure(blocks, start_block)
            file.write(f"{name}\n")
            for block_number, instruction_set in processed_blocks.items():
                if block_number is not None:
                    file.write(f"block {block_number}:\n")
                for instruction in instruction_set:
                    file.write(f"{instruction}\n")

    def processBlocksInProcedure(self, blocks, start_block):
        processed_blocks = {}
        seen_blocks = set()
        queue = [start_block]

        while queue:
            current_block = queue.pop(0)
            block = next((b for b in blocks if b['block'] == current_block), None)
            if not block:
                continue

            block_instructions = block['instructions'][0].copy()
            next_block = block.get('first_jump')

            if next_block is None and current_block != 'return':
                block_instructions.append('JUMP block return')
            elif next_block in seen_blocks:
                block_instructions.append(f'JUMP block {next_block}')
            elif next_block:
                queue.append(next_block)

            processed_blocks[current_block] = block_instructions
            seen_blocks.add(current_block)

        all_blocks = set(b['block'] for b in blocks)
        missing_blocks = all_blocks - seen_blocks
        missing_queue = list(missing_blocks)
        while missing_queue:
            block_num = missing_queue.pop(0)
            if block_num in seen_blocks:
                continue

            block = next(b for b in blocks if b['block'] == block_num)
            block_instructions = block['instructions'][0].copy()
            first_jump = block.get('first_jump')

            if first_jump is None and block_num != 'return':
                block_instructions.append('JUMP block return')
            elif first_jump in seen_blocks:
                block_instructions.append(f'JUMP block {first_jump}')
            elif first_jump:
                if first_jump in missing_queue:
                    missing_queue.remove(first_jump)
                    missing_queue.insert(0, first_jump)

            processed_blocks[block_num] = block_instructions
            seen_blocks.add(block_num)

        return processed_blocks

    def writeProgramBlocksToFile(self, blocks, start_block, filename, name):
        with open(filename, 'a') as file:
            processed_blocks = self.processBlocksInProgram(blocks, start_block)
            file.write(f"{name}\n")
            for block_number, instruction_set in processed_blocks.items():
                if block_number is not None:
                    file.write(f"block {block_number}:\n")
                for instruction in instruction_set:
                    file.write(f"{instruction}\n")

    def processBlocksInProgram(self, blocks, start_block):
        processed_blocks = {}
        seen_blocks = set()
        queue = [start_block]

        while queue:
            current_block = queue.pop(0)
            block = next((b for b in blocks if b['block'] == current_block), None)
            if not block:
                continue

            block_instructions = block['instructions'][0].copy()
            next_block = block.get('first_jump')

            if next_block is None and current_block != 'end':
                block_instructions.append('JUMP block end')
            elif next_block in seen_blocks:
                block_instructions.append(f'JUMP block {next_block}')
            elif next_block:
                queue.append(next_block)

            processed_blocks[current_block] = block_instructions
            seen_blocks.add(current_block)

        all_blocks = set(b['block'] for b in blocks)
        missing_blocks = all_blocks - seen_blocks
        missing_queue = list(missing_blocks)
        while missing_queue:
            block_num = missing_queue.pop(0)
            if block_num in seen_blocks:
                continue

            block = next(b for b in blocks if b['block'] == block_num)
            block_instructions = block['instructions'][0].copy()
            first_jump = block.get('first_jump')

            if first_jump is None and block_num != 'end':
                block_instructions.append('JUMP block end')
            elif first_jump in seen_blocks:
                block_instructions.append(f'JUMP block {first_jump}')
            elif first_jump:
                if first_jump in missing_queue:
                    missing_queue.remove(first_jump)
                    missing_queue.insert(0, first_jump)

            processed_blocks[block_num] = block_instructions
            seen_blocks.add(block_num)

        return processed_blocks
  
    def createReturnFromProcedure(self, type):
        assembly_code = []
        return_address = self.program_variables[type][2][0]['return address']
        assembly_code.append(Instructions.RST.value + " " + "h")
        ins = self.generateNumber(return_address, "h")
        if len(ins) != 0:   
            assembly_code.extend(ins)
        assembly_code.append(Instructions.LOAD.value + " " + "h")
        assembly_code.append(Instructions.JUMPR.value + " " + "a")

        return assembly_code

    def writeProgramToFile(self):
        with open('test1.mr', 'w') as file:
            for code in MUL:
                file.write(code + "\n")
            for code in DIV:
                file.write(code + "\n")
            for code in MOD:
                file.write(code + "\n")
            for block in self.program_basic_blocks[0]:
                for code in block["instructions"][0]:
                    file.write(code + "\n") 
            file.write("HALT")   

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
            ins = self.generateNumber(place_in_memory, register)
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
                ins = self.generateNumber(place_in_memory, register)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
            else:
                assembly_code.append(Instructions.RST.value + " " + register)
                ins = self.generateNumber(place_in_memory, register)
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
            ins = self.generateNumber(place_in_memory_of_variable2, register2)
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
                ins = self.generateNumber(place_in_memory_of_variable2, register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register2)
                assembly_code.append(Instructions.PUT.value + " " + register2)
            else:
                assembly_code.append(Instructions.RST.value + " " + register1)
                assembly_code.append(Instructions.RST.value + " " + register2)
                ins = self.generateNumber(place_in_memory_of_variable2, register2)
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
                ins = self.generateNumber(index + variable1['starts_at'], register2)
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
                ins = self.generateNumber(variable2['place_in_memory'], register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register2)
                assembly_code.append(Instructions.PUT.value + " " + register2)
                assembly_code.append(Instructions.RST.value + " " + register1)
                ins = self.generateNumber(variable1['starts_at'], register1)
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
                    ins = self.generateNumber(index + variable1['starts_at'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                else:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generateNumber(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generateNumber(index, register1)
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
                    ins = self.generateNumber(variable2['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generateNumber(variable1['starts_at'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.ADD.value + " " + register2) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == False and is_index_from_head == True:
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generateNumber(variable1['starts_at'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generateNumber(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.ADD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == True and is_index_from_head == False:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generateNumber(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generateNumber(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == True and is_index_from_head == True:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generateNumber(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generateNumber(variable2['place_in_memory'], register1)
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
                ins = self.generateNumber(index + variable1['starts_at'], register2)
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

                if variable2['initialized'] == False:
                    raise ValueError("ERROR: There is an uninitialized variable " + str(variable2['variable_2']))
                
                if variable1['initialized'] == False:
                    variable1['initialized'] = True
                assembly_code.append(Instructions.RST.value + " " + register1)
                assembly_code.append(Instructions.RST.value + " " + register2)
                ins = self.generateNumber(variable2['place_in_memory'], register2)
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.LOAD.value + " " + register2)
                assembly_code.append(Instructions.PUT.value + " " + register2)
                assembly_code.append(Instructions.RST.value + " " + register1)
                ins = self.generateNumber(variable1['starts_at'], register1)
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
                    ins = self.generateNumber(index + variable1['starts_at'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)  
                else:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generateNumber(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generateNumber(index, register1)
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
                
                if is_index_from_head == False:
                    if variable2['initialized'] == False:
                        raise ValueError("ERROR: There is an uninitialized variable " + str(variable2['variable_2']))

                if is_identifier_from_head == False and is_index_from_head == False:
                    if variable1['initialized'] == False:
                        variable1['initialized'] = True
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generateNumber(variable2['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generateNumber(variable1['starts_at'], register1)
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
                    ins = self.generateNumber(variable1['starts_at'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generateNumber(variable2['place_in_memory'], register1)
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
                    ins = self.generateNumber(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generateNumber(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)

                elif is_identifier_from_head == True and is_index_from_head == True:
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    assembly_code.append(Instructions.RST.value + " " + register2)
                    ins = self.generateNumber(variable1['place_in_memory'], register2)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + register2)
                    assembly_code.append(Instructions.PUT.value + " " + register2)
                    assembly_code.append(Instructions.RST.value + " " + register1)
                    ins = self.generateNumber(variable2['place_in_memory'], register1)
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.LOAD.value + " " + register1)    
                    assembly_code.append(Instructions.LOAD.value + " " + register1)
                    assembly_code.append(Instructions.ADD.value + " " + register2)  
                    assembly_code.append(Instructions.LOAD.value + " " + register1) 
                    assembly_code.append(Instructions.PUT.value + " " + register2)                    

        return assembly_code
    
    def getMulAssemblyCode(self, assembly_code, type):
        if type == '1':
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.PUT.value + " " + "h")
            assembly_code.append(Instructions.RST.value + " " + "d")
            assembly_code.append(Instructions.JUMP.value + " " + "1")
            assembly_code.append(Instructions.GET.value + " " + "d")
        elif type == '2':
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.GET.value + " " + "d")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.PUT.value + " " + "h")
            assembly_code.append(Instructions.RST.value + " " + "d")
            assembly_code.append(Instructions.JUMP.value + " " + "1")
            assembly_code.append(Instructions.GET.value + " " + "d")
        return assembly_code

    def getDivAssemblyCode(self, assembly_code, type):
        if type == '1':
            assembly_code.append(Instructions.PUT.value + " " + "d")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.GET.value + " " + "d")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.PUT.value + " " + "h")
            assembly_code.append(Instructions.RST.value + " " + "d")
            assembly_code.append(Instructions.JUMP.value + " " + "16")
            assembly_code.append(Instructions.GET.value + " " + "f")
        elif type == '2':
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.PUT.value + " " + "h")
            assembly_code.append(Instructions.RST.value + " " + "d")
            assembly_code.append(Instructions.JUMP.value + " " + "16")
            assembly_code.append(Instructions.GET.value + " " + "f")
        elif type == '3':
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.GET.value + " " + "d")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.PUT.value + " " + "h")
            assembly_code.append(Instructions.RST.value + " " + "d")
            assembly_code.append(Instructions.JUMP.value + " " + "16")
            assembly_code.append(Instructions.GET.value + " " + "f")
        return assembly_code

    def getModAssemblyCode(self, assembly_code, type):
        if type == '1':
            assembly_code.append(Instructions.PUT.value + " " + "d")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.GET.value + " " + "d")
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.PUT.value + " " + "h")
            assembly_code.append(Instructions.RST.value + " " + "d")
            assembly_code.append(Instructions.JUMP.value + " " + "63")
            assembly_code.append(Instructions.GET.value + " " + "f")
        elif type == '2':
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.PUT.value + " " + "h")
            assembly_code.append(Instructions.RST.value + " " + "d")
            assembly_code.append(Instructions.JUMP.value + " " + "63")
            assembly_code.append(Instructions.GET.value + " " + "f")
        elif type == '3':
            assembly_code.append(Instructions.PUT.value + " " + "b")
            assembly_code.append(Instructions.GET.value + " " + "d")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.PUT.value + " " + "h")
            assembly_code.append(Instructions.RST.value + " " + "d")
            assembly_code.append(Instructions.JUMP.value + " " + "63")
            assembly_code.append(Instructions.GET.value + " " + "f")
        return assembly_code

    def toIntegerVariableAssignIntegerVariable(self, instruction, type):
        assembly_code = []
        if isinstance(instruction[2], int):
            assembly_code = self.createAssemblyWhichStoresToIntegerVariable(instruction[0], type, assembly_code, "b")
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.extend(self.generateNumber(instruction[2], "a"))
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
            ins = self.generateNumber(instruction[3], "a")
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
            ins = self.generateNumber(instruction[3], "a")
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
            ins = self.generateNumber(instruction[2], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generateNumber(instruction[4], "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            if instruction[3] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "b")
            elif instruction[3] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "b")
            elif instruction[3] == '*':
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.getMulAssemblyCode(assembly_code, '1')
            elif instruction[3] == '/':
                assembly_code = self.getDivAssemblyCode(assembly_code, '1')                
            elif instruction[3] == '%':
                assembly_code = self.getModAssemblyCode(assembly_code, '1') 

        elif isinstance(instruction[2], int) and isinstance(instruction[4], str):
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generateNumber(instruction[2], "c")
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
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.getMulAssemblyCode(assembly_code, '1')
            elif instruction[3] == '/':
                assembly_code = self.getDivAssemblyCode(assembly_code, '1')
            elif instruction[3] == '%':
                assembly_code = self.getModAssemblyCode(assembly_code, '1')

        elif isinstance(instruction[2], str) and isinstance(instruction[4], int):
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generateNumber(instruction[4], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
            if instruction[3] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[3] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "c")
            elif instruction[3] == '*':
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code = self.getMulAssemblyCode(assembly_code, '1')
            elif instruction[3] == '/':
                assembly_code = self.getDivAssemblyCode(assembly_code, '2')
            elif instruction[3] == '%':
                assembly_code = self.getModAssemblyCode(assembly_code, '2')

        elif isinstance(instruction[2], str) and isinstance(instruction[4], str):
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
            if instruction[3] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[3] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "c")
            elif instruction[3] == '*':
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code = self.getMulAssemblyCode(assembly_code, '1')
            elif instruction[3] == '/':
                assembly_code = self.getDivAssemblyCode(assembly_code, '2')
            elif instruction[3] == '%':
                assembly_code = self.getModAssemblyCode(assembly_code, '2')

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
                ins = self.generateNumber(instruction[2], "c")
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
                    assembly_code = self.getMulAssemblyCode(assembly_code, '2')
                elif instruction[3] == '/':
                    assembly_code = self.getDivAssemblyCode(assembly_code, '3')
                elif instruction[3] == '%':
                    assembly_code = self.getModAssemblyCode(assembly_code, '3')        

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
                    assembly_code = self.getMulAssemblyCode(assembly_code, '2')
                elif instruction[3] == '/':
                    assembly_code = self.getDivAssemblyCode(assembly_code, '3')
                elif instruction[3] == '%':
                    assembly_code = self.getModAssemblyCode(assembly_code, '3')        

        elif instruction[4] in ['+', '-', '*', '/', '%']:
            if (isinstance(instruction[3], int) or isinstance(instruction[3], str)) and isinstance(instruction[5], int):
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generateNumber(instruction[5], "c")
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
                    assembly_code = self.getMulAssemblyCode(assembly_code, '2')
                elif instruction[4] == '/':
                    assembly_code = self.getDivAssemblyCode(assembly_code, '3')
                elif instruction[4] == '%':
                    assembly_code = self.getModAssemblyCode(assembly_code, '3')         
                    
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
                    assembly_code = self.getMulAssemblyCode(assembly_code, '2')
                elif instruction[4] == '/':
                    assembly_code = self.getDivAssemblyCode(assembly_code, '3')
                elif instruction[4] == '%':
                    assembly_code = self.getModAssemblyCode(assembly_code, '3')   

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
            assembly_code = self.getMulAssemblyCode(assembly_code, '2')
        elif instruction[4] == '/':
            assembly_code = self.getDivAssemblyCode(assembly_code, '3')
        elif instruction[4] == '%':
            assembly_code = self.getModAssemblyCode(assembly_code, '3')  
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
            ins = self.generateNumber(instruction[3], "a")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            ins = self.generateNumber(instruction[5], "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            if instruction[4] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "b")
            elif instruction[4] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "b")
            elif instruction[4] == '*':
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.getMulAssemblyCode(assembly_code, '1')
            elif instruction[4] == '/':
                assembly_code = self.getDivAssemblyCode(assembly_code, '1') 
            elif instruction[4] == '%':
                assembly_code = self.getModAssemblyCode(assembly_code, '1')

        elif isinstance(instruction[3], int) and isinstance(instruction[5], str):
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generateNumber(instruction[3], "c")
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
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.getMulAssemblyCode(assembly_code, '1')
            elif instruction[4] == '/':
                assembly_code = self.getDivAssemblyCode(assembly_code, '1') 
            elif instruction[4] == '%':
                assembly_code = self.getModAssemblyCode(assembly_code, '1')

        elif isinstance(instruction[3], str) and isinstance(instruction[5], int):
            assembly_code.append(Instructions.RST.value + " " + "c")
            ins = self.generateNumber(instruction[5], "c")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
            if instruction[4] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[4] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "c")
            elif instruction[4] == '*':
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code = self.getMulAssemblyCode(assembly_code, '1')
            elif instruction[4] == '/':
                assembly_code = self.getDivAssemblyCode(assembly_code, '2')
            elif instruction[4] == '%':
                assembly_code = self.getModAssemblyCode(assembly_code, '2')

        elif isinstance(instruction[3], str) and isinstance(instruction[5], str):
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[5], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
            if instruction[4] == '+':
                assembly_code.append(Instructions.ADD.value + " " + "c")
            elif instruction[4] == '-':
                assembly_code.append(Instructions.SUB.value + " " + "c")
            elif instruction[4] == '*':
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code = self.getMulAssemblyCode(assembly_code, '1')
            elif instruction[4] == '/':
                assembly_code = self.getDivAssemblyCode(assembly_code, '2')
            elif instruction[4] == '%':
                assembly_code = self.getModAssemblyCode(assembly_code, '2')

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
                ins = self.generateNumber(instruction[3], "c")
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
                    assembly_code = self.getMulAssemblyCode(assembly_code, '2')
                elif instruction[4] == '/':
                    assembly_code = self.getDivAssemblyCode(assembly_code, '3')
                elif instruction[4] == '%':
                    assembly_code = self.getModAssemblyCode(assembly_code, '3')          

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
                    assembly_code = self.getMulAssemblyCode(assembly_code, '2')
                elif instruction[4] == '/':
                    assembly_code = self.getDivAssemblyCode(assembly_code, '3')
                elif instruction[4] == '%':
                    assembly_code = self.getModAssemblyCode(assembly_code, '3')

        elif instruction[5] in ['+', '-', '*', '/', '%']:
            if (isinstance(instruction[4], int) or isinstance(instruction[4], str)) and isinstance(instruction[6], int):
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generateNumber(instruction[6], "c")
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
                    assembly_code = self.getMulAssemblyCode(assembly_code, '2')
                elif instruction[5] == '/':
                    assembly_code = self.getDivAssemblyCode(assembly_code, '3')
                elif instruction[5] == '%':
                    assembly_code = self.getModAssemblyCode(assembly_code, '3')          
                    
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
                    assembly_code = self.getMulAssemblyCode(assembly_code, '2')
                elif instruction[5] == '/':
                    assembly_code = self.getDivAssemblyCode(assembly_code, '3')
                elif instruction[5] == '%':
                    assembly_code = self.getModAssemblyCode(assembly_code, '3')

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
            assembly_code = self.getMulAssemblyCode(assembly_code, '2')
        elif instruction[5] == '/':
            assembly_code = self.getDivAssemblyCode(assembly_code, '3')
        elif instruction[5] == '%':
            assembly_code = self.getModAssemblyCode(assembly_code, '3')         
        assembly_code.append(Instructions.PUT.value + " " + "c")
        assembly_code = self.createAssemblyWhichStoresToArrayVariable(instruction[0], instruction[1], type, assembly_code, "a", "b")
        assembly_code.append(Instructions.GET.value + " " + "c")
        assembly_code.append(Instructions.STORE.value + " " + "b")

        return assembly_code
    
    def writeIntegerVariable(self, instruction, type):
        assembly_code = []
        if isinstance(instruction[1], int):
            assembly_code.append(Instructions.RST.value + " " + "a")
            ins = self.generateNumber(instruction[1], "a")
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
                ins = self.generateNumber(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "b") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '<':
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generateNumber(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)   
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "c") 
                assembly_code.append(Instructions.DEC.value + " " + "b")
                assembly_code.append(Instructions.SUB.value + " " + "b")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '>':
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.SUB.value + " " + "b")    
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

            elif instruction[1] == '<=':
                assembly_code.append(Instructions.RST.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)                
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)  
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '>=':
                assembly_code.append(Instructions.RST.value + " " + "a")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generateNumber(instruction[0], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)                
                ins = self.generateNumber(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)  
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '!=':
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generateNumber(instruction[2], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)  
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.PUT.value + " " + "e")
                assembly_code.append(Instructions.GET.value + " " + "b") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.ADD.value + " " + "e")
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))

        if isinstance(instruction[0], int) and isinstance(instruction[2], str):
            if instruction[1] == '=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")  
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "b") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '<':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "d")   
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                assembly_code.append(Instructions.GET.value + " " + "c") 
                assembly_code.append(Instructions.DEC.value + " " + "d")
                assembly_code.append(Instructions.SUB.value + " " + "d")
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '>':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.SUB.value + " " + "b")    
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

            elif instruction[1] == '<=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "b")
                assembly_code.append(Instructions.RST.value + " " + "a")               
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)  
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '>=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.RST.value + " " + "b")
                ins = self.generateNumber(instruction[0], "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)                
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '!=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "d")   
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[0], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")    
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.PUT.value + " " + "e")
                assembly_code.append(Instructions.GET.value + " " + "d") 
                assembly_code.append(Instructions.SUB.value + " " + "c")
                assembly_code.append(Instructions.ADD.value + " " + "e")
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))

        if isinstance(instruction[0], str) and isinstance(instruction[2], int):
            if instruction[1] == '=':
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[2], "a")
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
                
            elif instruction[1] == '<': 
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[2], "a")
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

            elif instruction[1] == '>':
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.SUB.value + " " + "c")    
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

            elif instruction[1] == '<=':
                assembly_code.append(Instructions.RST.value + " " + "a")               
                ins = self.generateNumber(instruction[2], "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins) 
                assembly_code.append(Instructions.PUT.value + " " + "c") 
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.SUB.value + " " + "c") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '>=':
                assembly_code.append(Instructions.RST.value + " " + "c")
                ins = self.generateNumber(instruction[2], "c")
                if len(ins) != 0:   
                    assembly_code.extend(ins)       
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "b")  
                assembly_code.append(Instructions.GET.value + " " + "c")          
                assembly_code.append(Instructions.SUB.value + " " + "b") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '!=':
                assembly_code.append(Instructions.RST.value + " " + "a")
                ins = self.generateNumber(instruction[2], "a")
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

            elif instruction[1] == '>':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c")
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.SUB.value + " " + "c")    
                assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

            elif instruction[1] == '<=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.PUT.value + " " + "c") 
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                assembly_code.append(Instructions.SUB.value + " " + "c") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '>=':
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                assembly_code.append(Instructions.PUT.value + " " + "d")  
                assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[2], type, assembly_code, "a", "b")          
                assembly_code.append(Instructions.SUB.value + " " + "d") 
                assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

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

        return assembly_code

    def checkConditionForIntegerAndArrayVariables(self, instruction, type, block):
        assembly_code = []
        if instruction[1] in ['=', '<', '>', '<=', '>=', '!=']:
            if instruction[1] == '=':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2],  instruction[3], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

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

            elif instruction[1] == '<':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump'])) 
                    assembly_code.append(Instructions.GET.value + " " + "c") 
                    assembly_code.append(Instructions.DEC.value + " " + "b")
                    assembly_code.append(Instructions.SUB.value + " " + "b")
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

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

            elif instruction[1] == '>':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.SUB.value + " " + "b")    
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "d")
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.SUB.value + " " + "d")    
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

            elif instruction[1] == '<=':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")               
                    ins = self.generateNumber(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)  
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.PUT.value + " " + "d")           
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '>=':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "a")
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    ins = self.generateNumber(instruction[0], "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)                
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

                elif isinstance(instruction[0], str):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "d")
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[0], type, assembly_code, "a", "b")  
                    assembly_code.append(Instructions.PUT.value + " " + "b")
                    assembly_code.append(Instructions.GET.value + " " + "d")           
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[1] == '!=':
                if isinstance(instruction[0], int):
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[2], instruction[3], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.GET.value + " " + "b")
                    assembly_code.append(Instructions.PUT.value + " " + "d")   
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(instruction[0], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "c")    
                    assembly_code.append(Instructions.SUB.value + " " + "d") 
                    assembly_code.append(Instructions.PUT.value + " " + "e")
                    assembly_code.append(Instructions.GET.value + " " + "d") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")
                    assembly_code.append(Instructions.ADD.value + " " + "e")
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump']))

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

        elif instruction[2] in ['=', '<', '>', '<=', '>=', '!=']:
            if instruction[2] == '=':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(instruction[3], "a")
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

            elif instruction[2] == '<':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(instruction[3], "a")
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

            elif instruction[2] == '>':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")    
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "c")
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c")    
                    assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

            elif instruction[2] == '<=':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")               
                    ins = self.generateNumber(instruction[3], "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins) 
                    assembly_code.append(Instructions.PUT.value + " " + "c") 
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "c") 
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.GET.value + " " + "b") 
                    assembly_code.append(Instructions.SUB.value + " " + "c") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[2] == '>=':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "c")
                    ins = self.generateNumber(instruction[3], "c")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)       
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.GET.value + " " + "c")          
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

                elif isinstance(instruction[3], str):
                    assembly_code = self.createAssemblyWhichGetsIntegerVariableFromMemory(instruction[3], type, assembly_code, "a", "b")
                    assembly_code.append(Instructions.PUT.value + " " + "c")       
                    assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b") 
                    assembly_code.append(Instructions.GET.value + " " + "c")          
                    assembly_code.append(Instructions.SUB.value + " " + "b") 
                    assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

            elif instruction[2] == '!=':
                if isinstance(instruction[3], int):
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(instruction[3], "a")
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
        
        elif instruction[2] == '>':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b") 
            assembly_code.append(Instructions.SUB.value + " " + "c")    
            assembly_code.append(Instructions.JZERO.value + " " + "block " + str(block['second_jump'])) 

        elif instruction[2] == '<=':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c") 
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b") 
            assembly_code.append(Instructions.SUB.value + " " + "c") 
            assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

        elif instruction[2] == '>=':
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[3], instruction[4], type, assembly_code, "a", "b")
            assembly_code.append(Instructions.GET.value + " " + "b")
            assembly_code.append(Instructions.PUT.value + " " + "c")       
            assembly_code = self.createAssemblyWhichGetsArrayVariableFromMemory(instruction[0], instruction[1], type, assembly_code, "a", "b") 
            assembly_code.append(Instructions.GET.value + " " + "c")          
            assembly_code.append(Instructions.SUB.value + " " + "b") 
            assembly_code.append(Instructions.JPOS.value + " " + "block " + str(block['second_jump']))

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

    def callProcedure(self, instruction, type):
        assembly_code = []
        if type == 'main':
            identifier = instruction[1]
            arguments = instruction[2]
            procedure_head_variables = self.program_variables[identifier][1] 
            procedure_return_address = self.program_variables[identifier][2][0]['return address']
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
                ins = self.generateNumber(place_in_memory_arg_in_proc_head, "b")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                ins = self.generateNumber(place_in_memory_of_variable1, "a")
                if len(ins) != 0:   
                    assembly_code.extend(ins)
                assembly_code.append(Instructions.STORE.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generateNumber(procedure_return_address, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.STORE.value + " " + "b")
            assembly_code.append(Instructions.JUMP.value + " " + identifier)
        else:
            identifier = instruction[1]
            arguments = instruction[2]

            procedure_head_variables = self.program_variables[identifier][1]
            procedure_return_address = self.program_variables[identifier][2][0]['return address']
            if len(self.program_variables[type][0]) > 0:
                variable1= None
                for i in range(len(procedure_head_variables)):
                    arg_in_proc_call = arguments[i]
                    for var in self.program_variables[type][0]:
                        if arg_in_proc_call in var.values():
                            variable1 = var
                            place_in_memory_of_variable1 = variable1['place_in_memory']
                        if isinstance(list(var.values())[0], tuple):
                            if list(var.values())[0][0] == arg_in_proc_call:
                                variable1 = var
                                place_in_memory_of_variable1 = variable1['starts_at']
                    place_in_memory_arg_in_proc_head = procedure_head_variables[i]['place_in_memory']
                    if variable1 != None:
                        assembly_code.append(Instructions.RST.value + " " + "b")
                        assembly_code.append(Instructions.RST.value + " " + "a")
                        ins = self.generateNumber(place_in_memory_arg_in_proc_head, "b")
                        if len(ins) != 0:   
                            assembly_code.extend(ins)
                        ins = self.generateNumber(place_in_memory_of_variable1, "a")
                        if len(ins) != 0:   
                            assembly_code.extend(ins)
                        assembly_code.append(Instructions.STORE.value + " " + "b")
                        variable1 = None
            variable1 = None
            for i in range(len(procedure_head_variables)):
                arg_in_proc_call = arguments[i]
                for var in self.program_variables[type][1]:
                    if arg_in_proc_call in var.values():
                        variable1 = var
                        place_in_memory_of_variable1 = variable1['place_in_memory']
                    if isinstance(list(var.values())[0], tuple):
                        if list(var.values())[0][0] == arg_in_proc_call:
                            variable1 = var
                            place_in_memory_of_variable1 = variable1['starts_at']
                place_in_memory_arg_in_proc_head = procedure_head_variables[i]['place_in_memory']
                if variable1 != None:
                    assembly_code.append(Instructions.RST.value + " " + "b")
                    assembly_code.append(Instructions.RST.value + " " + "a")
                    ins = self.generateNumber(place_in_memory_arg_in_proc_head, "b")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    ins = self.generateNumber(place_in_memory_of_variable1, "a")
                    if len(ins) != 0:   
                        assembly_code.extend(ins)
                    assembly_code.append(Instructions.LOAD.value + " " + "a")    
                    assembly_code.append(Instructions.STORE.value + " " + "b")
                    variable1 = None
            assembly_code.append(Instructions.RST.value + " " + "b")
            assembly_code.append(Instructions.RST.value + " " + "b")
            ins = self.generateNumber(procedure_return_address, "b")
            if len(ins) != 0:   
                assembly_code.extend(ins)
            assembly_code.append(Instructions.RST.value + " " + "a")
            assembly_code.append(Instructions.INC.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.SHL.value + " " + "a")
            assembly_code.append(Instructions.STRK.value + " " + "h")
            assembly_code.append(Instructions.ADD.value + " " + "h")
            assembly_code.append(Instructions.STORE.value + " " + "b")
            assembly_code.append(Instructions.JUMP.value + " " + identifier)

        return assembly_code
    