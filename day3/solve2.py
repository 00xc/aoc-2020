from multiprocessing import Pool

def worker(line_num, line, slope):
	right, down = slope

	# We don't land on this line
	if line_num % down != 0:
		return 0

	if line[ ((right*line_num) // down) % len(line) ] == "#":
		return 1
	return 0

if __name__ == '__main__':

	# (right_moves, down_moves)
	slopes = [ (1,1), (3,1), (5,1), (7,1), (1,2), ]

	results = []

	with Pool(4) as pool:
		for slope in slopes:
			with open("input.txt", "r") as f:
				res = pool.starmap(worker,
					[ (i, line.rstrip(), slope) for (i, line) in enumerate(f.readlines())])

			results.append(sum(res))

	out = 1
	for res in results:
		out *= res
	print(out)
