import cocotb
from riscvmodel.insn import *
from riscvmodel.variant import RV32I
from riscvmodel.regnames import x0, x1, x2, a0
from riscvmodel.isa import Instruction

class RVCMetaInstruction(Instruction):
    def __init__(self, encoding: int):
        self.encoding = encoding
    def encode(self) -> int:
        return self.encoding
    def execute(self, model):
        pass

def InstructionCADDIManual(rd: int, imm: int) -> RVCMetaInstruction:
    funct3 = 0b000
    op = 0b01
    imm6 = imm & 0x3F
    nzimm5 = (imm6 >> 5) & 1      # bit 5 (MSB/sign bit)
    nzimm4_0 = imm6 & 0x1F        # bits 4:0
    insn = RVCMetaInstruction((funct3 << 13) | (nzimm5 << 12) | (rd << 7) | (nzimm4_0 << 2) | op)
    return insn

def InstructionCADDI4SPNManual(): pass



