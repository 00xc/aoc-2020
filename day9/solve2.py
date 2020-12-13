from multiprocessing import Pool

PREAMBLE_SIZE = 25

def worker(data):
	target = data.pop(-1)

	for candidate in data:
		for num in filter(lambda e: e!=candidate, data):
			if candidate + num == target:
				return False
	return target

def worker2(index, data, target):
	sm = 0
	sequence = []

	for num in data[index:]:
		sequence.append(num)
		sm += num

		if sm > target:
			return None
		elif sm == target:
			return sequence

if __name__ == '__main__':
	
	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			data = list(map(int, f.readlines()))

		# Each call to worker sends a chunk of size PREAMBLE_SIZE + 1 (a number plus all the candidates to try to sum)
		wrong_num = list(filter(None, pool.map(worker,
			[data[i-PREAMBLE_SIZE:i+1] for i in range(PREAMBLE_SIZE, len(data))])))[0]
		print("Wrong number: {}".format(wrong_num))

		# Obtain sequence of numbers that add to the wrong number
		data = data[:data.index(wrong_num)]
		ret = list(filter(None, pool.starmap(worker2, [(i, data, wrong_num) for i in range(len(data))])))[0]

		print("Sequence: {}".format(" ".join(map(str, ret))))
		print("min(sequence) + max(sequence) = {}".format(min(ret) + max(ret)))




	