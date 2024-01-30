class Debugger:

    def __init__(self):
        self.errors = []
        self.warnings = []

    def programDebugger(self, main_commands_array, decl_in_main, procedure_commands_array, decl_in_procedures,  procedures_head):
        self.checkPossibleErrorsInCommands(main_commands_array, decl_in_main, None, procedures_head, 'main')
        for i in range(len(procedures_head)):
            procedure_identifier = procedures_head[i]['procedure identifier']
            declarations_for_procedure = None
            for k in range(len(decl_in_procedures)):
                if decl_in_procedures[k]['procedure identifier'] == procedure_identifier:
                    declarations_for_procedure = decl_in_procedures[k]
                    break
            if declarations_for_procedure != None:
                self.checkNameConflicts(declarations_for_procedure['declarations'], procedures_head[i])
                self.checkPossibleErrorsInCommands(procedure_commands_array[i], declarations_for_procedure['declarations'], procedures_head[i], procedures_head, procedures_head[i]["procedure identifier"])  
            else:
                self.checkPossibleErrorsInCommands(procedure_commands_array[i], [], procedures_head[i], procedures_head, procedures_head[i]["procedure identifier"])     

    def checkPossibleErrorsInCommands(self, list_of_commands, declarations, head, procedures_head, type):
        if head != None:
            arguments_declarations = head["arguments declarations"]
        else:
            arguments_declarations = []
        for i in range(len(list_of_commands)):
            if list_of_commands[i]["command type"] == "Assign":
                left_side = list_of_commands[i]["left side"]
                right_side = list_of_commands[i]["right side"]
                line_number = list_of_commands[i]["line number"]
                self.checkForUndeclaredVariablesInAssign(declarations, arguments_declarations, left_side, right_side, line_number)
                                                 
            elif list_of_commands[i]["command type"] == "Read":                   
                right_side = list_of_commands[i]["right side"]
                line_number = list_of_commands[i]["line number"]
                self.checkForUndeclaredVariablesInRead(declarations, arguments_declarations, right_side, line_number)

            elif list_of_commands[i]["command type"] == "Write":                   
                right_side = list_of_commands[i]["right side"]
                line_number = list_of_commands[i]["line number"]
                self.checkForUndeclaredVariablesInWrite(declarations, arguments_declarations, right_side, line_number)

            elif list_of_commands[i]["command type"] == "Procedure Call":                   
                identifier = list_of_commands[i]['procedure identifier']
                list_of_arguments = list_of_commands[i]['arguments']
                line_number = list_of_commands[i]['line number']
                self.checkWhetherTheCalledProcedureExistsAndWhetherItsUseIsCorrect(identifier, procedures_head, line_number, list_of_arguments, type)
                self.checkForExtraArgumentsInProcCall(identifier, list_of_arguments, procedures_head ,line_number)
                self.checkForUndeclaredVariablesAndIfTypeIsCorrectInProcCall(declarations, arguments_declarations, identifier, list_of_arguments, procedures_head, line_number)

            elif list_of_commands[i]["command type"] == "While Do":                   
                condition = list_of_commands[i]["condition"]
                commands = list_of_commands[i]["commands"]
                line_number = list_of_commands[i]["line number"]
                left_side = condition["left"]
                operator = condition["operator"]
                right_side = condition["right"]
                self.checkForUndeclaredVariablesInCondition(declarations, arguments_declarations, left_side, right_side, operator, line_number)
                self.checkPossibleErrorsInCommands(commands, declarations, head, procedures_head, type)

            elif list_of_commands[i]["command type"] == "Repeat Until":                   
                condition = list_of_commands[i]["condition"]
                commands = list_of_commands[i]["commands"]
                line_number = list_of_commands[i]["line number"]
                left_side = condition["left"]
                operator = condition["operator"]
                right_side = condition["right"]
                self.checkPossibleErrorsInCommands(commands, declarations, head, procedures_head, type)                
                self.checkForUndeclaredVariablesInCondition(declarations, arguments_declarations, left_side, right_side, operator, line_number)

            elif list_of_commands[i]["command type"] == "If":                   
                condition = list_of_commands[i]["condition"]
                if_commands = list_of_commands[i]["if commands"]
                if "else commands" in list_of_commands[i]:
                    else_commands = list_of_commands[i]["else commands"]
                else: 
                    else_commands = None
                line_number = list_of_commands[i]["line number"]
                left_side = condition["left"]
                operator = condition["operator"]
                right_side = condition["right"]
                if else_commands != None:
                    self.checkForUndeclaredVariablesInCondition(declarations, arguments_declarations, left_side, right_side, operator, line_number)
                    self.checkPossibleErrorsInCommands(if_commands, declarations, head, procedures_head, type)
                    self.checkPossibleErrorsInCommands(else_commands, declarations, head, procedures_head, type)
                else:
                    self.checkForUndeclaredVariablesInCondition(declarations, arguments_declarations, left_side, right_side, operator, line_number)
                    self.checkPossibleErrorsInCommands(if_commands, declarations, head, procedures_head, type)
    
    def checkForExtraArgumentsInProcCall(self, identifier, list_of_arguments, procedures_head, line_number):
        number_of_arguments = len(list_of_arguments)
        for i in range(len(procedures_head)):
            if procedures_head[i]['procedure identifier'] == identifier:
                if number_of_arguments < len(procedures_head[i]['arguments declarations']):
                    if len(procedures_head[i]['arguments declarations']) - number_of_arguments == 1:
                        raise ValueError("ERROR: There is a missing argument in procedure call in line " + str(line_number))
                    else:
                        raise ValueError("ERROR: There are missing arguments in procedure call in line " + str(line_number))
                elif number_of_arguments > len(procedures_head[i]['arguments declarations']):
                    if len(procedures_head[i]['arguments declarations']) - number_of_arguments == 1:
                        raise ValueError("ERROR: There is an extra argument in procedure call in line " + str(line_number))
                    else:
                        raise ValueError("ERROR: There are extra arguments in procedure call in line " + str(line_number))    

    def checkNameConflicts(self, decl_in_procedures,  procedures_head):
        args = []
        head = []
        is_conflict = False
        line_number = decl_in_procedures[0]['line number']
        for i in range(len(decl_in_procedures)):
            if isinstance(decl_in_procedures[i]['identifier'], str):
                args.append(decl_in_procedures[i]['identifier'])
            elif isinstance(decl_in_procedures[i]['identifier'], dict):
                args.append(decl_in_procedures[i]['identifier']['identifier'])
        for i in range(len(procedures_head['arguments declarations'])):
            head.append(procedures_head['arguments declarations'][i]['argument']['identifier'])
        for i in range(len(args)):
            for j in range(len(head)):
                if args[i] == head[j]:
                    is_conflict = True
                    break

        if is_conflict == True:
            raise ValueError("ERROR: There is a variable name conflict in line " + str(line_number)) 

    def checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(self, declarations, arguments_declarations, identifier, ident_can_be_int):
        is_declared_identifier = False
        is_correct_type_for_identifier_in_declarations = True
        for j in range(len(declarations)):
            ident = declarations[j]["identifier"]
            if isinstance(ident, dict):
                if identifier == ident["identifier"]:
                    is_correct_type_for_identifier_in_declarations = False
            if identifier == ident:
                is_declared_identifier = True
                is_correct_type_for_identifier_in_declarations = True
            else:
                if ident_can_be_int == True:                
                    if isinstance(identifier, int):
                        is_declared_identifier = True
                        is_correct_type_for_identifier_in_declarations = True

        is_passed_identifier_in_proc_head = False
        is_correct_type_for_identifier_in_proc_head = True
        if len(arguments_declarations) == 0:
            is_passed_identifier_in_proc_head = False
            is_correct_type_for_identifier_in_proc_head = True
        else:
            for z in range(len(arguments_declarations)):
                argument = arguments_declarations[z]["argument"]
                ident = argument["identifier"]
                is_array = argument["isArray"]                   
                if identifier == ident:
                    if is_array == False and is_passed_identifier_in_proc_head == False:
                        is_passed_identifier_in_proc_head = True
                        is_correct_type_for_identifier_in_proc_head = True
                    else:
                        if ident_can_be_int == True:
                            if isinstance(identifier, int):
                                is_passed_identifier_in_proc_head = True
                                is_correct_type_for_identifier_in_proc_head = True
                        if is_array == True:
                            is_correct_type_for_identifier_in_proc_head = False

        if is_correct_type_for_identifier_in_declarations == False or is_correct_type_for_identifier_in_proc_head == False:
            is_correct_type = False
        else: 
            is_correct_type = True

        return is_declared_identifier, is_passed_identifier_in_proc_head, is_correct_type

    def checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(self, declarations, arguments_declarations, identifier):
        is_declared_array_identifier = False
        is_correct_type_for_array_identifier_in_declarations = True
        for j in range(len(declarations)):
            ident = declarations[j]["identifier"]
            if isinstance(ident, dict):
                if identifier == ident["identifier"]:
                    is_correct_type_for_array_identifier_in_declarations = True
                    is_declared_array_identifier = True
            if identifier == ident:
                is_declared_array_identifier = False
                is_correct_type_for_array_identifier_in_declarations = False

        is_passed_array_identifier_in_proc_head = False
        is_correct_type_for_array_identifier_in_proc_head = True
        if len(arguments_declarations) == 0:
            is_passed_array_identifier_in_proc_head = False
            is_correct_type_for_array_identifier_in_proc_head = True
        else:
            for z in range(len(arguments_declarations)):
                argument = arguments_declarations[z]["argument"]
                ident = argument["identifier"]
                is_array = argument["isArray"]                   
                if identifier == ident:
                    if is_array == True and is_passed_array_identifier_in_proc_head == False:
                        is_passed_array_identifier_in_proc_head = True
                        is_correct_type_for_array_identifier_in_proc_head = True
                    else:
                        if is_array == False:
                            is_correct_type_for_array_identifier_in_proc_head = False

        if is_correct_type_for_array_identifier_in_declarations == False or is_correct_type_for_array_identifier_in_proc_head == False:
            is_correct_type = False
        else: 
            is_correct_type = True

        return is_declared_array_identifier, is_passed_array_identifier_in_proc_head, is_correct_type  
    
    def checkWhetherTheCalledProcedureExistsAndWhetherItsUseIsCorrect(self, identifier, procedures, line_number, list_of_arguments, type):
        proc_call = identifier + "("
        for j in range(len(list_of_arguments)):
            argument = list_of_arguments[j]['argument ' + str(j+1)]
            proc_call += argument
            if j < len(list_of_arguments)-1:
                proc_call += ", "
        proc_call += ")"
        if type == 'main':
            for i in range(len(procedures)):
                is_procedure_exists_for_main = False
                procedure_identifier = procedures[i]['procedure identifier']
                if type == 'main':
                    if identifier == procedure_identifier:
                        is_procedure_exists_for_main = True
                        break
            if is_procedure_exists_for_main == False:
                raise ValueError("ERROR: In line " + str(line_number) + " in the " + proc_call + " undeclared procedure is called") 
        else:
            for i in range(len(procedures)):
                is_procedure_exists_for_procedure = False
                is_correct_use = False
                procedure_identifier = procedures[i]['procedure identifier']
                if identifier == procedure_identifier:
                    if identifier == type:
                        is_procedure_exists_for_procedure = True
                        is_correct_use = False
                        break
                    else:
                        is_procedure_exists_for_procedure = True
                        is_correct_use = True
                        break
                    
            if is_procedure_exists_for_procedure == False and is_correct_use == False:
                raise ValueError("ERROR: In line " + str(line_number) + " in the " + proc_call + " undeclared procedure is called") 
            elif is_procedure_exists_for_procedure == True and is_correct_use == False:
                raise ValueError("ERROR: In line " + str(line_number) + " in the " + proc_call + " invalid procedure is called")

    def checkForUndeclaredVariablesAndIfTypeIsCorrectInProcCall(self, declarations, arguments_declarations, identifier, list_of_arguments, procedures_head, line_number):
        proc_call = identifier + "("
        for j in range(len(list_of_arguments)):
            argument = list_of_arguments[j]['argument ' + str(j+1)]
            proc_call += argument
            if j < len(list_of_arguments)-1:
                proc_call += ", "
        proc_call += ")"
        args = []
        for j in range(len(procedures_head)):
            if identifier == procedures_head[j]['procedure identifier']:
                head_of_procedure = procedures_head[j]['arguments declarations']
                for z in range(len(head_of_procedure)):
                    is_array = head_of_procedure[z]['argument']['isArray']
                    args.append(is_array)
        if len(args) != 0:
            for i in range(len(list_of_arguments)):
                argument = list_of_arguments[i]['argument ' + str(i+1)]
                is_declared_identifier = False
                is_correct_type = False
                for j in range(len(declarations)):
                    ident = declarations[j]["identifier"]
                    if isinstance(ident, dict):
                        if argument == ident["identifier"] and args[i] == True:
                            is_declared_identifier = True
                            is_correct_type = True
                        elif argument == ident["identifier"] and args[i] == False:
                            is_declared_identifier = True
                            is_correct_type = False
                    elif isinstance(ident, str):
                        if argument == ident and args[i] == False:
                            is_declared_identifier = True
                            is_correct_type = True
                        elif argument == ident and args[i] == True:
                            is_declared_identifier = True
                            is_correct_type = False

                is_passed_identifier_in_proc_head = False
                is_correct_type_in_proc_head = False
                if len(arguments_declarations) == 0:
                    is_passed_identifier_in_proc_head = False
                else:
                    for z in range(len(arguments_declarations)):
                        argument_from_declarations = arguments_declarations[z]["argument"]
                        ident = argument_from_declarations["identifier"] 
                        is_arr = argument_from_declarations["isArray"] 
                        if argument == ident and args[i] == is_arr:
                            if is_passed_identifier_in_proc_head == False and is_correct_type_in_proc_head == False:
                                is_passed_identifier_in_proc_head = True
                                is_correct_type_in_proc_head = True
                        elif argument == ident and args[i] != is_arr:
                            if is_passed_identifier_in_proc_head == False and is_correct_type_in_proc_head == False:
                                is_passed_identifier_in_proc_head = True
                                is_correct_type_in_proc_head = False


                if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + proc_call + " " + "there is an undeclared variable " +  "\'" + str(argument) + "\'") 
                elif is_correct_type == False and is_correct_type_in_proc_head == False:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + proc_call + " " + "there is an incorrect use of variable " +  "\'" + str(argument) + "\'") 

    def checkForUndeclaredVariablesInRead(self, declarations, arguments_declarations, right_side, line_number):
        if isinstance(right_side, str):
            is_declared_identifier, \
            is_passed_identifier_in_proc_head, \
            is_correct_type \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, False)

            if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                if is_correct_type == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(right_side) + "\'" + " " + "there is an undeclared variable " +  "\'" + str(right_side) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(right_side) + "\'" + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")  

        elif isinstance(right_side, dict):
            identifier = right_side["identifier"]
            index = right_side["index"]

            is_declared_identifier, \
            is_passed_identifier_in_proc_head, \
            is_correct_type_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier)

            if isinstance(index, int):
                is_declared_index = True
                is_passed_index_in_proc_head = True
                is_correct_type_index = True
            else:
                is_declared_index, \
                is_passed_index_in_proc_head, \
                is_correct_type_index \
                = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index, True)            

            if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                if is_correct_type_identifier == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an undeclared variable " +  "\'" + str(identifier) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier) + "\'") 

            if is_declared_index == False and is_passed_index_in_proc_head == False:
                if is_correct_type_index == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an undeclared variable " +  "\'" + str(index) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an incorrect use of array variable " +  "\'" + str(index) + "\'") 

    def checkForUndeclaredVariablesInWrite(self, declarations, arguments_declarations, right_side, line_number):
        if isinstance(right_side, str):
            is_declared_identifier, \
            is_passed_identifier_in_proc_head, \
            is_correct_type \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, False)

            if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                if is_correct_type == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(right_side) + "\'" + " " + "there is an undeclared variable " +  "\'" + str(right_side) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(right_side) + "\'" + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")  

        elif isinstance(right_side, dict):
            identifier = right_side["identifier"]
            index = right_side["index"]

            is_declared_identifier, \
            is_passed_identifier_in_proc_head, \
            is_correct_type_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier)

            if isinstance(index, int):
                is_declared_index = True
                is_passed_index_in_proc_head = True
                is_correct_type_index = True
            else:
                is_declared_index, \
                is_passed_index_in_proc_head, \
                is_correct_type_index \
                = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index, True)             

            if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                if is_correct_type_identifier == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an undeclared variable " +  "\'" + str(identifier) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier) + "\'") 

            if is_declared_index == False and is_passed_index_in_proc_head == False:
                if is_correct_type_index == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an undeclared variable " +  "\'" + str(index) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an incorrect use of array variable " +  "\'" + str(index) + "\'") 

    def checkForUndeclaredVariablesInCondition(self, declarations, arguments_declarations, left_side, right_side, operator, line_number):
        if isinstance(left_side, str) and (isinstance(right_side, str) or isinstance(right_side, int)):
            is_declared_identifier_left, \
            is_passed_identifier_left_in_proc_head, \
            is_correct_type1 \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side, True)

            is_declared_identifier_right, \
            is_passed_identifier_right_in_proc_head, \
            is_correct_type2 \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, True)

            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                if is_correct_type1 == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")                                                    
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type2 == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")

        elif isinstance(left_side, dict) and (isinstance(right_side, str) or isinstance(right_side, int)):
            left_side_identifier = left_side["identifier"]
            left_side_index = left_side["index"]

            is_declared_identifier_left, \
            is_passed_identifier_left_in_proc_head, \
            is_correct_type_left_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_identifier)

            is_declared_index_left, \
            is_passed_index_left_in_proc_head, \
            is_correct_type_left_index \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_index, True)

            is_declared_identifier_right, \
            is_passed_identifier_right_in_proc_head, \
            is_correct_type_right \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, True)

            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                if is_correct_type_left_identifier == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side_identifier) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an incorrect use of integer variable " +  "\'" + str(left_side_identifier) + "\'")                                                   
            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                if is_correct_type_left_index == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(left_side_index) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side_index) + "\'")
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type_right == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")     

        elif isinstance(left_side, str) and isinstance(right_side, dict):
            right_side_identifier = right_side["identifier"]
            right_side_index = right_side["index"]

            is_declared_identifier_left, \
            is_passed_identifier_left_in_proc_head, \
            is_correct_type_left \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side, False)            

            is_declared_identifier_right, \
            is_passed_identifier_right_in_proc_head, \
            is_correct_type_right_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_identifier)

            is_declared_index_right, \
            is_passed_index_right_in_proc_head, \
            is_correct_type_right_index \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_index, True)

            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                if is_correct_type_left == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an undeclared variable " + "\'" + str(left_side) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'") 
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type_right_identifier == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an undeclared variable " +  "\'" + str(right_side_identifier) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an incorrect use of integer variable " +  "\'" + str(right_side_identifier) + "\'")                                                   
            if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                if is_correct_type_right_index == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an undeclared variable " + "\'" + str(right_side_index) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side_index) + "\'")

        elif isinstance(left_side, dict) and isinstance(right_side, dict):
            left_side_identifier = left_side["identifier"]
            left_side_index = left_side["index"]
            right_side_identifier = right_side["identifier"]
            right_side_index = right_side["index"]

            is_declared_identifier_left, \
            is_passed_identifier_left_in_proc_head, \
            is_correct_type_left_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_identifier)

            is_declared_index_left, \
            is_passed_index_left_in_proc_head, \
            is_correct_type_left_index \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_index, True)

            is_declared_identifier_right, \
            is_passed_identifier_right_in_proc_head, \
            is_correct_type_right_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_identifier)

            is_declared_index_right, \
            is_passed_index_right_in_proc_head, \
            is_correct_type_right_index \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_index, True)

            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                if is_correct_type_left_identifier == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an undeclared variable " +  "\'" + str(left_side_identifier) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an incorrect use of integer variable " +  "\'" + str(left_side_identifier) + "\'")                                                   
            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                if is_correct_type_left_index == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an undeclared variable " + "\'" + str(left_side_index) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side_index) + "\'")
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type_right_identifier == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an undeclared variable " +  "\'" + str(right_side_identifier) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an incorrect use of integer variable " +  "\'" + str(right_side_identifier) + "\'")                                                   
            if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                if is_correct_type_right_index == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an undeclared variable " + "\'" + str(right_side_index) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side_index) + "\'")

    def checkForUndeclaredVariablesInAssign(self, declarations, arguments_declarations, left_side, right_side, line_number):
        if isinstance(left_side, str) and (isinstance(right_side, str) or isinstance(right_side, int)):
            is_declared_identifier_left, \
            is_passed_identifier_left_in_proc_head, \
            is_correct_type1 \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side, False)

            is_declared_identifier_right, \
            is_passed_identifier_right_in_proc_head, \
            is_correct_type2 \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, True)

            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                if is_correct_type1 == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) +  ":=" + str(right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'") 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) +  ":=" + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")                                                    
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type2 == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) +  ":=" + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) +  ":=" + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")      

        elif isinstance(left_side, dict) and (isinstance(right_side, str) or isinstance(right_side, int)):
            identifier_left = left_side["identifier"]
            index_left = left_side["index"]

            is_declared_identifier_left, \
            is_passed_identifier_left_in_proc_head, \
            is_correct_type_of_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)

            if isinstance(index_left, int):
                is_declared_index_left = True
                is_passed_index_left_in_proc_head = True
                is_correct_type_of_index = True
            else:
                is_declared_index_left, \
                is_passed_index_left_in_proc_head, \
                is_correct_type_of_index \
                = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)

            if isinstance(right_side, int):
                is_declared_identifier_right = True
                is_passed_identifier_right_in_proc_head = True
                is_correct_type = True
            else:
                is_declared_identifier_right, \
                is_passed_identifier_right_in_proc_head, \
                is_correct_type \
                = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, True)

            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                if is_correct_type_of_identifier == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")    
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")               
            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                if is_correct_type_of_index == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " " + "of an array" ) 
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'")                                      
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type == True:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(right_side) + "\'")

        elif isinstance(left_side, str) and isinstance(right_side, dict):
            if len(right_side) == 2:
                identifier_right = right_side["identifier"]
                index_right = right_side["index"]

                is_declared_identifier_left, \
                is_passed_identifier_left_in_proc_head, \
                is_correct_type \
                = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side, False)  

                is_declared_identifier_right, \
                is_passed_identifier_right_in_proc_head, \
                is_correct_type_of_identifier \
                = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_right)

                is_declared_index_right, \
                is_passed_index_right_in_proc_head, \
                is_correct_type_of_index \
                = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_right, True)

                if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                    if is_correct_type == True:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared variable " + "\'" + str(left_side) + "\'")
                    else:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of array variable " + "\'" + str(left_side) + "\'")                        
                if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                    if is_correct_type_of_identifier == True:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared identifier " +  "\'" + str(identifier_right) + "\'" + " of an array")  
                    else:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_right) + "\'")                  
                if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                    if is_correct_type_of_index == True:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared index " +  "\'" + str(index_right) + "\'" + " " + "of an array")   
                    else:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(index_right) + "\'") 

            elif len(right_side) == 3:
                left_side_of_right_side = right_side["left"]
                right_side_of_right_side = right_side["right"]
                if (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)): 

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type1 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side, False)

                    is_declared_identifier_left_of_right_side, \
                    is_passed_identifier_left_of_right_side_in_proc_head, \
                    is_correct_type2 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side, True)

                    is_declared_identifier_right_of_right_side, \
                    is_passed_identifier_right_of_right_side_in_proc_head, \
                    is_correct_type3 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side, True)                            
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type1 == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'")     
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")                                                                             
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " + "\'" + str(left_side_of_right_side) + "\'")   
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side) + "\'")                                                               
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type3 == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side_of_right_side) + "\'")
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side) + "\'")                            

                elif isinstance(left_side_of_right_side, dict) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)):
                    left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                    left_side_of_right_side_index = left_side_of_right_side["index"]

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type1 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side, False)

                    is_declared_left_side_of_right_side_identifier, \
                    is_passed_left_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_identifier)

                    is_declared_left_side_of_right_side_index, \
                    is_passed_left_side_of_right_side_index_in_proc_head, \
                    is_correct_type_of_index \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_index, True)

                    is_declared_identifier_right_of_right_side, \
                    is_passed_identifier_right_of_right_side_in_proc_head, \
                    is_correct_type2 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side, True)                             
 
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type1:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'")  
                        else: 
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")                                                                                
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")  
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                        
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " +  "\'" + str(right_side_of_right_side) + "\'") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side_of_right_side) + "\'")                            

                elif (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and isinstance(right_side_of_right_side, dict):  
                    right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                    right_side_of_right_side_index = right_side_of_right_side["index"]

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type1 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side, False)

                    is_declared_right_side_of_right_side_identifier, \
                    is_passed_right_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_identifier)

                    is_declared_right_side_of_right_side_index, \
                    is_passed_right_side_of_right_side_index_in_proc_head, \
                    is_correct_type_of_index \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_index, True)

                    is_declared_identifier_left_of_right_side, \
                    is_passed_identifier_left_of_right_side_in_proc_head, \
                    is_correct_type2 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side, True)   

                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type1 == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'")   
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")  
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'")
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(left_side_of_right_side) + "\'")                                                                                                          
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array")  
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                               
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")   
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")                                                       
                elif isinstance(left_side_of_right_side, dict) and isinstance(right_side_of_right_side, dict):
                    is_declared_identifier_left = False

                    right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                    right_side_of_right_side_index = right_side_of_right_side["index"]


                    left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                    left_side_of_right_side_index = left_side_of_right_side["index"]

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side, False)

                    is_declared_right_side_of_right_side_identifier, \
                    is_passed_right_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_right \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_identifier)

                    is_declared_right_side_of_right_side_index, \
                    is_passed_right_side_of_right_side_index_in_proc_head, \
                    is_correct_type_of_index_right \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_index, True)                         

                    is_declared_left_side_of_right_side_identifier, \
                    is_passed_left_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_left \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_identifier)

                    is_declared_left_side_of_right_side_index, \
                    is_passed_left_side_of_right_side_index_in_proc_head, \
                    is_correct_type_of_index_left \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_index, True)    
     
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'")     
                        else:                                     
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")       
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                          
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" " of an array")
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                              
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")
                        else:                                                                                       
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")
        elif isinstance(left_side, dict) and isinstance(right_side, dict):
            if len(right_side) == 2:
                identifier_left = left_side["identifier"]
                index_left = left_side["index"]

                identifier_right = right_side["identifier"]
                index_right = right_side["index"]

                is_declared_identifier_left, \
                is_passed_identifier_left_in_proc_head, \
                is_correct_type_of_identifier_left \
                = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)

                if isinstance(index_left, int):   
                    is_declared_index_left = True
                    is_passed_index_left_in_proc_head = True
                    is_correct_type_of_index_left = True
                else:
                    is_declared_index_left, \
                    is_passed_index_left_in_proc_head, \
                    is_correct_type_of_index_left \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)  

                if isinstance(index_right, int):
                    is_declared_index_right = True
                    is_passed_index_right_in_proc_head = True
                    is_correct_type_of_index_right = True
                else:                  
                    is_declared_index_right, \
                    is_passed_index_right_in_proc_head, \
                    is_correct_type_of_index_right \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_right, True) 

                is_declared_identifier_right, \
                is_passed_identifier_right_in_proc_head, \
                is_correct_type_of_identifier_right \
                = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_right)

                if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                    if is_correct_type_of_identifier_left == True:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared identifier "  +  "\'" + str(identifier_left) + "\'" " of an array")
                    else:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of integer variable "  +  "\'" + str(identifier_left) + "\'")                        
                if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                    if is_correct_type_of_index_left == True:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " " + "of an array") 
                    else:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'")                        
                if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                    if is_correct_type_of_identifier_right == True:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared identifier "  +  "\'" + str(identifier_right) + "\'" " of an array")   
                    else:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of integer variable "  +  "\'" + str(identifier_right) + "\'")                                        
                if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                    if is_correct_type_of_index_right == True:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared index " +  "\'" + str(index_right) + "\'" + " " + "of an array")
                    else:
                        raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(index_right) + "\'")   
                                             
            elif len(right_side) == 3:
                left_side_of_right_side = right_side["left"]
                right_side_of_right_side = right_side["right"]
                if (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)):
                    identifier_left = left_side["identifier"]
                    index_left = left_side["index"]

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type_of_identifier \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)
                    
                    if isinstance(index_left, int):
                        is_declared_index_left = True
                        is_passed_index_left_in_proc_head = True
                        is_correct_type_of_index = True
                    else:
                        is_declared_index_left, \
                        is_passed_index_left_in_proc_head, \
                        is_correct_type_of_index \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True) 

                    if isinstance(left_side_of_right_side, int):  
                        is_declared_identifier_left_of_right_side = True
                        is_passed_identifier_left_of_right_side_in_proc_head = True
                        is_correct_type1 = True
                    else:
                        is_declared_identifier_left_of_right_side, \
                        is_passed_identifier_left_of_right_side_in_proc_head, \
                        is_correct_type1 \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side, True)

                    if isinstance(right_side_of_right_side, int):
                        is_declared_identifier_right_of_right_side = True
                        is_passed_identifier_right_of_right_side_in_proc_head = True
                        is_correct_type2 = True
                    else:
                        is_declared_identifier_right_of_right_side, \
                        is_passed_identifier_right_of_right_side_in_proc_head, \
                        is_correct_type2 \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side, True)                                                         

                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")                               
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")  
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'" + " of an array")                                                                                                                
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type1 == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " + "\'" + str(left_side_of_right_side) + "\'") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side) + "\'")                                                                 
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side_of_right_side) + "\'")
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side) + "\'")                            

                elif isinstance(left_side_of_right_side, dict) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)):
                    left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                    left_side_of_right_side_index = left_side_of_right_side["index"]

                    identifier_left = left_side["identifier"]
                    index_left = left_side["index"]                            

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type_of_identifier \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)
                    
                    if isinstance(index_left, int):
                        is_declared_index_left = True
                        is_passed_index_left_in_proc_head = True
                        is_correct_type_of_index = True
                    else:
                        is_declared_index_left, \
                        is_passed_index_left_in_proc_head, \
                        is_correct_type_of_index \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)  

                    is_declared_left_side_of_right_side_identifier, \
                    is_passed_left_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_left \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_identifier)

                    if isinstance(left_side_of_right_side_index, int):
                        is_declared_left_side_of_right_side_index = True
                        is_passed_left_side_of_right_side_index_in_proc_head = True
                        is_correct_type_of_index_left = True
                    else:                     
                        is_declared_left_side_of_right_side_index, \
                        is_passed_left_side_of_right_side_index_in_proc_head, \
                        is_correct_type_of_index_left \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_index, True) 

                    if isinstance(right_side_of_right_side, int):
                        is_declared_identifier_right_of_right_side = True
                        is_passed_identifier_right_of_right_side_in_proc_head = True
                        is_correct_type = True
                    else:
                        is_declared_identifier_right_of_right_side, \
                        is_passed_identifier_right_of_right_side_in_proc_head, \
                        is_correct_type \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side, True)                                           
 
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")                            
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")   
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'")                                                                                                                
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")     
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                            
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")  
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                        
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " +  "\'" + str(right_side_of_right_side) + "\'") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side_of_right_side) + "\'")

                elif (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and isinstance(right_side_of_right_side, dict):  
                    right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                    right_side_of_right_side_index = right_side_of_right_side["index"]

                    identifier_left = left_side["identifier"]
                    index_left = left_side["index"]                            

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type_of_identifier \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)
                    
                    if isinstance(index_left, int):
                        is_declared_index_left = True
                        is_passed_index_left_in_proc_head = True
                        is_correct_type_of_index = True
                    else:
                        is_declared_index_left, \
                        is_passed_index_left_in_proc_head, \
                        is_correct_type_of_index \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)  

                    if isinstance(left_side_of_right_side, int):
                        is_declared_identifier_left_of_right_side = True
                        is_passed_identifier_left_of_right_side_in_proc_head = True
                        is_correct_type = True
                    else:
                        is_declared_identifier_left_of_right_side, \
                        is_passed_identifier_left_of_right_side_in_proc_head, \
                        is_correct_type \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side, True)                                     

                    is_declared_right_side_of_right_side_identifier, \
                    is_passed_right_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_right \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_identifier)

                    if isinstance(right_side_of_right_side_index, int):
                        is_declared_right_side_of_right_side_index = True
                        is_passed_right_side_of_right_side_index_in_proc_head = True
                        is_correct_type_of_index_right = True
                    else:
                        is_declared_right_side_of_right_side_index, \
                        is_passed_right_side_of_right_side_index_in_proc_head, \
                        is_correct_type_of_index_right \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_index, True)       
 
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")                            
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")    
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'")                            
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'")
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(left_side_of_right_side) + "\'")                                                                   
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")   
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")                                                       

                elif isinstance(left_side_of_right_side, dict) and isinstance(right_side_of_right_side, dict):

                    right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                    right_side_of_right_side_index = right_side_of_right_side["index"]

                    left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                    left_side_of_right_side_index = left_side_of_right_side["index"]
 
                    identifier_left = left_side["identifier"]
                    index_left = left_side["index"]                             

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type_of_identifier \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)
                    
                    if isinstance(index_left, int):
                        is_declared_index_left = True
                        is_passed_index_left_in_proc_head = True
                        is_correct_type_of_index = True
                    else:
                        is_declared_index_left, \
                        is_passed_index_left_in_proc_head, \
                        is_correct_type_of_index \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)    

                    is_declared_left_side_of_right_side_identifier, \
                    is_passed_left_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_left \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_identifier)

                    if isinstance(left_side_of_right_side_index, int):
                        is_declared_left_side_of_right_side_index = True
                        is_passed_left_side_of_right_side_index_in_proc_head = True
                        is_correct_type_of_index_left = True 
                    else:                    
                        is_declared_left_side_of_right_side_index, \
                        is_passed_left_side_of_right_side_index_in_proc_head, \
                        is_correct_type_of_index_left \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_index, True)                            

                    is_declared_right_side_of_right_side_identifier, \
                    is_passed_right_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_right \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_identifier)

                    if isinstance(right_side_of_right_side_index, int):
                        is_declared_right_side_of_right_side_index = True
                        is_passed_right_side_of_right_side_index_in_proc_head = True
                        is_correct_type_of_index_right = True
                    else:
                        is_declared_right_side_of_right_side_index, \
                        is_passed_right_side_of_right_side_index_in_proc_head, \
                        is_correct_type_of_index_right \
                        = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_index, True)                              
  
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")  
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")                             
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(index_left) + "\'" + " of an array")    
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(index_left) + "\'")  
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")   
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                               
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                                                                                                                    
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array")   
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                              
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array") 
                        else:
                            raise ValueError("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")
    