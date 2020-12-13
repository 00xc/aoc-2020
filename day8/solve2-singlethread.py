from multiprocessing import Pool

def parser(line):
	line = line.split(" ", 1)
	return (line[0], int(line[1]))

class VM:
	__slots__ = ["pc", "accumulator", "table", "code", "changed", "visited", "changed_instructions"]

	def __init__(self, file):
		self.pc = 0
		self.accumulator = 0
		self.table = { "jmp": self.jmp, "nop": self.nop, "acc": self.acc }

		# Read instructions
		with Pool(4) as pool:
			with open(file, "r") as f:
				self.code = pool.map(parser, f.read().rstrip().split("\n"))

		# Mark this run as having altered no instructions yet
		self.changed = 0

		# Mark all instructions as not changed and not visited
		self.visited = [0] * len(self.code)
		self.changed_instructions = [0] * len(self.code)

	def run(self):

		while 0 <= self.pc < len(self.code):
			instruction = self.code[self.pc]

			# Stop if we entered a loop, otherwise mark this instruction as visited
			if self.visited[self.pc] == 1:
				break
			self.visited[self.pc] = 1

			# If:
			# 1. We have not altered yet a single instruction during this run, and
			# 2. This instruction can be altered (jmp or nop), and
			# 3. We have not tried to alter this instruction ever
			if self.changed == 0 and instruction[0] != "acc" and self.changed_instructions[self.pc] == 0:
				self.changed = self.changed_instructions[self.pc] = 1

				# Alter instruction
				if instruction[0] == "jmp":
					self.table["nop"](instruction[1])
				elif instruction[0] == "nop":
					self.table["jmp"](instruction[1])
				else:
					assert(1 == 0)
			else:
				self.table[instruction[0]](instruction[1])

		# Check if we exited successfuly
		if self.pc == len(self.code):
			return self.accumulator
		return 0

	def restart(self):
		self.pc = self.accumulator = self.changed = 0
		self.visited = [0] * len(self.code)

	def jmp(self, arg):
		self.pc += arg

	def nop(self, arg):
		self.pc += 1

	def acc(self, arg):
		self.accumulator += arg
		self.pc += 1

if __name__ == '__main__':
	
	vm = VM("input.txt")
	
	while True:
		res = vm.run()
		if res != 0: break
		vm.restart()

	print("Done! accumulator={}".format(res))