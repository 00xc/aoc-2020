from multiprocessing import Pool

FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
REQUIRED_FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

def worker(passport):
	passport = dict([value.split(":") for value in passport.split()])
	for field in REQUIRED_FIELDS:
		if field not in passport:
			return 0
	return 1


if __name__ == '__main__':

	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			res = pool.map(worker, [p.rstrip() for p in f.read().split("\n\n")])

	print(sum(res))