import sys

f = open(sys.argv[1], 'r') # 파일 읽기

''' stages 함수 선언 '''
### Instruction Fetch ###
def IF(instruction):
	# instruction이 안들어왔거나 flush 해야할때 0 반환
	if (instruction == 0):
		pcw = 0
		iiw = 0
		return pcw, iiw
	
	# instruction이 있는 경우 pc write = 1, IF/ID write = 1
	pcw = 1
	iiw = 1
	return pcw, iiw

### Instruction Decode ###
def ID(instruction):
	# instruction이 들어오지 않았다면 레지스터에 모두 0값으로 할당
	if (instruction == 0):
		rs = 0
		rt = 0
		rd = 0
		return rs, rt, rd

	# instruction이 들어왔다면 instruction을 파싱해서 각 레지스터 값을 반환
	instruction = instruction.strip('\n').split(' ')
	opcode = instruction[0]

	# I-Type load and store parsing
	if opcode == 'LW' or opcode == 'SW':
		rd = instruction[1].strip(',')[1]
		rt, rs = instruction[2].split('(')
		rt = 0
		rs = rs.strip(')')[1]
	
	# I-Type immediate values parsing
	elif opcode == 'ADDI' or opcode == 'ORI':
		rt = instruction[1].strip(',')[1]
		rs = instruction[2].strip(',')[1]
		rd = 0

	# R-Type parsing
	else:
		rd = instruction[1].strip(',')[1]
		rs = instruction[2].strip(',')[1]
		rt = instruction[3][1]

	return rs, rt, rd

# def EX(instruction):
# 	if (instruction == 0):
# 		print(0)
# 		return

# 	instruction = instruction.strip('\n').split(' ')
# 	opcode = instruction[0]
# 	if opcode == 'LW' or opcode == 'SW':
# 		rd = instruction[1].strip(',')
# 		off, add = instruction[2].split('(')
# 		add = add.strip(')')
	
# 	else:
# 		rd = instruction[1].strip(',')
# 		rs = instruction[2].strip(',')
# 		rt = instruction[3]
	
# def MEM(instruction):
# 	if (instruction == 0):
# 		print(0)
# 		return

# 	instruction = instruction.strip('\n').split(' ')
# 	opcode = instruction[0]
# 	if opcode == 'LW' or opcode == 'SW':
# 		rd = instruction[1].strip(',')
# 		off, add = instruction[2].split('(')
# 		add = add.strip(')')
	
# 	else:
# 		rd = instruction[1].strip(',')
# 		rs = instruction[2].strip(',')
# 		rt = instruction[3]
	
# def WB(instruction):
# 	if (instruction == 0):
# 		print(0)
# 		return

# 	instruction = instruction.strip('\n').split(' ')
# 	opcode = instruction[0]
# 	if opcode == 'LW' or opcode == 'SW':
# 		rd = instruction[1].strip(',')
# 		off, add = instruction[2].split('(')
# 		add = add.strip(')')
	
# 	else:
# 		rd = instruction[1].strip(',')
# 		rs = instruction[2].strip(',')
# 		rt = instruction[3]


### 출력 테이블 ###
print('| IF/ID           | ID/EX                                     | EX/MEM       | MEM/WB       | Forward               |                                      |')
### 메인 ###
count = 0
while True:
	instruction = f.readline()
	if not instruction:
		if count == 5:
			break
		count += 1

	### writeback ###
	try:
		if memory == 0:
			writeback = 0
		else:
			writeback = memory
	except:
		writeback = 0
	
	### memory ###
	try:
		if execute == 0:
			memory = 0
		else:
			memory = execute
	except:
		memory = 0
	
	### execute ###
	try:
		if decode == 0:
			execute = 0
		else:
			execute = decode
	except:
		execute = 0
	
	### decode ###
	try:
		if fetch == 0:
			decode = 0
		else:
			decode = fetch
	except:
		decode = 0
	
	### fetch ###
	if instruction == '':
		fetch = 0
	else:
		fetch = instruction

	pcw, iiw = IF(fetch)
	iirs, iirt, iird = ID(decode)
	# iers, iert, ierd, iew, iem, ied = EX(execute)
	iers = 0
	iert = 0
	ierd = 0
	iew = 0 
	iem = 0
	ied = 0
	# emrd, emw = MEM(memory)
	emrd = 0
	emw = 0
	# mwrd, mww = WB(writeback)
	mwrd = 0
	mww = 0
	
	fa = 0
	fb = 0

	print('| $rs | $rt | $rd | $rs | $rt | $rd | $write | memread | $dst | $rd | $write | $rd | $write | Forward A | Forward B | PC write | IF/ID write|')# | ID/EX flush |')
	print('| {:2}  | {:2}  | {:2}  | {:2}  | {:2}  | {:2}  | {:2}     | {:2}      | {:2}   | {:2}  | {:2}     | {:2}  | {:2}     | {:2}        | {:2}        | {:2}       | {:2}          |'\
	.format(iirs, iirt, iird, iers, iert, ierd, iew, iem, ied, emrd, emw, mwrd, mww, fa, fb, pcw, iiw)) #, ief))
	print('|-----|-----|-----|-----|-----|-----|--------|---------|------|-----|--------|-----|--------|-----------|-----------|----------|------------|')




	
f.close()
