import ply.yacc as yacc
from Lexer import Lexer
from Node import *

class Parser:
    tokens = Lexer.tokens

    def p_program_all(self, p):
        """program_all : procedures main"""
        p[0] = ProgramNode(p[1], p[2])

    def p_procedures(self, p):
        """procedures : procedures PROCEDURE proc_head IS declarations IN commands END
                      | procedures PROCEDURE proc_head IS IN commands END
                      | """
        if len(p) == 9:
            p[0] = p[1]
            procedure_node = ProcedureNode(p[3], p[5], p[7])
            p[0].addProcedure(procedure_node)
        elif len(p) == 8:
            p[0] = p[1]
            procedure_node = ProcedureNode(p[3], None, p[6])
            p[0].addProcedure(procedure_node)
        else:
            p[0] = ProceduresNode()
        
    def p_main(self, p):
        """main : PROGRAM IS declarations IN commands END
                | PROGRAM IS IN commands END"""
        if len(p) == 7:
            p[0] = MainNode(p[3], p[5])
        else:
            p[0] = MainNode(None, p[4])

    def p_commands(self, p):
        """commands : commands command
                    | command"""
        if len(p) == 3:
            p[0] = p[1]
            p[0].addCommand(p[2])
        else:
            p[0] = CommandsNode()
            p[0].addCommand(p[1])

    def p_command(self, p):
        """command : identifier ASSIGN expression SEMICOLON
                   | IF condition THEN commands ELSE commands ENDIF
                   | IF condition THEN commands ENDIF
                   | WHILE condition DO commands ENDWHILE
                   | REPEAT commands UNTIL condition SEMICOLON
                   | proc_call SEMICOLON
                   | READ identifier SEMICOLON
                   | WRITE value SEMICOLON"""
        line_number = p.lexer.lineno
        if p[2] == ':=':
            p[0] = AssignNode(p[1], p[3], line_number-1)
        elif p[1] == 'IF':
            if len(p) == 8:
                p[0] = IfNode(p[2], p[4], p[6])
            else:
                p[0] = IfNode(p[2], p[4], None)
        elif p[1] == 'WHILE':
            p[0] = WhileDoNode(p[2], p[4])
        elif p[1] == 'REPEAT':
            p[0] = RepeatUntilNode(p[2], p[4])
        elif p[1] == 'READ':
            p[0] = ReadNode(p[2], line_number-1)
        elif p[1] == 'WRITE':
            p[0] = WriteNode(p[2], line_number-1)
        else:
            p[0] = p[1]

    def p_proc_head(self, p):
        """proc_head : IDENTIFIER LEFT_BRACKET args_decl RIGHT_BRACKET"""
        p[0] = ProcHeadNode(IdentifierNode(p[1]), p[3])

    def p_proc_call(self, p):
        """proc_call : IDENTIFIER LEFT_BRACKET args RIGHT_BRACKET"""
        p[0] = ProcCallNode(IdentifierNode(p[1]), p[3], p.lineno)

    def p_declarations(self, p):
        """declarations : declarations COMMA IDENTIFIER
                        | declarations COMMA IDENTIFIER LEFT_SQUARE_BRACKET NUMBER RIGHT_SQUARE_BRACKET
                        | IDENTIFIER
                        | IDENTIFIER LEFT_SQUARE_BRACKET NUMBER RIGHT_SQUARE_BRACKET"""
        if len(p) == 2:
            p[0] = DeclarationsNode()
            p[0].addDeclaration(IdentifierNode(p[1]))
        elif len(p) == 4:
            p[0] = p[1]
            p[0].addDeclaration(IdentifierNode(p[3]))
        elif len(p) == 7:
            p[0] = p[1]
            p[0].addDeclaration(ArrayNode(IdentifierNode(p[3]), NumberNode(p[5])))
        elif len(p) == 5:
            p[0] = DeclarationsNode()
            p[0].addDeclaration(ArrayNode(IdentifierNode(p[1]), NumberNode(p[3])))

    def p_args_decl(self, p):
        """args_decl : args_decl COMMA IDENTIFIER
                     | args_decl COMMA T IDENTIFIER
                     | IDENTIFIER
                     | T IDENTIFIER"""
        if len(p) == 2:
            p[0] = ArgsDeclNode()
            p[0].addArgumentDeclaration(p[1], False)
        elif len(p) == 3:
            p[0] = ArgsDeclNode()
            p[0].addArgumentDeclaration(p[2], True)
        elif len(p) == 4:
            p[0] = p[1]
            p[0].addArgumentDeclaration(p[3], False)
        elif len(p) == 5:
            p[0] = p[1]
            p[0].addArgumentDeclaration(p[4], True)

    def p_args(self, p):
        """args : args COMMA IDENTIFIER
                | IDENTIFIER"""
        if len(p) == 2:
            p[0] = ArgsNode()
            p[0].addArgument(IdentifierNode(p[1]))
        elif len(p) == 4:
            p[0] = p[1]
            p[0].addArgument(IdentifierNode(p[3]))

    def p_expression(self, p):
        """expression : value
                      | value PLUS value
                      | value MINUS value
                      | value ASTERISK value
                      | value SLASH value
                      | value PERCENT value"""
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = BinaryOperatorNode(p[2], p[1], p[3])

    def p_condition(self, p):
        """condition : value EQUAL value
                     | value NO_EQUAL value
                     | value GREATER value
                     | value LESS value
                     | value GREATER_EQUAL value
                     | value LESS_EQUAL value"""
        line_number = p.lexer.lineno
        p[0] = ConditionOperatorNode(p[2], p[1], p[3], line_number)

    def p_value(self, p):
        """value : NUMBER
                 | identifier"""
        if isinstance(p[1], int):
            p[0] = NumberNode(p[1])
        else:
            p[0] = p[1]

    def p_identifier(self, p):
        """identifier : IDENTIFIER
                      | IDENTIFIER LEFT_SQUARE_BRACKET NUMBER RIGHT_SQUARE_BRACKET
                      | IDENTIFIER LEFT_SQUARE_BRACKET IDENTIFIER RIGHT_SQUARE_BRACKET"""
        if len(p) == 2:
            p[0] = IdentifierNode(p[1])
        elif len(p) == 5 and isinstance(p[3], int):
            p[0] = IdentifierNode(ArrayNode(IdentifierNode(p[1]), NumberNode(p[3])))
        elif len(p) == 5 and isinstance(p[3], str):
            p[0] = IdentifierNode(ArrayNode(IdentifierNode(p[1]), IdentifierNode(p[3])))

    def p_error(self, p):
        print(f"Syntax error at line {p.lineno}. Unexpected token '{p.value}'")
        self.parser.errok()

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, debug=True, **kwargs)

    def parse(self, data, **kwargs):
        return self.parser.parse(data, lexer=Lexer().build(), **kwargs)
