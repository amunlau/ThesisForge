// Single-clock FIFO with no empty bypass. A full FIFO can replace its head
// on the same edge. Reset flushes all entries and suppresses both handshakes.
module fifo #(parameter integer DEPTH = 3) (
    input logic clk, reset, in_valid, out_ready,
    input logic [15:0] in_data,
    output logic in_ready, out_valid,
    output logic [15:0] out_data
);
    localparam integer PTR_BITS = DEPTH > 1 ? $clog2(DEPTH) : 1;
    logic [PTR_BITS-1:0] rd_ptr, wr_ptr;
    logic [$clog2(DEPTH+1)-1:0] count;
    logic [15:0] data [0:DEPTH-1];

    assign out_valid = !reset && count != 0;
    assign out_data = data[rd_ptr];
    assign in_ready = !reset && (count < DEPTH || (out_valid && out_ready));
    wire pop = out_valid && out_ready;
    wire push = in_ready && in_valid;

    always_ff @(posedge clk) begin
        if (reset) begin
            rd_ptr <= '0;
            wr_ptr <= '0;
            count <= '0;
        end else begin
            if (pop) rd_ptr <= rd_ptr == DEPTH-1 ? '0 : rd_ptr + 1'b1;
            if (push) begin
                data[wr_ptr] <= in_data;
                wr_ptr <= wr_ptr == DEPTH-1 ? '0 : wr_ptr + 1'b1;
            end
            if (push && !pop) count <= count + 1'b1;
            if (pop && !push) count <= count - 1'b1;
        end
    end
endmodule
