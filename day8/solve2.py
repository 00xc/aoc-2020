from multiprocessing import Pool

def parser(line):
	line = line.split(" ", 1)
	return (line[0], int(line[1]))

def worker(vm, i):
	return vm.run(i)

class VM:
	def __init__(self, code):
		self.code = code
		self.pc = 0
		self.accumulator = 0
		self.table = { "jmp": self.jmp, "nop": self.nop, "acc": self.acc }
		self.visited = [0] * len(self.code)

	def run(self, altered):

		while 0 <= self.pc < len(self.code):

			# Stop if we are in a loop
			if self.visited[self.pc] == 1:
				break
			self.visited[self.pc] = 1

			instruction = self.code[self.pc]
			if self.pc == altered:
				if instruction[0] == "jmp": self.table["nop"](instruction[1])
				elif instruction[0] == "nop": self.table["jmp"](instruction[1])
				else: assert(1 == 0)
			else:
				self.table[instruction[0]](instruction[1])
			
		# Return accumulator if execution was successful
		if self.pc == len(self.code):
			return self.accumulator

	def jmp(self, arg):
		self.pc += arg

	def nop(self, arg):
		self.pc += 1

	def acc(self, arg):
		self.accumulator += arg
		self.pc += 1

if __name__ == '__main__':

	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			code = pool.map(parser, f.read().rstrip().split("\n"))

		# Launch a VM for each possible altered instruction (jmp or nop)
		args = [(VM(code), i) for i, ins in enumerate(code) if ins[0] != "acc"]
		res = list(filter(None, pool.starmap(worker, args)))[0]

	print(res)
