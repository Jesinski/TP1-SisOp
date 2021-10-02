# -*- coding: utf-8 -*-

from dataclasses import dataclass
from random import seed
from random import randint
seed(1)

tempoGlobal = 0  # tempo total de simulação
admissao = []  # lista inicial de admissao de processos
prontos = []  # fila de processos prontos para execução
bloqueados = []  # fila de processos bloqueados
finalizados = []  # lista de processos finalizados
processador = []

@dataclass
class PCB:
    nome: str
    arrival: int
    pc: int = 0
    acc: float = 0.0
    estado: str = "admissao"
    waiting_time: int = 0
    processing_time: int = 0
    turnaround_time: int = 0
    prioridade: int = 2
    quantum: int = 0
    quantumAcc: int =  0
    tempo_bloqueado: int = 0

atual = PCB("placeholder", 1000)    
atual.estado = "running"
atual.prioridade = 500
atual.quantum = 100
atual.quantumAcc = 100

##################################################################################################################################

escolha = int(input("Digite '1' para usar o escalonador de Prioridade com Preempção, ou '2' para usar o escalonador de Round Robin com quantum definível: \n"))   
n_processos = int(input("Digite o número de processos que deseja carregar: \n"))  
jogar_fora = True

for i in range(n_processos):
    name = input("Digite o nome do processo {}: \n".format(i+1) )
    chegada = int(input("Digite o instante de tempo em que o processo entra no sistema (sai da fila de admissao para a fila de prontos): \n"))
    p = PCB(name, chegada)

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
    global prontos, atual, jogar_fora, processador

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
    global prontos, atual, jogar_fora, processador

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
    global atual, jogar_fora, finalizados, bloqueados, prontos, n_processos, processador

    if sys == 0:
        processador[0].estado = "finalizado"
        processador[0].turnaround_time = tempoGlobal - processador[0].arrival
        finalizados.append(processador[0])
        n_processos = n_processos - 1

    else:
        if sys == 1:
            print(processador[0].acc)
        else:
            processador[0].acc = float(input("Digite o valor que o acumulador deste processo receberá: \n"))    

        processador[0].tempo_bloqueado = randint(2, 4)
        processador[0].estado = "bloqueado"
        bloqueados.append(processador[0])

    processador.pop(0)    

 ##################################################################################################################################  

def executa():
    global atual

    processador[0].pc = processador[0].pc + 1     
    processador[0].processing_time = processador[0].processing_time + 1
    if escolha == 2: processador[0].quantumAcc = processador[0].quantumAcc + 1

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
        if processador[0].pc == 10:
            syscall(0)
        #else:
        #    sys = int(input("Digite a syscall. '1' para imprimir, '2' para leitura: \n"))
        #    syscall(sys)

    tempoGlobal = tempoGlobal + 1

##################################################################################################################################

print("Admissão: ", admissao, "\n")
print("Prontos: ", prontos, "\n")
print("Bloqueados ", bloqueados, "\n")
print("Finalizados: ", finalizados, "\n")
print("Tempo total de simulação: ", tempoGlobal, "\n")
