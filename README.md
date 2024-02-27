# spimulator
This code is a spim emulator written in Python. The code runs a good number of functions from the original mips assembly instruction set. 
<be />
Here is the link to a video of it running:    https://youtu.be/j1NALZKaHAs
<br />
The instructions are taken in as a .txt file in which there are lines of hex instructions. The data_memory file is where the actual memory of the emulator is stored and read from. There is an instructions_translated.txt file in which the instructions I used for some testing are included and translated from hex to mips assembly.
<br />
Here is a list of instructions that the spimulator runs right now:
def execute_instruction(self, instruction):
add<br />
and<br />
nor<br />
or<br />
slt<br />
sll<br />
sra<br />
srl<br />
sub<br />
addi<br />
slti<br />
andi<br />
ori<br />
lw<br />
sw<br />
beq<br />
bne<br />
j<br />
jal
