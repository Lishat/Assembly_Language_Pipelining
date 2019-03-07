registers = ["$zero","$s0", "$s1", "$s2", "$s3", "$s4", "$s5", "$s6", "$s7", "$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7", "$t8", "$t9", "$a0", "$v0", "$a1"]

def complete(code):
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
	write = []
	read = []
	for i in range(len(code)):
		try:
			if code[i][0] in sixth_typ:
				write.append([])
				read.append([code[i][1]])
			elif code[i][0] in fifth_typ:
				write.append([])
				read.append([code[i][1], code[i][2]])
			elif code[i][0] in seventh_typ: 
				write.append([code[i][1]])
				read.append([])
			elif code[i][0] in fourth_typ:
				write.append([code[i][1]])
				read.append([code[i][2]])
			elif code[i][0] in second_typ:
				write.append([code[i][2]])
				read.append([code[i][1]])
			elif code[i][0] in third_typ:
				write.append([code[i][1]])
				read.append([code[i][2]])
			elif code[i][0] in first_typ:
				write.append([code[i][1]])
				read.append([code[i][2], code[i][3]])	
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
					read_write.append([code[i], code[j]])
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
						write_read.append([code[i], code[j]])
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
					write_write.append([code[i], code[j]])
					break
			except:
				pass
			j += 1
		i += 1
	print("READ-WRITE DEPENDENCIES")
	[print(i) for i in read_write]
	print("WRITE-READ DEPENDENCIES")
	[print(i) for i in write_read]
	print("WRITE-WRITE DEPENDENCIES")
	[print(i) for i in write_write]
	
def whole():
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
	complete(code)
whole()
