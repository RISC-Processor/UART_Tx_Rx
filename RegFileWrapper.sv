module RegFileWrapper (
    input  logic          clk,        
    input  logic          rst,
    input  logic          en,
    input  logic          Tx_busy,
    output logic  [7:0]   dout,        // Output is now 8 bits
    output logic          Ready_Byte   // Ready signal for 8-bit data
//  output logic  [7: 0]  LED
);
    
//  assign LED = {3'b0, incrementer};
//	 assign LED = registerFile[4][7: 0];
    
    // State encoding
    typedef enum logic [2:0] {
        IDLE,
        OUTPUT_REG,
        OUTPUT_BYTE,
		  SEND_BYTE,
		  BYTE_SENT,
		  REG_SENT
    } state_t;
    
    state_t current_state = IDLE, next_state;
    
    logic [4:0] incrementer;         // Register index
    logic [1:0] byte_counter;        // To keep track of which byte is being sent
    logic [31:0] registerFile [31:0]; // Register file with 32 registers, 32-bit each
    logic [31:0] current_reg_value;   // Holds the current 32-bit register value
    
	
	 
    // State transition logic
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            current_state <= IDLE;
        end else begin
            current_state <= next_state;
        end
    end

    // State machine logic
    always_comb begin
        next_state = current_state; // Default to current state

        case (current_state)
            IDLE: begin
                if (en) begin
                    next_state = OUTPUT_REG;
                end
            end
            OUTPUT_REG: begin
                if (incrementer <= 31) begin  // Wait for feedback from OUTPUT_BYTE state
						  next_state = OUTPUT_BYTE;  // Move to the next register
                end else begin
						next_state = IDLE;  // All registers processed
                end
            end
            OUTPUT_BYTE: begin
                if (!Tx_busy) begin  // Wait for Tx to finish
                    next_state = SEND_BYTE;
                end
					 else begin
						next_state = OUTPUT_BYTE;
						end
            end
				SEND_BYTE: begin
					// WAIT SOME TIME IN THIS STAGE
					if (!Tx_busy) begin  // Wait for Tx to finish
                    next_state = BYTE_SENT;
                end
					 else begin
						next_state = SEND_BYTE;
						end
				end
				
				BYTE_SENT: begin
					if (byte_counter < 3) begin
						next_state = OUTPUT_BYTE;  // Output the next byte
				  end else if (byte_counter == 3) begin
						next_state = REG_SENT;
					end 
				end
				
				REG_SENT:begin
					next_state = OUTPUT_REG;  // Move back to OUTPUT_REG state
			   end
			  
			  default:
					next_state = IDLE;
		
			  endcase
    end
    
    // Output and internal register control
    always_ff @(posedge clk or posedge rst) begin
        if (rst) begin
            incrementer <= 5'b0;
            byte_counter <= 2'b0;
            dout <= 8'b00000000;
            Ready_Byte <= 1'b0;
        end else begin
            case (current_state)
                IDLE: begin
                    incrementer <= 5'b0;
                    byte_counter <= 2'b0;
                    dout <= 8'b00000000;
                    Ready_Byte <= 1'b0;
                end
                OUTPUT_REG: begin
                    current_reg_value <= registerFile[incrementer];  // Load the 32-bit register value
						  Ready_Byte <= 1'b0;  // Clear the ready signal until output is ready
						  byte_counter <= 2'b0;
                end
                SEND_BYTE: begin
                    Ready_Byte <= 1'b1;  // Signal that 8-bit data is ready
                    case (byte_counter)
                        2'd0: dout <= current_reg_value[31:24];  // Send MSB
                        2'd1: dout <= current_reg_value[23:16];  // Send next byte
                        2'd2: dout <= current_reg_value[15:8];   // Send next byte
                        2'd3: dout <= current_reg_value[7:0];    // Send LSB
                    endcase
//						  byte_counter <= byte_counter + 1;  // Move to the next byte
//                    if (byte_counter == 2'b11) begin
////                        incrementer <= incrementer + 1;  // Increment register index after transmitting 4 bytes
//								//byte_counter <= 2'b00;
//                    end
//						  else begin
//						  byte_counter <= byte_counter + 1;  // Move to the next byte
//						  end
                end
					 BYTE_SENT: begin
						Ready_Byte <= 1'b0;
						byte_counter <= byte_counter + 1;  // Move to the next byte
					 end
					 REG_SENT: begin
						  Ready_Byte <= 1'b0;
                    incrementer <= incrementer + 1;  // Increment register index after transmitting 4 bytes
					 end
            endcase
        end
    end

    
    // Initialize register file with test data
    initial begin
        registerFile[0]  = 32'b00000000000000000000000000000001; // Register 0
        registerFile[1]  = 32'b00000000000000000000000000000011; // Register 1
        registerFile[2]  = 32'b00000000000000000000000000000111; // Register 2
        registerFile[3]  = 32'b00000000000000000000000000001111; // Register 3
        registerFile[4]  = 32'b00000000000000000000000000011111; // Register 4
        registerFile[5]  = 32'b00000000000000000000000000111111; // Register 5
        registerFile[6]  = 32'b00000000000000000000000001111111; // Register 6
        registerFile[7]  = 32'b00000000000000000000000011111111; // Register 7
        registerFile[8]  = 32'b00000000000000000000000111111111; // Register 8
        registerFile[9]  = 32'b00000000000000000000001111111111; // Register 9
        registerFile[10] = 32'b00000000000000000000011111111111; // Register 10
        registerFile[11] = 32'b00000000000000000000111111111111; // Register 11
        registerFile[12] = 32'b00000000000000000001111111111111; // Register 12
        registerFile[13] = 32'b00000000000000000011111111111111; // Register 13
        registerFile[14] = 32'b00000000000000000111111111111111; // Register 14
        registerFile[15] = 32'b00000000000000001111111111111111; // Register 15
        registerFile[16] = 32'b00000000000000011111111111111111; // Register 16
        registerFile[17] = 32'b00000000000000111111111111111111; // Register 17
        registerFile[18] = 32'b00000000000001111111111111111111; // Register 18
        registerFile[19] = 32'b00000000000011111111111111111111; // Register 19
        registerFile[20] = 32'b00000000000111111111111111111111; // Register 20
        registerFile[21] = 32'b00000000001111111111111111111111; // Register 21
        registerFile[22] = 32'b00000000011111111111111111111111; // Register 22
        registerFile[23] = 32'b00000000111111111111111111111111; // Register 23
        registerFile[24] = 32'b00000001111111111111111111111111; // Register 24
        registerFile[25] = 32'b00000011111111111111111111111111; // Register 25
        registerFile[26] = 32'b00000111111111111111111111111111; // Register 26
        registerFile[27] = 32'b00001111111111111111111111111111; // Register 27
        registerFile[28] = 32'b00011111111111111111111111111111; // Register 28
        registerFile[29] = 32'b00111111111111111111111111111111; // Register 29
        registerFile[30] = 32'b01111111111111111111111111111111; // Register 30
        registerFile[31] = 32'b11111111111111111111111111111111; // Register 31
    end
    
endmodule
