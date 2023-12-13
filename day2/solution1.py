import re

#
# Organize the data into dict.
#   Cube hands will be organized as red,blue,green tuples
# Find solution based on constraints
#

data = open("./input.txt", "r")
game_id_search = re.compile(r"(?<=Game )\d+")
red_amount = re.compile(r"\d+(?= red)")
blue_amount = re.compile(r"\d+(?= blue)")
green_amount = re.compile(r"\d+(?= green)")
game_dict = dict()
solution = int()
cube_constraints = (12, 13, 14)


def find_cubes(game_input):
    try:
        red = int(red_amount.search(game_input).group(0))
    except:
        red = 0
    try:
        green = int(green_amount.search(game_input).group(0))
    except:
        green = 0
    try:
        blue = int(blue_amount.search(game_input).group(0))
    except:
        blue = 0
    return (red, green, blue)


def find_solution(cube_input, constraints):
    constraints = constraints
    cube_input = cube_input
    for hand in cube_input:
        if constraints[0] - hand[0] < 0:
            return False
        elif constraints[1] - hand[1] < 0:
            return False
        elif constraints[2] - hand[2] < 0:
            return False
    return True


for game in data.readlines():
    # Capture game information
    entry, games = game.split(":")
    game_list = games.split(";")

    # build dict info for game
    game_id = int(game_id_search.search(entry).group(0))
    game_dict[game_id] = {"cube_grabs": list()}
    for game in game_list:
        game_dict[game_id]["cube_grabs"].append(find_cubes(game))
        game_dict[game_id]["solution"] = find_solution(
            game_dict[game_id]["cube_grabs"], cube_constraints
        )

for game in game_dict:
    if game_dict[game]["solution"] == True:
        solution += game

print("Solution: ", solution)
