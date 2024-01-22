class BasicBlock:

    def __init__(self, type_of_instruction, is_first, is_last, previous, first_jump=None, second_jump=None, instruction=None, commands1=None, commands2=None):
        self.type_of_instruction = type_of_instruction
        self.is_first = is_first
        self.is_last = is_last
        self.previous = previous
        self.first_jump = first_jump
        self.second_jump = second_jump
        self.instruction = instruction
        self.commands1 = commands1
        self.commands2 = commands2

    @classmethod
    def create_assign_block(cls, type_of_instruction, is_first, is_last, previous, first_jump, instruction):
        return cls(type_of_instruction, is_first, is_last, previous, first_jump, instruction=instruction)

    @classmethod
    def create_while_block(cls, type_of_instruction, is_first, is_last, previous, first_jump, second_jump, instruction, commands):
        return cls(type_of_instruction, is_first, is_last, previous, first_jump, second_jump, instruction, commands1=commands)

    @classmethod
    def create_if_block(cls, type_of_instruction, is_first, is_last, previous, first_jump, second_jump, instruction, commands1, commands2):
        return cls(type_of_instruction, is_first, is_last, previous, first_jump, second_jump, instruction, commands1, commands2)

    def __str__(self):
        if self.type_of_instruction == 'Assign':
            return (f"AssignBlock(type_of_instruction={self.type_of_instruction}, "
                    f"is_first={self.is_first}, "
                    f"is_last={self.is_last}, "
                    f"instruction={self.instruction})")
        elif self.type_of_instruction == 'Read':
            return (f"ReadBlock(type_of_instruction={self.type_of_instruction}, "
                    f"is_first={self.is_first}, "
                    f"is_last={self.is_last}, "
                    f"instruction={self.instruction})")      
        elif self.type_of_instruction == 'Write':
            return (f"WriteBlock(type_of_instruction={self.type_of_instruction}, "
                    f"is_first={self.is_first}, "
                    f"is_last={self.is_last}, "
                    f"instruction={self.instruction})")      
        elif self.type_of_instruction == 'While Do':
            return (f"WhileBlock(type_of_instruction={self.type_of_instruction}, "
                    f"is_first={self.is_first}, "
                    f"is_last={self.is_last}, "
                    f"instruction={self.instruction}, "
                    f"commands={self.commands1})")
        elif self.type_of_instruction == 'Repeat Until':
            return (f"RepeatUntilBlock(type_of_instruction={self.type_of_instruction}, "
                    f"is_first={self.is_first}, "
                    f"is_last={self.is_last}, "
                    f"instruction={self.instruction}, "
                    f"commands={self.commands1})")
        elif self.type_of_instruction == 'If':
            if self.commands2:
                return (f"IfBlock(type_of_instruction={self.type_of_instruction}, "
                        f"is_first={self.is_first}, "
                        f"is_last={self.is_last}, "
                        f"instruction={self.instruction}, "
                        f"if_commands={self.commands1}, "
                        f"else_commands={self.commands2})")
            else:
                return (f"IfBlock(type_of_instruction={self.type_of_instruction}, "
                        f"is_first={self.is_first}, "
                        f"is_last={self.is_last}, "
                        f"instruction={self.instruction}, "
                        f"if_commands={self.commands1})")
        else:
            return "UnknownBlock"

    def __repr__(self):
        return self.__str__()

class BasicBlocks(BasicBlock):
    
    def __init__(self, procedure_commands_array, main_commands_array):
        self.main_program_blocks = []
        self.procedures_blocks = []
        self.blocks = []
        self.procedure_commands_array = procedure_commands_array
        self.main_commands_array = main_commands_array

    def createBasicBlocks(self):
        self.createBasicBlocksForMainProgram()
        self.createBasicBlocksForProcedures()
        return self.main_program_blocks, self.procedures_blocks

    def createBasicBlocksForMainProgram(self):
        self.blocks = []
        not_nested_instructions = self.getInstructions(self.main_commands_array)
        not_nested_blocks = self.createBlocks(not_nested_instructions)
        self.blocks.append(not_nested_blocks)
        for i in range(len(not_nested_blocks)):
            if not_nested_blocks[i].type_of_instruction == 'While Do':
                self.getInstructionsInWhileAndSetJumps(not_nested_blocks[i])   
            if not_nested_blocks[i].type_of_instruction == 'If':
                self.getInstructionsInIfAndSetJumps(not_nested_blocks[i])
        self.main_program_blocks.append(self.updateJumps())

    def createBasicBlocksForProcedures(self):
        for j in range(len(self.procedure_commands_array)):
            list_of_commands = self.procedure_commands_array[j]
            self.blocks = []
            not_nested_instructions = self.getInstructions(list_of_commands)
            not_nested_blocks = self.createBlocks(not_nested_instructions)
            self.blocks.append(not_nested_blocks)
            for i in range(len(not_nested_blocks)):
                if not_nested_blocks[i].type_of_instruction == 'While Do':
                    self.getInstructionsInWhileAndSetJumps(not_nested_blocks[i])   
                if not_nested_blocks[i].type_of_instruction == 'If':
                    self.getInstructionsInIfAndSetJumps(not_nested_blocks[i])
            self.procedures_blocks.append(self.updateJumps())
        
    def consolidateBlocks(self):
        consolidated_blocks = []
        block_number = 1

        for block_list in self.blocks:
            current_block = []
            for instruction in block_list:
                if instruction.type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                    current_block.append(instruction)
                else:
                    if current_block:
                        consolidated_blocks.append({block_number : current_block})
                        current_block = []
                        block_number += 1
                    consolidated_blocks.append({block_number : [instruction]})
                    block_number += 1

            if current_block:
                consolidated_blocks.append({block_number : current_block})
                block_number += 1

        return consolidated_blocks
    
    def updateJumps(self):
        updated_blocks = []
        consolidated_blocks = self.consolidateBlocks()
        for block_dict in consolidated_blocks:
            for block_number, instructions in block_dict.items():
                new_block = {'block': block_number, 'instructions': []}

                for instruction in instructions:
                    new_block['instructions'].append(instruction.instruction)

                if instructions[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                    jump_target = self.findJumpTarget(instructions[-1].first_jump, consolidated_blocks)
                    new_block['first_jump'] = jump_target
                if instructions[-1].type_of_instruction in ['While Do', 'If']:
                    jump_target = self.findJumpTarget(instructions[-1].first_jump, consolidated_blocks)                 
                    new_block['first_jump'] = jump_target
                    if instructions[-1].second_jump:
                        second_jump_target = self.findJumpTarget(instructions[-1].second_jump, consolidated_blocks)
                        new_block['second_jump'] = second_jump_target
                    else:
                        new_block['second_jump'] = None
                updated_blocks.append(new_block)
        return updated_blocks

    def findJumpTarget(self, jump, consolidated_blocks):
        for block_dict in consolidated_blocks:
            if jump in list(block_dict.values())[0]:
                return list(block_dict.keys())[0]
        return None

    def getInstructionsInWhileAndSetJumps(self, condition):
        nested_commands = condition.commands1
        condition.commands1 = None
        nested_instructions = self.getInstructions(nested_commands)
        nested_blocks = self.createBlocks(nested_instructions)
        self.blocks.append(nested_blocks)
        if nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
            condition.first_jump = nested_blocks[0]
            nested_blocks[0].previous = condition
            nested_blocks[-1].first_jump = condition
            if len(nested_blocks) >= 2:
                for i in range(len(nested_blocks)-1):
                    if nested_blocks[i].type_of_instruction in ['While Do']:
                        self.getInstructionsInWhileAndSetJumps(nested_blocks[i])
                    elif nested_blocks[i].type_of_instruction in ['If']:
                        self.getInstructionsInIfAndSetJumps(nested_blocks[i])
        elif nested_blocks[-1].type_of_instruction in ['While Do']:
            condition.first_jump = nested_blocks[0]
            nested_blocks[0].previous = condition
            nested_blocks[-1].second_jump = condition
            self.getInstructionsInWhileAndSetJumps(nested_blocks[-1])  
            if len(nested_blocks) >= 2:
                for i in range(len(nested_blocks)-1):
                    if nested_blocks[i].type_of_instruction in ['While Do']:
                        self.getInstructionsInWhileAndSetJumps(nested_blocks[i])    
                    elif nested_blocks[i].type_of_instruction in ['If']:
                        self.getInstructionsInIfAndSetJumps(nested_blocks[i])
        elif nested_blocks[-1].type_of_instruction in ['If']:
            condition.first_jump = nested_blocks[0]
            nested_blocks[0].previous = condition
            if len(nested_blocks) >= 2:
                for i in range(len(nested_blocks)-1):
                    if nested_blocks[i].type_of_instruction in ['While Do']:
                        self.getInstructionsInWhileAndSetJumps(nested_blocks[i])
                    elif nested_blocks[i].type_of_instruction in ['If']:
                        self.getInstructionsInIfAndSetJumps(nested_blocks[i])
            if nested_blocks[-1].commands2 == None:
                if_nested_commands = nested_blocks[-1].commands1
                nested_blocks[-1].commands1 = None
                if_nested_instructions = self.getInstructions(if_nested_commands)
                if_nested_blocks = self.createBlocks(if_nested_instructions)
                self.blocks.append(if_nested_blocks)
                if_nested_blocks[0].previous = nested_blocks[-1]
                nested_blocks[-1].first_jump = if_nested_blocks[0]
                if if_nested_blocks[-1].type_of_instruction == 'While Do':
                   self.getInstructionsInWhileAndSetJumps(if_nested_blocks[-1])
                   if_nested_blocks[-1].second_jump = condition
                   if len(if_nested_blocks) >= 2:
                        for i in range(len(if_nested_blocks)-1):
                            if if_nested_blocks[i].type_of_instruction in ['While Do']:
                                self.getInstructionsInWhileAndSetJumps(if_nested_blocks[i])
                            elif if_nested_blocks[i].type_of_instruction in ['If']:
                                self.getInstructionsInIfAndSetJumps(if_nested_blocks[i])                   
                elif if_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                    if_nested_blocks[-1].first_jump = condition
                    if len(if_nested_blocks) >= 2:
                        for i in range(len(if_nested_blocks)-1):
                            if if_nested_blocks[i].type_of_instruction in ['While Do']:
                                self.getInstructionsInWhileAndSetJumps(if_nested_blocks[i])
                            elif if_nested_blocks[i].type_of_instruction in ['If']:
                                self.getInstructionsInIfAndSetJumps(if_nested_blocks[i])              
            else:
                if_nested_commands = nested_blocks[-1].commands1
                nested_blocks[-1].commands1 = None
                if_nested_instructions = self.getInstructions(if_nested_commands)
                if_nested_blocks = self.createBlocks(if_nested_instructions)
                self.blocks.append(if_nested_blocks)
                if_nested_blocks[0].previous = nested_blocks[-1]

                else_nested_commands = nested_blocks[-1].commands2
                nested_blocks[-1].commands2 = None
                else_nested_instructions = self.getInstructions(else_nested_commands)
                else_nested_blocks = self.createBlocks(else_nested_instructions)
                self.blocks.append(else_nested_blocks)
                else_nested_blocks[0].previous = nested_blocks[-1]
                
                nested_blocks[-1].first_jump = if_nested_blocks[0]
                nested_blocks[-1].second_jump = else_nested_blocks[0]

                if if_nested_blocks[-1].type_of_instruction == 'While Do':
                   self.getInstructionsInWhileAndSetJumps(if_nested_blocks[-1])
                   if_nested_blocks[-1].second_jump = condition
                   if len(if_nested_blocks) >= 2:
                        for i in range(len(if_nested_blocks)-1):
                            if if_nested_blocks[i].type_of_instruction in ['While Do']:
                                self.getInstructionsInWhileAndSetJumps(if_nested_blocks[i])
                            elif if_nested_blocks[i].type_of_instruction in ['If']:
                                self.getInstructionsInIfAndSetJumps(if_nested_blocks[i])                   
                elif if_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                    if_nested_blocks[-1].first_jump = condition
                    if len(if_nested_blocks) >= 2:
                        for i in range(len(if_nested_blocks)-1):
                            if if_nested_blocks[i].type_of_instruction in ['While Do']:
                                self.getInstructionsInWhileAndSetJumps(if_nested_blocks[i])
                            elif if_nested_blocks[i].type_of_instruction in ['If']:
                                self.getInstructionsInIfAndSetJumps(if_nested_blocks[i])
                if else_nested_blocks[-1].type_of_instruction == 'While Do':
                   self.getInstructionsInWhileAndSetJumps(else_nested_blocks[-1])
                   else_nested_blocks[-1].second_jump = condition
                   if len(else_nested_blocks) >= 2:
                        for i in range(len(else_nested_blocks)-1):
                            if else_nested_blocks[i].type_of_instruction in ['While Do']:
                                self.getInstructionsInWhileAndSetJumps(else_nested_blocks[i])
                            elif else_nested_blocks[i].type_of_instruction in ['If']:
                                self.getInstructionsInIfAndSetJumps(else_nested_blocks[i])                   
                elif else_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                    else_nested_blocks[-1].first_jump = condition
                    if len(else_nested_blocks) >= 2:
                        for i in range(len(if_nested_blocks)-1):
                            if else_nested_blocks[i].type_of_instruction in ['While Do']:
                                self.getInstructionsInWhileAndSetJumps(else_nested_blocks[i])
                            elif else_nested_blocks[i].type_of_instruction in ['If']:
                                self.getInstructionsInIfAndSetJumps(else_nested_blocks[i])                    

        return nested_blocks   

    def getInstructionsInIfAndSetJumps(self, condition):
        if condition.commands2 == None:
            if_nested_commands = condition.commands1
            condition.commands1 = None
            if_nested_instructions = self.getInstructions(if_nested_commands)
            if_nested_blocks = self.createBlocks(if_nested_instructions)
            self.blocks.append(if_nested_blocks)
            if_nested_blocks[0].previous = condition
            condition.first_jump = if_nested_blocks[0]
            if len(if_nested_blocks) >= 2:
                for i in range(len(if_nested_blocks)-1):
                    if if_nested_blocks[i].type_of_instruction in ['While Do']:
                        self.getInstructionsInWhileAndSetJumps(if_nested_blocks[i])
                    elif if_nested_blocks[i].type_of_instruction in ['If']:
                        self.getInstructionsInIfAndSetJumps(if_nested_blocks[i])  
            if condition.second_jump != None:
                if if_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                    if_nested_blocks[-1].first_jump = condition.second_jump
                elif if_nested_blocks[-1].type_of_instruction in ['While Do']:
                    if_nested_blocks[-1].second_jump = condition.second_jump
                    self.getInstructionsInWhileAndSetJumps(if_nested_blocks[-1])
                elif if_nested_blocks[-1].type_of_instruction in ['If']:
                    if_nested_blocks[-1].second_jump = condition.second_jump
                    self.getInstructionsInIfAndSetJumps(if_nested_blocks[-1])
            else:   
                if if_nested_blocks[-1].type_of_instruction in ['While Do']:
                    self.getInstructionsInWhileAndSetJumps(if_nested_blocks[-1])
                elif if_nested_blocks[-1].type_of_instruction in ['If']:
                    self.getInstructionsInIfAndSetJumps(if_nested_blocks[-1])

        else:
            if_nested_commands = condition.commands1
            condition.commands1 = None
            if_nested_instructions = self.getInstructions(if_nested_commands)
            if_nested_blocks = self.createBlocks(if_nested_instructions)
            self.blocks.append(if_nested_blocks)
            if_nested_blocks[0].previous = condition
            condition.first_jump = if_nested_blocks[0]
            
            else_nested_commands = condition.commands2
            condition.commands2 = None
            else_nested_instructions = self.getInstructions(else_nested_commands)
            else_nested_blocks = self.createBlocks(else_nested_instructions) 
            self.blocks.append(else_nested_blocks)
            else_nested_blocks[0].previous = condition
            if len(if_nested_blocks) >= 2:
                for i in range(len(if_nested_blocks)-1):
                    if if_nested_blocks[i].type_of_instruction in ['While Do']:
                        self.getInstructionsInWhileAndSetJumps(if_nested_blocks[i])
                    elif if_nested_blocks[i].type_of_instruction in ['If']:
                        self.getInstructionsInIfAndSetJumps(if_nested_blocks[i])  

            if if_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall'] and else_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                if_nested_blocks[-1].first_jump = condition.second_jump
                else_nested_blocks[-1].first_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]

            elif if_nested_blocks[-1].type_of_instruction in ['While Do'] and else_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                if_nested_blocks[-1].second_jump = condition.second_jump
                else_nested_blocks[-1].first_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]
                self.getInstructionsInWhileAndSetJumps(if_nested_blocks[-1])

            elif if_nested_blocks[-1].type_of_instruction in ['If'] and else_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall']:
                if_nested_blocks[-1].second_jump = condition.second_jump
                else_nested_blocks[-1].first_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]                    
                self.getInstructionsInIfAndSetJumps(if_nested_blocks[-1])


            elif if_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall'] and else_nested_blocks[-1].type_of_instruction in ['While Do']:
                if_nested_blocks[-1].first_jump = condition.second_jump
                else_nested_blocks[-1].second_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]
                self.getInstructionsInWhileAndSetJumps(else_nested_blocks[-1])

            elif if_nested_blocks[-1].type_of_instruction in ['While Do'] and else_nested_blocks[-1].type_of_instruction in ['While Do']:
                if_nested_blocks[-1].second_jump = condition.second_jump
                else_nested_blocks[-1].second_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]
                self.getInstructionsInWhileAndSetJumps(if_nested_blocks[-1])
                self.getInstructionsInWhileAndSetJumps(else_nested_blocks[-1])

            elif if_nested_blocks[-1].type_of_instruction in ['If'] and else_nested_blocks[-1].type_of_instruction in ['While Do']:
                if_nested_blocks[-1].second_jump = condition.second_jump
                else_nested_blocks[-1].second_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]                    
                self.getInstructionsInIfAndSetJumps(if_nested_blocks[-1])
                self.getInstructionsInWhileAndSetJumps(else_nested_blocks[-1])  


            elif if_nested_blocks[-1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall'] and else_nested_blocks[-1].type_of_instruction in ['If']:
                if_nested_blocks[-1].first_jump = condition.second_jump
                else_nested_blocks[-1].second_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]
                self.getInstructionsInIfAndSetJumps(else_nested_blocks[-1])

            elif if_nested_blocks[-1].type_of_instruction in ['While Do'] and else_nested_blocks[-1].type_of_instruction in ['If']:
                if_nested_blocks[-1].second_jump = condition.second_jump
                else_nested_blocks[-1].second_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]
                self.getInstructionsInWhileAndSetJumps(if_nested_blocks[-1])
                self.getInstructionsInIfAndSetJumps(else_nested_blocks[-1])

            elif if_nested_blocks[-1].type_of_instruction in ['If'] and else_nested_blocks[-1].type_of_instruction in ['If']:
                if_nested_blocks[-1].second_jump = condition.second_jump
                else_nested_blocks[-1].second_jump = condition.second_jump
                condition.second_jump = else_nested_blocks[0]                    
                self.getInstructionsInIfAndSetJumps(if_nested_blocks[-1])
                self.getInstructionsInIfAndSetJumps(else_nested_blocks[-1])                    
                  
    
    def getInstructions(self, list_of_commands):
        not_nested_instructions = []
        for i, command in enumerate(list_of_commands):
            if command['command type'] == 'Assign':
                is_first = i == 0
                is_last = i == len(list_of_commands) - 1
                not_nested_instructions.append(
                    BasicBlock.create_assign_block('Assign', is_first, is_last, None, None, self.parseAssign(command))
                )

            elif command['command type'] == 'While Do':
                is_first = i == 0
                is_last = i == len(list_of_commands) - 1
                not_nested_instructions.append(
                    BasicBlock.create_while_block('While Do', is_first, is_last, None, None, None, self.parseCondition(command['condition']), command['commands'])
                )

            elif command['command type'] == 'Repeat Until':
                is_first = i == 0
                is_last = i == len(list_of_commands) - 1
                not_nested_instructions.append(
                    BasicBlock.create_while_block('Repeat Until', is_first, is_last, None, None, None, self.parseCondition(command['condition']), command['commands'])
                )

            elif command['command type'] == 'If':
                is_first = i == 0
                is_last = i == len(list_of_commands) - 1
                if 'else commands' in command:
                    not_nested_instructions.append(
                        BasicBlock.create_if_block('If', is_first, is_last, None, None, None, self.parseCondition(command['condition']), command['if commands'], command['else commands'])
                    )
                else:
                    not_nested_instructions.append(
                        BasicBlock.create_if_block('If', is_first, is_last, None, None, None, self.parseCondition(command['condition']), command['if commands'], None)
                    )

            elif command['command type'] == 'Read':
                is_first = i == 0
                is_last = i == len(list_of_commands) - 1
                not_nested_instructions.append(
                    BasicBlock.create_assign_block('Read', is_first, is_last, None, None, self.parseRead(command))
                )
            elif command['command type'] == 'Write':
                is_first = i == 0
                is_last = i == len(list_of_commands) - 1
                not_nested_instructions.append(
                    BasicBlock.create_assign_block('Write', is_first, is_last, None, None, self.parseWrite(command))
                )
            elif command['command type'] == 'Procedure Call':
                is_first = i == 0
                is_last = i == len(list_of_commands) - 1
                not_nested_instructions.append(
                    BasicBlock.create_assign_block('ProcCall', is_first, is_last, None, None, self.parseProcCall(command))
                )

        return not_nested_instructions

        
    def createBlocks(self, instructions):
        i = 0
        while i < len(instructions):
            if i != len(instructions)-1:
                if instructions[i].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall'] and instructions[i+1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall', 'While Do', 'If']:
                    if i == 0:
                        instructions[i].first_jump = instructions[i+1]
                    else:
                        if i+1 <= len(instructions)-1:
                            instructions[i].first_jump = instructions[i+1]
                            instructions[i].previous = instructions[i-1]
            else:
                instructions[i].previous = instructions[i-1]

            if i != len(instructions)-1:
                if instructions[i].type_of_instruction in ['While Do'] and instructions[i+1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall', 'While Do', 'If']:
                    if i == 0:
                        instructions[i].second_jump = instructions[i+1]
                    else:
                        if i+1 <= len(instructions)-1:
                            instructions[i].second_jump = instructions[i+1]
                            instructions[i].previous = instructions[i-1]
            else:
                instructions[i].previous = instructions[i-1]

            if i != len(instructions)-1:
                if instructions[i].type_of_instruction in ['If'] and instructions[i+1].type_of_instruction in ['Assign', 'Write', 'Read', 'ProcCall', 'While Do', 'If']:
                    if i == 0:
                        instructions[i].second_jump = instructions[i+1]
                    else:
                        if i+1 <= len(instructions)-1:
                            
                            instructions[i].second_jump = instructions[i+1]
                            instructions[i].previous = instructions[i-1]  
            else:
                instructions[i].second_jump = None        
            i += 1
        return instructions

    def parseAssign(self, command):
        if isinstance(command['left side'], str):
            if isinstance(command['right side'], (str,int)):
                current_block = (command['left side'], ':=', command['right side'])
            else:
                if len(command['right side']) == 2:
                    current_block = (command['left side'], ':=', command['right side']['identifier'], command['right side']['index'])
                else:
                    if isinstance(command['right side']['left'], (str,int)) and isinstance(command['right side']['right'], (str,int)):
                        current_block = (command['left side'], ':=', command['right side']['left'], command['right side']['operator'], command['right side']['right'])
                    elif isinstance(command['right side']['left'], dict) and isinstance(command['right side']['right'], (str,int)):
                        current_block = (command['left side'], ':=', command['right side']['left']['identifier'], command['right side']['left']['index'], command['right side']['operator'], command['right side']['right'])
                    elif isinstance(command['right side']['left'], (str,int)) and isinstance(command['right side']['right'], dict):
                        current_block = (command['left side'], ':=', command['right side']['left'], command['right side']['operator'], command['right side']['right']['identifier'], command['right side']['right']['index'])
                    elif isinstance(command['right side']['left'], dict) and isinstance(command['right side']['right'], dict):
                        current_block = (command['left side'], ':=', command['right side']['left']['identifier'], command['right side']['left']['index'], command['right side']['operator'], command['right side']['right']['identifier'], command['right side']['right']['index'])
        else:
            if isinstance(command['right side'], (str,int)):
                current_block = (command['left side']['identifier'], command['left side']['index'], ':=', command['right side'])
            else:
                if len(command['right side']) == 2:
                    current_block = (command['left side']['identifier'], command['left side']['index'], ':=', command['right side']['identifier'], command['right side']['index'])
                else:
                    if isinstance(command['right side']['left'], (str,int)) and isinstance(command['right side']['right'], (str,int)):
                        current_block = (command['left side']['identifier'], command['left side']['index'], ':=', command['right side']['left'], command['right side']['operator'], command['right side']['right'])
                    elif isinstance(command['right side']['left'], dict) and isinstance(command['right side']['right'], (str,int)):
                        current_block = (command['left side']['identifier'], command['left side']['index'], ':=', command['right side']['left']['identifier'], command['right side']['left']['index'], command['right side']['operator'], command['right side']['right'])
                    elif isinstance(command['right side']['left'], (str,int)) and isinstance(command['right side']['right'], dict):
                        current_block = (command['left side']['identifier'], command['left side']['index'], ':=', command['right side']['left'], command['right side']['operator'], command['right side']['right']['identifier'], command['right side']['right']['index'])
                    elif isinstance(command['right side']['left'], dict) and isinstance(command['right side']['right'], dict):
                        current_block = (command['left side']['identifier'], command['left side']['index'], ':=', command['right side']['left']['identifier'], command['right side']['left']['index'], command['right side']['operator'], command['right side']['right']['identifier'], command['right side']['right']['index'])
        return current_block

    def parseCondition(self, command):
        current_block = ()
        if isinstance(command['left'], (str,int)) and isinstance(command['right'], (str,int)):
            current_block = (command['left'], command['operator'], command['right'])
        elif isinstance(command['left'], (str,int)) and isinstance(command['right'], dict):
            current_block = (command['left'], command['operator'], command['right']['identifier'], command['right']['index'])
        elif isinstance(command['left'], dict) and isinstance(command['right'], (str,int)):
            current_block = (command['left']['identifier'], command['left']['index'], command['operator'], command['right'])
        elif isinstance(command['left'], dict) and isinstance(command['right'], dict):
            current_block = (command['left']['identifier'], command['left']['index'], command['operator'], command['right']['identifier'], command['right']['index'])
        return current_block
    
    def parseWrite(self, command):
        current_block = ()
        if isinstance(command['right side'], (str,int)):
            current_block = ('Write', command['right side'])
        elif isinstance(command['right side'], dict):
            current_block = ('Write', command['right side']['identifier'], command['right side']['index'])
        return current_block  

    def parseRead(self, command):
        current_block = ()
        if isinstance(command['right side'], (str,int)):
            current_block = ('Read', command['right side'])
        elif isinstance(command['right side'], dict):
            current_block = ('Read', command['right side']['identifier'], command['right side']['index'])
        return current_block     

    def parseProcCall(self, command):
        current_block = ()
        arguments = []
        for i in range(len(command['arguments'])):
            arguments.append(command['arguments'][i]['argument ' + str(i+1)])
        current_block = ('ProcCall', command['procedure identifier'], arguments)
        return current_block