from hdlConvertor.hdlAst import HdlName, HdlBuiltinFn, HdlIntValue, HdlCall, iHdlExpr


def BitsT(width, is_signed=False):
    """
    Create an AST expression of Bits type constructor
    (reg/std_logic_vector equivalent for BasicHdlSimModel)

    :type width: iHdlExpr
    """
    if isinstance(width, HdlCall):
        if width.fn == HdlBuiltinFn.DOWNTO:
            high, low = width.ops
            assert int(low) == 0
            width = int(high) + 1
        else:
            raise NotImplementedError(width)
    c = HdlCall()
    c.fn = HdlBuiltinFn.CALL
    c.ops = (
        HdlName("Bits3t"),
        HdlIntValue(width, None, None),
        HdlIntValue(int(is_signed), None, None)
    )
    return c


def sensitivityByOp(op):
    """
    Get sensitivity type for operator.

    :type op: HdlBuiltinFn
    :return: Tuple[sensitive on rising edge, sensitive to falling edge]
    """

    if op == HdlBuiltinFn.RISING:
        return (True, False)
    elif op == HdlBuiltinFn.FALLING:
        return (False, True)
    else:
        raise TypeError(op)