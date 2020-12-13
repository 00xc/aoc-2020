from multiprocessing import Pool

def parser(line):
	line = line.split(" ", 1)
	return (line[0], int(line[1]))

class VM:
	def __init__(self, file):
		self.accumulator = 0
		self.pc = 0
		self.table = { "jmp": self.jmp, "nop": self.nop, "acc": self.acc }

		# Read
		with Pool(4) as pool:
			with open(file, "r") as f:
				self.code = pool.map(parser, f.read().rstrip().split("\n"))

		self.visited = [0 for _ in range(len(self.code))]

	def run(self):
		while 0 <= self.pc < len(self.code):
			instruction = self.code[self.pc]

			if self.visited[self.pc] == 0:
				# Mark instruction as visited and run it
				self.visited[self.pc] = 1
				self.table[instruction[0]](instruction[1])

			else:
				break

		return self.pc, self.accumulator

	def jmp(self, arg):
		self.pc += arg

	def nop(self, arg):
		self.pc += 1

	def acc(self, arg):
		self.accumulator += arg
		self.pc += 1

if __name__ == '__main__':
	
	vm = VM("input.txt")
	vm.run()
	print("Exited @ {} with accumulator={}".format(vm.pc, vm.accumulator))