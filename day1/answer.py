
with open("input.txt", "r") as data:
    inputList = data.read().split("\n")
    outputList = []
    numberList = []
    solution = 0

    for entry in inputList:
        formattedOuput = ""
        for char in list(entry):
            if char.isdigit() == True:
                formattedOuput += char
        outputList.append(formattedOuput)
    
    for entry in outputList:
        trimmedNumber = int(f"{entry[0]}{entry[-1]}")
        solution += trimmedNumber

    print("Solution 1: " ,solution)