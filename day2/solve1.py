from multiprocessing import Pool

def worker(line):
	nums, char, password = line.rstrip().replace(":", "").split()
	n1, n2 = map(int, nums.split("-"))
	
	if n1 <= password.count(char) <= n2:
		return 1
	return 0

if __name__ == '__main__':

	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			result = pool.map(worker, f.readlines())
	print(sum((result)))
