`timescale 1ns/1ps
module tb;
  logic clk=0, rst, accept;
  logic [1:0] req, served, expected;
  integer edge_count=0, transfers=0, last_port, candidate;
  arbiter dut(.*);
  always #5 clk = ~clk;

  task automatic step(input bit reset, input bit enabled, input logic [1:0] requests);
    @(negedge clk);
    rst=reset; accept=enabled; req=requests; expected=0;
    if (reset) last_port=1;
    else if (enabled) begin
      for (int offset=1; offset<=2; offset++) begin
        candidate=(last_port+offset)%2;
        if (expected==0 && requests[candidate]) expected[candidate]=1;
      end
      if (expected!=0) last_port=expected[1];
    end
    @(posedge clk); #1;
    if (served !== expected)
      $fatal(1,"cycle=%0d rst=%b accept=%b req=%b expected=%b served=%b",
             edge_count,rst,accept,req,expected,served);
    edge_count++; if (served!=0) transfers++;
  endtask

  initial begin
    // Force each possible last winner, then exhaust all request/accept combinations.
    for (int last=0; last<2; last++)
      for (int en=0; en<2; en++)
        for (int r=0; r<4; r++) begin
          step(1,1,3); step(0,1,1<<last); step(0,en,r);
        end
    repeat (8) step(0,1,3);
    if (transfers!=30 || edge_count!=56) $fatal(1,"coverage incomplete");
    $display("PASS cycles=%0d transfers=%0d",edge_count,transfers);
    $finish;
  end
  initial #2000 $fatal(1,"timeout");
endmodule
