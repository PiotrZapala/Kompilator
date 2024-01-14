class Node:
    def __init__(self, node_type):
        self.node_type = node_type

class MainNode(Node):
    def __init__(self, declarations, commands):
        super().__init__("Main")
        self.declarations = declarations
        self.commands = commands

class ProgramNode(Node):
    def __init__(self, procedures, main):
        super().__init__("Program")
        self.procedures = procedures
        self.main = main

class ProceduresNode(Node):
    def __init__(self):
        super().__init__("Procedures")
        self.procedures = []

    def addProcedure(self, procedure):
        self.procedures.append(procedure)

class ProcedureNode(Node):
    def __init__(self, proc_head, declarations, commands):
        super().__init__("Procedure")
        self.proc_head = proc_head
        self.declarations = declarations
        self.commands = commands

class ProcHeadNode(Node):
    def __init__(self, identifier, declarations):
        super().__init__("ProcHead")
        self.identifier = identifier
        self.declarations = declarations

class ProcCallNode(Node):
    def __init__(self, identifier, args, line_number):
        super().__init__("ProcCall")
        self.identifier = identifier
        self.args = args
        self.line_number = line_number        

class IfNode(Node):
    def __init__(self, condition, commands1, commands2, line_number):
        super().__init__("If")
        self.condition = condition
        self.commands1 = commands1
        self.commands2 = commands2
        self.line_number = line_number

class WhileDoNode(Node):
    def __init__(self, condition, commands, line_number):
        super().__init__("WhileDo")
        self.condition = condition
        self.commands = commands
        self.line_number = line_number         

class RepeatUntilNode(Node):
    def __init__(self, commands, condition, line_number):
        super().__init__("RepeatUntil")
        self.commands = commands        
        self.condition = condition
        self.line_number = line_number       

class AssignNode(Node):
    def __init__(self, identifier, expression, line_number):
        super().__init__("Assign")
        self.identifier = identifier       
        self.expression = expression
        self.line_number = line_number        

class WriteNode(Node):
    def __init__(self, value, line_number):
        super().__init__("Write")
        self.value = value  
        self.line_number = line_number         

class ReadNode(Node):
    def __init__(self, identifier, line_number):
        super().__init__("Read")
        self.identifier = identifier     
        self.line_number = line_number

class BinaryOperatorNode(Node):
    def __init__(self, operator, left, right):
        super().__init__("BinaryOperator")
        self.operator = operator
        self.left = left        
        self.right = right

class ConditionOperatorNode(Node):
    def __init__(self, operator, left, right, line_number):
        super().__init__("ConditionOperator")
        self.operator = operator
        self.left = left        
        self.right = right
        self.line_number = line_number

class ArrayNode(Node):
    def __init__(self, identifier, index):
        super().__init__("Array")
        self.identifier = identifier
        self.index = index

class NumberNode(Node):
    def __init__(self, number):
        super().__init__("Number")
        self.number = number

class IdentifierNode(Node):
    def __init__(self, identifier):
        super().__init__("Identifier")
        self.identifier = identifier

class ArgsNode(Node):
    def __init__(self):
        super().__init__("Args")
        self.arguments = []

    def addArgument(self, identifier):
        self.arguments.append(identifier)

class ArgsDeclNode(Node):
    def __init__(self):
        super().__init__("ArgsDecl")
        self.argumentsDeclarations = []

    def addArgumentDeclaration(self, identifier, isArray):
        argument = {"identifier": identifier, "isArray": isArray}
        self.argumentsDeclarations.append(argument)
    
class CommandsNode(Node):
    def __init__(self):
        super().__init__("Commands")
        self.commands = []

    def addCommand(self, command):
        self.commands.append(command)
    
class DeclarationsNode(Node):
    def __init__(self):
        super().__init__("Declarations")
        self.declarations = []

    def addDeclaration(self, declaration):
        self.declarations.append(declaration)