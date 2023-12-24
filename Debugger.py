class Debugger:

    def __init__(self):
        self.errors = []
        self.warnings = []

    def programDebugger(self, main_commands_array, decl_in_main, procedure_commands_array, decl_in_procedures,  procedures_head):
        self.checkIfThereAreUndeclaredVariables(main_commands_array, decl_in_main, None)
        if len(self.errors) != 0:
            print("In Main Program there are some issues:")
            for k in range(len(self.errors)):
                print(self.errors[k])
        length_of_errors = len(self.errors)
        for i in range(len(procedures_head)):
            self.checkIfThereAreUndeclaredVariables(procedure_commands_array[i], decl_in_procedures[i], procedures_head[i])
            if len(self.errors) != 0:
                print("In procedure:", "\'" + procedures_head[i]["procedure identifier"] + "\'" + " there are some issues:")
                for j in range(length_of_errors, len(self.errors)):
                    print(self.errors[j])
            length_of_errors = len(self.errors)


    def checkIfThereAreUndeclaredVariables(self, list_of_commands, declarations, head):
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
                pass

            elif list_of_commands[i]["command type"] == "While Do":                   
                condition = list_of_commands[i]["condition"]
                commands = list_of_commands[i]["commands"]
                line_number = list_of_commands[i]["line number"]
                left_side = condition["left"]
                operator = condition["operator"]
                right_side = condition["right"]
                self.checkForUndeclaredVariablesInCondition(declarations, arguments_declarations, left_side, right_side, operator, line_number)
                self.checkIfThereAreUndeclaredVariables(commands, declarations, head)

            elif list_of_commands[i]["command type"] == "Repeat Until":                   
                condition = list_of_commands[i]["condition"]
                commands = list_of_commands[i]["commands"]
                line_number = list_of_commands[i]["line number"]
                left_side = condition["left"]
                operator = condition["operator"]
                right_side = condition["right"]
                self.checkIfThereAreUndeclaredVariables(commands, declarations, head)                
                self.checkForUndeclaredVariablesInCondition(declarations, arguments_declarations, left_side, right_side, operator, line_number)

            elif list_of_commands[i]["command type"] == "If":                   
                condition = list_of_commands[i]["condition"]
                if_commands = list_of_commands[i]["if commands"]
                else_commands = list_of_commands[i]["else commands"]
                line_number = list_of_commands[i]["line number"]
                left_side = condition["left"]
                operator = condition["operator"]
                right_side = condition["right"]
                if else_commands != None:
                    self.checkForUndeclaredVariablesInCondition(declarations, arguments_declarations, left_side, right_side, operator, line_number)
                    self.checkIfThereAreUndeclaredVariables(if_commands, declarations, head)
                    self.checkIfThereAreUndeclaredVariables(else_commands, declarations, head)
                else:
                    self.checkForUndeclaredVariablesInCondition(declarations, arguments_declarations, left_side, right_side, operator, line_number)
                    self.checkIfThereAreUndeclaredVariables(if_commands, declarations, head)


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

    def checkForUndeclaredVariablesInRead(self, declarations, arguments_declarations, right_side, line_number):
        if isinstance(right_side, str):
            is_declared_identifier, \
            is_passed_identifier_in_proc_head, \
            is_correct_type \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, False)

            if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                if is_correct_type == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(right_side) + "\'" + " " + "there is an undeclared variable " +  "\'" + str(right_side) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(right_side) + "\'" + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")  

        elif isinstance(right_side, dict):
            identifier = right_side["identifier"]
            index = right_side["index"]

            is_declared_identifier, \
            is_passed_identifier_in_proc_head, \
            is_correct_type_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier)

            is_declared_index, \
            is_passed_index_in_proc_head, \
            is_correct_type_index \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index, True)            

            if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                if is_correct_type_identifier == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an undeclared variable " +  "\'" + str(identifier) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier) + "\'") 

            if is_declared_index == False and is_passed_index_in_proc_head == False:
                if is_correct_type_index == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an undeclared variable " +  "\'" + str(index) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "READ " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an incorrect use of array variable " +  "\'" + str(index) + "\'") 

    def checkForUndeclaredVariablesInWrite(self, declarations, arguments_declarations, right_side, line_number):
        if isinstance(right_side, str):
            is_declared_identifier, \
            is_passed_identifier_in_proc_head, \
            is_correct_type \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, False)

            if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                if is_correct_type == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(right_side) + "\'" + " " + "there is an undeclared variable " +  "\'" + str(right_side) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(right_side) + "\'" + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")  

        elif isinstance(right_side, dict):
            identifier = right_side["identifier"]
            index = right_side["index"]

            is_declared_identifier, \
            is_passed_identifier_in_proc_head, \
            is_correct_type_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier)

            is_declared_index, \
            is_passed_index_in_proc_head, \
            is_correct_type_index \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index, True)            

            if is_declared_identifier == False and is_passed_identifier_in_proc_head == False:
                if is_correct_type_identifier == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an undeclared variable " +  "\'" + str(identifier) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier) + "\'") 

            if is_declared_index == False and is_passed_index_in_proc_head == False:
                if is_correct_type_index == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an undeclared variable " +  "\'" + str(index) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + "\'" + "WRITE " + str(identifier) + "[" +str(index) + "]" + "\'" + " " + "there is an incorrect use of array variable " +  "\'" + str(index) + "\'") 

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
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")                                                    
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type2 == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")

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
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side_identifier) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an incorrect use of integer variable " +  "\'" + str(left_side_identifier) + "\'")                                                   
            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                if is_correct_type_left_index == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(left_side_index) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side_index) + "\'")
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type_right == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")     

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
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an undeclared variable " + "\'" + str(left_side) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'") 
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type_right_identifier == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an undeclared variable " +  "\'" + str(right_side_identifier) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an incorrect use of integer variable " +  "\'" + str(right_side_identifier) + "\'")                                                   
            if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                if is_correct_type_right_index == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an undeclared variable " + "\'" + str(right_side_index) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side_index) + "\'")

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
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an undeclared variable " +  "\'" + str(left_side_identifier) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an incorrect use of integer variable " +  "\'" + str(left_side_identifier) + "\'")                                                   
            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                if is_correct_type_left_index == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an undeclared variable " + "\'" + str(left_side_index) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side_index) + "\'")
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type_right_identifier == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an undeclared variable " +  "\'" + str(right_side_identifier) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]"  + " " + "there is an incorrect use of integer variable " +  "\'" + str(right_side_identifier) + "\'")                                                   
            if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                if is_correct_type_right_index == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an undeclared variable " + "\'" + str(right_side_index) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side_identifier) +  "[" + str(left_side_index) + "]" + str(operator) + str(right_side_identifier) +  "[" + str(right_side_index) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side_index) + "\'")

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
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) +  ":=" + str(right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'") 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) +  ":=" + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")                                                    
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type2 == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) +  ":=" + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) +  ":=" + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side) + "\'")      

        elif isinstance(left_side, dict) and (isinstance(right_side, str) or isinstance(right_side, int)):
            identifier_left = left_side["identifier"]
            index_left = left_side["index"]

            is_declared_identifier_left, \
            is_passed_identifier_left_in_proc_head, \
            is_correct_type_of_identifier \
            = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)

            is_declared_index_left, \
            is_passed_index_left_in_proc_head, \
            is_correct_type_of_index \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)

            is_declared_identifier_right, \
            is_passed_identifier_right_in_proc_head, \
            is_correct_type \
            = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side, True)

            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                if is_correct_type_of_identifier == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")    
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")               
            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                if is_correct_type_of_index == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " " + "of an array" ) 
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'")                                      
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type == True:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(right_side) + "\'")

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
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared variable " + "\'" + str(left_side) + "\'")
                    else:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of array variable " + "\'" + str(left_side) + "\'")                        
                if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                    if is_correct_type_of_identifier == True:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared identifier " +  "\'" + str(identifier_right) + "\'" + " of an array")  
                    else:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_right) + "\'")                  
                if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                    if is_correct_type_of_index == True:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared index " +  "\'" + str(index_right) + "\'" + " " + "of an array")   
                    else:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(index_right) + "\'") 

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
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'")     
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")                                                                             
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " + "\'" + str(left_side_of_right_side) + "\'")   
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side) + "\'")                                                               
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type3 == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side_of_right_side) + "\'")
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side) + "\'")                            

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
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'")  
                        else: 
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")                                                                                
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                        
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " +  "\'" + str(right_side_of_right_side) + "\'") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side_of_right_side) + "\'")                            

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
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'")   
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")  
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'")
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(left_side_of_right_side) + "\'")                                                                                                          
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                               
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")                                                       
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
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared variable " +  "\'" + str(left_side) + "\'")     
                        else:                                     
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(left_side) + "\'")
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")       
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                          
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" " of an array")
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                              
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")
                        else:                                                                                       
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")
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
                    
                is_declared_index_left, \
                is_passed_index_left_in_proc_head, \
                is_correct_type_of_index_left \
                = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)  

                is_declared_identifier_right, \
                is_passed_identifier_right_in_proc_head, \
                is_correct_type_of_identifier_right \
                = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_right)
                    
                is_declared_index_right, \
                is_passed_index_right_in_proc_head, \
                is_correct_type_of_index_right \
                = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_right, True)                                                  

                if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                    if is_correct_type_of_identifier_left == True:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared identifier "  +  "\'" + str(identifier_left) + "\'" " of an array")
                    else:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of integer variable "  +  "\'" + str(identifier_left) + "\'")                        
                if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                    if is_correct_type_of_index_left == True:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " " + "of an array") 
                    else:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'")                        
                if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                    if is_correct_type_of_identifier_right == True:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared identifier "  +  "\'" + str(identifier_right) + "\'" " of an array")   
                    else:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of integer variable "  +  "\'" + str(identifier_right) + "\'")                                        
                if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                    if is_correct_type_of_index_right == True:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an undeclared index " +  "\'" + str(index_right) + "\'" + " " + "of an array")
                    else:
                        self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is an incorrect use of array variable " +  "\'" + str(index_right) + "\'")                        
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
                    
                    is_declared_index_left, \
                    is_passed_index_left_in_proc_head, \
                    is_correct_type_of_index \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True) 
                            
                    is_declared_identifier_left_of_right_side, \
                    is_passed_identifier_left_of_right_side_in_proc_head, \
                    is_correct_type1 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side, True)

                    is_declared_identifier_right_of_right_side, \
                    is_passed_identifier_right_of_right_side_in_proc_head, \
                    is_correct_type2 \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side, True)                                                         

                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")                               
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'" + " of an array")                                                                                                                
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type1 == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " + "\'" + str(left_side_of_right_side) + "\'") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side) + "\'")                                                                 
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " + "\'" + str(right_side_of_right_side) + "\'")
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side) + "\'")                            

                elif isinstance(left_side_of_right_side, dict) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)):
                    left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                    left_side_of_right_side_index = left_side_of_right_side["index"]

                    identifier_left = left_side["identifier"]
                    index_left = left_side["index"]                            

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type_of_identifier \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)
                    
                    is_declared_index_left, \
                    is_passed_index_left_in_proc_head, \
                    is_correct_type_of_index \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)   

                    is_declared_left_side_of_right_side_identifier, \
                    is_passed_left_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_left \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_identifier)

                    is_declared_left_side_of_right_side_index, \
                    is_passed_left_side_of_right_side_index_in_proc_head, \
                    is_correct_type_of_index_left \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_index, True) 

                    is_declared_identifier_right_of_right_side, \
                    is_passed_identifier_right_of_right_side_in_proc_head, \
                    is_correct_type \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side, True)                                           
 
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")                            
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'")                                                                                                                
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")     
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                            
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                        
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an undeclared variable " +  "\'" + str(right_side_of_right_side) + "\'") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is an incorrect use of array variable " +  "\'" + str(right_side_of_right_side) + "\'")

                elif (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and isinstance(right_side_of_right_side, dict):  
                    right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                    right_side_of_right_side_index = right_side_of_right_side["index"]

                    identifier_left = left_side["identifier"]
                    index_left = left_side["index"]                            

                    is_declared_identifier_left, \
                    is_passed_identifier_left_in_proc_head, \
                    is_correct_type_of_identifier \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, identifier_left)
                    
                    is_declared_index_left, \
                    is_passed_index_left_in_proc_head, \
                    is_correct_type_of_index \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)    

                    is_declared_identifier_left_of_right_side, \
                    is_passed_identifier_left_of_right_side_in_proc_head, \
                    is_correct_type \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side, True)                                     

                    is_declared_right_side_of_right_side_identifier, \
                    is_passed_right_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_right \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_identifier)

                    is_declared_right_side_of_right_side_index, \
                    is_passed_right_side_of_right_side_index_in_proc_head, \
                    is_correct_type_of_index_right \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_index, True)       
 
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")                            
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")    
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(index_left) + "\'")                            
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'")
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " +  "\'" + str(left_side_of_right_side) + "\'")                                                                   
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")                                                       

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
                    
                    is_declared_index_left, \
                    is_passed_index_left_in_proc_head, \
                    is_correct_type_of_index \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, index_left, True)  

                    is_declared_left_side_of_right_side_identifier, \
                    is_passed_left_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_left \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_identifier)

                    is_declared_left_side_of_right_side_index, \
                    is_passed_left_side_of_right_side_index_in_proc_head, \
                    is_correct_type_of_index_left \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, left_side_of_right_side_index, True)                            

                    is_declared_right_side_of_right_side_identifier, \
                    is_passed_right_side_of_right_side_identifier_in_proc_head, \
                    is_correct_type_of_identifier_right \
                    = self.checkIfArrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_identifier)

                    is_declared_right_side_of_right_side_index, \
                    is_passed_right_side_of_right_side_index_in_proc_head, \
                    is_correct_type_of_index_right \
                    = self.checkIfStrIdentIsDeclaredAndIfTypeIsCorrect(declarations, arguments_declarations, right_side_of_right_side_index, True)                              
  
                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " +  "\'" + str(identifier_left) + "\'")                             
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(index_left) + "\'" + " of an array")    
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(index_left) + "\'")  
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                               
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                                                                                                                    
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                              
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In line " + str(line_number) + " in the " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is an incorrect use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")
    