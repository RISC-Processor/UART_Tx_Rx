import re

# Register name to number mapping
REGISTER_MAP = {f'x{i}': i for i in range(32)}

# Opcode map for different instructions
OPCODES = {
    'lui': 0b0110111, 'auipc': 0b0010111, 'jal': 0b1101111, 'jalr': 0b1100111,
    'beq': 0b1100011, 'bne': 0b1100011, 'blt': 0b1100011, 'bge': 0b1100011,
    'bltu': 0b1100011, 'bgeu': 0b1100011, 'lw': 0b0000011, 'sw': 0b0100011,
    'addi': 0b0010011, 'andi': 0b0010011, 'ori': 0b0010011, 'xori': 0b0010011,
    'slti': 0b0010011, 'sltiu': 0b0010011, 'slli': 0b0010011, 'srli': 0b0010011,
    'srai': 0b0010011, 'add': 0b0110011, 'sub': 0b0110011, 'and': 0b0110011,
    'or': 0b0110011, 'xor': 0b0110011, 'sll': 0b0110011, 'srl': 0b0110011,
    'sra': 0b0110011, 'slt': 0b0110011, 'sltu': 0b0110011
}

# Funct3 map for instructions
FUNCT3 = {
    'add': 0b000, 'sub': 0b000, 'and': 0b111, 'or': 0b110, 'xor': 0b100,
    'sll': 0b001, 'srl': 0b101, 'sra': 0b101, 'slt': 0b010, 'sltu': 0b011,
    'addi': 0b000, 'andi': 0b111, 'ori': 0b110, 'xori': 0b100,
    'slti': 0b010, 'sltiu': 0b011, 'slli': 0b001, 'srli': 0b101, 'srai': 0b101,
    'beq': 0b000, 'bne': 0b001, 'blt': 0b100, 'bge': 0b101, 'bltu': 0b110,
    'bgeu': 0b111, 'lw': 0b010, 'sw': 0b010
}

# Funct7 map for R-type instructions
FUNCT7 = {'add': 0b0000000, 'sub': 0b0100000, 'sra': 0b0100000}

# Helper function to clean register names
def clean_register(reg):
    """Remove any trailing commas or whitespace from register names."""
    return reg.strip().replace(',', '')

# R-Type encoding
def encode_r_type(instr, rd, rs1, rs2):
    opcode = OPCODES[instr]
    funct3 = FUNCT3[instr]
    funct7 = FUNCT7.get(instr, 0)
    encoding = (
        (funct7 << 25) | (REGISTER_MAP[clean_register(rs2)] << 20) |
        (REGISTER_MAP[clean_register(rs1)] << 15) | (funct3 << 12) |
        (REGISTER_MAP[clean_register(rd)] << 7) | opcode
    )
    return encoding

# I-Type encoding
def encode_i_type(instr, rd, rs1, imm):
    opcode = OPCODES[instr]
    funct3 = FUNCT3[instr]
    imm = int(imm) & 0xFFF
    encoding = (
        (imm << 20) | (REGISTER_MAP[clean_register(rs1)] << 15) |
        (funct3 << 12) | (REGISTER_MAP[clean_register(rd)] << 7) | opcode
    )
    return encoding

# S-Type encoding
def encode_s_type(instr, rs1, rs2, imm):
    opcode = OPCODES[instr]
    funct3 = FUNCT3[instr]
    imm = int(imm) & 0xFFF
    encoding = (
        ((imm >> 5) << 25) | (REGISTER_MAP[clean_register(rs2)] << 20) |
        (REGISTER_MAP[clean_register(rs1)] << 15) | (funct3 << 12) |
        ((imm & 0x1F) << 7) | opcode
    )
    return encoding

# B-Type encoding
def encode_b_type(instr, rs1, rs2, imm):
    opcode = OPCODES[instr]
    funct3 = FUNCT3[instr]
    imm = int(imm) & 0xFFF
    encoding = (
        ((imm >> 12) << 31) | (((imm >> 5) & 0x3F) << 25) |
        (REGISTER_MAP[clean_register(rs2)] << 20) |
        (REGISTER_MAP[clean_register(rs1)] << 15) | (funct3 << 12) |
        (((imm >> 1) & 0xF) << 8) | ((imm & 0x1) << 7) | opcode
    )
    return encoding

# U-Type encoding
def encode_u_type(instr, rd, imm):
    opcode = OPCODES[instr]
    imm = int(imm) & 0xFFFFF
    encoding = (imm << 12) | (REGISTER_MAP[clean_register(rd)] << 7) | opcode
    return encoding

# J-Type encoding
def encode_j_type(instr, rd, imm):
    opcode = OPCODES[instr]
    imm = int(imm) & 0xFFFFF
    encoding = (
        ((imm >> 20) << 31) | (((imm >> 1) & 0x3FF) << 21) |
        (((imm >> 11) & 0x1) << 20) | (((imm >> 12) & 0xFF) << 12) |
        (REGISTER_MAP[clean_register(rd)] << 7) | opcode
    )
    return encoding

# Parse instruction and encode
def parse_instruction(line):
    parts = line.split()
    instr = parts[0]
    if instr in OPCODES:
        if instr in FUNCT7:  # R-type
            rd, rs1, rs2 = parts[1], parts[2], parts[3]
            return encode_r_type(instr, rd, rs1, rs2)
        elif instr in FUNCT3 and instr not in ['lw', 'sw', 'jalr']:
            rd, rs1, imm = parts[1], parts[2], parts[3]
            return encode_i_type(instr, rd, rs1, imm)
        elif instr in ['lw', 'sw']:
            rd, offset_rs1 = parts[1], parts[2]
            offset, rs1 = re.match(r'(\d+)\((x\d+)\)', offset_rs1).groups()
            if instr == 'lw':
                return encode_i_type(instr, rd, rs1, offset)
            else:
                return encode_s_type(instr, rs1, rd, offset)
        elif instr in ['beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu']:
            rs1, rs2, imm = parts[1], parts[2], parts[3]
            return encode_b_type(instr, rs1, rs2, imm)
        elif instr == 'jal':
            rd, imm = parts[1], parts[2]
            return encode_j_type(instr, rd, imm)
        elif instr in ['lui', 'auipc']:
            rd, imm = parts[1], parts[2]
            return encode_u_type(instr, rd, imm)
    return None

# Main function to read and encode instructions
def main():
    input_file = 'assembly_instructions.txt'
    output_file = 'riscv_instructions.txt'

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue
            encoding = parse_instruction(line)
            if encoding is not None:
                outfile.write(f'{encoding:032b}\n')

if __name__ == '__main__':
    main()
