registers = ["$zero","$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7", "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$t8", "$t9", "$a0", "$v0", "$a1"]
def put(a, instructions, case):
	List = []
	List = [a, case]
	instructions.insert(0, List)

def pop(instructions):
	try:
		while(instructions[-1][1] == 0):
			instructions.pop()
	except:
		pass
def decre(instructions):
	for i in range(len(instructions)):
		instructions[i][1] = instructions[i][1] - 1
	pop(instructions)

def check(instructions, *a):
	for i in range(len(a)):
		for j in range(len(instructions)):
			try:
				while(instructions[j][0] == a[i] and instructions[j][1] > 1):
					print("Stall Cycles")
					print(instructions)
					decre(instructions)
			except:
				pass
			
def main():
	keywords=["add", "addi", "mul", "muli", "div", "mfhi", "mflo", "beq", "bne", "li", "la", "lb", "sb", "syscall", "lw", "sw", "move"]
	instructions = []
	command = []
	MIPS = open("10","r")
	code = MIPS.read()
	code = code.replace("\t","")
	code = code.split("\n")
	try:
		while 1:
			code.remove("")
	except:
		pass
	program_run = 0
	cycles = 0
	for i in range(len(code)):
		code[i] = code[i].split(" ")
		for j in range(len(code[i])):
			code[i][j] = code[i][j].split(",")
			try:
				code[i][j].remove("")
			except:
				pass
			code[i][j] = "".join(code[i][j])
	for i in range(len(code)):
		if(code[i][0] == "add" or code[i][0] == "mul"):
			decre(instructions)
			check(instructions, code[i][2], code[i][3]) 
			put(code[i][1], instructions, 5)
		elif(code[i][0] == "addi" or code[i][0] == "muli" or code[i][0] == "move" or code[i][0] == "srl" or code[i][0] == "sll"):
			decre(instructions)
			check(instructions, code[i][2])
			put(code[i][1], instructions, 5)
		elif(code[i][0] == "li" or code[i][0] == "la" or code[i][0] == "lb" or code[i][0] == "lw"):
			decre(instructions)
			check(instructions, code[i][2])
			put(code[i][1], instructions, 5)
		elif(code[i][0] == "sw" or code[i][0] == "sb"):
			decre(instructions)
			check(instructions, code[i][1])
			put(code[i][2], instructions, 4)
		elif(code[i][0] == "div" or code[i][0] == "beq" or code[i][0] == "bne" or code[i][0] == "bge" or code[i][0] == "bgt" or code[i][0] == "blt" or code[i][0] == "ble"):
			decre(instructions)
			check(instructions, code[i][1], code[i][2])
		elif(code[i][0] == "mfhi" or code[i][0] == "mflo" or code[i][0] == "j"):
			decre(instructions)
		elif(code[i][0] == "beqz" or code[i][0] == "bltz" or code[i][0] == "bgtz"):
			decre(instructions)
			check(instructions, code[i][1])
		else:
			pass
		print(instructions)
main()
