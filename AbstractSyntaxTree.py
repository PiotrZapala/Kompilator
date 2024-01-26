from Node import *

class AbstractSyntaxTree:

    def __init__(self, root):
        self.root = root 
        self.variable_declarations_in_main = []
        self.variable_declarations_in_procedures = []
        self.arguments_declarations_in_procedures_head = []
        self.list_of_main_program_commands = []
        self.list_of_procedure_commands = []

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
                line_number = procedure.declarations.line_number
                variable_declarations_in_procedure = []
                for declaration in declarations_array:
                    if declaration.node_type == "Identifier":
                        identifier = declaration.identifier
                        variable_declarations_in_procedure.append({"identifier" : identifier, "line number": line_number})
                    elif declaration.node_type == "Array":
                        identifier = declaration.identifier.identifier
                        range = declaration.index.number
                        variable_declarations_in_procedure.append({"identifier" : {"identifier" : identifier, "range" :range}, "line number": line_number})
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
                line_number = command.line_number

                expr, ident = self.createAssign(identifier, expression)

                list_of_commands.append({"command type": "Assign", "left side": ident, "right side": expr, "line number": line_number})

            elif command.node_type == "Read":
                identifier = command.identifier
                line_number = command.line_number                

                ident = self.createRead(identifier)

                list_of_commands.append({"command type": "Read", "right side": ident, "line number": line_number})

            elif command.node_type == "Write":
                value = command.value
                line_number = command.line_number                

                val = self.createWrite(value)
                
                list_of_commands.append({"command type": "Write", "right side": val, "line number": line_number})

            elif command.node_type == "ProcCall":
                identifier = command.identifier.identifier
                arguments = command.args.arguments
                line_number = command.line_number                

                args = self.createProcedureCall(arguments)

                list_of_commands.append({"command type" : "Procedure Call" ,"procedure identifier" : identifier, "arguments" : args, "line number": line_number})

            elif command.node_type == "WhileDo":
                condition = command.condition
                commands = command.commands.commands
                line_number = command.condition.line_number

                cond = self.createConditionOrBinaryOperator(condition)
                commands_in_while = self.getListOfCommands(commands)

                list_of_commands.append({"command type" : "While Do" ,"condition" : cond, "commands": commands_in_while, "line number": line_number})

            elif command.node_type == "RepeatUntil":
                commands = command.commands.commands                
                condition = command.condition
                line_number = command.condition.line_number

                commands_in_repeat = self.getListOfCommands(commands)
                cond = self.createConditionOrBinaryOperator(condition)

                list_of_commands.append({"command type" : "Repeat Until" ,"commands": commands_in_repeat, "condition" : cond, "line number": line_number})

            elif command.node_type == "If":
                condition = command.condition
                commands1 = command.commands1.commands
                line_number = command.condition.line_number
                commands_in_if = self.getListOfCommands(commands1)
                cond = self.createConditionOrBinaryOperator(condition)
                if command.commands2 != None:
                    commands2 = command.commands2.commands
                    commands_in_else = self.getListOfCommands(commands2)
                    list_of_commands.append({"command type" : "If" ,"condition" : cond, "if commands" : commands_in_if, "else commands": commands_in_else, "line number": line_number})                    
                else: 
                    list_of_commands.append({"command type" : "If" ,"condition" : cond, "if commands": commands_in_if, "line number": line_number})

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

    def printNestedDict(self, d, indent=0):
        for key, value in d.items():
            if isinstance(value, dict):
                print(" " * indent + f"{key}:")
                self.printNestedDict(value, indent + 4)
            elif isinstance(value, list):
                print(" " * indent + f"{key}:")
                for item in value:
                    self.printNestedDict(item, indent + 4)
            else:
                print(" " * indent + f"{key}: {value}")

    def printMainProgram(self, decl_in_main, main_commands_array):
        print()
        print("Main Program Declarations")
        for z in range(len(decl_in_main)):
            self.printNestedDict(decl_in_main[z])
        print()
        print("Main Program Commands")
        for i in range(len(main_commands_array)):
            self.printNestedDict(main_commands_array[i])

    def printProcedures(self, procedures_head, decl_in_procedures, procedure_commands_array):
        for k in range(len(procedures_head)):
            print()
            print("Procedure Identifier")
            print(procedures_head[k]["procedure identifier"])
            print()
            print("Procedure Head")
            for j in range(len(procedures_head[k]["arguments declarations"])):
                self.printNestedDict(procedures_head[k]["arguments declarations"][j])
            print()
            print("Procedure Declarations")
            if len(decl_in_procedures) != 0:
                for z in range(len(decl_in_procedures[k])):
                    self.printNestedDict(decl_in_procedures[k][z])
            print()
            print("Procedure Commands")
            for i in range(len(procedure_commands_array[k])):
                self.printNestedDict(procedure_commands_array[k][i])