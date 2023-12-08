import re
from pprint import pprint


data = open("./input.txt", "r")
schematic_list = data.readlines()
symbol_search = re.compile(r"[#$%&*+\-/=@]")
part_number_search = re.compile(r"\d+")
pn_id = 0
line_id = 0
pn_dict = {}
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

    if top_pos:
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

        pn = part_number_search.search(line,match_loc[1]+1)
        pn_id += 1

for part in pn_dict:
    if pn_dict[part]["valid"] == True:
        solution += int(pn_dict[part]["pn"])

pprint(solution)