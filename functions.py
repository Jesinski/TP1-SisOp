#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from OS import PCB

# Aritimético
def add(PCB: PCB, opt1):
    PCB.acc+opt1
    return PCB


def sub(PCB: PCB, opt1):
    PCB.acc-opt1
    return PCB


def mult(PCB: PCB, opt1):
    PCB.acc*opt1
    return PCB


def div(PCB: PCB, opt1):
    PCB.acc/opt1
    return PCB

# Memórias
def load(PCB: PCB, opt1):
    PCB.acc = opt1
    return PCB

def store(PCB: PCB, opt1):
    PCB.variaveis[opt1] = PCB.acc
    return PCB

# Salto
def brany(PCB: PCB, label):
    newPC = -1
    for x in range(PCB.sequencia_comandos):
        if (x.command == label+":"):
            newPC = x.value
            break
        
    PCB.pc = newPC
    return PCB


# debug
def main():
    print("ok")


if __name__ == "__main__":
    main()
