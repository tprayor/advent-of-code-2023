import re
from pprint import pprint

#
# Global Variables
#

# input
data = open("./input.txt", "r")
schematic_list = data.readlines()
# regex
symbol_search = re.compile(r"[#$%&*+\-/=@]")
part_number_search = re.compile(r"\d+")
ratio_search = re.compile(r"\d+")
gear_search = re.compile(r"[*]")
# data model
pn_dict = {}
gear_dict = {}


def find_perimeter(line_id: int, line: str, pn_span: tuple):
    """_summary_

    Parameters
    ----------
    line_id : int
        the line number for where the part number resides.
    line : str
        the portion of line to search. Since re.search() only brings back a
        single match, I crop the line to search to the character after the
        previous match
    pn_span : tuple
        start and end coordinates (A,Z) for the found part number within
        the full line.

    Returns
    -------
    tuple
        tuple containing the left, right, top and bottom perimeters
    """
    line = line
    left, right, top, bottom = (None, None, None, None)
    # set up span of top and bottom perimeters to catch diagnals
    topbot_span = list(pn_span)
    topbot_span[0] -= 1
    topbot_span[1] += 1

    # determine initial perimeter list indexes
    left_pos = pn_span[0] - 1
    right_pos = pn_span[1]
    top_pos = line_id - 1
    bottom_pos = line_id + 1

    # test if part number is on the edges of the schematic
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

    # determine the characters around the perimeter of the part number
    if left_pos:
        left = line[left_pos]

    if right_pos:
        right = line[right_pos]

    if top_pos is not None:
        top = schematic_list[top_pos][topbot_span[0] : topbot_span[1]]

    if bottom_pos:
        bottom = schematic_list[bottom_pos][topbot_span[0] : topbot_span[1]]

    return (left, right, top, bottom)


def is_valid(perimeter: tuple):
    """determine if the part number is valid

    Parameters
    ----------
    perimeter : tuple
        the left, right, top, and bottom perimeters.

    Returns
    -------
    Boolean
        True if symbol_search finds a valid character in perimeter
    """
    for side in perimeter:
        if side:
            if symbol_search.search(side):
                return True
    return False


def find_gear_ratio(line_id: int, gear_span: tuple, perimeter: tuple):
    """Find valid gear ratios.

    Parameters
    ----------
    line_id : int
        Number of the line where the gear ratio exists
    gear_span : tuple
        Starting and ending span of the gear (A,Z)
    perimeter : tuple
        the perimeter characters around the gear as (left, right, top, bottom)

    Returns
    -------
    list
        list of all valid ratios for the current gear
    """
    ratios = []
    left, right, top, bottom = perimeter
    left_ratio, right_ratio, top_ratio, bottom_ratio = (None, None, None, None)

    # If a perimeter edge is a valid gear, add to ratios list
    if left:
        if left.isdigit():
            left_ratio = [
                pn_dict[id]["pn"]
                for id in pn_dict
                if gear_span[0] >= pn_dict[id]["pn_span"][0]
                and gear_span[0] == pn_dict[id]["pn_span"][1]
                and pn_dict[id]["pn_line"] == line_id
            ][0]
            ratios.append(left_ratio)

    if right:
        if right.isdigit():
            right_ratio = [
                pn_dict[id]["pn"]
                for id in pn_dict
                if gear_span[1] == pn_dict[id]["pn_span"][0]
                and gear_span[1] <= pn_dict[id]["pn_span"][1]
                and pn_dict[id]["pn_line"] == line_id
            ][0]
            ratios.append(right_ratio)

    # top and bottom perimeters can have two or more valid ratios returned
    if top:
        if ratio_search.search(top):
            top_ratio = [
                pn_dict[id]["pn"]
                for id in pn_dict
                if gear_span[0] <= pn_dict[id]["pn_span"][1]
                and gear_span[1] >= pn_dict[id]["pn_span"][0]
                and pn_dict[id]["pn_line"] == line_id - 1
            ]
            for r in top_ratio:
                ratios.append(r)

    if bottom:
        if ratio_search.search(bottom):
            bottom_ratio = [
                pn_dict[id]["pn"]
                for id in pn_dict
                if gear_span[0] <= pn_dict[id]["pn_span"][1]
                and gear_span[1] >= pn_dict[id]["pn_span"][0]
                and pn_dict[id]["pn_line"] == line_id + 1
            ]
            for r in bottom_ratio:
                ratios.append(r)

    return ratios


def main():
    """Main function to execute the script logic."""

    pn_id = 0
    gear_id = 0
    line_id = 0
    solution = 0

    # Loop schematic to determine part number locations
    for line in schematic_list:
        match_loc = (0, 0)
        line_id = schematic_list.index(line)
        pn = part_number_search.search(line, match_loc[1])
        line_remaining = line[match_loc[0] :]
        while pn:
            match_loc = pn.span()
            pn_dict[pn_id] = {
                "pn": pn.group(0),
                "pn_span": match_loc,
                "pn_line": line_id,
                "perimeter": find_perimeter(line_id, line_remaining, match_loc),
            }
            pn_dict[pn_id]["valid"] = is_valid(pn_dict[pn_id]["perimeter"])

            pn = part_number_search.search(line, match_loc[1] + 1)
            pn_id += 1

    # Loop schematic to determine gear ratios
    for line in schematic_list:
        match_loc = (0, 0)
        line_id = schematic_list.index(line)
        gear = gear_search.search(line, match_loc[1])
        line_remaining = line[match_loc[0] :]
        while gear:
            match_loc = gear.span()
            gear_dict[gear_id] = {
                "gear_span": match_loc,
                "gear_line": line_id,
                "perimeter": find_perimeter(line_id, line_remaining, match_loc),
            }
            gear_dict[gear_id]["ratio"] = find_gear_ratio(
                line_id, match_loc, gear_dict[gear_id]["perimeter"]
            )
            gear = gear_search.search(line, match_loc[1])
            gear_id += 1

    for gear in gear_dict:
        if len(gear_dict[gear]["ratio"]) == 2:
            solution += int(gear_dict[gear]["ratio"][0]) * int(
                gear_dict[gear]["ratio"][1]
            )

    pprint(solution)


if __name__ == "__main__":
    main()
