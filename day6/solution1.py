import re


class RaceCalc:
    """
    A class to represent toy boat race times
    ...

    Attributes
    ----------
    max_time : int
        The max time of the race. You can't go over this time amount
    winning_distance : int
        the distance to beat within the timelimit to win the race
    winning_times : list[tuple[str]]
        List of winning tuples signifying a winning posibility (hold_time, distance).

    """

    def __init__(self, max_time: int, winning_distance: int) -> None:
        self.max_time = max_time
        self.winning_distance = winning_distance
        self.winning_times = []
        for hold_time in range(self.max_time):
            if (max_time - hold_time) * hold_time > winning_distance:
                distance = (max_time - hold_time) * hold_time
                self.winning_times.append((hold_time, distance))
        pass

    def __repr__(self) -> str:
        pass

    def __str__(self) -> str:
        pass


def main():
    """
    Main function to execute the script logic.
    This one had such little input, that I just created it by hand
    """
    solution = 0

    race1 = RaceCalc(42, 308)
    race2 = RaceCalc(89, 1179)
    race3 = RaceCalc(91, 1291)
    race4 = RaceCalc(89, 1467)
    solution = (
        len(race1.winning_times)
        * len(race2.winning_times)
        * len(race3.winning_times)
        * len(race4.winning_times)
    )
    print("Solution: ", solution)
    pass


if __name__ == "__main__":
    main()
