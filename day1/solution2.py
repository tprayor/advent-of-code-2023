import re

startingDigitSearch = re.compile(r"^(\d|one|two|three|four|five|six|seven|eight|nine)")
endingDigitSearch = re.compile(r"(\d|one|two|three|four|five|six|seven|eight|nine)$")
digitConversion = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0'
}
with open("input.txt", "r") as data:
    file = data.read()
    inputList = file.split("\n")
    outputList = []
    solution = 0

    for entry in inputList:
        count = 0
        capture = startingDigitSearch.findall(entry[:])
        while len(capture) == 0:
            count += 1
            capture = startingDigitSearch.findall(entry[count:])
        if capture[0].isdigit() == False:
            startingDigit = digitConversion[capture[0]]
        else:
            startingDigit = capture[0]

        count = 0
        capture = endingDigitSearch.findall(entry[:])
        while len(capture) == 0:
            count -= 1
            capture = endingDigitSearch.findall(entry[:count])
        if capture[0].isdigit() == False:
            endingDigit = digitConversion[capture[0]]
        else:
            endingDigit = capture[0]       

        formattedNumber = int(f"{startingDigit}{endingDigit}")
        outputList.append(formattedNumber)
    
    for entry in outputList:
        solution += entry

    print("Solution: ", solution)