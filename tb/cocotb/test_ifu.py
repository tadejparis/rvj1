from base import get_rtl_files
from forastero.io import IORole, io_suffix_style
from forastero import BaseBench
from forastero.monitor import MonitorEvent
from forastero.driver import DriverEvent
from cocotb.triggers import ClockCycles, RisingEdge
from rvj1.io import IfuToDecoderIO, IfuJmpIO
from rvj1.request import IfuJmpInitiator
from rvj1.response import IfuToDecMonitor, DecoderResponder
from rvj1.sequence import ifu_jmp_to_addr, dec_backpressure_seq
from rvj1.transaction import InstrAddrResponse
import os

from base import WAVES, RVFI, RVFI_TRACE, ASSERTIONS
from cocotb_tools.runner import get_runner

from riscvmodel.insn import *
from riscvmodel.variant import RV32I
from riscvmodel.regnames import x0, x1, x2, a0

from test_ifu_rvc import *

def create_program() -> list:
    instructions = [
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        InstructionADDI(rd=a0, rs1=x0, imm=42),
        #InstructionADDI(rd=a0, rs1=x0, imm=50),
        #InstructionADDI(rd=a0, rs1=x0, imm=42)
        InstructionCADDI(rd=a0, imm = 6),
        InstructionCADDI(rd=a0, imm = 6),
        InstructionCADDI(rd=a0, imm = 5),
        InstructionCADDI(rd=a0, imm = 5)
    ]
    return instructions

def write_hex(instructions: list, path: str, base_addr: int = 0):
    with open(path, "w") as f:
        ostanek = -1;
        for insn in instructions:
            encoded = insn.encode()
            left  = (encoded >> 16) & 0xFFFF
            right = encoded & 0xFFFF
            
            if (encoded & 0b11 == 0b11 and ostanek == -1):
                f.write(f"{left:04X}")
                f.write(f"{right:04X}\n")
                ostanek = -1
            elif encoded & 0b11 == 0b11:
                f.write(f"{right:04X}") # levi del vrstice
                f.write(f"{ostanek:04X}\n") # desni del vrstice
                ostanek = left
            elif encoded & 0b11 != 0b11 and ostanek == -1:
                ostanek = encoded  
            else:
                f.write(f"{encoded:04X}") # levi del vrstice
                f.write(f"{ostanek:04X}\n") # desni del vrstice
                ostanek = -1
                

instructions = create_program()
write_hex(instructions, "test.hex")


class IfuTB(BaseBench):
    def __init__(self, dut):
        super().__init__(dut, clk=dut.clk_i, rst=dut.rstn_i, rst_active_high=False)
        dec_io = IfuToDecoderIO(dut, "dec", IORole.INITIATOR, io_style=io_suffix_style)
        ifu_jmp_io = IfuJmpIO(dut, "jmp", IORole.RESPONDER, io_style=io_suffix_style)
        self.register(
            "dec_mon", 
            IfuToDecMonitor(self, dec_io, self.clk, self.rst),
            sb_filter=self.filter_dec_data_on_error
        )
        self.register(
            "dec_resp_drv",
            DecoderResponder(self, dec_io, self.clk, self.rst, blocking=False),
        )
        self.register(
            "ifu_jmp_drv",
            IfuJmpInitiator(self, ifu_jmp_io, self.clk, self.rst)
        )
        self.ifu_jmp_drv.subscribe(DriverEvent.POST_DRIVE, self.jump_change_counter)
        self.dec_mon.subscribe(MonitorEvent.CAPTURE, self.push_reference)
        self.counter = 1

    def push_reference(self, monitor, event, obj) -> None:
        target_addr = int(0x8000_0000 + (self.counter * 4))
        outofbounds = 0x8000_0100
        error = (target_addr > outofbounds)
        self.scoreboard.channels["dec_mon"].push_reference(
            InstrAddrResponse(
                instr=0 if error else instructions[self.counter-1], 
                error=error
            )
        )
        self.counter += 1


    def jump_change_counter(self, driver, event, obj):
        self.counter = int(((obj.addr - 0x8000_0000) / 4) + 1)

        
    def filter_dec_data_on_error(self, 
                            mon: IfuToDecMonitor,
                            event: MonitorEvent, 
                            obj: InstrAddrResponse) -> InstrAddrResponse | None:
        if obj.error:
            obj.instr = 0 # blank out instruction on error signal
        return obj	

    async def initialise(self) -> None:
        """Initialise the DUT's I/O"""
        self.rst.value = 0
        for comp in self._components.values():
            comp.io.initialise(IORole.opposite(comp.io.role))

    async def reset(self, init=True, wait_during=10, wait_after=1) -> None:
        """
        Reset the DUT.

        :param init:        Initialise the DUT's I/O
        :param wait_during: Clock cycles to hold reset active for (defaults to 20)
        :param wait_after:  Clock cycles to wait after lowering reset (defaults to 1)
        """
        # Drive reset high
        self.rst.value = 0
        # Initialise I/O
        if init:
            await self.initialise()
        # Wait before dropping reset
        if wait_during > 0:
            await ClockCycles(self.clk, wait_during)
        # Drop reset
        self.rst.value = 1
        # Wait for a bit
        if wait_after > 0:
            self.info(f"Waiting for {wait_after} cycles")
            await ClockCycles(self.clk, wait_after)


@IfuTB.testcase(
    reset_wait_during=2,
    reset_wait_after=0,
    timeout=100,
    shutdown_delay=1,
    shutdown_loops=2,

)
async def smoke(tb: IfuTB, log):
    await ClockCycles(tb.clk, 10)


@IfuTB.testcase(
    reset_wait_during=2,
    reset_wait_after=0,
    timeout=1000,
    shutdown_delay=1,
    shutdown_loops=2,

)
async def linear_run(tb: IfuTB, log):
    log.info("Scheduling random backpressure on the decoder interface.")
    tb.schedule(dec_backpressure_seq(dec=tb.dec_resp_drv), blocking=False)
    log.info("Using the jump interface to set the IFU (boot) address.")
    tb.schedule(ifu_jmp_to_addr(ifu_jmp_drv=tb.ifu_jmp_drv, addr=0x8000_0000))
    await ClockCycles(tb.clk, 300)

@IfuTB.testcase(
    reset_wait_during=2,
    reset_wait_after=0,
    timeout=1000,
    shutdown_delay=1,
    shutdown_loops=2,

)
async def run_and_jump(tb: IfuTB, log):
    log.info("Scheduling random backpressure on the decoder interface.")
    tb.schedule(dec_backpressure_seq(dec=tb.dec_resp_drv), blocking=False)
    log.info("Using the jump interface to set the IFU (boot) address.")
    tb.schedule(ifu_jmp_to_addr(ifu_jmp_drv=tb.ifu_jmp_drv, addr=0x8000_0000))
    await ClockCycles(tb.clk, 50)
    tb.schedule(ifu_jmp_to_addr(ifu_jmp_drv=tb.ifu_jmp_drv, addr=0x8000_006c))
    await ClockCycles(tb.clk, 100)


@IfuTB.testcase(
    reset_wait_during=2,
    reset_wait_after=0,
    timeout=1000,
    shutdown_delay=0,
    shutdown_loops=0
)
async def response_error(tb: IfuTB, log):
    log.info("Scheduling random backpressure on the decoder interface.")
    tb.schedule(dec_backpressure_seq(dec=tb.dec_resp_drv), blocking=False)
    log.info("Using the jump interface to set the IFU (boot) address.")
    tb.schedule(ifu_jmp_to_addr(ifu_jmp_drv=tb.ifu_jmp_drv, addr=0x8000_0000))
    await RisingEdge(tb.dec_error_o)
    await RisingEdge(tb.dec_ready_i)
    await ClockCycles(tb.clk, 10)

if __name__ == "__main__":
    sim = os.getenv("SIM", default="verilator")
    build_args = ["-Wno-fatal", "--no-stop-fail", "-Wno-REDEFMACRO"]
    if WAVES:
        build_args += ["--trace-fst"]
    if RVFI:
        build_args += [f"-DRVFI"]
    if RVFI_TRACE:
        build_args += [f"-DRVFI_TRACE"]
    if ASSERTIONS:
        build_args += [f"-DASSERTIONS"]
    runner = get_runner(sim)
    runner.build(
        sources=get_rtl_files("verilog"),
        includes=["/foss/designs/rvj1/rtl/inc"],
        build_args=build_args,
        hdl_toplevel="ifu_mem_test_top",
        parameters={"BASE_ADDR": 0x8000_0000, "MEM_SIZE_WORDS":64},
        always=True,
        waves=False,
    )
    runner.test(
        hdl_toplevel="ifu_mem_test_top", 
        test_module="test_ifu",
        plusargs=["+MEM_INIT_FILE0=/foss/designs/rvj1/tb/cocotb/test.hex"]
    )
  
