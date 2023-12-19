import re

#
# Global Variables
#

# input
data = open("./input.txt", "r")
garden_mappings = data.read()
# data model
garden_dict = {"maps": {}, "seeds": []}


class GardenMap:
    """
    A class to represent garden mappings
    ...

    Attributes
    ----------
    garden_map : dict (class attribute)
        Container to hold mapping information so different mappings can can pass data between each other.
    name : str
        Name of the mapping
    source : str
        Source input for mapping. For example, "seeds" in the "seeds-to-soil" mapping.
    dest : str
        Destination output for mapping. For example, "soil" in the "seeds-to-soil" mapping.
    mappings : list[list[str]]
        List of lists with three entires denoting [destionation_starting_int, source_starting_int, mapping_range].


    Methods
    -------
    map_input(additional=""):
        Prints the person's name and age.
    """

    garden_map = {}
    mapping_search = re.compile(r"\d+")

    def __init__(self, name: str, mappings: list) -> None:
        self.mapping_search = re.compile(r"\d+")
        self.name = name
        self.source, self.dest = self.name.split("-to-")
        self.mappings = []

        individual_maps_list = mappings.split("\n")
        for mapping in individual_maps_list:
            self.mappings.append(GardenMap.mapping_search.findall(mapping))

        GardenMap.garden_map[self.name] = {
            "source": self.source,
            "destination": self.dest,
            "mappings": self.mappings,
        }
        pass

    def map_input(self, source_input: int, mappings: list = None, dest: str = None):
        """A recursive method that determines what a given input value matches to in this
          garden mapping instance. If this GardenMap instance is not the "humidity-to-location"
          mapping, it will continue to recursively call itself until it returns a location
          as required by the challenge.

        Parameters
        ----------
        source_input : int
            Value of the source input. In the challenge, this is a "seed" value being input
            into the "seed-to-soil" mapping, but you can use any mapping you like as long as all
            of the mapping have been created in the class.
        mappings : list, optional
            List of lists with three entires denoting [destionation_starting_int, source_starting_int, mapping_range].
            If no list is provided, map_input will use local mappings attribute.
        dest : str, optional
            The destination mapping to send the output if not at the final "location" mapping.
            If no destination is provided, map_input will use the local dest attribute.

        Returns
        -------
        int
            the location of the initial input

        self.map_input()
            when additional mappings are required.
        """
        # set variables
        if mappings is None:
            mappings = self.mappings
        if dest is None:
            dest = self.dest

        for mapping in mappings:
            dest_range_start = int(mapping[0])
            src_range_start = int(mapping[1])
            map_range = int(mapping[2])

            # test if source_input is within source range
            if src_range_start + map_range > source_input >= src_range_start:
                output = (
                    src_range_start
                    - (src_range_start - dest_range_start)
                    + (source_input - src_range_start)
                )
                break
            else:
                output = source_input

        # test for final mapping
        if dest == "location":
            return output
        else:
            # pass final output on to next mapping
            for mapping in GardenMap.garden_map:
                if GardenMap.garden_map[mapping]["source"] == dest:
                    return self.map_input(
                        output,
                        GardenMap.garden_map[mapping]["mappings"],
                        GardenMap.garden_map[mapping]["destination"],
                    )

    def __repr__(self) -> str:
        return f"Mapping Name: {self.name}, Mappings: {self.mappings}"

    def __str__(self) -> str:
        return f"Mapping Name: {self.name}, Mappings: {self.mappings}"


def main():
    """Main function to execute the script logic."""
    solution = []
    seperated_mappings = re.split("\n\n", garden_mappings)

    # gather seed values
    seed_values = seperated_mappings.pop(0).split(": ")[1]
    garden_dict["seeds"] = seed_values.split(" ")
    # gather mappings
    for mapping in seperated_mappings:
        mapping_name, mappings = mapping.split(" map:\n")
        garden_dict["maps"][mapping_name] = GardenMap(mapping_name, mappings)

    for seed in garden_dict["seeds"]:
        solution.append(garden_dict["maps"]["seed-to-soil"].map_input(int(seed)))

    print(f"Solution: {min(solution)}")
    pass


if __name__ == "__main__":
    main()
