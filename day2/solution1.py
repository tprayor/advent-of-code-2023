import re
from pprint import pprint


#
# 1) organize the data into dict.
# Cube hands will be organized as red,blue,green pairs
#
data = open("./input.txt", "r")
game_id_search = re.compile(r"(?<=Game )\d+")
red_amount = re.compile(r"\d+(?= red)")
blue_amount = re.compile(r"\d+(?= blue)")
green_amount = re.compile(r"\d+(?= green)")
game_dict = dict()

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
    return (red,green,blue)

def find_solution(cube_input, constraints):
    constraints = constraints
    cube_input = cube_input
    cube_totals = [0,0,0]
    solution = []

    for hand in cube_input:
        if constraints[0] - hand[0] < 0
        

    for 



for game in data.readlines():
    # Capture game information
    entry, games = game.split(':')
    game_list = games.split(";")

    # build dict info for game
    game_id = int(game_id_search.search(entry).group(0))
    game_dict[game_id] = {'cube_grabs':list()}
    for game in game_list:
        game_dict[game_id]['cube_grabs'].append(find_cubes(game))

pprint(game_dict)
