"""
抽象语法树(AST)节点定义
定义了中文智能合约编译器的所有AST节点类型
"""

from typing import List, Optional, Any
from enum import Enum


class NodeType(Enum):
    """AST节点类型枚举"""
    PROGRAM = "program"
    CONTRACT = "contract"
    FUNCTION = "function"
    CONSTRUCTOR = "constructor"
    STATE_VARIABLE = "state_variable"
    EVENT = "event"
    PARAMETER = "parameter"
    BLOCK = "block"
    RETURN_STATEMENT = "return_statement"
    IF_STATEMENT = "if_statement"
    FOR_STATEMENT = "for_statement"
    WHILE_STATEMENT = "while_statement"
    EXPRESSION_STATEMENT = "expression_statement"
    VARIABLE_DECLARATION = "variable_declaration"
    ASSIGNMENT = "assignment"
    BINARY_EXPRESSION = "binary_expression"
    UNARY_EXPRESSION = "unary_expression"
    CALL_EXPRESSION = "call_expression"
    MEMBER_EXPRESSION = "member_expression"
    INDEX_EXPRESSION = "index_expression"
    IDENTIFIER = "identifier"
    LITERAL = "literal"


class Visibility(Enum):
    """可见性修饰符"""
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"
    EXTERNAL = "external"


class Mutability(Enum):
    """状态可变性修饰符"""
    PURE = "pure"
    VIEW = "view"
    PAYABLE = "payable"
    NONE = "none"


class ASTNode:
    """AST节点基类"""
    def __init__(self, node_type: NodeType, line: int = 0, column: int = 0):
        self.node_type = node_type
        self.line = line
        self.column = column


class Program(ASTNode):
    """程序根节点"""
    def __init__(self, contracts=None, line=0, column=0):
        super().__init__(NodeType.PROGRAM, line, column)
        self.contracts = contracts if contracts is not None else []


class Contract(ASTNode):
    """合约节点"""
    def __init__(self, name="", state_variables=None, functions=None, events=None, constructor=None, line=0, column=0):
        super().__init__(NodeType.CONTRACT, line, column)
        self.name = name
        self.state_variables = state_variables if state_variables is not None else []
        self.functions = functions if functions is not None else []
        self.events = events if events is not None else []
        self.constructor = constructor


class StateVariable(ASTNode):
    """状态变量节点"""
    def __init__(self, name="", var_type="", visibility=Visibility.PRIVATE, initial_value=None, line=0, column=0):
        super().__init__(NodeType.STATE_VARIABLE, line, column)
        self.name = name
        self.var_type = var_type
        self.visibility = visibility
        self.initial_value = initial_value


class Function(ASTNode):
    """函数节点"""
    def __init__(self, name="", parameters=None, return_type=None, visibility=Visibility.PUBLIC, 
                 mutability=Mutability.NONE, body=None, line=0, column=0):
        super().__init__(NodeType.FUNCTION, line, column)
        self.name = name
        self.parameters = parameters if parameters is not None else []
        self.return_type = return_type
        self.visibility = visibility
        self.mutability = mutability
        self.body = body


class Constructor(ASTNode):
    """构造函数节点"""
    def __init__(self, parameters=None, body=None, line=0, column=0):
        super().__init__(NodeType.CONSTRUCTOR, line, column)
        self.parameters = parameters if parameters is not None else []
        self.body = body


class Event(ASTNode):
    """事件节点"""
    def __init__(self, name="", parameters=None, line=0, column=0):
        super().__init__(NodeType.EVENT, line, column)
        self.name = name
        self.parameters = parameters if parameters is not None else []


class Parameter(ASTNode):
    """参数节点"""
    def __init__(self, name="", param_type="", line=0, column=0):
        super().__init__(NodeType.PARAMETER, line, column)
        self.name = name
        self.param_type = param_type


class Block(ASTNode):
    """代码块节点"""
    def __init__(self, statements=None, line=0, column=0):
        super().__init__(NodeType.BLOCK, line, column)
        self.statements = statements if statements is not None else []


class Statement(ASTNode):
    """语句基类"""
    pass


class ReturnStatement(Statement):
    """返回语句节点"""
    def __init__(self, value=None, line=0, column=0):
        super().__init__(NodeType.RETURN_STATEMENT, line, column)
        self.value = value


class IfStatement(Statement):
    """条件语句节点"""
    def __init__(self, condition=None, then_block=None, else_block=None, line=0, column=0):
        super().__init__(NodeType.IF_STATEMENT, line, column)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class ForStatement(Statement):
    """循环语句节点"""
    def __init__(self, init=None, condition=None, update=None, body=None, line=0, column=0):
        super().__init__(NodeType.FOR_STATEMENT, line, column)
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body


class WhileStatement(Statement):
    """while循环语句节点"""
    def __init__(self, condition=None, body=None, line=0, column=0):
        super().__init__(NodeType.WHILE_STATEMENT, line, column)
        self.condition = condition
        self.body = body


class ExpressionStatement(Statement):
    """表达式语句节点"""
    def __init__(self, expression=None, line=0, column=0):
        super().__init__(NodeType.EXPRESSION_STATEMENT, line, column)
        self.expression = expression


class VariableDeclaration(Statement):
    """变量声明节点"""
    def __init__(self, name="", var_type="", initial_value=None, line=0, column=0):
        super().__init__(NodeType.VARIABLE_DECLARATION, line, column)
        self.name = name
        self.var_type = var_type
        self.initial_value = initial_value


class Expression(ASTNode):
    """表达式基类"""
    pass


class Assignment(Expression):
    """赋值表达式节点"""
    def __init__(self, left=None, operator="=", right=None, line=0, column=0):
        super().__init__(NodeType.ASSIGNMENT, line, column)
        self.left = left
        self.operator = operator
        self.right = right


class BinaryExpression(Expression):
    """二元表达式节点"""
    def __init__(self, left=None, operator="", right=None, line=0, column=0):
        super().__init__(NodeType.BINARY_EXPRESSION, line, column)
        self.left = left
        self.operator = operator
        self.right = right


class UnaryExpression(Expression):
    """一元表达式节点"""
    def __init__(self, operator="", operand=None, prefix=True, line=0, column=0):
        super().__init__(NodeType.UNARY_EXPRESSION, line, column)
        self.operator = operator
        self.operand = operand
        self.prefix = prefix


class CallExpression(Expression):
    """函数调用表达式节点"""
    def __init__(self, callee=None, arguments=None, line=0, column=0):
        super().__init__(NodeType.CALL_EXPRESSION, line, column)
        self.callee = callee
        self.arguments = arguments if arguments is not None else []


class MemberExpression(Expression):
    """成员访问表达式节点"""
    def __init__(self, object=None, property="", line=0, column=0):
        super().__init__(NodeType.MEMBER_EXPRESSION, line, column)
        self.object = object
        self.property = property


class IndexExpression(Expression):
    """索引访问表达式节点"""
    def __init__(self, object=None, index=None, line=0, column=0):
        super().__init__(NodeType.INDEX_EXPRESSION, line, column)
        self.object = object
        self.index = index


class Identifier(Expression):
    """标识符节点"""
    def __init__(self, name="", line=0, column=0):
        super().__init__(NodeType.IDENTIFIER, line, column)
        self.name = name


class Literal(Expression):
    """字面量节点"""
    def __init__(self, value=None, literal_type="", line=0, column=0):
        super().__init__(NodeType.LITERAL, line, column)
        self.value = value
        self.literal_type = literal_type

