class SPIMEmulator:
    def __init__(self):
        # Initialize registers (32 general-purpose registers)
        self.registers = [0] * 32
        self.register_names = ['$zero', '$at', '$v0', '$v1', '$a0', '$a1', '$a2', '$a3',
                  '$t0', '$t1', '$t2', '$t3', '$t4', '$t5', '$t6', '$t7',
                  '$s0', '$s1', '$s2', '$s3', '$s4', '$s5', '$s6', '$s7',
                  '$t8', '$t9', '$k0', '$k1', '$gp', '$sp', '$fp', '$ra']

        # Initialize memory (4 KB)
        self.memory = [0] * 4096

        # Program Counter (PC)
        self.pc = 0

        # Data Memory (limited in size)
        self.data_memory = [0] * 1024

        # Termination flag
        self.is_run = True

    def load_instructions(self, filename):
        # Read instructions from the file and store them in memory
        with open(filename, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                instruction = int(line.strip(), 16)
                self.memory[i] = instruction

    def load_data_memory(self, filename):
        # Read initial data memory state from a file
        with open(filename, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                value = int(line.strip(), 16)
                self.data_memory[i] = value

    def execute_instruction(self, instruction):
        if instruction == 0:
            return  # NOP
        if instruction == 0x0000000C and self.registers[2] == 10:
            self.is_run = False
            return
        opcode = (instruction >> 26) & 0x3F
        rs = (instruction >> 21) & 0x1F
        rt = (instruction >> 16) & 0x1F
        rd = (instruction >> 11) & 0x1F
        shamt = (instruction >> 6) & 0x1F
        funct = instruction & 0x3F
        immediate = instruction & 0xFFFF

        if opcode == 0:  # R-type instruction
            if funct == 32:  # add
                self.registers[rd] = (self.registers[rs] + self.registers[rt]) & 0xFFFFFFFF
            elif funct == 36:  # and
                self.registers[rd] = self.registers[rs] & self.registers[rt]
            elif funct == 39:  # nor
                self.registers[rd] = ~(self.registers[rs] | self.registers[rt]) & 0xFFFFFFFF
            elif funct == 37:  # or
                self.registers[rd] = self.registers[rs] | self.registers[rt]
            elif funct == 42:  # slt
                self.registers[rd] = int(self.registers[rs] < self.registers[rt])
            elif funct == 0:  # sll
                self.registers[rd] = (self.registers[rt] << shamt) & 0xFFFFFFFF
            elif funct == 3:  # sra
                self.registers[rd] = (self.registers[rt] >> shamt) & 0xFFFFFFFF
            elif funct == 2:  # srl
                self.registers[rd] = self.registers[rt] >> shamt
            elif funct == 34:  # sub
                self.registers[rd] = (self.registers[rs] - self.registers[rt]) & 0xFFFFFFFF
                print(str(self.registers[rs]) + ", " + str(self.registers[rt]))

        #I-type instructions
        elif opcode == 8:  # addi
            self.registers[rt] = (self.registers[rs] + immediate) & 0xFFFFFFFF
        elif funct == 10:  # slti
            self.registers[rd] = int(self.registers[rs] < self.registers[rt])
        elif opcode == 12:  # andi
            self.registers[rt] = (self.registers[rs] & immediate)
        elif opcode == 13:  # ori
            self.registers[rt] = (self.registers[rs] | immediate)
        elif opcode == 35:  # lw
                address = (self.registers[rs] + immediate) & 0xFFFFFFFF
                self.registers[rt] = self.data_memory[address]
        elif opcode == 43:  # sw
                address = (self.registers[rs] + immediate) & 0xFFFFFFFF
                self.data_memory[address] = self.registers[rt]

        elif opcode in [4, 5]:  # I-type branch instructions
            offset = immediate << 2
            if opcode == 4:  # beq
                if self.registers[rs] == self.registers[rt]:
                    self.pc += offset
            elif opcode == 5:  # bne
                if self.registers[rs] != self.registers[rt]:
                    self.pc += offset

        elif opcode in [2, 3]:  # J-type instructions
            target = instruction & 0x3FFFFFF
            if opcode == 2:  # j
                self.pc = target
            elif opcode == 3:  # jal
                self.registers[31] = self.pc + 4
                self.pc = target

        else:
            print(f"Unsupported instruction: {hex(instruction)}")

    def run(self):
        while self.is_run and self.pc < len(self.memory):
            # Fetch instruction from memory
            instruction = self.memory[self.pc]

            # Execute the instruction
            self.execute_instruction(instruction)

            # Increment Program Counter
            self.pc += 1

        if self.is_run:
            print("ERROR: Program was never terminated")

    def print_registers(self):
        print("Registers:")
        for i, value in enumerate(self.registers):
            print(f"{self.register_names[i]}: {value}")

    def print_memory(self):
        print("Data Memory:")
        for i, value in enumerate(self.data_memory):
            print(f"Address {hex(i)}: {hex(value)}")


if __name__ == "__main__":
    emulator = SPIMEmulator()

    # Load instructions from a file
    emulator.load_instructions("instructions.txt")

    # Load initial data memory state from a file
    emulator.load_data_memory("data_memory.txt")

    # Run the emulator
    emulator.run()

    # Print the final state of registers and data memory
    #emulator.print_registers()
    #emulator.print_memory()
