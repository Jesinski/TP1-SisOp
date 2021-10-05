#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from random import seed
from random import randint
from data import *
from PCB import *
from functions import *
seed(1)

tempoGlobal = 0  # tempo total de simulação
admissao = []  # lista inicial de admissao de processos
prontos = []  # fila de processos prontos para execução
bloqueados = []  # fila de processos bloqueados
finalizados = []  # lista de processos finalizados
processador = []



##################################################################################################################################

escolha = int(input("Digite '1' para usar o escalonador de Prioridade com Preempção, ou '2' para usar o escalonador de Round Robin com quantum definível: \n"))
n_processos = int(input("Digite o número de processos que deseja carregar: \n"))  

for i in range(n_processos):
# Procurar pelo nome do programa
    validPCB = False
    program: list
    while not validPCB:
        name = input("Digite o nome do processo (arquivo + extensão) {}: \n".format(i+1) )
        try:
            program = open("./programs/"+name, "r").readlines()
            validPCB = True
            break
        except:
            print("Nome de arquivo inválido.\nO arquivo deverá estar na pasta \"./programs\"\n")
    
    chegada = int(input("Digite o instante de tempo em que o processo entra no sistema (sai da fila de admissao para a fila de prontos): \n"))
    dicionario_variaveis = getVariableDictionary(program)
    comandos = getCodeCommandsList(program)
    p = PCB(name, chegada, dicionario_variaveis, comandos, program)

    if escolha == 1:
        prio = int(input("Digite o nível de prioridade deste processo, entre 0, 1 e 2. O padrão é baixa (2). \n"))
        p.prioridade = prio
    else:
        quan = int(input("Digite o quantum (tempo de execução por estadia no processador) para este processo. Deve ser maior que 0. \n"))
        p.quantum = quan

    admissao.append(p)

for processo in admissao:
    print(processo, "\n")
  
##################################################################################################################################

def escalonadorPrioridade(): 
    global prontos, processador

    prontos.sort(key=lambda x: x.prioridade, reverse=False)

    for p in prontos:
        if p.prioridade < processador[0].prioridade:
            aux = p
            prontos.remove(p) 
            aux.estado = "running"
            processador[0].estado = "pronto"
            prontos.append(processador[0])
            processador[0] = aux
            

def  escalonadorRoundRobin():
    global prontos, processador

    if processador[0].quantumAcc >= processador[0].quantum:
        if prontos != []:
            aux = prontos.pop(0)
            aux.estado = "running"
            processador[0].quantumAcc = 0
            processador[0].estado = "pronto"
            prontos.append(processador[0])
            processador[0] = aux

        
 ##################################################################################################################################     
     
def syscall(sys):
    global finalizados, bloqueados, prontos, n_processos, processador

    if sys == 0:
        processador[0].estado = "finalizado"
        processador[0].turnaround_time = tempoGlobal - processador[0].arrival
        finalizados.append(processador[0])
        n_processos = n_processos - 1

    else:
        if sys == 1:
            print("O valor do ACC deste processo é: ",processador[0].acc, "\n")
        else:
            processador[0].acc = int(input("Digite o valor que o acumulador deste processo receberá: \n"))    

        processador[0].tempo_bloqueado = randint(10, 20)
        processador[0].estado = "bloqueado"
        bloqueados.append(processador[0])

    processador.pop(0)    

 ##################################################################################################################################  

def executa():
    global processador
    #consome a linha

    p = processador[0]
    pc = p.pc
    opt1 = p.sequencia_comandos[pc].value
    comando = p.sequencia_comandos[pc].command
    imediato = p.sequencia_comandos[pc].isImmediate

    if comando != "syscall":
        if comando[:2] != "BR":
            if (comando == "add") and (imediato == True): # Adição
                p = add(p, int(opt1[1:]))

            elif (comando == "add") and (imediato == False):
                opt1 = int(p.variaveis.get(opt1))
                p = add(p, opt1)  

            elif (comando == "sub") and (imediato == True): # Subtração
                p = sub(p, int(opt1[1:]))

            elif (comando == "sub") and (imediato == False):
                opt1 = int(p.variaveis.get(opt1))
                p = sub(p, opt1)     

            elif (comando == "mult") and (imediato == True): # Multiplicação
                p = mult(p, int(opt1[1:]))

            elif (comando == "mult") and (imediato == False):
                opt1 = int(p.variaveis.get(opt1))
                p = mult(p, opt1) 

            elif (comando == "div") and (imediato == True): # Divisão
                p = div(p, int(opt1[1:]))

            elif (comando == "div") and (imediato == False):
                opt1 = int(p.variaveis.get(opt1))
                p = div(p, opt1)         

            elif (comando == "load") and (imediato == True): # Load
                p = load(p, int(opt1[1:]))    
                
            elif (comando == "load") and (imediato == False):
                opt1 = int(p.variaveis.get(opt1))
                p = load(p, opt1)  
                
            elif comando == "store":   # Store
                    p = store(p, opt1) 
            p.pc = p.pc + 1

        else:       
            
            if comando == "BRANY":
                p = brany(p, opt1) 

            elif comando == "BRPOS":
                p = brpos(p, opt1)    

            elif comando == "BRZERO":
                p = brzero(p, opt1)  

            else:  p = brneg(p, opt1)
                             
        p.processing_time = p.processing_time + 1
        if escolha == 2: p.quantumAcc = p.quantumAcc + 1    
        processador[0] = p

    else:
        if opt1 == "0": syscall(0)  
        elif opt1 == "1": syscall(1)
        else: syscall(2)    
    

################################################################################################################################## 
def printProcesso(p):
    print(" Nome: ",p.nome)
    print(" Arrival: ",p.arrival)
    print(" Variaveis: ",p.variaveis)
    print(" PC: ",p.pc)
    print(" ACC: ",p.acc)
    print("Estado: ",p.estado)
    print(" Waiting Time: ",p.waiting_time)
    print(" Processing Time: ",p.processing_time)
    print(" Turnaround Time: ",p.turnaround_time)
    print(" Prioridade: ",p.prioridade)
    print(" Quantum: ",p.quantum)
    print(" QuantumAcc: ",p.quantumAcc)
    print(" Tempo para desbloquear: ",p.tempo_bloqueado)
##################################################################################################################################    

while n_processos > 0:

    for c in prontos:
        c.waiting_time = c.waiting_time + 1

    for a in admissao:
        if a.arrival == tempoGlobal:
            j = a
            admissao.remove(a)
            j.estado = "pronto"
            prontos.append(j)
           
    for b in bloqueados:
        b.tempo_bloqueado = b.tempo_bloqueado - 1
        if b.tempo_bloqueado == 0:    
            i = b
            bloqueados.remove(b)
            i.estado = "pronto"
            i.pc = i.pc + 1
            prontos.append(i)     

    print("Antigo atual: \n", processador, "\n")

    if processador == []:
        if prontos != []:
            if escolha == 1:
                prontos.sort(key=lambda x: x.prioridade, reverse=False)
            processador.append(prontos.pop(0))
            processador[0].estado = "running"

    elif escolha == 1:
        escalonadorPrioridade()
    else:
        escalonadorRoundRobin()

    print("Novo atual: \n", processador, "\n")    

    if processador != []: 
        executa()

    tempoGlobal = tempoGlobal + 1

##################################################################################################################################

print("Admissão: ", admissao, "\n")
print("Prontos: ", prontos, "\n")
print("Bloqueados ", bloqueados, "\n")
print("Finalizados: \n")
for p in finalizados:
    printProcesso(p)
    print("\n")
print("Tempo total de simulação: ", tempoGlobal, "\n")
