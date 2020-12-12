from multiprocessing import Pool

def worker(args):
	n, line = args
	if line[(3*n) % len(line)] == "#":
		return 1
	return 0

if __name__ == '__main__':

	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			res = pool.map(worker, [(i, line.rstrip()) for (i, line) in enumerate(f.readlines())])

	print(sum(res))

