from multiprocessing import Pool

def worker(args):
	n1, nums = args
	
	for n2 in filter(lambda e: e!=n1, nums):
		if n1 + n2 == 2020:
			print("{} + {} = 2020 => {}".format(n1, n2, n1*n2))

if __name__ == '__main__':

	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			data = pool.map(int, f.readlines())
		pool.map(worker, [(n, data) for n in data])