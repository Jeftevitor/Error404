import pygame
from Class.receptor import Receptor

class Sinc:
    def __init__(self,jogo):
        self.receptores = []

        self.receptores.append(Receptor (jogo.seta_esquerda.x, jogo.seta_esquerda.y, 'esquerda' )) 
        self.receptores.append(Receptor (jogo.seta_baixo.x, jogo.seta_baixo.y, 'baixo' )) 
        self.receptores.append(Receptor (jogo.seta_cima.x, jogo.seta_cima.y, 'cima' )) 
        self.receptores.append(Receptor (jogo.seta_direita.x, jogo.seta_direita.y, 'direita' ))