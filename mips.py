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
	if not instruction: # 더 이상 읽을 instruction이 없을 경우
		if count == 5:	# 현재 들어온 싸이클을 모두 읽고
			break # 종료
		count += 1


	### Writeback ###
	try:
		if emopc == 0:
			mwrd = 0
			mww  = 0
		else:
			mwrd = emrd
			mww = emw
	
	# 첫 싸이클 때 입력 값이 없어서 생기는 오류 처리
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

	# 첫 싸이클 때 입력 값이 없어서 생기는 오류 처리
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

			# Forwarding
			# fa, fb 값 초기화
			fa = '00'
			fb = '00' 

			# EX hazard
			if emw == 1 and emrd != 0 and emrd == iers:
				fa = '10'
			elif emw == 1 and emrd != 0 and emrd == iert:
				fb = '10'

			# MEM hazard (not 의 뒷부분은 더블 데이터 해저드를 방지 하기 위한 조건 검사)
			if mww == 1 and mwrd != 0 and mwrd == iers and not (emw == 1 and emrd != 0 and emrd == iers):
				fa = '01'
			elif mww == 1 and mwrd != 0 and mwrd == iert and not (emw == 1 and emrd != 0 and emrd == iert):
				fb = '01'

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

	# 첫 싸이클 때 입력 값이 없어서 생기는 오류 처리
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

			# load-use data hazed determination
			if iem == 1 and (iert == iirs or iert == iirt):
				# pc write와 IF/ID Write 0 으로 설정
				pcw = 0
				iiw = 0
				# 다음 stage로 값이 넘어가지 않도록 iiopc == 0으로 변경
				iiopc = 0

		else: # instruction이 더이상 없을 시
			iiopc = 0
			iirs = 0
			iirt = 0
			iird = 0

	# 첫 싸이클 때 입력 값이 없어서 생기는 오류 처리
	except:
		iiopc = 0
		iirs = 0
		iirt = 0
		iird = 0
	
	### Instruction Fetch ###
	if not instruction:
		instruction = 0

	try:
		if (pcw == 1 and iiw == 1): # pipeline bubble이 발생하지 않을 경우
			opc, pcw, iiw, rs, rt, rd = fetch(instruction)
		
		else:	# pipeline이 발생했을 경우 새로운 Instruction을 불러오지 않고 한번 더 같은 instruction으로 진행 
			# pc write 와 IF/ID write 를 == 1로 재설정
			pcw = 1
			iiw = 1
	except:
		opc, pcw, iiw, rs, rt, rd = fetch(instruction)
	
	cycle += 1 # 사이클 수 1 증가 

	
	### 테이블 출력 ###
	fw.write('|             | $rs | $rt | $rd | $rs | $rt | $rd | $write | memread | $dst | $rd | $write | $rd | $write | Forward A | Forward B | PC write | IF/ID write|\n')
	fw.write('| Cycle {:>3}   | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}  | {:>2}     | {:>2}      | {:>2}   | {:>2}  | {:>2}     | {:>2}  | {:>2}     | {:>2}        | {:>2}        | {:>2}       | {:>2}          |\n'\
	.format(cycle, iirs, iirt, iird, iers, iert, ierd, iew, iem, ied, emrd, emw, mwrd, mww, fa, fb, pcw, iiw))
	fw.write('|-------------|-----|-----|-----|-----|-----|-----|--------|---------|------|-----|--------|-----|--------|-----------|-----------|----------|------------|\n')
	

### 파일 읽기 쓰기 종료 ###
fr.close()
fw.close()