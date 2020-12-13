from multiprocessing.dummy import Pool as DummyPool

def string_filter(st, blacklist):
	for b in blacklist:
		st = st.replace(b, "")
	return st

def parser(line):
	container, contained = string_filter(line, (" bags", " bag", ".", "no other")).split(" contain ")
	out[container] = [tuple(element.split(" ", 1)) for element in contained.split(", ") if element]

def find_bags(out, k):
	total = 0

	for contained in out[k]:
		total += int(contained[0]) + int(contained[0]) * find_bags(out, contained[1])

	return total

if __name__ == '__main__':
	
	out = {}

	with DummyPool(4) as pool:
		with open("input.txt", "r") as f:
			pool.map(parser, f.read().rstrip().split("\n"))

	start = "shiny gold"
	print(find_bags(out, start))