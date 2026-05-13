from riscvmodel.insn import InstructionADDI
from test_ifu_rvc import *

from riscvmodel.regnames import x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x28, x29, x30, x31
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
            InstructionCADDI(x2, 5)
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {x1: 10, x2: 5}

class CADDI4SPNTest(Program):
    """Basic test of C.ADDI4SPN instruction"""

    def __init__(self):
        insns = [
            InstructionCADDI4SPN(x1, 2),
            InstructionCADDI4SPN(x1, 1),
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {x1: 12}


RV32IC_TESTS = {
    "caddi4spn": InstructionCADDI4SPN,
    "clw":       InstructionCLW,
    "csw":       InstructionCSW,
    "caddi":     InstructionCADDI,
    "cjal":      InstructionCJAL,   
    "cli":       InstructionCLI,
    "caddi16sp": InstructionCADDI16SP,
    "clui":      InstructionCLUI,
    "csrli":     InstructionCSRLI,
    "csrai":     InstructionCSRAI,
    "candi":     InstructionCANDI,
    "csub":      InstructionCSUB,
    "cxor":      InstructionCXOR,
    "cor":       InstructionCOR,
    "cand":      InstructionCAND,
    "cj":        InstructionCJ,
    "cslli":     InstructionCSLLI,
    "clwsp":     InstructionCLWSP,
    "cjr":       InstructionCJR,
    "cmv":       InstructionCMV,
    "cebreak":   InstructionCEBREAK,
    "cjalr":     InstructionCJALR,
    "cadd":      InstructionCADD,
    "cswsp":     InstructionCSWSP,
}
