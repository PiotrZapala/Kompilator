class Debugger:
    def __init__(self):
        self.errors = []

    def programDebugger(self, main_commands_array, decl_in_main, procedure_commands_array, decl_in_procedures,  procedures_head):
        main_program_errors = self.checkIfThereAreUndeclaredVariables(main_commands_array, decl_in_main, None)
        if len(main_program_errors) != 0:
            print("In Main Program there are some issues:")
            for k in range(len(main_program_errors)):
                print(main_program_errors[k])
        for i in range(len(procedures_head)):
            procedure_errors = self.checkIfThereAreUndeclaredVariables(procedure_commands_array[i], decl_in_procedures[i], procedures_head[i])
            if len(procedure_errors) != 0:
                print("In procedure:", "\'" + procedures_head[i]["procedure identifier"] + "\'" + " there are some issues:")
                for j in range(len(procedure_errors)):
                    print(procedure_errors[j])


    def checkIfThereAreUndeclaredVariables(self, list_of_commands, declarations, head):
        if head != None:
            arguments_declarations = head["arguments declarations"]
        else:
            arguments_declarations = []
        for i in range(len(list_of_commands)):
            if list_of_commands[i]["command type"] == "Assign":
                left_side = list_of_commands[i]["left side"]
                right_side = list_of_commands[i]["right side"]
                self.checkForUndeclaredVariablesInAssign(declarations, arguments_declarations, left_side, right_side)
                                                 
            elif list_of_commands[i]["command type"] == "Read":                   
                pass
            elif list_of_commands[i]["command type"] == "Write":                   
                pass
            elif list_of_commands[i]["command type"] == "Procedure Call":                   
                pass
            elif list_of_commands[i]["command type"] == "While Do":                   
                pass
            elif list_of_commands[i]["command type"] == "Repeat Until":                   
                pass
            elif list_of_commands[i]["command type"] == "If":                   
                pass

        return self.errors

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
    
    def checkForUndeclaredVariablesInAssign(self, declarations, arguments_declarations, left_side, right_side):
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
                    self.errors.append("ERROR: In " + str(left_side) +  ":=" + str(right_side) + " " + "there is undeclared variable " +  "\'" + str(left_side) + "\'") 
                else:
                    self.errors.append("ERROR: In " + str(left_side) +  ":=" + str(right_side) + " " + "improper use of array variable " +  "\'" + str(left_side) + "\'")                                                    
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type2 == True:
                    self.errors.append("ERROR: In " + str(left_side) +  ":=" + str(right_side) + " " + "there is undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    self.errors.append("ERROR: In " + str(left_side) +  ":=" + str(right_side) + " " + "improper use of array variable " +  "\'" + str(right_side) + "\'")      

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
                    self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")    
                else:
                    self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "improper use of integer variable " +  "\'" + str(identifier_left) + "\'")               
            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                if is_correct_type_of_index == True:
                    self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is undeclared index " +  "\'" + str(index_left) + "\'" + " " + "of an array" ) 
                else:
                    self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "improper use of array variable " +  "\'" + str(index_left) + "\'")                                      
            if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                if is_correct_type == True:
                    self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "there is undeclared variable " + "\'" + str(right_side) + "\'")
                else:
                    self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(right_side) + " " + "improper use of array variable " + "\'" + str(right_side) + "\'")

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
                        self.errors.append("ERROR: In " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is undeclared variable " + "\'" + str(left_side) + "\'")
                    else:
                        self.errors.append("ERROR: In " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "improper use of array variable " + "\'" + str(left_side) + "\'")                        
                if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                    if is_correct_type_of_identifier == True:
                        self.errors.append("ERROR: In " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is undeclared identifier " +  "\'" + str(identifier_right) + "\'" + " of an array")  
                    else:
                        self.errors.append("ERROR: In " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "improper use of integer variable " +  "\'" + str(identifier_right) + "\'")                  
                if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                    if is_correct_type_of_index == True:
                        self.errors.append("ERROR: In " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is undeclared index " +  "\'" + str(index_right) + "\'" + " " + "of an array")   
                    else:
                        self.errors.append("ERROR: In " + str(left_side) + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "improper use of array variable " +  "\'" + str(index_right) + "\'") 

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
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared variable " +  "\'" + str(left_side) + "\'")     
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " +  "\'" + str(left_side) + "\'")                                                                             
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared variable " + "\'" + str(left_side_of_right_side) + "\'")   
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " + "\'" + str(left_side_of_right_side) + "\'")                                                               
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type3 == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared variable " + "\'" + str(right_side_of_right_side) + "\'")
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " + "\'" + str(right_side_of_right_side) + "\'")                            

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
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared variable " +  "\'" + str(left_side) + "\'")  
                        else: 
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " +  "\'" + str(left_side) + "\'")                                                                                
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                        
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared variable " +  "\'" + str(right_side_of_right_side) + "\'") 
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " +  "\'" + str(right_side_of_right_side) + "\'")                            

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
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared variable " +  "\'" + str(left_side) + "\'")   
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " +  "\'" + str(left_side) + "\'")  
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'")
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " +  "\'" + str(left_side_of_right_side) + "\'")                                                                                                          
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                               
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")                                                       
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
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared variable " +  "\'" + str(left_side) + "\'")     
                        else:                                     
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " +  "\'" + str(left_side) + "\'")
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")       
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                          
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" " of an array")
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                              
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")
                        else:                                                                                       
                            self.errors.append("ERROR: In " + str(left_side) + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")
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
                        self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is undeclared identifier "  +  "\'" + str(identifier_left) + "\'" " of an array")
                    else:
                        self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "improper use of integer variable "  +  "\'" + str(identifier_left) + "\'")                        
                if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                    if is_correct_type_of_index_left == True:
                        self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is undeclared index " +  "\'" + str(index_left) + "\'" + " " + "of an array") 
                    else:
                        self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "improper use of array variable " +  "\'" + str(index_left) + "\'")                        
                if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                    if is_correct_type_of_identifier_right == True:
                        self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is undeclared identifier "  +  "\'" + str(identifier_right) + "\'" " of an array")   
                    else:
                        self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "improper use of integer variable "  +  "\'" + str(identifier_right) + "\'")                                        
                if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                    if is_correct_type_of_index_right == True:
                        self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "there is undeclared index " +  "\'" + str(index_right) + "\'" + " " + "of an array")
                    else:
                        self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(identifier_right) +  "[" +str(index_right) + "]" + " " + "improper use of array variable " +  "\'" + str(index_right) + "\'")                        
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
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of integer variable " +  "\'" + str(identifier_left) + "\'")                               
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " +  "\'" + str(index_left) + "\'" + " of an array")                                                                                                                
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type1 == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared variable " + "\'" + str(left_side_of_right_side) + "\'") 
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " + "\'" + str(left_side_of_right_side) + "\'")                                                                 
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type2 == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared variable " + "\'" + str(right_side_of_right_side) + "\'")
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side) + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " + "\'" + str(right_side_of_right_side) + "\'")                            

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
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of integer variable " +  "\'" + str(identifier_left) + "\'")                            
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " +  "\'" + str(index_left) + "\'")                                                                                                                
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")     
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                            
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                        
                    if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                        if is_correct_type == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "there is undeclared variable " +  "\'" + str(right_side_of_right_side) + "\'") 
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"])  + str(right_side_of_right_side) + " " + "improper use of array variable " +  "\'" + str(right_side_of_right_side) + "\'")

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
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of integer variable " +  "\'" + str(identifier_left) + "\'")                            
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared index " +  "\'" + str(index_left) + "\'" + " of an array")    
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " +  "\'" + str(index_left) + "\'")                            
                    if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                        if is_correct_type == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'")
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " +  "\'" + str(left_side_of_right_side) + "\'")                                                                   
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                                
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side)  + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")                                                       

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
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared identifier " +  "\'" + str(identifier_left) + "\'" + " of an array")  
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of integer variable " +  "\'" + str(identifier_left) + "\'")                             
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        if is_correct_type_of_index == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared index " + "\'" + str(index_left) + "\'" + " of an array")    
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " + "\'" + str(index_left) + "\'")  
                    if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_left == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared identifier " + "\'" + str(left_side_of_right_side_identifier) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of integer variable " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                                               
                    if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_left == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared index " + "\'" + str(left_side_of_right_side_index) + "\'" + " of an array")
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " + "\'" + str(left_side_of_right_side_index) + "\'")                                                                                                                                                    
                    if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                        if is_correct_type_of_identifier_right == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared identifier " + "\'" + str(right_side_of_right_side_identifier) + "\'" + " of an array")   
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of integer variable " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                                              
                    if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                        if is_correct_type_of_index_right == True:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "there is undeclared index " + "\'" + str(right_side_of_right_side_index) + "\'" + " of an array") 
                        else:
                            self.errors.append("ERROR: In " + str(identifier_left) + "[" +str(index_left) + "]" + ":=" + str(left_side_of_right_side_identifier) +  "[" +str(left_side_of_right_side_index) + "]" + str(right_side["operator"]) + str(right_side_of_right_side_identifier) +  "[" +str(right_side_of_right_side_index) + "]" +  " " + "improper use of array variable " + "\'" + str(right_side_of_right_side_index) + "\'")
    