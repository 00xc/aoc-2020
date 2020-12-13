from collections import Counter
from multiprocessing import Pool

def worker(index, data):
	return data[index+1] - data[index]

if __name__ == '__main__':

	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			data = [0] + sorted(pool.map(int, f.readlines()))
		res = pool.starmap(worker, [(i, data) for i in range(len(data)-1)]) + [3]

		counts = Counter(res)
		print(counts[1] * counts[3])
