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

def _reg3(r: int) -> int:
    """Extract the 3-bit compressed register field (assumes r in 8..15)."""
    return r & 0x7

def InstructionCADDI4SPN(rd_prime: int, nzuimm: int) -> RVCMetaInstruction:
    op = 0b00
    funct3 = 0b000
    u = nzuimm & 0x3FF
    nzuimm_5_4 = (u >> 4) & 0x3
    nzuimm_9_6 = (u >> 6) & 0xF
    nzuimm_2   = (u >> 2) & 0x1
    nzuimm_3   = (u >> 3) & 0x1
    rd3 = _reg3(rd_prime)
    insn = (funct3 << 13) | (nzuimm_5_4 << 11) | (nzuimm_9_6 << 7) | \
           (nzuimm_2 << 6) | (nzuimm_3 << 5) | (rd3 << 2) | op
    return RVCMetaInstruction(insn)

def InstructionCLW(rd_prime: int, rs1_prime: int, uimm: int) -> RVCMetaInstruction:
    op = 0b00
    funct3 = 0b010
    u = uimm & 0x7F
    uimm_5_3 = (u >> 3) & 0x7
    uimm_2   = (u >> 2) & 0x1
    uimm_6   = (u >> 6) & 0x1
    insn = (funct3 << 13) | (uimm_5_3 << 10) | (_reg3(rs1_prime) << 7) | \
           (uimm_2 << 6) | (uimm_6 << 5) | (_reg3(rd_prime) << 2) | op
    return RVCMetaInstruction(insn)

def InstructionCSW(rs1_prime: int, rs2_prime: int, uimm: int) -> RVCMetaInstruction:
    op = 0b00
    funct3 = 0b110
    u = uimm & 0x7F
    uimm_5_3 = (u >> 3) & 0x7
    uimm_2   = (u >> 2) & 0x1
    uimm_6   = (u >> 6) & 0x1
    insn = (funct3 << 13) | (uimm_5_3 << 10) | (_reg3(rs1_prime) << 7) | \
           (uimm_2 << 6) | (uimm_6 << 5) | (_reg3(rs2_prime) << 2) | op
    return RVCMetaInstruction(insn)
 
def InstructionCADDI(rd: int, imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b000
    imm6 = imm & 0x3F
    nzimm5   = (imm6 >> 5) & 1
    nzimm4_0 = imm6 & 0x1F
    insn = (funct3 << 13) | (nzimm5 << 12) | (rd << 7) | (nzimm4_0 << 2) | op
    return RVCMetaInstruction(insn)
 
def InstructionCJAL(imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b001
    o = imm & 0xFFF
    bit11 = (o >> 11) & 1
    bit4  = (o >> 4)  & 1
    bit98 = (o >> 8)  & 0x3
    bit10 = (o >> 10) & 1
    bit6  = (o >> 6)  & 1
    bit7  = (o >> 7)  & 1
    bit31 = (o >> 1)  & 0x7
    bit5  = (o >> 5)  & 1
    imm_field = (bit11 << 10) | (bit4 << 9) | (bit98 << 7) | (bit10 << 6) | \
                (bit6  <<  5) | (bit7 << 4) | (bit31 <<  1) | bit5
    insn = (funct3 << 13) | (imm_field << 2) | op
    return RVCMetaInstruction(insn)
 
def InstructionCLI(rd: int, imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b010
    imm6 = imm & 0x3F
    imm5   = (imm6 >> 5) & 1
    imm4_0 = imm6 & 0x1F
    insn = (funct3 << 13) | (imm5 << 12) | (rd << 7) | (imm4_0 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCADDI16SP(imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b011
    rd = 2  # x2 = sp
    n = imm & 0x3FF
    bit9   = (n >> 9) & 1
    bit4   = (n >> 4) & 1
    bit6   = (n >> 6) & 1
    bit8_7 = (n >> 7) & 0x3
    bit5   = (n >> 5) & 1
    imm_field = (bit9 << 5) | (bit4 << 4) | (bit6 << 3) | (bit8_7 << 1) | bit5
    # imm_field is 6 bits: bit[5] → position 12, bits[4:0] → positions 6:2
    insn = (funct3 << 13) | ((imm_field >> 5 & 1) << 12) | (rd << 7) | \
           ((imm_field & 0x1F) << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCLUI(rd: int, imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b011
    imm6 = imm & 0x3F
    imm5   = (imm6 >> 5) & 1
    imm4_0 = imm6 & 0x1F
    insn = (funct3 << 13) | (imm5 << 12) | (rd << 7) | (imm4_0 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCSRLI(rs1_prime: int, shamt: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b100
    s = shamt & 0x3F
    sh5   = (s >> 5) & 1
    sh4_0 = s & 0x1F
    insn = (funct3 << 13) | (sh5 << 12) | (0b00 << 10) | \
           (_reg3(rs1_prime) << 7) | (sh4_0 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCSRAI(rs1_prime: int, shamt: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b100
    s = shamt & 0x3F
    sh5   = (s >> 5) & 1
    sh4_0 = s & 0x1F
    insn = (funct3 << 13) | (sh5 << 12) | (0b01 << 10) | \
           (_reg3(rs1_prime) << 7) | (sh4_0 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCANDI(rs1_prime: int, imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b100
    imm6 = imm & 0x3F
    imm5   = (imm6 >> 5) & 1
    imm4_0 = imm6 & 0x1F
    insn = (funct3 << 13) | (imm5 << 12) | (0b10 << 10) | \
           (_reg3(rs1_prime) << 7) | (imm4_0 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCSUB(rd_prime: int, rs2_prime: int) -> RVCMetaInstruction:
    op = 0b01
    insn = (0b100 << 13) | (0 << 12) | (0b11 << 10) | \
           (_reg3(rd_prime) << 7) | (0b00 << 5) | (_reg3(rs2_prime) << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCXOR(rd_prime: int, rs2_prime: int) -> RVCMetaInstruction:
    op = 0b01
    insn = (0b100 << 13) | (0 << 12) | (0b11 << 10) | \
           (_reg3(rd_prime) << 7) | (0b01 << 5) | (_reg3(rs2_prime) << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCOR(rd_prime: int, rs2_prime: int) -> RVCMetaInstruction:
    op = 0b01
    insn = (0b100 << 13) | (0 << 12) | (0b11 << 10) | \
           (_reg3(rd_prime) << 7) | (0b10 << 5) | (_reg3(rs2_prime) << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCAND(rd_prime: int, rs2_prime: int) -> RVCMetaInstruction:
    op = 0b01
    insn = (0b100 << 13) | (0 << 12) | (0b11 << 10) | \
           (_reg3(rd_prime) << 7) | (0b11 << 5) | (_reg3(rs2_prime) << 2) | op
    return RVCMetaInstruction(insn) 
 
def InstructionCJ(imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b101
    o = imm & 0xFFF
    bit11 = (o >> 11) & 1
    bit4  = (o >> 4)  & 1
    bit98 = (o >> 8)  & 0x3
    bit10 = (o >> 10) & 1
    bit6  = (o >> 6)  & 1
    bit7  = (o >> 7)  & 1
    bit31 = (o >> 1)  & 0x7
    bit5  = (o >> 5)  & 1
    imm_field = (bit11 << 10) | (bit4 << 9) | (bit98 << 7) | (bit10 << 6) | \
                (bit6  <<  5) | (bit7 <<  4) | (bit31 <<  1) | bit5
    insn = (funct3 << 13) | (imm_field << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCBEQZ(rs1_prime: int, imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b110
    o = imm & 0x1FF
    bit8   = (o >> 8) & 1
    bit4_3 = (o >> 3) & 0x3
    bit7_6 = (o >> 6) & 0x3
    bit2_1 = (o >> 1) & 0x3
    bit5   = (o >> 5) & 1
    insn = (funct3 << 13) | (bit8 << 12) | (bit4_3 << 10) | \
           (_reg3(rs1_prime) << 7) | (bit7_6 << 5) | (bit2_1 << 3) | \
           (bit5 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCBNEZ(rs1_prime: int, imm: int) -> RVCMetaInstruction:
    op = 0b01
    funct3 = 0b111
    o = imm & 0x1FF
    bit8   = (o >> 8) & 1
    bit4_3 = (o >> 3) & 0x3
    bit7_6 = (o >> 6) & 0x3
    bit2_1 = (o >> 1) & 0x3
    bit5   = (o >> 5) & 1
    insn = (funct3 << 13) | (bit8 << 12) | (bit4_3 << 10) | \
           (_reg3(rs1_prime) << 7) | (bit7_6 << 5) | (bit2_1 << 3) | \
           (bit5 << 2) | op
    return RVCMetaInstruction(insn)
  
def InstructionCSLLI(rd: int, shamt: int) -> RVCMetaInstruction:
    op = 0b10
    funct3 = 0b000
    s = shamt & 0x3F
    sh5   = (s >> 5) & 1
    sh4_0 = s & 0x1F
    insn = (funct3 << 13) | (sh5 << 12) | (rd << 7) | (sh4_0 << 2) | op
    return RVCMetaInstruction(insn)
 
def InstructionCLWSP(rd: int, uimm: int) -> RVCMetaInstruction:
    op = 0b10
    funct3 = 0b010
    u = uimm & 0xFF
    bit5   = (u >> 5) & 1
    bit4_2 = (u >> 2) & 0x7
    bit7_6 = (u >> 6) & 0x3
    insn = (funct3 << 13) | (bit5 << 12) | (rd << 7) | \
           (bit4_2 << 4) | (bit7_6 << 2) | op
    return RVCMetaInstruction(insn)
 

def InstructionCJR(rs1: int) -> RVCMetaInstruction:
    op = 0b10
    insn = (0b1000 << 12) | (rs1 << 7) | (0b00000 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCMV(rd: int, rs2: int) -> RVCMetaInstruction:
    op = 0b10
    insn = (0b1000 << 12) | (rd << 7) | (rs2 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCEBREAK() -> RVCMetaInstruction:
    return RVCMetaInstruction(0x9002)
 
 
def InstructionCJALR(rs1: int) -> RVCMetaInstruction:
    op = 0b10
    insn = (0b1001 << 12) | (rs1 << 7) | (0b00000 << 2) | op
    return RVCMetaInstruction(insn)
 
 
def InstructionCADD(rd: int, rs2: int) -> RVCMetaInstruction:
    op = 0b10
    insn = (0b1001 << 12) | (rd << 7) | (rs2 << 2) | op
    return RVCMetaInstruction(insn)
 
def InstructionCSWSP(rs2: int, uimm: int) -> RVCMetaInstruction:
    op = 0b10
    funct3 = 0b110
    u = uimm & 0xFF
    uimm_5_2 = (u >> 2) & 0xF
    uimm_7_6 = (u >> 6) & 0x3
    insn = (funct3 << 13) | (uimm_5_2 << 9) | (uimm_7_6 << 7) | \
           (rs2 << 2) | op
    return RVCMetaInstruction(insn)
