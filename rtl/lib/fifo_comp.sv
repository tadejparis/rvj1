// 
// FIFO always reads in 32 bits of data. It outputs either 32 bit or 16 bit,
// depending on the last two bits (see RV compressed instrucitons). If the
// output is 16 bit, it is expected that the lower 16 bits of output_data_o
// are populated, and the other 16 bits is set to zero.
//

// LIMITATIONS:
// - assume DEPTH is po2 (for pointer arithmetic) TODO

module fifo_comp #(
  parameter int DEPTH=4
)(
    input  logic        clk_i,
    input  logic        rstn_i,

    output logic        input_ready_o,
    input  logic        input_valid_i,
    input  logic [31:0] input_data_i,

    input  logic        output_ready_i,
    output logic        output_valid_o,
    output logic [31:0] output_data_o
);
  reg [15:0] mem[DEPTH];
  logic [$clog2(DEPTH)-1:0] read_ptr, write_ptr, read_ptr_next, write_ptr_next;
  logic [$clog2(DEPTH + 1)-1:0] fifo_counter;

  logic input_fire, output_fire;
  assign input_fire = input_ready_o && input_valid_i;
  assign output_fire = output_ready_i && output_valid_o;

  // Next pointer
  always_comb begin
    // Check if 32 bit else compressed
      if (mem[read_ptr][1:0] == 2'b11) begin
        read_ptr_next = read_ptr + 2;
      end else begin
        read_ptr_next = read_ptr + 1;
      end
  end
  assign write_ptr_next = write_ptr + 2;
  
  // WRITE POINTER
  // Handling writing is easier since it is always 32 bits
  always_ff @(posedge clk_i) begin
    if (~rstn_i)
      write_ptr <= '0;
    else if (input_fire)
      write_ptr <= write_ptr_next;
  end

  // READ POINTER
  always_ff @(posedge clk_i) begin
    if (~rstn_i)
      read_ptr <= '0;
    else if (output_fire)
      read_ptr <= read_ptr_next;
  end

  // Parcel counter
  always_ff @(posedge clk_i) begin
    if (~rstn_i)
      fifo_counter <= '0;
    else if (input_fire && ~output_fire) // push / write
      fifo_counter <= fifo_counter + 2;
    else if (~input_fire && output_fire) // pop / read
      // Check if 32 bit else compressed
      if (mem[read_ptr][1:0] == 2'b11) begin
        fifo_counter <= fifo_counter - 2;
      end else begin
        fifo_counter <= fifo_counter - 1;
      end
    else if (input_fire && output_fire && mem[read_ptr][1:0] != 2'b11) begin
      // both read and write, reading 16 bit
      fifo_counter <= fifo_counter + 1;
    end
  end

  // Input data
  always_ff @(posedge clk_i) begin
    if (input_fire) begin
      mem[write_ptr    ] <= input_data_i[15:0];
      mem[write_ptr + 1] <= input_data_i[31:16];
    end
  end
  // Output data
  always_comb begin
    // Check if 32 bit else compressed
    if (mem[read_ptr][1:0] == 2'b11) begin
      output_data_o = {mem[read_ptr + 1], mem[read_ptr]};
    end else begin
      output_data_o = {16'b0, mem[read_ptr]}; // zero-padded compressed
    end
  end

  // fifo not empty?
  always_comb begin
    if (mem[read_ptr][1:0] == 2'b11) begin
      // 32 bit: assure at least two parcels remain in FIFO to be read
      output_valid_o = fifo_counter > 1 && (rstn_i);
    end else begin
      // 16 bit: we can read a single parcel
      output_valid_o = fifo_counter > 0 && (rstn_i);
    end
  end


  assign input_ready_o  = fifo_counter < DEPTH - 1;  // FIFO not full
endmodule
