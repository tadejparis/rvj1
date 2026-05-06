import cocotb
from riscvmodel.insn import *
from riscvmodel.variant import RV32I
from riscvmodel.regnames import x0, x1, x2, a0

def InstructionCADDIManual(rd: int, imm: int) -> int:
    funct3 = 0b000
    op = 0b01
    imm6 = imm & 0x3F
    nzimm5 = (imm6 >> 5) & 1      # bit 5 (MSB/sign bit)
    nzimm4_0 = imm6 & 0x1F        # bits 4:0
    return (funct3 << 13) | (nzimm5 << 12) | (rd << 7) | (nzimm4_0 << 2) | op

# TODO is this manual encoding correct?


def create_program() -> list:
    instructions = [
        InstructionADDI(rd=a0, rs1=x0, imm=42).encode(),
        #InstructionCADDIManual(rd=a0, imm = 5)
    ]
    return instructions

def write_hex(instructions: list, path: str, base_addr: int = 0):
    with open(path, "w") as f:
        #f.write(f"@{base_addr:08X}\n")
        for insn in instructions:
            f.write(f"{insn:08X}\n")

instructions = create_program()
write_hex(instructions, "test.hex")
