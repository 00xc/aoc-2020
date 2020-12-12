from multiprocessing import Pool

def check_hgt(hgt):
	if hgt[-2:] == "cm" and 150 <= int(hgt[:-2]) <= 193: return True		
	elif hgt[-2:] == "in" and 59 <= int(hgt[:-2]) <= 76: return True
	return False

FIELDS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
REQUIRED_FIELDS = {
	"byr": lambda e: e.isnumeric() and 1920 <= int(e) <= 2002,
	"iyr": lambda e: e.isnumeric() and 2010 <= int(e) <= 2020,
	"eyr": lambda e: e.isnumeric() and 2020 <= int(e) <= 2030,
	"hgt": lambda e: e[:-2].isnumeric() and check_hgt(e),
	"hcl": lambda e: len(e) == 7 and e[0] == "#" and all(c in ("0123456789abcdef") for c in e[1:]),
	"ecl": lambda e: e in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
	"pid": lambda e: len(e) == 9 and e.isnumeric(),
}

def worker(passport):
	passport = dict([value.split(":") for value in passport.split()])
	for field, requirement in REQUIRED_FIELDS.items():
		if field not in passport or not requirement(passport[field]):
			return 0
	return 1


if __name__ == '__main__':

	with Pool(4) as pool:
		with open("input.txt", "r") as f:
			res = pool.map(worker, [p.rstrip() for p in f.read().split("\n\n")])

	print(sum(res))