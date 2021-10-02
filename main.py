#!/usr/bin/env python3

def main():
   
    for sourceCodePath in ["./programs/prog1.txt", "./programs/prog2.txt", "./programs/prog3.txt"]:
        program = open(sourceCodePath, "r").readlines()

        # Lookups to identify the code and data section
        class Lookups:
            code = ".code\n"
            endcode = ".endcode\n"
            data = ".data\n"
            enddata = ".enddata"
        
        # Lines beloging to the code and the data
        class Indexes:
            code = -1
            endcode = -1
            data = -1
            enddata = -1

        dataMemory = loadDataIntoMemory(getLineIndexOfLookup(sourceCodePath, Lookups.data), getLineIndexOfLookup(sourceCodePath, Lookups.enddata), program)
        print(dataMemory)
    

# Opening the file over and over again for sure is not the best way to do that, but it works for small cases
def getLineIndexOfLookup(sourcePath, lookup):
    with open(sourcePath, "r") as f: data = f.readlines()
    lineIndex = data.index(lookup)
    return lineIndex

# Get the program's data section, extract all key and value pairs representing variable names and values then return as a dictionary
def loadDataIntoMemory(dataIndex, enddataIndex, program):
    variables = {}
    dataSection = program[dataIndex+1:enddataIndex]
    for pos in range(len(dataSection)):
        dataSection[pos] = dataSection[pos].lstrip()
        dataSection[pos] = dataSection[pos].rstrip()
        lineArr = dataSection[pos].split(" ")
        variables[lineArr[0]] = lineArr[1]
    
    return variables



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()