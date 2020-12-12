from multiprocessing import Pool

def worker(group):
	return len(set.intersection(*[set(a) for a in group.split("\n")]))

if __name__ == '__main__':
	
	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			ret = pool.map(worker, f.read().rstrip().split("\n\n"))
	print(sum(ret))