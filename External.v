module External(
	input 		          		CLOCK_50,
	output		     [7:0]		LED,
	input 		     [1:0]		KEY,
	input 		     [3:0]		SW,
	output wire Tx,
	input wire Rx
);

wire Txclk_en, Rxclk_en, Tx_busy, Ready_Byte;
wire [7:0] RegFiletToTx, Instruction_8;
wire ready;
			
					
InstMemWrapper InstMemWrapper_u(
					.clk(CLOCK_50),
					.rst(KEY[1]),
					.data_in(Instruction_8),
					.en(ready),
					.LED(LED)
					);

					
RegFileWrapper RegFileWrapper_u(
    .clk(CLOCK_50),        
    .rst(KEY[1]),
	 .en(KEY[0]),
	 .Tx_busy(Tx_busy),
	 .dout(RegFiletToTx),
	 .Ready_Byte(Ready_Byte),
//	 .LED(LED)
);


transmitter uart_Tx(
				   .data_in(RegFiletToTx),
					.wr_en(Ready_Byte),
					.clk_50m(CLOCK_50),
					.clken(Txclk_en), 
					.Tx(Tx),
					.Tx_busy(Tx_busy)
					); 
					
										
baudrate uart_baud(	
				   .clk_50m(CLOCK_50),
					.Rxclk_en(Rxclk_en),
					.Txclk_en(Txclk_en)
					);
					

receiver uart_Rx(  
				   .Rx(Rx),
			      .ready(ready),
					.clk_50m(CLOCK_50),
					.clken(Rxclk_en), 
					.data_out(Instruction_8)
					);


endmodule
