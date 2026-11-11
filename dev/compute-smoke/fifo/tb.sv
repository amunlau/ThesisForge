`timescale 1ns/1ps
module tb #(parameter integer DEPTH = 3);
    logic clk = 0;
    logic reset, in_valid, in_ready, out_valid, out_ready;
    logic [15:0] in_data, out_data;
    logic expected_ready, expected_valid;
    logic [15:0] expected_data;
    string vectors;
    integer fd, cycles, count, fields;
    fifo #(.DEPTH(DEPTH)) dut(.*);
    always #5 clk = ~clk;

    initial begin
        if (!$value$plusargs("vectors=%s", vectors) || !$value$plusargs("cycles=%d", cycles))
            $fatal(1, "missing vector file or expected cycle count");
        fd = $fopen(vectors, "r");
        if (fd == 0) $fatal(1, "could not open vectors");
        // Drive on the falling edge. Check the settled signals consumed by
        // the following rising edge, before the FIFO updates its pointers.
        for (count = 0; count < cycles; count = count + 1) begin
            @(negedge clk);
            fields = $fscanf(fd, "%d %d %d %d %d %d %d", reset, in_valid, in_data,
                             out_ready, expected_ready, expected_valid, expected_data);
            if (fields != 7) $fatal(1, "incomplete vector row %0d", count);
            #1;
            if (in_ready !== expected_ready || out_valid !== expected_valid ||
                    (expected_valid && out_data !== expected_data))
                $fatal(1, "cycle=%0d depth=%0d input(rst,v,d,ready)=%b,%b,%h,%b expected(ready,v,d)=%b,%b,%h got=%b,%b,%h",
                       count, DEPTH, reset, in_valid, in_data, out_ready, expected_ready,
                       expected_valid, expected_data, in_ready, out_valid, out_data);
            @(posedge clk);
        end
        $display("PASS depth=%0d cycles=%0d", DEPTH, count);
        $finish;
    end
endmodule
