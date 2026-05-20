from riscvmodel.insn import InstructionADDI
from test_ifu_rvc import *

from riscvmodel.regnames import x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x28, x29, x30, x31
from riscvmodel.csrnames import misa, mscratch, mtvec, mepc, mcause, mstatus, mtval
from riscvmodel.program import Program

from collections.abc import Iterable

BOOT_ADDR = 0x8000_0000
DATA_ADDR = 0x8000_0400

def load_addr(addr: int, reg: int) -> list:
    upper_addr = addr & 0xFFFFF_000
    lower_addr = addr & 0x00000_FFF
    ret = [
        InstructionLUI(reg, (upper_addr >> 12)),
    ]
    if lower_addr != 0:
        ret.append(
            InstructionADDI(reg, reg, lower_addr)
        )
    return ret

def flatten_list(items, ignore_types=(bytes, str)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten_list(x)
        else:
            yield x

class CADDITest(Program):
    """Basic test of C.ADDI instruction"""

    def __init__(self):
        insns = [
            InstructionCADDI(x1, 2),
            InstructionCADDI(x1, 8),
            InstructionCADDI(x3, 5)
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {x1: 10, x3: 5}

class CADDI4SPNTest(Program):
    """Basic test of C.ADDI4SPN instruction"""

    def __init__(self):
        insns = [
            InstructionCADDI4SPN(x9, 4),
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {x9: 4}

class CSWLWTest(Program):
    """Basic test of C.SW and C.LW instruction"""

    def __init__(self):
        insns = [
            InstructionLUI(x8, 0),
            InstructionADDI(x8, x8, 4),
            load_addr(DATA_ADDR, x9),
            InstructionSW(x9, x8, 0),
            InstructionCLW(x10, x9, 0),
            InstructionCLW(x11, x9, 0),
            InstructionADDI(x31, x0, 1)
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {            
            x9: 0x80000400,
            x8: 4,
            x10: 4,
            x11: 4,
            x31: 0x1
            }

class CJALTest(Program):
    """Basic test of C.ADDI4SPN instruction"""

    def __init__(self):
        insns = [
            InstructionCADDI4SPN(x2, 8),
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {x2: 8}



RV32IC_TESTS = {
    "caddi":     CADDITest(),
    "caddi4spn": CADDI4SPNTest(),
    "cswlw":       CSWLWTest(),
}
