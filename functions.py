#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PCB import *

# Aritimético
def add(PCB: PCB, opt1):
    PCB.acc = PCB.acc + opt1
    return PCB

def sub(PCB: PCB, opt1):
    PCB.acc =  PCB.acc - opt1
    return PCB

def mult(PCB: PCB, opt1):
    PCB.acc =  PCB.acc*opt1
    return PCB

def div(PCB: PCB, opt1):
    PCB.acc = PCB.acc/opt1
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
    for x in PCB.sequencia_comandos:
        if (x.command == label+":"):
            PCB.pc = x.index + 1
            break
    return PCB

def brpos(PCB: PCB, label):
    if PCB.acc > 0:
        for x in PCB.sequencia_comandos:
            if (x.command == label+":"):
                PCB.pc = x.index + 1
                break
    else: PCB.pc = PCB.pc + 1        
    return PCB  

def brzero(PCB: PCB, label):
    if PCB.acc == 0:
        for x in PCB.sequencia_comandos:
            if (x.command == label+":"):
                PCB.pc = x.index + 1
                break
    else: PCB.pc = PCB.pc + 1         
    return PCB   

def brneg(PCB: PCB, label):
    if PCB.acc > 0:
        for x in PCB.sequencia_comandos:
            if (x.command == label+":"):
                PCB.pc = x.index + 1
                break
    else: PCB.pc = PCB.pc + 1          
    return PCB             


# debug
#def main():
  #  print("ok")


#if __name__ == "__main__":
 #   main()
