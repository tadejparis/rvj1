from riscvmodel.insn import InstructionADDI
from test_ifu_rvc import *

from riscvmodel.regnames import x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11,x13, x15, x22, x28, x29, x30, x31
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
            InstructionCADDI(x3, 5),
            InstructionCADDI(x3, 3)
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {x1: 10, x3: 8}

class CADDI4SPNTest(Program):
    """Basic test of C.ADDI4SPN instruction"""

    def __init__(self):
        insns = [
            InstructionCADDI4SPN(x9, 4),
            InstructionCADDI4SPN(x10, 4)
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {x9: 4, x10: 4}

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
    """Basic test of C.JAL instruction"""

    def __init__(self):
        insns = [
            InstructionCADDI(x2, 1),     # 0x8000_0000
            InstructionCADDI(x2, 1),     # 0x8000_0002
            InstructionADDI(x2, x0, 2),  # 0x8000_0004
            InstructionADDI(x3, x0, 3),  # 0x8000_0008
            InstructionCJAL(0x8),        # 0x8000_000c ->
            InstructionCADDI(x11, 11),   # 0x8000_000e   |
            InstructionADDI(x4, x0, 4),  # 0x8000_0010   |
            InstructionADDI(x5, x0, 5),  # 0x8000_0014 <-
            InstructionADDI(x6, x0, 6),  # 0x8000_0018
            InstructionADDI(x7, x0, 7),  # 0x8000_001c
            InstructionADDI(x8, x0, 8),  
            InstructionADDI(x9, x0, 9),
            InstructionADDI(x31, x0, 1)
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {
            0: 0,
            1: 0x8000000e,
            2: 2,
            3: 3,
            4: 0,
            5: 5,
            6: 6,
            7: 7,
            8: 8,
            9: 9,
            11: 0}

class CLITest(Program):
    """Basic test of C.LI instruction"""

    def __init__(self):
        insns = [
            InstructionCLI(x2, 4),
            InstructionCLI(x3, 5)
        ]
        super().__init__(insns)
    def expects(self) -> dict:
        return {            
            2: 4,
            3: 5,
        }

class CADDI16SPTest(Program):
    """Basic test of C.LI instruction"""

    def __init__(self):
        insns = [
            InstructionCADDI16SP(48),
            InstructionCADDI16SP(48)
        ]
        super().__init__(insns)
    def expects(self) -> dict:
        return {            
            2: 96,
        }

class CLUITEST(Program):
    """Basic test of C.LI instruction"""

    def __init__(self):
        insns = [
            InstructionCLUI(x3, 5),
            InstructionCLUI(x4, 5)
        ]
        super().__init__(insns)
    def expects(self) -> dict:
        return {            
            3: 0x5000,
            4: 0x5000,
        }

class CSWTest2(Program):
    """Basic test of C.LI instruction"""

    def __init__(self):
        insns = [
            InstructionADDI(x5, x0, 4),
            InstructionADDI(x8, x0, 4),
            InstructionADDI(x13, x0, 4),
            InstructionADDI(x15, x0, 4),
            InstructionADDI(x22, x0, 4),

            InstructionCSW(x8, x15, 8),
            InstructionCLI(x5, 1),
            InstructionADDI(x22, x0, -129),
            InstructionCADD(x22, x5),
            InstructionSW(x22, x8, 12),
            InstructionCADDI(x13, -1)
        ]
        super().__init__(insns)
    def expects(self) -> dict:
        return {            
            5: 1,
            8: 4,
            13: 3,
            15: 4,
            22: -128
        }


RV32IC_TESTS = {
    "caddi":     CADDITest(),
    "caddi4spn": CADDI4SPNTest(),
    "cswlw":     CSWLWTest(),
    "cjal":      CJALTest(),
    "cli":       CLITest(),
    "caddi16sp": CADDI16SPTest(),
    "clui":      CLUITEST(),
    "csw2":      CSWTest2()
}
