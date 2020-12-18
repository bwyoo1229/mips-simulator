import sys

fr = open(sys.argv[1], 'r') # 파일 읽기
fw = open(sys.argv[1] + '.out.txt', 'w')

''' stages 함수 선언 '''
### Instruction Fetch ###
def fetch(instruction):
	# instruction이 안들어왔거나 flush 해야할때 0 반환
	if (instruction == 0):
		pcw = 0
		iiw = 0
		rs = 0
		rt = 0
		rd = 0
		return pcw, iiw, rs, rt, rd

	else:
		# instruction이 들어왔다면 instruction을 파싱해서 각 레지스터 값을 반환
		instruction = instruction.strip('\n').split(' ')
		opcode = instruction[0]

		# I-Type load and store parsing
		if opcode == 'LW' or opcode == 'SW':
			rt = instruction[1].strip(',')[1]
			rd, rs = instruction[2].split('(')
			rd = 0
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

		pcw = 1
		iiw = 1

	return pcw, iiw, rs, rt, rd

### 출력 테이블 ###
print('|-------------|-----------------|-------------------------------------------|--------------|--------------|-----------------------|-----------------------|')
print('| Cycle #     | IF/ID           | ID/EX                                     | EX/MEM       | MEM/WB       | Forward               |                                      |')
print('|-------------|-----------------|-------------------------------------------|--------------|--------------|-----------------------|-----------------------|')

fw.write('|-------------|-----------------|-------------------------------------------|--------------|--------------|-----------------------|-----------------------|\n')
fw.write('| Cycle #     | IF/ID           | ID/EX                                     | EX/MEM       | MEM/WB       | Forward               |                                      |\n')
fw.write('|-------------|-----------------|-------------------------------------------|--------------|--------------|-----------------------|-----------------------|\n')

### 메인 ###
count = 0
cycle = 0
while True:
	instruction = fr.readline()
	if not instruction:
		if count == 5:
			break
		count += 1

	# ### Writeback ###
	# try:
	# 	if memory == 0:
	# 		writeback = 0
	# 	else:
	# 		writeback = memory
	# except:
	# 	writeback = 0
	
	# ### Memory ###
	# try:
	# 	if execute == 0:
	# 		memory = 0
	# 	else:
	# 		memory = execute
	# except:
	# 	memory = 0
	
	### Execution ###
	try:
		if iirs == 0 and iirt == 0 and iird  == 0: # 전부 0인 경우 버블이다
			iers = 0
			iert = 0
			ierd = 0
		else:
			iers = iirs
			iert = iirt
			ierd = iird
	except:
		iers = 0
		iert = 0
		ierd = 0
	
	### Instruction Decode ###
	try:
		if pcw == 1 and iiw == 1:
			iirs = rs
			iirt = rt
			iird = rd
		else:
			iirs = 0
			iirt = 0
			iird = 0
	except:
		iirs = 0
		iirt = 0
		iird = 0
	
	### Instruction Fetch ###
	if not instruction:
		instruction = 0

	pcw, iiw, rs, rt, rd = fetch(instruction)

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
	
	cycle += 1 # 사이클 수 1 증가 

	### 테이블 출력 ###
	print('|             | $rs | $rt | $rd | $rs | $rt | $rd | $write | memread | $dst | $rd | $write | $rd | $write | Forward A | Forward B | PC write | IF/ID write|')# | ID/EX flush |')
	print('| Cycle {:>3}   | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}     | {:>2}      | {:>2}   | {:>2}  | {:>2}     | {:>2}  | {:>2}     | {:>2}        | {:>2}        | {:>2}       | {:>2}          |'\
	.format(cycle, iirs, iirt, iird, iers, iert, ierd, iew, iem, ied, emrd, emw, mwrd, mww, fa, fb, pcw, iiw)) #, ief))
	print('|-------------|-----|-----|-----|-----|-----|-----|--------|---------|------|-----|--------|-----|--------|-----------|-----------|----------|------------|')
	
	fw.write('|             | $rs | $rt | $rd | $rs | $rt | $rd | $write | memread | $dst | $rd | $write | $rd | $write | Forward A | Forward B | PC write | IF/ID write|\n')
	fw.write('| Cycle {:>3}   | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}     | {:>2}      | {:>2}   | {:>2}  | {:>2}     | {:>2}  | {:>2}     | {:>2}        | {:>2}        | {:>2}       | {:>2}          |\n'\
	.format(cycle, iirs, iirt, iird, iers, iert, ierd, iew, iem, ied, emrd, emw, mwrd, mww, fa, fb, pcw, iiw))
	fw.write('|-------------|-----|-----|-----|-----|-----|-----|--------|---------|------|-----|--------|-----|--------|-----------|-----------|----------|------------|\n')
	


### 파일 읽기 쓰기 종료 ###
fr.close()
fw.close()