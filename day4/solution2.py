import re

#
# Global Variables
#

# regex
card_id_search = re.compile(r"\d+")
number_search = re.compile(r"\d+")

# data model
card_dict = {}


def gather_matches(user_numbers: list, scratch_numbers: list):
    """Determine the number of matches on a card

    Parameters
    ----------
    user_numbers : list
        Numbers provided to user for matching
    scratch_numbers : list
        Winning numbers scratched off of a card

    Returns
    -------
    list
        A list of matched numbers
    """
    matches = []
    for number in user_numbers:
        if number in scratch_numbers:
            matches.append(number)
    return matches


def find_points(matches: list):
    """Determine how many points a card is worth.

    Parameters
    ----------
    matches : list
        The matched numbers on a card

    Returns
    -------
    int
        Point total
    """
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


def find_card_count(card_id, match_count, card_count):
    count = 0
    while count < match_count:
        card_id += 1
        count += 1
        card_dict[card_id]["card_count"] += card_count
    pass


def main():
    """Main function to execute the script logic."""

    data = open("./input.txt", "r")
    cards_list = data.readlines()
    solution = 0

    # organize data into dict.
    for card in cards_list:
        # gather data
        card_beginning, scratch_numbers = card.split("|")
        card_number, user_numbers = card_beginning.split(":")
        card_id = int(card_id_search.search(card_number).group(0))
        user_numbers_list = number_search.findall(user_numbers)
        scratch_numbers_list = number_search.findall(scratch_numbers)

        card_dict[card_id] = {
            "user_numbers": user_numbers_list,
            "scratch_numbers": scratch_numbers_list,
            "card_count": 1,
        }

        card_dict[card_id]["number_matches"] = gather_matches(
            card_dict[card_id]["user_numbers"], card_dict[card_id]["scratch_numbers"]
        )
        card_dict[card_id]["points"] = find_points(card_dict[card_id]["number_matches"])

    # gather card counts
    for card in card_dict:
        count = card_dict[card]["card_count"]
        matches = len(card_dict[card]["number_matches"])
        find_card_count(card, matches, count)

    # find solution
    for card in card_dict:
        solution += card_dict[card]["card_count"]

    print("Solution: ", solution)


if __name__ == "__main__":
    main()
