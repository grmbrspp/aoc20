import time
import copy 

begin = time.time()

###

seat_map = {
	"floor": set(),
	"empty": set(),
	"occupied": set(),
	"history": [0]
}

neighbourhood = {(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)}


def getAdjacents(point: tuple, floor: set, part2: bool) -> set:
	if not part2:
		return {(point[0]+x, point[1]+y) for x,y in neighbourhood}

	res = set()
	for x, y in neighbourhood:
		neighbour = (point[0]+x, point[1]+y)
		while neighbour in floor:
			neighbour = (neighbour[0]+x, neighbour[1]+y)
		res.add(neighbour)

	return res


def getNextState(d: dict, part2: bool) -> dict:
	empty, occupied = set(), set()
	for seat in d["empty"]:
		for a in getAdjacents(seat, d["floor"], part2):
			if a in d["occupied"]:
				empty.add(seat)
				break
		else:
			occupied.add(seat)

	occ_threshold = 5 if part2 else 4
	for seat in d["occupied"]:
		occ_adjacents = [a for a in getAdjacents(seat, d["floor"], part2) if a in d["occupied"]]
		if len(occ_adjacents)  < occ_threshold:
			occupied.add(seat)
		else:
			empty.add(seat)

	return {
		"floor": d["floor"],
		"empty": empty,
		"occupied": occupied,
		"history": d["history"] + [len(occupied)]
	}


def hasStabilised(system: list) -> bool:
	if len(system) < 5:
		return False

	if len(set(system[-5:])) > 1:
		return False

	return True


with open("input.txt") as input_file:
	for y, line in enumerate(input_file):
		for x, char in enumerate(line):
			pos = (x,y)
			if char == ".":
				seat_map["floor"].add(pos)
			if char == "L":
				seat_map["empty"].add(pos)

#clone = copy.deepcopy(seat_map)
p1 = seat_map
while not hasStabilised(p1["history"]):
	p1 = getNextState(p1, part2=False)

p2 = seat_map
while not hasStabilised(p2["history"]):
	p2 = getNextState(p2, part2=True)

print(f"Part 1: {p1['history'][-1]}")
print(f"Part 2: {p2['history'][-1]}")
#print(len(clone['history']))
###

end = time.time()
print(f"Runtime: {end - begin}")