from enum import Enum
from typing import Dict, Union, Tuple, Optional

"""
This module contains the containers for Hardware Description Language Abstract Syntax Tree (HDL AST)

(System) Verilog/VHDL can be converted by this format and back using this library
Main container is HdlContext which can store all other objects.

:note: this module is using PEP484 type hints, and the typehints are in comments
    to sustain Python 2.7 compatibility
:attention: this module is just simple format of HDL and does not performs all check,
    e.g. you can use a string as a type of the port, but such a module can not be synthetised

:attention: classes in his module are used from C++
"""


class CodePosition():
    __slots__ = ["startLine", "stopLine", "startColumn", "stopColumn"]

    def __init__(self, startLine, stopLine, startColumn, stopColumn):
        self.startLine = startLine  # type: int
        self.stopLine = stopLine  # type: int
        self.startColumn = startColumn  # type: int
        self.stopColumn = stopColumn  # type: int


class HdlDirection(Enum):
    (IN,
    OUT,
    INOUT,
    BUFFER,
    LINKAGE,
    INTERNAL,
    UNKNOWN) = range(6)


class HdlName(str):
    """
    Reference to name string in name table
    """
    __slots__ = []


class HdlAll():
    """
    Constant which corresponds to VHDL "all" keyword or "*" in verilog sensitivitylist
    """
    __slots__ = []


class HdlTypeType():
    """
    Type which means that the object is type of type
    """
    __slots__ = []


HdlTypeInt = int
HdlTypeStr = str
HdlTypeFloat = float
HdlTypeEnum = Enum


# arrays are described as HdlCall(HdlBuildinFn.INDEX, (type, array size))
# [TODO] HdlTypeStruct/Union
class HdlTypeBits():
    """
    The type which represents bit or bit vector in HDL (std_logic/_vector in VHDL [0:8] in verilog)

    :note: you should let lsb=0, it is there only for legacy issues
    """
    __slots__ = ["msb", "lsb", "signed"]

    def __init__(self, msb, lsb=0, signed=False):
        self.msb = msb
        self.lsb = lsb
        self.signed = signed

    def __hash__(self):
        return hash((self.msb, self.lsb, self.signed))

    def __eq__(self, other):
        return isinstance(other, HdlTypeBits) and (
            self.msb == other.msb
            and self.lsb == other.lsb
            and self.signed == other.signed)

class HdlImport(list):
    """
    Container for import in HDL code

    this is List[Union[HdlName, HdlAll]]
    """
    __slots__ = []


class HdlTypeAuto():
    """
    Type which means that the type is automatically resolved from the type of the value
    """
    __slots__ = []


class iHdlObj():
    """
    Object with direct represenation in HDL

    :ivar doc: doc from the HDL related probably to this object
    """
    __slots__ = ["doc"]

    def __init__(self):
        self.doc: str = ""


class HdlIntValue():
    """
    Object for represenation of int value in in HDL (= also for the bitstrings)
    """
    __slots__ = ["val", "bits"]

    def __init__(self, val, bits):
        self.val = val  # type: int
        self.bits = bits  # type: Optional[int]


# None is equivalent of HDL null
iHdlExpr = Union[HdlName, HdlInt, float, string, None, List["iHdlExpr"], HdlAll, "HdlCall"]


class HdlBuildinFn(Enum):
    """
    The build in functions and operators in HDL languages
    """
    (
    RANGE,  # range used in VHDL type specifications
    REVERSE_RANGE,
    ACROSS,
    THROUGH,
    REFERENCE,
    TOLERANCE,
    INDEX,  # array index
    DOWNTO,  # downto for the slice specification
    TO,  # to for the slice specification
    SUB,  # can also be unary minus
    ADD,  # can also be unary plus
    DIV,
    MUL,
    MOD,
    REM,
    CONCAT,  # concatenation of signals
    REPL_CONCAT,  # replicative concatenation {<N>, <item>} duplicates and concatenates the item N times
    POW,  # bin operator power of
    ABS,  # absolute value
    NOT,
    NEG,  # negation
    LOG_AND,
    LOG_OR,
    AND,
    OR,
    NAND,
    NOR,
    XOR,
    XNOR,
    EQ,  # ==
    NEQ,  # ~
    LOWERTHAN,  # <
    LE,  # <=
    GREATERTHAN,  # >
    GE,  # >=
    SLL,  # shift left logical
    SRL,  # shift right logical
    SLA,  # shift left arithmetical
    SRA,  # shift right arithmetical
    ROL,  # rotate left
    ROR,  # rotate right
    TERNARY,
    DOT,
    CALL,
    ARROW,  # arrow operator used in vhdl type descriptions
    RISING,  # rising edge/posedge event operator
    FALLING,  # falling edge/negedge event operator
    MAP_ASSOCIATION,
    MATCH_EQ,  # VHDL-2008 matching ops (the X values are ignored while match)
    MATCH_NEQ,
    MATCH_LT,
    MATCH_LE,
    MATCH_GT,
    MATCH_GE,
    ) = range(53)
    # note that in verilog bitewise operators can have only one argument


class HdlCall():
    """
    Container for call of the HDL function in HDL code
    """
    __slots__ = ["fn", "ops"]

    def __init__(self):
        self.fn = None  # type: Union[HdlBuildinFn, iHdlExpr]
        self.ops = []  # type: List[iHdlExpr]


class iHdlObjWithName(iHdlObj):
    """
    :ivar name: reference to name of the object
    """
    __slots__ = ["name"]

    def __init__(self):
        super(iHdlObjWithName, self).__init__()
        self.name = None  # type: HdlName


class iInModuleHdlObj():
    """
    Object which can apear in the module body
    """
    __slots__ = []


class HdlImport(iHdlObj):
    """
    The import statements used in VHDL

    :note: note that this does not corresponds to include as include is processed by preprocessor
    :ivar path: the list of namemes which are in the import
    :ivar wildcard: flag if true all objects from specified namespace should be imported
    """
    __slots__ = ["path", "wildcard"]

    def __init__(self):
        self.path = []  # type: List[str]
        self.wildcard = False  # type: bool


class HdlVariableDef(iHdlObj, iInModuleHdlObj):
    __slots__ = ["type", "value", "latched", "direction"]

    def __init__(self):
        iHdlObj.__init__(self)
        iInModuleHdlObj.__init__(self)
        self.type = None  # type: HdlType
        self.value = None  # iHdlExpr
        self.latched = False  # type: bool
        self.direction = None  # type: HdlDirection


class HdlNamespace(iHdlObjWithName):
    """
    Corresponds to VHDL package/package body or System Verilog namespace
    """
    __slots__ = ["objs"]

    def __init__(self):
        super(HdlNamespace, self).__init__()
        self.objs = []  # type: List[iHdlObj]


class HdlModuleDec(HdlNamespace):
    """
    HDL Module declaration

    Corresponds to VHDL entity and the first first part of the module with the ports and parameters
    """
    __slots__ = ["params", "ports", objs]

    def __init__(self):
        super(HdlModuleDec, self).__init__()
        self.params = []  # type: List[HdlVariableDef]
        self.ports = []  # type: List[HdlVariableDef]


class HdlModuleDef(iHdlObjWithName):
    """
    :ivar name: name of the architecture in VHDL or name of module in Verilog
    :ivar module_name: the name of entity in VHDL or same as name in Verilog
    """
    __slots__ = ["module_name", "objs"]

    def __init__(self):
        super(HdlModuleDef, self).__init__()
        self.module_name = None  # type: HdlName
        self.objs = []  # type: List[Union[iHdlObj, iInModuleHdlObj]]


class HdlComponentInst(iHdlObjWithName, iInModuleHdlObj):
    """
    HDL Component insance

    :ivar name: name of this component instance in this module
    :ivar module_name: HdlId or iHdlExpr made from HdlIds and dot operators
    :ivar param_map: same as port_map just port parameters of the component
    :ivar port_map: the list of iHdlExpr with map operator for map assignment or any other iHdlExpr for positional mapping
    """
    __slots__ = ["module_name", "param_map", "port_map"]

    def __init__(self):
        iHdlObjWithName.__init__(self)
        iInModuleHdlObj.__init__(self)
        self.module_name = None  # type: iHdlExpr
        self.param_map = []  # type: List[iHdlExpr]
        self.port_map = []  # type: List[iHdlExpr]


class iHdlStatement(iHdlObj, iInModuleHdlObj):
    """
    :ivar labels: list of labes, the first label is for this statement
        the others are for it's branches
    :ivar in_preproc: if True the statement is VHDL generate
            or other different of type of statement which should be evaluated complile time
    """
    __slots__ = ["labels", "in_preproc"]

    def __init__(self):
        iHdlObj.__init__(self)
        iInModuleHdlObj.__init__(self)
        self.labels = []  # type: List[HdlName]
        self.in_prepoc = False  # type: bool


class HdlStatementBlock(iHdlStatement, list):
    """
    Block of statements in HDL
    List[Union[iHdlExpr, iHdlStatement, HdlVariableDef, iHdlTypeDef]]
    """
    __slots__ = []

    def __init__(self):
        super(HdlStatementBlock, self).__init__()


class HdlAssignStm(iHdlStatement):
    """
    HDL assignment (blocking/non blocking is resolved from type of the variable)
    """
    __slots__ = ["src", "dst"]

    def __init__(self):
        super(HdlAssignStm, self).__init__(iHdlStatement)
        self.src = None  # type: iHdlExpr
        self.dst = None  # type: iHdlExpr


class HdlIfStm(iHdlStatement):
    """
    HDL if statement

    :ivar cond: condition in if statement
    :ivar if_true: block of statements which is in if true branch
    :ivar elifs: tuples of
    """
    __slots__ = ["cond", "if_true", "if_false"]

    def __init__(self):
        super(HdlIfStm, self).__init__()
        self.cond = None  # type: iHdlExpr
        self.if_true = HdlStatementBlock()  # type: HdlStatementBlock
        self.elifs = []  # type: List[Tuple[iHdlExpr, HdlStatementBlock]]
        self.if_false = None  # type: Optional[HdlStatementBlock]


class HdlProcessStm(HdlStatementBlock, iHdlObjWithName):
    """
    HdlProcess statement
    the container of statements with the sensitivity specified

    :ivar sensitivity: optional list of expessions which specifies
        the trigger of the evaluation of the process
    """
    __slots__ = ["sensitivity"]

    def __init__(self):
        HdlStatementBlock.__init__(self)
        iHdlObjWithName.__init__(self)
        self.sensitivity = None  # type: Optional[iHdlExpr]


class HdlCaseStm(iHdlStatement):
    """
    HDL case statement
    """
    __slots__ = ["switch_on", "cases", "default"]

    def __init__(self):
        super(iHdlStatement, self).__init__()
        self.switch_on = None  # type: iHdlExpr
        self.cases = []  # type: List[Tuple[iHdlExpr, HdlStatementBlock]]
        self.default = None  # type: Optional[Tuple[iHdlExpr, HdlStatementBlock]]


class HdlForStm(iHdlStatement):
    """
    HDL for statement
    """
    __slots__ = ["params", "body"]

    def __init__(self):
        super(iHdlStatement, self).__init__()
        self.params = []  # type: List[iHdlExpr]
        self.body = []  # type: Tuple[iHdlExpr, HdlStatementBlock]


class HdlWhileStm(iHdlStatement):
    """
    HDL case statement
    """
    __slots__ = ["params", "body"]

    def __init__(self):
        super(iHdlStatement, self).__init__()
        self.cond = None  # type: iHdlExpr
        self.body = []  # type: Tuple[iHdlExpr, HdlStatementBlock]


class HdlReturnStm(iHdlStatement):
    """
    HDL return statement
    """
    __slots__ = ["val"]

    def __init__(self):
        super(iHdlStatement, self).__init__()
        self.val = None  # type: iHdlExpr


class HdlBreakStm(iHdlStatement):
    """
    HDL break statement
    """
    __slots__ = []


class HdlContinueStm(iHdlStatement):
    """
    HDL break statement
    """
    __slots__ = []


class HdlContext():
    """
    The container of the objects specified in HDL files

    :ivar objs: the list of the object from the HDL files
    """

    def __init__(self):
        self.objs = []  # type: List[iHdlObj]