import sys


fr = open(sys.argv[1], 'r') # 파일 읽기
fw = open(sys.argv[1] + '.out.txt', 'w') # 결과 파일 쓰기


''' Instruction을 받아오는 함수 선언 '''
### Instruction Fetch ###
def fetch(instruction):
	# instruction이 안들어왔거나 flush 해야할때 0 반환
	if (instruction == 0):
		opcode = 0
		rs = 0
		rt = 0
		rd = 0
		pcw = 0
		iiw = 0
		return opcode, pcw, iiw, rs, rt, rd

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

		return opcode, pcw, iiw, rs, rt, rd


### 출력 테이블 ###
fw.write('|-------------|-----------------|-------------------------------------------|--------------|--------------|-----------------------|-----------------------|\n')
fw.write('| Cycle #     | IF/ID           | ID/EX                                     | EX/MEM       | MEM/WB       | Forward               |                                      |\n')
fw.write('|-------------|-----------------|-------------------------------------------|--------------|--------------|-----------------------|-----------------------|\n')


''' 메인 프로세서 '''
count = 0
cycle = 0

while True:
	instruction = fr.readline()
	if not instruction:
		if count == 5:
			break
		count += 1


	### Writeback ###
	try:
		if emopc == 0:
			mwrd = 0
			mww  = 0
		else:
			mwrd = emrd
			mww = emw
	
	except:
		mwrd = 0
		mww = 0
	
	### Memory ###
	try:
		if ieopc == 0:
			emopc = 0
			emrd = 0
			emw = 0
		else: # ID/EX stage에서 넘겨 받은 destination register를 rd register로 넘겨줌
			emopc = ieopc
			if ied == 1: # ied 1인 경우 R-type
				emrd = ierd
			elif ied == 0: # ied 가 0인 경우 I-type
				emrd = iert

			emw = iew # ID/EX stage에서 넘겨 받은 regWrite

	except:
		emopc = 0
		emrd = 0
		emw = 0
	
	### Execution ###
	try:
		if iiopc == 0: # 오퍼레이션 코드가 없으면 버블이다
			ieopc = 0
			iers = 0
			iert = 0
			ierd = 0
			iew = 0
			iem = 0
			ied = 0
			fa = '00'
			fb = '00'
		else:
			ieopc = iiopc
			iers = iirs
			iert = iirt
			ierd = iird
			iew = 1

			# forwarding determination
			# 더블 데이터 해저드 발생 시 EX hazard로 덮어씌울 수 있도록 MEM 해저드 먼저 연산
			# fa, fb 값 초기화
			fa = '00'
			fb = '00' 

			# MEM hazard
			if (mww == 1 and mwrd != 0) and mwrd == iers:
				fa = '01'
			elif (mww == 1 and mwrd != 0) and mwrd == iert:
				fb = '10'

			# EX hazard
			if emw == 1 and emrd != 0 and emrd == iers:
				fa = '10'
			elif emw == 1 and emrd != 0 and emrd == iert:
				fb = '10'
			
			# lw instruction 이라면 메모리를 사용하는 것이기 때문에 memread == 1
			if ieopc == 'LW':
				iem = 1
			else:
				iem = 0

			# Instruction Type 에 따라 dst register  판단해서 dst register 값 넘겨주기
			if ieopc == 0: # 넘겨 받는 레지스터 값이 하나도 없을 경우 버블이다
				ied = 0
			elif ieopc == 'ADD' or ieopc == 'OR': # R-Type 일경우 (destination register는 rd)
				ied = 1
			else: # I-Type 일경우 (destination register는 rt)
				ied = 0

	except:
		ieopc = 0
		iers = 0
		iert = 0
		ierd = 0
		iew = 0
		iem = 0
		ied = 0
		fa = '00'
		fb = '00'
	
	### Instruction Decode ###
	try:
		if pcw == 1 and iiw == 1:
			iiopc = opc
			iirs = rs
			iirt = rt
			iird = rd
		else: # 버블 시
			iiopc = 0
			iirs = 0
			iirt = 0
			iird = 0
	except:
		iiopc = 0
		iirs = 0
		iirt = 0
		iird = 0
	
	### Instruction Fetch ###
	if not instruction:
		instruction = 0

	opc, pcw, iiw, rs, rt, rd = fetch(instruction)

	# wb 예외처리 필요함!!
	
	cycle += 1 # 사이클 수 1 증가 

	
	### 테이블 출력 ###
	fw.write('|             | $rs | $rt | $rd | $rs | $rt | $rd | $write | memread | $dst | $rd | $write | $rd | $write | Forward A | Forward B | PC write | IF/ID write|\n')
	fw.write('| Cycle {:>3}   | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}     | {:>2}      | {:>2}   | {:>2}  | {:>2}     | {:>2}  | {:>2}     | {:>2}        | {:>2}        | {:>2}       | {:>2}          |\n'\
	.format(cycle, iirs, iirt, iird, iers, iert, ierd, iew, iem, ied, emrd, emw, mwrd, mww, fa, fb, pcw, iiw))
	fw.write('|-------------|-----|-----|-----|-----|-----|-----|--------|---------|------|-----|--------|-----|--------|-----------|-----------|----------|------------|\n')
	

### 파일 읽기 쓰기 종료 ###
fr.close()
fw.close()