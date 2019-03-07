registers = ["$zero","$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7", "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$t8", "$t9", "$a0", "$v0", "$a1"]
def put(a, instructions, case):
	List = []
	List = [a, case]
	instructions.insert(0, List)

def pop(instructions, command):
	try:
		while(instructions[-1][1] <= 0):
			instructions.pop()
	except:
		pass
	try:
		while(command[-1][1] <= 0):
			command.pop()
	except:
		pass
def decre(instructions, command):
	for i in range(len(instructions)):
		instructions[i][1] = instructions[i][1] - 1
	for i in range(len(command)):
		command[i][1] -= 1
	pop(instructions, command)

def check(instructions, command, *a):
	for i in range(len(a)):
		for j in range(len(instructions)):
			try:
				while(instructions[j][0] == a[i] and instructions[j][1] > 1):
					print("Stall Cycles")
					print(command)
					decre(instructions, command)
			except:
				pass
read_write = []
write_read = []
write_write = []
first_typ = ["add", "mul"]
third_typ = [ "addi", "muli", "move", "srl", "sll"]
fourth_typ = [ "la", "lb", "lw", "li"]
second_typ = ["sw", "sb"]
fifth_typ = ["beq", "bne", "ble", "blt", "div", "bge", "bgt"]
sixth_typ = ["beqz", "bltz", "bgtz"]
seventh_typ = ["mfhi", "mflo"]
def dependencies(command, code):
	List = []
	for i in range(len(command)):
		List.insert(0, command[i][0])
	List.append(code)
	write = []
	read = []
	for i in range(len(List)):
		try:
			if List[i][0] in sixth_typ:
				write.append([])
				read.append([List[i][1]])
			elif List[i][0] in fifth_typ:
				write.append([])
				read.append([List[i][1], List[i][2]])
			elif List[i][0] in seventh_typ: 
				write.append([List[i][1]])
			elif List[i][0] in fourth_typ:
				write.append([List[i][1]])
				read.append([List[i][2]])
			elif List[i][0] in second_typ:
				write.append([List[i][2]])
				read.append([List[i][1]])
			elif List[i][0] in third_typ:
				write.append([List[i][1]])
				read.append([List[i][2]])
			elif List[i][0] in first_typ:
				write.append([List[i][1]])
				read.append([List[i][2], List[i][3]])	
			else:
				write.append([])
				read.append([])
		except:
			write.append([])
			read.append([])	
		
	#READ_AFTER_WRITE
	i = 0
	while i < len(write):
		j = i + 1
		while j < len(write):
			try:
				if write[i][0] in read[j]:
					read_write.append([List[i], List[j]])
			except:
				pass
			j += 1
		i += 1
	#WRITE_AFTER_READ
	i = 0
	while i < len(write):
		j = i + 1
		while j < len(write):
			k = 0
			while True:
				try:
					if read[i][k] == write[j][0]:
						write_read.append([List[i], List[j]])
						break
				except:
					break
				k += 1
			j += 1
		i += 1
	#WRITE_AFTER_WRITE
	i = 0
	while i < len(write):
		j = i + 1
		while j < len(write):
			try:
				if write[i][0] == write[j][0]:
					write_write.append([List[i], List[j]])
					break
			except:
				pass
			j += 1
		i += 1	
		
def nobypass():
	keywords=["add", "addi", "mul", "muli", "div", "mfhi", "mflo", "beq", "bne", "li", "la", "lb", "sb", "syscall", "lw", "sw", "move"]
	instructions = []
	command = []
	MIPS = open("7","r")
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
			decre(instructions, command)
			dependencies(command, code[i])
			check(instructions, command, code[i][2], code[i][3]) 
			put(code[i][1], instructions, 5)
			command.insert(0, [code[i], 5])
		elif(code[i][0] == "addi" or code[i][0] == "muli" or code[i][0] == "move" or code[i][0] == "srl" or code[i][0] == "sll"):
			decre(instructions, command)
			dependencies(command, code[i])
			check(instructions, command, code[i][2])
			put(code[i][1], instructions, 5)
			command.insert(0, [code[i], 5])
		elif(code[i][0] == "li" or code[i][0] == "la" or code[i][0] == "lb" or code[i][0] == "lw"):
			decre(instructions, command)
			dependencies(command, code[i])
			check(instructions, command, code[i][2])
			put(code[i][1], instructions, 5)
			command.insert(0, [code[i], 5])
		elif(code[i][0] == "sw" or code[i][0] == "sb"):
			decre(instructions, command)
			dependencies(command, code[i])
			check(instructions, command, code[i][1])
			put(code[i][2], instructions, 4)
			command.insert(0, [code[i], 4])
		elif(code[i][0] == "div" or code[i][0] == "beq" or code[i][0] == "bne" or code[i][0] == "bge" or code[i][0] == "bgt" or code[i][0] == "blt" or code[i][0] == "ble"):
			decre(instructions, command)
			dependencies(command, code[i])
			check(instructions, command, code[i][1], code[i][2])
			command.insert(0, [code[i], 2])
		elif(code[i][0] == "mfhi" or code[i][0] == "mflo" or code[i][0] == "j"):
			decre(instructions, command)
			dependencies(command, code[i])
			command.insert(0, [code[i], 2])
		elif(code[i][0] == "beqz" or code[i][0] == "bltz" or code[i][0] == "bgtz"):
			decre(instructions, command)
			dependencies(command, code[i])
			check(instructions, command, code[i][1])
			command.insert(0, [code[i], 2])
		else:
			pass
		print(command)
nobypass()
final_read_write = []
final_write_read = []
final_write_write = []
print("READ-WRITE DEPENDENCIES")
if(len(read_write) > 0):
	for i in read_write:
		if i not in final_read_write:
			print(i)
			final_read_write.append(i)
else:
	print("NONE")
print("WRITE-READ DEPENDENCIES")
if(len(write_read) > 0):
	for i in write_read:
		if i not in final_write_read:
			print(i)
			final_write_read.append(i)
else:
	print("NONE")
print("WRITE-WRITE DEPENDENCIES")
if(len(write_write) > 0):
	for i in write_write:
		if i not in final_write_write:
			print(i)
			final_write_write.append(i)
else:
	print("NONE")	
