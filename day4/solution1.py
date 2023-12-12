import re
from pprint import pprint


#
# organize data into dict.
#

data = open("./input.txt", "r")
cards_list = data.readlines()
card_id_search = re.compile(r"\d+")
number_search = re.compile(r"\d+")
card_dict = {}
solution = 0

def gather_matches(user_numbers, scratch_numbers):
    matches = []
    for number in user_numbers:
        if number in scratch_numbers:
            matches.append(number)
    return matches

def find_points(matches):
    win_count = len(matches)
    count = 0
    points = 0
    while count != win_count:
        if points == 0:
            points += 1
        else:
            points *= 2
        count += 1
    return points


for card in cards_list:
    #gather data
    card_beginning,scratch_numbers = card.split("|")
    card_number, user_numbers = card_beginning.split(":")
    card_id = card_id_search.search(card_number).group(0)
    user_numbers_list = number_search.findall(user_numbers)
    scratch_numbers_list = number_search.findall(scratch_numbers)

    card_dict[card_id] = {
        "user_numbers":user_numbers_list,
        "scratch_numbers":scratch_numbers_list}
    
    card_dict[card_id]["number_matches"] = gather_matches(card_dict[card_id]["user_numbers"], card_dict[card_id]["scratch_numbers"])
    card_dict[card_id]["points"] = find_points(card_dict[card_id]["number_matches"])

pprint(card_dict)


for card in card_dict:
    solution += card_dict[card]["points"]

print("Solution: ", solution)