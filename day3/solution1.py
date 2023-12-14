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
# data model
pn_dict = {}


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


def main():
    """Main function to execute the script logic."""

    pn_id = 0
    line_id = 0
    solution = 0

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

    for part in pn_dict:
        if pn_dict[part]["valid"] == True:
            solution += int(pn_dict[part]["pn"])

    pprint(solution)


if __name__ == "__main__":
    main()
