from dataclasses import dataclass
from data import *

@dataclass
class PCB:
    nome: str
    arrival: int
    variaveis: dict
    sequencia_comandos: list[CodeLine]
    program: str
    pc: int = 0
    acc: int = 0
    estado: str = "admissao"
    waiting_time: int = 0
    processing_time: int = 0
    turnaround_time: int = 0
    prioridade: int = 2
    quantum: int = 0
    quantumAcc: int =  0
    tempo_bloqueado: int = 0
    