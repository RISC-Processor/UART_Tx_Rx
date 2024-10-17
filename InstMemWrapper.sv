module InstMemWrapper (
	input logic  clk,
	input logic  rst,
	input logic  [7: 0] data_in,
	input logic  en,
	output logic [7: 0]  LED
);


reg [7:0] i = 0;
integer j;
reg [7: 0] InstMem [255: 0]; // To hold 64 instructions 

always @(posedge en) begin
 	 InstMem[i] <= data_in;
	 i <= i + 1;
end

initial begin
	i <= 0;
	for (j = 0; j <= 255; j = j + 1) begin
		InstMem[j] <= 8'b01010101;
	end
end

assign LED = InstMem[4];

endmodule