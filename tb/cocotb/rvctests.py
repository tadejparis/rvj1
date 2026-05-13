from riscvmodel.insn import InstructionADDI
from test_ifu_rvc import InstructionCADDIManual

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
            InstructionCADDIManual(x1, 2),
            InstructionCADDIManual(x1, 8),
            InstructionCADDIManual(x2, 5)
        ]
        super().__init__(insns)
    
    def expects(self) -> dict:
        return {x1: 10, x2: 5}


RVC_INSTRUCTIONS = {
    "CDDI4SPN": InstructionCADDI4SPN,
    "CFLD":      InstructionCFLD,
    "CLW":       InstructionCLW,
    "CSW":       InstructionCSW,
    "CADDI":     InstructionCADDI,
    "CJAL":      InstructionCJAL,   
    "CLI":       InstructionCLI,
    "CADDI16SP": InstructionCADDI16SP,
    "CLUI":      InstructionCLUI,
    "CSRLI":     InstructionCSRLI,
    "CSRAI":     InstructionCSRAI,
    "CANDI":     InstructionCANDI,
    "CSUB":      InstructionCSUB,
    "CXOR":      InstructionCXOR,
    "COR":       InstructionCOR,
    "CAND":      InstructionCAND,
    "CJ":        InstructionCJ,
    "CSLLI":     InstructionCSLLI,
    "CLWSP":     InstructionCLWSP,
    "CJR":       InstructionCJR,
    "CMV":       InstructionCMV,
    "CEBREAK":   InstructionCEBREAK,
    "CJALR":     InstructionCJALR,
    "CADD":      InstructionCADD,
    "CSWSP":     InstructionCSWSP,
}
