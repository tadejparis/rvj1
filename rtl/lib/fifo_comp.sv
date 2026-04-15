// 
// FIFO always reads in 32 bits of data. It outputs either 32 bit or 16 bit,
// depending on the last two bits (see RV compressed instrucitons). If the
// output is 16 bit, it is expected that the lower 16 bits of read_data_o
// are populated, and the other 16 bits is set to zero.
//

// LIMITATIONS:
// - assume DEPTH is po2 (for pointer arithmetic) TODO

module fifo_comp #(
  parameter int DEPTH=4
)(
    input  logic        clk_i,
    input  logic        rstn_i,

    output logic        write_ready_o,
    input  logic        write_valid_i,
    input  logic [31:0] write_data_i,

    input  logic        read_ready_i,
    output logic        read_valid_o,
    output logic [31:0] read_data_o,

    input  logic        input_err_i,
    output logic        output_err_o
);
  logic [15:0] mem[DEPTH];
  logic        err_mem[DEPTH];
  logic [$clog2(DEPTH)-1:0] read_ptr, write_ptr, read_ptr_next, write_ptr_next;
  logic [$clog2(DEPTH + 1)-1:0] fifo_counter;

  logic write_fire, read_fire;
  assign write_fire = write_ready_o && write_valid_i;
  assign read_fire = read_ready_i && read_valid_o;

  // Next pointer
  assign read_ptr_next = read_ptr + 2;
  assign write_ptr_next = write_ptr + 2;
  
  // WRITE POINTER
  // Handling writing is easier since it is always 32 bits
  always_ff @(posedge clk_i) begin
    if (~rstn_i)
      write_ptr <= '0;
    else if (write_fire)
      write_ptr <= write_ptr_next;
  end

  // READ POINTER
  always_ff @(posedge clk_i) begin
    if (~rstn_i)
      read_ptr <= '0;
    else if (read_fire)
      read_ptr <= read_ptr_next;
  end

  // Parcel counter
  always_ff @(posedge clk_i) begin
    if (~rstn_i)
      fifo_counter <= '0;
    else if (write_fire && ~read_fire) // push / write
      fifo_counter <= fifo_counter + 2;
    else if (~write_fire && read_fire) // pop / read
      fifo_counter <= fifo_counter - 2;
  end

  // Input data
  always_ff @(posedge clk_i) begin
    if (write_fire) begin
      mem[write_ptr    ] <= write_data_i[15:0];
      mem[write_ptr + 1] <= write_data_i[31:16];
    end
  end

  always_ff @(posedge clk_i) begin
    if (write_fire) begin
      err_mem[write_ptr    ] <= input_err_i;
      err_mem[write_ptr + 1] <= input_err_i;
    end
  end

  // Output data
  assign read_data_o = {mem[read_ptr + 1], mem[read_ptr]};
  assign output_err_o = err_mem[read_ptr];

  assign read_valid_o = fifo_counter > 1; // FIFO not empty
  assign write_ready_o  = fifo_counter < DEPTH - 1;  // FIFO not full
endmodule