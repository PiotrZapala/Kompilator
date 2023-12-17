from Node import *

class AbstractSyntaxTree:

    def __init__(self, root):
        self.root = root 
        self.variable_declarations_in_main = []
        self.variable_declarations_in_procedures = []
        self.arguments_declarations_in_procedures_head = []
        self.list_of_main_program_commands = []
        self.list_of_procedure_commands = []
        self.errors = []

    def traverseTreeForCommands(self):
        main = self.root.main
        main_commands_array = main.commands.commands
        self.list_of_main_program_commands = self.getListOfCommands(main_commands_array)
        procedures = self.root.procedures.procedures
        for procedure in procedures:
            procedure_commands_array = procedure.commands.commands
            self.list_of_procedure_commands.append(self.getListOfCommands(procedure_commands_array))
        return self.list_of_main_program_commands, self.list_of_procedure_commands


    def getVariableDeclarationsInMain(self):
        main = self.root.main
        if main.declarations != None:
            declarations_array = main.declarations.declarations
            for declaration in declarations_array:
                if declaration.node_type == "Identifier":
                    identifier = declaration.identifier
                    self.variable_declarations_in_main.append({"identifier" : identifier})
                elif declaration.node_type == "Array":
                    identifier = declaration.identifier.identifier
                    range = declaration.index.number
                    self.variable_declarations_in_main.append({"identifier" : {"identifier" : identifier, "range" :range}})
                else:
                    raise ValueError("Invalid variable declaration type!")
            
        return self.variable_declarations_in_main

    def getVariableDeclarationsInProcedures(self):
        procedures_array = self.root.procedures.procedures
        for procedure in procedures_array:
            if procedure.declarations != None:
                declarations_array = procedure.declarations.declarations
                variable_declarations_in_procedure = []
                for declaration in declarations_array:
                    if declaration.node_type == "Identifier":
                        identifier = declaration.identifier
                        variable_declarations_in_procedure.append({"identifier" : identifier})
                    elif declaration.node_type == "Array":
                        identifier = declaration.identifier.identifier
                        range = declaration.index.number
                        variable_declarations_in_procedure.append({"identifier" : {"identifier" : identifier, "range" :range}})
                    else:
                        raise ValueError("Invalid variable declaration type!")
                self.variable_declarations_in_procedures.append(variable_declarations_in_procedure)

        return self.variable_declarations_in_procedures
    
    def getArgumentsDeclarationsInProceduresHead(self):
        procedures_array = self.root.procedures.procedures
        for procedure in procedures_array:
            arguments = procedure.proc_head.declarations.argumentsDeclarations
            arg = []
            i = 1
            for argument in arguments:
                arg.append({"argument" : argument})
                i += 1
            procedure_identifier = procedure.proc_head.identifier.identifier
            procedure_head = {"procedure identifier": procedure_identifier, "arguments declarations": arg}
            self.arguments_declarations_in_procedures_head.append(procedure_head)
        
        return self.arguments_declarations_in_procedures_head
    
    def getListOfCommands(self, commands_array):
        list_of_commands = []
        for command in commands_array:

            if command.node_type == "Assign":
                identifier = command.identifier
                expression = command.expression

                expr, ident = self.createAssign(identifier, expression)

                list_of_commands.append({"command type": "Assign", "left side": ident, "right side": expr})

            elif command.node_type == "Read":
                identifier = command.identifier

                ident = self.createRead(identifier)

                list_of_commands.append({"command type": "Read", "right side": ident})

            elif command.node_type == "Write":
                value = command.value

                val = self.createWrite(value)
                
                list_of_commands.append({"command type": "Write", "right side": val})

            elif command.node_type == "ProcCall":
                identifier = command.identifier.identifier
                arguments = command.args.arguments

                args = self.createProcedureCall(arguments)

                list_of_commands.append({"command type" : "Procedure Call" ,"procedure identifier" : identifier, "arguments" : args})

            elif command.node_type == "WhileDo":
                condition = command.condition
                commands = command.commands.commands

                cond = self.createConditionOrBinaryOperator(condition)
                commands_in_while = self.getListOfCommands(commands)

                list_of_commands.append({"command type" : "While Do" ,"condition" : cond, "commands": commands_in_while})

            elif command.node_type == "RepeatUntil":
                pass

            elif command.node_type == "If":
                condition = command.condition
                commands1 = command.commands1.commands
                commands_in_if = self.getListOfCommands(commands1)
                cond = self.createConditionOrBinaryOperator(condition)
                if command.commands2 != None:
                    commands2 = command.commands2.commands
                    commands_in_else = self.getListOfCommands(commands2)
                    list_of_commands.append({"command type" : "If Else" ,"condition" : cond, "if commands" : commands_in_if, "else commands": commands_in_else})                    
                else: 
                    list_of_commands.append({"command type" : "If" ,"condition" : cond, "commands": commands_in_if})

        return list_of_commands


    def createAssign(self, identifier, expression):
        if expression.node_type == "Number":
            expr = expression.number

        elif expression.node_type == "Identifier":
            if isinstance(expression.identifier, str):
                expr = expression.identifier
            elif isinstance(expression.identifier, ArrayNode):
                if isinstance(expression.identifier.index, NumberNode):
                    expr = {"identifier": expression.identifier.identifier.identifier, "index": expression.identifier.index.number}
                elif isinstance(expression.identifier.index, IdentifierNode):
                    expr = {"identifier": expression.identifier.identifier.identifier, "index": expression.identifier.index.identifier}

        elif expression.node_type == "BinaryOperator":
            expr = self.createConditionOrBinaryOperator(expression)

        if identifier.node_type == "Identifier":
            if isinstance(identifier.identifier, str):
                ident = identifier.identifier
            elif isinstance(identifier.identifier, ArrayNode):
                if isinstance(identifier.identifier.index, NumberNode):
                    ident = {"identifier": identifier.identifier.identifier.identifier, "index": identifier.identifier.index.number}
                elif isinstance(identifier.identifier.index, IdentifierNode):
                    ident = {"identifier": identifier.identifier.identifier.identifier, "index": identifier.identifier.index.identifier}  
        return expr, ident
    
    def createRead(self, identifier):
        if identifier.node_type == "Identifier":
            if isinstance(identifier.identifier, str):
                ident = identifier.identifier
            elif isinstance(identifier.identifier, ArrayNode):
                if isinstance(identifier.identifier.index, NumberNode):
                    ident = {"identifier": identifier.identifier.identifier.identifier, "index": identifier.identifier.index.number}
                elif isinstance(identifier.identifier.index, IdentifierNode):
                    ident = {"identifier": identifier.identifier.identifier.identifier, "index": identifier.identifier.index.identifier} 
        return ident
    
    def createWrite(self, value):
        if value.node_type == "Number":
            val = value.number        
        if value.node_type == "Identifier":
            if isinstance(value.identifier, str):
                val = value.identifier
            elif isinstance(value.identifier, ArrayNode):
                if isinstance(value.identifier.index, NumberNode):
                    val = {"identifier": value.identifier.identifier.identifier, "index": value.identifier.index.number}
                elif isinstance(value.identifier.index, IdentifierNode):
                    val = {"identifier": value.identifier.identifier.identifier, "index": value.identifier.index.identifier} 
        return val
    
    def createProcedureCall(self, arguments):
        arguments_in_procedure_call = []
        i = 1
        for argument in arguments:
            arguments_in_procedure_call.append({"argument {}".format(i) : argument.identifier})
            i += 1
        return arguments_in_procedure_call
    
    def createConditionOrBinaryOperator(self, condition_or_expression):
        op = condition_or_expression.operator

        left = None
        right = None
        left_index = None
        right_index = None

        if condition_or_expression.left.node_type == "Number":
            left = condition_or_expression.left.number
        elif condition_or_expression.left.node_type == "Identifier" and isinstance(condition_or_expression.left.identifier, str):
            left = condition_or_expression.left.identifier
        else:   
            id_left = condition_or_expression.left.identifier.identifier.identifier
            if condition_or_expression.left.identifier.index.node_type == "Number":
                left_index = condition_or_expression.left.identifier.index.number
            elif condition_or_expression.left.identifier.index.node_type == "Identifier":
                left_index = condition_or_expression.left.identifier.index.identifier                            

        if condition_or_expression.right.node_type == "Number":
            right = condition_or_expression.right.number
        elif condition_or_expression.right.node_type == "Identifier" and isinstance(condition_or_expression.right.identifier, str):
            right = condition_or_expression.right.identifier
        else:   
            id_right = condition_or_expression.right.identifier.identifier.identifier
            if condition_or_expression.right.identifier.index.node_type == "Number":
                right_index = condition_or_expression.right.identifier.index.number
            elif condition_or_expression.right.identifier.index.node_type == "Identifier":
                right_index = condition_or_expression.right.identifier.index.identifier 

        if left is not None and right is not None:
            cond_or_expr = {"left": left, "operator": op, "right": right}
        elif left is not None and right is None:
            cond_or_expr = {"left": left, "operator": op, "right": {"identifier": id_right, "index": right_index}}
        elif left is None and right is not None:
            cond_or_expr = {"left": {"identifier": id_left, "index": left_index}, "operator": op, "right": right}
        else:
            cond_or_expr = {"left": {"identifier": id_left, "index": left_index}, "operator": op, "right": {"identifier": id_right, "index": right_index}}

        return cond_or_expr  

    def checkIfThereAreUndeclaredVariables(self, list_of_commands, declarations, proc_head):
        arguments_declarations = proc_head["arguments declarations"]
        for i in range(len(list_of_commands)):
            if list_of_commands[i]["command type"] == "Assign":
                left_side = list_of_commands[i]["left side"]
                right_side = list_of_commands[i]["right side"]
                if isinstance(left_side, str) and (isinstance(right_side, str) or isinstance(right_side, int)):
                    is_declared_identifier_left = False
                    is_declared_identifier_right = False
                    for j in range(len(declarations)):
                        if left_side == declarations[j]["identifier"]:
                            is_declared_identifier_left = True
                        if right_side == declarations[j]["identifier"]:
                            is_declared_identifier_right = True
                        else:
                            if isinstance(right_side, int):
                                is_declared_identifier_right = True

                    is_passed_identifier_left_in_proc_head = False
                    is_passed_identifier_right_in_proc_head = False 
                    for z in range(len(arguments_declarations)):
                        argument = arguments_declarations[z]["argument"]
                        ident = argument["identifier"]
                        is_array = argument["isArray"]
                        if left_side == ident:
                            if is_array == False and is_passed_identifier_left_in_proc_head == False:
                                is_passed_identifier_left_in_proc_head = True                      
                        if right_side == ident:
                            if is_array == False and is_passed_identifier_right_in_proc_head == False:
                                is_passed_identifier_right_in_proc_head = True
                        else:
                            if isinstance(right_side, int):
                                is_passed_identifier_right_in_proc_head = True

                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        self.errors.append("Undeclared variable" +  "\'" + str(left_side) + "\'")                                                      
                    if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                        self.errors.append("Undeclared variable " + "\'" + str(right_side) + "\'")
                      

                elif isinstance(left_side, dict) and (isinstance(right_side, str) or isinstance(right_side, int)):
                    identifier_left = left_side["identifier"]
                    index_left = left_side["index"]
                    is_declared_identifier_left = False
                    is_declared_index_left = False
                    is_declared_identifier_right = False
                    for j in range(len(declarations)):
                        if isinstance(declarations[j]["identifier"], dict):
                            if identifier_left == declarations[j]["identifier"]["identifier"]:
                                is_declared_identifier_left = True
                        elif isinstance(declarations[j]["identifier"], str):
                            if index_left == declarations[j]["identifier"]:
                                is_declared_index_left = True
                            elif isinstance(index_left, int):
                                is_declared_index_left = True
                        if right_side == declarations[j]["identifier"]:
                            is_declared_identifier_right = True
                        else:
                            if isinstance(right_side, int):
                                is_declared_identifier_right = True

                    is_passed_identifier_left_in_proc_head = False
                    is_passed_index_left_in_proc_head = False
                    is_passed_identifier_right_in_proc_head = False   
                    for z in range(len(arguments_declarations)):
                        argument = arguments_declarations[z]["argument"]
                        ident = argument["identifier"]
                        is_array = argument["isArray"]                    
                        if identifier_left == ident:
                            if is_array == True and is_passed_identifier_left_in_proc_head == False:
                                is_passed_identifier_left_in_proc_head = True
                        if index_left == ident:
                            if is_array == False and is_passed_index_left_in_proc_head == False:
                                is_passed_index_left_in_proc_head = True 
                        else:                              
                            if isinstance(index_left, int):
                                is_passed_index_left_in_proc_head = True
                        if right_side == ident:
                            if is_array == False and is_passed_identifier_right_in_proc_head == False:
                                is_passed_identifier_right_in_proc_head = True
                        else:
                            if isinstance(right_side, int):
                                is_passed_identifier_right_in_proc_head = True                                

                    if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                        self.errors.append("Undeclared identifier of an array " +  "\'" + str(identifier_left) + "\'")                  
                    if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                        self.errors.append("Undeclared index " +  "\'" + str(index_left) + "\'" + " " + "of an array" )                                      
                    if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                        self.errors.append("Undeclared variable " + "\'" + str(right_side) + "\'")
                elif isinstance(left_side, str) and isinstance(right_side, dict):
                    if len(right_side) == 2:
                        identifier_right = right_side["identifier"]
                        index_right = right_side["index"]
                        is_declared_identifier_right = False
                        is_declared_index_right = False
                        is_declared_identifier_left = False
                        for j in range(len(declarations)):
                            if isinstance(declarations[j]["identifier"], dict):
                                if identifier_right == declarations[j]["identifier"]["identifier"]:
                                    is_declared_identifier_right = True
                            elif isinstance(declarations[j]["identifier"], str):
                                if index_right == declarations[j]["identifier"]:
                                    is_declared_index_right = True
                                elif isinstance(index_right, int):
                                    is_declared_index_right = True
                            if left_side == declarations[j]["identifier"]:
                                is_declared_identifier_left = True

                        is_passed_identifier_right_in_proc_head = False
                        is_passed_index_right_in_proc_head = False
                        is_passed_identifier_left_in_proc_head = False   
                        for z in range(len(arguments_declarations)):
                            argument = arguments_declarations[z]["argument"]
                            ident = argument["identifier"]
                            is_array = argument["isArray"]                    
                            if identifier_right == ident:
                                if is_array == True and is_passed_identifier_right_in_proc_head == False:
                                    is_passed_identifier_right_in_proc_head = True
                            if index_right == ident:
                                if is_array == False and is_passed_index_right_in_proc_head == False:
                                    is_passed_index_right_in_proc_head = True 
                            else:                              
                                if isinstance(index_right, int):
                                    is_passed_index_right_in_proc_head = True
                            if left_side == ident:
                                if is_array == False and is_passed_identifier_left_in_proc_head == False:
                                    is_passed_identifier_left_in_proc_head = True                             

                        if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                            self.errors.append("Undeclared identifier of an array " +  "\'" + str(identifier_right) + "\'")                  
                        if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                            self.errors.append("Undeclared index " +  "\'" + str(index_right) + "\'" + " " + "of an array" )                                      
                        if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                            self.errors.append("Undeclared variable " + "\'" + str(left_side) + "\'")
                    elif len(right_side) == 3:
                        left_side_of_right_side = right_side["left"]
                        right_side_of_right_side = right_side["right"]
                        if (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)):
                            is_declared_identifier_left = False
                            is_declared_identifier_left_of_right_side = False
                            is_declared_identifier_right_of_right_side = False
                            for j in range(len(declarations)):
                                if left_side == declarations[j]["identifier"]:
                                    is_declared_identifier_left = True
                                if left_side_of_right_side == declarations[j]["identifier"]:
                                    is_declared_identifier_left_of_right_side = True
                                else:
                                    if isinstance(left_side_of_right_side, int):
                                        is_declared_identifier_left_of_right_side = True                                    
                                if right_side_of_right_side == declarations[j]["identifier"]:
                                    is_declared_identifier_right_of_right_side = True
                                else:
                                    if isinstance(right_side_of_right_side, int):
                                        is_declared_identifier_right_of_right_side = True
                            is_passed_identifier_left_in_proc_head = False
                            is_passed_identifier_left_of_right_side_in_proc_head = False 
                            is_passed_identifier_right_of_right_side_in_proc_head = False 
                            for z in range(len(arguments_declarations)):
                                argument = arguments_declarations[z]["argument"]
                                ident = argument["identifier"]
                                is_array = argument["isArray"]
                                if left_side == ident:
                                    if is_array == False and is_passed_identifier_left_in_proc_head == False:
                                        is_passed_identifier_left_in_proc_head = True                      
                                if left_side_of_right_side == ident:
                                    if is_array == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                        is_passed_identifier_left_of_right_side_in_proc_head = True
                                else:
                                    if isinstance(left_side_of_right_side, int):
                                        is_passed_identifier_left_of_right_side_in_proc_head = True
                                if right_side_of_right_side == ident:
                                    if is_array == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                                        is_passed_identifier_right_of_right_side_in_proc_head = True 
                                else:
                                    if isinstance(right_side_of_right_side, int):
                                        is_passed_identifier_right_of_right_side_in_proc_head = True  
                            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(left_side) + "\'")                                                      
                            if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " + "\'" + str(left_side_of_right_side) + "\'")                                     
                            if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " + "\'" + str(right_side_of_right_side) + "\'")

                        elif isinstance(left_side_of_right_side, dict) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)):
                            left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                            left_side_of_right_side_index = left_side_of_right_side["index"]
                            is_declared_identifier_left = False
                            is_declared_left_side_of_right_side_identifier = False
                            is_declared_left_side_of_right_side_index = False
                            is_declared_identifier_right_of_right_side = False
                            for j in range(len(declarations)):
                                if isinstance(declarations[j]["identifier"], dict):
                                    if left_side_of_right_side_identifier == declarations[j]["identifier"]["identifier"]:
                                        is_declared_left_side_of_right_side_identifier = True
                                elif isinstance(declarations[j]["identifier"], str):
                                    if left_side_of_right_side_index == declarations[j]["identifier"]:
                                        is_declared_left_side_of_right_side_index = True
                                    elif isinstance(left_side_of_right_side_index, int):
                                        is_declared_left_side_of_right_side_index = True
                                    if right_side_of_right_side == declarations[j]["identifier"]:
                                        is_declared_identifier_right_of_right_side = True
                                    elif isinstance(right_side_of_right_side, int):
                                        is_declared_identifier_right_of_right_side = True                                        
                                if left_side == declarations[j]["identifier"]:
                                    is_declared_identifier_left = True
                            is_passed_identifier_left_in_proc_head = False
                            is_passed_left_side_of_right_side_identifier_in_proc_head = False 
                            is_passed_left_side_of_right_side_index_in_proc_head = False 
                            is_passed_identifier_right_of_right_side_in_proc_head = False
                            for z in range(len(arguments_declarations)):
                                argument = arguments_declarations[z]["argument"]
                                ident = argument["identifier"]
                                is_array = argument["isArray"]
                                if left_side_of_right_side_identifier == ident:
                                    if is_array == True and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                                        is_passed_left_side_of_right_side_identifier_in_proc_head = True
                                if left_side_of_right_side_index == ident:
                                    if is_array == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                                        is_passed_left_side_of_right_side_index_in_proc_head = True 
                                else:                              
                                    if isinstance(left_side_of_right_side_index, int):
                                        is_passed_left_side_of_right_side_index_in_proc_head = True
                                if right_side_of_right_side == ident:
                                    if is_array == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                                        is_passed_identifier_right_of_right_side_in_proc_head = True
                                else:
                                    if isinstance(right_side_of_right_side, int):
                                        is_passed_identifier_right_of_right_side_in_proc_head = True 
                                if left_side == ident:
                                    if is_array == False and is_passed_identifier_left_in_proc_head == False:
                                        is_passed_identifier_left_in_proc_head = True
 
                            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(left_side) + "\'")                                                      
                            if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                     
                            if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(left_side_of_right_side_index) + "\'")                              
                            if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(right_side_of_right_side) + "\'") 

                        elif (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and isinstance(right_side_of_right_side, dict):  
                            right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                            right_side_of_right_side_index = right_side_of_right_side["index"]
                            is_declared_identifier_left = False
                            is_declared_right_side_of_right_side_identifier = False
                            is_declared_right_side_of_right_side_index = False
                            is_declared_identifier_left_of_right_side = False
                            for j in range(len(declarations)):
                                if isinstance(declarations[j]["identifier"], dict):
                                    if right_side_of_right_side_identifier == declarations[j]["identifier"]["identifier"]:
                                        is_declared_right_side_of_right_side_identifier = True
                                elif isinstance(declarations[j]["identifier"], str):
                                    if right_side_of_right_side_index == declarations[j]["identifier"]:
                                        is_declared_right_side_of_right_side_index = True
                                    elif isinstance(right_side_of_right_side_index, int):
                                        is_declared_right_side_of_right_side_index = True
                                    if left_side_of_right_side == declarations[j]["identifier"]:
                                        is_declared_identifier_left_of_right_side = True
                                    elif isinstance(left_side_of_right_side, int):
                                        is_declared_identifier_left_of_right_side = True                                        
                                if left_side == declarations[j]["identifier"]:
                                    is_declared_identifier_left = True
                            is_passed_identifier_left_in_proc_head = False
                            is_passed_right_side_of_right_side_identifier_in_proc_head = False 
                            is_passed_right_side_of_right_side_index_in_proc_head = False 
                            is_passed_identifier_left_of_right_side_in_proc_head = False
                            for z in range(len(arguments_declarations)):
                                argument = arguments_declarations[z]["argument"]
                                ident = argument["identifier"]
                                is_array = argument["isArray"]
                                if right_side_of_right_side_identifier == ident:
                                    if is_array == True and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                                        is_passed_right_side_of_right_side_identifier_in_proc_head = True
                                if right_side_of_right_side_index == ident:
                                    if is_array == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                                        is_passed_right_side_of_right_side_index_in_proc_head = True 
                                else:                              
                                    if isinstance(right_side_of_right_side_index, int):
                                        is_passed_right_side_of_right_side_index_in_proc_head = True
                                if left_side_of_right_side == ident:
                                    if is_array == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                        is_passed_identifier_left_of_right_side_in_proc_head = True
                                else:
                                    if isinstance(left_side_of_right_side, int):
                                        is_passed_identifier_left_of_right_side_in_proc_head = True 
                                if left_side == ident:
                                    if is_array == False and is_passed_identifier_left_in_proc_head == False:
                                        is_passed_identifier_left_in_proc_head = True
 
                            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(left_side) + "\'")                                                      
                            if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                     
                            if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(right_side_of_right_side_index) + "\'")                              
                            if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'")
                        elif isinstance(left_side_of_right_side, dict) and isinstance(right_side_of_right_side, dict):
                            is_declared_identifier_left = False
                            right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                            right_side_of_right_side_index = right_side_of_right_side["index"]
                            is_declared_right_side_of_right_side_identifier = False
                            is_declared_right_side_of_right_side_index = False 
                            left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                            left_side_of_right_side_index = left_side_of_right_side["index"]
                            is_declared_left_side_of_right_side_identifier = False
                            is_declared_left_side_of_right_side_index = False   
                            for j in range(len(declarations)):
                                if isinstance(declarations[j]["identifier"], dict):
                                    if right_side_of_right_side_identifier == declarations[j]["identifier"]["identifier"]:
                                        is_declared_right_side_of_right_side_identifier = True
                                    if left_side_of_right_side_identifier == declarations[j]["identifier"]["identifier"]:
                                        is_declared_left_side_of_right_side_identifier = True
                                elif isinstance(declarations[j]["identifier"], str):
                                    if right_side_of_right_side_index == declarations[j]["identifier"]:
                                        is_declared_right_side_of_right_side_index = True
                                    elif isinstance(right_side_of_right_side_index, int):
                                        is_declared_right_side_of_right_side_index = True
                                    if left_side_of_right_side_index == declarations[j]["identifier"]:
                                        is_declared_left_side_of_right_side_index = True
                                    elif isinstance(left_side_of_right_side_index, int):
                                        is_declared_left_side_of_right_side_index = True                                         
                                if left_side == declarations[j]["identifier"]:
                                    is_declared_identifier_left = True  
                            is_passed_identifier_left_in_proc_head = False
                            is_passed_left_side_of_right_side_identifier_in_proc_head = False 
                            is_passed_left_side_of_right_side_index_in_proc_head = False  
                            is_passed_right_side_of_right_side_identifier_in_proc_head = False 
                            is_passed_right_side_of_right_side_index_in_proc_head = False  
                            for z in range(len(arguments_declarations)):
                                argument = arguments_declarations[z]["argument"]
                                ident = argument["identifier"]
                                is_array = argument["isArray"]
                                if right_side_of_right_side_identifier == ident:
                                    if is_array == True and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                                        is_passed_right_side_of_right_side_identifier_in_proc_head = True

                                if right_side_of_right_side_index == ident:
                                    if is_array == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                                        is_passed_right_side_of_right_side_index_in_proc_head = True 
                                else:                              
                                    if isinstance(right_side_of_right_side_index, int):
                                        is_passed_right_side_of_right_side_index_in_proc_head = True

                                if left_side_of_right_side_identifier == ident:
                                    if is_array == True and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                                        is_passed_left_side_of_right_side_identifier_in_proc_head = True

                                if left_side_of_right_side_index == ident:
                                    if is_array == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                                        is_passed_left_side_of_right_side_index_in_proc_head = True 
                                else:                              
                                    if isinstance(left_side_of_right_side_index, int):
                                        is_passed_left_side_of_right_side_index_in_proc_head = True    

                                if left_side == ident:
                                    if is_array == False and is_passed_identifier_left_in_proc_head == False:
                                        is_passed_identifier_left_in_proc_head = True    
                            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(left_side) + "\'")                                                      
                            if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                     
                            if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(right_side_of_right_side_index) + "\'")                                                                                   
                            if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                     
                            if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(left_side_of_right_side_index) + "\'")                                                                                                                                                                                                                                     
                elif isinstance(left_side, dict) and isinstance(right_side, dict):
                    if len(right_side) == 2:
                        identifier_left = left_side["identifier"]
                        index_left = left_side["index"]
                        identifier_right = right_side["identifier"]
                        index_right = right_side["index"]
                        is_declared_identifier_right = False
                        is_declared_index_right = False
                        is_declared_identifier_left = False
                        is_declared_index_left = False        
                        for j in range(len(declarations)):
                            if isinstance(declarations[j]["identifier"], dict):
                                if identifier_right == declarations[j]["identifier"]["identifier"]:
                                    is_declared_identifier_right = True
                                elif identifier_left == declarations[j]["identifier"]["identifier"]:
                                    is_declared_identifier_left = True                                    
                            elif isinstance(declarations[j]["identifier"], str):
                                if index_right == declarations[j]["identifier"]:
                                    is_declared_index_right = True
                                elif index_left == declarations[j]["identifier"]:
                                    is_declared_index_left = True
                                elif isinstance(index_right, int):
                                    is_declared_index_right = True
                                elif isinstance(index_left, int):
                                    is_declared_index_left = True
                        is_passed_identifier_right_in_proc_head = False
                        is_passed_index_right_in_proc_head = False
                        is_passed_identifier_left_in_proc_head = False  
                        is_passed_index_left_in_proc_head = False    
                        for z in range(len(arguments_declarations)):
                            argument = arguments_declarations[z]["argument"]
                            ident = argument["identifier"]
                            is_array = argument["isArray"]                    
                            if identifier_right == ident:
                                if is_array == True and is_passed_identifier_right_in_proc_head == False:
                                    is_passed_identifier_right_in_proc_head = True
                            if index_right == ident:
                                if is_array == False and is_passed_index_right_in_proc_head == False:
                                    is_passed_index_right_in_proc_head = True 
                            else:                              
                                if isinstance(index_right, int):
                                    is_passed_index_right_in_proc_head = True

                            if identifier_left == ident:
                                if is_array == True and is_passed_identifier_left_in_proc_head == False:
                                    is_passed_identifier_left_in_proc_head = True
                            if index_left == ident:
                                if is_array == False and is_passed_index_left_in_proc_head == False:
                                    is_passed_index_left_in_proc_head = True 
                            else:                              
                                if isinstance(index_left, int):
                                    is_passed_index_left_in_proc_head = True    
                        if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                            self.errors.append("Undeclared variable " + "\'" + str(identifier_left) + "\'")
                        if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                            self.errors.append("Undeclared index " +  "\'" + str(index_left) + "\'" + " " + "of an array" ) 
                        if is_declared_identifier_right == False and is_passed_identifier_right_in_proc_head == False:
                            self.errors.append("Undeclared identifier of an array " +  "\'" + str(identifier_right) + "\'")                  
                        if is_declared_index_right == False and is_passed_index_right_in_proc_head == False:
                            self.errors.append("Undeclared index " +  "\'" + str(index_right) + "\'" + " " + "of an array" )
                    elif len(right_side) == 3:
                        left_side_of_right_side = right_side["left"]
                        right_side_of_right_side = right_side["right"]
                        if (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)):
                            is_declared_identifier_left = False
                            is_declared_index_left = False
                            is_declared_identifier_left_of_right_side = False
                            is_declared_identifier_right_of_right_side = False
                            identifier_left = left_side["identifier"]
                            index_left = left_side["index"]
                            for j in range(len(declarations)):
                                if isinstance(declarations[j]["identifier"], dict):
                                    if identifier_left == declarations[j]["identifier"]["identifier"]:
                                        is_declared_identifier_left = True                                  
                                elif isinstance(declarations[j]["identifier"], str):
                                    if index_left == declarations[j]["identifier"]:
                                        is_declared_index_left = True
                                    elif isinstance(index_left, int):
                                        is_declared_index_left = True
                                if left_side_of_right_side == declarations[j]["identifier"]:
                                    is_declared_identifier_left_of_right_side = True
                                else:
                                    if isinstance(left_side_of_right_side, int):
                                        is_declared_identifier_left_of_right_side = True                                    
                                if right_side_of_right_side == declarations[j]["identifier"]:
                                    is_declared_identifier_right_of_right_side = True
                                else:
                                    if isinstance(right_side_of_right_side, int):
                                        is_declared_identifier_right_of_right_side = True
                            is_passed_identifier_left_in_proc_head = False
                            is_passed_index_left_in_proc_head = False                            
                            is_passed_identifier_left_of_right_side_in_proc_head = False 
                            is_passed_identifier_right_of_right_side_in_proc_head = False 
                            for z in range(len(arguments_declarations)):
                                argument = arguments_declarations[z]["argument"]
                                ident = argument["identifier"]
                                is_array = argument["isArray"]
                                if identifier_left == ident:
                                    if is_array == True and is_passed_identifier_left_in_proc_head == False:
                                        is_passed_identifier_left_in_proc_head = True   
                                if index_left == ident:
                                    if is_array == False and is_passed_index_left_in_proc_head == False:
                                            is_passed_index_left_in_proc_head = True 
                                else: 
                                    if isinstance(index_left, int):
                                            is_passed_index_left_in_proc_head = True                                                          
                                if left_side_of_right_side == ident:
                                    if is_array == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                        is_passed_identifier_left_of_right_side_in_proc_head = True
                                else:
                                    if isinstance(left_side_of_right_side, int):
                                        is_passed_identifier_left_of_right_side_in_proc_head = True
                                if right_side_of_right_side == ident:
                                    if is_array == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                                        is_passed_identifier_right_of_right_side_in_proc_head = True 
                                else:
                                    if isinstance(right_side_of_right_side, int):
                                        is_passed_identifier_right_of_right_side_in_proc_head = True  
                            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " +  "\'" + str(identifier_left) + "\'")   
                            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " +  "\'" + str(index_left) + "\'")                                                                                     
                            if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " + "\'" + str(left_side_of_right_side) + "\'")                                     
                            if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " + "\'" + str(right_side_of_right_side) + "\'")

                        elif isinstance(left_side_of_right_side, dict) and (isinstance(right_side_of_right_side, str) or isinstance(right_side_of_right_side, int)):
                            left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                            left_side_of_right_side_index = left_side_of_right_side["index"]
                            is_declared_identifier_left = False
                            is_declared_index_left = False
                            is_declared_left_side_of_right_side_identifier = False
                            is_declared_left_side_of_right_side_index = False
                            is_declared_identifier_right_of_right_side = False
                            identifier_left = left_side["identifier"]
                            index_left = left_side["index"]                            
                            for j in range(len(declarations)):
                                if isinstance(declarations[j]["identifier"], dict):
                                    if left_side_of_right_side_identifier == declarations[j]["identifier"]["identifier"]:
                                        is_declared_left_side_of_right_side_identifier = True
                                    if identifier_left == declarations[j]["identifier"]["identifier"]:
                                        is_declared_identifier_left = True                                          
                                elif isinstance(declarations[j]["identifier"], str):
                                    if left_side_of_right_side_index == declarations[j]["identifier"]:
                                        is_declared_left_side_of_right_side_index = True
                                    elif isinstance(left_side_of_right_side_index, int):
                                        is_declared_left_side_of_right_side_index = True
                                    if right_side_of_right_side == declarations[j]["identifier"]:
                                        is_declared_identifier_right_of_right_side = True
                                    elif isinstance(right_side_of_right_side, int):
                                        is_declared_identifier_right_of_right_side = True  
                                    if index_left == declarations[j]["identifier"]:
                                        is_declared_index_left = True
                                    elif isinstance(index_left, int):
                                        is_declared_index_left = True                                                                              
                            is_passed_identifier_left_in_proc_head = False
                            is_passed_index_left_in_proc_head = False
                            is_passed_left_side_of_right_side_identifier_in_proc_head = False 
                            is_passed_left_side_of_right_side_index_in_proc_head = False 
                            is_passed_identifier_right_of_right_side_in_proc_head = False
                            for z in range(len(arguments_declarations)):
                                argument = arguments_declarations[z]["argument"]
                                ident = argument["identifier"]
                                is_array = argument["isArray"]
                                if identifier_left == ident:
                                    if is_array == True and is_passed_identifier_left_in_proc_head == False:
                                        is_passed_identifier_left_in_proc_head = True   
                                if index_left == ident:
                                    if is_array == False and is_passed_index_left_in_proc_head == False:
                                            is_passed_index_left_in_proc_head = True  
                                else: 
                                    if isinstance(index_left, int):
                                        is_passed_index_left_in_proc_head = True    

                                if left_side_of_right_side_identifier == ident:
                                    if is_array == True and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                                        is_passed_left_side_of_right_side_identifier_in_proc_head = True
                                if left_side_of_right_side_index == ident:
                                    if is_array == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                                        is_passed_left_side_of_right_side_index_in_proc_head = True 
                                else:                              
                                    if isinstance(left_side_of_right_side_index, int):
                                        is_passed_left_side_of_right_side_index_in_proc_head = True
                                if right_side_of_right_side == ident:
                                    if is_array == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                                        is_passed_identifier_right_of_right_side_in_proc_head = True
                                else:
                                    if isinstance(right_side_of_right_side, int):
                                        is_passed_identifier_right_of_right_side_in_proc_head = True 
 
                            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " +  "\'" + str(identifier_left) + "\'") 
                            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " +  "\'" + str(index_left) + "\'")                                                                                      
                            if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                     
                            if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(left_side_of_right_side_index) + "\'")                              
                            if is_declared_identifier_right_of_right_side == False and is_passed_identifier_right_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(right_side_of_right_side) + "\'") 

                        elif (isinstance(left_side_of_right_side, str) or isinstance(left_side_of_right_side, int)) and isinstance(right_side_of_right_side, dict):  
                            right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                            right_side_of_right_side_index = right_side_of_right_side["index"]
                            is_declared_identifier_left = False
                            is_declared_index_left = False
                            is_declared_right_side_of_right_side_identifier = False
                            is_declared_right_side_of_right_side_index = False
                            is_declared_identifier_left_of_right_side = False
                            identifier_left = left_side["identifier"]
                            index_left = left_side["index"]                            
                            for j in range(len(declarations)):
                                if isinstance(declarations[j]["identifier"], dict):
                                    if right_side_of_right_side_identifier == declarations[j]["identifier"]["identifier"]:
                                        is_declared_right_side_of_right_side_identifier = True
                                    if identifier_left == declarations[j]["identifier"]["identifier"]:
                                        is_declared_identifier_left = True                                          
                                elif isinstance(declarations[j]["identifier"], str):
                                    if right_side_of_right_side_index == declarations[j]["identifier"]:
                                        is_declared_right_side_of_right_side_index = True
                                    elif isinstance(right_side_of_right_side_index, int):
                                        is_declared_right_side_of_right_side_index = True
                                    if left_side_of_right_side == declarations[j]["identifier"]:
                                        is_declared_identifier_left_of_right_side = True
                                    elif isinstance(left_side_of_right_side, int):
                                        is_declared_identifier_left_of_right_side = True  
                                    if index_left == declarations[j]["identifier"]:
                                        is_declared_index_left = True
                                    elif isinstance(index_left, int):
                                        is_declared_index_left = True                                                                              
                            is_passed_identifier_left_in_proc_head = False
                            is_passed_index_left_in_proc_head = False
                            is_passed_right_side_of_right_side_identifier_in_proc_head = False 
                            is_passed_right_side_of_right_side_index_in_proc_head = False 
                            is_passed_identifier_left_of_right_side_in_proc_head = False
                            for z in range(len(arguments_declarations)):
                                argument = arguments_declarations[z]["argument"]
                                ident = argument["identifier"]
                                is_array = argument["isArray"]
                                if identifier_left == ident:
                                    if is_array == True and is_passed_identifier_left_in_proc_head == False:
                                        is_passed_identifier_left_in_proc_head = True   
                                if index_left == ident:
                                    if is_array == False and is_passed_index_left_in_proc_head == False:
                                            is_passed_index_left_in_proc_head = True  
                                else: 
                                    if isinstance(index_left, int):
                                        is_passed_index_left_in_proc_head = True    

                                if right_side_of_right_side_identifier == ident:
                                    if is_array == True and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                                        is_passed_right_side_of_right_side_identifier_in_proc_head = True
                                if right_side_of_right_side_index == ident:
                                    if is_array == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                                        is_passed_right_side_of_right_side_index_in_proc_head = True 
                                else:                              
                                    if isinstance(right_side_of_right_side_index, int):
                                        is_passed_right_side_of_right_side_index_in_proc_head = True
                                if left_side_of_right_side == ident:
                                    if is_array == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                        is_passed_identifier_left_of_right_side_in_proc_head = True
                                else:
                                    if isinstance(left_side_of_right_side, int):
                                        is_passed_identifier_left_of_right_side_in_proc_head = True 
 
                            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " +  "\'" + str(identifier_left) + "\'") 
                            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " +  "\'" + str(index_left) + "\'")    
                            if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'")                                                                                                                   
                            if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                     
                            if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(right_side_of_right_side_index) + "\'")                              
                            if is_declared_identifier_left_of_right_side == False and is_passed_identifier_left_of_right_side_in_proc_head == False:
                                self.errors.append("Undeclared variable " +  "\'" + str(left_side_of_right_side) + "\'") 
                        elif isinstance(left_side_of_right_side, dict) and isinstance(right_side_of_right_side, dict):
                            is_declared_identifier_left = False
                            is_declared_index_left = False
                            right_side_of_right_side_identifier = right_side_of_right_side["identifier"]
                            right_side_of_right_side_index = right_side_of_right_side["index"]
                            is_declared_right_side_of_right_side_identifier = False
                            is_declared_right_side_of_right_side_index = False 
                            left_side_of_right_side_identifier = left_side_of_right_side["identifier"]
                            left_side_of_right_side_index = left_side_of_right_side["index"]
                            is_declared_left_side_of_right_side_identifier = False
                            is_declared_left_side_of_right_side_index = False   
                            identifier_left = left_side["identifier"]
                            index_left = left_side["index"]                             
                            for j in range(len(declarations)):
                                if isinstance(declarations[j]["identifier"], dict):
                                    if right_side_of_right_side_identifier == declarations[j]["identifier"]["identifier"]:
                                        is_declared_right_side_of_right_side_identifier = True
                                    if left_side_of_right_side_identifier == declarations[j]["identifier"]["identifier"]:
                                        is_declared_left_side_of_right_side_identifier = True
                                    if identifier_left == declarations[j]["identifier"]["identifier"]:
                                        is_declared_identifier_left = True  
                                elif isinstance(declarations[j]["identifier"], str):
                                    if right_side_of_right_side_index == declarations[j]["identifier"]:
                                        is_declared_right_side_of_right_side_index = True
                                    elif isinstance(right_side_of_right_side_index, int):
                                        is_declared_right_side_of_right_side_index = True
                                    if left_side_of_right_side_index == declarations[j]["identifier"]:
                                        is_declared_left_side_of_right_side_index = True
                                    elif isinstance(left_side_of_right_side_index, int):
                                        is_declared_left_side_of_right_side_index = True  
                                    if index_left == declarations[j]["identifier"]:
                                        is_declared_index_left = True
                                    elif isinstance(index_left, int):
                                        is_declared_index_left = True  

                            is_passed_identifier_left_in_proc_head = False
                            is_passed_index_left_in_proc_head = False                            
                            is_passed_left_side_of_right_side_identifier_in_proc_head = False 
                            is_passed_left_side_of_right_side_index_in_proc_head = False  
                            is_passed_right_side_of_right_side_identifier_in_proc_head = False 
                            is_passed_right_side_of_right_side_index_in_proc_head = False  
                            for z in range(len(arguments_declarations)):
                                argument = arguments_declarations[z]["argument"]
                                ident = argument["identifier"]
                                is_array = argument["isArray"]
                                if right_side_of_right_side_identifier == ident:
                                    if is_array == True and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                                        is_passed_right_side_of_right_side_identifier_in_proc_head = True

                                if right_side_of_right_side_index == ident:
                                    if is_array == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                                        is_passed_right_side_of_right_side_index_in_proc_head = True 
                                else:                              
                                    if isinstance(right_side_of_right_side_index, int):
                                        is_passed_right_side_of_right_side_index_in_proc_head = True

                                if left_side_of_right_side_identifier == ident:
                                    if is_array == True and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                                        is_passed_left_side_of_right_side_identifier_in_proc_head = True

                                if left_side_of_right_side_index == ident:
                                    if is_array == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                                        is_passed_left_side_of_right_side_index_in_proc_head = True 
                                else:                              
                                    if isinstance(left_side_of_right_side_index, int):
                                        is_passed_left_side_of_right_side_index_in_proc_head = True     

                                if identifier_left == ident:
                                    if is_array == True and is_passed_identifier_left_in_proc_head == False:
                                        is_passed_identifier_left_in_proc_head = True   
                                if index_left == ident:
                                    if is_array == False and is_passed_index_left_in_proc_head == False:
                                            is_passed_index_left_in_proc_head = True  
                                else: 
                                    if isinstance(index_left, int):
                                        is_passed_index_left_in_proc_head = True   
                            if is_declared_identifier_left == False and is_passed_identifier_left_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " +  "\'" + str(identifier_left) + "\'")  
                            if is_declared_index_left == False and is_passed_index_left_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(index_left) + "\'")                                                                                        
                            if is_declared_right_side_of_right_side_identifier == False and is_passed_right_side_of_right_side_identifier_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " + "\'" + str(right_side_of_right_side_identifier) + "\'")                                     
                            if is_declared_right_side_of_right_side_index == False and is_passed_right_side_of_right_side_index_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(right_side_of_right_side_index) + "\'")                                                                                   
                            if is_declared_left_side_of_right_side_identifier == False and is_passed_left_side_of_right_side_identifier_in_proc_head == False:
                                self.errors.append("Undeclared identifier of an array " + "\'" + str(left_side_of_right_side_identifier) + "\'")                                     
                            if is_declared_left_side_of_right_side_index == False and is_passed_left_side_of_right_side_index_in_proc_head == False:
                                self.errors.append("Undeclared index of an array " + "\'" + str(left_side_of_right_side_index) + "\'")        
                                                 
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

        for k in range(len(self.errors)):
            print(self.errors[k])