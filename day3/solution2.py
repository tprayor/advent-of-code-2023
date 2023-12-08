import re
from pprint import pprint


data = open("./input.txt", "r")
schematic_list = data.readlines()
symbol_search = re.compile(r"[#$%&*+\-/=@]")
part_number_search = re.compile(r"\d+")
ratio_search = re.compile(r"\d+")
gear_search = re.compile(r"[*]")
pn_id = 0
gear_id = 0
line_id = 0
pn_dict = {}
gear_dict = {}
solution = 0


def find_perimeter(line_id,line, pn_span):
    """Left, Right, Top, Bottom

    Parameters
    ----------
    line_id  : _type_
        _description_
    pn_span : _type_
        _description_
    """
    line = line
    left,right,top,bottom = (None,None,None,None)
    # Set up span of top and bottom perimeters to catch diagnals
    topbot_span = list(pn_span)
    topbot_span[0] -= 1
    topbot_span[1] += 1

    # Determine initial perimeter list indexes
    left_pos = pn_span[0] - 1
    right_pos = pn_span[1]
    top_pos = line_id - 1
    bottom_pos = line_id + 1

    # Test if perimeter is on the edge of the schematic 
    if left_pos < 0:          
        left_pos = None
        topbot_span[0] += 1

    try:                      
        line[right_pos]
    except IndexError:
        right_pos = None
        topbot_span[1] -= 1

    if top_pos < 0:  
        top_pos = None

    try:
        schematic_list[bottom_pos]
    except IndexError:
        bottom_pos = None

    # Determine the characters around the perimeter of the part number
    if left_pos:
        left = line[left_pos]

    if right_pos:
        right = line[right_pos]

    if top_pos != None:
        top = schematic_list[top_pos][topbot_span[0]:topbot_span[1]]

    if bottom_pos:
        bottom = schematic_list[bottom_pos][topbot_span[0]:topbot_span[1]]

    return (left,right,top,bottom)

def is_valid(perimeter):
    for side in perimeter:
        if side:
            if symbol_search.search(side):
                return True
    return False

def find_gear_ratio(line_id, gear_span, perimeter):

    # NOTE: I intentionally assumed that there wouldn't be more than 2 ratios unless this fails to find the answer.
    #   A quick look over the input file 
    ratios = []
    left,right,top,bottom = perimeter
    left_ratio,right_ratio,top_ratio,bottom_ratio = (None,None,None,None)

    if left:
        if left.isdigit():
            left_ratio = [pn_dict[id]["pn"] for id in pn_dict if gear_span[0] >= pn_dict[id]["pn_span"][0] and gear_span[0] == pn_dict[id]["pn_span"][1] and pn_dict[id]["pn_line"] == line_id][0]
            ratios.append(left_ratio)

    if right:
        if right.isdigit():
            right_ratio = [pn_dict[id]["pn"] for id in pn_dict if gear_span[1] == pn_dict[id]["pn_span"][0] and gear_span[1] <= pn_dict[id]["pn_span"][1] and pn_dict[id]["pn_line"] == line_id][0]
            ratios.append(right_ratio)

    if top:
        if ratio_search.search(top):
            top_ratio = [pn_dict[id]["pn"] for id in pn_dict if gear_span[0] <= pn_dict[id]["pn_span"][1] and gear_span[1] >= pn_dict[id]["pn_span"][0] and pn_dict[id]["pn_line"] == line_id-1]
            for r in top_ratio:
                ratios.append(r)

    if bottom:
        if ratio_search.search(bottom):
            bottom_ratio = [pn_dict[id]["pn"] for id in pn_dict if gear_span[0] <= pn_dict[id]["pn_span"][1] and gear_span[1] >= pn_dict[id]["pn_span"][0] and pn_dict[id]["pn_line"] == line_id+1]
            for r in bottom_ratio:
                ratios.append(r)

    return ratios


# Loop schematic to determine part number locations
for line in schematic_list:
    match_loc = (0,0)
    line_id = schematic_list.index(line)
    pn = part_number_search.search(line,match_loc[1])
    line_remaining = line[match_loc[0]:]
    while pn:
        match_loc = pn.span()
        pn_dict[pn_id] = {"pn":pn.group(0),
                             "pn_span": match_loc,
                             "pn_line": line_id,
                             "perimeter": find_perimeter(line_id,line_remaining, match_loc)}
        pn_dict[pn_id]["valid"] = is_valid(pn_dict[pn_id]["perimeter"])
        pn = part_number_search.search(line,match_loc[1])
        pn_id += 1

# Loop schematic to determine gear ratios
for line in schematic_list:
    match_loc = (0,0)
    line_id = schematic_list.index(line)
    gear = gear_search.search(line,match_loc[1])
    line_remaining = line[match_loc[0]:]
    while gear:
        match_loc = gear.span()
        gear_dict[gear_id] = {"gear_span": match_loc,
                             "gear_line": line_id,
                             "perimeter": find_perimeter(line_id, line_remaining, match_loc)}
        gear_dict[gear_id]["ratio"] = find_gear_ratio(line_id, match_loc, gear_dict[gear_id]["perimeter"])
        gear = gear_search.search(line,match_loc[1])
        gear_id += 1

for gear in gear_dict:
    if len(gear_dict[gear]["ratio"]) == 2:
        solution += int(gear_dict[gear]["ratio"][0]) * int(gear_dict[gear]["ratio"][1])

pprint(solution)