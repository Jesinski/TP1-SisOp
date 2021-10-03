#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dataclasses import dataclass

# Lookups to identify the code and data section


class Lookups:
    code = ".code\n"
    endcode = ".endcode\n"
    data = ".data\n"
    enddata = ".enddata"


@dataclass
class CodeLine:
    index: int
    command: str
    value: str
    isImmediate: bool


# Opening the file over and over again for sure is not the best way to do that, but it works for small cases
def getLineIndexOfLookup(source, lookup):
    lineIndex = source.index(lookup)
    return lineIndex


def getCodeCommandsList(program):
    codeList: list[CodeLine] = []

    codeIndex = getLineIndexOfLookup(program, Lookups.code)
    endcodeIndex = getLineIndexOfLookup(program, Lookups.endcode)
    codeSection: list[str] = program[codeIndex+1:endcodeIndex]

    currentIndex = 0
    for pos in range(len(codeSection)):
        codeSection[pos] = codeSection[pos].lstrip()
        codeSection[pos] = codeSection[pos].rstrip()
        lineArr = codeSection[pos].split(" ")
        if (len(lineArr) < 2):
            codeList.append(
                CodeLine(currentIndex, lineArr[0], currentIndex, False))
        else:
            isImmediate = True if lineArr[1].find("#") != -1 else False
            codeList.append(
                CodeLine(currentIndex, lineArr[0], lineArr[1], isImmediate))
        currentIndex = currentIndex + 1

    return codeList

# Get the program's data section, extract all key and value pairs representing variable names and values then return as a dictionary


def getVariableDictionary(program):
    dataIndex = getLineIndexOfLookup(program, Lookups.data)
    enddataIndex = getLineIndexOfLookup(program, Lookups.enddata)
    variables = {}
    dataSection = program[dataIndex+1:enddataIndex]
    for pos in range(len(dataSection)):
        dataSection[pos] = dataSection[pos].lstrip()
        dataSection[pos] = dataSection[pos].rstrip()
        lineArr = dataSection[pos].split(" ")
        variables[lineArr[0]] = lineArr[1]

    return variables

# debug


def main():

    # for sourceCodePath in ["./programs/prog1.txt", "./programs/prog2.txt", "./programs/prog3.txt"]:
    for sourceCodePath in ["./programs/prog1.txt", "./programs/prog2.txt", "./programs/prog3.txt"]:
        program = open(sourceCodePath, "r").readlines()

        # dataMemory = getVariableDictionary(program)
        # print(dataMemory)

        codeLines = getCodeCommandsList(program)
        print(codeLines)


if __name__ == "__main__":
    main()
