from collections import defaultdict
from multiprocessing.dummy import Pool as DummyPool

def string_filter(st, blacklist):
	for b in blacklist:
		st = st.replace(b, "")
	return st

def parser(line):
	container, contained = string_filter(line, (" bags", " bag", ".", "no other")).split(" contain ")
	for cnt in filter(lambda e: e[2:], contained.split(", ")):
		out[cnt[2:]].append(container)

def find_bags(out, k, total=set()):
	if k not in out:
		return ""

	for container in out[k]:
		total.add(container)
		total.update(find_bags(out, container, total))

	return total

if __name__ == '__main__':
	
	out = defaultdict(list)

	with DummyPool(4) as pool:
		with open("input.txt", "r") as f:
			pool.map(parser, f.read().rstrip().split("\n"))


	start = "shiny gold"
	print(len(find_bags(out, start)))